import os
import re
import csv
import ast
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Set

# Set up logging for this module
logger = logging.getLogger(__name__)

# List of columns to parse as Python lists/sets
SET_FIELDS: Set[str] = {
    "wundtyp",
    "wundstadium",
    "wundrand",
    "wundumgebung",
    "spuelloesung",
    "debridement",
    "praeferenz_produkt",
    "alternative_produkt",
    "antimikrobielles_agens",
    "sekundaerverband",
    "hautschutz",
    "kompression_produkte",
}

# List of LLM columns to parse as Python lists/sets when loading from CSV
LLM_SET_FIELDS: Set[str] = {
    "wundphase",
    "wundrand",
    "wundumgebung",
    "debridement_methode",
    "praeferenz_verbandklasse",
    "alternativ_verbandklasse",
    "antimikrobielles_agens",
    "sekundaerverband_fixierung",
    "wundrand_hautschutz",
    "kompression_art",
}


def _parse_set_field(val: str) -> List[str]:
    """
    Helper function to parse set fields from CSV.
    Empty strings are converted to empty lists.
    Values formatted as a string list (e.g. '["A", "B"]') are parsed using ast.literal_eval.
    If parsing fails, returns the value as a single-element list.
    """
    if val is None or val.strip() == "":
        return []
    
    val_stripped = val.strip()
    try:
        parsed = ast.literal_eval(val_stripped)
        if isinstance(parsed, (list, tuple, set)):
            return [str(item) for item in parsed]
        return [str(parsed)]
    except Exception as e:
        logger.debug(f"Failed to parse set field value '{val}' with ast.literal_eval: {e}")
        return [val_stripped]

def normalize_image_id(raw_id: str) -> str | None:
    """
    Normalizes image ID strings to the format 'wunde_{n:02d}'.
    For example: 'Bild1' -> 'wunde_01', 'Bild10' -> 'wunde_10', 'wunde_02' -> 'wunde_02'.
    Returns None if no numeric part can be identified.
    """
    if not raw_id or not isinstance(raw_id, str):
        return None
    
    # Check if it is already in the 'wunde_XX' format
    if re.match(r"^wunde_\d{2,}$", raw_id):
        return raw_id
        
    # Match patterns like 'Bild1', 'bild 01', 'wunde 1'
    match = re.search(r"(?:Bild|wunde)\s*(\d+)", raw_id, re.IGNORECASE)
    if match:
        num = int(match.group(1))
        return f"wunde_{num:02d}"
        
    # Fallback to any contiguous digits
    match_any = re.search(r"\d+", raw_id)
    if match_any:
        num = int(match_any.group())
        return f"wunde_{num:02d}"
        
    return None

