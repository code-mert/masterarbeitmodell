import os
import sys
import pandas as pd
import ipywidgets as widgets
from IPython.display import display

# Ensure parent directory is in system path to allow importing eval module
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from eval.loaders import load_llm_outputs, load_ground_truth
def clean_display_value(val):
    """
    Formatierungshilfe: Wandelt Listen oder JSON-Listen in saubere, 
    kommagetrennte Strings ohne eckige Klammern und Anführungszeichen um.
    """
    if val is None:
        return "— (leer)"
    if hasattr(val, "__len__") and not isinstance(val, (str, dict)):
        if len(val) == 0:
            return "— (leer)"
        return ", ".join(str(x) for x in val if x)
    else:
        try:
            if not val or pd.isna(val):
                return "— (leer)"
        except ValueError:
            if pd.isna(val).any():
                return "— (leer)"
        
    if isinstance(val, str):
        val_stripped = val.strip()
        if val_stripped.startswith('[') and val_stripped.endswith(']'):
            try:
                import ast
                parsed = ast.literal_eval(val_stripped)
                if isinstance(parsed, (list, tuple, set)):
                    if not parsed:
                        return "— (leer)"
                    return ", ".join(str(x) for x in parsed if x)
            except:
                pass
        if val_stripped in ["", "nan", "—"]:
            return "— (leer)"
        return val_stripped
        
    return str(val)

def load_llm_dataframe(path: str) -> pd.DataFrame:
    """
    Loads LLM outputs from a CSV file or a directory of JSON files and returns them 
    as a pandas DataFrame sorted naturally by image_id.
    """
    llm_data = load_llm_outputs(path)
    records = []
    for image_id, parsed in llm_data.items():
        row = {"image_id": image_id}
        row.update(parsed)
        records.append(row)
        
    df = pd.DataFrame(records)
    if not df.empty and "image_id" in df.columns:
        df = df.sort_values(
            by="image_id",
            key=lambda x: x.str.extract(r"(\d+)")[0].astype(float) if x.str.contains(r"\d+").any() else x
        ).reset_index(drop=True)
    return df

def load_gt_dataframe(path: str) -> pd.DataFrame:
    """
    Loads Ground Truth records from a CSV file and returns them 
    as a pandas DataFrame sorted naturally by image_id.
    """
    gt_data = load_ground_truth(path)
    records = []
    for image_id, parsed in gt_data.items():
        row = {"image_id": image_id}
        row.update(parsed)
        records.append(row)
        
    df = pd.DataFrame(records)
    if not df.empty and "image_id" in df.columns:
        df = df.sort_values(
            by="image_id",
            key=lambda x: x.str.extract(r"(\d+)")[0].astype(float) if x.str.contains(r"\d+").any() else x
        ).reset_index(drop=True)
    return df

def explore_answers_interactive(df: pd.DataFrame, label: str = "Kategorie"):
    """
    Displays an interactive dropdown widget to list all wound answers for a selected category.
    """
    if df.empty:
        print("Das DataFrame ist leer.")
        return
        
    categories = sorted([col for col in df.columns if col not in ['image_id', 'user_id', 'updated_at', 'ist_fertig']])
    
    def show_answers(selected_category):
        if not selected_category:
            print("Keine Kategorie ausgewählt.")
            return
            
        if selected_category in df.columns:
            print(f"Antworten für Kategorie '{selected_category}' nach Wundnummer:\n")
            for _, row in df.iterrows():
                img_id = row['image_id']
                val = row[selected_category]
                
                # Check for Sonstiges and append corresponding sonstige text
                if selected_category == 'wundtyp' and 'wundtyp_sonstiges' in df.columns:
                    sonst = row['wundtyp_sonstiges']
                    if pd.notna(sonst) and str(sonst).strip() != "":
                        if isinstance(val, list):
                            val = [f"Sonstiges ({sonst})" if str(x).strip().lower() == "sonstiges" else x for x in val]
                        elif isinstance(val, str):
                            if val.strip().lower() == "sonstiges":
                                val = f"Sonstiges ({sonst})"
                                
                elif selected_category == 'wundstadium' and 'wundstadium_sonstiges' in df.columns:
                    sonst = row['wundstadium_sonstiges']
                    if pd.notna(sonst) and str(sonst).strip() != "":
                        if isinstance(val, list):
                            val = [f"Sonstiges ({sonst})" if str(x).strip().lower() == "sonstiges" else x for x in val]
                        elif isinstance(val, str):
                            if val.strip().lower() == "sonstiges":
                                val = f"Sonstiges ({sonst})"
                
                val_str = clean_display_value(val)
                print(f"{img_id}: {val_str}")
        else:
            print(f"Die Kategorie '{selected_category}' existiert nicht im Datensatz.")

    category_select = widgets.Dropdown(
        options=categories,
        value='wundtyp' if 'wundtyp' in categories else (categories[0] if categories else None),
        description=f'{label}:',
        style={'description_width': 'initial'},
        disabled=False,
    )

    return widgets.interactive(show_answers, selected_category=category_select)

