"""
run_befund_experiment.py

Experiment "Bild + Befund" (Two-Stage L&R):
Stage 2 wird erneut ausgeführt – mit der gespeicherten Stage-1-Wundbeschreibung der KI
aus runs/gpt-5/two_stage_lr. Exsudat und Infektion von Experte 2 werden in die Stage-1-Beschreibung
übernommen (Exsudat überschrieben, Infektion ergänzt) und zusätzlich als verifizierte Befunde
gekennzeichnet. Stage 1 wird NICHT neu ausgeführt.

Bedingungen:
  befund     (Standard)  Stage 1 der KI + Exsudat/Infektion von Experte 2  -> runs/gpt-5/two_stage_lr_befund
  befund     (--experte 1) Stage 1 der KI + Exsudat/Infektion von Experte 1 -> runs/gpt-5/two_stage_lr_befund_e1
  kontrolle  (--kontrolle) Stage 1 der KI unverändert, ohne Befunde        -> runs/gpt-5/two_stage_lr_kontrolle

Usage:
    python run_befund_experiment.py 1-2              # Testlauf Bild1 und Bild2
    python run_befund_experiment.py all              # alle 60 Bilder
    python run_befund_experiment.py all --kontrolle  # Kontrollbedingung
    python run_befund_experiment.py 1 --dry-run      # nur Prompt erzeugen, kein API-Aufruf

Bereits vorhandene Ergebnisse werden übersprungen (Wiederaufnahme ohne doppelte Kosten).
"""

import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from prompts.zero_shot_prompt import load_catalog
from prompts.two_stage_prompt import (
    MODEL, TEMPERATURE, MAX_TOKENS, REASONING_EFFORT, STAGE1_KEYS_LR,
    get_stage2_system_prompt, build_stage2_user_prompt,
)
from core.client import call_llm_api
from core.storage import save_run, compute_hash, _atomic_write_json

load_dotenv()

IMAGE_DIR = Path("data/wundbilder")
CATALOG_DIR = Path("data/l&r_produktkatalog")
RUNS_DIR = Path("runs")
STAGE1_SOURCE_DIR = RUNS_DIR / MODEL / "two_stage_lr"
EXPERT_GT_PATHS = {
    1: Path("data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv"),
    2: Path("data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv"),
}


def load_lr_catalog() -> str:
    """Lädt den L&R-Katalog exakt wie run_experiment.py (lr0–lr3, gleiche Trenner)."""
    catalog_files = [CATALOG_DIR / f"lr{i}_produktkatalog.md" for i in range(4)]
    catalog_texts = [f"### Katalogteil: {cf.name}\n\n" + load_catalog(str(cf)) for cf in catalog_files]
    return "\n\n---\n\n".join(catalog_texts)


def load_stage1_output(bild_nr: int) -> tuple[dict, str]:
    """
    Lädt die Stage-1-Beschreibung aus dem Two-Stage-Lauf mit der höchsten run_id
    (derselbe Lauf, der auch in two_stage_lr_raw.csv eingeflossen ist).
    """
    run_dir = STAGE1_SOURCE_DIR / f"Bild{bild_nr}"
    run_files = sorted(run_dir.glob("run_*.json"), key=lambda p: int(p.stem.split("_")[1]))
    if not run_files:
        raise FileNotFoundError(f"Kein Two-Stage-Lauf gefunden in {run_dir}")
    source = run_files[-1]
    with open(source, "r", encoding="utf-8") as f:
        parsed = json.load(f)["parsed_output"]
    stage1 = {k: parsed[k] for k in STAGE1_KEYS_LR if k in parsed}
    return stage1, str(source.as_posix())


def insert_findings_into_stage1(stage1: dict, findings: dict) -> dict:
    """
    Übernimmt die Experten-Befunde in die Stage-1-Beschreibung:
    exsudat_menge wird überschrieben, infektion_vorhanden direkt dahinter eingefügt
    (war bisher kein Stage-1-Feld, sondern wurde in Stage 2 entschieden).
    """
    result = {}
    for key, value in stage1.items():
        result[key] = findings.get(key, value) if key == "exsudat_menge" else value
        if key == "exsudat_menge" and "infektion_vorhanden" in findings:
            result["infektion_vorhanden"] = findings["infektion_vorhanden"]
    if "infektion_vorhanden" in findings and "infektion_vorhanden" not in result:
        result["infektion_vorhanden"] = findings["infektion_vorhanden"]
    return result


def format_exsudat(val) -> str | None:
    """'Leicht, Mäßig' -> 'Leicht bis Mäßig'. Enthaltung/leer -> None."""
    if pd.isna(val):
        return None
    s = str(val).strip()
    if not s or "enthaltung" in s.lower() or "keine angabe" in s.lower():
        return None
    parts = [p.strip() for p in s.split(",") if p.strip()]
    return " bis ".join(parts)


def format_infektion(val) -> str | None:
    """'Ja'/'Nein' -> 'ja'/'nein' (wie im Schema). Leer -> None."""
    if pd.isna(val):
        return None
    s = str(val).strip().lower()
    return s if s in ("ja", "nein") else None


def load_expert_findings(gt_path: Path) -> dict:
    df = pd.read_csv(gt_path, sep=";")
    findings = {}
    for _, row in df.iterrows():
        m = re.search(r"\d+", str(row["image_id"]))
        if not m:
            continue
        findings[int(m.group())] = {
            "exsudat_menge": format_exsudat(row.get("exsudat")),
            "infektion_vorhanden": format_infektion(row.get("infektion")),
        }
    return findings


