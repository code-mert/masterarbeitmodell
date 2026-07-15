import os
import sys
import re
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, HTML

# Ensure parent directory (project root) is in the path to allow loading eval module and utils
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils_notebook import metrics, clean

def resolve_path(rel_path):
    """
    Sucht robust nach dem übergebenen Pfad ausgehend vom aktuellen Arbeitsverzeichnis
    oder dem Projekt-Root.
    """
    if os.path.exists(rel_path):
        return os.path.abspath(rel_path)
        
    current = os.path.abspath(os.path.dirname(__file__))
    for _ in range(5):
        if os.path.exists(os.path.join(current, "data")):
            cleaned_rel = rel_path.replace("../", "")
            full = os.path.join(current, cleaned_rel)
            if os.path.exists(full):
                return full
        current = os.path.dirname(current)
        
    return os.path.abspath(rel_path)

def load_csv(path):
    """Lädt eine CSV-Datei mit automatischer Trennzeichen-Erkennung."""
    if not os.path.exists(path):
        print(f"Fehler: Datei existiert nicht: {path}")
        return pd.DataFrame()
    try:
        with open(path, "r", encoding="utf-8") as f:
            first_line = f.readline()
            sep = ";" if ";" in first_line else ","
        df = pd.read_csv(path, sep=sep).fillna("")
        return df
    except Exception as e:
        print(f"Fehler beim Laden von {path}: {e}")
        return pd.DataFrame()

def normalize_image_id(image_id):
    """Normalisiert die Bild-ID auf das Format wunde_XX."""
    if not isinstance(image_id, str):
        image_id = str(image_id)
    match = re.search(r"(\d+)", image_id)
    if match:
        num = int(match.group(1))
        return f"wunde_{num:02d}"
    return image_id

def extract_product_set(record, keys):
    """
    Extrahiert alle Produktbezeichnungen (Debridement, Primärverband, Sekundärverband)
    aus den angegebenen Schlüsseln eines Datensatzes und kombiniert sie in ein bereinigtes Set.
    """
    combined_set = set()
    for k in keys:
        val = record.get(k)
        if val is None or (isinstance(val, float) and pd.isna(val)):
            continue
        cleaned_val = clean.clean_whitespace(val)
        items = metrics.to_clean_set(cleaned_val)
        combined_set.update(items)
    return combined_set

def format_set_display(product_set):
    """Formatiert ein Produktset als lesbaren, sortierten Komma-String."""
    if not product_set:
        return "—"
    return ", ".join(sorted(list(product_set)))