def explore_distributions_interactive(df: pd.DataFrame, df_norm: pd.DataFrame = None, label: str = "Kategorie"):
    """
    Displays an interactive dropdown widget to show the frequency distribution of answers for a selected category.
    If df_norm is provided, displays raw and normalized distributions side-by-side.
    """
    from IPython.display import display, HTML
    
    # Handle positional arguments if label was passed as second argument
    if isinstance(df_norm, str):
        label = df_norm
        df_norm = None
        
    if df.empty:
        print("Das DataFrame ist leer.")
        return
        
    categories = sorted([col for col in df.columns if col not in ['image_id', 'user_id', 'updated_at', 'ist_fertig']])
    
    def show_distribution(selected_category):
        if not selected_category:
            print("Keine Kategorie ausgewählt.")
            return
            
        def get_counts_for_df(target_df):
            if selected_category not in target_df.columns:
                return None, 0, 0
            series = target_df[selected_category].dropna()
            
            # Process Sonstiges to include detailed text
            if selected_category == 'wundtyp' and 'wundtyp_sonstiges' in target_df.columns:
                def process_wundtyp(row):
                    val = row['wundtyp']
                    sonst = row['wundtyp_sonstiges']
                    if pd.isna(val):
                        return val
                    if pd.notna(sonst) and str(sonst).strip() != "":
                        if isinstance(val, list):
                            return [f"Sonstiges ({sonst})" if str(x).strip().lower() == "sonstiges" else x for x in val]
                        elif isinstance(val, str) and val.strip().lower() == "sonstiges":
                            return f"Sonstiges ({sonst})"
                    return val
                series = target_df.apply(process_wundtyp, axis=1).dropna()
                
            elif selected_category == 'wundstadium' and 'wundstadium_sonstiges' in target_df.columns:
                def process_wundstadium(row):
                    val = row['wundstadium']
                    sonst = row['wundstadium_sonstiges']
                    if pd.isna(val):
                        return val
                    if pd.notna(sonst) and str(sonst).strip() != "":
                        if isinstance(val, list):
                            return [f"Sonstiges ({sonst})" if str(x).strip().lower() == "sonstiges" else x for x in val]
                        elif isinstance(val, str) and val.strip().lower() == "sonstiges":
                            return f"Sonstiges ({sonst})"
                    return val
                series = target_df.apply(process_wundstadium, axis=1).dropna()
                
            series_display = series.apply(clean_display_value)
            total = series_display.count()
            counts = series_display.value_counts()
            return counts, total, len(counts)

        # Get counts for raw
        counts_raw, total_raw, unique_raw = get_counts_for_df(df)
        
        # If df_norm is provided, get counts for norm
        if df_norm is not None:
            counts_norm, total_norm, unique_norm = get_counts_for_df(df_norm)
            
            if counts_raw is None or counts_norm is None:
                print(f"Die Kategorie '{selected_category}' existiert nicht in beiden Datensätzen.")
                return
                
            df_raw_counts = pd.DataFrame({"Antwort": counts_raw.index, "Anzahl": counts_raw.values})
            df_norm_counts = pd.DataFrame({"Antwort": counts_norm.index, "Anzahl": counts_norm.values})
            
            reduction = (1.0 - unique_norm / unique_raw) * 100.0 if unique_raw > 0 else 0.0
            
            style = """
            <style>
                .explore-table {
                    border-collapse: collapse;
                    width: 100%;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    font-size: 12px;
                    margin-top: 10px;
                }
                .explore-table th {
                    background-color: #1d3557;
                    color: white;
                    padding: 8px 10px;
                    text-align: left;
                    border: 1px solid #d3d3d3;
                    font-weight: bold;
                }
                .explore-table td {
                    padding: 6px 10px;
                    border: 1px solid #e0e0e0;
                }
                .explore-table tr:nth-child(even) {
                    background-color: #f8f9fa;
                }
            </style>
            """
            
            html_raw = f"""
            <div style="float: left; width: 48%; margin-right: 4%;">
                <h3 style="color: #1d3557; font-family: 'Segoe UI', Arial, sans-serif; margin-bottom: 5px;">Roh-Version (Raw GT)</h3>
                <p style="margin: 0; font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; color: #457b9d;">
                    <b>{unique_raw}</b> unterschiedliche Antworten / {total_raw} Einträge
                </p>
                {df_raw_counts.to_html(index=False, classes='explore-table')}
            </div>
            """
            
            html_norm = f"""
            <div style="float: left; width: 48%;">
                <h3 style="color: #2a9d8f; font-family: 'Segoe UI', Arial, sans-serif; margin-bottom: 5px;">Normalisiert (Normalised GT)</h3>
                <p style="margin: 0; font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; color: #2a9d8f;">
                    <b>{unique_norm}</b> unterschiedliche Antworten / {total_norm} Einträge (<b>-{reduction:.1f}%</b> Reduktion)
                </p>
                {df_norm_counts.to_html(index=False, classes='explore-table')}
            </div>
            """
            
            display(HTML(f'{style}<div style="width: 100%; overflow: hidden; margin-top: 15px;">{html_raw}{html_norm}</div>'))
            
        else:
            # Original single DataFrame printout
            if counts_raw is None:
                print(f"Die Kategorie '{selected_category}' existiert nicht im Datensatz.")
                return
            print(f"Häufigkeitsverteilung für Kategorie '{selected_category}':")
            print(f"-> {unique_raw} unterschiedliche Antworten aus insgesamt {total_raw} Einträgen:\n")
            for antwort, anzahl in counts_raw.items():
                antwort_display = clean_display_value(antwort)
                print(f"- {antwort_display}: {anzahl}x")

    category_select = widgets.Dropdown(
        options=categories,
        value='wundtyp' if 'wundtyp' in categories else (categories[0] if categories else None),
        description=f'{label}:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='300px'),
        disabled=False,
    )

    return widgets.interactive(show_distribution, selected_category=category_select)

