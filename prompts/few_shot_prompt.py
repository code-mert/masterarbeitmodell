"""
few_shot_prompt.py

Few-Shot Prompt für die Wundbildanalyse.
Ermöglicht die Übergabe von 3 Beispiel-Wundbildern mit ihren entsprechenden
Ground-Truth-Ergebnissen als Kontext vor der Analyse des eigentlichen Wundbildes.

Usage:
    from prompts.few_shot_prompt import analyze_wound_image_few_shot
"""

import json
import time
from datetime import datetime
from pathlib import Path
from openai import OpenAI

from schema import OUTPUT_SCHEMA
from lr_schema import OUTPUT_SCHEMA_LR
from core.image_utils import encode_image, get_media_type
from core.parsing import parse_json_response

# Wir importieren die Einstellungen und Basisprompts aus zero_shot_prompt,
# um Redundanz zu vermeiden und Konsistenz zu wahren.
from prompts.zero_shot_prompt import (
    MODEL,
    TEMPERATURE,
    MAX_TOKENS,
    REASONING_EFFORT,
    get_system_prompt,
    build_user_prompt,
    load_catalog
)

def map_csv_to_schema(gt_record: dict, mode: str = "standard") -> dict:
    """
    Konvertiert einen Ground Truth Datensatz (aus dem CSV) in das entsprechende JSON-Schema.
    Behandelt Listen- und Stringkonvertierungen sowie Enum-Anpassungen.
    """
    if mode == "lr":
        wundtyp_val = gt_record.get("wundtyp", "")
        if isinstance(wundtyp_val, list):
            wundtyp_str = ", ".join(wundtyp_val)
        else:
            wundtyp_str = str(wundtyp_val)
            
        wundstadium_list = gt_record.get("wundstadium", [])
        wundstadium_val = "Sonstiges"
        wundstadium_sonstiges_val = ""
        lr_stadium_enum = ["Exsudation", "Nekrose", "Fibrinbelag", "Granulation", "Epithelisierung", "Infektion", "Sonstiges"]
        if wundstadium_list:
            first_stadium = wundstadium_list[0]
            if first_stadium in lr_stadium_enum:
                wundstadium_val = first_stadium
            elif "Fibrinbelag" in first_stadium:
                wundstadium_val = "Fibrinbelag"
            elif "Nekrose" in first_stadium:
                wundstadium_val = "Nekrose"
            else:
                wundstadium_val = "Sonstiges"
                wundstadium_sonstiges_val = first_stadium
        
        infektion_val = gt_record.get("infektion", "")
        infektion_vorhanden = "nein"
        if "ja" in str(infektion_val).lower() or "verdacht" in str(infektion_val).lower() or "deutlich" in str(infektion_val).lower():
            infektion_vorhanden = "ja"
            
        spuelloesung_list = gt_record.get("spuelloesung", [])
        spuelloesung_val = ""
        if spuelloesung_list:
            first_spuel = spuelloesung_list[0]
            if "antimikrobiell" in first_spuel.lower():
                spuelloesung_val = "Antimikrobielle Spüllösung"
            elif "neutral" in first_spuel.lower() or "nacl" in first_spuel.lower() or "ringer" in first_spuel.lower():
                spuelloesung_val = "Neutrale Spüllösung"
                
        praeferenz_wundauflage = gt_record.get("praeferenz_produkt", [])
        alternativ_wundauflage = gt_record.get("alternative_produkt", [])
        if not alternativ_wundauflage:
            alternativ_wundauflage = None
            
        praeferenz_ergaenzung = gt_record.get("sekundaerverband", [])
        alternativ_ergaenzung = gt_record.get("sekundaerverband", [])
        if not alternativ_ergaenzung:
            alternativ_ergaenzung = None
            
        kompression_ind = gt_record.get("kompression_indiziert", "")
        kompression_indiziert = "nein"
        if "ja" in str(kompression_ind).lower():
            kompression_indiziert = "ja"
            
        return {
            "wundtyp": wundtyp_str,
            "lokalisation": gt_record.get("lokalisation", ""),
            "wundstadium": wundstadium_val,
            "wundstadium_sonstiges": wundstadium_sonstiges_val,
            "wundgrund": gt_record.get("wundtyp_spezifikation", ""),
            "wundrand": gt_record.get("wundrand", []),
            "wundumgebung": gt_record.get("wundumgebung", []),
            "exsudat_menge": gt_record.get("exsudat", "Keine"),
            "weitere_auffaelligkeiten": gt_record.get("auffaelligkeiten", ""),
            "debridement_notwendig": "ja" if "ja" in str(gt_record.get("debridement_notwendig", "")).lower() else "nein",
            "debridement_methode": gt_record.get("debridement", []),
            "infektion_vorhanden": infektion_vorhanden,
            "spuelloesung": spuelloesung_val,
            "praeferenz_wundauflage": praeferenz_wundauflage,
            "alternativ_wundauflage": alternativ_wundauflage,
            "praeferenz_ergaenzung": praeferenz_ergaenzung,
            "alternativ_ergaenzung": alternativ_ergaenzung,
            "kompression_indiziert": kompression_indiziert,
            "kompression_produkt": gt_record.get("kompression_produkte", []),
            "einschraenkungen_annahmen": gt_record.get("einschraenkungen", "")
        }
    else:
        wundtyp_val = gt_record.get("wundtyp", "")
        wundtyp_enum = [
            "Dekubitus",
            "Ulcus cruris venosum",
            "Ulcus cruris arteriosum",
            "Ulcus cruris mixtum",
            "Diabetisches Fußulkus",
            "Traumatische Wunde",
            "Tumorwunde",
            "Verbrennungswunde",
            "Postoperative Wunde",
            "Sonstiges"
        ]
        wundtyp_str = "Sonstiges"
        wundtyp_sonstiges_str = ""
        if isinstance(wundtyp_val, list) and wundtyp_val:
            first_wund = wundtyp_val[0]
            if first_wund in wundtyp_enum:
                wundtyp_str = first_wund
            else:
                wundtyp_str = "Sonstiges"
                wundtyp_sonstiges_str = first_wund
        elif isinstance(wundtyp_val, str) and wundtyp_val:
            if wundtyp_val in wundtyp_enum:
                wundtyp_str = wundtyp_val
            else:
                wundtyp_str = "Sonstiges"
                wundtyp_sonstiges_str = wundtyp_val
                
        wundtyp_spec = gt_record.get("wundtyp_spezifikation", "")
        if not wundtyp_spec and isinstance(wundtyp_val, list) and len(wundtyp_val) > 1:
            wundtyp_spec = wundtyp_val[1]
            
        exsudat = gt_record.get("exsudat", "Keine")
        if "stark" in str(exsudat).lower():
            if "sehr" in str(exsudat).lower():
                exsudat_menge = "Sehr stark"
            else:
                exsudat_menge = "Stark"
        elif "mäßig" in str(exsudat).lower() or "maessig" in str(exsudat).lower():
            exsudat_menge = "Mäßig"
        elif "leicht" in str(exsudat).lower():
            exsudat_menge = "Leicht"
        else:
            exsudat_menge = "Keine"
            
        infektion = gt_record.get("infektion", "Keine Infektionszeichen")
        infektionsstatus = "Keine Infektionszeichen"
        if "deutlich" in str(infektion).lower():
            infektionsstatus = "Deutliche Infektionszeichen"
        elif "verdacht" in str(infektion).lower() or "kritisch" in str(infektion).lower():
            infektionsstatus = "Verdacht auf Infektion / kritische Kolonisation"
            
        spuelloesung_list = gt_record.get("spuelloesung", [])
        spuelloesung = ""
        if spuelloesung_list:
            first_spuel = spuelloesung_list[0]
            if "phmb" in first_spuel.lower() or "octenisept" in first_spuel.lower() or "antimikrobiell" in first_spuel.lower():
                spuelloesung = "Antimikrobielle Spüllösung (PHMB, Octenisept)"
            elif "nacl" in first_spuel.lower() or "ringer" in first_spuel.lower() or "neutral" in first_spuel.lower():
                spuelloesung = "Neutrale Spüllösung (NaCl, Ringer)"
                
        debridement_notwendig = "ja" if "ja" in str(gt_record.get("debridement_notwendig", "")).lower() else "nein"
        antimikrobiell_notwendig = gt_record.get("antimikrobiell_notwendig", "")
        antimikrobieller_verband = "ja" if "ja" in str(antimikrobiell_notwendig).lower() else "nein"
        
        kompression_ind = gt_record.get("kompression_indiziert", "")
        if "ja" in str(kompression_ind).lower():
            kompression_indiziert = "ja"
        elif "nein" in str(kompression_ind).lower():
            kompression_indiziert = "nein"
        else:
            kompression_indiziert = "nicht beurteilbar"
            
        alternativ_verbandklasse = gt_record.get("alternative_produkt", [])
        if not alternativ_verbandklasse:
            alternativ_verbandklasse = None
            
        return {
            "wundtyp": wundtyp_str,
            "wundtyp_sonstiges": wundtyp_sonstiges_str,
            "wundtyp_spezifizierung": wundtyp_spec,
            "lokalisation": gt_record.get("lokalisation", ""),
            "wundphase": gt_record.get("wundstadium", []),
            "exsudat_menge": exsudat_menge,
            "infektionsstatus": infektionsstatus,
            "wundrand": gt_record.get("wundrand", []),
            "wundumgebung": gt_record.get("wundumgebung", []),
            "weitere_auffaelligkeiten": gt_record.get("auffaelligkeiten", ""),
            "debridement_notwendig": debridement_notwendig,
            "spuelloesung": spuelloesung,
            "debridement_methode": gt_record.get("debridement", []),
            "praeferenz_verbandklasse": gt_record.get("praeferenz_produkt", []),
            "alternativ_verbandklasse": alternativ_verbandklasse,
            "antimikrobieller_verband": antimikrobieller_verband,
            "antimikrobielles_agens": gt_record.get("antimikrobielles_agens", []),
            "sekundaerverband_fixierung": gt_record.get("sekundaerverband", []),
            "wundrand_hautschutz": gt_record.get("hautschutz", []),
            "kompression_indiziert": kompression_indiziert,
            "kompression_art": gt_record.get("kompression_produkte", []),
            "einschraenkungen_annahmen": gt_record.get("einschraenkungen", "")
        }


