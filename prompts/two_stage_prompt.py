"""
two_stage_prompt.py

2-Stage CoT Prompt-Ansatz für die Wundbildanalyse.
Stage 1: Bild -> Wundbeschreibung (Strukturierter Befund)
Stage 2: Bild + Wundbeschreibung (Stage 1) + Produktkatalog -> Wundbehandlung (Produkte/Klassen)

Usage:
    from prompts.two_stage_prompt import analyze_wound_image_two_stage
"""

import json
from typing import Dict, Any, Tuple
from openai import OpenAI

from schema import OUTPUT_SCHEMA
from lr_schema import OUTPUT_SCHEMA_LR
from core.client import call_llm_api


MODEL = "gpt-5"
TEMPERATURE = 1
MAX_TOKENS = 16384
REASONING_EFFORT = "high"


STAGE1_KEYS_STANDARD = [
    "wundtyp",
    "wundtyp_sonstiges",
    "wundtyp_spezifizierung",
    "lokalisation",
    "wundphase",
    "exsudat_menge",
    "infektionsstatus",
    "wundrand",
    "wundumgebung",
    "weitere_auffaelligkeiten",
]

STAGE2_KEYS_STANDARD = [
    "debridement_notwendig",
    "spuelloesung",
    "debridement_methode",
    "praeferenz_verbandklasse",
    "alternativ_verbandklasse",
    "antimikrobieller_verband",
    "antimikrobielles_agens",
    "sekundaerverband_fixierung",
    "wundrand_hautschutz",
    "kompression_indiziert",
    "kompression_art",
    "einschraenkungen_annahmen",
]

STAGE1_KEYS_LR = [
    "wundtyp",
    "lokalisation",
    "wundstadium",
    "wundstadium_sonstiges",
    "wundgrund",
    "wundrand",
    "wundrand_sonstiges",
    "wundumgebung",
    "wundumgebung_sonstiges",
    "exsudat_menge",
    "weitere_auffaelligkeiten",
]

STAGE2_KEYS_LR = [
    "debridement_notwendig",
    "debridement_methode",
    "infektion_vorhanden",
    "spuelloesung",
    "praeferenz_wundauflage",
    "alternativ_wundauflage",
    "praeferenz_ergaenzung",
    "alternativ_ergaenzung",
    "kompression_indiziert",
    "kompression_produkt",
    "einschraenkungen_annahmen",
]


def extract_subschema(full_schema: Dict[str, Any], keys: list) -> Dict[str, Any]:
    """Erstellt ein Teil-JSON-Schema für die angegebenen Keys basierend auf einem Vollschema."""
    sub_properties = {k: full_schema["properties"][k] for k in keys if k in full_schema["properties"]}
    full_req = full_schema.get("required", [])
    sub_required = [k for k in keys if k in full_req]
    
    return {
        "type": "object",
        "properties": sub_properties,
        "required": sub_required
    }


def get_stage1_schema(mode: str = "standard") -> Dict[str, Any]:
    """Gibt das JSON-Schema für Stage 1 (Wundbeschreibung) zurück."""
    if mode == "lr":
        return extract_subschema(OUTPUT_SCHEMA_LR, STAGE1_KEYS_LR)
    return extract_subschema(OUTPUT_SCHEMA, STAGE1_KEYS_STANDARD)


def get_stage2_schema(mode: str = "standard") -> Dict[str, Any]:
    """Gibt das JSON-Schema für Stage 2 (Wundbehandlung) zurück."""
    if mode == "lr":
        return extract_subschema(OUTPUT_SCHEMA_LR, STAGE2_KEYS_LR)
    return extract_subschema(OUTPUT_SCHEMA, STAGE2_KEYS_STANDARD)


# ============================================================
# STAGE 1 PROMPTS
# ============================================================

def get_stage1_system_prompt() -> str:
    return """You are an experienced wound care specialist. Your task is Stage 1 of a 2-stage assessment: \
Analyze the provided wound image and provide a comprehensive, structured clinical assessment of the wound \
(wound description / visual characteristics).

Important constraints:
- Base your analysis solely on the provided wound image.
- Output your findings strictly in the specified JSON format for Stage 1.
- Respond ONLY with the JSON object, no additional conversational text."""


