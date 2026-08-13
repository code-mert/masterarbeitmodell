import os
import re
import json
import pandas as pd
from pathlib import Path

# =====================================================================
# IMPORT MAPPINGS
# =====================================================================
try:
    from .mappings_LR import (
        SPELLING_MAPPING,
        WUNDTYP_GT_MAPPING,
        LOKALISATION_GT_MAPPING,
        WUNDGRUND_GT_MAPPING,
        EXSUDAT_GT_MAPPING,
        WUNDUMGEBUNG_GT_MAPPING,
        WUNDRAND_GT_MAPPING,
        PRODUKT_GT_MAPPING,
        DEBRIDEMENT_GT_MAPPING,
        LOKALISATION_KEYWORDS
    )
except ImportError:
    from mappings_LR import (
        SPELLING_MAPPING,
        WUNDTYP_GT_MAPPING,
        LOKALISATION_GT_MAPPING,
        WUNDGRUND_GT_MAPPING,
        EXSUDAT_GT_MAPPING,
        WUNDUMGEBUNG_GT_MAPPING,
        WUNDRAND_GT_MAPPING,
        PRODUKT_GT_MAPPING,
        DEBRIDEMENT_GT_MAPPING,
        LOKALISATION_KEYWORDS
    )


# =====================================================================
# TEXT CLEANING FUNCTIONS
# =====================================================================
def split_by_delimiters_outside_parentheses(text, delimiters=[','], strip=True):
    """
    Splits a string by given delimiters, but only if they are not inside parentheses
    or part of protected phrases.
    """
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

def apply_spelling_mapping(text):
    """
    Ersetzt Wörter basierend auf der Spelling-Mapping-Tabelle und behält die originale Schreibweise bei.
    """
    if not isinstance(text, str):
        return text
    for word, replacement in SPELLING_MAPPING.items():
        pattern = re.compile(rf'\b{word}\b', re.IGNORECASE)
        
        def preserve_case(match):
            matched_text = match.group(0)
            if matched_text.isupper():
                return replacement.upper()
            elif matched_text[0].isupper():
                return replacement.capitalize()
            return replacement.lower()
            
        text = pattern.sub(preserve_case, text)
    return text

def clean_whitespace(val):
    """
    Bereinigt überflüssige Leerzeichen, Zeilenumbrüche, standardisiert Pfeile,
    Dashes und wendet Spelling-Mappings an.
    """
    if not isinstance(val, str):
        return val
    
    val_stripped = val.strip()
    
    # JSON-Listen parsen und Elemente rekursiv säubern
    if val_stripped.startswith('[') and val_stripped.endswith(']'):
        try:
            lst = json.loads(val_stripped)
            if isinstance(lst, list):
                cleaned_list = [clean_whitespace(item) for item in lst]
                return json.dumps(cleaned_list, ensure_ascii=False)
        except:
            pass
            
    val_stripped = apply_spelling_mapping(val_stripped)
    val_stripped = val_stripped.replace('⁺', '+').replace('–', '-').replace('—', '-')
    val_stripped = re.sub(r'-->|->|=>|→', '->', val_stripped)
    val_stripped = re.sub(r'\r?\n', ' ', val_stripped)
    return re.sub(r'[ \t]+', ' ', val_stripped).strip()

def normalise_lokalisation(text):
    """
    Decodiert Lokalisations-Keywords in standardisierte Körperteil-Bezeichnungen.
    """
def normalise_lokalisation(text):
    """
    Normalisiert Lokalisationsangaben auf die 6 Standard-Kategorien.
    """
    return normalise_by_mapping(text, LOKALISATION_GT_MAPPING)