DEFAULT_FEW_SHOT_EXAMPLE_IDS = ["wunde_04", "wunde_18"]


def find_image_path(image_id: str, image_dir: Path = Path("data/wundbilder")) -> Path:
    """Findet die Bilddatei für eine gegebenen Image ID (z.B. wunde_04 -> Bild4.jpg)."""
    import re
    match = re.search(r"\d+", image_id)
    if match:
        num = int(match.group())
        for f in image_dir.glob("*"):
            stem_lower = f.stem.lower()
            if stem_lower in (f"bild{num}", f"bild{num:02d}", f"wunde_{num:02d}", f"wunde_{num}"):
                return f
    raise FileNotFoundError(f"Keine Bilddatei für '{image_id}' in '{image_dir}' gefunden.")


def get_default_few_shot_examples(mode: str = "standard", example_ids: list = None) -> list:
    """
    Lädt automatisch die 2 prägnanten Few-Shot-Beispiele (wunde_04 und wunde_18)
    inklusive ihrer Ground-Truth-Daten und Bildpfade.
    """
    from eval.loaders import load_ground_truth
    if example_ids is None:
        example_ids = DEFAULT_FEW_SHOT_EXAMPLE_IDS

    csv_path = "data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv" if mode == "lr" else "data/ground_truth/allgemeine_verbandsklassen.csv"
    gt_data = load_ground_truth(csv_path)

    examples = []
    for eid in example_ids:
        if eid in gt_data:
            img_p = find_image_path(eid)
            examples.append({
                "image_path": str(img_p),
                "gt_record": gt_data[eid]
            })
    return examples


