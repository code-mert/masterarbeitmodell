import os
import sys
import re
import random
import pandas as pd
import numpy as np
import ipywidgets as widgets
from IPython.display import display, Image, HTML
import matplotlib.pyplot as plt
import seaborn as sns

# Paths setup relative to this directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GT_DIR = os.path.join(BASE_DIR, "data", "ground_truth", "lohmann_rauscher")
LLM_DIR = os.path.join(BASE_DIR, "data", "llm_outputs")
IMAGE_DIR = os.path.join(BASE_DIR, "data", "wundbilder")

# Import official metrics from eval/metrics.py
sys.path.insert(0, BASE_DIR)
try:
    from eval.metrics import best_path_f1, set_f1, exact_match, precision_recall
except ImportError:
    from metrics import best_path_f1, set_f1, exact_match, precision_recall

CATEGORY_MAPPING = {
    "wundtyp": {
        "gt": ["wundtyp"],
        "llm": ["wundtyp"],
        "title": "Wundtyp"
    },
    "lokalisation": {
        "gt": ["lokalisation"],
        "llm": ["lokalisation"],
        "title": "Lokalisation"
    },
    "wundstadium": {
        "gt": ["wundstadium"],
        "llm": ["wundstadium"],
        "title": "Wundstadium"
    },
    "wundgrund": {
        "gt": ["wundgrund"],
        "llm": ["wundgrund"],
        "title": "Wundgrund"
    },
    "wundrand": {
        "gt": ["wundrand"],
        "llm": ["wundrand"],
        "title": "Wundrand"
    },
    "wundumgebung": {
        "gt": ["wundumgebung"],
        "llm": ["wundumgebung"],
        "title": "Wundumgebung"
    },
    "exsudat": {
        "gt": ["exsudat"],
        "llm": ["exsudat_menge"],
        "title": "Exsudat"
    },
    "infektion": {
        "gt": ["infektion"],
        "llm": ["infektion_vorhanden"],
        "title": "Infektion"
    },
    "debridement": {
        "gt": ["debridement_notwendig", "debridement"],
        "llm": ["debridement_notwendig", "debridement_methode"],
        "title": "Debridement"
    },
    "primaerverband": {
        "gt": ["praeferenz_produkt", "alternative_produkt"],
        "llm": ["praeferenz_wundauflage", "alternativ_wundauflage"],
        "title": "Primärverband"
    },
    "primärverband": {
        "gt": ["praeferenz_produkt", "alternative_produkt"],
        "llm": ["praeferenz_wundauflage", "alternativ_wundauflage"],
        "title": "Primärverband"
    },
    "sekundaerverband": {
        "gt": ["ergaenzende_produkte_praeferenz", "ergaenzende_produkte_alternativ"],
        "llm": ["praeferenz_ergaenzung", "alternativ_ergaenzung"],
        "title": "Sekundärverband"
    },
    "sekundärverband": {
        "gt": ["ergaenzende_produkte_praeferenz", "ergaenzende_produkte_alternativ"],
        "llm": ["praeferenz_ergaenzung", "alternativ_ergaenzung"],
        "title": "Sekundärverband"
    },
    "kompression": {
        "gt": ["kompression_indiziert", "kompression_produkte"],
        "llm": ["kompression_indiziert", "kompression_produkt"],
        "title": "Kompression"
    }
}

PRODUCT_FAMILY_MAP = {
    "suprasorb a": "Suprasorb A (Alginat)",
    "suprasorb a pro": "Suprasorb A (Alginat)",
    "suprasorb a + ag": "Suprasorb A (Alginat)",

    "suprasorb p": "Suprasorb P (Schaumstoff)",
    "suprasorb p sensitive": "Suprasorb P (Schaumstoff)",
    "suprasorb p sensiflex": "Suprasorb P (Schaumstoff)",
    "suprasorb p + phmb": "Suprasorb P (Schaumstoff)",

    "suprasorb x": "Suprasorb X (Hydrobalance)",
    "suprasorb x pro": "Suprasorb X (Hydrobalance)",
    "suprasorb x + phmb": "Suprasorb X (Hydrobalance)",

    "suprasorb liquacel pro": "Suprasorb Liquacel (Hydrofiber)",
    "suprasorb liquacel": "Suprasorb Liquacel (Hydrofiber)",

    "vliwasorb pro": "Vliwasorb (Superabsorber)",
    "vliwasorb sensitive": "Vliwasorb (Superabsorber)",
    "vliwazell pro": "Vliwasorb (Superabsorber)",
    "vliwazell": "Vliwasorb (Superabsorber)",

    "solvaline n": "Solvaline / Lomatuell (Atraumatische Auflage)",
    "solvaline": "Solvaline / Lomatuell (Atraumatische Auflage)",
    "lomatuell pro": "Solvaline / Lomatuell (Atraumatische Auflage)",
    "lomatuell": "Solvaline / Lomatuell (Atraumatische Auflage)",

    "vliwaktiv": "Vliwaktiv (Aktivkohle)",
    "vliwaktiv ag": "Vliwaktiv (Aktivkohle)",

    "suprasorb cnp": "Suprasorb CNP (NPWT)",
    "suprasorb f protect": "Suprasorb F (Folie)",
    "suprasorb f": "Suprasorb F (Folie)",
    "suprasorb g gel-kompresse": "Suprasorb G (Gel)",
    "suprasorb g": "Suprasorb G (Gel)",
    "amorphes gel": "Suprasorb G (Gel)",
    "suprasorb h": "Suprasorb H (Hydrokolloid)",
    "metalline kompresse": "Metalline",
    "metalline": "Metalline",
}