def normalise_by_mapping(val, mapping_dict):
    """
    Normalisiert einen Feldwert (kommagetrennt oder JSON-Liste) basierend auf einer Mapping-Tabelle.
    Prüft zuerst Kombinationen (case-insensitiv, reihenfolgeunabhängig), dann einzelne Werte.
    """
    if not isinstance(val, str):
        return val
    
    val_stripped = val.strip()
    is_json = False
    
    if val_stripped.startswith('[') and val_stripped.endswith(']'):
        try:
            items = json.loads(val_stripped)
            if isinstance(items, list):
                is_json = True
            else:
                items = [val_stripped]
        except:
            items = split_by_delimiters_outside_parentheses(val_stripped)
    else:
        items = split_by_delimiters_outside_parentheses(val_stripped)
        
    # Clean whitespace and spelling for each parsed item
    items = [clean_whitespace(item) for item in items if item]
    
    # Helper to flat-split items by commas (so "a, b" becomes ["a", "b"])
    def flatten_items(lst):
        flat = []
        for x in lst:
            flat.extend([clean_whitespace(p) for p in split_by_delimiters_outside_parentheses(x)])
        return flat

    if is_json:
        items_flat = items
    else:
        items_flat = flatten_items(items)
    
    # Check if the entire group of items matches a key in mapping_dict (case-insensitive, order-independent)
    for k, v in mapping_dict.items():
        cleaned_key = clean_whitespace(k)
        key_items = [clean_whitespace(x) for x in split_by_delimiters_outside_parentheses(cleaned_key)]
        if {x.lower() for x in items_flat} == {x.lower() for x in key_items}:
            v_flat = flatten_items(v)
            if is_json:
                return json.dumps(v_flat, ensure_ascii=False)
            else:
                return ", ".join(v_flat)
                
    mapped_items = []
    for item in items_flat:
        matched = False
        for k, v in mapping_dict.items():
            cleaned_key = clean_whitespace(k)
            key_items = [clean_whitespace(x) for x in split_by_delimiters_outside_parentheses(cleaned_key)]
            if item.lower() == cleaned_key.lower():
                mapped_items.extend(flatten_items(v))
                matched = True
                break
            # Only match single items here to avoid partial match with multi-item keys
            elif len(key_items) == 1:
                if item.lower() == key_items[0].lower():
                    mapped_items.extend(flatten_items(v))
                    matched = True
                    break
        if not matched:
            if item and item not in ["nan", "—", ""]:
                mapped_items.append(item)
                
    if not is_json:
        mapped_items = flatten_items(mapped_items)
    mapped_items = sorted(list(set(mapped_items)))
    
    if is_json:
        return json.dumps(mapped_items, ensure_ascii=False)
    else:
        return ", ".join(mapped_items)


# =====================================================================
# COLUMN SPECIFIC NORMALIZATION FUNCTIONS
# =====================================================================
def normalise_wundumgebung(val):
    return normalise_by_mapping(val, WUNDUMGEBUNG_GT_MAPPING)

def normalise_wundrand(val):
    return normalise_by_mapping(val, WUNDRAND_GT_MAPPING)

def normalise_exsudat(val):
    return normalise_by_mapping(val, EXSUDAT_GT_MAPPING)

def normalise_wundgrund(val):
    # Immer als JSON-Liste ausgeben für F1-Score (Set-basierte Auswertung)
    if pd.isna(val) or val is None or str(val).strip() in ["", "nan", "—", "— (leer)"]:
        return "[]"
    items = normalise_by_mapping(val, WUNDGRUND_GT_MAPPING)
    if not isinstance(items, str):
        return "[]"
    if not (items.startswith('[') and items.endswith(']')):
        item_list = [x.strip() for x in split_by_delimiters_outside_parentheses(items) if isinstance(x, str) and x.strip()]
        return json.dumps(item_list, ensure_ascii=False)
    return items

def normalise_produkt(val):
    return normalise_by_mapping(val, PRODUKT_GT_MAPPING)

def normalise_debridement(val):
    return normalise_by_mapping(val, DEBRIDEMENT_GT_MAPPING)

def normalise_wundtyp(val):
    """
    Normalisiert Wundtypen auf die 10 medizinischen Hauptkategorien.
    """
    return normalise_by_mapping(val, WUNDTYP_GT_MAPPING)


