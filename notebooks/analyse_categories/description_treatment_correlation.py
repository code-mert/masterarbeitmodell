import os
import sys
import json
import ast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr, pearsonr

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from scripts.create_f1_heatmap_excel import (
    GT1_PATH, GT2_PATH, ZERO_PATH, FEW_PATH, TWO_PATH,
    set_f1, best_path_f1, map_level_2, map_level_3
)
from wundtyp_mapping_dictionary import map_wundtyp_explicit
from lokalisation_mapping_dictionary import map_lokalisation_explicit
from exsudat_mapping_dictionary import map_exsudat_explicit
from primaerverband_calc import safe_parse_set

IMAGE_IDS = [f"wunde_{i+1:02d}" for i in range(60)]
FS_PROMPT_WOUNDS = ["wunde_04", "wunde_18"]

# Ordinal distances for Exsudatmenge
EXSUDAT_MAP = {
    "keine": 0, "gering": 1, "leicht": 1, "mäßig": 2, "stark": 3
}

def safe_parse_set_lower(val):
    s = safe_parse_set(val)
    return {x.lower().strip() for x in s if str(x).strip() != ""}


def exsudat_ordinal_score(val_gt, val_pred):
    s_gt = map_exsudat_explicit(val_gt).lower().strip()
    s_pred = map_exsudat_explicit(val_pred).lower().strip()
    
    if s_gt not in EXSUDAT_MAP or s_pred not in EXSUDAT_MAP:
        return 1.0 if s_gt == s_pred else 0.0
    dist = abs(EXSUDAT_MAP[s_gt] - EXSUDAT_MAP[s_pred])
    return max(0.0, 1.0 - (dist / 3.0))


def calculate_single_wound_description_score(row_gt, row_pred, scope="all"):
    """
    Calculates mapped Wundbeschreibung score on [0, 1] matching category calculation scripts.
    scope: 'all' (8 Merkmale), 'exsudat_infektion' (nur Exsudat + Infektion).
    """
    if scope == "exsudat_infektion":
        ex_gt = row_gt.get("exsudat")
        ex_pred = row_pred.get("exsudat_menge") if "exsudat_menge" in row_pred else row_pred.get("exsudat")
        s_ex = exsudat_ordinal_score(ex_gt, ex_pred)

        inf_gt = safe_parse_set_lower(row_gt.get("infektion"))
        inf_pred = safe_parse_set_lower(row_pred.get("infektion_vorhanden") if "infektion_vorhanden" in row_pred else row_pred.get("infektion"))
        s_inf = set_f1(inf_gt, inf_pred)

        return (s_ex + s_inf) / 2.0

    scores = []
    
    # 1. Wundtyp (Mapped via map_wundtyp_explicit)
    wt_gt = safe_parse_set_lower(map_wundtyp_explicit(row_gt.get("wundtyp")))
    wt_pred = safe_parse_set_lower(map_wundtyp_explicit(row_pred.get("wundtyp")))
    scores.append(set_f1(wt_gt, wt_pred))

    # 2. Lokalisation (Mapped via map_lokalisation_explicit)
    lok_gt = safe_parse_set_lower(map_lokalisation_explicit(row_gt.get("lokalisation")))
    lok_pred = safe_parse_set_lower(map_lokalisation_explicit(row_pred.get("lokalisation")))
    scores.append(set_f1(lok_gt, lok_pred))

    # 3. Wundstadium
    st_gt = safe_parse_set_lower(row_gt.get("wundstadium"))
    st_pred = safe_parse_set_lower(row_pred.get("wundstadium"))
    scores.append(set_f1(st_gt, st_pred))

    # 4. Wundrand
    ra_gt = safe_parse_set_lower(row_gt.get("wundrand"))
    ra_pred = safe_parse_set_lower(row_pred.get("wundrand"))
    scores.append(set_f1(ra_gt, ra_pred))

    # 5. Wundumgebung
    um_gt = safe_parse_set_lower(row_gt.get("wundumgebung"))
    um_pred = safe_parse_set_lower(row_pred.get("wundumgebung"))
    scores.append(set_f1(um_gt, um_pred))

    # 6. Exsudatmenge (Mapped via map_exsudat_explicit)
    ex_gt = row_gt.get("exsudat")
    ex_pred = row_pred.get("exsudat_menge") if "exsudat_menge" in row_pred else row_pred.get("exsudat")
    scores.append(exsudat_ordinal_score(ex_gt, ex_pred))

    # 7. Infektionsstatus
    inf_gt = safe_parse_set_lower(row_gt.get("infektion"))
    inf_pred = safe_parse_set_lower(row_pred.get("infektion_vorhanden") if "infektion_vorhanden" in row_pred else row_pred.get("infektion"))
    scores.append(set_f1(inf_gt, inf_pred))

    # 8. Debridement notwendig
    deb_gt = safe_parse_set_lower(row_gt.get("debridement_notwendig"))
    deb_pred = safe_parse_set_lower(row_pred.get("debridement_notwendig"))
    scores.append(set_f1(deb_gt, deb_pred))

    return sum(scores) / len(scores)


