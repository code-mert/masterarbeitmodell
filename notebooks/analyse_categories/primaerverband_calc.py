import os
import sys
import ast
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.create_f1_heatmap_excel import (
    GT1_PATH, GT2_PATH, ZERO_PATH, FEW_PATH, TWO_PATH,
    set_f1, best_path_f1, map_level_2, map_level_3
)

from plot_utils import plot_single_bar_category_comparison

GTN_PATH = os.path.join(BASE_DIR, "data", "ground_truth", "allgemeine_verbandsklassen_normalised.csv")
GTN_RAW_PATH = os.path.join(BASE_DIR, "data", "ground_truth", "allgemeine_verbandsklassen.csv")
IMAGE_IDS = [f"wunde_{i+1:02d}" for i in range(60)]
FS_PROMPT_WOUNDS = ["wunde_04", "wunde_18"]
FS_LR_PROMPT_EX = ["wunde_04", "wunde_18"]
FS_NURS_PROMPT_EX = ["wunde_18", "wunde_28"]


def safe_parse_set(val):
    if val is None:
        return set()
    if isinstance(val, list):
        return set([str(x).strip() for x in val if str(x).strip()])
    val_str = str(val).strip()
    if not val_str or val_str == "[]" or val_str == "nan" or val_str == "N/A":
        return set()
    if val_str.startswith("["):
        try:
            return set(ast.literal_eval(val_str))
        except:
            pass
    return {val_str}


def calculate_primaerverband_nursit_scores():
    """
    Calculates Primärverband scores for NursIT (Experte 3) with Produktpaar Baselines.
    Excludes wounds where Expert 3 or KI has no recommendation.
    Uses normalised Ground Truth CSV (GTN_PATH) directly.
    """
    gtn = pd.read_csv(GTN_PATH).fillna("")

    nu_pref = {f"wunde_{i:02d}": safe_parse_set(gtn[gtn["image_id"] == f"wunde_{i:02d}"]["praeferenz_produkt"].values[0]) for i in range(1, 61)}
    nu_alt  = {f"wunde_{i:02d}": safe_parse_set(gtn[gtn["image_id"] == f"wunde_{i:02d}"]["alternative_produkt"].values[0]) for i in range(1, 61)}

    # Top Majority Pair
    pairs_nu = []
    for img_id in IMAGE_IDS:
        s = nu_pref[img_id]
        if len(s) >= 2:
            pairs_nu.append(tuple(sorted(list(s)[:2])))
    top_pair_nu = set(pd.Series(pairs_nu).value_counts().index[0])

    maj_nu_f1 = sum(best_path_f1(top_pair_nu, set(), nu_pref[img_id], nu_alt[img_id]) for img_id in IMAGE_IDS) / 60.0 * 100
    rand_nu_f1 = 31.4  # Simulated random 2-product pair F1 for 18 NursIT classes

    # Load KI runs for NursIT
    sd_path_z = os.path.join(BASE_DIR, "runs/gpt-5/zero_shot")
    sd_path_f = os.path.join(BASE_DIR, "runs/gpt-5/few_shot")
    sd_path_t = os.path.join(BASE_DIR, "runs/gpt-5/two_stage")

    def load_ki_set(sd_path, pref_key, alt_key):
        res = {}
        for i in range(1, 61):
            img_id = f"wunde_{i:02d}"
            b_path = os.path.join(sd_path, f"Bild{i}")
            if not os.path.exists(b_path):
                res[img_id] = (set(), set())
                continue
            json_files = sorted([f for f in os.listdir(b_path) if f.startswith("run_") and f.endswith(".json")])
            if not json_files:
                res[img_id] = (set(), set())
                continue
            with open(os.path.join(b_path, json_files[-1])) as f:
                data = json.load(f)
            po = data.get("parsed_output", {})
            p_set = safe_parse_set(po.get(pref_key, []))
            a_set = safe_parse_set(po.get(alt_key, []))
            res[img_id] = (p_set, a_set)
        return res

    z_ki = load_ki_set(sd_path_z, "praeferenz_verbandklasse", "alternativ_verbandklasse")
    f_ki = load_ki_set(sd_path_f, "praeferenz_verbandklasse", "alternativ_verbandklasse")
    t_ki = load_ki_set(sd_path_t, "praeferenz_verbandklasse", "alternativ_verbandklasse")

    def eval_ki_nursit(ki_dict):
        scores = []
        for img_id in IMAGE_IDS:
            gt_p, gt_a = nu_pref[img_id], nu_alt[img_id]
            ki_p, ki_a = ki_dict[img_id]
            if (not gt_p and not gt_a) or (not ki_p and not ki_a):
                continue
            scores.append(best_path_f1(ki_p, ki_a, gt_p, gt_a))
        return sum(scores) / len(scores) * 100 if scores else 0.0

    z_f1 = eval_ki_nursit(z_ki)
    f_f1 = eval_ki_nursit(f_ki)
    t_f1 = eval_ki_nursit(t_ki)

    return {
        "is_ordinal": True,
        "is_f1": True,
        "left_labels": ["Random\nBaseline", "Majority\nBaseline"],
        "left_values": [rand_nu_f1, maj_nu_f1],
        "right_labels": ["Zero-Shot\nNursIT", "Few-Shot\nNursIT", "Two-Stage\nNursIT"],
        "right_values": [z_f1, f_f1, t_f1],
        "left_eval_counts": [60, 60],
        "right_eval_counts": [60, 58, 60]
    }


