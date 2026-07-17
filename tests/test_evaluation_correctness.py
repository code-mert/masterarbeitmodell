import pytest
import os
import numpy as np

from eval.loaders import load_ground_truth, load_llm_outputs, matched_image_ids
from eval.mapping import align, filter_markers, unpack_value
from eval.metrics import set_f1, best_path_f1, exact_match, precision_recall
from eval.baselines import (
    evaluate_single_dataset_pair,
    evaluate_baselines_dual,
    parse_exsudat_level,
    UNASSESSABLE_EXSUDAT_PHRASES,
    extract_gt_field_value
)

GT1_PATH = "data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv"
GT2_PATH = "data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv"
LLM_PATH = "data/llm_outputs/zero_shot_lr/zero_shot_lr_normalised.csv"


def test_align_symmetric_keys():
    """
    Verifies that align() works symmetrically when given either LLM output format
    keys or Ground Truth CSV keys.
    """
    gt1 = load_ground_truth(GT1_PATH)
    gt2 = load_ground_truth(GT2_PATH)
    
    img_id = "wunde_01"
    rec1 = gt1[img_id]
    rec2 = gt2[img_id]

    # Structurally align rec1 against rec2 (Ground Truth vs Ground Truth)
    aligned_gt = align(rec1, rec2)
    
    # Assert that GT2 keys are extracted correctly (not defaulting to empty sets)
    p2, a2 = extract_gt_field_value(rec2, "primaerverband")
    extracted_p2 = aligned_gt["primaerverband"]["llm_praef"]
    extracted_a2 = aligned_gt["primaerverband"]["llm_alt"]

    assert set(extracted_p2) == set(filter_markers(p2))
    assert set(extracted_a2) == set(filter_markers(a2))


def test_inter_rater_calculation():
    """
    Asserts that Inter-Rater evaluation (Experte 1 vs Experte 2) yields the exact 
    expected scores and is not zeroed out by key mismatch bugs.
    """
    gt1 = load_ground_truth(GT1_PATH)
    gt2 = load_ground_truth(GT2_PATH)
    common_ids = matched_image_ids(gt1, gt2)
    
    scores, per_image = evaluate_single_dataset_pair(gt1, gt2, common_ids)

    # Calculate expected union set F1 directly
    direct_prim_f1 = []
    for img_id in common_ids:
        p1, a1 = extract_gt_field_value(gt1[img_id], "primaerverband")
        p2, a2 = extract_gt_field_value(gt2[img_id], "primaerverband")
        set1 = set(filter_markers(p1)) | set(filter_markers(a1))
        set2 = set(filter_markers(p2)) | set(filter_markers(a2))
        direct_prim_f1.append(set_f1(set1, set2))
        
    expected_prim_f1 = float(np.mean(direct_prim_f1))
    
    # Assert that evaluation pipeline matches direct computation
    assert abs(scores["primaerverband"] - expected_prim_f1) < 1e-5
    assert scores["primaerverband"] > 0.30  # Inter-rater primärverband should be ~0.3405
    assert scores["sekundaerverband"] > 0.80  # Inter-rater sekundärverband should be ~0.8333
    assert scores["debridement"] > 0.35      # Inter-rater debridement should be ~0.4105


def test_best_path_f1_union_logic():
    """
    Verifies that best_path_f1 evaluates Union Set F1 correctly and does not
    grant false 1.0 scores to empty alternative sets when primary sets differ.
    """
    gt_p = {"Suprasorb CNP"}
    gt_a = set()
    llm_p = {"Suprasorb P"}
    llm_a = set()

    f1, exact, prec, rec = best_path_f1(llm_p, llm_a, gt_p, gt_a)

    # Disjoint primary predictions with empty alternative sets MUST score F1 = 0.0
    assert f1 == 0.0
    assert exact is False

    # Identical union sets MUST score F1 = 1.0
    f1_perfect, exact_perfect, _, _ = best_path_f1({"Suprasorb CNP"}, set(), {"Suprasorb CNP"}, set())
    assert f1_perfect == 1.0
    assert exact_perfect is True


def test_exsudat_parsing_unassessable_phrases():
    """
    Verifies that all unassessable phrases parse to None instead of 0 (Keine).
    """
    for phrase in UNASSESSABLE_EXSUDAT_PHRASES:
        assert parse_exsudat_level(phrase) is None
        assert parse_exsudat_level(f"Hinweis: {phrase}") is None

    # Valid levels must still parse correctly
    assert parse_exsudat_level("Keine Exsudation") == 0
    assert parse_exsudat_level("Leicht") == 1
    assert parse_exsudat_level("Mäßig") == 2
    assert parse_exsudat_level("Stark") == 3
    assert parse_exsudat_level("Sehr stark") == 4