def map_product_set(prod_set, group_by_family=True):
    if not group_by_family or not prod_set:
        return prod_set
    mapped = set()
    for item in prod_set:
        item_lower = item.strip().lower()
        if item_lower in PRODUCT_FAMILY_MAP:
            mapped.add(PRODUCT_FAMILY_MAP[item_lower])
        else:
            if "suprasorb a" in item_lower:
                mapped.add("Suprasorb A (Alginat)")
            elif "suprasorb p" in item_lower:
                mapped.add("Suprasorb P (Schaumstoff)")
            elif "suprasorb x" in item_lower:
                mapped.add("Suprasorb X (Hydrobalance)")
            elif "suprasorb liquacel" in item_lower:
                mapped.add("Suprasorb Liquacel (Hydrofiber)")
            elif "vliwasorb" in item_lower or "vliwazell" in item_lower:
                mapped.add("Vliwasorb (Superabsorber)")
            elif "solvaline" in item_lower or "lomatuell" in item_lower:
                mapped.add("Solvaline / Lomatuell (Atraumatische Auflage)")
            elif "vliwaktiv" in item_lower:
                mapped.add("Vliwaktiv (Aktivkohle)")
            elif "cnp" in item_lower:
                mapped.add("Suprasorb CNP (NPWT)")
            else:
                mapped.add(item)
    return mapped


def normalize_image_id(img_id):
    if not isinstance(img_id, str):
        img_id = str(img_id)
    match = re.search(r"(\d+)", img_id)
    if match:
        num = int(match.group(1))
        return f"wunde_{num:02d}"
    return img_id


def load_csv(path):
    if not os.path.exists(path):
        return pd.DataFrame()
    with open(path, "r", encoding="utf-8") as f:
        first_line = f.readline()
        sep = ";" if ";" in first_line else ","
    df = pd.read_csv(path, sep=sep).fillna("")
    if "image_id" in df.columns:
        df["image_id"] = df["image_id"].apply(normalize_image_id)
    return df


def to_clean_set(val):
    if not val:
        return set()
    if isinstance(val, set):
        return {str(x).strip().lower() for x in val if str(x).strip()}
    if isinstance(val, list):
        return {str(x).strip().lower() for x in val if str(x).strip()}
    s = str(val).strip().lower()
    s = re.sub(r"<div[^>]*>|</div>", " ", s)
    s = re.sub(r"[\[\]'\"`]", "", s)
    if not s or s in ["—", "leer", "keine angabe"]:
        return set()
    parts = [p.strip() for p in re.split(r"[,;|]+", s) if p.strip()]
    return set(parts)


def get_category_tables(category_key):
    key = category_key.lower().strip()
    if key not in CATEGORY_MAPPING:
        raise ValueError(f"Unbekannte Kategorie '{category_key}'. Verfügbar: {list(CATEGORY_MAPPING.keys())}")

    cfg = CATEGORY_MAPPING[key]
    gt_cols = cfg["gt"]
    llm_cols = cfg["llm"]

    gt1_r = load_csv(os.path.join(GT_DIR, "Experte1_LR_GroundTruth.csv"))
    gt1_n = load_csv(os.path.join(GT_DIR, "Experte1_LR_GroundTruth_normalised.csv"))
    gt2_r = load_csv(os.path.join(GT_DIR, "Experte2_LR_GroundTruth.csv"))
    gt2_n = load_csv(os.path.join(GT_DIR, "Experte2_LR_GroundTruth_normalised.csv"))

    zero_r = load_csv(os.path.join(LLM_DIR, "zero_shot_lr", "zero_shot_lr_raw.csv"))
    zero_n = load_csv(os.path.join(LLM_DIR, "zero_shot_lr", "zero_shot_lr_normalised.csv"))

    few_r = load_csv(os.path.join(LLM_DIR, "few_shot_lr", "few_shot_lr_raw.csv"))
    few_n = load_csv(os.path.join(LLM_DIR, "few_shot_lr", "few_shot_lr_normalised.csv"))

    two_r = load_csv(os.path.join(LLM_DIR, "two_stage_lr", "two_stage_lr_raw.csv"))
    two_n = load_csv(os.path.join(LLM_DIR, "two_stage_lr", "two_stage_lr_normalised.csv"))

    image_ids = [f"wunde_{i:02d}" for i in range(1, 61)]
    records_raw = []
    records_norm = []

    def get_val(df, img_id, cols):
        if df.empty or "image_id" not in df.columns:
            return "", "", ""
        sub = df[df["image_id"] == img_id]
        if sub.empty:
            return "", "", ""
        row = sub.iloc[0]
        val1 = str(row.get(cols[0], "")).strip()
        val2 = str(row.get(cols[1], "")).strip() if len(cols) > 1 else ""

        if len(cols) == 2:
            s1 = val1 if val1 else "—"
            s2 = val2 if val2 else "—"
            rendered = f"<div>{s1}</div><div style='border-top:1px dashed #adb5bd; margin:4px 0;'></div><div>{s2}</div>"
            return rendered, val1, val2
        else:
            return val1, val1, ""

    for img_id in image_ids:
        v_gt1_r, p_gt1_r, a_gt1_r = get_val(gt1_r, img_id, gt_cols)
        v_gt1_n, p_gt1_n, a_gt1_n = get_val(gt1_n, img_id, gt_cols)

        v_gt2_r, p_gt2_r, a_gt2_r = get_val(gt2_r, img_id, gt_cols)
        v_gt2_n, p_gt2_n, a_gt2_n = get_val(gt2_n, img_id, gt_cols)

        v_zero_r, p_zero_r, a_zero_r = get_val(zero_r, img_id, llm_cols)
        v_zero_n, p_zero_n, a_zero_n = get_val(zero_n, img_id, llm_cols)

        v_few_r, p_few_r, a_few_r = get_val(few_r, img_id, llm_cols)
        v_few_n, p_few_n, a_few_n = get_val(few_n, img_id, llm_cols)

        v_two_r, p_two_r, a_two_r = get_val(two_r, img_id, llm_cols)
        v_two_n, p_two_n, a_two_n = get_val(two_n, img_id, llm_cols)

        records_raw.append({
            "image_id": img_id,
            "Experte 1": v_gt1_r, "GT1_p": p_gt1_r, "GT1_a": a_gt1_r,
            "Experte 2": v_gt2_r, "GT2_p": p_gt2_r, "GT2_a": a_gt2_r,
            "Zero-Shot": v_zero_r, "Zero_p": p_zero_r, "Zero_a": a_zero_r,
            "Few-Shot": v_few_r, "Few_p": p_few_r, "Few_a": a_few_r,
            "Two-Stage": v_two_r, "Two_p": p_two_r, "Two_a": a_two_r,
        })
        records_norm.append({
            "image_id": img_id,
            "Experte 1": v_gt1_n, "GT1_p": p_gt1_n, "GT1_a": a_gt1_n,
            "Experte 2": v_gt2_n, "GT2_p": p_gt2_n, "GT2_a": a_gt2_n,
            "Zero-Shot": v_zero_n, "Zero_p": p_zero_n, "Zero_a": a_zero_n,
            "Few-Shot": v_few_n, "Few_p": p_few_n, "Few_a": a_few_n,
            "Two-Stage": v_two_n, "Two_p": p_two_n, "Two_a": a_two_n,
        })

    df_r = pd.DataFrame(records_raw)
    df_n = pd.DataFrame(records_norm)
    df_r._category_key = key
    df_n._category_key = key
    return df_r, df_n