def analyze_wound_image_few_shot(
    image_path: str,
    catalog: str,
    examples: list = None,
    client: OpenAI = None,
    mode: str = "standard"
) -> dict:
    """
    Schickt ein Wundbild + Katalog + 2 Few-Shot Beispiele (Bilder & Ground Truth)
    an das LLM über die OpenAI API.

    Args:
        image_path: Pfad zum Ziel-Wundbild, das analysiert werden soll.
        catalog: Katalog-String.
        examples: Liste von 2 Dictionaries mit 'image_path' und 'gt_record'.
                  Falls None, werden automatisch wunde_04 und wunde_18 geladen.
        client: OpenAI Client. Wird automatisch erstellt falls None.
        mode: "standard" für generische Verbandklassen, "lr" für L&R-Produkte.

    Returns:
        dict mit der standardisierten LLM-Antwort und Metadaten.
    """
    if client is None:
        client = OpenAI()

    if examples is None:
        examples = get_default_few_shot_examples(mode=mode)

    # 1. System Prompt & User Prompt (Target) aufbauen
    system_prompt = get_system_prompt(mode)
    user_prompt = build_user_prompt(catalog, mode)

    # 2. Chat-Verlauf (Messages) aufbauen
    messages = []
    messages.append({"role": "system", "content": system_prompt})

    # Few-Shot-Beispiele hinzufügen
    for idx, ex in enumerate(examples):
        ex_img_path = ex.get("image_path")
        ex_gt = ex.get("gt_record")
        
        if not ex_img_path or ex_gt is None:
            raise ValueError(f"Beispiel {idx} ist unvollständig (benötigt 'image_path' und 'gt_record').")

        # Ground Truth ins passende JSON-Schema überführen
        if isinstance(ex_gt, dict):
            # Prüfen ob es ein roher CSV-Record ist (z.B. enthält 'image_id')
            if "image_id" in ex_gt:
                ex_gt_mapped = map_csv_to_schema(ex_gt, mode)
            else:
                ex_gt_mapped = ex_gt
            ex_gt_str = json.dumps(ex_gt_mapped, indent=2, ensure_ascii=False)
        else:
            ex_gt_str = str(ex_gt)

        # Beispielbild codieren
        ex_img_b64 = encode_image(ex_img_path)
        ex_media_type = get_media_type(ex_img_path)

        # User-Nachricht mit dem Beispielbild
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": f"Analyze the following example wound image (Example {idx + 1})."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{ex_media_type};base64,{ex_img_b64}",
                        "detail": "high"
                    }
                }
            ]
        })

        # Assistant-Nachricht mit der korrekten Ground-Truth-Antwort
        messages.append({
            "role": "assistant",
            "content": ex_gt_str
        })

    # 3. Ziel-Nachricht (Target Wundbild & Instruktionen) hinzufügen
    target_img_b64 = encode_image(image_path)
    target_media_type = get_media_type(image_path)

    messages.append({
        "role": "user",
        "content": [
            {"type": "text", "text": user_prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{target_media_type};base64,{target_img_b64}",
                    "detail": "high"
                }
            }
        ]
    })

    # 4. API-Aufruf durchführen
    start_time = time.time()

    completion = client.chat.completions.create(
        model=MODEL,
        temperature=TEMPERATURE,
        max_completion_tokens=MAX_TOKENS,
        reasoning_effort=REASONING_EFFORT,
        messages=messages
    )

    elapsed = time.time() - start_time
    raw_response = completion.choices[0].message.content
    parsed = parse_json_response(raw_response)
    usage = completion.usage

    # Ansatzspezifische Metadaten anreichern
    approach_name = "few_shot_lr" if mode == "lr" else "few_shot"
    questionnaire_name = "fragebogen_1_lr_produkte" if mode == "lr" else "fragebogen_1_verbandsklassen"

    return {
        "response": parsed,
        "raw_response": raw_response,
        "metadata": {
            "model": MODEL,
            "temperature": TEMPERATURE,
            "timestamp": datetime.now().isoformat(),
            "image_name": Path(image_path).stem,
            "elapsed_seconds": round(elapsed, 2),
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
            "json_valid": parsed is not None,
            "prompt_approach": approach_name,
            "questionnaire": questionnaire_name
        }
    }
