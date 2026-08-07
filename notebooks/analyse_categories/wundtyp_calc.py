import os
import sys
import pandas as pd

# Ensure scripts folder is in sys.path
SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../scripts"))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from create_wundtyp_excel import parse_val_str, load_ki_wundtyp
from wundtyp_mapping_dictionary import map_wundtyp_explicit

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

def calculate_wundtyp_lr_scores():
    """
    Calculates L&R Baselines, Inter-Rater Agreement, and KI Model Scores for Wundtyp (60 Wounds total).
    All strings map 1-to-1 via wundtyp_mapping_dictionary.py.
    Best of Both checks if KI mapped output matches mapped Experte 1 OR mapped Experte 2.
    """
    gt1_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv"), sep=";")
    gt2_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv"), sep=";")

    z_lr = load_ki_wundtyp("zero_shot_lr")
    f_lr = load_ki_wundtyp("few_shot_lr")
    t_lr = load_ki_wundtyp("two_stage_lr")

    exp_data = []
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        r1 = gt1_norm[gt1_norm["image_id"] == img_id]
        r2 = gt2_norm[gt2_norm["image_id"] == img_id]

        v1_raw = parse_val_str(r1["wundtyp"].values[0]) if len(r1) > 0 else ""
        v2_raw = parse_val_str(r2["wundtyp"].values[0]) if len(r2) > 0 else ""

        m1 = map_wundtyp_explicit(v1_raw)
        m2 = map_wundtyp_explicit(v2_raw)

        exp_data.append({
            "img_id": img_id,
            "m1": m1,
            "m2": m2
        })

    df_exp = pd.DataFrame(exp_data)
    total_wounds = 60

    # 1. Random Baseline (Strictly 1 out of 8 = 7.5 / 60 = 12.5%)
    random_cnt = 7.5
    random_pct = 12.5

    # 2. Majority Baseline on Best of Both (Always predicting Ulkus unspezifisch)
    majority_cat = "Ulkus (Ätiologie unspezifisch)"
    best_maj_hits = 0
    for row in exp_data:
        if row["m1"] == majority_cat or row["m2"] == majority_cat:
            best_maj_hits += 1
    majority_best_pct = (best_maj_hits / total_wounds) * 100

    # 3. Inter-Rater Agreement (Experte 1 == Experte 2)
    inter_hits = sum(df_exp["m1"] == df_exp["m2"])
    inter_rater_pct = (inter_hits / total_wounds) * 100

    # 4. KI Models on Best of Both (ki_mapped == m1 or ki_mapped == m2)
    ki_models = {
        "Zero-Shot L&R": z_lr,
        "Few-Shot L&R": f_lr,
        "Two-Stage L&R": t_lr
    }

    ki_counts = []
    ki_pcts = []
    for name, model_dict in ki_models.items():
        hits = 0
        for row in exp_data:
            img_id = row["img_id"]
            m1, m2 = row["m1"], row["m2"]
            ki_mapped = map_wundtyp_explicit(model_dict.get(img_id, ""))
            if ki_mapped == m1 or ki_mapped == m2:
                hits += 1
        ki_counts.append(hits)
        ki_pcts.append((hits / total_wounds) * 100)

    return {
        "total_wounds": total_wounds,
        "left_labels": ["Random\nBaseline", "Majority\nBaseline", "Inter-Rater\nAgreement"],
        "left_counts": [random_cnt, best_maj_hits, inter_hits],
        "left_values": [random_pct, majority_best_pct, inter_rater_pct],
        "right_labels": ["Zero-Shot\nL&R", "Few-Shot\nL&R", "Two-Stage\nL&R"],
        "right_counts": ki_counts,
        "right_values": ki_pcts
    }