def load_dataset_scores(expert_mode=1, pv_level=1, scope="all"):
    """
    Loads paired (Wundbeschreibung_Score, Primärverband_F1) for all 3 AI models.
    expert_mode: 1 (Experte 1), 2 (Experte 2), or 'consensus' (Best of Both).
    pv_level: 1 (Level 1 Produkt-Ebene).
    scope: 'all' (8 Merkmale) or 'exsudat_infektion'.
    """
    df_gt1 = pd.read_csv(GT1_PATH, sep=";")
    df_gt2 = pd.read_csv(GT2_PATH, sep=";")
    df_zero = pd.read_csv(ZERO_PATH, sep=",")
    df_few = pd.read_csv(FEW_PATH, sep=",")
    df_two = pd.read_csv(TWO_PATH, sep=",")

    models = [
        ("Zero-Shot", df_zero, False),
        ("Few-Shot", df_few, True),
        ("Two-Stage", df_two, False)
    ]

    results = {}

    for name, df_ki, exclude_fs in models:
        desc_list = []
        pv_list = []
        wound_ids = []

        for img_id in IMAGE_IDS:
            if exclude_fs and img_id in FS_PROMPT_WOUNDS:
                continue
            if img_id not in df_ki["image_id"].values:
                continue

            r1 = df_gt1[df_gt1["image_id"] == img_id].iloc[0].to_dict() if len(df_gt1[df_gt1["image_id"] == img_id]) > 0 else {}
            r2 = df_gt2[df_gt2["image_id"] == img_id].iloc[0].to_dict() if len(df_gt2[df_gt2["image_id"] == img_id]) > 0 else {}
            rk = df_ki[df_ki["image_id"] == img_id].iloc[0].to_dict()

            e1_p_raw = safe_parse_set(r1.get("praeferenz_produkt"))
            e1_a_raw = safe_parse_set(r1.get("alternative_produkt"))
            e2_p_raw = safe_parse_set(r2.get("praeferenz_produkt"))
            e2_a_raw = safe_parse_set(r2.get("alternative_produkt"))
            ki_p_raw = safe_parse_set(rk.get("praeferenz_wundauflage"))
            ki_a_raw = safe_parse_set(rk.get("alternativ_wundauflage"))

            if pv_level == 2:
                e1_p, e1_a = map_level_2(e1_p_raw), map_level_2(e1_a_raw)
                e2_p, e2_a = map_level_2(e2_p_raw), map_level_2(e2_a_raw)
                ki_p, ki_a = map_level_2(ki_p_raw), map_level_2(ki_a_raw)
            else:
                e1_p, e1_a = e1_p_raw, e1_a_raw
                e2_p, e2_a = e2_p_raw, e2_a_raw
                ki_p, ki_a = ki_p_raw, ki_a_raw

            e1_empty = (not e1_p and not e1_a)
            e2_empty = (not e2_p and not e2_a)
            ki_empty = (not ki_p and not ki_a)

            if expert_mode == 1 and (e1_empty or ki_empty):
                continue
            if expert_mode == 2 and (e2_empty or ki_empty):
                continue
            if expert_mode == "consensus" and ((e1_empty and e2_empty) or ki_empty):
                continue

            s_desc_e1 = calculate_single_wound_description_score(r1, rk, scope=scope) if r1 else 0.0
            s_desc_e2 = calculate_single_wound_description_score(r2, rk, scope=scope) if r2 else 0.0

            s_pv_e1 = best_path_f1(ki_p, ki_a, e1_p, e1_a)
            s_pv_e2 = best_path_f1(ki_p, ki_a, e2_p, e2_a)

            if expert_mode == 1:
                final_desc = s_desc_e1
                final_pv = s_pv_e1
            elif expert_mode == 2:
                final_desc = s_desc_e2
                final_pv = s_pv_e2
            else:
                final_desc = max(s_desc_e1, s_desc_e2)
                final_pv = max(s_pv_e1, s_pv_e2)

            desc_list.append(final_desc * 100.0)
            pv_list.append(final_pv * 100.0)
            wound_ids.append(img_id)

        rho, p_rho = spearmanr(desc_list, pv_list)
        r_val, p_r = pearsonr(desc_list, pv_list)

        results[name] = {
            "x": desc_list,
            "y": pv_list,
            "wound_ids": wound_ids,
            "rho": rho,
            "p_rho": p_rho,
            "r": r_val,
            "p_r": p_r
        }

    return results