def calculate_product_sets_comparison(path_llm=None):
    """
    Berechnet die kombinierten F1-Scores für alle Produktsets (Debridement-Methode, 
    Primärverband und Sekundärverband zusammen) für Phase 1 (normalisiert).
    
    Vergleicht:
    1. Experten-Einigkeit untereinander (Experte 1 vs. Experte 2)
    2. LLM vs. Experte 1
    3. LLM vs. Experte 2
    4. LLM Best Match (Max F1 aus LLM vs Exp 1 und LLM vs Exp 2)
    
    Rückgabe:
    - df_summary: Zusammenfassung der durchschnittlichen Scores
    - df_detail: Detailtabelle pro Wunde
    """
    path_gt1 = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv")
    path_gt2 = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv")
    path_llm = resolve_path(path_llm) if path_llm else resolve_path("../../data/llm_outputs/zero_shot_lr/zero_shot_lr_normalised.csv")
    
    df_gt1 = load_csv(path_gt1)
    df_gt2 = load_csv(path_gt2)
    df_llm = load_csv(path_llm)
    
    for df in [df_gt1, df_gt2, df_llm]:
        if not df.empty and "image_id" in df.columns:
            df["image_id"] = df["image_id"].apply(normalize_image_id)
            
    all_ids = []
    if not df_llm.empty:
        all_ids = sorted(df_llm["image_id"].dropna().unique().tolist())
    if not all_ids:
        all_ids = [f"wunde_{i:02d}" for i in range(1, 61)]
        
    gt_product_keys = [
        "debridement",
        "praeferenz_produkt",
        "alternative_produkt",
        "ergaenzende_produkte_praeferenz",
        "ergaenzende_produkte_alternativ"
    ]
    
    llm_product_keys = [
        "debridement_methode",
        "praeferenz_wundauflage",
        "alternativ_wundauflage",
        "praeferenz_ergaenzung",
        "alternativ_ergaenzung"
    ]
    
    detail_rows = []
    
    for img_id in all_ids:
        sub_gt1 = df_gt1[df_gt1["image_id"] == img_id] if not df_gt1.empty else pd.DataFrame()
        sub_gt2 = df_gt2[df_gt2["image_id"] == img_id] if not df_gt2.empty else pd.DataFrame()
        sub_llm = df_llm[df_llm["image_id"] == img_id] if not df_llm.empty else pd.DataFrame()
        
        rec_gt1 = sub_gt1.iloc[0].to_dict() if not sub_gt1.empty else {}
        rec_gt2 = sub_gt2.iloc[0].to_dict() if not sub_gt2.empty else {}
        rec_llm = sub_llm.iloc[0].to_dict() if not sub_llm.empty else {}
        
        set_gt1 = extract_product_set(rec_gt1, gt_product_keys)
        set_gt2 = extract_product_set(rec_gt2, gt_product_keys)
        set_llm = extract_product_set(rec_llm, llm_product_keys)
        
        f1_experts = metrics.calculate_f1(set_gt1, set_gt2)
        f1_llm_exp1 = metrics.calculate_f1(set_llm, set_gt1)
        f1_llm_exp2 = metrics.calculate_f1(set_llm, set_gt2)
        f1_llm_best = max(f1_llm_exp1, f1_llm_exp2)
        f1_llm_mean = (f1_llm_exp1 + f1_llm_exp2) / 2.0
        
        detail_rows.append({
            "image_id": img_id,
            "Experte 1 Produktset": format_set_display(set_gt1),
            "Experte 2 Produktset": format_set_display(set_gt2),
            "LLM Output Produktset": format_set_display(set_llm),
            "Experten-Einigkeit (F1)": f1_experts,
            "LLM vs Exp 1 (F1)": f1_llm_exp1,
            "LLM vs Exp 2 (F1)": f1_llm_exp2,
            "LLM Best Match (F1)": f1_llm_best,
            "LLM Mean (F1)": f1_llm_mean
        })
        
    df_detail = pd.DataFrame(detail_rows)
    
    # Natürliche Sortierung nach Wund-ID
    if not df_detail.empty:
        df_detail = df_detail.sort_values(
            by="image_id",
            key=lambda x: x.str.extract(r"(\d+)")[0].astype(float)
        ).reset_index(drop=True)
        
    mean_experts = df_detail["Experten-Einigkeit (F1)"].mean() if not df_detail.empty else 0.0
    mean_llm_exp1 = df_detail["LLM vs Exp 1 (F1)"].mean() if not df_detail.empty else 0.0
    mean_llm_exp2 = df_detail["LLM vs Exp 2 (F1)"].mean() if not df_detail.empty else 0.0
    mean_llm_best = df_detail["LLM Best Match (F1)"].mean() if not df_detail.empty else 0.0
    mean_llm_avg = df_detail["LLM Mean (F1)"].mean() if not df_detail.empty else 0.0
    
    summary_rows = [
        {"Metrik / Vergleich": "Experten-Einigkeit untereinander (F1 Mean)", "Score / F1-Score": mean_experts},
        {"Metrik / Vergleich": "LLM vs. Experte 1 (F1 Mean)", "Score / F1-Score": mean_llm_exp1},
        {"Metrik / Vergleich": "LLM vs. Experte 2 (F1 Mean)", "Score / F1-Score": mean_llm_exp2},
        {"Metrik / Vergleich": "LLM Best Match (Max F1 Mean)", "Score / F1-Score": mean_llm_best},
        {"Metrik / Vergleich": "LLM Durchschnitt (Mean F1)", "Score / F1-Score": mean_llm_avg},
    ]
    
    df_summary = pd.DataFrame(summary_rows)
    
    return df_summary, df_detail