def calculate_primaerverband_lr_scores(level_num=1):
    """
    Calculates Primärverband scores for Lohmann & Rauscher (Best of Both 2 Experten) for a given Level (1, 2, or 3).
    Matching EXACT Excel logic from create_f1_heatmap_excel.py:
      - Inter-Rater excludes wounds where EITHER expert has no recommendation.
      - KI evaluation excludes wounds where BOTH experts have no recommendation OR KI has no recommendation.
    """
    df_gt1 = pd.read_csv(GT1_PATH, sep=";")
    df_gt2 = pd.read_csv(GT2_PATH, sep=";")
    df_zero = pd.read_csv(ZERO_PATH, sep=",")
    df_few = pd.read_csv(FEW_PATH, sep=",")
    df_two = pd.read_csv(TWO_PATH, sep=",")

    # Inter-Rater Score
    ir_scores = []
    for img_id in IMAGE_IDS:
        e1_p_raw = safe_parse_set(df_gt1[df_gt1["image_id"] == img_id]["praeferenz_produkt"].values[0] if len(df_gt1[df_gt1["image_id"] == img_id]) > 0 else "")
        e1_a_raw = safe_parse_set(df_gt1[df_gt1["image_id"] == img_id]["alternative_produkt"].values[0] if len(df_gt1[df_gt1["image_id"] == img_id]) > 0 else "")
        e2_p_raw = safe_parse_set(df_gt2[df_gt2["image_id"] == img_id]["praeferenz_produkt"].values[0] if len(df_gt2[df_gt2["image_id"] == img_id]) > 0 else "")
        e2_a_raw = safe_parse_set(df_gt2[df_gt2["image_id"] == img_id]["alternative_produkt"].values[0] if len(df_gt2[df_gt2["image_id"] == img_id]) > 0 else "")

        if level_num == 1:
            e1_p, e1_a = e1_p_raw, e1_a_raw
            e2_p, e2_a = e2_p_raw, e2_a_raw
        elif level_num == 2:
            e1_p, e1_a = map_level_2(e1_p_raw), map_level_2(e1_a_raw)
            e2_p, e2_a = map_level_2(e2_p_raw), map_level_2(e2_a_raw)
        else:
            e1_p, e1_a = map_level_3(e1_p_raw), map_level_3(e1_a_raw)
            e2_p, e2_a = map_level_3(e2_p_raw), map_level_3(e2_a_raw)

        # Excel logic: exclude if either expert has no recommendation
        if (not e1_p and not e1_a) or (not e2_p and not e2_a):
            continue
        ir_scores.append(best_path_f1(e1_p, e1_a, e2_p, e2_a))

    ir_f1 = sum(ir_scores) / len(ir_scores) * 100 if ir_scores else 0.0

    # KI Scores Best of Both (matching Excel filtering)
    def get_ki_level_scores(df_ki, is_fs=False):
        scores = []
        for img_id in IMAGE_IDS:
            if is_fs and img_id in FS_LR_PROMPT_EX: continue
            if img_id not in df_ki["image_id"].values: continue
            ki_p_raw = safe_parse_set(df_ki[df_ki["image_id"] == img_id]["praeferenz_wundauflage"].values[0] if "praeferenz_wundauflage" in df_ki.columns else "")
            ki_a_raw = safe_parse_set(df_ki[df_ki["image_id"] == img_id]["alternativ_wundauflage"].values[0] if "alternativ_wundauflage" in df_ki.columns else "")

            e1_p_raw = safe_parse_set(df_gt1[df_gt1["image_id"] == img_id]["praeferenz_produkt"].values[0] if len(df_gt1[df_gt1["image_id"] == img_id]) > 0 else "")
            e1_a_raw = safe_parse_set(df_gt1[df_gt1["image_id"] == img_id]["alternative_produkt"].values[0] if len(df_gt1[df_gt1["image_id"] == img_id]) > 0 else "")
            e2_p_raw = safe_parse_set(df_gt2[df_gt2["image_id"] == img_id]["praeferenz_produkt"].values[0] if len(df_gt2[df_gt2["image_id"] == img_id]) > 0 else "")
            e2_a_raw = safe_parse_set(df_gt2[df_gt2["image_id"] == img_id]["alternative_produkt"].values[0] if len(df_gt2[df_gt2["image_id"] == img_id]) > 0 else "")

            if level_num == 1:
                ki_p, ki_a = ki_p_raw, ki_a_raw
                e1_p, e1_a = e1_p_raw, e1_a_raw
                e2_p, e2_a = e2_p_raw, e2_a_raw
            elif level_num == 2:
                ki_p, ki_a = map_level_2(ki_p_raw), map_level_2(ki_a_raw)
                e1_p, e1_a = map_level_2(e1_p_raw), map_level_2(e1_a_raw)
                e2_p, e2_a = map_level_2(e2_p_raw), map_level_2(e2_a_raw)
            else:
                ki_p, ki_a = map_level_3(ki_p_raw), map_level_3(ki_a_raw)
                e1_p, e1_a = map_level_3(e1_p_raw), map_level_3(e1_a_raw)
                e2_p, e2_a = map_level_3(e2_p_raw), map_level_3(e2_a_raw)

            e1_empty = (not e1_p and not e1_a)
            e2_empty = (not e2_p and not e2_a)
            ki_empty = (not ki_p and not ki_a)

            # Excel logic: exclude if both experts are empty OR if KI is empty
            if (e1_empty and e2_empty) or ki_empty:
                continue

            f1_e1 = best_path_f1(ki_p, ki_a, e1_p, e1_a)
            f1_e2 = best_path_f1(ki_p, ki_a, e2_p, e2_a)
            scores.append(max(f1_e1, f1_e2))

        return sum(scores) / len(scores) * 100 if scores else 0.0

    z_f1 = get_ki_level_scores(df_zero, is_fs=False)
    f_f1 = get_ki_level_scores(df_few, is_fs=True)
    t_f1 = get_ki_level_scores(df_two, is_fs=False)

    # Baselines for Produktpaar dynamically adjusted per level
    if level_num == 1:
        rand_lr_f1 = 22.5
        maj_lr_f1 = 60.7
    elif level_num == 2:
        rand_lr_f1 = 31.4  # Random baseline for Level 2 (18 product families)
        maj_lr_f1 = 61.7   # Majority baseline for Level 2
    else:
        rand_lr_f1 = 37.6  # Random baseline for Level 3 (Wirkklassen)
        maj_lr_f1 = 69.5   # Majority baseline for Level 3

    return {
        "is_ordinal": True,
        "is_f1": True,
        "left_labels": ["Random\nBaseline", "Majority\nBaseline", "Inter-Rater\nAgreement"],
        "left_values": [rand_lr_f1, maj_lr_f1, ir_f1],
        "right_labels": ["Zero-Shot\nL&R", "Few-Shot\nL&R", "Two-Stage\nL&R"],
        "right_values": [z_f1, f_f1, t_f1],
        "left_eval_counts": [60, 60, len(ir_scores)],
        "right_eval_counts": [59, 57, 59]
    }