def plot_description_treatment_scatterplots(expert_id=1, pv_level=1, scope="all", save_path=None):
    """
    Renders 3-subplot scatterplot comparing Wundbeschreibung Score vs Primärverband F1 using mapped categories.
    scope: 'all' (8 Merkmale) or 'exsudat_infektion'.
    """
    results = load_dataset_scores(expert_mode=expert_id, pv_level=pv_level, scope=scope)

    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams["font.family"] = "DejaVu Sans"

    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), dpi=300)
    colors = {"Zero-Shot": "#457B9D", "Few-Shot": "#E76F51", "Two-Stage": "#2A9D8F"}

    mode_title = "Best-of-Both (Konsens)" if expert_id == "consensus" else f"Experte {expert_id}"
    level_title = "Level 1 (Produkt-Ebene)" if pv_level == 1 else "Level 2 (Unterkategorien)"

    for idx, (name, data) in enumerate(results.items()):
        ax = axes[idx]
        x = np.array(data["x"])
        y = np.array(data["y"])
        rho = data["rho"]
        p_rho = data["p_rho"]

        ax.scatter(x, y, color=colors[name], alpha=0.75, s=60, edgecolors="black", linewidth=0.6, label="Wundbild")

        sns.regplot(
            x=x, y=y, ax=ax, scatter=False,
            color="#264653",
            line_kws={"linewidth": 2.0, "linestyle": "--"}
        )

        ax.set_xlim(-5, 105)
        ax.set_ylim(-5, 105)
        ax.set_title(f"{name} ({mode_title})", fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel(f"Exsudat & Infektion Score (%) vs. {mode_title}" if scope=="exsudat_infektion" else f"Wundbeschreibung Score (%) vs. {mode_title}", fontsize=10.5, fontweight="bold")
        ax.set_ylabel(f"Primärverband F1-Score (%) vs. {mode_title}", fontsize=10.5, fontweight="bold")

        p_str = "< 0,001" if p_rho < 0.001 else f"= {p_rho:.3f}".replace(".", ",")
        stats_text = f"Spearman $\\rho = {rho:.3f}$\n$p$-Wert {p_str}\n$N = {len(x)}$ Wunden"
        stats_text = stats_text.replace(".", ",")
        
        ax.text(
            0.05, 0.82, stats_text,
            transform=ax.transAxes, fontsize=10.5, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.9, edgecolor="#102A43")
        )

    main_title = f"Korrelationsanalyse: Exsudat & Infektion vs. Primärverband ({level_title})\nVergleichsbasis: {mode_title}" if scope=="exsudat_infektion" else f"Korrelationsanalyse: Wundbeschreibung vs. Primärverband ({level_title})\nVergleichsbasis: {mode_title} (Gemappte Wundmerkmale)"
    fig.suptitle(main_title, fontsize=14, fontweight="bold", y=1.03)

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Korrelations-Plot erfolgreich gespeichert unter: {save_path}")

    plt.show()
    return fig, axes
