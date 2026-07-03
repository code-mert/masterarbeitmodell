import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def compute_hash(content: str) -> str:
    """Berechnet den SHA-256 Hash eines Strings und gibt die ersten 16 Zeichen zurück."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def get_run_dir(
    model: str, prompt_approach: str, image_id: str, base_dir: Path = Path("runs")
) -> Path:
    """Konstruiert den Pfad zum Run-Verzeichnis für ein bestimmtes Bild."""
    return base_dir / model / prompt_approach / image_id


def get_next_run_number(run_dir: Path) -> int:
    """
    Ermittelt die nächste freie Run-Nummer im Verzeichnis.
    Sucht nach Dateien im Format run_NNN.json und gibt die höchste gefundene Nummer + 1 zurück.
    Ignoriert Lücken (z.B. wenn 1 und 3 existieren, wird 4 zurückgegeben).
    Gibt 1 zurück, wenn keine Runs vorhanden sind oder das Verzeichnis nicht existiert.
    """
    if not run_dir.exists():
        return 1

    max_num = 0
    for p in run_dir.glob("run_*.json"):
        name = p.stem  # z.B. "run_001"
        try:
            num = int(name.split("_")[1])
            if num > max_num:
                max_num = num
        except (IndexError, ValueError):
            continue

    return max_num + 1


def _atomic_write_json(file_path: Path, data: Any) -> None:
    """Schreibt JSON-Daten atomar über eine .tmp Datei."""
    tmp_path = file_path.with_suffix(".tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        # Atomares Umbenennen (überschreibt Zieldatei falls vorhanden)
        tmp_path.replace(file_path)
    finally:
        # Sicherstellen, dass .tmp entfernt wird, falls etwas schiefgeht
        if tmp_path.exists():
            tmp_path.unlink()


def save_run(
    model: str,
    prompt_approach: str,
    image_id: str,
    raw_response: str,
    parsed_output: dict | None,
    json_valid: bool,
    parse_errors: list[str],
    latency_seconds: float,
    meta_info: dict,
    base_dir: Path = Path("runs"),
    prompt_tokens: int | None = None,
    completion_tokens: int | None = None,
    total_tokens: int | None = None,
    cached_tokens: int | None = None,
    uncached_tokens: int | None = None,
    reasoning_tokens: int | None = None,
    system_prompt: str | None = None,
    user_prompt: str | None = None,
    catalog_text: str | None = None,
) -> Path:
    """
    Speichert einen neuen Run und aktualisiert/erstellt die _meta.json.
    
    `meta_info` muss folgende Keys enthalten:
      - model_version
      - prompt_hash
      - prompt_version
      - temperature
      - catalog_hash
    """
    run_dir = get_run_dir(model, prompt_approach, image_id, base_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    parent_dir = run_dir.parent
    parent_dir.mkdir(parents=True, exist_ok=True)

    if system_prompt is not None:
        sys_prompt_path = parent_dir / "system_prompt.txt"
        if not sys_prompt_path.exists():
            with open(sys_prompt_path, "w", encoding="utf-8") as f:
                f.write(system_prompt)

    if user_prompt is not None:
        user_prompt_path = parent_dir / "user_prompt.txt"
        if not user_prompt_path.exists():
            with open(user_prompt_path, "w", encoding="utf-8") as f:
                f.write(user_prompt)

    if catalog_text is not None:
        cat_path = parent_dir / "catalog.md"
        if not cat_path.exists():
            with open(cat_path, "w", encoding="utf-8") as f:
                f.write(catalog_text)
    
    meta_path = run_dir / "_meta.json"
    now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    CACHED_RATES = {
        "gpt-4o": 0.5,
        "gpt-4o-2024-08-06": 0.5,
        "gpt-4-turbo": 0.5,
        "gpt-5": 0.1,
    }
    DEFAULT_CACHED_RATE = 0.1

    rates = {
        "gpt-4o": (2.5, 10.0),
        "gpt-4o-2024-08-06": (2.5, 10.0),
        "gpt-4-turbo": (10.0, 30.0),
        "gpt-5": (5.0, 15.0),
    }.get(model, (5.0, 15.0))

    cached_rate = CACHED_RATES.get(model, DEFAULT_CACHED_RATE)
    
    run_prompt_tokens = prompt_tokens or 0
    run_cached = cached_tokens or 0
    run_uncached = uncached_tokens or (run_prompt_tokens - run_cached)
    if run_uncached < 0:
        run_uncached = max(0, run_prompt_tokens - run_cached)
    run_completion = completion_tokens or 0
    
    cost_input = (run_uncached * rates[0] + run_cached * rates[0] * cached_rate) / 1_000_000
    cost_output = (run_completion * rates[1]) / 1_000_000
    cost_total = cost_input + cost_output
    
    # 1. _meta.json behandeln
    if not meta_path.exists():
        meta_data = {
            "image_id": image_id,
            "model": model,
            "model_version": meta_info["model_version"],
            "prompt_approach": prompt_approach,
            "prompt_hash": meta_info["prompt_hash"],
            "prompt_version": meta_info["prompt_version"],
            "temperature": meta_info["temperature"],
            "catalog_hash": meta_info["catalog_hash"],
            "created_at": now_iso,
            "n_runs_completed": 1,
            "sum_cached_tokens": run_cached,
            "sum_uncached_tokens": run_uncached,
            "cache_hit_rate": round(run_cached / run_prompt_tokens, 4) if run_prompt_tokens > 0 else 0.0,
            "total_usage": {
                "prompt_tokens": run_prompt_tokens,
                "completion_tokens": run_completion,
                "total_tokens": total_tokens or (run_prompt_tokens + run_completion),
                "cached_tokens": run_cached,
                "uncached_tokens": run_uncached,
                "reasoning_tokens": reasoning_tokens or 0,
                "total_cost_usd": round(cost_total, 6),
            }
        }
    else:
        with open(meta_path, "r", encoding="utf-8") as f:
            meta_data = json.load(f)
            
        # Konsistenzprüfung
        checks = ["prompt_hash", "catalog_hash", "model_version", "temperature", "prompt_version"]
        for key in checks:
            if meta_data.get(key) != meta_info[key]:
                raise ValueError(
                    f"Diskrepanz in _meta.json: {key} hat sich geändert "
                    f"(alt: {meta_data.get(key)}, neu: {meta_info[key]})."
                )
                
        meta_data["n_runs_completed"] += 1
        
        if "sum_cached_tokens" not in meta_data:
            meta_data["sum_cached_tokens"] = 0
        if "sum_uncached_tokens" not in meta_data:
            meta_data["sum_uncached_tokens"] = meta_data.get("total_usage", {}).get("prompt_tokens", 0)

        meta_data["sum_cached_tokens"] += run_cached
        meta_data["sum_uncached_tokens"] += run_uncached
        
        total_prompt_tokens = meta_data.get("total_usage", {}).get("prompt_tokens", 0) + run_prompt_tokens
        if total_prompt_tokens > 0:
            meta_data["cache_hit_rate"] = round(meta_data["sum_cached_tokens"] / total_prompt_tokens, 4)
        else:
            meta_data["cache_hit_rate"] = 0.0

        if "total_usage" not in meta_data:
            meta_data["total_usage"] = {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "total_cost_usd": 0.0,
            }
            
        meta_data["total_usage"]["prompt_tokens"] += run_prompt_tokens
        meta_data["total_usage"]["completion_tokens"] += run_completion
        meta_data["total_usage"]["total_tokens"] += total_tokens or (run_prompt_tokens + run_completion)
        
        if "cached_tokens" not in meta_data["total_usage"]:
            meta_data["total_usage"]["cached_tokens"] = 0
        if "uncached_tokens" not in meta_data["total_usage"]:
            meta_data["total_usage"]["uncached_tokens"] = meta_data["total_usage"]["prompt_tokens"] - run_prompt_tokens
            
        meta_data["total_usage"]["cached_tokens"] += run_cached
        meta_data["total_usage"]["uncached_tokens"] += run_uncached
        
        if "reasoning_tokens" not in meta_data["total_usage"]:
            meta_data["total_usage"]["reasoning_tokens"] = 0
        meta_data["total_usage"]["reasoning_tokens"] += reasoning_tokens or 0
        
        meta_data["total_usage"]["total_cost_usd"] = round(meta_data["total_usage"]["total_cost_usd"] + cost_total, 6)
        
    # Atomar schreiben
    _atomic_write_json(meta_path, meta_data)

    # 2. Run-Datei speichern
    run_id = get_next_run_number(run_dir)
    run_filename = f"run_{run_id:03d}.json"
    run_path = run_dir / run_filename
    
    run_data = {
        "run_id": run_id,
        "image_id": image_id,
        "timestamp": now_iso,
        "latency_seconds": latency_seconds,
        "raw_response": raw_response,
        "parsed_output": parsed_output,
        "json_valid": json_valid,
        "parse_errors": parse_errors,
    }
    
    if prompt_tokens is not None and completion_tokens is not None:
        run_data["usage"] = {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens or (prompt_tokens + completion_tokens),
            "cached_tokens": run_cached,
            "uncached_tokens": run_uncached,
            "reasoning_tokens": reasoning_tokens or 0,
            "costs": {
                "input_usd": round(cost_input, 6),
                "output_usd": round(cost_output, 6),
                "total_usd": round(cost_total, 6),
            }
        }
        
    _atomic_write_json(run_path, run_data)
    return run_path


def load_runs(
    model: str, prompt_approach: str, image_id: str, base_dir: Path = Path("runs")
) -> list[dict]:
    """Lädt alle Runs für ein Bild und gibt sie sortiert nach run_id zurück."""
    run_dir = get_run_dir(model, prompt_approach, image_id, base_dir)
    if not run_dir.exists():
        return []

    runs = []
    for p in run_dir.glob("run_*.json"):
        try:
            with open(p, "r", encoding="utf-8") as f:
                run_data = json.load(f)
                runs.append(run_data)
        except (json.JSONDecodeError, OSError):
            continue
            
    runs.sort(key=lambda x: x.get("run_id", 0))
    return runs


def load_meta(
    model: str, prompt_approach: str, image_id: str, base_dir: Path = Path("runs")
) -> dict | None:
    """Lädt die Metadaten (_meta.json) für ein Bild."""
    meta_path = get_run_dir(model, prompt_approach, image_id, base_dir) / "_meta.json"
    if not meta_path.exists():
        return None
    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def list_image_ids(
    model: str, prompt_approach: str, base_dir: Path = Path("runs")
) -> list[str]:
    """Listet alle image_ids unter base_dir / model / prompt_approach."""
    parent_dir = base_dir / model / prompt_approach
    if not parent_dir.exists() or not parent_dir.is_dir():
        return []
        
    return sorted([d.name for d in parent_dir.iterdir() if d.is_dir()])