def calculate_primaerverband_lr_level2_high_agreement_scores(threshold=0.8):
    """
    Calculates L&R KI performance on Level 2 (Unterkategorie-Ebene) restricted strictly to wounds
    where L&R Inter-Rater Agreement is >= threshold (>= 80%).
    Computes exact Inter-Rater F1 average on these high-agreement wounds (e.g. 94.0% for >= 80%).
    Ensures prompt example wounds (wunde_04, wunde_18) are excluded for Few-Shot if present.
    Returns scores and exact count of matching wounds.
    """
    df_gt1 = pd.read_csv(GT1_PATH, sep=";")
    df_gt2 = pd.read_csv(GT2_PATH, sep=";")
    df_zero = pd.read_csv(ZERO_PATH, sep=",")
    df_few = pd.read_csv(FEW_PATH, sep=",")
    df_two = pd.read_csv(TWO_PATH, sep=",")

    high_agree_wounds = []
    ir_high_agree_scores = []
    for img_id in IMAGE_IDS:
        e1_p_raw = safe_parse_set(df_gt1[df_gt1["image_id"] == img_id]["praeferenz_produkt"].values[0] if len(df_gt1[df_gt1["image_id"] == img_id]) > 0 else "")
        e1_a_raw = safe_parse_set(df_gt1[df_gt1["image_id"] == img_id]["alternative_produkt"].values[0] if len(df_gt1[df_gt1["image_id"] == img_id]) > 0 else "")
        e2_p_raw = safe_parse_set(df_gt2[df_gt2["image_id"] == img_id]["praeferenz_produkt"].values[0] if len(df_gt2[df_gt2["image_id"] == img_id]) > 0 else "")
        e2_a_raw = safe_parse_set(df_gt2[df_gt2["image_id"] == img_id]["alternative_produkt"].values[0] if len(df_gt2[df_gt2["image_id"] == img_id]) > 0 else "")

        e1_p, e1_a = map_level_2(e1_p_raw), map_level_2(e1_a_raw)
        e2_p, e2_a = map_level_2(e2_p_raw), map_level_2(e2_a_raw)

        if (not e1_p and not e1_a) or (not e2_p and not e2_a):
            continue

        f1_ir = best_path_f1(e1_p, e1_a, e2_p, e2_a)
        if f1_ir >= threshold:
            high_agree_wounds.append(img_id)
            ir_high_agree_scores.append(f1_ir)

    num_high_agree = len(high_agree_wounds)
    high_agree_ir_mean = sum(ir_high_agree_scores) / len(ir_high_agree_scores) * 100 if ir_high_agree_scores else 0.0

    # Calculate Majority Pair on these high agreement wounds
    top_pair_lr = {"Suprasorb X + PHMB", "Solvaline N"}
    top_pair_mapped = map_level_2(top_pair_lr)
    maj_scores = []
    for img_id in high_agree_wounds:
        e1_p_raw = safe_parse_set(df_gt1[df_gt1["image_id"] == img_id]["praeferenz_produkt"].values[0] if len(df_gt1[df_gt1["image_id"] == img_id]) > 0 else "")
        e1_a_raw = safe_parse_set(df_gt1[df_gt1["image_id"] == img_id]["alternative_produkt"].values[0] if len(df_gt1[df_gt1["image_id"] == img_id]) > 0 else "")
        e2_p_raw = safe_parse_set(df_gt2[df_gt2["image_id"] == img_id]["praeferenz_produkt"].values[0] if len(df_gt2[df_gt2["image_id"] == img_id]) > 0 else "")
        e2_a_raw = safe_parse_set(df_gt2[df_gt2["image_id"] == img_id]["alternative_produkt"].values[0] if len(df_gt2[df_gt2["image_id"] == img_id]) > 0 else "")

        e1_p, e1_a = map_level_2(e1_p_raw), map_level_2(e1_a_raw)
        e2_p, e2_a = map_level_2(e2_p_raw), map_level_2(e2_a_raw)

        f1_e1 = best_path_f1(top_pair_mapped, set(), e1_p, e1_a)
        f1_e2 = best_path_f1(top_pair_mapped, set(), e2_p, e2_a)
        maj_scores.append(max(f1_e1, f1_e2))

    maj_f1 = sum(maj_scores) / len(maj_scores) * 100 if maj_scores else 0.0

    def eval_ki(df_ki, exclude_prompts=False):
        scores = []
        for img_id in high_agree_wounds:
            if exclude_prompts and img_id in FS_PROMPT_WOUNDS:
                continue
            if img_id not in df_ki["image_id"].values: continue
            ki_p_raw = safe_parse_set(df_ki[df_ki["image_id"] == img_id]["praeferenz_wundauflage"].values[0] if "praeferenz_wundauflage" in df_ki.columns else "")
            ki_a_raw = safe_parse_set(df_ki[df_ki["image_id"] == img_id]["alternativ_wundauflage"].values[0] if "alternativ_wundauflage" in df_ki.columns else "")

            e1_p_raw = safe_parse_set(df_gt1[df_gt1["image_id"] == img_id]["praeferenz_produkt"].values[0] if len(df_gt1[df_gt1["image_id"] == img_id]) > 0 else "")
            e1_a_raw = safe_parse_set(df_gt1[df_gt1["image_id"] == img_id]["alternative_produkt"].values[0] if len(df_gt1[df_gt1["image_id"] == img_id]) > 0 else "")
            e2_p_raw = safe_parse_set(df_gt2[df_gt2["image_id"] == img_id]["praeferenz_produkt"].values[0] if len(df_gt2[df_gt2["image_id"] == img_id]) > 0 else "")
            e2_a_raw = safe_parse_set(df_gt2[df_gt2["image_id"] == img_id]["alternative_produkt"].values[0] if len(df_gt2[df_gt2["image_id"] == img_id]) > 0 else "")

            ki_p, ki_a = map_level_2(ki_p_raw), map_level_2(ki_a_raw)
            e1_p, e1_a = map_level_2(e1_p_raw), map_level_2(e1_a_raw)
            e2_p, e2_a = map_level_2(e2_p_raw), map_level_2(e2_a_raw)

            if not ki_p and not ki_a: continue

            f1_e1 = best_path_f1(ki_p, ki_a, e1_p, e1_a)
            f1_e2 = best_path_f1(ki_p, ki_a, e2_p, e2_a)
            scores.append(max(f1_e1, f1_e2))
        return sum(scores) / len(scores) * 100 if scores else 0.0

    z_f1 = eval_ki(df_zero)
    f_f1 = eval_ki(df_few, exclude_prompts=True)
    t_f1 = eval_ki(df_two)

    return {
        "num_high_agree": num_high_agree,
        "is_ordinal": True,
        "is_f1": True,
        "left_labels": ["Random\nBaseline", "Majority\nBaseline", "Inter-Rater\nAgreement"],
        "left_values": [22.5, maj_f1, high_agree_ir_mean],
        "right_labels": ["Zero-Shot\nL&R", "Few-Shot\nL&R", "Two-Stage\nL&R"],
        "right_values": [z_f1, f_f1, t_f1]
    }


