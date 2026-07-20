import os
import sys
import re
import ast
import json
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, HTML, Image

# Pfad anpassen, um utils_notebook und das eval-Modul zu importieren
notebooks_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
for p in [notebooks_dir, root_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

from utils_notebook import metrics, clean
from utils_notebook.LR_utils_notebook.metrics_LR import format_val, parse_cell_value, get_score
from eval.baselines import evaluate_baselines_dual, BaselineEvaluator, load_lr_catalog_pools

def resolve_path(rel_path):
    """
    Sucht robust nach dem übergebenen Pfad ausgehend vom aktuellen Arbeitsverzeichnis
    oder dem Projekt-Root.
    """
    if os.path.exists(rel_path):
        return os.path.abspath(rel_path)
        
    # Versuche vom Projekt-Root aus zu suchen
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


def show_image(image_id, base_dir="data/wundbilder"):
    """Sucht nach dem Wundbild und zeigt es an."""
    resolved_dir = resolve_path(base_dir)
    match = re.search(r"wunde_(\d+)", image_id)
    if match:
        num = int(match.group(1))
        file_name = f"Bild{num}.jpg"
        file_path = os.path.join(resolved_dir, file_name)
        if os.path.exists(file_path):
            display(Image(filename=file_path, width=400))
        else:
            # Falls kein Bild gefunden, suche in Unterordnern
            fallback_found = False
            for root, _, files in os.walk(resolved_dir):
                if file_name in files:
                    display(Image(filename=os.path.join(root, file_name), width=400))
                    fallback_found = True
                    break
            if not fallback_found:
                print(f"Wundbild {file_name} in {resolved_dir} nicht gefunden.")

def compare_wunden_interactive(normalised=False, path_llm_raw=None, path_llm_norm=None):
    """
    Erstellt ein interaktives Widget, das die Ground Truth von beiden Experten (Experte 1 & 2) 
    und die LLM-Ausgaben (jeweils roh oder normalisiert) für ein ausgewähltes Wundbild vergleicht.
    """
    # Pfade auflösen
    path_gt1_raw = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth.csv")
    path_gt1_norm = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv")
    path_gt2_raw = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth.csv")
    path_gt2_norm = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv")
    path_llm_raw = resolve_path(path_llm_raw) if path_llm_raw else resolve_path("../../data/llm_outputs/zero_shot_lr/zero_shot_lr_raw.csv")
    path_llm_norm = resolve_path(path_llm_norm) if path_llm_norm else resolve_path("../../data/llm_outputs/zero_shot_lr/zero_shot_lr_normalised.csv")
    
    # Laden der DataFrames
    df_gt1_r = load_csv(path_gt1_raw)
    df_gt1_n = load_csv(path_gt1_norm)
    df_gt2_r = load_csv(path_gt2_raw)
    df_gt2_n = load_csv(path_gt2_norm)
    df_llm_r = load_csv(path_llm_raw)
    df_llm_n = load_csv(path_llm_norm)
    
    # Normalisiere image_id in allen DataFrames
    for df in [df_gt1_r, df_gt1_n, df_gt2_r, df_gt2_n, df_llm_r, df_llm_n]:
        if not df.empty and "image_id" in df.columns:
            df["image_id"] = df["image_id"].apply(normalize_image_id)
            
    # Verfügbare Wund-IDs aus den LLM-Rohdaten ermitteln
    all_ids = []
    if not df_llm_r.empty:
        all_ids = sorted(df_llm_r["image_id"].dropna().unique().tolist())
    if not all_ids:
        all_ids = [f"wunde_{i:02d}" for i in range(1, 61)]
        
    image_out = widgets.Output()
    table_out = widgets.Output()
        
    def render_table(image_id):
        # Zeilendaten extrahieren
        def get_rec(df):
            if df.empty:
                return {}
            subset = df[df["image_id"] == image_id]
            if subset.empty:
                return {}
            return subset.iloc[0].to_dict()
            
        r_gt1_r = get_rec(df_gt1_r)
        r_gt1_n = get_rec(df_gt1_n)
        r_gt2_r = get_rec(df_gt2_r)
        r_gt2_n = get_rec(df_gt2_n)
        r_llm_r = get_rec(df_llm_r)
        r_llm_n = get_rec(df_llm_n)
        
        # Definition der Kategorien & Spaltenzuordnungen (Lohmann & Rauscher)
        categories_config = [
            ("Wundtyp", "wundtyp", "wundtyp", "Exact Match"),
            ("Lokalisation", "lokalisation", "lokalisation", "Exact Match"),
            ("Wundstadium", "wundstadium", "wundstadium", "F1 Checklist"),
            ("Wundgrund", "wundgrund", "wundgrund", "F1 Checklist"),
            ("Wundrand", "wundrand", "wundrand", "F1 Checklist"),
            ("Wundumgebung", "wundumgebung", "wundumgebung", "F1 Checklist"),
            ("Exsudat", "exsudat", "exsudat_menge", "Ordinal Distance"),
            ("Infektion", "infektion", "infektion_vorhanden", "Exact Match"),
            ("Wundspüllösung", "spuelloesung", "spuelloesung", "Exact Match"),
            ("Débridement notwendig?", "debridement_notwendig", "debridement_notwendig", "Exact Match"),
            ("Débridement Methode", "debridement", "debridement_methode", "F1 Checklist"),
            ("Primärverband", "Primärverband", "Primärverband", "Cross-Match F1"),
            ("Sekundärverband", "Sekundärverband", "Sekundärverband", "Cross-Match F1"),
            ("Kompression indiziert?", "kompression_indiziert", "kompression_indiziert", "Exact Match"),
            ("Kompression Produkte", "kompression_produkte", "kompression_produkt", "F1 Checklist"),
            ("Auffälligkeiten", "auffaelligkeiten", "weitere_auffaelligkeiten", "Keine (deskriptiv)"),
            ("Einschränkungen/Annahmen", "einschraenkungen", "einschraenkungen_annahmen", "Keine (deskriptiv)"),
        ]
        
        rows = []
        for cat_name, gt_key, llm_key, metric in categories_config:
            if cat_name in ["Primärverband", "Sekundärverband"]:
                if cat_name == "Primärverband":
                    g_pref, g_alt = "praeferenz_produkt", "alternative_produkt"
                    l_pref, l_alt = "praeferenz_wundauflage", "alternativ_wundauflage"
                else:
                    g_pref, g_alt = "ergaenzende_produkte_praeferenz", "ergaenzende_produkte_alternativ"
                    l_pref, l_alt = "praeferenz_ergaenzung", "alternativ_ergaenzung"
                    
                # Roh-Werte
                gt1_r_str = f"<b>P:</b> {format_val(r_gt1_r.get(g_pref))}<br><b>A:</b> {format_val(r_gt1_r.get(g_alt))}"
                gt2_r_str = f"<b>P:</b> {format_val(r_gt2_r.get(g_pref))}<br><b>A:</b> {format_val(r_gt2_r.get(g_alt))}"
                llm_r_str = f"<b>P:</b> {format_val(r_llm_r.get(l_pref))}<br><b>A:</b> {format_val(r_llm_r.get(l_alt))}"
                
                # Normalisierte Werte
                gt1_n_str = f"<b>P:</b> {format_val(r_gt1_n.get(g_pref))}<br><b>A:</b> {format_val(r_gt1_n.get(g_alt))}"
                gt2_n_str = f"<b>P:</b> {format_val(r_gt2_n.get(g_pref))}<br><b>A:</b> {format_val(r_gt2_n.get(g_alt))}"
                llm_n_str = f"<b>P:</b> {format_val(r_llm_n.get(l_pref))}<br><b>A:</b> {format_val(r_llm_n.get(l_alt))}"
                
                # Parsen für Score-Berechnung
                gt1_r_p = parse_cell_value(r_gt1_r.get(g_pref))
                gt1_r_a = parse_cell_value(r_gt1_r.get(g_alt))
                gt1_n_p = parse_cell_value(r_gt1_n.get(g_pref))
                gt1_n_a = parse_cell_value(r_gt1_n.get(g_alt))
                
                gt2_r_p = parse_cell_value(r_gt2_r.get(g_pref))
                gt2_r_a = parse_cell_value(r_gt2_r.get(g_alt))
                gt2_n_p = parse_cell_value(r_gt2_n.get(g_pref))
                gt2_n_a = parse_cell_value(r_gt2_n.get(g_alt))
                
                llm_r_p = parse_cell_value(r_llm_r.get(l_pref))
                llm_r_a = parse_cell_value(r_llm_r.get(l_alt))
                llm_n_p = parse_cell_value(r_llm_n.get(l_pref))
                llm_n_a = parse_cell_value(r_llm_n.get(l_alt))
                
                # Scores berechnen mit best_path_f1 (Cross-Match F1)
                f1_1_r, _ = metrics.best_path_f1(metrics.to_clean_set(llm_r_p), metrics.to_clean_set(llm_r_a), metrics.to_clean_set(gt1_r_p), metrics.to_clean_set(gt1_r_a))
                f1_1_n, _ = metrics.best_path_f1(metrics.to_clean_set(clean.clean_whitespace(llm_n_p)), metrics.to_clean_set(clean.clean_whitespace(llm_n_a)), metrics.to_clean_set(clean.clean_whitespace(gt1_n_p)), metrics.to_clean_set(clean.clean_whitespace(gt1_n_a)))
                
                f1_2_r, _ = metrics.best_path_f1(metrics.to_clean_set(llm_r_p), metrics.to_clean_set(llm_r_a), metrics.to_clean_set(gt2_r_p), metrics.to_clean_set(gt2_r_a))
                f1_2_n, _ = metrics.best_path_f1(metrics.to_clean_set(clean.clean_whitespace(llm_n_p)), metrics.to_clean_set(clean.clean_whitespace(llm_n_a)), metrics.to_clean_set(clean.clean_whitespace(gt2_n_p)), metrics.to_clean_set(clean.clean_whitespace(gt2_n_a)))
                
                if normalised:
                    cell_gt1 = gt1_n_str
                    cell_gt2 = gt2_n_str
                    cell_llm = llm_n_str
                    score_str = f"<b>Ex1:</b> {f1_1_n:.0%}<br><b>Ex2:</b> {f1_2_n:.0%}"
                    color_score = max(f1_1_n, f1_2_n)
                else:
                    cell_gt1 = gt1_r_str
                    cell_gt2 = gt2_r_str
                    cell_llm = llm_r_str
                    score_str = f"<b>Ex1:</b> {f1_1_r:.0%}<br><b>Ex2:</b> {f1_2_r:.0%}"
                    color_score = max(f1_1_r, f1_2_r)
                
            else:
                # Standard-Felder
                v_gt1_r = parse_cell_value(r_gt1_r.get(gt_key))
                v_gt1_n = parse_cell_value(r_gt1_n.get(gt_key))
                v_gt2_r = parse_cell_value(r_gt2_r.get(gt_key))
                v_gt2_n = parse_cell_value(r_gt2_n.get(gt_key))
                v_llm_r = parse_cell_value(r_llm_r.get(llm_key))
                v_llm_n = parse_cell_value(r_llm_n.get(llm_key))
                
                gt1_r_str = format_val(v_gt1_r)
                gt2_r_str = format_val(v_gt2_r)
                llm_r_str = format_val(v_llm_r)
                
                gt1_n_str = format_val(v_gt1_n)
                gt2_n_str = format_val(v_gt2_n)
                llm_n_str = format_val(v_llm_n)
                
                if metric == "Keine (deskriptiv)":
                    color_score = None
                    score_str = "—"
                else:
                    s1_r = get_score(cat_name, v_gt1_r, v_llm_r, True)
                    s1_n = get_score(cat_name, v_gt1_n, v_llm_n, False)
                    s2_r = get_score(cat_name, v_gt2_r, v_llm_r, True)
                    s2_n = get_score(cat_name, v_gt2_n, v_llm_n, False)
                    
                    if normalised:
                        score_str = f"<b>Ex1:</b> {s1_n:.0%}<br><b>Ex2:</b> {s2_n:.0%}"
                        color_score = max(s1_n, s2_n)
                    else:
                        score_str = f"<b>Ex1:</b> {s1_r:.0%}<br><b>Ex2:</b> {s2_r:.0%}"
                        color_score = max(s1_r, s2_r)
                        
                if normalised:
                    cell_gt1 = gt1_n_str
                    cell_gt2 = gt2_n_str
                    cell_llm = llm_n_str
                else:
                    cell_gt1 = gt1_r_str
                    cell_gt2 = gt2_r_str
                    cell_llm = llm_r_str
            
            rows.append({
                "Kategorie": cat_name,
                "GT Experte 1": cell_gt1,
                "GT Experte 2": cell_gt2,
                "LLM Output": cell_llm,
                "Score": score_str,
                "Metrik": metric,
                "color_score": color_score
            })
            
        df_compare = pd.DataFrame(rows)
        
        # Zeilenfärbung basierend auf dem maximalen ausgewählten Score (Roh oder Norm)
        def apply_row_style(row):
            max_score = row["color_score"]
            if max_score is None:
                base_style = "background-color: #ffffff; color: #333333; border: 1px solid #e2e8f0;"
            elif max_score >= 0.999: # 100% Match -> Grün
                base_style = "background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;"
            elif max_score > 0.001: # Über 0% Match -> Orange
                base_style = "background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba;"
            else: # 0% Match -> Rot
                base_style = "background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;"
                
            return [base_style] * len(row)
            
        # Styler initialisieren
        styler = df_compare.style.apply(apply_row_style, axis=1)
        styler = styler.hide(axis="index").hide(subset=["color_score"], axis="columns")
        
        # Spaltenbreiten setzen
        styler = styler.set_properties(subset=["GT Experte 1", "GT Experte 2", "LLM Output"], **{"width": "22%"})
        styler = styler.set_properties(subset=["Score", "Metrik"], **{"width": "10%"})
        
        # CSS Styles für die Tabelle (Schriftgröße erhöht: th auf 14px, td auf 13px)
        styler = styler.set_table_styles([
            {"selector": "th", "props": [
                ("background-color", "#1d3557"), ("color", "white"),
                ("font-family", "Segoe UI, Arial, sans-serif"), ("font-size", "14px"),
                ("font-weight", "bold"), ("padding", "10px 12px"), ("border", "1px solid #d3d3d3"),
                ("text-align", "center")
            ]},
            {"selector": "td", "props": [
                ("font-family", "Segoe UI, Arial, sans-serif"), ("font-size", "13px"),
                ("padding", "8px 10px"), ("border", "1px solid #d3d3d3"),
                ("line-height", "1.4")
            ]},
            {"selector": ".col0, .col2, .col3", "props": [
                ("border-right", "2.5px solid #1d3557")
            ]},
            {"selector": "table", "props": [("border-collapse", "collapse"), ("width", "100%")]}
        ])
        
        display(HTML(f"<h3 style='font-family: Segoe UI, Arial, sans-serif; color: #1d3557; margin-top: 20px;'>Vergleich für Bild-ID: {image_id}</h3>"))
        display(styler)

    def on_wund_change(change):
        image_id = change["new"]
        if image_id:
            with image_out:
                image_out.clear_output(wait=True)
                show_image(image_id)
            with table_out:
                table_out.clear_output(wait=True)
                render_table(image_id)

    # Interaktiven Dropdown-Selektor erstellen
    wunde_select = widgets.Dropdown(
        options=all_ids,
        value=all_ids[0] if all_ids else None,
        description='Wund-ID:',
        style={'description_width': 'initial'},
        disabled=False,
    )
    
    wunde_select.observe(on_wund_change, names="value")
    
    # Initiale Befüllung der Ausgaben
    with image_out:
        show_image(wunde_select.value)
    with table_out:
        render_table(wunde_select.value)
        
    # Ausgabe: Bild oben, Dropdown in der Mitte, Tabelle unten
    display(widgets.VBox([image_out, wunde_select, table_out]))


def compare_categories_interactive(normalised=False, path_llm_raw=None, path_llm_norm=None):
    """
    Erstellt ein interaktives Widget mit einem Dropdown-Menü zur Auswahl einer Kategorie
    und vergleicht Ground Truth und LLM-Ausgaben (roh oder normalisiert) für alle Wundbilder side-by-side.
    """
    # Pfade auflösen
    path_gt1_raw = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth.csv")
    path_gt1_norm = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv")
    path_gt2_raw = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth.csv")
    path_gt2_norm = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv")
    path_llm_raw = resolve_path(path_llm_raw) if path_llm_raw else resolve_path("../../data/llm_outputs/zero_shot_lr/zero_shot_lr_raw.csv")
    path_llm_norm = resolve_path(path_llm_norm) if path_llm_norm else resolve_path("../../data/llm_outputs/zero_shot_lr/zero_shot_lr_normalised.csv")
    
    # Laden der DataFrames
    df_gt1_r = load_csv(path_gt1_raw)
    df_gt1_n = load_csv(path_gt1_norm)
    df_gt2_r = load_csv(path_gt2_raw)
    df_gt2_n = load_csv(path_gt2_norm)
    df_llm_r = load_csv(path_llm_raw)
    df_llm_n = load_csv(path_llm_norm)
    
    # Normalisiere image_id in allen DataFrames
    for df in [df_gt1_r, df_gt1_n, df_gt2_r, df_gt2_n, df_llm_r, df_llm_n]:
        if not df.empty and "image_id" in df.columns:
            df["image_id"] = df["image_id"].apply(normalize_image_id)
            
    # Verfügbare Wund-IDs ermitteln
    all_ids = []
    if not df_llm_r.empty:
        all_ids = sorted(df_llm_r["image_id"].dropna().unique().tolist())
    if not all_ids:
        all_ids = [f"wunde_{i:02d}" for i in range(1, 61)]
        
    # Liste der Kategorien & Spaltenzuordnungen in der vom User gewünschten Reihenfolge
    categories_config = {
        "Wundtyp": {"gt_key": "wundtyp", "llm_key": "wundtyp", "metric": "Exact Match"},
        "Lokalisation": {"gt_key": "lokalisation", "llm_key": "lokalisation", "metric": "Exact Match"},
        "Wundstadium": {"gt_key": "wundstadium", "llm_key": "wundstadium", "metric": "F1 Checklist"},
        "Wundgrund": {"gt_key": "wundgrund", "llm_key": "wundgrund", "metric": "F1 Checklist"},
        "Wundrand": {"gt_key": "wundrand", "llm_key": "wundrand", "metric": "F1 Checklist"},
        "Wundumgebung": {"gt_key": "wundumgebung", "llm_key": "wundumgebung", "metric": "F1 Checklist"},
        "Exsudat": {"gt_key": "exsudat", "llm_key": "exsudat_menge", "metric": "Ordinal Distance"},
        "Debridement notwendig": {"gt_key": "debridement_notwendig", "llm_key": "debridement_notwendig", "metric": "Exact Match"},
        "Debridement Methode": {"gt_key": "debridement", "llm_key": "debridement_methode", "metric": "F1 Checklist"},
        "Infektionsverdacht": {"gt_key": "infektion", "llm_key": "infektion_vorhanden", "metric": "Exact Match"},
        "Spüllösung": {"gt_key": "spuelloesung", "llm_key": "spuelloesung", "metric": "Exact Match"},
        "Primärverband": {"special": "Primärverband", "metric": "Cross-Match F1"},
        "Sekundärverband": {"special": "Sekundärverband", "metric": "Cross-Match F1"},
        "Kompression indiziert": {"gt_key": "kompression_indiziert", "llm_key": "kompression_indiziert", "metric": "Exact Match"},
        "Kompression Produkt": {"gt_key": "kompression_produkte", "llm_key": "kompression_produkt", "metric": "F1 Checklist"}
    }
    
    table_out = widgets.Output()
    
    def render_category_table(category_name):
        if not category_name:
            print("Keine Kategorie ausgewählt.")
            return
            
        cfg = categories_config[category_name]
        rows = []
        
        for img_id in all_ids:
            # Zeilendaten holen
            def get_rec(df):
                if df.empty:
                    return {}
                subset = df[df["image_id"] == img_id]
                if subset.empty:
                    return {}
                return subset.iloc[0].to_dict()
                
            r_gt1_r = get_rec(df_gt1_r)
            r_gt1_n = get_rec(df_gt1_n)
            r_gt2_r = get_rec(df_gt2_r)
            r_gt2_n = get_rec(df_gt2_n)
            r_llm_r = get_rec(df_llm_r)
            r_llm_n = get_rec(df_llm_n)
            
            if "special" in cfg:
                cat_type = cfg["special"]
                if cat_type == "Primärverband":
                    g_pref, g_alt = "praeferenz_produkt", "alternative_produkt"
                    l_pref, l_alt = "praeferenz_wundauflage", "alternativ_wundauflage"
                else:
                    g_pref, g_alt = "ergaenzende_produkte_praeferenz", "ergaenzende_produkte_alternativ"
                    l_pref, l_alt = "praeferenz_ergaenzung", "alternativ_ergaenzung"
                    
                # Roh-Werte
                gt1_r_str = f"<b>P:</b> {format_val(r_gt1_r.get(g_pref))}<br><b>A:</b> {format_val(r_gt1_r.get(g_alt))}"
                gt2_r_str = f"<b>P:</b> {format_val(r_gt2_r.get(g_pref))}<br><b>A:</b> {format_val(r_gt2_r.get(g_alt))}"
                llm_r_str = f"<b>P:</b> {format_val(r_llm_r.get(l_pref))}<br><b>A:</b> {format_val(r_llm_r.get(l_alt))}"
                
                # Normalisierte Werte
                gt1_n_str = f"<b>P:</b> {format_val(r_gt1_n.get(g_pref))}<br><b>A:</b> {format_val(r_gt1_n.get(g_alt))}"
                gt2_n_str = f"<b>P:</b> {format_val(r_gt2_n.get(g_pref))}<br><b>A:</b> {format_val(r_gt2_n.get(g_alt))}"
                llm_n_str = f"<b>P:</b> {format_val(r_llm_n.get(l_pref))}<br><b>A:</b> {format_val(r_llm_n.get(l_alt))}"
                
                # Parsen für Score-Berechnung
                gt1_r_p = parse_cell_value(r_gt1_r.get(g_pref))
                gt1_r_a = parse_cell_value(r_gt1_r.get(g_alt))
                gt1_n_p = parse_cell_value(r_gt1_n.get(g_pref))
                gt1_n_a = parse_cell_value(r_gt1_n.get(g_alt))
                
                gt2_r_p = parse_cell_value(r_gt2_r.get(g_pref))
                gt2_r_a = parse_cell_value(r_gt2_r.get(g_alt))
                gt2_n_p = parse_cell_value(r_gt2_n.get(g_pref))
                gt2_n_a = parse_cell_value(r_gt2_n.get(g_alt))
                
                llm_r_p = parse_cell_value(r_llm_r.get(l_pref))
                llm_r_a = parse_cell_value(r_llm_r.get(l_alt))
                llm_n_p = parse_cell_value(r_llm_n.get(l_pref))
                llm_n_a = parse_cell_value(r_llm_n.get(l_alt))
                
                f1_1_r, _ = metrics.best_path_f1(metrics.to_clean_set(llm_r_p), metrics.to_clean_set(llm_r_a), metrics.to_clean_set(gt1_r_p), metrics.to_clean_set(gt1_r_a))
                f1_1_n, _ = metrics.best_path_f1(metrics.to_clean_set(clean.clean_whitespace(llm_n_p)), metrics.to_clean_set(clean.clean_whitespace(llm_n_a)), metrics.to_clean_set(clean.clean_whitespace(gt1_n_p)), metrics.to_clean_set(clean.clean_whitespace(gt1_n_a)))
                
                f1_2_r, _ = metrics.best_path_f1(metrics.to_clean_set(llm_r_p), metrics.to_clean_set(llm_r_a), metrics.to_clean_set(gt2_r_p), metrics.to_clean_set(gt2_r_a))
                f1_2_n, _ = metrics.best_path_f1(metrics.to_clean_set(clean.clean_whitespace(llm_n_p)), metrics.to_clean_set(clean.clean_whitespace(llm_n_a)), metrics.to_clean_set(clean.clean_whitespace(gt2_n_p)), metrics.to_clean_set(clean.clean_whitespace(gt2_n_a)))
                
                if normalised:
                    cell_gt1 = gt1_n_str
                    cell_gt2 = gt2_n_str
                    cell_llm = llm_n_str
                    score_str = f"<b>Ex1:</b> {f1_1_n:.0%}<br><b>Ex2:</b> {f1_2_n:.0%}"
                    color_score = max(f1_1_n, f1_2_n)
                else:
                    cell_gt1 = gt1_r_str
                    cell_gt2 = gt2_r_str
                    cell_llm = llm_r_str
                    score_str = f"<b>Ex1:</b> {f1_1_r:.0%}<br><b>Ex2:</b> {f1_2_r:.0%}"
                    color_score = max(f1_1_r, f1_2_r)
                    
            else:
                gt_k = cfg["gt_key"]
                llm_k = cfg["llm_key"]
                
                v_gt1_r = parse_cell_value(r_gt1_r.get(gt_k))
                v_gt1_n = parse_cell_value(r_gt1_n.get(gt_k))
                v_gt2_r = parse_cell_value(r_gt2_r.get(gt_k))
                v_gt2_n = parse_cell_value(r_gt2_n.get(gt_k))
                v_llm_r = parse_cell_value(r_llm_r.get(llm_k))
                v_llm_n = parse_cell_value(r_llm_n.get(llm_k))
                
                gt1_r_str = format_val(v_gt1_r)
                gt2_r_str = format_val(v_gt2_r)
                llm_r_str = format_val(v_llm_r)
                
                gt1_n_str = format_val(v_gt1_n)
                gt2_n_str = format_val(v_gt2_n)
                llm_n_str = format_val(v_llm_n)
                
                s1_r = get_score(category_name, v_gt1_r, v_llm_r, True)
                s1_n = get_score(category_name, v_gt1_n, v_llm_n, False)
                s2_r = get_score(category_name, v_gt2_r, v_llm_r, True)
                s2_n = get_score(category_name, v_gt2_n, v_llm_n, False)
                
                if normalised:
                    cell_gt1 = gt1_n_str
                    cell_gt2 = gt2_n_str
                    cell_llm = llm_n_str
                    score_str = f"<b>Ex1:</b> {s1_n:.0%}<br><b>Ex2:</b> {s2_n:.0%}"
                    color_score = max(s1_n, s2_n)
                else:
                    cell_gt1 = gt1_r_str
                    cell_gt2 = gt2_r_str
                    cell_llm = llm_r_str
                    score_str = f"<b>Ex1:</b> {s1_r:.0%}<br><b>Ex2:</b> {s2_r:.0%}"
                    color_score = max(s1_r, s2_r)
                    
            rows.append({
                "Wund-ID": img_id,
                "GT Experte 1": cell_gt1,
                "GT Experte 2": cell_gt2,
                "LLM Output": cell_llm,
                "Score": score_str,
                "color_score": color_score
            })
            
        df_compare = pd.DataFrame(rows)
        
        # Numerische Sortierung der Wund-IDs
        if not df_compare.empty:
            df_compare = df_compare.sort_values(
                by='Wund-ID',
                key=lambda x: x.str.extract(r'(\d+)')[0].astype(float)
            ).reset_index(drop=True)
            
        # Zeilenfärbung
        def apply_row_style(row):
            max_score = row["color_score"]
            if max_score is None:
                base_style = "background-color: #ffffff; color: #333333; border: 1px solid #e2e8f0;"
            elif max_score >= 0.999: # 100% Match -> Grün
                base_style = "background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;"
            elif max_score > 0.001: # Über 0% Match -> Orange
                base_style = "background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba;"
            else: # 0% Match -> Rot
                base_style = "background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;"
            return [base_style] * len(row)
            
        styler = df_compare.style.apply(apply_row_style, axis=1)
        styler = styler.hide(axis="index").hide(subset=["color_score"], axis="columns")
        
        # Spaltenbreiten (Wund-ID: 10%, GT und LLM Output: 26%, Score: 12%)
        styler = styler.set_properties(subset=["GT Experte 1", "GT Experte 2", "LLM Output"], **{"width": "26%"})
        styler = styler.set_properties(subset=["Score"], **{"width": "12%"})
        
        # CSS Styles für die Tabelle
        styler = styler.set_table_styles([
            {"selector": "th", "props": [
                ("background-color", "#1d3557"), ("color", "white"),
                ("font-family", "Segoe UI, Arial, sans-serif"), ("font-size", "14px"),
                ("font-weight", "bold"), ("padding", "10px 12px"), ("border", "1px solid #d3d3d3"),
                ("text-align", "center")
            ]},
            {"selector": "td", "props": [
                ("font-family", "Segoe UI, Arial, sans-serif"), ("font-size", "13px"),
                ("padding", "8px 10px"), ("border", "1px solid #d3d3d3"),
                ("line-height", "1.4")
            ]},
            {"selector": ".col0, .col2, .col3", "props": [
                ("border-right", "2.5px solid #1d3557")
            ]},
            {"selector": "table", "props": [("border-collapse", "collapse"), ("width", "100%")]}
        ])
        
        display(HTML(f"<h3 style='font-family: Segoe UI, Arial, sans-serif; color: #1d3557; margin-top: 20px;'>Vergleich aller Wunden für Kategorie: {category_name}</h3>"))
        display(styler)
        
    def on_cat_change(change):
        category_name = change["new"]
        if category_name:
            with table_out:
                table_out.clear_output(wait=True)
                render_category_table(category_name)
                
    # Dropdown setup in the exact order requested
    cat_select = widgets.Dropdown(
        options=list(categories_config.keys()),
        value="Wundtyp",
        description="Kategorie:",
        style={'description_width': 'initial'},
        disabled=False,
    )
    
    cat_select.observe(on_cat_change, names="value")
    
    # Initiale Befüllung
    with table_out:
        render_category_table(cat_select.value)
        
    display(widgets.VBox([cat_select, table_out]))


def calculate_summary_LR(expert_id, normalised=False, path_llm_raw=None, path_llm_norm=None):
    """
    Berechnet die aggregierten Metriken (Mean Score und Exact-Match-Rate) über alle Wundbilder
    speziell für die Lohmann & Rauscher Kategorien im Vergleich zu einem bestimmten Experten.
    """
    # Pfade auflösen
    path_gt_raw = resolve_path(f"../../data/ground_truth/lohmann_rauscher/Experte{expert_id}_LR_GroundTruth.csv")
    path_gt_norm = resolve_path(f"../../data/ground_truth/lohmann_rauscher/Experte{expert_id}_LR_GroundTruth_normalised.csv")
    path_llm_raw = resolve_path(path_llm_raw) if path_llm_raw else resolve_path("../../data/llm_outputs/zero_shot_lr/zero_shot_lr_raw.csv")
    path_llm_norm = resolve_path(path_llm_norm) if path_llm_norm else resolve_path("../../data/llm_outputs/zero_shot_lr/zero_shot_lr_normalised.csv")
    
    # Laden der DataFrames
    df_gt = load_csv(path_gt_norm if normalised else path_gt_raw)
    df_llm = load_csv(path_llm_norm if normalised else path_llm_raw)
    
    # Normalisiere image_id in allen DataFrames
    for df in [df_gt, df_llm]:
        if not df.empty and "image_id" in df.columns:
            df["image_id"] = df["image_id"].apply(normalize_image_id)
            
    # Verfügbare Wund-IDs ermitteln
    all_ids = []
    if not df_llm.empty:
        all_ids = sorted(df_llm["image_id"].dropna().unique().tolist())
    if not all_ids:
        all_ids = [f"wunde_{i:02d}" for i in range(1, 61)]
        
    categories_config = {
        "Wundtyp": {"gt_key": "wundtyp", "llm_key": "wundtyp", "metric_type": "exact"},
        "Lokalisation": {"gt_key": "lokalisation", "llm_key": "lokalisation", "metric_type": "exact"},
        "Wundstadium": {"gt_key": "wundstadium", "llm_key": "wundstadium", "metric_type": "checklist"},
        "Wundgrund": {"gt_key": "wundgrund", "llm_key": "wundgrund", "metric_type": "checklist"},
        "Wundrand": {"gt_key": "wundrand", "llm_key": "wundrand", "metric_type": "checklist"},
        "Wundumgebung": {"gt_key": "wundumgebung", "llm_key": "wundumgebung", "metric_type": "checklist"},
        "Exsudat": {"gt_key": "exsudat", "llm_key": "exsudat_menge", "metric_type": "ordinal"},
        "Debridement notwendig": {"gt_key": "debridement_notwendig", "llm_key": "debridement_notwendig", "metric_type": "exact"},
        "Debridement Methode": {"gt_key": "debridement", "llm_key": "debridement_methode", "metric_type": "checklist"},
        "Infektionsverdacht": {"gt_key": "infektion", "llm_key": "infektion_vorhanden", "metric_type": "exact"},
        "Spüllösung": {"gt_key": "spuelloesung", "llm_key": "spuelloesung", "metric_type": "exact"},
        "Primärverband": {"special": "Primärverband", "metric_type": "cross_match"},
        "Sekundärverband": {"special": "Sekundärverband", "metric_type": "cross_match"},
        "Kompression indiziert": {"gt_key": "kompression_indiziert", "llm_key": "kompression_indiziert", "metric_type": "exact"},
        "Kompression Produkt": {"gt_key": "kompression_produkte", "llm_key": "kompression_produkt", "metric_type": "checklist"}
    }
    
    # Für jedes Wundbild und jede Kategorie den Score berechnen
    cat_scores = {cat: [] for cat in categories_config}
    cat_exacts = {cat: [] for cat in categories_config}
    
    for img_id in all_ids:
        gt_subset = df_gt[df_gt["image_id"] == img_id]
        llm_subset = df_llm[df_llm["image_id"] == img_id]
        
        r_gt = gt_subset.iloc[0].to_dict() if not gt_subset.empty else {}
        r_llm = llm_subset.iloc[0].to_dict() if not llm_subset.empty else {}
        
        for cat, cfg in categories_config.items():
            if "special" in cfg:
                cat_type = cfg["special"]
                if cat_type == "Primärverband":
                    g_pref, g_alt = "praeferenz_produkt", "alternative_produkt"
                    l_pref, l_alt = "praeferenz_wundauflage", "alternativ_wundauflage"
                else:
                    g_pref, g_alt = "ergaenzende_produkte_praeferenz", "ergaenzende_produkte_alternativ"
                    l_pref, l_alt = "praeferenz_ergaenzung", "alternativ_ergaenzung"
                    
                gt_p = parse_cell_value(r_gt.get(g_pref))
                gt_a = parse_cell_value(r_gt.get(g_alt))
                llm_p = parse_cell_value(r_llm.get(l_pref))
                llm_a = parse_cell_value(r_llm.get(l_alt))
                
                # Cross-match F1
                if normalised:
                    f1_val, exact_val = metrics.best_path_f1(
                        metrics.to_clean_set(clean.clean_whitespace(llm_p)),
                        metrics.to_clean_set(clean.clean_whitespace(llm_a)),
                        metrics.to_clean_set(clean.clean_whitespace(gt_p)),
                        metrics.to_clean_set(clean.clean_whitespace(gt_a))
                    )
                else:
                    f1_val, exact_val = metrics.best_path_f1(
                        metrics.to_clean_set(llm_p),
                        metrics.to_clean_set(llm_a),
                        metrics.to_clean_set(gt_p),
                        metrics.to_clean_set(gt_a)
                    )
                cat_scores[cat].append(f1_val)
                cat_exacts[cat].append(exact_val)
            else:
                gt_k = cfg["gt_key"]
                llm_k = cfg["llm_key"]
                
                v_gt = parse_cell_value(r_gt.get(gt_k))
                v_llm = parse_cell_value(r_llm.get(llm_k))
                
                # Score berechnen
                score_val = get_score(cat, v_gt, v_llm, raw_flag=(not normalised))
                exact_val = metrics.score_exact(v_gt, v_llm)
                
                if score_val is not None:
                    cat_scores[cat].append(score_val)
                    cat_exacts[cat].append(exact_val)
                    
    summary_rows = []
    for cat, cfg in categories_config.items():
        scores = cat_scores[cat]
        exacts = cat_exacts[cat]
        
        mean_score = sum(scores) / len(scores) if scores else float('nan')
        mean_exact = sum(exacts) / len(exacts) if exacts else float('nan')
        
        summary_rows.append({
            "Kategorie": cat,
            "Typ": cfg.get("special", cfg.get("metric_type")),
            "Score / F1-Score (Mean)": mean_score,
            "Exact-Match-Rate": mean_exact
        })
        
    return pd.DataFrame(summary_rows)


def display_summary_LR(df_summary):
    """
    Formatiert und stellt das Summary-DataFrame mit dem L&R-Design dar.
    """
    styler = df_summary.style.format({
        "Score / F1-Score (Mean)": "{:.1%}",
        "Exact-Match-Rate": "{:.1%}"
    })
    styler = styler.hide(axis="index")
    styler = styler.set_table_styles([
        {"selector": "th", "props": [
            ("background-color", "#1d3557"), ("color", "white"),
            ("font-family", "Segoe UI, Arial, sans-serif"), ("font-size", "13px"),
            ("font-weight", "bold"), ("padding", "8px 10px"), ("border", "1px solid #d3d3d3")
        ]},
        {"selector": "td", "props": [
            ("font-family", "Segoe UI, Arial, sans-serif"), ("font-size", "13px"),
            ("padding", "8px 10px"), ("border", "1px solid #e0e0e0")
        ]},
        {"selector": "table", "props": [("border-collapse", "collapse"), ("width", "100%")]}
    ])
    display(styler)


def calculate_experts_summary_LR(normalised=False):
    """
    Berechnet die Übereinstimmung (Mean Score und Exact-Match-Rate) zwischen Experte 1 und Experte 2
    über alle Wundbilder hinweg für die 15 Lohmann & Rauscher Kategorien.
    """
    path_gt1_raw = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth.csv")
    path_gt1_norm = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv")
    path_gt2_raw = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth.csv")
    path_gt2_norm = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv")
    
    df_gt1 = load_csv(path_gt1_norm if normalised else path_gt1_raw)
    df_gt2 = load_csv(path_gt2_norm if normalised else path_gt2_raw)
    
    for df in [df_gt1, df_gt2]:
        if not df.empty and "image_id" in df.columns:
            df["image_id"] = df["image_id"].apply(normalize_image_id)
            
    all_ids = []
    if not df_gt1.empty:
        all_ids = sorted(df_gt1["image_id"].dropna().unique().tolist())
    if not all_ids:
        all_ids = [f"wunde_{i:02d}" for i in range(1, 61)]
        
    categories_config = {
        "Wundtyp": {"gt_key": "wundtyp", "metric_type": "exact"},
        "Lokalisation": {"gt_key": "lokalisation", "metric_type": "exact"},
        "Wundstadium": {"gt_key": "wundstadium", "metric_type": "checklist"},
        "Wundgrund": {"gt_key": "wundgrund", "metric_type": "checklist"},
        "Wundrand": {"gt_key": "wundrand", "metric_type": "checklist"},
        "Wundumgebung": {"gt_key": "wundumgebung", "metric_type": "checklist"},
        "Exsudat": {"gt_key": "exsudat", "metric_type": "ordinal"},
        "Debridement notwendig": {"gt_key": "debridement_notwendig", "metric_type": "exact"},
        "Debridement Methode": {"gt_key": "debridement", "metric_type": "checklist"},
        "Infektionsverdacht": {"gt_key": "infektion", "metric_type": "exact"},
        "Spüllösung": {"gt_key": "spuelloesung", "metric_type": "exact"},
        "Primärverband": {"special": "Primärverband", "metric_type": "cross_match"},
        "Sekundärverband": {"special": "Sekundärverband", "metric_type": "cross_match"},
        "Kompression indiziert": {"gt_key": "kompression_indiziert", "metric_type": "exact"},
        "Kompression Produkt": {"gt_key": "kompression_produkte", "metric_type": "checklist"}
    }
    
    cat_scores = {cat: [] for cat in categories_config}
    cat_exacts = {cat: [] for cat in categories_config}
    
    for img_id in all_ids:
        gt1_subset = df_gt1[df_gt1["image_id"] == img_id]
        gt2_subset = df_gt2[df_gt2["image_id"] == img_id]
        
        r_gt1 = gt1_subset.iloc[0].to_dict() if not gt1_subset.empty else {}
        r_gt2 = gt2_subset.iloc[0].to_dict() if not gt2_subset.empty else {}
        
        for cat, cfg in categories_config.items():
            if "special" in cfg:
                cat_type = cfg["special"]
                if cat_type == "Primärverband":
                    g_pref, g_alt = "praeferenz_produkt", "alternative_produkt"
                else:
                    g_pref, g_alt = "ergaenzende_produkte_praeferenz", "ergaenzende_produkte_alternativ"
                    
                gt1_p = parse_cell_value(r_gt1.get(g_pref))
                gt1_a = parse_cell_value(r_gt1.get(g_alt))
                gt2_p = parse_cell_value(r_gt2.get(g_pref))
                gt2_a = parse_cell_value(r_gt2.get(g_alt))
                
                if normalised:
                    f1_val, exact_val = metrics.best_path_f1(
                        metrics.to_clean_set(clean.clean_whitespace(gt2_p)),
                        metrics.to_clean_set(clean.clean_whitespace(gt2_a)),
                        metrics.to_clean_set(clean.clean_whitespace(gt1_p)),
                        metrics.to_clean_set(clean.clean_whitespace(gt1_a))
                    )
                else:
                    f1_val, exact_val = metrics.best_path_f1(
                        metrics.to_clean_set(gt2_p),
                        metrics.to_clean_set(gt2_a),
                        metrics.to_clean_set(gt1_p),
                        metrics.to_clean_set(gt1_a)
                    )
                cat_scores[cat].append(f1_val)
                cat_exacts[cat].append(exact_val)
            else:
                gt_k = cfg["gt_key"]
                v_gt1 = parse_cell_value(r_gt1.get(gt_k))
                v_gt2 = parse_cell_value(r_gt2.get(gt_k))
                
                score_val = get_score(cat, v_gt1, v_gt2, raw_flag=(not normalised))
                exact_val = metrics.score_exact(v_gt1, v_gt2)
                
                if score_val is not None:
                    cat_scores[cat].append(score_val)
                    cat_exacts[cat].append(exact_val)
                    
    summary_rows = []
    for cat, cfg in categories_config.items():
        scores = cat_scores[cat]
        exacts = cat_exacts[cat]
        
        mean_score = sum(scores) / len(scores) if scores else float('nan')
        mean_exact = sum(exacts) / len(exacts) if exacts else float('nan')
        
        summary_rows.append({
            "Kategorie": cat,
            "Typ": cfg.get("special", cfg.get("metric_type")),
            "Score / F1-Score (Mean)": mean_score,
            "Exact-Match-Rate": mean_exact
        })
        
    return pd.DataFrame(summary_rows)


def compare_wunden_trace_interactive(path_llm_raw=None, path_llm_norm=None):
    """
    Erstellt ein interaktives Widget, mit dem man für ein ausgewähltes Wundbild 
    die Rohwerte und normalisierten Werte aller 3 Akteure (Experte 1, Experte 2, LLM) 
    nebeneinander in einer 7-spaltigen Tabelle nachverfolgen kann.
    """
    path_gt1_raw = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth.csv")
    path_gt1_norm = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv")
    path_gt2_raw = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth.csv")
    path_gt2_norm = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv")
    path_llm_raw = resolve_path(path_llm_raw) if path_llm_raw else resolve_path("../../data/llm_outputs/zero_shot_lr/zero_shot_lr_raw.csv")
    path_llm_norm = resolve_path(path_llm_norm) if path_llm_norm else resolve_path("../../data/llm_outputs/zero_shot_lr/zero_shot_lr_normalised.csv")
    
    df_gt1_r = load_csv(path_gt1_raw)
    df_gt1_n = load_csv(path_gt1_norm)
    df_gt2_r = load_csv(path_gt2_raw)
    df_gt2_n = load_csv(path_gt2_norm)
    df_llm_r = load_csv(path_llm_raw)
    df_llm_n = load_csv(path_llm_norm)
    
    for df in [df_gt1_r, df_gt1_n, df_gt2_r, df_gt2_n, df_llm_r, df_llm_n]:
        if not df.empty and "image_id" in df.columns:
            df["image_id"] = df["image_id"].apply(normalize_image_id)
            
    all_ids = []
    if not df_llm_r.empty:
        all_ids = sorted(df_llm_r["image_id"].dropna().unique().tolist())
    if not all_ids:
        all_ids = [f"wunde_{i:02d}" for i in range(1, 61)]
        
    categories_config = [
        ("Wundtyp", "wundtyp", "wundtyp"),
        ("Lokalisation", "lokalisation", "lokalisation"),
        ("Wundstadium", "wundstadium", "wundstadium"),
        ("Wundgrund", "wundgrund", "wundgrund"),
        ("Wundrand", "wundrand", "wundrand"),
        ("Wundumgebung", "wundumgebung", "wundumgebung"),
        ("Exsudat", "exsudat", "exsudat_menge"),
        ("Debridement notwendig", "debridement_notwendig", "debridement_notwendig"),
        ("Debridement Methode", "debridement", "debridement_methode"),
        ("Infektionsverdacht", "infektion", "infektion_vorhanden"),
        ("Spüllösung", "spuelloesung", "spuelloesung"),
        ("Primärverband", "Primärverband", "Primärverband"),
        ("Sekundärverband", "Sekundärverband", "Sekundärverband"),
        ("Kompression indiziert", "kompression_indiziert", "kompression_indiziert"),
        ("Kompression Produkt", "kompression_produkte", "kompression_produkt"),
    ]
    
    image_out = widgets.Output()
    table_out = widgets.Output()
    
    def render_table(image_id):
        def get_rec(df):
            if df.empty:
                return {}
            subset = df[df["image_id"] == image_id]
            if subset.empty:
                return {}
            return subset.iloc[0].to_dict()
            
        r_gt1_r = get_rec(df_gt1_r)
        r_gt1_n = get_rec(df_gt1_n)
        r_gt2_r = get_rec(df_gt2_r)
        r_gt2_n = get_rec(df_gt2_n)
        r_llm_r = get_rec(df_llm_r)
        r_llm_n = get_rec(df_llm_n)
        
        rows = []
        for cat_name, gt_key, llm_key in categories_config:
            if cat_name in ["Primärverband", "Sekundärverband"]:
                if cat_name == "Primärverband":
                    g_pref, g_alt = "praeferenz_produkt", "alternative_produkt"
                    l_pref, l_alt = "praeferenz_wundauflage", "alternativ_wundauflage"
                else:
                    g_pref, g_alt = "ergaenzende_produkte_praeferenz", "ergaenzende_produkte_alternativ"
                    l_pref, l_alt = "praeferenz_ergaenzung", "alternativ_ergaenzung"
                    
                gt1_r_str = f"<b>P:</b> {format_val(r_gt1_r.get(g_pref))}<br><b>A:</b> {format_val(r_gt1_r.get(g_alt))}"
                gt1_n_str = f"<b>P:</b> {format_val(r_gt1_n.get(g_pref))}<br><b>A:</b> {format_val(r_gt1_n.get(g_alt))}"
                gt2_r_str = f"<b>P:</b> {format_val(r_gt2_r.get(g_pref))}<br><b>A:</b> {format_val(r_gt2_r.get(g_alt))}"
                gt2_n_str = f"<b>P:</b> {format_val(r_gt2_n.get(g_pref))}<br><b>A:</b> {format_val(r_gt2_n.get(g_alt))}"
                llm_r_str = f"<b>P:</b> {format_val(r_llm_r.get(l_pref))}<br><b>A:</b> {format_val(r_llm_r.get(l_alt))}"
                llm_n_str = f"<b>P:</b> {format_val(r_llm_n.get(l_pref))}<br><b>A:</b> {format_val(r_llm_n.get(l_alt))}"
            else:
                gt1_r_str = format_val(parse_cell_value(r_gt1_r.get(gt_key)))
                gt1_n_str = format_val(parse_cell_value(r_gt1_n.get(gt_key)))
                gt2_r_str = format_val(parse_cell_value(r_gt2_r.get(gt_key)))
                gt2_n_str = format_val(parse_cell_value(r_gt2_n.get(gt_key)))
                llm_r_str = format_val(parse_cell_value(r_llm_r.get(llm_key)))
                llm_n_str = format_val(parse_cell_value(r_llm_n.get(llm_key)))
                
            rows.append({
                "Kategorie": cat_name,
                "GT Experte 1 Roh": gt1_r_str,
                "GT Experte 1 Norm": gt1_n_str,
                "GT Experte 2 Roh": gt2_r_str,
                "GT Experte 2 Norm": gt2_n_str,
                "LLM Output Roh": llm_r_str,
                "LLM Output Norm": llm_n_str
            })
            
        df_compare = pd.DataFrame(rows)
        
        def highlight_changes(data):
            styles = pd.DataFrame("", index=data.index, columns=data.columns)
            for idx, row in data.iterrows():
                if row["GT Experte 1 Roh"] != row["GT Experte 1 Norm"]:
                    styles.at[idx, "GT Experte 1 Norm"] = "background-color: #e0f2fe; font-weight: bold; color: #0369a1;"
                if row["GT Experte 2 Roh"] != row["GT Experte 2 Norm"]:
                    styles.at[idx, "GT Experte 2 Norm"] = "background-color: #e0f2fe; font-weight: bold; color: #0369a1;"
                if row["LLM Output Roh"] != row["LLM Output Norm"]:
                    styles.at[idx, "LLM Output Norm"] = "background-color: #e0f2fe; font-weight: bold; color: #0369a1;"
            return styles
            
        styler = df_compare.style.apply(highlight_changes, axis=None)
        styler = styler.hide(axis="index")
        
        # Spaltenbreiten
        styler = styler.set_properties(subset=["GT Experte 1 Roh", "GT Experte 1 Norm", "GT Experte 2 Roh", "GT Experte 2 Norm", "LLM Output Roh"], **{"width": "14%"})
        styler = styler.set_properties(subset=["LLM Output Norm"], **{"width": "17%"})
        styler = styler.set_properties(subset=["Kategorie"], **{"width": "13%"})
        
        styler = styler.set_table_styles([
            {"selector": "th", "props": [
                ("background-color", "#1d3557"), ("color", "white"),
                ("font-family", "Segoe UI, Arial, sans-serif"), ("font-size", "14px"),
                ("font-weight", "bold"), ("padding", "10px 12px"), ("border", "1px solid #d3d3d3"),
                ("text-align", "center")
            ]},
            {"selector": "td", "props": [
                ("font-family", "Segoe UI, Arial, sans-serif"), ("font-size", "13px"),
                ("padding", "8px 10px"), ("border", "1px solid #d3d3d3"),
                ("line-height", "1.4")
            ]},
            {"selector": ".col0, .col2, .col4", "props": [
                ("border-right", "2.5px solid #1d3557")
            ]},
            {"selector": "table", "props": [("border-collapse", "collapse"), ("width", "100%")]}
        ])
        
        display(HTML(f"<h3 style='font-family: Segoe UI, Arial, sans-serif; color: #1d3557; margin-top: 20px;'>Normalisierungs-Trace für {image_id}</h3>"))
        display(styler)
        
    def on_wund_change(change):
        image_id = change["new"]
        if image_id:
            with image_out:
                image_out.clear_output(wait=True)
                show_image(image_id)
            with table_out:
                table_out.clear_output(wait=True)
                render_table(image_id)
                
    wunde_select = widgets.Dropdown(
        options=all_ids,
        value=all_ids[0] if all_ids else None,
        description='Wund-ID:',
        style={'description_width': 'initial'},
        disabled=False,
    )
    wunde_select.observe(on_wund_change, names="value")
    
    with image_out:
        show_image(wunde_select.value)
    with table_out:
        render_table(wunde_select.value)
        
    display(widgets.VBox([image_out, wunde_select, table_out]))


def compare_categories_trace_interactive(path_llm_raw=None, path_llm_norm=None):
    """
    Erstellt ein interaktives Widget, mit dem man für eine ausgewählte Kategorie 
    die Rohwerte und normalisierten Werte aller Wundbilder nebeneinander 
    in einer 7-spaltigen Tabelle nachverfolgen kann.
    """
    path_gt1_raw = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth.csv")
    path_gt1_norm = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv")
    path_gt2_raw = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth.csv")
    path_gt2_norm = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv")
    path_llm_raw = resolve_path(path_llm_raw) if path_llm_raw else resolve_path("../../data/llm_outputs/zero_shot_lr/zero_shot_lr_raw.csv")
    path_llm_norm = resolve_path(path_llm_norm) if path_llm_norm else resolve_path("../../data/llm_outputs/zero_shot_lr/zero_shot_lr_normalised.csv")
    
    df_gt1_r = load_csv(path_gt1_raw)
    df_gt1_n = load_csv(path_gt1_norm)
    df_gt2_r = load_csv(path_gt2_raw)
    df_gt2_n = load_csv(path_gt2_norm)
    df_llm_r = load_csv(path_llm_raw)
    df_llm_n = load_csv(path_llm_norm)
    
    for df in [df_gt1_r, df_gt1_n, df_gt2_r, df_gt2_n, df_llm_r, df_llm_n]:
        if not df.empty and "image_id" in df.columns:
            df["image_id"] = df["image_id"].apply(normalize_image_id)
            
    all_ids = []
    if not df_llm_r.empty:
        all_ids = sorted(df_llm_r["image_id"].dropna().unique().tolist())
    if not all_ids:
        all_ids = [f"wunde_{i:02d}" for i in range(1, 61)]
        
    categories_config = {
        "Wundtyp": {"gt_key": "wundtyp", "llm_key": "wundtyp"},
        "Lokalisation": {"gt_key": "lokalisation", "llm_key": "lokalisation"},
        "Wundstadium": {"gt_key": "wundstadium", "llm_key": "wundstadium"},
        "Wundgrund": {"gt_key": "wundgrund", "llm_key": "wundgrund"},
        "Wundrand": {"gt_key": "wundrand", "llm_key": "wundrand"},
        "Wundumgebung": {"gt_key": "wundumgebung", "llm_key": "wundumgebung"},
        "Exsudat": {"gt_key": "exsudat", "llm_key": "exsudat_menge"},
        "Debridement notwendig": {"gt_key": "debridement_notwendig", "llm_key": "debridement_notwendig"},
        "Debridement Methode": {"gt_key": "debridement", "llm_key": "debridement_methode"},
        "Infektionsverdacht": {"gt_key": "infektion", "llm_key": "infektion_vorhanden"},
        "Spüllösung": {"gt_key": "spuelloesung", "llm_key": "spuelloesung"},
        "Primärverband": {"special": "Primärverband"},
        "Sekundärverband": {"special": "Sekundärverband"},
        "Kompression indiziert": {"gt_key": "kompression_indiziert", "llm_key": "kompression_indiziert"},
        "Kompression Produkt": {"gt_key": "kompression_produkte", "llm_key": "kompression_produkt"}
    }
    
    table_out = widgets.Output()
    
    def render_table(category_name):
        cfg = categories_config[category_name]
        rows = []
        
        for img_id in all_ids:
            def get_rec(df):
                if df.empty:
                    return {}
                subset = df[df["image_id"] == img_id]
                if subset.empty:
                    return {}
                return subset.iloc[0].to_dict()
                
            r_gt1_r = get_rec(df_gt1_r)
            r_gt1_n = get_rec(df_gt1_n)
            r_gt2_r = get_rec(df_gt2_r)
            r_gt2_n = get_rec(df_gt2_n)
            r_llm_r = get_rec(df_llm_r)
            r_llm_n = get_rec(df_llm_n)
            
            if "special" in cfg:
                cat_type = cfg["special"]
                if cat_type == "Primärverband":
                    g_pref, g_alt = "praeferenz_produkt", "alternative_produkt"
                    l_pref, l_alt = "praeferenz_wundauflage", "alternativ_wundauflage"
                else:
                    g_pref, g_alt = "ergaenzende_produkte_praeferenz", "ergaenzende_produkte_alternativ"
                    l_pref, l_alt = "praeferenz_ergaenzung", "alternativ_ergaenzung"
                    
                gt1_r_str = f"<b>P:</b> {format_val(r_gt1_r.get(g_pref))}<br><b>A:</b> {format_val(r_gt1_r.get(g_alt))}"
                gt1_n_str = f"<b>P:</b> {format_val(r_gt1_n.get(g_pref))}<br><b>A:</b> {format_val(r_gt1_n.get(g_alt))}"
                gt2_r_str = f"<b>P:</b> {format_val(r_gt2_r.get(g_pref))}<br><b>A:</b> {format_val(r_gt2_r.get(g_alt))}"
                gt2_n_str = f"<b>P:</b> {format_val(r_gt2_n.get(g_pref))}<br><b>A:</b> {format_val(r_gt2_n.get(g_alt))}"
                llm_r_str = f"<b>P:</b> {format_val(r_llm_r.get(l_pref))}<br><b>A:</b> {format_val(r_llm_r.get(l_alt))}"
                llm_n_str = f"<b>P:</b> {format_val(r_llm_n.get(l_pref))}<br><b>A:</b> {format_val(r_llm_n.get(l_alt))}"
            else:
                gt_k = cfg["gt_key"]
                llm_k = cfg["llm_key"]
                
                gt1_r_str = format_val(parse_cell_value(r_gt1_r.get(gt_k)))
                gt1_n_str = format_val(parse_cell_value(r_gt1_n.get(gt_k)))
                gt2_r_str = format_val(parse_cell_value(r_gt2_r.get(gt_k)))
                gt2_n_str = format_val(parse_cell_value(r_gt2_n.get(gt_k)))
                llm_r_str = format_val(parse_cell_value(r_llm_r.get(llm_k)))
                llm_n_str = format_val(parse_cell_value(r_llm_n.get(llm_k)))
                
            rows.append({
                "Wund-ID": img_id,
                "GT Experte 1 Roh": gt1_r_str,
                "GT Experte 1 Norm": gt1_n_str,
                "GT Experte 2 Roh": gt2_r_str,
                "GT Experte 2 Norm": gt2_n_str,
                "LLM Output Roh": llm_r_str,
                "LLM Output Norm": llm_n_str
            })
            
        df_compare = pd.DataFrame(rows)
        
        if not df_compare.empty:
            df_compare = df_compare.sort_values(
                by='Wund-ID',
                key=lambda x: x.str.extract(r'(\d+)')[0].astype(float)
            ).reset_index(drop=True)
            
        def highlight_changes(data):
            styles = pd.DataFrame("", index=data.index, columns=data.columns)
            for idx, row in data.iterrows():
                if row["GT Experte 1 Roh"] != row["GT Experte 1 Norm"]:
                    styles.at[idx, "GT Experte 1 Norm"] = "background-color: #e0f2fe; font-weight: bold; color: #0369a1;"
                if row["GT Experte 2 Roh"] != row["GT Experte 2 Norm"]:
                    styles.at[idx, "GT Experte 2 Norm"] = "background-color: #e0f2fe; font-weight: bold; color: #0369a1;"
                if row["LLM Output Roh"] != row["LLM Output Norm"]:
                    styles.at[idx, "LLM Output Norm"] = "background-color: #e0f2fe; font-weight: bold; color: #0369a1;"
            return styles
            
        styler = df_compare.style.apply(highlight_changes, axis=None)
        styler = styler.hide(axis="index")
        
        # Spaltenbreiten
        styler = styler.set_properties(subset=["GT Experte 1 Roh", "GT Experte 1 Norm", "GT Experte 2 Roh", "GT Experte 2 Norm", "LLM Output Roh"], **{"width": "14%"})
        styler = styler.set_properties(subset=["LLM Output Norm"], **{"width": "17%"})
        styler = styler.set_properties(subset=["Wund-ID"], **{"width": "13%"})
        
        styler = styler.set_table_styles([
            {"selector": "th", "props": [
                ("background-color", "#1d3557"), ("color", "white"),
                ("font-family", "Segoe UI, Arial, sans-serif"), ("font-size", "14px"),
                ("font-weight", "bold"), ("padding", "10px 12px"), ("border", "1px solid #d3d3d3"),
                ("text-align", "center")
            ]},
            {"selector": "td", "props": [
                ("font-family", "Segoe UI, Arial, sans-serif"), ("font-size", "13px"),
                ("padding", "8px 10px"), ("border", "1px solid #d3d3d3"),
                ("line-height", "1.4")
            ]},
            {"selector": ".col0, .col2, .col4", "props": [
                ("border-right", "2.5px solid #1d3557")
            ]},
            {"selector": "table", "props": [("border-collapse", "collapse"), ("width", "100%")]}
        ])
        
        display(HTML(f"<h3 style='font-family: Segoe UI, Arial, sans-serif; color: #1d3557; margin-top: 20px;'>Normalisierungs-Trace für Kategorie: {category_name}</h3>"))
        display(styler)
        
    def on_cat_change(change):
        category_name = change["new"]
        if category_name:
            with table_out:
                table_out.clear_output(wait=True)
                render_table(category_name)
                
    cat_select = widgets.Dropdown(
        options=list(categories_config.keys()),
        value="Wundtyp",
        description="Kategorie:",
        style={'description_width': 'initial'},
        disabled=False,
    )
    cat_select.observe(on_cat_change, names="value")
    
    with table_out:
        render_table(cat_select.value)
        
    display(widgets.VBox([cat_select, table_out]))


def calculate_consensus_summary_LR(normalised=False, path_llm_raw=None, path_llm_norm=None):
    """
    Berechnet die aggregierten Metriken (Mean Score und Exact-Match-Rate) über alle Wundbilder,
    wobei für jedes Wundbild und jede Kategorie der jeweils bessere Score (Maximum) 
    aus dem Vergleich mit Experte 1 und Experte 2 gewählt wird.
    """
    path_gt1_raw = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth.csv")
    path_gt1_norm = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv")
    path_gt2_raw = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth.csv")
    path_gt2_norm = resolve_path("../../data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv")
    path_llm_raw = resolve_path(path_llm_raw) if path_llm_raw else resolve_path("../../data/llm_outputs/zero_shot_lr/zero_shot_lr_raw.csv")
    path_llm_norm = resolve_path(path_llm_norm) if path_llm_norm else resolve_path("../../data/llm_outputs/zero_shot_lr/zero_shot_lr_normalised.csv")
    
    df_gt1 = load_csv(path_gt1_norm if normalised else path_gt1_raw)
    df_gt2 = load_csv(path_gt2_norm if normalised else path_gt2_raw)
    df_llm = load_csv(path_llm_norm if normalised else path_llm_raw)
    
    for df in [df_gt1, df_gt2, df_llm]:
        if not df.empty and "image_id" in df.columns:
            df["image_id"] = df["image_id"].apply(normalize_image_id)
            
    all_ids = []
    if not df_llm.empty:
        all_ids = sorted(df_llm["image_id"].dropna().unique().tolist())
    if not all_ids:
        all_ids = [f"wunde_{i:02d}" for i in range(1, 61)]
        
    categories_config = {
        "Wundtyp": {"gt_key": "wundtyp", "llm_key": "wundtyp", "metric_type": "exact"},
        "Lokalisation": {"gt_key": "lokalisation", "llm_key": "lokalisation", "metric_type": "exact"},
        "Wundstadium": {"gt_key": "wundstadium", "llm_key": "wundstadium", "metric_type": "checklist"},
        "Wundgrund": {"gt_key": "wundgrund", "llm_key": "wundgrund", "metric_type": "checklist"},
        "Wundrand": {"gt_key": "wundrand", "llm_key": "wundrand", "metric_type": "checklist"},
        "Wundumgebung": {"gt_key": "wundumgebung", "llm_key": "wundumgebung", "metric_type": "checklist"},
        "Exsudat": {"gt_key": "exsudat", "llm_key": "exsudat_menge", "metric_type": "ordinal"},
        "Debridement notwendig": {"gt_key": "debridement_notwendig", "llm_key": "debridement_notwendig", "metric_type": "exact"},
        "Debridement Methode": {"gt_key": "debridement", "llm_key": "debridement_methode", "metric_type": "checklist"},
        "Infektionsverdacht": {"gt_key": "infektion", "llm_key": "infektion_vorhanden", "metric_type": "exact"},
        "Spüllösung": {"gt_key": "spuelloesung", "llm_key": "spuelloesung", "metric_type": "exact"},
        "Primärverband": {"special": "Primärverband", "metric_type": "cross_match"},
        "Sekundärverband": {"special": "Sekundärverband", "metric_type": "cross_match"},
        "Kompression indiziert": {"gt_key": "kompression_indiziert", "llm_key": "kompression_indiziert", "metric_type": "exact"},
        "Kompression Produkt": {"gt_key": "kompression_produkte", "llm_key": "kompression_produkt", "metric_type": "checklist"}
    }
    
    # Für jedes Wundbild und jede Kategorie den Score berechnen
    cat_scores = {cat: [] for cat in categories_config}
    cat_exacts = {cat: [] for cat in categories_config}
    
    for img_id in all_ids:
        gt1_subset = df_gt1[df_gt1["image_id"] == img_id]
        gt2_subset = df_gt2[df_gt2["image_id"] == img_id]
        llm_subset = df_llm[df_llm["image_id"] == img_id]
        
        r_gt1 = gt1_subset.iloc[0].to_dict() if not gt1_subset.empty else {}
        r_gt2 = gt2_subset.iloc[0].to_dict() if not gt2_subset.empty else {}
        r_llm = llm_subset.iloc[0].to_dict() if not llm_subset.empty else {}
        
        for cat, cfg in categories_config.items():
            if "special" in cfg:
                cat_type = cfg["special"]
                if cat_type == "Primärverband":
                    g_pref, g_alt = "praeferenz_produkt", "alternative_produkt"
                    l_pref, l_alt = "praeferenz_wundauflage", "alternativ_wundauflage"
                else:
                    g_pref, g_alt = "ergaenzende_produkte_praeferenz", "ergaenzende_produkte_alternativ"
                    l_pref, l_alt = "praeferenz_ergaenzung", "alternativ_ergaenzung"
                    
                gt1_p = parse_cell_value(r_gt1.get(g_pref))
                gt1_a = parse_cell_value(r_gt1.get(g_alt))
                gt2_p = parse_cell_value(r_gt2.get(g_pref))
                gt2_a = parse_cell_value(r_gt2.get(g_alt))
                llm_p = parse_cell_value(r_llm.get(l_pref))
                llm_a = parse_cell_value(r_llm.get(l_alt))
                
                # F1 vs Expert 1 und 2
                if normalised:
                    f1_1, exact1 = metrics.best_path_f1(
                        metrics.to_clean_set(clean.clean_whitespace(llm_p)),
                        metrics.to_clean_set(clean.clean_whitespace(llm_a)),
                        metrics.to_clean_set(clean.clean_whitespace(gt1_p)),
                        metrics.to_clean_set(clean.clean_whitespace(gt1_a))
                    )
                    f1_2, exact2 = metrics.best_path_f1(
                        metrics.to_clean_set(clean.clean_whitespace(llm_p)),
                        metrics.to_clean_set(clean.clean_whitespace(llm_a)),
                        metrics.to_clean_set(clean.clean_whitespace(gt2_p)),
                        metrics.to_clean_set(clean.clean_whitespace(gt2_a))
                    )
                else:
                    f1_1, exact1 = metrics.best_path_f1(
                        metrics.to_clean_set(llm_p),
                        metrics.to_clean_set(llm_a),
                        metrics.to_clean_set(gt1_p),
                        metrics.to_clean_set(gt1_a)
                    )
                    f1_2, exact2 = metrics.best_path_f1(
                        metrics.to_clean_set(llm_p),
                        metrics.to_clean_set(llm_a),
                        metrics.to_clean_set(gt2_p),
                        metrics.to_clean_set(gt2_a)
                    )
                cat_scores[cat].append(max(f1_1, f1_2))
                cat_exacts[cat].append(max(exact1, exact2))
            else:
                gt_k = cfg["gt_key"]
                llm_k = cfg["llm_key"]
                
                v_gt1 = parse_cell_value(r_gt1.get(gt_k))
                v_gt2 = parse_cell_value(r_gt2.get(gt_k))
                v_llm = parse_cell_value(r_llm.get(llm_k))
                
                s1 = get_score(cat, v_gt1, v_llm, raw_flag=(not normalised))
                s2 = get_score(cat, v_gt2, v_llm, raw_flag=(not normalised))
                exact1 = metrics.score_exact(v_gt1, v_llm)
                exact2 = metrics.score_exact(v_gt2, v_llm)
                
                if s1 is not None and s2 is not None:
                    cat_scores[cat].append(max(s1, s2))
                    cat_exacts[cat].append(max(exact1, exact2))
                    
    summary_rows = []
    for cat, cfg in categories_config.items():
        scores = cat_scores[cat]
        exacts = cat_exacts[cat]
        
        mean_score = sum(scores) / len(scores) if scores else float('nan')
        mean_exact = sum(exacts) / len(exacts) if exacts else float('nan')
        
        summary_rows.append({
            "Kategorie": cat,
            "Typ": cfg.get("special", cfg.get("metric_type")),
            "Score / F1-Score (Mean)": mean_score,
            "Exact-Match-Rate": mean_exact
        })
        
    return pd.DataFrame(summary_rows)
