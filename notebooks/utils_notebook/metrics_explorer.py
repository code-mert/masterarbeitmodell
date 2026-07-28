import os
import sys
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output

# Ensure parent directory (project root) is in the path to allow loading eval module
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from eval.loaders import load_ground_truth, load_llm_outputs, matched_image_ids
from utils_notebook import clean, metrics

# =====================================================================
# COLUMN & CATEGORY CONFIGURATION
# =====================================================================
COLUMN_MAPPING = {
    "spuelloesung": "spuelloesung",
    "debridement_notwendig": "debridement_notwendig",
    "antimikrobiell_notwendig": "antimikrobieller_verband",
    "kompression_indiziert": "kompression_indiziert",
    "exsudat": "exsudat_menge",
    "infektion": "infektionsstatus",
    "wundtyp": "wundtyp",
    "lokalisation": "lokalisation",
    "wundstadium": "wundphase",
    "wundrand": "wundrand",
    "wundumgebung": "wundumgebung",
    "debridement": "debridement_methode",
    "praeferenz_produkt": "praeferenz_verbandklasse",
    "alternative_produkt": "alternativ_verbandklasse",
    "antimikrobielles_agens": "antimikrobielles_agens",
    "sekundaerverband": "sekundaerverband_fixierung",
    "hautschutz": "wundrand_hautschutz",
    "kompression_produkte": "kompression_art",
    "wundtyp_spezifikation": "wundtyp_spezifizierung",
    "auffaelligkeiten": "weitere_auffaelligkeiten",
    "einschraenkungen": "einschraenkungen_annahmen",
}

CATEGORY_TYPES = {
    "exact": ["debridement_notwendig", "antimikrobiell_notwendig", "kompression_indiziert", "wundtyp"],
    "ordinal": ["exsudat", "infektion"],
    "decode": ["lokalisation"],
    "checklist": ["spuelloesung", "wundstadium", "wundrand", "wundumgebung", "debridement", "praeferenz_produkt", 
                  "alternative_produkt", "antimikrobielles_agens", "sekundaerverband", "hautschutz", "kompression_produkte"],
    "skip": ["wundtyp_spezifikation", "auffaelligkeiten", "einschraenkungen"]
}

