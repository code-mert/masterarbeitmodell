import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
from prompts.zero_shot_prompt import analyze_wound_image, load_catalog, get_system_prompt, MODEL, TEMPERATURE
from prompts.few_shot_prompt import analyze_wound_image_few_shot, get_default_few_shot_examples, DEFAULT_FEW_SHOT_EXAMPLE_IDS
from prompts.two_stage_prompt import analyze_wound_image_two_stage
from core.storage import save_run, compute_hash

# Lade den API-Key aus der .env Datei
load_dotenv()

# ============================================================
# KONFIGURATION
# ============================================================

# Hier kommen deine Bilder rein (Ordner wird automatisch erstellt)
IMAGE_DIR = Path("data/wundbilder") 

# Der Ordner, in dem die Markdown-Kataloge liegen (wird dynamisch überschrieben)
CATALOG_DIR = Path("data/produktkatalog") 

# Hier werden die Runs pro Bild gespeichert
RUNS_DIR = Path("runs")

def main():
    # 0. Katalog & Prompt-Ansatz auswählen
    print("============================================================")
    print("Wundbild-Analyse Experiment-Runner")
    print("============================================================")
    print("Bitte wähle den Produktkatalog und den Prompt-Ansatz aus:")
    print("  1: Zero-Shot (Generischer Produktkatalog)")
    print("  2: Zero-Shot (Lohmann & Rauscher Produktkatalog)")
    print("  3: Few-Shot (Lohmann & Rauscher Produktkatalog, 2 Beispiele)")
    print("  4: Few-Shot (Generischer Produktkatalog, 2 Beispiele)")
    print("  5: 2-Stage CoT (Lohmann & Rauscher Produktkatalog)")
    print("  6: 2-Stage CoT (Generischer Produktkatalog)")
    
    choice = input("Deine Auswahl (1-6, Standard: 2): ").strip()
    is_few_shot = False
    is_two_stage = False

    if choice == "1":
        mode = "standard"
        catalog_dir = Path("data/produktkatalog")
        prompt_approach = "zero_shot"
        print("-> Modus: Zero-Shot mit Generischem Produktkatalog ausgewählt.")
    elif choice == "3":
        mode = "lr"
        catalog_dir = Path("data/l&r_produktkatalog")
        prompt_approach = "few_shot_lr"
        is_few_shot = True
        print("-> Modus: Few-Shot mit L&R Produktkatalog (2 Beispiele) ausgewählt.")
    elif choice == "4":
        mode = "standard"
        catalog_dir = Path("data/produktkatalog")
        prompt_approach = "few_shot"
        is_few_shot = True
        print("-> Modus: Few-Shot mit Generischem Produktkatalog (2 Beispiele) ausgewählt.")
    elif choice == "5":
        mode = "lr"
        catalog_dir = Path("data/l&r_produktkatalog")
        prompt_approach = "two_stage_lr"
        is_two_stage = True
        print("-> Modus: 2-Stage CoT mit L&R Produktkatalog ausgewählt.")
    elif choice == "6":
        mode = "standard"
        catalog_dir = Path("data/produktkatalog")
        prompt_approach = "two_stage"
        is_two_stage = True
        print("-> Modus: 2-Stage CoT mit Generischem Produktkatalog ausgewählt.")
    else:
        mode = "lr"
        catalog_dir = Path("data/l&r_produktkatalog")
        prompt_approach = "zero_shot_lr"
        print("-> Modus: Zero-Shot mit L&R Produktkatalog ausgewählt.")

    # 1. Benötigte Ordner erstellen
    RUNS_DIR.mkdir(exist_ok=True)
    if not IMAGE_DIR.exists():
        IMAGE_DIR.mkdir()
        print(f"Ordner '{IMAGE_DIR}' wurde erstellt!")
        print("Bitte füge deine Wundbilder (JPG, PNG) dort ein und starte das Skript erneut.")
        return

    # Prüfen, ob Bilder im Ordner sind
    image_files = [f for f in IMAGE_DIR.glob("*.*") if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]]
    if not image_files:
        print(f"Keine Bilder im Ordner '{IMAGE_DIR}' gefunden. Bitte füge welche ein.")
        return

    def natural_sort_key(path):
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', path.name)]

    image_files = sorted(image_files, key=natural_sort_key)

    # 2. Produktkatalog laden
    if mode == "lr":
        catalog_files = [
            catalog_dir / "lr0_produktkatalog.md",
            catalog_dir / "lr1_produktkatalog.md",
            catalog_dir / "lr2_produktkatalog.md",
            catalog_dir / "lr3_produktkatalog.md"
        ]
        missing = [f for f in catalog_files if not f.exists()]
        if missing:
            print(f"Folgende Katalogdateien wurden nicht gefunden: {[f.name for f in missing]}")
            return
            
        print("Lade L&R Kataloge und kombiniere sie...")
        catalog_texts = []
        for cf in catalog_files:
            print(f" - Lese {cf.name}...")
            catalog_texts.append(f"### Katalogteil: {cf.name}\n\n" + load_catalog(str(cf)))
        catalog_text = "\n\n---\n\n".join(catalog_texts)
    else:
        catalog_md_file = catalog_dir / "AllgemeineProdukte.md"
        if not catalog_md_file.exists():
            print(f"Katalogdatei nicht gefunden: {catalog_md_file}")
            return
            
        print("Lade Katalog...")
        print(f" - Lese {catalog_md_file.name}...")
        catalog_text = f"### Katalogteil: {catalog_md_file.name}\n\n" + load_catalog(str(catalog_md_file))
    
    # 3. Verfügbare Bilder anzeigen und Abfrage starten
    print("\nFolgende Bilder sind im Ordner verfügbar (nummeriert nach natürlicher Sortierung):")
    for idx, img in enumerate(image_files, 1):
        print(f"  {idx:02d}: {img.stem}  (Datei: {img.name})")
        
    choice = input("\nWelches Bild/Spanne möchtest du analysieren? (z.B. '1-5', 'all', 'Bild3' oder '3'): ").strip()
    
    # 4. Gewählte(s) Bild(er) finden
    selected_images = []
    
    # Versuche Spanne wie "1-5" oder "01-05" zu parsen
    range_match = re.match(r"^(\d+)\s*-\s*(\d+)$", choice)
    
    if choice.lower() == "all":
        selected_images = image_files
    elif range_match:
        start_idx = int(range_match.group(1))
        end_idx = int(range_match.group(2))
        if 1 <= start_idx <= end_idx <= len(image_files):
            selected_images = image_files[start_idx - 1:end_idx]
        else:
            print(f"❌ Ungültiger Bereich! Bitte Wertzahlen zwischen 1 und {len(image_files)} eingeben.")
            return
    elif choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(image_files):
            selected_images = [image_files[idx - 1]]
        else:
            print(f"❌ Ungültige Bildnummer! Bitte eine Zahl zwischen 1 und {len(image_files)} eingeben.")
            return
    else:
        for img in image_files:
            if img.stem.lower() == choice.lower() or img.name.lower() == choice.lower():
                selected_images.append(img)
                break
                
    if not selected_images:
        print(f"❌ Bild/Spanne '{choice}' nicht gefunden.")
        return

    # Few-Shot Beispiele laden falls Few-Shot gewählt
    few_shot_examples = []
    if is_few_shot:
        few_shot_examples = get_default_few_shot_examples(mode)

    print(f"\nStarte Analyse für {len(selected_images)} Bild(er) im Modus '{prompt_approach}' ...")
    
    for img_idx, selected_image in enumerate(selected_images, 1):
        print(f"\n============================================================")
        print(f"Verarbeite Bild {img_idx}/{len(selected_images)}: {selected_image.name}")
        print(f"============================================================")
        
        # In Few-Shot Modus: Beispielbilder überspringen, da sie als Kontext dienen
        if is_few_shot:
            m = re.search(r"\d+", selected_image.stem)
            img_id_norm = f"wunde_{int(m.group()):02d}" if m else selected_image.stem.lower()
            if img_id_norm in DEFAULT_FEW_SHOT_EXAMPLE_IDS:
                print(f"⏩ Überspringe '{selected_image.name}' ({img_id_norm}), da dieses Bild als Few-Shot Kontextbeispiel verwendet wird.")
                continue

        try:
            # KI aufrufen
            if is_two_stage:
                result = analyze_wound_image_two_stage(
                    image_path=str(selected_image),
                    catalog=catalog_text,
                    mode=mode
                )
            elif is_few_shot:
                result = analyze_wound_image_few_shot(
                    image_path=str(selected_image),
                    catalog=catalog_text,
                    examples=few_shot_examples,
                    mode=mode
                )
            else:
                result = analyze_wound_image(
                    image_path=str(selected_image),
                    catalog=catalog_text,
                    mode=mode
                )
            
            raw_response = result["raw_response"]
            parsed_output = result["response"]
            json_valid = result["metadata"].get("json_valid", True)
            
            errors = []
            if not json_valid:
                errors.append("Fehler beim Parsen der JSON-Antwort.")
                
            meta_info = {
                "model_version": MODEL,
                "prompt_hash": compute_hash(result.get("system_prompt", get_system_prompt(mode))),
                "prompt_version": "v1.0",
                "temperature": TEMPERATURE,
                "catalog_hash": compute_hash(catalog_text)
            }
            if is_two_stage:
                meta_info["stage_1"] = result["metadata"]["stage_1"]
                meta_info["stage_2"] = result["metadata"]["stage_2"]
            
            run_path = save_run(
                model=MODEL,
                prompt_approach=prompt_approach,
                image_id=selected_image.stem,
                raw_response=raw_response,
                parsed_output=parsed_output,
                json_valid=json_valid,
                parse_errors=errors,
                latency_seconds=result["metadata"].get("elapsed_seconds", 0.0),
                meta_info=meta_info,
                base_dir=RUNS_DIR,
                prompt_tokens=result["metadata"].get("prompt_tokens"),
                completion_tokens=result["metadata"].get("completion_tokens"),
                total_tokens=result["metadata"].get("total_tokens"),
                cached_tokens=result["metadata"].get("cached_tokens"),
                uncached_tokens=result["metadata"].get("uncached_tokens"),
                reasoning_tokens=result["metadata"].get("reasoning_tokens"),
                system_prompt=result.get("system_prompt"),
                user_prompt=result.get("user_prompt"),
                catalog_text=catalog_text
            )
            
            print(f"✅ Analyse erfolgreich! Gespeichert unter: {run_path}")
            
        except Exception as e:
            print(f"❌ Fehler bei der Analyse von Bild {selected_image.name}: {e}")

if __name__ == "__main__":
    main()