def calculate_wundtyp_nursit_scores():
    """
    Calculates NursIT Baselines and KI Model Scores for Wundtyp (Experte 3, 60 Wounds total).
    """
    gtn_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/allgemeine_verbandsklassen_normalised.csv"))

    z_nurs = load_ki_wundtyp("zero_shot")
    f_nurs = load_ki_wundtyp("few_shot")
    t_nurs = load_ki_wundtyp("two_stage")

    exp3_mapped = {}
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        r3 = gtn_norm[gtn_norm["image_id"] == img_id]
        v3_raw = parse_val_str(r3["wundtyp"].values[0]) if len(r3) > 0 else ""
        exp3_mapped[img_id] = map_wundtyp_explicit(v3_raw)

    s_exp3 = pd.Series(exp3_mapped)
    total_wounds = 60

    # 1. Random Baseline (1/8 of 60 = 7.5 = 12.5%)
    random_cnt = 7.5
    random_acc = 12.5

    # 2. Majority Baseline (Dekubitus = 21 / 60 = 35.0%)
    majority_cat = s_exp3.value_counts().idxmax()
    majority_cnt = (s_exp3 == majority_cat).sum()
    majority_acc = (majority_cnt / total_wounds) * 100

    # 3. NursIT AI Models
    ki_nursit = {
        "Zero-Shot NursIT": z_nurs,
        "Few-Shot NursIT": f_nurs,
        "Two-Stage NursIT": t_nurs
    }

    ki_counts = []
    ki_pcts = []
    for name, model_dict in ki_nursit.items():
        hits = 0
        for img_id, m3 in exp3_mapped.items():
            ki_val = map_wundtyp_explicit(model_dict.get(img_id, ""))
            if ki_val == m3:
                hits += 1
        ki_counts.append(hits)
        ki_pcts.append((hits / total_wounds) * 100)

    return {
        "total_wounds": total_wounds,
        "left_labels": ["Random\nBaseline", "Majority\nBaseline"],
        "left_counts": [random_cnt, majority_cnt],
        "left_values": [random_acc, majority_acc],
        "right_labels": ["Zero-Shot\nNursIT", "Few-Shot\nNursIT", "Two-Stage\nNursIT"],
        "right_counts": ki_counts,
        "right_values": ki_pcts
    }


def calculate_wundtyp_consensus_scores():
    """
    Calculates AI Model performance on the 30 wounds where ALL 3 experts agree 100%.
    """
    gt1_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv"), sep=";")
    gt2_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv"), sep=";")
    gtn_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/allgemeine_verbandsklassen_normalised.csv"))

    z_lr = load_ki_wundtyp("zero_shot_lr")
    f_lr = load_ki_wundtyp("few_shot_lr")
    t_lr = load_ki_wundtyp("two_stage_lr")

    z_nurs = load_ki_wundtyp("zero_shot")
    f_nurs = load_ki_wundtyp("few_shot")
    t_nurs = load_ki_wundtyp("two_stage")

    consensus_wounds = {}
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        r1 = gt1_norm[gt1_norm["image_id"] == img_id]
        r2 = gt2_norm[gt2_norm["image_id"] == img_id]
        r3 = gtn_norm[gtn_norm["image_id"] == img_id]

        v1_raw = parse_val_str(r1["wundtyp"].values[0]) if len(r1) > 0 else ""
        v2_raw = parse_val_str(r2["wundtyp"].values[0]) if len(r2) > 0 else ""
        v3_raw = parse_val_str(r3["wundtyp"].values[0]) if len(r3) > 0 else ""

        m1 = map_wundtyp_explicit(v1_raw)
        m2 = map_wundtyp_explicit(v2_raw)
        m3 = map_wundtyp_explicit(v3_raw)

        valid_labels = [x for x in [m1, m2, m3] if x and x not in ["Enthaltung / keine Angabe", "N/A"]]
        if len(valid_labels) == 3 and valid_labels[0] == valid_labels[1] == valid_labels[2]:
            consensus_wounds[img_id] = valid_labels[0]

    total_consensus = len(consensus_wounds) # 30

    lr_models = {
        "Zero-Shot L&R": z_lr,
        "Few-Shot L&R": f_lr,
        "Two-Stage L&R": t_lr
    }

    nursit_models = {
        "Zero-Shot NursIT": z_nurs,
        "Few-Shot NursIT": f_nurs,
        "Two-Stage NursIT": t_nurs
    }

    lr_counts = []
    lr_pcts = []
    for name, model_dict in lr_models.items():
        hits = 0
        for img_id, target in consensus_wounds.items():
            ki_mapped = map_wundtyp_explicit(model_dict.get(img_id, ""))
            if ki_mapped == target:
                hits += 1
        lr_counts.append(hits)
        lr_pcts.append((hits / total_consensus) * 100)

    nursit_counts = []
    nursit_pcts = []
    for name, model_dict in nursit_models.items():
        hits = 0
        for img_id, target in consensus_wounds.items():
            ki_mapped = map_wundtyp_explicit(model_dict.get(img_id, ""))
            if ki_mapped == target:
                hits += 1
        nursit_counts.append(hits)
        nursit_pcts.append((hits / total_consensus) * 100)

    return {
        "total_consensus": total_consensus,
        "left_labels": ["Zero-Shot\nL&R", "Few-Shot\nL&R", "Two-Stage\nL&R"],
        "left_counts": lr_counts,
        "left_pcts": lr_pcts,
        "right_labels": ["Zero-Shot\nNursIT", "Few-Shot\nNursIT", "Two-Stage\nNursIT"],
        "right_counts": nursit_counts,
        "right_pcts": nursit_pcts
    }
