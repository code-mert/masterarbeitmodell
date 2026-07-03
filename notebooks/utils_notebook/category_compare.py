import os
import sys
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, HTML

# Ensure parent directory (project root) is in the path to allow loading eval module
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from eval.loaders import load_ground_truth, load_llm_outputs, matched_image_ids

def compare_categories_interactive(csv_path: str, json_dir: str):
    """
    Sets up an interactive widget with a dropdown to select a category
    and compare Ground Truth and LLM outputs for all matched wounds side-by-side.
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

    print(f"Erfolgreich {len(matched_ids)} Wundbilder zum Kategorievergleich geladen.")

    # Mapping of categories between GT (CSV) and LLM (JSON)
    CATEGORIES = {
        "Wundtyp": {"gt_key": "wundtyp", "llm_key": "wundtyp"},
        "Spezifizierung": {"gt_key": "wundtyp_spec", "llm_key": "wundtyp_spezifizierung"},
        "Lokalisation": {"gt_key": "lokalisation", "llm_key": "lokalisation"},
        "Wundstadium / -phase": {"gt_key": "wundstadium", "llm_key": "wundphase"},
        "Exsudat-Menge": {"gt_key": "exsudat", "llm_key": "exsudat_menge"},
        "Infektionsstatus": {"gt_key": "infektion", "llm_key": "infektionsstatus"},
        "Wundrand": {"gt_key": "wundrand", "llm_key": "wundrand"},
        "Wundumgebung": {"gt_key": "wundumgebung", "llm_key": "wundumgebung"},
        "Weitere Auffälligkeiten": {"gt_key": "auffaelligkeiten", "llm_key": "weitere_auffaelligkeiten"},
        "Débridement notwendig?": {"gt_key": "debridement_notwendig", "llm_key": "debridement_notwendig"},
        "Débridement-Methode": {"gt_key": "debridement", "llm_key": "debridement_methode"},
        "Spüllösung": {"gt_key": "spuelloesung", "llm_key": "spuelloesung"},
        "1. Primärverband (Präferenz & Alternative)": {"special": "primaerverband"},
        "Antimikrobieller Verband?": {"gt_key": "antimikrobiell_notwendig", "llm_key": "antimikrobieller_verband"},
        "Antimikrobielles Agens": {"gt_key": "antimikrobielles_agens", "llm_key": "antimikrobielles_agens"},
        "4. Sekundärverband / Fixierung": {"gt_key": "sekundaerverband", "llm_key": "sekundaerverband_fixierung"},
        "5. Hautschutz": {"gt_key": "hautschutz", "llm_key": "wundrand_hautschutz"},
        "Kompression indiziert?": {"gt_key": "kompression_indiziert", "llm_key": "kompression_indiziert"},
        "Kompression (Art/Produkte)": {"gt_key": "kompression_produkte", "llm_key": "kompression_art"},
        "Einschränkungen / Annahmen": {"gt_key": "einschraenkungen", "llm_key": "einschraenkungen_annahmen"},
    }

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

    # Define the comparison display function
    def zeige_kategorie_vergleich(Kategorie):
        if not Kategorie:
            print("Keine Kategorie ausgewählt.")
            return

        cfg = CATEGORIES[Kategorie]
        rows = []
        
        for img_id in matched_ids:
            gt_rec = gt_data[img_id]
            llm_rec = llm_data[img_id]

            if "special" in cfg and cfg["special"] == "primaerverband":
                gt_val = f"Präferenz: {format_val(gt_rec.get('praeferenz_product', gt_rec.get('praeferenz_produkt')))} | Alternative: {format_val(gt_rec.get('alternative_product', gt_rec.get('alternative_produkt')))}"
                llm_val = f"Präferenz: {format_val(llm_rec.get('praeferenz_verbandklasse'))} | Alternative: {format_val(llm_rec.get('alternativ_verbandklasse'))}"
            else:
                gt_k = cfg["gt_key"]
                llm_k = cfg["llm_key"]
                
                # Check for alternative key names in gt
                if gt_k == "wundtyp_spec" and "wundtyp_spezifikation" in gt_rec:
                    gt_k = "wundtyp_spezifikation"
                
                gt_val = format_val(gt_rec.get(gt_k))
                
                # Resolve wundtyp "Sonstiges" for LLM output
                if Kategorie == "Wundtyp":
                    resolved_llm_wundtyp = get_resolved_wundtyp(llm_rec)
                    llm_val = format_val(resolved_llm_wundtyp)
                else:
                    llm_val = format_val(llm_rec.get(llm_k))

            rows.append({
                "Wund-ID": img_id,
                "Ground Truth (GT)": gt_val,
                "LLM Output": llm_val
            })

        df_compare = pd.DataFrame(rows)

        # Natural (numeric) sort of Wund-IDs (wunde_01, wunde_02, ...)
        if not df_compare.empty:
            df_compare = df_compare.sort_values(
                by='Wund-ID',
                key=lambda x: x.str.extract(r'(\d+)')[0].astype(float)
            ).reset_index(drop=True)

        # Style table
        def values_match(val1, val2):
            import re
            def to_set(v):
                if v is None:
                    return set()
                v_str = str(v).strip().lower()
                if v_str in ["—", "— (leer)", "nan", ""]:
                    return set()
                parts = [x.strip() for x in re.split(r'[,|]', v_str) if x.strip()]
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
                ("font-size", "11px"),
                ("font-weight", "bold"),
                ("padding", "8px 10px"),
                ("border", "1px solid #d3d3d3")
            ]},
            {"selector": "td", "props": [
                ("font-family", "Segoe UI, Arial, sans-serif"),
                ("font-size", "11px"),
                ("padding", "8px 10px"),
                ("border", "1px solid #e0e0e0"),
                ("text-align", "left")
            ]},
            {"selector": "table", "props": [
                ("border-collapse", "collapse"),
                ("width", "100%")
            ]}
        ]).hide(axis="index")

        display(HTML(f"<h3 style='font-family: Segoe UI, Arial, sans-serif; color: #1d3557; margin-top: 20px;'>Vergleich aller Wunden für Kategorie: {Kategorie}</h3>"))
        display(styled_compare)

    # 5. Dropdown widget setup
    category_select = widgets.Dropdown(
        options=list(CATEGORIES.keys()),
        value="Wundtyp",
        description="Kategorie:",
        style={'description_width': 'initial'},
        disabled=False,
    )

    display(widgets.interactive(zeige_kategorie_vergleich, Kategorie=category_select))
