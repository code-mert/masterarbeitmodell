"""
run_few_shot.py

Beispiel-Skript zur Ausführung einer Few-Shot Wundbildanalyse.
Lädt 3 Beispiel-Wundbilder + deren Ground Truth aus dem CSV, analysiert ein viertes Bild und speichert das Ergebnis.

Usage:
    .venv/bin/python examples/run_few_shot.py
"""

import sys
from pathlib import Path
from dotenv import load_dotenv

# Füge das Projektverzeichnis zum Python-Pfad hinzu
sys.path.append(str(Path(__file__).resolve().parent.parent))

from prompts.few_shot_prompt import analyze_wound_image_few_shot, load_catalog, MODEL, TEMPERATURE, get_system_prompt
from eval.loaders import load_ground_truth
from core.storage import save_run, compute_hash

# Lade Umgebungsvariablen (.env)
load_dotenv()

IMAGE_DIR = Path("data/wundbilder")
CSV_PATH = "data/ground_truth/allgemeine_verbandsklassen.csv"
CATALOG_PATH = "data/produktkatalog/AllgemeineProdukte.md"

def find_image_path(image_id: str, image_dir: Path) -> Path:
    """Findet die Bilddatei für eine gegebenen Image ID (z.B. wunde_01 -> Bild1.jpg)."""
    import re
    match = re.search(r"\d+", image_id)
    if match:
        num = int(match.group())
        for f in image_dir.glob("*"):
            stem_lower = f.stem.lower()
            if stem_lower in (f"bild{num}", f"bild{num:02d}", f"wunde_{num:02d}", f"wunde_{num}"):
                return f
    raise FileNotFoundError(f"Keine Bilddatei für '{image_id}' in '{image_dir}' gefunden.")

def main():
    print("=" * 80)
    print("FEW-SHOT WUNDBILDANALYSE TEST RUNNER")
    print("=" * 80)

    # 1. Ground Truth laden
    print("Lade Ground Truth CSV...")
    gt_data = load_ground_truth(CSV_PATH)
    print(f"-> {len(gt_data)} Ground Truth Datensätze geladen.")

    # 2. Katalog laden
    print("Lade Produktkatalog...")
    catalog = load_catalog(CATALOG_PATH)

    # 3. Few-Shot Beispiele festlegen (2 ausgewählte prägnante Wundbilder: wunde_04 und wunde_18)
    example_ids = ["wunde_04", "wunde_18"]
    examples = []
    
    print("\nBereite Few-Shot Beispiele vor (2 Bilder):")
    for eid in example_ids:
        if eid not in gt_data:
            print(f"❌ Fehler: '{eid}' nicht in Ground Truth Daten gefunden.")
            return
            
        try:
            img_path = find_image_path(eid, IMAGE_DIR)
            examples.append({
                "image_path": str(img_path),
                "gt_record": gt_data[eid]
            })
            print(f" - {eid} -> Bild: {img_path.name}")
        except FileNotFoundError as e:
            print(f"❌ {e}")
            return

    # 4. Zielbild definieren (z. B. wunde_01)
    target_id = "wunde_01"
    
    # Prüfen, ob das Zielbild eines der Beispielbilder ist (soll im Gesamtlauf übersprungen werden):
    if target_id in example_ids:
        print(f"\n⏩ Überspringe '{target_id}', da es als Few-Shot Beispielbild verwendet wird.")
        return

    try:
        target_img_path = find_image_path(target_id, IMAGE_DIR)
        print(f"\nZielbild zur Analyse: {target_id} -> {target_img_path.name}")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return

    # 5. Few-Shot API-Call ausführen
    print("\nStarte Few-Shot Analyse (Aufruf der API)...")
    try:
        result = analyze_wound_image_few_shot(
            image_path=str(target_img_path),
            catalog=catalog,
            examples=examples,
            mode="standard"
        )
        
        print("\n" + "=" * 80)
        print("LLM ANTWORT (GEPARST)")
        print("=" * 80)
        import pprint
        pprint.pprint(result["response"])
        
        print("\n" + "=" * 80)
        print("METADATEN")
        print("=" * 80)
        pprint.pprint(result["metadata"])

        # Ergebnisse abspeichern
        raw_response = result["raw_response"]
        parsed_output = result["response"]
        json_valid = result["metadata"]["json_valid"]
        
        errors = []
        if not json_valid:
            errors.append("Fehler beim Parsen der JSON-Antwort.")
            
        meta_info = {
            "model_version": MODEL,
            "prompt_hash": compute_hash(get_system_prompt("standard")),
            "prompt_version": "v1.0",
            "temperature": TEMPERATURE,
            "catalog_hash": compute_hash(catalog)
        }
        
        run_path = save_run(
            model=MODEL,
            prompt_approach=result["metadata"]["prompt_approach"],
            image_id=target_id,
            raw_response=raw_response,
            parsed_output=parsed_output,
            json_valid=json_valid,
            parse_errors=errors,
            latency_seconds=result["metadata"]["elapsed_seconds"],
            meta_info=meta_info,
            prompt_tokens=result["metadata"].get("prompt_tokens"),
            completion_tokens=result["metadata"].get("completion_tokens"),
            total_tokens=result["metadata"].get("total_tokens")
        )
        
        print("\n" + "=" * 80)
        print(f"✅ Ergebnisse gespeichert unter: {run_path}")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Fehler während der API-Analyse: {e}")

if __name__ == "__main__":
    main()