# Backward compatibility aliases
explore_llm_answers_interactive = explore_answers_interactive
explore_llm_distributions_interactive = explore_distributions_interactive

def convert_llm_jsons_to_raw_csv(json_dir: str, output_csv_path: str):
    """
    Crawls raw JSON output files and compiles them into a single sorted raw CSV file on disk.
    """
    from pathlib import Path
    llm_data = load_llm_outputs(json_dir)
    if not llm_data:
        print(f"Keine LLM-Outputs im Ordner {json_dir} gefunden.")
        return
        
    records = []
    for image_id, parsed_output in llm_data.items():
        row = {"image_id": image_id}
        row.update(parsed_output)
        records.append(row)
        
    df = pd.DataFrame(records)
    # Sort naturally by image_id
    if not df.empty and "image_id" in df.columns:
        df = df.sort_values(
            by="image_id",
            key=lambda x: x.str.extract(r"(\d+)")[0].astype(float) if x.str.contains(r"\d+").any() else x
        ).reset_index(drop=True)
        
    output_file = Path(output_csv_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"Rohe LLM-Tabelle erfolgreich erstellt: {output_csv_path}")


def compare_gt_interactive(df_raw: pd.DataFrame, df_norm: pd.DataFrame):
    """
    Sets up an interactive widget with a dropdown to select a wound and compare
    raw Ground Truth and normalized Ground Truth side-by-side.
    """
    if df_raw.empty or df_norm.empty:
        print("Eines der DataFrames ist leer.")
        return

    # Get intersection of image_ids, preserving the order of df_raw
    raw_ids = df_raw['image_id'].dropna().unique().tolist()
    norm_ids = set(df_norm['image_id'].dropna().unique())
    matched_ids = [img_id for img_id in raw_ids if img_id in norm_ids]

    if not matched_ids:
        print("Keine gemeinsamen Wundbilder (image_ids) gefunden.")
        return

    from IPython.display import HTML

    # Columns to compare
    exclude_cols = {'image_id', 'user_id', 'updated_at', 'ist_fertig'}
    all_cols = sorted(list(set(df_raw.columns).union(set(df_norm.columns)) - exclude_cols))

    def compare_single(image_id):
        if not image_id:
            print("Kein Wundbild ausgewählt.")
            return

        row_raw = df_raw[df_raw['image_id'] == image_id]
        row_norm = df_norm[df_norm['image_id'] == image_id]

        if row_raw.empty or row_norm.empty:
            print(f"Fehler: Daten für {image_id} konnten nicht in beiden DataFrames gefunden werden.")
            return

        row_raw = row_raw.iloc[0]
        row_norm = row_norm.iloc[0]

        comparison_rows = []
        for col in all_cols:
            val_raw = row_raw.get(col, None)
            val_norm = row_norm.get(col, None)

            comparison_rows.append({
                "Kategorie": col,
                "Rohe GT": clean_display_value(val_raw),
                "Normalisierte GT": clean_display_value(val_norm)
            })

        df_compare = pd.DataFrame(comparison_rows)

        def style_rows(row):
            raw_val = row["Rohe GT"]
            norm_val = row["Normalisierte GT"]
            if str(raw_val).strip() == str(norm_val).strip():
                return ["", "", ""]
            else:
                color = "#fff3e0"      # soft orange
                text_color = "#e65100" # darker orange
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

        display(HTML(f"<h3 style='font-family: Segoe UI, Arial, sans-serif; color: #1d3557; margin-top: 20px;'>Vergleich der Ground Truth für Bild-ID: {image_id}</h3>"))
        display(styled_compare)

    wunde_select = widgets.Dropdown(
        options=matched_ids,
        value=matched_ids[0] if matched_ids else None,
        description='Wundbild:',
        style={'description_width': 'initial'},
        disabled=False,
    )

    return widgets.interactive(compare_single, image_id=wunde_select)