# =====================================================================
# EVALUATION RUNNER
# =====================================================================
def calculate_scores(csv_path: str, json_dir: str, raw: bool = False) -> pd.DataFrame:
    """
    Berechnet die Scores für alle Wundbilder.
    Wenn raw=True, werden keine Mappings oder Säuberungen durchgeführt (Phase 0).
    Wenn raw=False, werden Spelling-Mapping, Whitespace-Bereinigung und Dekodierungen angewendet (Phase 1).
    """
    gt_data = load_ground_truth(csv_path)
    llm_data = load_llm_outputs(json_dir)
    matched_ids = matched_image_ids(gt_data, llm_data)

    is_lr = False
    if matched_ids:
        sample_llm = llm_data[matched_ids[0]]
        is_lr = "praeferenz_wundauflage" in sample_llm

    if is_lr:
        col_mapping = {
            "spuelloesung": "spuelloesung",
            "debridement_notwendig": "debridement_notwendig",
            "kompression_indiziert": "kompression_indiziert",
            "exsudat": "exsudat_menge",
            "infektion": "infektion_vorhanden",
            "wundtyp": "wundtyp",
            "lokalisation": "lokalisation",
            "wundstadium": "wundstadium",
            "wundrand": "wundrand",
            "wundumgebung": "wundumgebung",
            "debridement": "debridement_methode",
            "praeferenz_produkt": "praeferenz_wundauflage",
            "alternative_produkt": "alternativ_wundauflage",
            "ergaenzende_produkte_praeferenz": "praeferenz_ergaenzung",
            "ergaenzende_produkte_alternativ": "alternativ_ergaenzung",
            "kompression_produkte": "kompression_produkt",
            "wundtyp_spezifikation": "wundtyp_spezifizierung",
            "auffaelligkeiten": "weitere_auffaelligkeiten",
            "einschraenkungen": "einschraenkungen_annahmen",
            "wundgrund": "wundgrund"
        }
    else:
        col_mapping = COLUMN_MAPPING

    results = []
    for img_id in matched_ids:
        gt_rec = gt_data[img_id]
        llm_rec = llm_data[img_id]
        
        row_scores = {"image_id": img_id}
        
        # 1. Berechnung für Primärverband (best-path cross-match)
        llm_p_col = col_mapping["praeferenz_produkt"]
        llm_a_col = col_mapping["alternative_produkt"]
        if raw:
            gt_p = metrics.to_clean_set(gt_rec.get("praeferenz_produkt"))
            gt_a = metrics.to_clean_set(gt_rec.get("alternative_produkt"))
            llm_p = metrics.to_clean_set(llm_rec.get(llm_p_col))
            llm_a = metrics.to_clean_set(llm_rec.get(llm_a_col))
        else:
            gt_p = metrics.to_clean_set(clean.clean_whitespace(gt_rec.get("praeferenz_produkt")))
            gt_a = metrics.to_clean_set(clean.clean_whitespace(gt_rec.get("alternative_produkt")))
            llm_p = metrics.to_clean_set(clean.clean_whitespace(llm_rec.get(llm_p_col)))
            llm_a = metrics.to_clean_set(clean.clean_whitespace(llm_rec.get(llm_a_col)))
            
        prim_f1, prim_exact = metrics.best_path_f1(llm_p, llm_a, gt_p, gt_a)
        row_scores["primaerverband_f1"] = prim_f1
        row_scores["primaerverband_exact"] = prim_exact
        
        # 2. Übrige Kategorien
        for gt_col, llm_col in col_mapping.items():
            if gt_col in ["praeferenz_produkt", "alternative_produkt"]:
                continue
                
            gt_val = gt_rec.get(gt_col)
            llm_val = llm_rec.get(llm_col)
            
            # Wundtyp: Merge mit Sonstiges-Freitexten
            if gt_col == "wundtyp":
                # Für GT: wundtyp_spezifikation
                gt_val = clean.merge_wundtyp_sonstiges(gt_val, gt_rec.get("wundtyp_spezifikation"))
                # Für LLM: wundtyp_sonstiges
                llm_val = clean.merge_wundtyp_sonstiges(llm_val, llm_rec.get("wundtyp_sonstiges"))
            
            # Säubern/Bereinigen falls nicht raw
            if not raw:
                gt_val_c = clean.clean_whitespace(gt_val)
                llm_val_c = clean.clean_whitespace(llm_val)
            else:
                gt_val_c = gt_val
                llm_val_c = llm_val

            score = None
            exact = None
            
            if gt_col in CATEGORY_TYPES["exact"]:
                if gt_col == "wundtyp":
                    if raw:
                        score = 1.0 if metrics.to_clean_set(gt_val_c) == metrics.to_clean_set(llm_val_c) else 0.0
                    else:
                        gt_mapped = metrics.to_clean_set(clean.normalise_wundtyp(gt_val_c))
                        llm_mapped = metrics.to_clean_set(clean.normalise_wundtyp(llm_val_c))
                        score = 1.0 if gt_mapped == llm_mapped else 0.0
                else:
                    score = metrics.score_exact(gt_val_c, llm_val_c)
                row_scores[f"{gt_col}_exact"] = score
                
            elif gt_col in CATEGORY_TYPES["ordinal"]:
                score, exact = metrics.score_ordinal(gt_col, gt_val_c, llm_val_c)
                row_scores[f"{gt_col}_score"] = score
                row_scores[f"{gt_col}_exact"] = exact
                
            elif gt_col in CATEGORY_TYPES["decode"]:
                if gt_col == "lokalisation":
                    if raw:
                        score, exact = metrics.evaluate_checklist(gt_val_c, llm_val_c)
                    else:
                        gt_mapped = metrics.to_clean_set(clean.normalise_lokalisation(gt_val_c))
                        llm_mapped = metrics.to_clean_set(clean.normalise_lokalisation(llm_val_c))
                        score = metrics.calculate_f1(gt_mapped, llm_mapped)
                        exact = 1.0 if gt_mapped == llm_mapped else 0.0
                
                row_scores[f"{gt_col}_f1"] = score
                row_scores[f"{gt_col}_exact"] = exact
                
            elif gt_col in CATEGORY_TYPES["checklist"]:
                score, exact = metrics.evaluate_checklist(gt_val_c, llm_val_c)
                row_scores[f"{gt_col}_f1"] = score
                row_scores[f"{gt_col}_exact"] = exact
                
        results.append(row_scores)

    df_scores = pd.DataFrame(results)
    
    # Natürliche Sortierung nach Wund-ID
    if not df_scores.empty:
        df_scores = df_scores.sort_values(
            by='image_id',
            key=lambda x: x.str.extract(r'(\d+)')[0].astype(float)
        ).reset_index(drop=True)
        
    return df_scores