def load_ground_truth(csv_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Loads Ground Truth data from a CSV file.
    All set fields are parsed into Python lists of strings.
    
    Args:
        csv_path: Absolute or relative path to the CSV file.
        
    Returns:
        A dictionary mapping image_id (e.g., 'wunde_01') to row record dictionary.
    """
    records = {}
    path = Path(csv_path)
    if not path.exists():
        logger.error(f"Ground Truth CSV file not found: {csv_path}")
        raise FileNotFoundError(f"Ground Truth CSV file not found: {csv_path}")

    # Using DictReader automatically handles multiline cell contents.
    with open(path, mode="r", encoding="utf-8") as f:
        # Detect delimiter automatically
        first_line = f.readline()
        f.seek(0)
        delimiter = ";" if ";" in first_line else ","
        
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            image_id = row.get("image_id")
            if not image_id:
                continue
            
            parsed_row = {}
            for col, val in row.items():
                if col in SET_FIELDS:
                    parsed_row[col] = _parse_set_field(val)
                else:
                    parsed_row[col] = val.strip() if val is not None else ""
            
            records[image_id] = parsed_row
            
    return records

def load_llm_outputs(path: str) -> Dict[str, Dict[str, Any]]:
    """
    Loads LLM outputs.
    If path is a CSV file, reads it directly and parses row columns.
    If path is a directory, recursively scans the directory for JSON files, parses them, 
    and returns a dictionary of valid LLM outputs.
    
    Args:
        path: Path to the CSV file or the directory containing individual JSON files.
        
    Returns:
        A dictionary mapping normalized image_id (e.g. 'wunde_01') to parsed_output.
    """
    outputs = {}
    p = Path(path)
    if not p.exists():
        logger.warning(f"LLM output path does not exist: {path}")
        return outputs

    if p.is_file():
        # Load from CSV file
        with open(p, mode="r", encoding="utf-8") as f:
            # Detect delimiter automatically
            first_line = f.readline()
            f.seek(0)
            delimiter = ";" if ";" in first_line else ","
            
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                image_id = row.get("image_id")
                if not image_id:
                    continue
                
                normalized_id = normalize_image_id(image_id)
                if not normalized_id:
                    continue
                    
                parsed_row = {}
                for col, val in row.items():
                    if col == "image_id":
                        continue
                    if col in LLM_SET_FIELDS:
                        parsed_row[col] = _parse_set_field(val)
                    else:
                        parsed_row[col] = val.strip() if val is not None else ""
                
                outputs[normalized_id] = parsed_row
        return outputs

    # If it is a directory, walk recursively
    highest_runs = {}
    for root, _, files in os.walk(p):
        for file in sorted(files):
            if not file.endswith(".json") or file == "_meta.json":
                continue
            
            full_path = Path(root) / file
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                logger.error(f"Error reading JSON file {full_path}: {e}")
                continue
            
            # Check for parsed_output
            if "parsed_output" not in data:
                if "json_valid" in data and data.get("json_valid") is False:
                    logger.warning(f"Skipping invalid JSON output (json_valid == false): {full_path}")
                continue
                
            # Skip if invalid
            if data.get("json_valid") is False:
                logger.warning(f"Skipping invalid JSON output (json_valid == false): {full_path}")
                continue
                
            raw_image_id = data.get("image_id")
            if not raw_image_id:
                logger.warning(f"File {full_path} has no 'image_id' field.")
                continue
                
            normalized_id = normalize_image_id(raw_image_id)
            if not normalized_id:
                logger.warning(f"Could not normalize image_id '{raw_image_id}' from {full_path}.")
                continue
                
            run_id = data.get("run_id", 0)
            if normalized_id not in highest_runs or run_id > highest_runs[normalized_id]:
                highest_runs[normalized_id] = run_id
                outputs[normalized_id] = data["parsed_output"]

    return outputs

def matched_image_ids(gt: Dict[str, Any], llm: Dict[str, Any]) -> List[str]:
    """
    Finds the intersection of image IDs between Ground Truth and LLM outputs.
    Logs missing outputs for GT images as INFO.
    
    Args:
        gt: Dictionary of ground truth records.
        llm: Dictionary of LLM output records.
        
    Returns:
        A sorted list of image IDs present in both dictionaries.
    """
    gt_keys = set(gt.keys())
    llm_keys = set(llm.keys())
    
    intersection = sorted(list(gt_keys.intersection(llm_keys)))
    
    missing_in_llm = gt_keys - llm_keys
    missing_in_gt = llm_keys - gt_keys
    
    if missing_in_llm:
        logger.info(f"Fehlende LLM-Outputs (GT vorhanden, JSON fehlt) [{len(missing_in_llm)}]: {', '.join(sorted(missing_in_llm))}")
    else:
        logger.info("Keine fehlenden LLM-Outputs für vorhandene GT-Bilder.")
        
    if missing_in_gt:
        logger.info(f"LLM-Outputs vorhanden, aber kein GT-Eintrag [{len(missing_in_gt)}]: {', '.join(sorted(missing_in_gt))}")
        
    return intersection