def build_stage1_user_prompt(mode: str = "standard") -> str:
    schema = get_stage1_schema(mode)
    schema_str = json.dumps(schema, indent=2, ensure_ascii=False)
    
    return f"""Analyze the provided wound image and describe all visual characteristics of the wound in detail.

Provide your wound assessment in the following exact JSON format:

{schema_str}

Respond ONLY with the JSON object."""


# ============================================================
# STAGE 2 PROMPTS
# ============================================================

def get_stage2_system_prompt(mode: str = "standard") -> str:
    target = "dressing classes" if mode == "standard" else "Lohmann & Rauscher (L&R) products"
    
    return f"""You are an experienced wound care specialist. Your task is Stage 2 of a 2-stage assessment: \
Select the optimal treatment plan and {target} based on BOTH the provided wound image AND the structured \
Stage 1 wound assessment.

Important constraints:
- You must ONLY recommend {target} that appear in the provided product catalog.
- Carefully evaluate the Stage 1 wound assessment together with visual features in the image before determining treatment recommendations.
- For primary dressings (and secondary dressings/supplements where required), recommend coherent treatment sets.
- Output your treatment recommendation strictly in the specified JSON format for Stage 2.
- Respond ONLY with the JSON object, no additional text."""


def build_stage2_user_prompt(catalog: str, stage1_output: Dict[str, Any], mode: str = "standard") -> str:
    schema = get_stage2_schema(mode)
    schema_str = json.dumps(schema, indent=2, ensure_ascii=False)
    stage1_json_str = json.dumps(stage1_output, indent=2, ensure_ascii=False)
    target = "Lohmann & Rauscher (L&R) products" if mode == "lr" else "dressing classes"
    
    return f"""## Available Product Catalog
The following products/classes are available for recommendation. You must ONLY recommend items listed in this catalog.

<product_catalog>
{catalog}
</product_catalog>

## Stage 1 Wound Assessment
The visual assessment from Stage 1 produced the following structured findings:

<stage_1_wound_assessment>
{stage1_json_str}
</stage_1_wound_assessment>

## Task (Stage 2)
Using the wound image and the Stage 1 wound assessment above, select the appropriate {target} \
from the product catalog for:
1. Wound bed preparation / Débridement
2. Primary dressing (preferred and alternative options)
3. Secondary dressing / fixation / skin protection
4. Compression therapy

Provide your treatment recommendations in the following exact JSON format:

{schema_str}

Respond ONLY with the JSON object, no additional text."""


# ============================================================
# ORCHESTRIERUNG: 2-STAGE EXECUTION
# ============================================================

