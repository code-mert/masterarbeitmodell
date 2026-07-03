from typing import Dict, Any, List

# Central list of prefixes/values for empty set detection.
# Any value starting with these prefixes is considered an empty-set marker and is filtered out.
EMPTY_MARKERS: List[str] = [
    "Nicht erforderlich",
    "Kein Débridement erforderlich",
]

def filter_markers(lst: List[Any]) -> List[Any]:
    """
    Filters out any element from the list that starts with or matches any of the EMPTY_MARKERS.
    Keeps values in their original form (no lower, strip, or NFKC on the returned elements).
    """
    if not lst:
        return []
    
    filtered = []
    for item in lst:
        item_str = str(item).strip()
        is_marker = False
        for marker in EMPTY_MARKERS:
            if item_str.startswith(marker):
                is_marker = True
                break
        if not is_marker:
            filtered.append(item)
            
    return filtered

def unpack_value(val: Any) -> str:
    """
    Brings categorical fields to a unified string format.
    Unpacks single-element lists to a string. Keeps other types as string.
    Returns an empty string for None or empty lists.
    """
    if val is None:
        return ""
    if isinstance(val, list):
        if len(val) > 0:
            return str(val[0])
        return ""
    return str(val)

def align(gt_record: Dict[str, Any], llm_record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Aligns a Ground Truth record and an LLM record structurally into a unified format.
    Ensures that empty sets are normalized and categorical fields are unpacked.
    No content normalization (like lowercase/strip/NFKC) is performed on the raw lists/values.
    
    Args:
        gt_record: Dictionary of a ground truth image record.
        llm_record: Dictionary of an LLM parsed_output record.
        
    Returns:
        A dictionary containing the aligned evaluation levels and categorical fields.
    """
    return {
        # 6 Evaluationsebenen (pro Ebene das Paar/die Paare)
        "primaerverband": {
            "llm_praef": filter_markers(llm_record.get("praeferenz_verbandklasse") or []),
            "llm_alt": filter_markers(llm_record.get("alternativ_verbandklasse") or []),
            "gt_praef": filter_markers(gt_record.get("praeferenz_produkt") or []),
            "gt_alt": filter_markers(gt_record.get("alternative_produkt") or [])
        },
        "debridement": {
            "llm": filter_markers(llm_record.get("debridement_methode") or []),
            "gt": filter_markers(gt_record.get("debridement") or [])
        },
        "antimikrobielles_agens": {
            "llm": filter_markers(llm_record.get("antimikrobielles_agens") or []),
            "gt": filter_markers(gt_record.get("antimikrobielles_agens") or [])
        },
        "sekundaerverband": {
            "llm": filter_markers(llm_record.get("sekundaerverband_fixierung") or []),
            "gt": filter_markers(gt_record.get("sekundaerverband") or [])
        },
        "hautschutz": {
            "llm": filter_markers(llm_record.get("wundrand_hautschutz") or []),
            "gt": filter_markers(gt_record.get("hautschutz") or [])
        },
        "kompression": {
            "llm": filter_markers(llm_record.get("kompression_art") or []),
            "gt": filter_markers(gt_record.get("kompression_produkte") or [])
        },
        
        # Angeglichene kategoriale Felder
        "kategorial": {
            "wundtyp": {
                "llm": unpack_value(llm_record.get("wundtyp")),
                "gt": unpack_value(gt_record.get("wundtyp"))
            },
            "wundstadium": {
                "llm": unpack_value(llm_record.get("wundphase")),
                "gt": unpack_value(gt_record.get("wundstadium"))
            },
            "exsudat": {
                "llm": unpack_value(llm_record.get("exsudat_menge")),
                "gt": unpack_value(gt_record.get("exsudat"))
            },
            "infektion": {
                "llm": unpack_value(llm_record.get("infektionsstatus")),
                "gt": unpack_value(gt_record.get("infektion"))
            },
            "debridement_notwendig": {
                "llm": unpack_value(llm_record.get("debridement_notwendig")),
                "gt": unpack_value(gt_record.get("debridement_notwendig"))
            },
            "antimikrobiell_notwendig": {
                "llm": unpack_value(llm_record.get("antimikrobieller_verband")),
                "gt": unpack_value(gt_record.get("antimikrobiell_notwendig"))
            },
            "kompression_indiziert": {
                "llm": unpack_value(llm_record.get("kompression_indiziert")),
                "gt": unpack_value(gt_record.get("kompression_indiziert"))
            }
        }
    }
