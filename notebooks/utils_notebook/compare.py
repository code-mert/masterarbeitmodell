import os
import sys
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, HTML

# Ensure parent directory (project root) is in the path to allow loading eval module
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from eval.loaders import load_ground_truth, load_llm_outputs, matched_image_ids, normalize_image_id

def compare_wunden_interactive(csv_path: str, json_dir: str):
    """
    Sets up an interactive widget with a dropdown to select a wound and compare
    Ground Truth and LLM outputs side-by-side.
    """
    # 1. Load data
    try:
        gt_data = load_ground_truth(csv_path)
        llm_data = load_llm_outputs(json_dir)
    except Exception as e:
        print(f"Fehler beim Laden der Daten: {e}")
        return

    # 2. Find intersecting image IDs
    matched_ids = matched_image_ids(gt_data, llm_data)
    if not matched_ids:
        print("Keine übereinstimmenden Wundbilder (image_ids) gefunden.")
        return

    print(f"Erfolgreich {len(matched_ids)} Wundbilder zum Vergleich geladen.")

    # Helper function to format values beautifully
    def format_val(val):
        if val is None:
            return "—"
        if isinstance(val, (list, set, tuple)):
            if len(val) == 0:
                return "—"
            return ", ".join(str(item) for item in val if item)
        if isinstance(val, str):
            val_stripped = val.strip()
            if val_stripped.startswith('[') and val_stripped.endswith(']'):
                try:
                    import ast
                    parsed = ast.literal_eval(val_stripped)
                    if isinstance(parsed, (list, tuple, set)):
                        if len(parsed) == 0:
                            return "—"
                        return ", ".join(str(item) for item in parsed if item)
                except:
                    pass
            if val_stripped in ["", "nan", "—"]:
                return "—"
            return val_stripped
        return str(val)

    # Function to get resolved wundtyp for LLM (replacing "Sonstiges" with the custom text)
    def get_resolved_wundtyp(llm_rec):
        raw_wundtyp = llm_rec.get("wundtyp")
        # Handle list format
        if isinstance(raw_wundtyp, (list, set, tuple)):
            resolved = []
            for item in raw_wundtyp:
                if str(item).strip().lower() == "sonstiges":
                    sonstiges_val = llm_rec.get("wundtyp_sonstiges")
                    if sonstiges_val and str(sonstiges_val).strip():
                        resolved.append(str(sonstiges_val))
                    else:
                        resolved.append(str(item))
                else:
                    resolved.append(str(item))
            return resolved
        # Handle single string format
        elif isinstance(raw_wundtyp, str):
            if raw_wundtyp.strip().lower() == "sonstiges":
                sonstiges_val = llm_rec.get("wundtyp_sonstiges")
                if sonstiges_val and str(sonstiges_val).strip():
                    return sonstiges_val
            return raw_wundtyp
        return raw_wundtyp

    # 3. Define compare function for widgets
    def compare_single(image_id):
        if not image_id:
            print("Kein Wundbild ausgewählt.")
            return

        normalized_id = normalize_image_id(image_id)
        if not normalized_id or normalized_id not in gt_data or normalized_id not in llm_data:
            print(f"Fehler: Daten für {image_id} konnten nicht gefunden/normalisiert werden.")
            return

        gt_rec = gt_data[normalized_id]
        llm_rec = llm_data[normalized_id]

        # Resolve "Sonstiges" for wundtyp
        resolved_llm_wundtyp = get_resolved_wundtyp(llm_rec)

        # Auto-detect if we are in L&R mode
        is_lr = "praeferenz_wundauflage" in llm_rec

        if is_lr:
            # Helper to resolve "Sonstiges" for other L&R fields
            def get_resolved_field(field_name):
                raw_val = llm_rec.get(field_name)
                sonstiges_key = f"{field_name}_sonstiges"
                if not raw_val:
                    return raw_val
                if isinstance(raw_val, (list, set, tuple)):
                    resolved = []
                    for item in raw_val:
                        if str(item).strip().lower() == "sonstiges":
                            sonstiges_val = llm_rec.get(sonstiges_key)
                            if sonstiges_val and str(sonstiges_val).strip():
                                resolved.append(str(sonstiges_val))
                            else:
                                resolved.append(str(item))
                        else:
                            resolved.append(str(item))
                    return resolved
                elif isinstance(raw_val, str):
                    if raw_val.strip().lower() == "sonstiges":
                        sonstiges_val = llm_rec.get(sonstiges_key)
                        if sonstiges_val and str(sonstiges_val).strip():
                            return sonstiges_val
                    return raw_val
                return raw_val

            resolved_llm_wundstadium = get_resolved_field("wundstadium")
            resolved_llm_wundrand = get_resolved_field("wundrand")
            resolved_llm_wundumgebung = get_resolved_field("wundumgebung")

            comparison_rows = [
                # === KLINISCHE ANAMNESE UND STATUS ===
                {"Kategorie": "Wundtyp", "Ground Truth (GT)": format_val(gt_rec.get("wundtyp")), "LLM Output": format_val(resolved_llm_wundtyp)},
                {"Kategorie": "Lokalisation", "Ground Truth (GT)": format_val(gt_rec.get("lokalisation")), "LLM Output": format_val(llm_rec.get("lokalisation"))},
                {"Kategorie": "Wundstadium / -phase", "Ground Truth (GT)": format_val(gt_rec.get("wundstadium")), "LLM Output": format_val(resolved_llm_wundstadium)},
                {"Kategorie": "Wundgrund", "Ground Truth (GT)": format_val(gt_rec.get("wundgrund")), "LLM Output": format_val(llm_rec.get("wundgrund"))},
                {"Kategorie": "Exsudat-Menge", "Ground Truth (GT)": format_val(gt_rec.get("exsudat")), "LLM Output": format_val(llm_rec.get("exsudat_menge"))},
                {"Kategorie": "Infektionsstatus", "Ground Truth (GT)": format_val(gt_rec.get("infektion")), "LLM Output": format_val(llm_rec.get("infektion_vorhanden"))},
                {"Kategorie": "Wundrand", "Ground Truth (GT)": format_val(gt_rec.get("wundrand")), "LLM Output": format_val(resolved_llm_wundrand)},
                {"Kategorie": "Wundumgebung", "Ground Truth (GT)": format_val(gt_rec.get("wundumgebung")), "LLM Output": format_val(resolved_llm_wundumgebung)},
                {"Kategorie": "Weitere Auffälligkeiten", "Ground Truth (GT)": format_val(gt_rec.get("auffaelligkeiten")), "LLM Output": format_val(llm_rec.get("weitere_auffaelligkeiten"))},
                
                # === BEHANDLUNGSEMPFEHLUNGEN ===
                {"Kategorie": "Débridement notwendig?", "Ground Truth (GT)": format_val(gt_rec.get("debridement_notwendig")), "LLM Output": format_val(llm_rec.get("debridement_notwendig"))},
                {"Kategorie": "Débridement-Methode", "Ground Truth (GT)": format_val(gt_rec.get("debridement")), "LLM Output": format_val(llm_rec.get("debridement_methode"))},
                {"Kategorie": "Spüllösung", "Ground Truth (GT)": format_val(gt_rec.get("spuelloesung")), "LLM Output": format_val(llm_rec.get("spuelloesung"))},
                {"Kategorie": "1. Primärverband (Präferenz)", "Ground Truth (GT)": format_val(gt_rec.get("praeferenz_produkt")), "LLM Output": format_val(llm_rec.get("praeferenz_wundauflage"))},
                {"Kategorie": "1. Primärverband (Alternative)", "Ground Truth (GT)": format_val(gt_rec.get("alternative_produkt")), "LLM Output": format_val(llm_rec.get("alternativ_wundauflage"))},
                
                {"Kategorie": "4. Sekundärverband / Fixierung (Präferenz)", "Ground Truth (GT)": format_val(gt_rec.get("ergaenzende_produkte_praeferenz")), "LLM Output": format_val(llm_rec.get("praeferenz_ergaenzung"))},
                {"Kategorie": "4. Sekundärverband / Fixierung (Alternative)", "Ground Truth (GT)": format_val(gt_rec.get("ergaenzende_produkte_alternativ")), "LLM Output": format_val(llm_rec.get("alternativ_ergaenzung"))},
                
                # Kompressions-Teil (Ja/Nein + Produkt)
                {"Kategorie": "Kompression indiziert?", "Ground Truth (GT)": format_val(gt_rec.get("kompression_indiziert")), "LLM Output": format_val(llm_rec.get("kompression_indiziert"))},
                {"Kategorie": "Kompression (Art/Produkte)", "Ground Truth (GT)": format_val(gt_rec.get("kompression_produkte")), "LLM Output": format_val(llm_rec.get("kompression_produkt"))},
                
                # Einschränkungen / Annahmen
                {"Kategorie": "Einschränkungen / Annahmen", "Ground Truth (GT)": format_val(gt_rec.get("einschraenkungen")), "LLM Output": format_val(llm_rec.get("einschraenkungen_annahmen"))},
            ]
        else:
            comparison_rows = [
                # === KLINISCHE ANAMNESE UND STATUS ===
                {"Kategorie": "Wundtyp", "Ground Truth (GT)": format_val(gt_rec.get("wundtyp")), "LLM Output": format_val(resolved_llm_wundtyp)},
                {"Kategorie": "Spezifizierung", "Ground Truth (GT)": format_val(gt_rec.get("wundtyp_spezifikation")), "LLM Output": format_val(llm_rec.get("wundtyp_spezifizierung"))},
                {"Kategorie": "Lokalisation", "Ground Truth (GT)": format_val(gt_rec.get("lokalisation")), "LLM Output": format_val(llm_rec.get("lokalisation"))},
                {"Kategorie": "Wundstadium / -phase", "Ground Truth (GT)": format_val(gt_rec.get("wundstadium")), "LLM Output": format_val(llm_rec.get("wundphase"))},
                {"Kategorie": "Exsudat-Menge", "Ground Truth (GT)": format_val(gt_rec.get("exsudat")), "LLM Output": format_val(llm_rec.get("exsudat_menge"))},
                {"Kategorie": "Infektionsstatus", "Ground Truth (GT)": format_val(gt_rec.get("infektion")), "LLM Output": format_val(llm_rec.get("infektionsstatus"))},
                {"Kategorie": "Wundrand", "Ground Truth (GT)": format_val(gt_rec.get("wundrand")), "LLM Output": format_val(llm_rec.get("wundrand"))},
                {"Kategorie": "Wundumgebung", "Ground Truth (GT)": format_val(gt_rec.get("wundumgebung")), "LLM Output": format_val(llm_rec.get("wundumgebung"))},
                {"Kategorie": "Weitere Auffälligkeiten", "Ground Truth (GT)": format_val(gt_rec.get("auffaelligkeiten")), "LLM Output": format_val(llm_rec.get("weitere_auffaelligkeiten"))},
                
                # === BEHANDLUNGSEMPFEHLUNGEN ===
                {"Kategorie": "Débridement notwendig?", "Ground Truth (GT)": format_val(gt_rec.get("debridement_notwendig")), "LLM Output": format_val(llm_rec.get("debridement_notwendig"))},
                {"Kategorie": "Débridement-Methode", "Ground Truth (GT)": format_val(gt_rec.get("debridement")), "LLM Output": format_val(llm_rec.get("debridement_methode"))},
                {"Kategorie": "Spüllösung", "Ground Truth (GT)": format_val(gt_rec.get("spuelloesung")), "LLM Output": format_val(llm_rec.get("spuelloesung"))},
                {"Kategorie": "1. Primärverband (Präferenz)", "Ground Truth (GT)": format_val(gt_rec.get("praeferenz_produkt")), "LLM Output": format_val(llm_rec.get("praeferenz_verbandklasse"))},
                {"Kategorie": "1. Primärverband (Alternative)", "Ground Truth (GT)": format_val(gt_rec.get("alternative_produkt")), "LLM Output": format_val(llm_rec.get("alternativ_verbandklasse"))},
                
                # Antimikrobieller Teil (Ja/Nein + Produkt)
                {"Kategorie": "Antimikrobieller Verband?", "Ground Truth (GT)": format_val(gt_rec.get("antimikrobiell_notwendig")), "LLM Output": format_val(llm_rec.get("antimikrobieller_verband"))},
                {"Kategorie": "Antimikrobielles Agens", "Ground Truth (GT)": format_val(gt_rec.get("antimikrobielles_agens")), "LLM Output": format_val(llm_rec.get("antimikrobielles_agens"))},
                
                {"Kategorie": "4. Sekundärverband / Fixierung", "Ground Truth (GT)": format_val(gt_rec.get("sekundaerverband")), "LLM Output": format_val(llm_rec.get("sekundaerverband_fixierung"))},
                {"Kategorie": "5. Hautschutz", "Ground Truth (GT)": format_val(gt_rec.get("hautschutz")), "LLM Output": format_val(llm_rec.get("wundrand_hautschutz"))},
                
                # Kompressions-Teil (Ja/Nein + Produkt)
                {"Kategorie": "Kompression indiziert?", "Ground Truth (GT)": format_val(gt_rec.get("kompression_indiziert")), "LLM Output": format_val(llm_rec.get("kompression_indiziert"))},
                {"Kategorie": "Kompression (Art/Produkte)", "Ground Truth (GT)": format_val(gt_rec.get("kompression_produkte")), "LLM Output": format_val(llm_rec.get("kompression_art"))},
                
                # Einschränkungen / Annahmen
                {"Kategorie": "Einschränkungen / Annahmen", "Ground Truth (GT)": format_val(gt_rec.get("einschraenkungen")), "LLM Output": format_val(llm_rec.get("einschraenkungen_annahmen"))},
            ]

        df_compare = pd.DataFrame(comparison_rows)

        # Style the comparison table
        def values_match(val1, val2):
            def split_by_delimiters_outside_parentheses(text, delimiters=[',', '|'], strip=True):
                if not isinstance(text, str):
                    return [text]
                
                text_stripped = text.strip()
                
                # If the text is wrapped in brackets or quotes, it represents a quoted list of items
                starts_ends_quotes = (text_stripped.startswith('"') and text_stripped.endswith('"')) or \
                                     (text_stripped.startswith("'") and text_stripped.endswith("'"))
                starts_ends_brackets = (text_stripped.startswith('[') and text_stripped.endswith(']'))
                
                if starts_ends_quotes or starts_ends_brackets:
                    double_quotes_count = text_stripped.count('"')
                    single_quotes_count = text_stripped.count("'")
                    
                    # If it uses double quotes, extract all double-quoted substrings
                    if double_quotes_count >= 2:
                        import re
                        items = re.findall(r'"([^"]*)"', text_stripped)
                        if items:
                            return [p.strip() if strip else p for p in items if p.strip()]
                            
                    # If it uses single quotes, extract all single-quoted substrings
                    if single_quotes_count >= 2:
                        import re
                        items = re.findall(r"'([^']*)'", text_stripped)
                        if items:
                            return [p.strip() if strip else p for p in items if p.strip()]
                
                # Define protected phrases (case-insensitive)
                protected_phrases = [
                    "cvi-typische hautveränderungen (hyperpigmentierung, atrophie blanche, lipodermatosklerose)",
                    "cvi-typische hautveränderungen (hyperppigmentierung, atropie blanche, lipodermatosklerose)",
                    "cvi-typische hautveränderungen (hyperpigmentierung, atrophie blanche, lipdermatosklerose)",
                    "autolytisch (hydrogele, hydrokolloide, folienverbände)",
                    "mechanisch (monofilament-pad, feuchte kompressen, wundspülung)",
                    "chirurgisch/scharf (skalpell, kürette)",
                    "neutrale spüllösung (nacl, ringer)",
                    "antimikrobielle spüllösung (phmb, octenisept)"
                ]
                
                temp_text = text
                replacements = {}
                for i, phrase in enumerate(protected_phrases):
                    start = 0
                    while True:
                        idx = temp_text.lower().find(phrase, start)
                        if idx == -1:
                            break
                        matched_text = temp_text[idx:idx+len(phrase)]
                        placeholder = f"__PROTECTED_PHRASE_{i}__"
                        replacements[placeholder] = matched_text
                        temp_text = temp_text[:idx] + placeholder + temp_text[idx+len(phrase):]
                        start = idx + len(placeholder)

                parts = []
                current = []
                depth = 0
                for char in temp_text:
                    if char == '(':
                        depth += 1
                    elif char == ')':
                        depth = max(0, depth - 1)
                    
                    if char in delimiters and depth == 0:
                        part = "".join(current)
                        if strip:
                            part = part.strip()
                        parts.append(part)
                        current = []
                    else:
                        current.append(char)
                if current:
                    part = "".join(current)
                    if strip:
                        part = part.strip()
                    parts.append(part)
                
                # Restore replacements in split parts
                restored_parts = []
                for part in parts:
                    for placeholder, original in replacements.items():
                        part = part.replace(placeholder, original)
                    restored_parts.append(part)
                    
                return [p for p in restored_parts if p]

            def to_set(v):
                if v is None:
                    return set()
                v_str = str(v).strip().lower()
                if v_str in ["—", "— (leer)", "nan", ""]:
                    return set()
                parts = [x.strip() for x in split_by_delimiters_outside_parentheses(v_str)]
                return set(parts)
            return to_set(val1) == to_set(val2)

        def style_rows(row):
            gt_val = row["Ground Truth (GT)"]
            llm_val = row["LLM Output"]
            is_match = values_match(gt_val, llm_val)
            color = "#e8f5e9" if is_match else "#fff3e0"
            text_color = "#2e7d32" if is_match else "#e65100"
            return [
                "",
                f"background-color: {color}; color: {text_color}; font-weight: 500;",
                f"background-color: {color}; color: {text_color}; font-weight: 500;"
            ]

        styled_compare = df_compare.style.apply(style_rows, axis=1).set_table_styles([
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

        display(HTML(f"<h3 style='font-family: Segoe UI, Arial, sans-serif; color: #1d3557; margin-top: 20px;'>Detailvergleich für Bild-ID: {normalized_id}</h3>"))
        display(styled_compare)

    # 4. Create widget dropdown and register interactive trigger
    wunde_select = widgets.Dropdown(
        options=matched_ids,
        value=matched_ids[0] if matched_ids else None,
        description='Wundbild:',
        style={'description_width': 'initial'},
        disabled=False,
    )

    return widgets.interactive(compare_single, image_id=wunde_select)


def compare_categories_detailed_interactive(raw_csv_gt: str, raw_csv_llm: str, norm_csv_gt: str, norm_csv_llm: str):
    """
    Sets up an interactive widget to compare Ground Truth and LLM outputs (raw vs. normalized)
    for a selected category, with color highlighting for score drops.
    """
    import ast
    import json
    import pandas as pd
    import ipywidgets as widgets
    from IPython.display import display, HTML, clear_output
    from utils_notebook.metrics_explorer import COLUMN_MAPPING, CATEGORY_TYPES
    from utils_notebook import metrics, clean
    from eval.loaders import normalize_image_id

    # Delimiter detection helper
    def detect_delimiter(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                first_line = f.readline()
                return ";" if ";" in first_line else ","
        except:
            return ","

    # Auto-detect if L&R mode
    try:
        df_llm_temp = pd.read_csv(raw_csv_llm, nrows=1)
        is_lr = "praeferenz_wundauflage" in df_llm_temp.columns
    except:
        is_lr = False

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
            "wundgrund": "wundgrund",
        }
    else:
        col_mapping = COLUMN_MAPPING

    # Filter categories so that they only contain fields present in both files
    try:
        sep_gt = detect_delimiter(raw_csv_gt)
        sep_llm = detect_delimiter(raw_csv_llm)
        df_gt_cols = pd.read_csv(raw_csv_gt, sep=sep_gt, nrows=0).columns.tolist()
        df_llm_cols = pd.read_csv(raw_csv_llm, sep=sep_llm, nrows=0).columns.tolist()
    except Exception as e:
        df_gt_cols = []
        df_llm_cols = []

    valid_categories = []
    for gt_col, llm_col in col_mapping.items():
        if gt_col in df_gt_cols and llm_col in df_llm_cols:
            valid_categories.append(gt_col)
    
    categories = sorted(valid_categories)


    def parse_cell_value(val):
        """Konvertiert String-Repräsentationen von Listen wieder in echte Listen."""
        if not isinstance(val, str):
            return val
        val_stripped = val.strip()
        if val_stripped.startswith('[') and val_stripped.endswith(']'):
            try:
                parsed = ast.literal_eval(val_stripped)
                if isinstance(parsed, (list, tuple, set)):
                    return list(parsed)
            except Exception:
                pass
        return val_stripped

    def get_row_score_for_cat(cat, gt_val, llm_val):
        """Berechnet den Score passend zum Kategorie-Typ."""
        cat_type = "exact"
        for t, cats in CATEGORY_TYPES.items():
            if cat in cats:
                cat_type = t
                break
                
        # Wundtyp Sonderfall
        if cat == "wundtyp":
            gt_set = metrics.to_clean_set(gt_val)
            llm_set = metrics.to_clean_set(llm_val)
            return 1.0 if gt_set == llm_set else 0.0
            
        if cat_type == "exact":
            return metrics.score_exact(gt_val, llm_val)
        elif cat_type == "ordinal":
            score, _ = metrics.score_ordinal(cat, gt_val, llm_val)
            return score
        else: # checklist / decode
            f1, _ = metrics.evaluate_checklist(gt_val, llm_val)
            return f1

    def show_category_details(selected_cat):
        # Delimiter detection
        def detect_delimiter(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    first_line = f.readline()
                    return ";" if ";" in first_line else ","
            except:
                return ","

        # Laden der DataFrames und Füllen von NaNs
        try:
            sep_gt_r = detect_delimiter(raw_csv_gt)
            sep_gt_n = detect_delimiter(norm_csv_gt)
            sep_llm_r = detect_delimiter(raw_csv_llm)
            sep_llm_n = detect_delimiter(norm_csv_llm)

            df_gt_r = pd.read_csv(raw_csv_gt, sep=sep_gt_r).fillna("")
            df_gt_n = pd.read_csv(norm_csv_gt, sep=sep_gt_n).fillna("")
            df_llm_r = pd.read_csv(raw_csv_llm, sep=sep_llm_r).fillna("")
            df_llm_n = pd.read_csv(norm_csv_llm, sep=sep_llm_n).fillna("")
        except Exception as e:
            print(f"Fehler beim Laden der CSV-Dateien: {e}")
            return
        
        gt_col = selected_cat
        llm_col = col_mapping.get(selected_cat)
        
        if not llm_col or gt_col not in df_gt_r.columns or llm_col not in df_llm_r.columns:
            print(f"Kategorie '{selected_cat}' ist in den DataFrames nicht verfügbar.")
            return
            
        # Extrahieren und Spalten vereinheitlichen
        df1 = df_gt_r[["image_id", gt_col]].copy().rename(columns={gt_col: "GT (Roh)"})
        df1["image_id"] = df1["image_id"].apply(normalize_image_id)
        df1["GT (Roh) parsed"] = df1["GT (Roh)"].apply(parse_cell_value)
        
        df2 = df_gt_n[["image_id", gt_col]].copy().rename(columns={gt_col: "GT (Normalisiert)"})
        df2["image_id"] = df2["image_id"].apply(normalize_image_id)
        df2["GT (Normalisiert) parsed"] = df2["GT (Normalisiert)"].apply(parse_cell_value)
        
        df3 = df_llm_r[["image_id", llm_col]].copy().rename(columns={llm_col: "LLM (Roh)"})
        df3["image_id"] = df3["image_id"].apply(normalize_image_id)
        df3["LLM (Roh) parsed"] = df3["LLM (Roh)"].apply(parse_cell_value)
        
        df4 = df_llm_n[["image_id", llm_col]].copy().rename(columns={llm_col: "LLM (Normalisiert)"})
        df4["image_id"] = df4["image_id"].apply(normalize_image_id)
        df4["LLM (Normalisiert) parsed"] = df4["LLM (Normalisiert)"].apply(parse_cell_value)
        
        # Zusammenführen der Daten
        m = pd.merge(df1, df2, on="image_id", how="inner")
        m = pd.merge(m, df3, on="image_id", how="inner")
        m = pd.merge(m, df4, on="image_id", how="inner")
        
        # Sortieren nach Bildnummer
        m["img_num"] = m["image_id"].str.extract(r"(\d+)")[0].astype(int)
        m = m.sort_values(by="img_num").drop(columns=["img_num"]).reset_index(drop=True)
        
        # Float-Scores berechnen (für den Hintergrund-Vergleich)
        m["Score (Raw) Float"] = m.apply(lambda r: get_row_score_for_cat(selected_cat, r["GT (Roh) parsed"], r["LLM (Roh) parsed"]), axis=1)
        m["Score (Bereinigt) Float"] = m.apply(lambda r: get_row_score_for_cat(selected_cat, r["GT (Normalisiert) parsed"], r["LLM (Normalisiert) parsed"]), axis=1)
        
        # Hilfsspalten entfernen
        m = m.drop(columns=["GT (Roh) parsed", "GT (Normalisiert) parsed", "LLM (Roh) parsed", "LLM (Normalisiert) parsed"])
        
        # Anzeigen-Spalten erzeugen
        is_skip = selected_cat in CATEGORY_TYPES.get("skip", [])
        
        if is_skip:
            m["Score (Raw)"] = "-"
            m["Score (Bereinigt)"] = "-"
        else:
            m["Score (Raw)"] = m["Score (Raw) Float"].apply(lambda x: f"{x:.0%}")
            
            def get_norm_display(row):
                raw = row["Score (Raw) Float"]
                norm = row["Score (Bereinigt) Float"]
                if raw > norm:
                    return f"{norm:.0%} ⚠️ (Fällt!)"
                return f"{norm:.0%}"
                
            m["Score (Bereinigt)"] = m.apply(get_norm_display, axis=1)
        
        # Nur die gewünschten Spalten für das Styler-Objekt anzeigen
        display_cols = [
            "image_id", "GT (Roh)", "LLM (Roh)", "Score (Raw)", 
            "GT (Normalisiert)", "LLM (Normalisiert)", "Score (Bereinigt)"
        ]
        
        # Row-Styling Funktion (Match = Grün, Teilweise = Orange, No-Match = Rot, Verschlechterung = Lila Highlight)
        def apply_color(row):
            img_id = row["image_id"]
            # Hole die originalen numerischen Werte aus dem DataFrame m
            row_original = m[m["image_id"] == img_id].iloc[0]
            
            if is_skip:
                # Neutrale Darstellung für Freitext/Kommentare
                base_style = "background-color: #ffffff; color: #333333; border: 1px solid #e2e8f0;"
                return [base_style] * len(row)
            
            score_raw = row_original["Score (Raw) Float"]
            score_norm = row_original["Score (Bereinigt) Float"]
            
            # Grundfarbton der Zeile basierend auf Score (Bereinigt) bestimmen
            if score_norm >= 0.999: # 100% Match -> Grün
                base_style = "background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;"
            elif score_norm > 0.001: # Teilweise Match -> Orange
                base_style = "background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba;"
            else: # Kein Match -> Rot
                base_style = "background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;"
                
            styles = [base_style] * len(row)
            
            # Highlight bei Verschlechterung
            if score_raw > score_norm:
                # Score (Raw) ist Index 3, Score (Bereinigt) ist Index 6
                styles[3] = "background-color: #ebd4f5; color: #5a189a; font-weight: bold; border: 2px solid #9d4edd;"
                styles[6] = "background-color: #ebd4f5; color: #5a189a; font-weight: bold; border: 2px solid #9d4edd;"
                
            return styles

        # Styler initialisieren und anzeigen
        styler = m[display_cols].style.apply(apply_color, axis=1)
        
        # CSS Tabellen-Styles für Jupyter
        styler = styler.set_table_styles([
            {"selector": "th", "props": [
                ("background-color", "#1d3557"), ("color", "white"),
                ("font-family", "Segoe UI, Arial, sans-serif"), ("font-size", "12px"),
                ("font-weight", "bold"), ("padding", "10px 12px"), ("border", "1px solid #d3d3d3"),
                ("text-align", "center")
            ]},
            {"selector": "td", "props": [
                ("font-family", "Segoe UI, Arial, sans-serif"), ("font-size", "11px"),
                ("padding", "8px 10px")
            ]},
            {"selector": "table", "props": [("border-collapse", "collapse"), ("width", "100%")]}
        ]).hide(axis="index")
        
        display(styler)

    # Widget UI erstellen
    dropdown = widgets.Dropdown(
        options=categories,
        value="wundrand" if "wundrand" in categories else (categories[0] if categories else None),
        description="Kategorie:",
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='300px')
    )

    output_area = widgets.Output()

    def on_change(change):
        with output_area:
            clear_output(wait=True)
            show_category_details(change['new'])

    dropdown.observe(on_change, names='value')

    display(widgets.HTML("<h3 style='font-family: Segoe UI, Arial, sans-serif; color: #1d3557; margin-top: 15px;'>GT vs. LLM Detailvergleich (Verschlechterungen markiert)</h3>"))
    display(dropdown)
    display(output_area)

    # Initiale Anzeige
    with output_area:
        show_category_details(dropdown.value)


