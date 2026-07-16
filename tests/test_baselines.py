import pytest
import os
import random
from pathlib import Path

from eval.baselines import (
    parse_markdown_h3_headers,
    load_lr_catalog_pools,
    calculate_qwk,
    parse_exsudat_level,
    generate_majority_predictions_loo,
    generate_random_prediction_single_run,
    evaluate_single_dataset_pair,
    BaselineEvaluator,
    evaluate_baselines_dual
)
from eval.loaders import load_ground_truth, load_llm_outputs

CATALOG_DIR = "data/l&r_produktkatalog"
GT1_PATH = "data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv"
GT2_PATH = "data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv"
LLM_PATH = "data/llm_outputs/zero_shot_lr/zero_shot_lr_normalised.csv"


def test_catalog_pools_loading():
    pools = load_lr_catalog_pools(CATALOG_DIR)
    assert "debridement" in pools
    assert "primaerverband" in pools
    assert "sekundaerverband" in pools
    assert "kompression" in pools

    assert len(pools["debridement"]) == 6
    assert len(pools["primaerverband"]) == 32
    assert len(pools["sekundaerverband"]) == 12
    assert len(pools["kompression"]) == 37

    assert "Debrisoft Pad" in pools["debridement"]
    assert "Suprasorb CNP" in pools["primaerverband"]
    assert "Curapor" in pools["sekundaerverband"]
    assert "Rosidal K" in pools["kompression"]


def test_qwk_metric():
    # Perfect agreement
    y_true = [0, 1, 2, 3, 4]
    y_pred = [0, 1, 2, 3, 4]
    assert calculate_qwk(y_true, y_pred) == 1.0

    # Slight disagreement
    y_pred_slight = [0, 1, 2, 2, 4]
    qwk_val = calculate_qwk(y_true, y_pred_slight)
    assert 0.8 < qwk_val < 1.0

    # Parsing levels
    assert parse_exsudat_level("Mäßig") == 2
    assert parse_exsudat_level("Leicht") == 1
    assert parse_exsudat_level("Keine") == 0
    assert parse_exsudat_level("Sehr stark") == 4
    assert parse_exsudat_level("Unbekannt") is None


def test_leave_one_out_majority():
    # Synthetic GT records to test LOO isolation
    synthetic_gt = {
        "wunde_01": {
            "debridement": ["UniqueTo01"],
            "praeferenz_produkt": ["ProdA"],
            "alternative_produkt": [],
            "ergaenzende_produkte_praeferenz": [],
            "ergaenzende_produkte_alternativ": [],
            "kompression_produkte": [],
            "lokalisation": "Arm",
            "exsudat": "Mäßig"
        },
        "wunde_02": {
            "debridement": ["ProdCommon"],
            "praeferenz_produkt": ["ProdA"],
            "alternative_produkt": [],
            "ergaenzende_produkte_praeferenz": [],
            "ergaenzende_produkte_alternativ": [],
            "kompression_produkte": [],
            "lokalisation": "Bein",
            "exsudat": "Stark"
        },
        "wunde_03": {
            "debridement": ["ProdCommon"],
            "praeferenz_produkt": ["ProdB"],
            "alternative_produkt": [],
            "ergaenzende_produkte_praeferenz": [],
            "ergaenzende_produkte_alternativ": [],
            "kompression_produkte": [],
            "lokalisation": "Bein",
            "exsudat": "Stark"
        }
    }

    maj_preds = generate_majority_predictions_loo(synthetic_gt)
    
    # For wunde_01 (k=1 for debridement), training set is wunde_02 and wunde_03.
    # Most common debridement in train set is 'ProdCommon'. 'UniqueTo01' MUST NOT appear!
    assert maj_preds["wunde_01"]["debridement_methode"] == ["ProdCommon"]
    # Most common lokalisation in train set for wunde_01 is 'Bein' (from 02 and 03)
    assert maj_preds["wunde_01"]["lokalisation"] == "Bein"


def test_oracle_k_set_sizes():
    gt1 = load_ground_truth(GT1_PATH)
    maj_preds = generate_majority_predictions_loo(gt1)
    
    for img_id, rec in gt1.items():
        maj_rec = maj_preds[img_id]
        
        # Check set sizes match GT set sizes (Oracle-k)
        gt_deb = [x for x in rec.get("debridement", []) if not str(x).startswith("Nicht")]
        assert len(maj_rec["debridement_methode"]) == len(gt_deb)

        gt_prim_p = [x for x in rec.get("praeferenz_produkt", []) if not str(x).startswith("Nicht")]
        assert len(maj_rec["praeferenz_wundauflage"]) == len(gt_prim_p)


def test_random_baseline_reproducibility():
    evaluator = BaselineEvaluator(gt1_path=GT1_PATH, gt2_path=GT2_PATH, catalog_dir=CATALOG_DIR)
    
    res1 = evaluator.run_evaluation(LLM_PATH, n_runs=100, seed=42)
    res2 = evaluator.run_evaluation(LLM_PATH, n_runs=100, seed=42)
    
    for f in ["debridement", "primaerverband", "sekundaerverband", "kompression"]:
        assert res1["rand_summary1"][f]["mean"] == res2["rand_summary1"][f]["mean"]
        assert res1["rand_summary1"][f]["ci_low"] == res2["rand_summary1"][f]["ci_low"]
        assert res1["rand_summary1"][f]["ci_high"] == res2["rand_summary1"][f]["ci_high"]


def test_non_catalog_rate_and_warnings():
    evaluator = BaselineEvaluator(gt1_path=GT1_PATH, gt2_path=GT2_PATH, catalog_dir=CATALOG_DIR)
    audit1 = evaluator.audit_gt_catalog_coverage(evaluator.gt1, "Experte 1")
    
    # We know Experte 1 has free-text items in primaerverband and sekundaerverband
    assert audit1["primaerverband"]["non_catalog_items"] > 0
    assert audit1["sekundaerverband"]["non_catalog_items"] > 0
    assert 0.0 < audit1["primaerverband"]["non_catalog_rate"] < 1.0


def test_full_baseline_pipeline():
    results = evaluate_baselines_dual(GT1_PATH, GT2_PATH, LLM_PATH, catalog_dir=CATALOG_DIR, n_runs=50, seed=42)
    
    df_summary = results["summary_table"]
    df_per_image = results["per_image_table"]
    
    assert not df_summary.empty
    assert len(df_summary) == 7  # 6 main fields + 1 extra exsudatmenge_dist metric row
    
    expected_cols = [
        "Feld", "Metrik", "GT1 Random (Mean [95% CI])", "GT1 Majority", "GT1 LLM",
        "GT2 Random (Mean [95% CI])", "GT2 Majority", "GT2 LLM",
        "Experte 1 vs Experte 2 (Inter-Rater)", "GT1 n_empty", "GT1 non_catalog_rate"
    ]
    for col in expected_cols:
        assert col in df_summary.columns
        
    assert not df_per_image.empty
    assert len(df_per_image) == 60  # 60 images