def calculate_summary(df_scores: pd.DataFrame) -> pd.DataFrame:
    """
    Berechnet den Durchschnitt über alle Wundbilder.
    """
    base_categories = {
        "primaerverband": "checklist (best path)",
        "spuelloesung": "checklist",
        "debridement_notwendig": "exact",
        "antimikrobiell_notwendig": "exact",
        "kompression_indiziert": "exact",
        "exsudat": "ordinal",
        "infektion": "ordinal",
        "wundtyp": "exact",
        "lokalisation": "decode",
        "wundstadium": "checklist",
        "wundrand": "checklist",
        "wundumgebung": "checklist",
        "debridement": "checklist",
        "antimikrobielles_agens": "checklist",
        "sekundaerverband": "checklist",
        "hautschutz": "checklist",
        "kompression_produkte": "checklist",
        "wundgrund": "checklist",
    }
    
    # Active categories filtering based on which columns exist in df_scores
    active_categories = {}
    for cat, cat_type in base_categories.items():
        cols = [f"{cat}_f1", f"{cat}_score", f"{cat}_exact"]
        if any(col in df_scores.columns for col in cols):
            active_categories[cat] = cat_type
            
    summary_rows = []
    for cat, cat_type in active_categories.items():
        if cat_type in ["checklist", "checklist (best path)", "decode"]:
            score_col = f"{cat}_f1"
        elif cat_type == "ordinal":
            score_col = f"{cat}_score"
        else:
            score_col = f"{cat}_exact"
            
        exact_col = f"{cat}_exact"
        
        mean_score = df_scores[score_col].mean() if score_col in df_scores.columns else float('nan')
        mean_exact = df_scores[exact_col].mean() if exact_col in df_scores.columns else float('nan')
        
        summary_rows.append({
            "Kategorie": cat,
            "Typ": cat_type,
            "Score / F1-Score (Mean)": mean_score,
            "Exact-Match-Rate": mean_exact
        })
        
    if not summary_rows:
        return pd.DataFrame(columns=["Kategorie", "Typ", "Score / F1-Score (Mean)", "Exact-Match-Rate"])
        
    return pd.DataFrame(summary_rows).sort_values(by=["Typ", "Kategorie"]).reset_index(drop=True)