def evaluate_product_match(pred_p, pred_a, gt_p, gt_a, group_by_family=False):
    p_set = map_product_set(to_clean_set(pred_p), group_by_family)
    a_set = map_product_set(to_clean_set(pred_a), group_by_family)
    gp_set = map_product_set(to_clean_set(gt_p), group_by_family)
    ga_set = map_product_set(to_clean_set(gt_a), group_by_family)

    f1, exact, _, _ = best_path_f1(p_set, a_set, gp_set, ga_set)
    return f1, exact


def classify_row_match(row, col_name, category_key, group_by_family=False):
    prefix_map = {
        "Zero-Shot": "Zero",
        "Few-Shot": "Few",
        "Two-Stage": "Two"
    }
    pfx = prefix_map[col_name]
    key = category_key.lower().strip()

    is_product = key in ["primaerverband", "primärverband", "sekundaerverband", "sekundärverband"]

    if is_product:
        f1_1, exact_1 = evaluate_product_match(row[f"{pfx}_p"], row[f"{pfx}_a"], row["GT1_p"], row["GT1_a"], group_by_family)
        f1_2, exact_2 = evaluate_product_match(row[f"{pfx}_p"], row[f"{pfx}_a"], row["GT2_p"], row["GT2_a"], group_by_family)

        if exact_1 and exact_2:
            return "both"
        if exact_1:
            return "gt1"
        if exact_2:
            return "gt2"
        if f1_1 > 0 or f1_2 > 0:
            return "partial"
        return "none"
    else:
        p_set = to_clean_set(row[col_name])
        g1_set = to_clean_set(row["Experte 1"])
        g2_set = to_clean_set(row["Experte 2"])

        if not p_set:
            if not g1_set and not g2_set:
                return "both"
            return "none"

        f1_1 = set_f1(p_set, g1_set)
        f1_2 = set_f1(p_set, g2_set)
        ex_1 = exact_match(p_set, g1_set)
        ex_2 = exact_match(p_set, g2_set)

        if ex_1 and ex_2:
            return "both"
        if ex_1:
            return "gt1"
        if ex_2:
            return "gt2"
        if f1_1 > 0 or f1_2 > 0:
            return "partial"
        return "none"


def style_category_table(df, category_key=None, group_by_family=False):
    if category_key is None:
        category_key = getattr(df, "_category_key", "wundtyp")

    visible_cols = ["image_id", "Experte 1", "Experte 2", "Zero-Shot", "Few-Shot", "Two-Stage"]
    display_df = df[visible_cols].copy()

    def apply_styles(row):
        styles = [""] * len(row)
        orig_row = df.loc[row.name]

        for i, col_name in enumerate(row.index):
            if col_name == "image_id":
                styles[i] = "background-color: #e9ecef; color: #111111; font-weight: bold; border-right: 2px solid #dee2e6;"
            elif col_name == "Experte 1":
                styles[i] = "background-color: #d3f9d8; color: #083e12; font-weight: bold; opacity: 1.0;"
            elif col_name == "Experte 2":
                styles[i] = "background-color: #d0ebff; color: #002b49; font-weight: bold; opacity: 1.0;"
            elif col_name in ["Zero-Shot", "Few-Shot", "Two-Stage"]:
                status = classify_row_match(orig_row, col_name, category_key, group_by_family)
                if status == "both":
                    styles[i] = "background-color: #eebefa; color: #360745; font-weight: bold; opacity: 1.0;"
                elif status == "gt1":
                    styles[i] = "background-color: #c3fae8; color: #044229; font-weight: bold; opacity: 1.0;"
                elif status == "gt2":
                    styles[i] = "background-color: #d0ebff; color: #002b49; font-weight: bold; opacity: 1.0;"
                elif status == "partial":
                    styles[i] = "background-color: #fff3bf; color: #594200; font-weight: bold; opacity: 1.0;"
                else:
                    styles[i] = "background-color: #ffe3e3; color: #7a0000; font-weight: bold; opacity: 1.0;"
        return styles

    styler = display_df.style.apply(apply_styles, axis=1)
    styler.set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#343a40'), ('color', '#ffffff'), ('font-weight', 'bold'), ('text-align', 'center'), ('padding', '8px')]},
        {'selector': 'td', 'props': [('padding', '6px 10px'), ('font-size', '13px')]},
        {'selector': 'table', 'props': [('border-collapse', 'collapse'), ('width', '100%')]}
    ])
    return HTML(styler.to_html())