def analyze_wound_image_two_stage(
    image_path: str,
    catalog: str,
    client: OpenAI = None,
    mode: str = "standard"
) -> Dict[str, Any]:
    """
    Führt die 2-Stage Wundanalyse durch:
    Stage 1: Wundbild -> Wundbeschreibung
    Stage 2: Wundbild + Wundbeschreibung + Katalog -> Wundbehandlung

    Args:
        image_path: Pfad zum Wundbild.
        catalog: Produktkatalog als String.
        client: OpenAI Client Instance (optional).
        mode: "standard" für generische Klassen, "lr" für L&R-Produkte.

    Returns:
        Dict mit zusammengesetztem Gesamtergebnis (response) und Metadaten beider Stages.
    """
    approach_name = "two_stage_lr" if mode == "lr" else "two_stage"
    questionnaire_name = "fragebogen_1_lr_produkte" if mode == "lr" else "fragebogen_1_verbandsklassen"

    # --------------------------------------------------------
    # STAGE 1: Wundbeschreibung
    # --------------------------------------------------------
    print("-> Starte Stage 1: Visuelle Wundbeschreibung...")
    stage1_system = get_stage1_system_prompt()
    stage1_user = build_stage1_user_prompt(mode)

    stage1_res = call_llm_api(
        model=MODEL,
        system_prompt=stage1_system,
        user_prompt=stage1_user,
        image_path=image_path,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        reasoning_effort=REASONING_EFFORT,
        client=client,
        prompt_cache_key=f"stage1_{mode}"
    )

    stage1_parsed = stage1_res.get("response") or {}
    if isinstance(stage1_parsed, dict) and "properties" in stage1_parsed and isinstance(stage1_parsed["properties"], dict):
        stage1_parsed = stage1_parsed["properties"]

    # --------------------------------------------------------
    # STAGE 2: Wundbehandlung
    # --------------------------------------------------------
    print("-> Starte Stage 2: Wundbehandlung (Katalogbasierte Produktauswahl + Bild & Befund)...")
    stage2_system = get_stage2_system_prompt(mode)
    stage2_user = build_stage2_user_prompt(catalog, stage1_parsed, mode)

    stage2_res = call_llm_api(
        model=MODEL,
        system_prompt=stage2_system,
        user_prompt=stage2_user,
        image_path=image_path,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        reasoning_effort=REASONING_EFFORT,
        client=client,
        prompt_cache_key=f"stage2_{mode}"
    )

    stage2_parsed = stage2_res.get("response") or {}
    if isinstance(stage2_parsed, dict) and "properties" in stage2_parsed and isinstance(stage2_parsed["properties"], dict):
        stage2_parsed = stage2_parsed["properties"]

    # --------------------------------------------------------
    # COMBINE RESULTS
    # --------------------------------------------------------
    combined_response = {}
    combined_response.update(stage1_parsed)
    combined_response.update(stage2_parsed)

    stage1_meta = stage1_res.get("metadata", {})
    stage2_meta = stage2_res.get("metadata", {})

    elapsed_seconds = round(stage1_meta.get("elapsed_seconds", 0.0) + stage2_meta.get("elapsed_seconds", 0.0), 2)
    prompt_tokens = stage1_meta.get("prompt_tokens", 0) + stage2_meta.get("prompt_tokens", 0)
    completion_tokens = stage1_meta.get("completion_tokens", 0) + stage2_meta.get("completion_tokens", 0)
    total_tokens = stage1_meta.get("total_tokens", 0) + stage2_meta.get("total_tokens", 0)
    cached_tokens = stage1_meta.get("cached_tokens", 0) + stage2_meta.get("cached_tokens", 0)
    uncached_tokens = stage1_meta.get("uncached_tokens", 0) + stage2_meta.get("uncached_tokens", 0)
    reasoning_tokens = stage1_meta.get("reasoning_tokens", 0) + stage2_meta.get("reasoning_tokens", 0)
    json_valid = (stage1_parsed is not None) and (stage2_parsed is not None)

    final_result = {
        "response": combined_response,
        "raw_response": f"=== STAGE 1 ===\n{stage1_res.get('raw_response', '')}\n\n=== STAGE 2 ===\n{stage2_res.get('raw_response', '')}",
        "metadata": {
            "model": MODEL,
            "prompt_approach": approach_name,
            "questionnaire": questionnaire_name,
            "temperature": TEMPERATURE,
            "max_tokens": MAX_TOKENS,
            "reasoning_effort": REASONING_EFFORT,
            "elapsed_seconds": elapsed_seconds,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cached_tokens": cached_tokens,
            "uncached_tokens": uncached_tokens,
            "reasoning_tokens": reasoning_tokens,
            "json_valid": json_valid,
            "stage_1": {
                "system_prompt": stage1_system,
                "user_prompt": stage1_user,
                "raw_response": stage1_res.get("raw_response"),
                "parsed_response": stage1_parsed,
                "metadata": stage1_meta,
            },
            "stage_2": {
                "system_prompt": stage2_system,
                "user_prompt": stage2_user,
                "raw_response": stage2_res.get("raw_response"),
                "parsed_response": stage2_parsed,
                "metadata": stage2_meta,
            }
        },
        "system_prompt": f"Stage 1 System:\n{stage1_system}\n\nStage 2 System:\n{stage2_system}",
        "user_prompt": f"Stage 1 User:\n{stage1_user}\n\nStage 2 User:\n{stage2_user}"
    }

    return final_result