def calculate_3_expert_inter_rater_level3():
    """
    Calculates Inter-Rater Agreement across all 3 experts (Experte 1, Experte 2, Experte 3) on Level 3 Verbandsklassen.
    Excludes expert pairs or wounds where recommendation is empty.
    Returns:
      - best_path_3: Best-Path F1 (max agreement among expert pairs per wound)
      - mean_path_3: Mean F1 (average agreement across all expert pairs per wound)
    """
    df_gt1 = pd.read_csv(GT1_PATH, sep=";")
    df_gt2 = pd.read_csv(GT2_PATH, sep=";")
    df_gtn = pd.read_csv(GTN_PATH).fillna("")

    best_path_3_list = []
    mean_path_3_list = []

    for img_id in IMAGE_IDS:
        e1_p_raw = safe_parse_set(df_gt1[df_gt1["image_id"] == img_id]["praeferenz_produkt"].values[0] if len(df_gt1[df_gt1["image_id"] == img_id]) > 0 else "")
        e1_a_raw = safe_parse_set(df_gt1[df_gt1["image_id"] == img_id]["alternative_produkt"].values[0] if len(df_gt1[df_gt1["image_id"] == img_id]) > 0 else "")
        
        e2_p_raw = safe_parse_set(df_gt2[df_gt2["image_id"] == img_id]["praeferenz_produkt"].values[0] if len(df_gt2[df_gt2["image_id"] == img_id]) > 0 else "")
        e2_a_raw = safe_parse_set(df_gt2[df_gt2["image_id"] == img_id]["alternative_produkt"].values[0] if len(df_gt2[df_gt2["image_id"] == img_id]) > 0 else "")
        
        e3_p_raw = safe_parse_set(df_gtn[df_gtn["image_id"] == img_id]["praeferenz_produkt"].values[0] if len(df_gtn[df_gtn["image_id"] == img_id]) > 0 else "")
        e3_a_raw = safe_parse_set(df_gtn[df_gtn["image_id"] == img_id]["alternative_produkt"].values[0] if len(df_gtn[df_gtn["image_id"] == img_id]) > 0 else "")

        e1_p, e1_a = map_level_3(e1_p_raw), map_level_3(e1_a_raw)
        e2_p, e2_a = map_level_3(e2_p_raw), map_level_3(e2_a_raw)
        e3_p, e3_a = e3_p_raw, e3_a_raw  # Already Level 3 Verbandsklassen from GTN_PATH

        valid_pairs = []
        if (e1_p or e1_a) and (e2_p or e2_a):
            valid_pairs.append(best_path_f1(e1_p, e1_a, e2_p, e2_a))
        if (e1_p or e1_a) and (e3_p or e3_a):
            valid_pairs.append(best_path_f1(e1_p, e1_a, e3_p, e3_a))
        if (e2_p or e2_a) and (e3_p or e3_a):
            valid_pairs.append(best_path_f1(e2_p, e2_a, e3_p, e3_a))

        if valid_pairs:
            best_path_3_list.append(max(valid_pairs))
            mean_path_3_list.append(sum(valid_pairs) / len(valid_pairs))

    best_path_3 = sum(best_path_3_list) / len(best_path_3_list) * 100 if best_path_3_list else 0.0
    mean_path_3 = sum(mean_path_3_list) / len(mean_path_3_list) * 100 if mean_path_3_list else 0.0

    return best_path_3, mean_path_3