def parse_selection(choice: str, n_max: int = 60) -> list[int]:
    if choice.lower() == "all":
        return list(range(1, n_max + 1))
    m = re.match(r"^(\d+)\s*-\s*(\d+)$", choice)
    if m:
        return list(range(int(m.group(1)), int(m.group(2)) + 1))
    if choice.isdigit():
        return [int(choice)]
    raise ValueError(f"Ungültige Auswahl '{choice}'. Erlaubt: 'all', '1-5', '3'.")


def main():
    parser = argparse.ArgumentParser(description="Experiment Bild + Befund (Two-Stage L&R, nur Stage 2)")
    parser.add_argument("auswahl", help="'all', Bereich wie '1-5' oder einzelne Nummer")
    parser.add_argument("--kontrolle", action="store_true", help="Kontrollbedingung ohne Befunde")
    parser.add_argument("--dry-run", action="store_true", help="Nur Prompt erzeugen und ausgeben, kein API-Aufruf")
    parser.add_argument("--experte", type=int, choices=[1, 2], default=2,
                        help="Von welchem Experten Exsudat/Infektion übernommen werden (Standard: 2)")
    args = parser.parse_args()

    condition = "kontrolle" if args.kontrolle else "befund"
    expert_label = f"Experte {args.experte}"
    if condition == "kontrolle":
        prompt_approach = "two_stage_lr_kontrolle"
    elif args.experte == 2:
        prompt_approach = "two_stage_lr_befund"      # bisheriger Ordner, unverändert
    else:
        prompt_approach = f"two_stage_lr_befund_e{args.experte}"
    bilder = parse_selection(args.auswahl)

    catalog_text = load_lr_catalog()
    expert_findings = load_expert_findings(EXPERT_GT_PATHS[args.experte])
    system_prompt = get_stage2_system_prompt("lr")

    print(f"Bedingung: {condition}  ->  {RUNS_DIR / MODEL / prompt_approach}")
    print(f"Bilder: {bilder[0]}–{bilder[-1]} ({len(bilder)} Stück)\n")

    for bild_nr in bilder:
        image_id = f"Bild{bild_nr}"
        out_dir = RUNS_DIR / MODEL / prompt_approach / image_id
        if not args.dry_run and any(out_dir.glob("run_*.json")):
            print(f"⏩ {image_id}: bereits vorhanden, übersprungen.")
            continue

        image_path = IMAGE_DIR / f"{image_id}.jpg"
        if not image_path.exists():
            print(f"❌ {image_id}: Bilddatei {image_path} nicht gefunden.")
            continue

        stage1, stage1_source = load_stage1_output(bild_nr)
        stage1_original_exsudat = stage1.get("exsudat_menge")

        verified_findings = None
        injected = {}
        if condition == "befund":
            f = expert_findings.get(bild_nr, {})
            injected = {k: v for k, v in f.items() if v is not None}
            stage1 = insert_findings_into_stage1(stage1, injected)
            verified_findings = injected or None

        user_prompt = build_stage2_user_prompt(catalog_text, stage1, "lr", verified_findings=verified_findings)

        if args.dry_run:
            print(f"===== {image_id} | Befund: {injected} =====")
            print(user_prompt)
            continue

        try:
            res = call_llm_api(
                model=MODEL,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                image_path=str(image_path),
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                reasoning_effort=REASONING_EFFORT,
                prompt_cache_key="stage2_lr",
            )
        except Exception as e:
            print(f"❌ {image_id}: API-Fehler: {e}")
            continue

        stage2 = res.get("response") or {}
        if isinstance(stage2, dict) and isinstance(stage2.get("properties"), dict):
            stage2 = stage2["properties"]

        combined = dict(stage1)
        combined.update(stage2)
        meta = res["metadata"]
        json_valid = bool(res.get("response"))

        run_path = save_run(
            model=MODEL,
            prompt_approach=prompt_approach,
            image_id=image_id,
            raw_response=res.get("raw_response", ""),
            parsed_output=combined,
            json_valid=json_valid,
            parse_errors=[] if json_valid else ["Fehler beim Parsen der JSON-Antwort."],
            latency_seconds=meta.get("elapsed_seconds", 0.0),
            meta_info={
                "model_version": MODEL,
                "prompt_hash": compute_hash(system_prompt),
                "prompt_version": f"v1.0-{condition}",
                "temperature": TEMPERATURE,
                "catalog_hash": compute_hash(catalog_text),
            },
            base_dir=RUNS_DIR,
            prompt_tokens=meta.get("prompt_tokens"),
            completion_tokens=meta.get("completion_tokens"),
            total_tokens=meta.get("total_tokens"),
            cached_tokens=meta.get("cached_tokens"),
            uncached_tokens=meta.get("uncached_tokens"),
            reasoning_tokens=meta.get("reasoning_tokens"),
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            catalog_text=catalog_text,
        )

        # Experiment-Infos ergänzen (save_run speichert keine zusätzlichen Metadaten)
        with open(run_path, "r", encoding="utf-8") as f:
            run_data = json.load(f)
        run_data["experiment"] = {
            "bedingung": condition,
            "stage1_quelle": stage1_source,
            "befund_quelle": expert_label if condition == "befund" else None,
            "eingesetzte_befunde": injected,
            "fehlende_befunde": [k for k in ("exsudat_menge", "infektion_vorhanden") if k not in injected] if condition == "befund" else [],
            "stage1_exsudat_original": stage1_original_exsudat,
            "infektion_ki_output": stage2.get("infektion_vorhanden"),
            "user_prompt_hash": compute_hash(user_prompt),
        }
        _atomic_write_json(run_path, run_data)

        cost = run_data.get("usage", {}).get("costs", {}).get("total_usd")
        print(f"✅ {image_id}: {stage2.get('praeferenz_wundauflage')} | Befund {injected} | {cost} USD")


if __name__ == "__main__":
    sys.exit(main())
