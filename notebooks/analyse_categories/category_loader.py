import os
import sys
import re
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, Image, HTML

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
    """
    Erstellt zwei DataFrames (df_raw und df_norm) für eine bestimmte Kategorie.
    Spalten: ['image_id', 'Experte 1', 'Experte 2', 'Zero-Shot', 'Few-Shot', 'Two-Stage']
    """
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


def evaluate_product_match(pred_p, pred_a, gt_p, gt_a):
    """
    Nutzt best_path_f1 aus eval/metrics.py für Produkt-Sets.
    Returns (f1_score, exact_match_bool).
    """
    p_set = to_clean_set(pred_p)
    a_set = to_clean_set(pred_a)
    gp_set = to_clean_set(gt_p)
    ga_set = to_clean_set(gt_a)

    f1, exact, _, _ = best_path_f1(p_set, a_set, gp_set, ga_set)
    return f1, exact


def classify_row_match(row, col_name, category_key):
    """
    Klassifiziert den Match-Status eines LLM-Ansatzes relativ zu Experte 1 und Experte 2
    unter Verwendung der offiziellen eval/metrics.py Metriken.
    """
    prefix_map = {
        "Zero-Shot": "Zero",
        "Few-Shot": "Few",
        "Two-Stage": "Two"
    }
    pfx = prefix_map[col_name]
    key = category_key.lower().strip()

    is_product = key in ["primaerverband", "primärverband", "sekundaerverband", "sekundärverband"]

    if is_product:
        f1_1, exact_1 = evaluate_product_match(row[f"{pfx}_p"], row[f"{pfx}_a"], row["GT1_p"], row["GT1_a"])
        f1_2, exact_2 = evaluate_product_match(row[f"{pfx}_p"], row[f"{pfx}_a"], row["GT2_p"], row["GT2_a"])

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
        # Standard Single-String / Checklist Matching
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


def style_category_table(df, category_key=None):
    """
    Färbt die Tabelle basierend auf Übereinstimmung unter Verwendung der eval/metrics.py Logik.
    - Lila (#e2d9f3): Exakter Match (F1=1.0) mit BEIDEN Experten
    - Grün (#c3fae8): Exakter Match (F1=1.0) mit Experte 1
    - Blau (#d0ebff): Exakter Match (F1=1.0) mit Experte 2
    - Orange (#fff3bf): Teilweiser Match (F1 > 0)
    - Rot (#ffe3e3): Kein Match (F1 = 0)
    """
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
                status = classify_row_match(orig_row, col_name, category_key)
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


def get_discrepancies(category_key=None):
    """
    Filtert alle Wundbeispiele heraus, bei denen mindestens ein LLM-Ansatz abweicht oder nur teilweise übereinstimmt.
    """
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
    """
    Filtert die Wundbeispiele heraus, bei denen ALLE 3 LLM-Ansätze (Zero-Shot, Few-Shot, Two-Stage)
    keine Übereinstimmung mit einem der Experten erzielen konnten (alle 3 auf 'none' / Rot).
    """
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