# =====================================================================
# DISPLAY FUNCTIONS
# =====================================================================
def display_scores_interactive(df_scores: pd.DataFrame):
    """
    Rendert ein interaktives Interface, in dem man einzelne Metriken
    ein- und ausblenden kann, inklusive Alle/Keine Buttons.
    """
    score_cols = [col for col in df_scores.columns if col != 'image_id']
    
    col_selector = widgets.SelectMultiple(
        options=score_cols,
        value=score_cols,
        rows=min(12, len(score_cols)),
        description='Spalten:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='450px', margin='10px 0px 10px 0px')
    )
    
    btn_all = widgets.Button(
        description="Alle auswählen",
        button_style='primary',
        icon='check-square',
        layout=widgets.Layout(margin='0px 10px 0px 0px')
    )
    btn_none = widgets.Button(
        description="Alle abwählen",
        button_style='warning',
        icon='square-o'
    )
    
    buttons_layout = widgets.HBox([btn_all, btn_none])
    output_area = widgets.Output()
    
    def on_all_clicked(b):
        col_selector.value = col_selector.options
        
    def on_none_clicked(b):
        col_selector.value = ()
        
    btn_all.on_click(on_all_clicked)
    btn_none.on_click(on_none_clicked)
    
    def update_table(change=None):
        with output_area:
            clear_output(wait=True)
            selected_cols = ['image_id'] + list(col_selector.value)
            df_filtered = df_scores[selected_cols]
            
            numeric_cols = [col for col in df_filtered.columns if col != 'image_id']
            styled_df = df_filtered.style.format(
                {col: "{:.0%}" for col in numeric_cols}
            ).set_table_styles([
                {"selector": "th", "props": [
                    ("background-color", "#1d3557"),
                    ("color", "white"),
                    ("font-family", "Segoe UI, Arial, sans-serif"),
                    ("font-size", "11px"),
                    ("font-weight", "bold"),
                    ("padding", "6px 8px"),
                    ("border", "1px solid #d3d3d3"),
                    ("white-space", "nowrap"),
                    ("text-align", "center")
                ]},
                {"selector": "td", "props": [
                    ("font-family", "Segoe UI, Arial, sans-serif"),
                    ("font-size", "11px"),
                    ("padding", "6px"),
                    ("border", "1px solid #e0e0e0"),
                    ("text-align", "center")
                ]},
                {"selector": "table", "props": [
                    ("border-collapse", "collapse"),
                    ("width", "100%")
                ]}
            ]).hide(axis="index")
            
            html_table = styled_df.to_html()
            scrollable_html = f'<div style="overflow-x: auto; max-width: 100%; border: 1px solid #e0e0e0; border-radius: 4px; padding: 4px;">{html_table}</div>'
            display(HTML(scrollable_html))
            
    col_selector.observe(lambda change: update_table(), names='value')
    
    ui_layout = widgets.VBox([
        widgets.HTML("<h3 style='font-family: Segoe UI, Arial, sans-serif; color: #1d3557;'>Metriken-Explorer</h3>"),
        widgets.HTML("<p style='font-family: Segoe UI, Arial, sans-serif;'>Wähle aus, welche Spalten angezeigt werden sollen:</p>"),
        buttons_layout,
        col_selector,
        output_area
    ])
    
    display(ui_layout)
    update_table()

def display_summary(df_summary: pd.DataFrame):
    """
    Stylet und rendert die Summary-Tabelle der gemittelten Ergebnisse.
    """
    numeric_cols = ["Score / F1-Score (Mean)", "Exact-Match-Rate"]
    styled_summary = df_summary.style.format(
        {col: "{:.1%}" for col in numeric_cols}
    ).set_table_styles([
        {"selector": "th", "props": [
            ("background-color", "#1d3557"),
            ("color", "white"),
            ("font-family", "Segoe UI, Arial, sans-serif"),
            ("font-size", "12px"),
            ("font-weight", "bold"),
            ("padding", "8px 10px"),
            ("border", "1px solid #d3d3d3")
        ]},
        {"selector": "td", "props": [
            ("font-family", "Segoe UI, Arial, sans-serif"),
            ("font-size", "12px"),
            ("padding", "8px 10px"),
            ("border", "1px solid #e0e0e0")
        ]},
        {"selector": "table", "props": [
            ("border-collapse", "collapse"),
            ("width", "100%")
        ]}
    ]).hide(axis="index")
    
    display(HTML("<h3 style='font-family: Segoe UI, Arial, sans-serif; color: #1d3557; margin-top: 25px;'>Aggregierte Ergebnisse (Durchschnitt über alle Wundbilder)</h3>"))
    display(styled_summary)