def display_legend():
    html = """
    <div style='margin-bottom: 14px; font-family: sans-serif; font-size: 13px; line-height: 2.0; background: #ffffff; padding: 12px; border-radius: 6px; border: 1px solid #dee2e6;'>
        <b style='color: #111;'>Legende & Offizielle Evaluation (eval/metrics.py):</b><br/>
        <span style='background-color: #eebefa; color: #360745; padding: 4px 8px; border-radius: 4px; font-weight: bold; margin-right: 8px;'>🟣 Lila</span> Exakter Match (Exact / Best-Path F1 = 100%) mit <b>BEIDEN Experten</b><br/>
        <span style='background-color: #c3fae8; color: #044229; padding: 4px 8px; border-radius: 4px; font-weight: bold; margin-right: 8px;'>🟢 Grün</span> Exakter Match mit <b>Experte 1</b><br/>
        <span style='background-color: #d0ebff; color: #002b49; padding: 4px 8px; border-radius: 4px; font-weight: bold; margin-right: 8px;'>🔵 Blau</span> Exakter Match mit <b>Experte 2</b><br/>
        <span style='background-color: #fff3bf; color: #594200; padding: 4px 8px; border-radius: 4px; font-weight: bold; margin-right: 8px;'>🟠 Orange</span> <b>Teilweiser Match</b> (F1 > 0% / Schnittmenge vorhanden)<br/>
        <span style='background-color: #ffe3e3; color: #7a0000; padding: 4px 8px; border-radius: 4px; font-weight: bold; margin-right: 8px;'>🔴 Rot</span> <b>Keine Übereinstimmung</b> (F1 = 0%)<br/>
        <hr style='border: none; border-top: 1px solid #eee; margin: 8px 0;'/>
        <span style='background-color: #d3f9d8; color: #083e12; padding: 4px 8px; border-radius: 4px; font-weight: bold; margin-right: 8px;'>Experte 1 Spalte</span> Ground Truth Experte 1 (Oben: Präferenz / Unten: Alternativ)<br/>
        <span style='background-color: #d0ebff; color: #002b49; padding: 4px 8px; border-radius: 4px; font-weight: bold; margin-right: 8px;'>Experte 2 Spalte</span> Ground Truth Experte 2 (Oben: Präferenz / Unten: Alternativ)
    </div>
    """
    display(HTML(html))


def evaluate_primaerverband_grouped():
    _, df_norm = get_category_tables("primärverband")

    all_gt_prods = []
    for _, r in df_norm.iterrows():
        p1 = to_clean_set(r["GT1_p"])
        p2 = to_clean_set(r["GT2_p"])
        all_gt_prods.extend(list(p1) + list(p2))

    maj_prod = pd.Series(all_gt_prods).mode()[0] if all_gt_prods else "suprasorb p sensiflex"
    maj_p, maj_a = maj_prod, ""

    results = []

    models = [
        ("Baseline (Majority)", "majority"),
        ("Zero-Shot", "Zero"),
        ("Few-Shot", "Few"),
        ("Two-Stage", "Two")
    ]

    for label, pfx in models:
        f1_exp1_u, f1_exp2_u, f1_cons_u = [], [], []
        f1_exp1_g, f1_exp2_g, f1_cons_g = [], [], []

        for _, r in df_norm.iterrows():
            if pfx == "majority":
                pred_p, pred_a = maj_p, maj_a
            else:
                pred_p, pred_a = r[f"{pfx}_p"], r[f"{pfx}_a"]

            score1_u, _ = evaluate_product_match(pred_p, pred_a, r["GT1_p"], r["GT1_a"], group_by_family=False)
            score2_u, _ = evaluate_product_match(pred_p, pred_a, r["GT2_p"], r["GT2_a"], group_by_family=False)
            f1_exp1_u.append(score1_u)
            f1_exp2_u.append(score2_u)
            f1_cons_u.append(max(score1_u, score2_u))

            score1_g, _ = evaluate_product_match(pred_p, pred_a, r["GT1_p"], r["GT1_a"], group_by_family=True)
            score2_g, _ = evaluate_product_match(pred_p, pred_a, r["GT2_p"], r["GT2_a"], group_by_family=True)
            f1_exp1_g.append(score1_g)
            f1_exp2_g.append(score2_g)
            f1_cons_g.append(max(score1_g, score2_g))

        m_exp1_u, m_exp2_u, m_cons_u = np.mean(f1_exp1_u), np.mean(f1_exp2_u), np.mean(f1_cons_u)
        m_exp1_g, m_exp2_g, m_cons_g = np.mean(f1_exp1_g), np.mean(f1_exp2_g), np.mean(f1_cons_g)

        results.append({
            "Modell / Ansatz": label,
            "Exp 1 (Ungruppiert)": m_exp1_u,
            "Exp 1 (Produktfamilie)": m_exp1_g,
            "Δ Exp 1": m_exp1_g - m_exp1_u,
            "Exp 2 (Ungruppiert)": m_exp2_u,
            "Exp 2 (Produktfamilie)": m_exp2_g,
            "Δ Exp 2": m_exp2_g - m_exp2_u,
            "Best-of-Both (Ungruppiert)": m_cons_u,
            "Best-of-Both (Produktfamilie)": m_cons_g,
            "Δ Best-of-Both": m_cons_g - m_cons_u,
        })

    f1_inter_u, f1_inter_g = [], []
    for _, r in df_norm.iterrows():
        s_u, _ = evaluate_product_match(r["GT1_p"], r["GT1_a"], r["GT2_p"], r["GT2_a"], group_by_family=False)
        s_g, _ = evaluate_product_match(r["GT1_p"], r["GT1_a"], r["GT2_p"], r["GT2_a"], group_by_family=True)
        f1_inter_u.append(s_u)
        f1_inter_g.append(s_g)

    m_inter_u = np.mean(f1_inter_u)
    m_inter_g = np.mean(f1_inter_g)

    results.append({
        "Modell / Ansatz": "Experten-Übereinstimmung (Exp 1 vs Exp 2)",
        "Exp 1 (Ungruppiert)": m_inter_u,
        "Exp 1 (Produktfamilie)": m_inter_g,
        "Δ Exp 1": m_inter_g - m_inter_u,
        "Exp 2 (Ungruppiert)": m_inter_u,
        "Exp 2 (Produktfamilie)": m_inter_g,
        "Δ Exp 2": m_inter_g - m_inter_u,
        "Best-of-Both (Ungruppiert)": m_inter_u,
        "Best-of-Both (Produktfamilie)": m_inter_g,
        "Δ Best-of-Both": m_inter_g - m_inter_u,
    })

    res_df = pd.DataFrame(results)

    format_dict = {
        "Exp 1 (Ungruppiert)": "{:.1%}",
        "Exp 1 (Produktfamilie)": "{:.1%}",
        "Δ Exp 1": "{:+.1%}",
        "Exp 2 (Ungruppiert)": "{:.1%}",
        "Exp 2 (Produktfamilie)": "{:.1%}",
        "Δ Exp 2": "{:+.1%}",
        "Best-of-Both (Ungruppiert)": "{:.1%}",
        "Best-of-Both (Produktfamilie)": "{:.1%}",
        "Δ Best-of-Both": "{:+.1%}",
    }

    styler = res_df.style.format(format_dict)
    styler.set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#1e293b'), ('color', '#ffffff'), ('font-weight', 'bold'), ('text-align', 'center'), ('padding', '10px')]},
        {'selector': 'td', 'props': [('padding', '8px 12px'), ('font-size', '13px'), ('text-align', 'center')]},
        {'selector': 'table', 'props': [('border-collapse', 'collapse'), ('width', '100%')]}
    ])
    return styler


