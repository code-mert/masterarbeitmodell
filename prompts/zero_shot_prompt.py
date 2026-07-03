"""
zero_shot_prompt.py

Zero-Shot Prompt für die Wundbildanalyse (Fragebogen 1 - Verbandsklassen).
Enthält System Prompt, User Prompt Builder und API-Call Funktion.

Usage:
    from zero_shot_prompt import analyze_wound_image, load_catalog
"""

import json
from pathlib import Path
from openai import OpenAI
from schema import OUTPUT_SCHEMA
from lr_schema import OUTPUT_SCHEMA_LR
from core.client import call_llm_api


# ============================================================
# MODELL-EINSTELLUNGEN
# ============================================================

MODEL = "gpt-5"
TEMPERATURE = 1
MAX_TOKENS = 16384
REASONING_EFFORT = "high"


# ============================================================
# SYSTEM PROMPT & CONSTRAINTS
# ============================================================

def get_constraints(mode: str) -> str:
    """Gibt die zentralen Anweisungen und Einschränkungen für das LLM zurück."""
    target = "dressing classes" if mode == "standard" else "Lohmann & Rauscher (L&R) products"
    
    return f"""Important constraints:
- You are working ONLY from the provided wound image. You have NO access to patient history, lab results, or other clinical metadata.
- You may ONLY recommend {target} that appear in the provided catalog.
- You must provide a preferred treatment option and a therapeutically equivalent alternative treatment option for the primary wound dressing (and secondary dressing if using the L&R catalog), as defined in the JSON schema fields (e.g. praeferenz_... and alternativ_...).
- Within any recommended set, all listed {target} must be clinically compatible and form a coherent treatment plan.
- Provide your response in the exact JSON format specified."""


def get_system_prompt(mode: str = "standard") -> str:
    """Gibt den System-Prompt für den gewählten Modus zurück."""
    target = "dressing classes" if mode == "standard" else "Lohmann & Rauscher (L&R) products"
    constraints = get_constraints(mode)
    
    return f"""You are an experienced wound care specialist with extensive knowledge \
of wound assessment and wound care selection. You work in a clinical setting and \
are tasked with analyzing wound images and recommending appropriate {target}.
 
You will be provided with:
1. A wound image for analysis
2. A catalog of available {target}
 
{constraints}"""


# ============================================================
# PROMPT BUILDER
# ============================================================

def build_user_prompt(catalog: str, mode: str = "standard") -> str:
    """
    Baut den User-Prompt aus Katalog + Aufgabenstellung + JSON-Schema.

    Args:
        catalog: Inhalt der Katalogdatei als String.
        mode: "standard" für generische Verbandklassen, "lr" für L&R-Produkte.

    Returns:
        Fertiger User-Prompt als String.
    """
    schema = OUTPUT_SCHEMA_LR if mode == "lr" else OUTPUT_SCHEMA
    schema_json = json.dumps(schema, indent=2, ensure_ascii=False)
    target = "Lohmann & Rauscher (L&R) products" if mode == "lr" else "dressing classes"
    constraints = get_constraints(mode)
    
    return f"""## Available Product Catalog
The following products are available for recommendation. \
You must ONLY recommend products from this catalog.

<product_catalog>
{catalog}
</product_catalog>

## Task
Analyze the provided wound image and recommend appropriate {target} \
from the catalog above.
 
{constraints}
 
Provide your recommendations in the following JSON format:
 
{schema_json}
 
Respond ONLY with the JSON object, no additional text."""


# ============================================================
# HILFSFUNKTIONEN
# ============================================================

def load_catalog(path: str) -> str:
    """Lädt den Markdown-Katalog als String."""
    with open(path, "r", encoding="utf-8") as f:
        catalog = f.read()
    print(f"Katalog geladen: {len(catalog):,} Zeichen (~{len(catalog) // 4:,} Tokens)")
    return catalog


# ============================================================
# API-CALL
# ============================================================

def analyze_wound_image(image_path: str, catalog: str, client: OpenAI = None, mode: str = "standard") -> dict:
    """
    Schickt ein Wundbild + Katalog an GPT-5 (Zero-Shot) über den zentralen LLM Client.

    Args:
        image_path: Pfad zum Wundbild.
        catalog: Katalog-String (aus load_catalog).
        client: OpenAI Client. Wird automatisch erstellt falls None.
        mode: "standard" für generische Verbandklassen, "lr" für L&R-Produkte.

    Returns:
        dict mit:
            - 'response': Geparstes JSON (oder None bei Parse-Fehler)
            - 'raw_response': Roher Antwort-String
            - 'metadata': Modell, Timestamp, Tokens etc.
    """
    user_prompt = build_user_prompt(catalog, mode)
    system_prompt = get_system_prompt(mode)
    
    approach_name = "zero_shot_lr" if mode == "lr" else "zero_shot"
    prompt_cache_key = f"{approach_name}_{mode}"

    result = call_llm_api(
        model=MODEL,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        image_path=image_path,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        reasoning_effort=REASONING_EFFORT,
        client=client,
        prompt_cache_key=prompt_cache_key
    )

    # Ansatzspezifische Metadaten anreichern
    questionnaire_name = "fragebogen_1_lr_produkte" if mode == "lr" else "fragebogen_1_verbandsklassen"
    
    result["metadata"]["prompt_approach"] = approach_name
    result["metadata"]["questionnaire"] = questionnaire_name
    
    result["system_prompt"] = system_prompt
    result["user_prompt"] = user_prompt

    return result