# =====================================================================
# GT FILE NORMALIZATION (Semicolon Delimiter)
# =====================================================================
def clean_ground_truth(input_path: str, output_path: str):
    """
    Führt die Normalisierung auf die Lohmann Rauscher GT CSV-Datei aus und speichert sie am Zielort.
    """
    input_file = Path(input_path)
    output_file = Path(output_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"Eingabedatei existiert nicht: {input_path}")
        
    # Semicolon separator
    df = pd.read_csv(input_file, sep=";")
    df_cleaned = df.copy()
    
    for col in df_cleaned.columns:
        if col in ['image_id', 'user_id', 'updated_at', 'ist_fertig', 'id']:
            continue
        df_cleaned[col] = df_cleaned[col].apply(clean_whitespace)
        
    if 'lokalisation' in df_cleaned.columns:
        df_cleaned['lokalisation'] = df_cleaned['lokalisation'].apply(normalise_lokalisation)
        
    if 'wundtyp' in df_cleaned.columns:
        df_cleaned['wundtyp'] = df_cleaned['wundtyp'].apply(normalise_wundtyp)
        
    if 'wundumgebung' in df_cleaned.columns:
        df_cleaned['wundumgebung'] = df_cleaned['wundumgebung'].apply(normalise_wundumgebung)
        
    if 'wundrand' in df_cleaned.columns:
        df_cleaned['wundrand'] = df_cleaned['wundrand'].apply(normalise_wundrand)
        
    if 'wundgrund' in df_cleaned.columns:
        df_cleaned['wundgrund'] = df_cleaned['wundgrund'].apply(normalise_wundgrund)
        
    if 'exsudat' in df_cleaned.columns:
        df_cleaned['exsudat'] = df_cleaned['exsudat'].apply(normalise_exsudat)
        
    if 'praeferenz_produkt' in df_cleaned.columns:
        df_cleaned['praeferenz_produkt'] = df_cleaned['praeferenz_produkt'].apply(normalise_produkt)
        
    if 'alternative_produkt' in df_cleaned.columns:
        df_cleaned['alternative_produkt'] = df_cleaned['alternative_produkt'].apply(normalise_produkt)
        
    if 'ergaenzende_produkte_praeferenz' in df_cleaned.columns:
        df_cleaned['ergaenzende_produkte_praeferenz'] = df_cleaned['ergaenzende_produkte_praeferenz'].apply(normalise_produkt)
        
    if 'ergaenzende_produkte_alternativ' in df_cleaned.columns:
        df_cleaned['ergaenzende_produkte_alternativ'] = df_cleaned['ergaenzende_produkte_alternativ'].apply(normalise_produkt)
        
    if 'debridement' in df_cleaned.columns:
        df_cleaned['debridement'] = df_cleaned['debridement'].apply(normalise_debridement)
        
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df_cleaned.to_csv(output_file, sep=";", index=False)
    print(f"Normalisierte Datei erfolgreich erstellt: {output_path}")

# Alias für Kompatibilität
normalize_gt_file = clean_ground_truth


# =====================================================================
# LLM FILE NORMALIZATION
# =====================================================================

def _safe_parse_list(val):
    """
    Parst einen String sicher als Liste, falls dieser mit eckigen Klammern umschlossen ist.
    """
    import ast
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
    return val


def merge_wundtyp_sonstiges(wundtyp_val, sonstiges_val):
    """
    Hilfsfunktion, die 'Sonstiges' aus wundtyp entfernt und durch den 
    konkreten sonstigen Wundtyp ersetzt, falls dieser vorhanden ist.
    Unterstützt sowohl Strings als auch Listen.
    """
    if wundtyp_val is None:
        return wundtyp_val
    if hasattr(wundtyp_val, "__len__") and not isinstance(wundtyp_val, (str, dict)):
        if len(wundtyp_val) == 0:
            return wundtyp_val
    else:
        # Check for single values
        try:
            if not wundtyp_val or pd.isna(wundtyp_val):
                return wundtyp_val
        except ValueError:
            # Fallback if somehow an ambiguous comparison happens
            if pd.isna(wundtyp_val).any():
                return wundtyp_val
        
    sonst_str = str(sonstiges_val).strip() if pd.notna(sonstiges_val) else ""
    if sonst_str.lower() in ["nan", "—", ""]:
        sonst_str = ""
        
    is_list = isinstance(wundtyp_val, list)
    if not is_list and isinstance(wundtyp_val, str):
        val_stripped = wundtyp_val.strip()
        if val_stripped.startswith('[') and val_stripped.endswith(']'):
            try:
                import ast
                parsed = ast.literal_eval(val_stripped)
                if isinstance(parsed, (list, tuple, set)):
                    wundtyp_val = list(parsed)
                    is_list = True
            except:
                pass
        if not is_list:
            wundtyp_val = split_by_delimiters_outside_parentheses(val_stripped)
            is_list = True

    if is_list:
        new_list = []
        for x in wundtyp_val:
            x_str = str(x).strip()
            if x_str.lower() == "sonstiges":
                if sonst_str:
                    new_list.append(sonst_str)
                else:
                    new_list.append(x_str)
            else:
                new_list.append(x_str)
        import json
        return json.dumps(new_list, ensure_ascii=False)
    
    wund_str = str(wundtyp_val).strip()
    if wund_str.lower() == "sonstiges":
        return sonst_str if sonst_str else wund_str
    return wund_str