def plot_primaerverband_bar_chart(evaluation_mode="best_of_both"):
    """
    Erstellt ein Balkendiagramm für die 3 LLM-Ansätze (Zero-Shot, Few-Shot, Two-Stage).
    Für jeden der 3 Ansätze werden 7 Balken in folgender Reihenfolge angezeigt:
      1. Baseline (Random)
      2. Baseline (Majority)
      3. Expertenkonsens (ungruppiert)
      4. Expertenkonsens (gruppiert)
      5. Score (ungruppiert)
      6. Score (gruppiert)
      7. Exact Match (gruppiert)
    Insgesamt 21 Balken (3 Gruppen x 7 Balken).
    """
    _, df_norm = get_category_tables("primärverband")

    catalog_prods = [
        "suprasorb a", "suprasorb a pro", "suprasorb a + ag",
        "suprasorb p", "suprasorb p sensitive", "suprasorb p sensiflex", "suprasorb p + phmb",
        "suprasorb x", "suprasorb x pro", "suprasorb x + phmb",
        "suprasorb liquacel pro", "vliwasorb pro", "vliwasorb sensitive", "vliwazell pro",
        "solvaline n", "lomatuell pro", "vliwaktiv", "vliwaktiv ag", "suprasorb cnp"
    ]

    rng = random.Random(42)
    rand_f1_list = []
    for _ in range(100):
        run_scores = []
        for _, r in df_norm.iterrows():
            rand_p = [rng.choice(catalog_prods)]
            rand_a = [rng.choice(catalog_prods)]
            if evaluation_mode == "exp1":
                s, _ = evaluate_product_match(rand_p, rand_a, r["GT1_p"], r["GT1_a"], False)
            elif evaluation_mode == "exp2":
                s, _ = evaluate_product_match(rand_p, rand_a, r["GT2_p"], r["GT2_a"], False)
            else:
                s1, _ = evaluate_product_match(rand_p, rand_a, r["GT1_p"], r["GT1_a"], False)
                s2, _ = evaluate_product_match(rand_p, rand_a, r["GT2_p"], r["GT2_a"], False)
                s = max(s1, s2)
            run_scores.append(s)
        rand_f1_list.append(np.mean(run_scores))
    score_random = np.mean(rand_f1_list)

    all_gt_prods = []
    for _, r in df_norm.iterrows():
        p1 = to_clean_set(r["GT1_p"])
        p2 = to_clean_set(r["GT2_p"])
        all_gt_prods.extend(list(p1) + list(p2))
    maj_prod = pd.Series(all_gt_prods).mode()[0] if all_gt_prods else "suprasorb p sensiflex"

    maj_scores = []
    for _, r in df_norm.iterrows():
        if evaluation_mode == "exp1":
            s, _ = evaluate_product_match(maj_prod, "", r["GT1_p"], r["GT1_a"], False)
        elif evaluation_mode == "exp2":
            s, _ = evaluate_product_match(maj_prod, "", r["GT2_p"], r["GT2_a"], False)
        else:
            s1, _ = evaluate_product_match(maj_prod, "", r["GT1_p"], r["GT1_a"], False)
            s2, _ = evaluate_product_match(maj_prod, "", r["GT2_p"], r["GT2_a"], False)
            s = max(s1, s2)
        maj_scores.append(s)
    score_majority = np.mean(maj_scores)

    inter_scores_u, inter_scores_g = [], []
    for _, r in df_norm.iterrows():
        s_u, _ = evaluate_product_match(r["GT1_p"], r["GT1_a"], r["GT2_p"], r["GT2_a"], False)
        s_g, _ = evaluate_product_match(r["GT1_p"], r["GT1_a"], r["GT2_p"], r["GT2_a"], True)
        inter_scores_u.append(s_u)
        inter_scores_g.append(s_g)
    score_exp_konsens_u = np.mean(inter_scores_u)
    score_exp_konsens_g = np.mean(inter_scores_g)

    approaches = [
        ("Zero-Shot", "Zero"),
        ("Few-Shot", "Few"),
        ("Two-Stage", "Two")
    ]

    plot_data = []

    for label, pfx in approaches:
        sc_u_list, sc_g_list, ex_g_list = [], [], []
        for _, r in df_norm.iterrows():
            pred_p, pred_a = r[f"{pfx}_p"], r[f"{pfx}_a"]
            if evaluation_mode == "exp1":
                s_u, _ = evaluate_product_match(pred_p, pred_a, r["GT1_p"], r["GT1_a"], False)
                s_g, ex_g = evaluate_product_match(pred_p, pred_a, r["GT1_p"], r["GT1_a"], True)
            elif evaluation_mode == "exp2":
                s_u, _ = evaluate_product_match(pred_p, pred_a, r["GT2_p"], r["GT2_a"], False)
                s_g, ex_g = evaluate_product_match(pred_p, pred_a, r["GT2_p"], r["GT2_a"], True)
            else:
                s1_u, _ = evaluate_product_match(pred_p, pred_a, r["GT1_p"], r["GT1_a"], False)
                s2_u, _ = evaluate_product_match(pred_p, pred_a, r["GT2_p"], r["GT2_a"], False)
                s_u = max(s1_u, s2_u)

                s1_g, ex1_g = evaluate_product_match(pred_p, pred_a, r["GT1_p"], r["GT1_a"], True)
                s2_g, ex2_g = evaluate_product_match(pred_p, pred_a, r["GT2_p"], r["GT2_a"], True)
                s_g = max(s1_g, s2_g)
                ex_g = max(ex1_g, ex2_g)

            sc_u_list.append(s_u)
            sc_g_list.append(s_g)
            ex_g_list.append(ex_g)

        s_u_mean = np.mean(sc_u_list)
        s_g_mean = np.mean(sc_g_list)
        ex_g_mean = np.mean(ex_g_list)

        plot_data.append({
            "Ansatz": label,
            "1. Baseline (Random)": score_random,
            "2. Baseline (Majority)": score_majority,
            "3. Expertenkonsens (ungruppiert)": score_exp_konsens_u,
            "4. Expertenkonsens (gruppiert)": score_exp_konsens_g,
            "5. Score (ungruppiert)": s_u_mean,
            "6. Score (gruppiert)": s_g_mean,
            "7. Exact Match (gruppiert)": ex_g_mean
        })

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(17, 7))

    x_labels = ["Zero-Shot", "Few-Shot", "Two-Stage"]
    bar_categories = [
        "1. Baseline (Random)",
        "2. Baseline (Majority)",
        "3. Expertenkonsens (ungruppiert)",
        "4. Expertenkonsens (gruppiert)",
        "5. Score (ungruppiert)",
        "6. Score (gruppiert)",
        "7. Exact Match (gruppiert)"
    ]

    colors = ["#94a3b8", "#475569", "#8b5cf6", "#c084fc", "#f97316", "#10b981", "#06b6d4"]

    x = np.arange(len(x_labels))
    width = 0.115

    for i, cat in enumerate(bar_categories):
        values = [d[cat] for d in plot_data]
        offset = (i - 3) * width
        rects = ax.bar(x + offset, [v * 100 for v in values], width, label=cat, color=colors[i], edgecolor="black", linewidth=0.8)

        for rect in rects:
            height = rect.get_height()
            ax.annotate(f"{height:.1f}%",
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, fontfamily='sans-serif', fontweight='bold')

    ax.set_ylabel("Score / Rate (%)", fontsize=12, fontweight='bold')
    title_mode = "Best-of-Both (Konsens)" if evaluation_mode == "best_of_both" else f"vs. {evaluation_mode.upper()}"
    ax.set_title(f"Primärverband Evaluation: Metriken-Vergleich pro LLM-Ansatz ({title_mode})", fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontsize=12, fontweight='bold')
    ax.legend(title="Metriken / Balken", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, fontsize=9.5)
    ax.set_ylim(0, 85)

    plt.tight_layout()
    plt.show()


