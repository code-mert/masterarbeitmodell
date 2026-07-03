import json
# pyrefly: ignore [missing-import]
import pytest
from pathlib import Path
from core.storage import (
    compute_hash,
    get_run_dir,
    get_next_run_number,
    save_run,
    load_runs,
    load_meta,
    list_image_ids,
)


@pytest.fixture
def meta_info():
    return {
        "model_version": "gpt-4o-2024-08-06",
        "prompt_hash": compute_hash("dummy_prompt"),
        "prompt_version": "v1.2",
        "temperature": 1.0,
        "catalog_hash": compute_hash("dummy_catalog"),
    }


def test_compute_hash():
    h1 = compute_hash("test")
    h2 = compute_hash("test")
    h3 = compute_hash("other")
    assert h1 == h2
    assert h1 != h3
    assert len(h1) == 16


def test_get_run_dir(tmp_path):
    rd = get_run_dir("gpt-4o", "zero_shot", "img1", base_dir=tmp_path)
    assert rd == tmp_path / "gpt-4o" / "zero_shot" / "img1"


def test_save_run_creates_meta(tmp_path, meta_info):
    run_path = save_run(
        model="gpt-4o",
        prompt_approach="zero_shot",
        image_id="img1",
        raw_response='{"test": 123}',
        parsed_output={"test": 123},
        json_valid=True,
        parse_errors=[],
        latency_seconds=1.5,
        meta_info=meta_info,
        base_dir=tmp_path,
    )
    
    assert run_path.name == "run_001.json"
    assert run_path.exists()
    
    rd = run_path.parent
    meta_path = rd / "_meta.json"
    assert meta_path.exists()
    
    with open(meta_path, "r", encoding="utf-8") as f:
        meta_data = json.load(f)
        
    assert meta_data["n_runs_completed"] == 1
    assert meta_data["model_version"] == meta_info["model_version"]
    assert meta_data["prompt_hash"] == meta_info["prompt_hash"]
    assert "created_at" in meta_data
    
    # Check no tmp files
    tmp_files = list(rd.glob("*.tmp"))
    assert len(tmp_files) == 0


def test_save_two_runs(tmp_path, meta_info):
    save_run("gpt-4o", "zs", "img1", "{}", {}, True, [], 1.0, meta_info, tmp_path)
    run_path2 = save_run("gpt-4o", "zs", "img1", "{}", {}, True, [], 1.0, meta_info, tmp_path)
    
    assert run_path2.name == "run_002.json"
    
    rd = run_path2.parent
    with open(rd / "_meta.json", "r", encoding="utf-8") as f:
        meta_data = json.load(f)
        
    assert meta_data["n_runs_completed"] == 2
    assert (rd / "run_001.json").exists()
    assert (rd / "run_002.json").exists()


def test_get_next_run_number_with_gaps(tmp_path):
    rd = tmp_path / "test_gaps"
    rd.mkdir(parents=True)
    (rd / "run_001.json").touch()
    (rd / "run_003.json").touch()
    (rd / "run_xyz.json").touch()  # invalid name, should be ignored
    
    assert get_next_run_number(rd) == 4


def test_save_run_raises_value_error_on_inconsistent_meta(tmp_path, meta_info):
    save_run("gpt-4o", "zs", "img1", "{}", {}, True, [], 1.0, meta_info, tmp_path)
    
    # Mutate meta info
    meta_info_bad = meta_info.copy()
    meta_info_bad["prompt_hash"] = "different_hash"
    
    with pytest.raises(ValueError) as exc:
        save_run("gpt-4o", "zs", "img1", "{}", {}, True, [], 1.0, meta_info_bad, tmp_path)
        
    assert "prompt_hash" in str(exc.value)


def test_load_runs_empty(tmp_path):
    runs = load_runs("gpt-4o", "zs", "img1", tmp_path)
    assert runs == []


def test_load_runs_sorted(tmp_path, meta_info):
    # Save a few runs
    save_run("gpt-4o", "zs", "img1", "A", None, False, [], 1.0, meta_info, tmp_path)
    save_run("gpt-4o", "zs", "img1", "B", None, False, [], 1.0, meta_info, tmp_path)
    save_run("gpt-4o", "zs", "img1", "C", None, False, [], 1.0, meta_info, tmp_path)
    
    # We purposefully rename run_002.json to simulate out of order file reading via glob
    rd = get_run_dir("gpt-4o", "zs", "img1", tmp_path)
    (rd / "run_002.json").replace(rd / "run_004.json")
    
    runs = load_runs("gpt-4o", "zs", "img1", tmp_path)
    # The IDs are embedded in the run data
    assert len(runs) == 3
    assert runs[0]["run_id"] == 1
    assert runs[1]["run_id"] == 2  # The ID inside the JSON is still 2! Even if file was renamed, we sort by run_id inside JSON, wait.
    assert runs[2]["run_id"] == 3


def test_list_image_ids(tmp_path, meta_info):
    save_run("gpt-4o", "zs", "img1", "{}", {}, True, [], 1.0, meta_info, tmp_path)
    save_run("gpt-4o", "zs", "img2", "{}", {}, True, [], 1.0, meta_info, tmp_path)
    
    images = list_image_ids("gpt-4o", "zs", tmp_path)
    assert images == ["img1", "img2"]