def normalize_llm_file(input_path: str, output_path: str):
    """
    Führt die Normalisierung auf die rohe LLM CSV-Datei aus (speziell für Lohmann Rauscher) und speichert sie am Zielort.
    """
    print("--- RUNNING LR SPECIFIC NORMALIZATION ---")
    input_file = Path(input_path)
    output_file = Path(output_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"Eingabedatei existiert nicht: {input_path}")
        
    df = pd.read_csv(input_file)
    df_cleaned = df.copy()
    
    # Merge wundtyp and wundtyp_sonstiges
    if 'wundtyp' in df_cleaned.columns and 'wundtyp_sonstiges' in df_cleaned.columns:
        df_cleaned['wundtyp'] = df_cleaned.apply(
            lambda r: merge_wundtyp_sonstiges(r['wundtyp'], r['wundtyp_sonstiges']),
            axis=1
        )
        
    for col in df_cleaned.columns:
        if col == 'image_id':
            continue
            
        def clean_field(val):
            if pd.isna(val):
                return ""
            parsed_val = _safe_parse_list(val)
            if isinstance(parsed_val, list):
                # Bereinige jedes Element der Liste
                cleaned_lst = [clean_whitespace(x) for x in parsed_val if x is not None]
                return json.dumps(cleaned_lst, ensure_ascii=False)
            else:
                return clean_whitespace(parsed_val)
                
        df_cleaned[col] = df_cleaned[col].apply(clean_field)
        
    if 'lokalisation' in df_cleaned.columns:
        df_cleaned['lokalisation'] = df_cleaned['lokalisation'].apply(normalise_lokalisation)
        
    if 'wundtyp' in df_cleaned.columns:
        df_cleaned['wundtyp'] = df_cleaned['wundtyp'].apply(normalise_wundtyp)
        
    if 'wundumgebung' in df_cleaned.columns:
        df_cleaned['wundumgebung'] = df_cleaned['wundumgebung'].apply(normalise_wundumgebung)
        
    if 'wundrand' in df_cleaned.columns:
        df_cleaned['wundrand'] = df_cleaned['wundrand'].apply(normalise_wundrand)
        
    if 'wundgrund' in df_cleaned.columns:
        df_cleaned['wundgrund'] = df_cleaned['wundgrund'].apply(normalise_wundgrund)
        
    if 'exsudat' in df_cleaned.columns:
        df_cleaned['exsudat'] = df_cleaned['exsudat'].apply(normalise_exsudat)
        
    if 'exsudat_menge' in df_cleaned.columns:
        df_cleaned['exsudat_menge'] = df_cleaned['exsudat_menge'].apply(normalise_exsudat)
        
    if 'praeferenz_wundauflage' in df_cleaned.columns:
        df_cleaned['praeferenz_wundauflage'] = df_cleaned['praeferenz_wundauflage'].apply(normalise_produkt)
        
    if 'alternativ_wundauflage' in df_cleaned.columns:
        df_cleaned['alternativ_wundauflage'] = df_cleaned['alternativ_wundauflage'].apply(normalise_produkt)
        
    if 'praeferenz_ergaenzung' in df_cleaned.columns:
        df_cleaned['praeferenz_ergaenzung'] = df_cleaned['praeferenz_ergaenzung'].apply(normalise_produkt)
        
    if 'alternativ_ergaenzung' in df_cleaned.columns:
        df_cleaned['alternativ_ergaenzung'] = df_cleaned['alternativ_ergaenzung'].apply(normalise_produkt)
        
    if 'debridement_methode' in df_cleaned.columns:
        df_cleaned['debridement_methode'] = df_cleaned['debridement_methode'].apply(normalise_debridement)
        
    if 'debridement' in df_cleaned.columns:
        df_cleaned['debridement'] = df_cleaned['debridement'].apply(normalise_debridement)
        
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df_cleaned.to_csv(output_file, index=False)
    print(f"Normalisierte LLM-Datei erfolgreich erstellt: {output_path}")