def inspection_dropdown_primaerverband():
    """
    Interaktives Dropdown für Primärverband: Wundbild auswählen und gezielt
    Präferenz- und Alternativ-Sets von Experte 1, Experte 2, Zero-Shot, Few-Shot und Two-Stage einsehen,
    inklusive Farbcodierung (Lila, Grün, Blau, Orange, Rot) für Treffer / Abweichungen.
    """
    df_raw, df_norm = get_category_tables("primärverband")
    image_ids = df_norm["image_id"].tolist()

    dropdown = widgets.Dropdown(
        options=image_ids,
        value=image_ids[0],
        description='Wundbild:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='260px')
    )

    out = widgets.Output()

    def on_change(change):
        selected_id = change['new'] if isinstance(change, dict) else change
        with out:
            out.clear_output(wait=True)
            print(f"=== PRIMÄRVERBAND EINZELINSPEKTION: {selected_id} ===")
            show_wound_image(selected_id, width=380)

            r_norm = df_norm[df_norm["image_id"] == selected_id].iloc[0]

            inspect_rows = []
            entries = [
                ("Experte 1 (Ground Truth)", "GT1_p", "GT1_a", "gt1_exp"),
                ("Experte 2 (Ground Truth)", "GT2_p", "GT2_a", "gt2_exp"),
                ("Zero-Shot", "Zero_p", "Zero_a", "Zero-Shot"),
                ("Few-Shot", "Few_p", "Few_a", "Few-Shot"),
                ("Two-Stage", "Two_p", "Two_a", "Two-Stage"),
            ]

            row_colors = []

            for label, p_key, a_key, mode in entries:
                pref_val = r_norm.get(p_key, "")
                alt_val = r_norm.get(a_key, "")
                pref_set = to_clean_set(pref_val)
                alt_set = to_clean_set(alt_val)

                pref_fam = map_product_set(pref_set, group_by_family=True)
                alt_fam = map_product_set(alt_set, group_by_family=True)

                inspect_rows.append({
                    "Akteur / Ansatz": label,
                    "Präferenz-Produkt(e)": ", ".join(pref_set) if pref_set else "—",
                    "Alternativ-Produkt(e)": ", ".join(alt_set) if alt_set else "—",
                    "Produktfamilie (Präferenz)": ", ".join(pref_fam) if pref_fam else "—",
                    "Produktfamilie (Alternativ)": ", ".join(alt_fam) if alt_fam else "—"
                })

                if mode == "gt1_exp":
                    row_colors.append("background-color: #d3f9d8; color: #083e12; font-weight: bold;")
                elif mode == "gt2_exp":
                    row_colors.append("background-color: #d0ebff; color: #002b49; font-weight: bold;")
                else:
                    status = classify_row_match(r_norm, mode, "primärverband")
                    if status == "both":
                        row_colors.append("background-color: #eebefa; color: #360745; font-weight: bold;")
                    elif status == "gt1":
                        row_colors.append("background-color: #c3fae8; color: #044229; font-weight: bold;")
                    elif status == "gt2":
                        row_colors.append("background-color: #d0ebff; color: #002b49; font-weight: bold;")
                    elif status == "partial":
                        row_colors.append("background-color: #fff3bf; color: #594200; font-weight: bold;")
                    else:
                        row_colors.append("background-color: #ffe3e3; color: #7a0000; font-weight: bold;")

            res_df = pd.DataFrame(inspect_rows)

            def apply_row_styles(row):
                idx = row.name
                color_style = row_colors[idx]
                return [color_style] * len(row)

            styler = res_df.style.apply(apply_row_styles, axis=1)
            styler.set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#1e293b'), ('color', '#ffffff'), ('font-weight', 'bold'), ('text-align', 'center'), ('padding', '8px')]},
                {'selector': 'td', 'props': [('padding', '8px 12px'), ('font-size', '13px'), ('text-align', 'left')]},
                {'selector': 'table', 'props': [('border-collapse', 'collapse'), ('width', '100%')]}
            ])

            display(HTML(styler.to_html()))

    dropdown.observe(on_change, names='value')

    display(dropdown)
    display(out)
    on_change(image_ids[0])