def display_product_sets_comparison(path_llm=None):
    """
    Berechnet die Produktsets-Vergleichsdaten und stellt sie stilvoll im Notebook dar.
    Zeigt zuerst die Übersicht der Durchschnittswerte und dann die interaktive/vollständige Detailtabelle.
    """
    df_summary, df_detail = calculate_product_sets_comparison(path_llm=path_llm)
    
    # 1. Darstellung der Zusammenfassung
    display(HTML("<h3 style='font-family: Segoe UI, Arial, sans-serif; color: #1d3557; margin-bottom: 10px;'>Gesamt-Vergleich der kombinierten Produktsets (Debridement + Primärverband + Sekundärverband)</h3>"))
    
    summary_styler = df_summary.style.format({
        "Score / F1-Score": "{:.1%}"
    }).hide(axis="index").set_table_styles([
        {"selector": "th", "props": [
            ("background-color", "#1d3557"), ("color", "white"),
            ("font-family", "Segoe UI, Arial, sans-serif"), ("font-size", "14px"),
            ("font-weight", "bold"), ("padding", "8px 12px"), ("text-align", "left")
        ]},
        {"selector": "td", "props": [
            ("font-family", "Segoe UI, Arial, sans-serif"), ("font-size", "13px"),
            ("padding", "8px 12px"), ("border-bottom", "1px solid #e2e8f0")
        ]}
    ])
    display(summary_styler)
    
    # 2. Darstellung der Detailtabelle
    display(HTML("<h3 style='font-family: Segoe UI, Arial, sans-serif; color: #1d3557; margin-top: 25px; margin-bottom: 10px;'>Detailergebnisse pro Wunde</h3>"))
    
    # Vorformatierte Darstellung für HTML
    df_display = df_detail.copy()
    
    score_cols = ["Experten-Einigkeit (F1)", "LLM vs Exp 1 (F1)", "LLM vs Exp 2 (F1)", "LLM Best Match (F1)"]
    
    def apply_score_style(val):
        if pd.isna(val):
            return "background-color: #ffffff; color: #333333;"
        if val >= 0.999:
            return "background-color: #d4edda; color: #155724; font-weight: bold;" # Grün (100%)
        elif val > 0.001:
            return "background-color: #fff3cd; color: #856404;" # Orange (>0%)
        else:
            return "background-color: #f8d7da; color: #721c24;" # Rot (0%)

    styler = df_display.style.format({
        "Experten-Einigkeit (F1)": "{:.1%}",
        "LLM vs Exp 1 (F1)": "{:.1%}",
        "LLM vs Exp 2 (F1)": "{:.1%}",
        "LLM Best Match (F1)": "{:.1%}",
        "LLM Mean (F1)": "{:.1%}"
    })
    
    map_func = getattr(styler, "map", getattr(styler, "applymap", None))
    styler = map_func(apply_score_style, subset=score_cols)
    
    styler = styler.hide(axis="index")
    styler = styler.set_table_styles([
        {"selector": "th", "props": [
            ("background-color", "#1d3557"), ("color", "white"),
            ("font-family", "Segoe UI, Arial, sans-serif"), ("font-size", "13px"),
            ("font-weight", "bold"), ("padding", "8px 10px"), ("border", "1px solid #d3d3d3"),
            ("text-align", "center")
        ]},
        {"selector": "td", "props": [
            ("font-family", "Segoe UI, Arial, sans-serif"), ("font-size", "12px"),
            ("padding", "6px 8px"), ("border", "1px solid #e2e8f0"),
            ("vertical-align", "top")
        ]}
    ])
    
    # Spaltenbreiten optimieren
    styler = styler.set_properties(subset=["image_id"], **{"width": "8%", "text-align": "center", "font-weight": "bold"})
    styler = styler.set_properties(subset=["Experte 1 Produktset", "Experte 2 Produktset", "LLM Output Produktset"], **{"width": "24%"})
    styler = styler.set_properties(subset=score_cols + ["LLM Mean (F1)"], **{"width": "9%", "text-align": "center"})
    
    display(styler)
    
    return df_summary, df_detail

if __name__ == "__main__":
    df_s, df_d = calculate_product_sets_comparison()
    print("--- ZUSAMMENFASSUNG ---")
    print(df_s.to_string(index=False))