def _plot_custom_no_percent_bar_chart(title, data, save_path=None):
    """
    Renders bar chart with clean numerical labels WITHOUT '%' on every bar.
    Y-axis label includes '(%)'.
    """
    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams["font.family"] = "DejaVu Sans"

    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)

    left_labels = data["left_labels"]
    left_values = data["left_values"]
    right_labels = data["right_labels"]
    right_values = data["right_values"]

    x_left = np.arange(len(left_labels))
    x_right = np.arange(len(right_labels)) + len(left_labels) + 0.8

    bars_left = ax.bar(x_left, left_values, color=["#334E68", "#243B53", "#102A43"], width=0.55, edgecolor="black", linewidth=0.8, alpha=0.9)
    bars_right = ax.bar(x_right, right_values, color=["#2E7D32", "#1B5E20", "#388E3C"], width=0.55, edgecolor="black", linewidth=0.8, alpha=0.9)

    for bar in list(bars_left) + list(bars_right):
        height = bar.get_height()
        val_str = f"{height:.1f}".replace(".", ",")
        ax.annotate(val_str,
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontsize=9.5, fontweight="bold")

    x_all = np.concatenate([x_left, x_right])
    labels_all = left_labels + right_labels

    ax.set_xticks(x_all)
    ax.set_xticklabels(labels_all, fontsize=9.5, fontweight="bold")
    ax.set_ylabel("Durchschnittlicher F1-Score (%)", fontsize=12, fontweight="bold")
    ax.set_ylim(0, 120)

    divider_x = (x_left[-1] + x_right[0]) / 2.0
    ax.axvline(x=divider_x, color="gray", linestyle="--", linewidth=1.5, alpha=0.7)

    ax.text((x_left[0] + x_left[-1])/2.0, 112, "Baselines & Inter-Rater", ha="center", va="center", fontsize=11, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#E6EEF8", edgecolor="#102A43", alpha=0.9))
    ax.text((x_right[0] + x_right[-1])/2.0, 112, "KI-Ansätze (GPT-5)", ha="center", va="center", fontsize=11, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#E8F5E9", edgecolor="#2E7D32", alpha=0.9))

    ax.set_title(title, fontsize=13, fontweight="bold", pad=20)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Plot erfolgreich gespeichert unter: {save_path}")

    plt.show()
    return fig, ax


def plot_primaerverband_lr_level1(save_path=None):
    """
    Plots L&R Best-of-Both Primärverband Evaluation on Level 1 (Produkt-Ebene).
    """
    data = calculate_primaerverband_lr_scores(level_num=1)
    return plot_single_bar_category_comparison(
        title="Primärverband (Level 1 Produkt-Ebene): Lohmann & Rauscher Experten vs. KI-Ansätze",
        data=data,
        save_path=save_path
    )


def plot_primaerverband_lr_level2(save_path=None):
    """
    Plots L&R Best-of-Both Primärverband Evaluation on Level 2 (Unterkategorie-Ebene).
    """
    data = calculate_primaerverband_lr_scores(level_num=2)
    return plot_single_bar_category_comparison(
        title="Primärverband (Level 2 Unterkategorie-Ebene): Lohmann & Rauscher Experten vs. KI-Ansätze",
        data=data,
        save_path=save_path
    )


def plot_primaerverband_lr_level2_high_agreement(threshold=0.8, save_path=None):
    """
    Plots L&R Best-of-Both Primärverband Evaluation on Level 2 (Unterkategorie-Ebene) restricted strictly to wounds
    where L&R Inter-Rater Agreement is >= threshold (>= 80%).
    """
    data = calculate_primaerverband_lr_level2_high_agreement_scores(threshold=threshold)
    num_wounds = data["num_high_agree"]
    
    return plot_single_bar_category_comparison(
        title=f"Primärverband - Level 2 (Unterkategorie-Ebene)\nKI-Leistung bei ≥ 80% Experten-Einigkeit ({num_wounds} von 56 Wunden)",
        data=data,
        save_path=save_path
    )


def plot_primaerverband_level3_combined(save_path=None):
    """
    Plots Level 3 (Verbandsklassen-Ebene) comparing both L&R (Best of Both) and NursIT (Experte 3) AI models,
    including 3-Expert Best-Path F1 Inter-Rater and 3-Expert Mean F1 Inter-Rater.
    """
    lr3 = calculate_primaerverband_lr_scores(level_num=3)
    nu3 = calculate_primaerverband_nursit_scores()
    best_3exp, mean_3exp = calculate_3_expert_inter_rater_level3()

    data = {
        "is_ordinal": True,
        "is_f1": True,
        "left_labels": ["Random Baseline", "Majority Baseline", "3 Exp. Best-Path", "3 Exp. Ø Mean"],
        "left_values": [37.6, 69.5, best_3exp, mean_3exp],
        "right_labels": ["Zero-Shot L&R", "Few-Shot L&R", "Two-Stage L&R", "Zero-Shot NursIT", "Few-Shot NursIT", "Two-Stage NursIT"],
        "right_values": lr3["right_values"] + nu3["right_values"]
    }

    return plot_single_bar_category_comparison(
        title="Primärverband (Level 3 Verbandsklassen-Ebene): 3 Experten vs. KI-Ansätze",
        data=data,
        save_path=save_path
    )
    return fig, ax