def get_discrepancies(category_key=None):
    df_raw, df_norm = get_category_tables(category_key or "wundtyp")
    key = getattr(df_norm, "_category_key", category_key or "wundtyp")
    discrepant_rows = []

    for _, row in df_norm.iterrows():
        z_status = classify_row_match(row, "Zero-Shot", key)
        f_status = classify_row_match(row, "Few-Shot", key)
        t_status = classify_row_match(row, "Two-Stage", key)

        if any(s in ["partial", "none"] for s in [z_status, f_status, t_status]):
            discrepant_rows.append(row["image_id"])

    df_disc_raw = df_raw[df_raw["image_id"].isin(discrepant_rows)]
    df_disc_norm = df_norm[df_norm["image_id"].isin(discrepant_rows)]
    df_disc_raw._category_key = key
    df_disc_norm._category_key = key
    return df_disc_raw, df_disc_norm


def get_failed_cases(category_key=None):
    df_raw, df_norm = get_category_tables(category_key or "wundtyp")
    key = getattr(df_norm, "_category_key", category_key or "wundtyp")
    failed_rows = []

    for _, row in df_norm.iterrows():
        z_status = classify_row_match(row, "Zero-Shot", key)
        f_status = classify_row_match(row, "Few-Shot", key)
        t_status = classify_row_match(row, "Two-Stage", key)

        if z_status == "none" and f_status == "none" and t_status == "none":
            failed_rows.append(row["image_id"])

    df_failed_raw = df_raw[df_raw["image_id"].isin(failed_rows)]
    df_failed_norm = df_norm[df_norm["image_id"].isin(failed_rows)]
    df_failed_raw._category_key = key
    df_failed_norm._category_key = key
    return df_failed_raw, df_failed_norm


def show_wound_image(image_id, width=350):
    match = re.search(r"wunde_(\d+)", image_id)
    if match:
        num = int(match.group(1))
        file_name = f"Bild{num}.jpg"
        file_path = os.path.join(IMAGE_DIR, file_name)
        if os.path.exists(file_path):
            display(Image(filename=file_path, width=width))
            return
        for root, _, files in os.walk(IMAGE_DIR):
            if file_name in files:
                display(Image(filename=os.path.join(root, file_name), width=width))
                return
        print(f"Bild {file_name} nicht gefunden in {IMAGE_DIR}")
    else:
        print(f"Ungültiges Bild-ID Format: {image_id}")


def interactive_inspection(category_key=None):
    df_raw, df_norm = get_category_tables(category_key or "wundtyp")
    key = getattr(df_norm, "_category_key", category_key or "wundtyp")
    image_ids = df_raw["image_id"].tolist()

    dropdown = widgets.Dropdown(
        options=image_ids,
        value=image_ids[0],
        description='Wundbild:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='250px')
    )

    out = widgets.Output()

    def on_change(change):
        selected_id = change['new'] if isinstance(change, dict) else change
        with out:
            out.clear_output(wait=True)
            print(f"=== WUNDBILD: {selected_id} ===")
            show_wound_image(selected_id)

            display_legend()

            row_raw = df_raw[df_raw["image_id"] == selected_id]
            row_norm = df_norm[df_norm["image_id"] == selected_id]

            print("--- ROH-ANTWORTEN (RAW) ---")
            display(style_category_table(row_raw, key))

            print("\n--- NORMALISIERTE ANTWORTEN (NORMALISED) ---")
            display(style_category_table(row_norm, key))

    dropdown.observe(on_change, names='value')

    display(dropdown)
    display(out)

    # Trigger initial view
    on_change(image_ids[0])


