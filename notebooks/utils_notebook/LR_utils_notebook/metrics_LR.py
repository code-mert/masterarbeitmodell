import os
import sys
import ast
import re

# Pfad anpassen, um utils_notebook und das eval-Modul zu importieren
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils_notebook import metrics, clean

def format_val(val):
    """Formatierungshilfe für Zelleninhalte."""
    if val is None or (isinstance(val, str) and val.strip() in ["", "nan", "—"]):
        return "—"
    if isinstance(val, list):
        return ", ".join(str(x) for x in val)
    return str(val)

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

def get_score(category, val_gt, val_llm, raw_flag=True):
    """Berechnet den Score passend zum Kategorie-Typ."""
    # Normalisieren, um Schreibweisen (Umlaute, Akzente, Bindestriche, etc.) robust zu vergleichen
    cat_clean = category.lower().replace("é", "e").replace("ä", "a").replace("ü", "u").replace("-", " ").strip()
    
    if cat_clean == "exsudat":
        score, _ = metrics.score_ordinal(category.lower(), val_gt, val_llm)
        return score
    elif cat_clean in [
        "wundstadium", 
        "wundrand", 
        "wundumgebung", 
        "wundgrund",
        "debridement methode", 
        "kompression produkte", 
        "kompression produkt", 
        "kompression product"
    ]:
        f1, _ = metrics.evaluate_checklist(val_gt, val_llm)
        return f1
    elif cat_clean in ["auffalligkeiten", "einschrankungen/annahmen", "einschrankungen annahmen"]:
        return None
    else: # exact match (inkl. Wundtyp, Infektion, Lokalisation, etc.)
        return metrics.score_exact(val_gt, val_llm)