def analyze_primaerverband_failed_cases():
    """
    Analysiert und visualisiert die 5 absoluten Härtefälle beim Primärverband,
    bei denen alle 3 LLM-Ansätze (Zero-Shot, Few-Shot, Two-Stage) F1 = 0% erzielen.
    """
    df_raw, df_norm = get_category_tables("primärverband")

    failed_ids = []
    for _, r in df_norm.iterrows():
        z_g1, _ = evaluate_product_match(r['Zero_p'], r['Zero_a'], r['GT1_p'], r['GT1_a'], True)
        z_g2, _ = evaluate_product_match(r['Zero_p'], r['Zero_a'], r['GT2_p'], r['GT2_a'], True)
        f_g1, _ = evaluate_product_match(r['Few_p'], r['Few_a'], r['GT1_p'], r['GT1_a'], True)
        f_g2, _ = evaluate_product_match(r['Few_p'], r['Few_a'], r['GT2_p'], r['GT2_a'], True)
        t_g1, _ = evaluate_product_match(r['Two_p'], r['Two_a'], r['GT1_p'], r['GT1_a'], True)
        t_g2, _ = evaluate_product_match(r['Two_p'], r['Two_a'], r['GT2_p'], r['GT2_a'], True)

        if max(z_g1, z_g2) == 0 and max(f_g1, f_g2) == 0 and max(t_g1, t_g2) == 0:
            failed_ids.append(r['image_id'])

    print(f"=== ABSOLUTE HÄRTEFÄLLE (PRIMÄRVERBAND): {len(failed_ids)} VON 60 WUNDBILDERN ({(len(failed_ids)/60)*100:.1f}%) ===")
    print("Bei diesen 5 Wundbildern erzielt kein einziger LLM-Ansatz einen Treffer auf Produktfamilien-Ebene.\n")

    dropdown = widgets.Dropdown(
        options=failed_ids,
        value=failed_ids[0],
        description='Härtefall Wundbild:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='280px')
    )

    out = widgets.Output()

    def on_change(change):
        selected_id = change['new'] if isinstance(change, dict) else change
        with out:
            out.clear_output(wait=True)
            print(f"=== PRIMÄRVERBAND HÄRTEFALL: {selected_id} ===")
            show_wound_image(selected_id, width=380)

            r_norm = df_norm[df_norm["image_id"] == selected_id].iloc[0]

            rows = []
            entries = [
                ("Experte 1 (Ground Truth)", "GT1_p", "GT1_a"),
                ("Experte 2 (Ground Truth)", "GT2_p", "GT2_a"),
                ("Zero-Shot", "Zero_p", "Zero_a"),
                ("Few-Shot", "Few_p", "Few_a"),
                ("Two-Stage", "Two_p", "Two_a"),
            ]

            for label, p_key, a_key in entries:
                pref_set = to_clean_set(r_norm.get(p_key, ""))
                alt_set = to_clean_set(r_norm.get(a_key, ""))
                pref_fam = map_product_set(pref_set, group_by_family=True)
                alt_fam = map_product_set(alt_set, group_by_family=True)

                rows.append({
                    "Akteur / Ansatz": label,
                    "Präferenz-Produkt(e)": ", ".join(pref_set) if pref_set else "—",
                    "Alternativ-Produkt(e)": ", ".join(alt_set) if alt_set else "—",
                    "Produktfamilie (Präferenz)": ", ".join(pref_fam) if pref_fam else "—",
                    "Produktfamilie (Alternativ)": ", ".join(alt_fam) if alt_fam else "—"
                })

            res_df = pd.DataFrame(rows)
            styler = res_df.style.set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#7f1d1d'), ('color', '#ffffff'), ('font-weight', 'bold'), ('text-align', 'center'), ('padding', '8px')]},
                {'selector': 'td', 'props': [('padding', '8px 12px'), ('font-size', '13px'), ('text-align', 'left')]},
                {'selector': 'table', 'props': [('border-collapse', 'collapse'), ('width', '100%')]}
            ])
            display(HTML(styler.to_html()))

    dropdown.observe(on_change, names='value')
    display(dropdown)
    display(out)
    on_change(failed_ids[0])


def plot_primaerverband_confusion_matrix(model_approach="Two-Stage", evaluation_mode="best_of_both"):
    """
    Erstellt eine Heatmap-Verwechslungsmatrix (Confusion Matrix) der Produktfamilien
    zwischen den Experten-Empfehlungen und den Modell-Vorhersagen.
    """
    _, df_norm = get_category_tables("primärverband")

    pfx_map = {"Zero-Shot": "Zero", "Few-Shot": "Few", "Two-Stage": "Two"}
    pfx = pfx_map.get(model_approach, "Two")

    main_labels = [
        'Suprasorb P (Schaumstoff)',
        'Suprasorb A (Alginat)',
        'Suprasorb Liquacel (Hydrofiber)',
        'Vliwasorb (Superabsorber)',
        'Suprasorb X (Hydrobalance)',
        'Solvaline / Lomatuell (Atraumatische Auflage)',
        'Suprasorb G (Gel)',
        'Suprasorb CNP (NPWT)'
    ]

    gt_list, pred_list = [], []

    for _, r in df_norm.iterrows():
        p_set = to_clean_set(r[f"{pfx}_p"])
        p_fam = list(map_product_set(p_set, group_by_family=True))

        g1_set = to_clean_set(r["GT1_p"])
        g2_set = to_clean_set(r["GT2_p"])

        if evaluation_mode == "exp1":
            g_fam = list(map_product_set(g1_set, group_by_family=True))
        elif evaluation_mode == "exp2":
            g_fam = list(map_product_set(g2_set, group_by_family=True))
        else:
            g_fam = list(set(list(map_product_set(g1_set, True)) + list(map_product_set(g2_set, True))))

        if not g_fam: g_fam = ["Sonstige / Keine"]
        if not p_fam: p_fam = ["Sonstige / Keine"]

        for g in g_fam:
            g_clean = g if g in main_labels else "Sonstige / Keine"
            for p in p_fam:
                p_clean = p if p in main_labels else "Sonstige / Keine"
                gt_list.append(g_clean)
                pred_list.append(p_clean)

    labels_order = [l for l in main_labels if l in gt_list or l in pred_list] + ["Sonstige / Keine"]

    cm = pd.crosstab(
        pd.Series(gt_list, name='Ground Truth (Experten)'),
        pd.Series(pred_list, name=f'Modell ({model_approach})')
    ).reindex(index=labels_order, columns=labels_order, fill_value=0)

    sns.set_theme(style="white")
    fig, ax = plt.subplots(figsize=(11, 8.5))

    sns.heatmap(cm, annot=True, fmt='d', cmap='YlGnBu', cbar=True, ax=ax, linewidths=0.5, linecolor='gray')

    title_mode = "Best-of-Both Konsens" if evaluation_mode == "best_of_both" else f"vs. {evaluation_mode.upper()}"
    ax.set_title(f"Verwechslungsmatrix Produktfamilien (Primärverband): {model_approach} ({title_mode})", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel(f"Modell-Vorhersage ({model_approach})", fontsize=11, fontweight='bold')
    ax.set_ylabel("Ground Truth (Experten-Empfehlung)", fontsize=11, fontweight='bold')

    plt.xticks(rotation=45, ha='right', fontsize=9.5)
    plt.yticks(rotation=0, fontsize=9.5)

    plt.tight_layout()
    plt.show()


