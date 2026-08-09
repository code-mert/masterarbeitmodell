import os
import sys
import pandas as pd

# Ensure scripts folder is in sys.path
SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../scripts"))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from create_wundtyp_excel import parse_val_str
from create_exsudat_excel import load_ki_exsudat
from exsudat_mapping_dictionary import map_exsudat_explicit, calculate_ordinal_score

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

FS_LR_PROMPT_EX = ["wunde_04", "wunde_18"]
FS_NURS_PROMPT_EX = ["wunde_18", "wunde_28"]

def get_agreement_info(v1, v2, v3):
    valid = [v for v in [v1, v2, v3] if v and v not in ["keine Angabe", "Enthaltung / keine Angabe", "N/A"]]
    if len(valid) < 2:
        return "N/A", None
    if len(valid) == 3:
        if valid[0] == valid[1] == valid[2]:
            return "3/3 Einig", valid[0]
        if valid[0] == valid[1] or valid[0] == valid[2]:
            return "2/3 Einig", valid[0]
        if valid[1] == valid[2]:
            return "2/3 Einig", valid[1]
        return "0/3 Uneinig", None
    if len(valid) == 2:
        if valid[0] == valid[1]:
            return "2/2 Einig", valid[0]
        return "0/2 Uneinig", None
    return "0/3 Uneinig", None


def calculate_exsudat_lr_ordinal_scores():
    """
    Calculates L&R Baselines, Inter-Rater Agreement, and KI Model Scores for Exsudat (Ordinal Score %).
    """
    gt1_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv"), sep=";")
    gt2_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv"), sep=";")

    z_lr = load_ki_exsudat("zero_shot_lr")
    f_lr = load_ki_exsudat("few_shot_lr")
    t_lr = load_ki_exsudat("two_stage_lr")

    exp_data = []
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        r1 = gt1_norm[gt1_norm["image_id"] == img_id]
        r2 = gt2_norm[gt2_norm["image_id"] == img_id]

        v1_raw = parse_val_str(r1["exsudat"].values[0]) if len(r1) > 0 and "exsudat" in r1.columns else ""
        v2_raw = parse_val_str(r2["exsudat"].values[0]) if len(r2) > 0 and "exsudat" in r2.columns else ""

        m1 = map_exsudat_explicit(v1_raw)
        m2 = map_exsudat_explicit(v2_raw)

        exp_data.append({"img_id": img_id, "m1": m1, "m2": m2})

    # 1. Random Baseline Ordinal Score L&R (Best of Both)
    rand_scores = []
    for r in exp_data:
        sc1_all = [calculate_ordinal_score(g, r["m1"]) for g in ["Keine", "Leicht", "Mäßig", "Stark"]]
        sc2_all = [calculate_ordinal_score(g, r["m2"]) for g in ["Keine", "Leicht", "Mäßig", "Stark"]]
        v1 = [s for s in sc1_all if s is not None]
        v2 = [s for s in sc2_all if s is not None]
        if v1 and v2:
            cand = [max(s1, s2) for s1, s2 in zip(sc1_all, sc2_all) if s1 is not None and s2 is not None]
            rand_scores.append(sum(cand)/len(cand))
        elif v1: rand_scores.append(sum(v1)/len(v1))
        elif v2: rand_scores.append(sum(v2)/len(v2))
    random_pct = (sum(rand_scores) / len(rand_scores)) * 100

    # 2. Majority Baseline Ordinal Score L&R (Predicting Mäßig)
    maj_scores = []
    for r in exp_data:
        sc1 = calculate_ordinal_score("Mäßig", r["m1"])
        sc2 = calculate_ordinal_score("Mäßig", r["m2"])
        v = [s for s in [sc1, sc2] if s is not None]
        if v: maj_scores.append(max(v))
    majority_pct = (sum(maj_scores) / len(maj_scores)) * 100

    # 3. Inter-Rater Agreement Ordinal Score (E1 vs E2)
    inter_scores = [calculate_ordinal_score(r["m1"], r["m2"]) for r in exp_data if calculate_ordinal_score(r["m1"], r["m2"]) is not None]
    inter_pct = (sum(inter_scores) / len(inter_scores)) * 100

    # 4. KI Models
    def eval_ki(ki_dict, p_ex):
        sc_list = []
        for r in exp_data:
            if r["img_id"] in p_ex: continue
            ki_m = map_exsudat_explicit(ki_dict.get(r["img_id"], ""))
            sc1 = calculate_ordinal_score(ki_m, r["m1"])
            sc2 = calculate_ordinal_score(ki_m, r["m2"])
            v = [s for s in [sc1, sc2] if s is not None]
            if v: sc_list.append(max(v))
        return (sum(sc_list)/len(sc_list))*100, len(sc_list)

    z_pct, z_tot = eval_ki(z_lr, [])
    f_pct, f_tot = eval_ki(f_lr, FS_LR_PROMPT_EX)
    t_pct, t_tot = eval_ki(t_lr, [])

    return {
        "is_ordinal": True,
        "y_max": 100,
        "y_label": "Durchschnittlicher Ordinal Score (%)",
        "left_labels": ["Random\nBaseline", "Majority\nBaseline", "Inter-Rater\nAgreement"],
        "left_values": [random_pct, majority_pct, inter_pct],
        "left_eval_counts": [len(rand_scores), len(maj_scores), len(inter_scores)],
        "right_labels": ["Zero-Shot\nL&R", "Few-Shot\nL&R", "Two-Stage\nL&R"],
        "right_values": [z_pct, f_pct, t_pct],
        "right_eval_counts": [z_tot, f_tot, t_tot]
    }


def calculate_exsudat_nursit_ordinal_scores():
    """
    Calculates NursIT Baselines and KI Model Scores for Exsudat (Experte 3, Ordinal Score %).
    """
    gtn_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/allgemeine_verbandsklassen_normalised.csv"))

    z_nurs = load_ki_exsudat("zero_shot")
    f_nurs = load_ki_exsudat("few_shot")
    t_nurs = load_ki_exsudat("two_stage")

    exp3_mapped = {}
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        r3 = gtn_norm[gtn_norm["image_id"] == img_id]
        v3_raw = parse_val_str(r3["exsudat"].values[0]) if len(r3) > 0 and "exsudat" in r3.columns else ""
        exp3_mapped[img_id] = map_exsudat_explicit(v3_raw)

    # 1. Random Baseline Ordinal Score NursIT
    rand_scores = []
    for img_id, mn in exp3_mapped.items():
        v = [calculate_ordinal_score(g, mn) for g in ["Keine", "Leicht", "Mäßig", "Stark"] if calculate_ordinal_score(g, mn) is not None]
        if v: rand_scores.append(sum(v)/len(v))
    random_pct = (sum(rand_scores)/len(rand_scores))*100

    # 2. Majority Baseline Ordinal Score NursIT (Predicting Mäßig)
    maj_scores = [calculate_ordinal_score("Mäßig", mn) for mn in exp3_mapped.values() if calculate_ordinal_score("Mäßig", mn) is not None]
    majority_pct = (sum(maj_scores)/len(maj_scores))*100

    # 3. NursIT KI Models
    def eval_ki(ki_dict, p_ex):
        sc_list = []
        for img_id, mn in exp3_mapped.items():
            if img_id in p_ex: continue
            ki_m = map_exsudat_explicit(ki_dict.get(img_id, ""))
            sc = calculate_ordinal_score(ki_m, mn)
            if sc is not None: sc_list.append(sc)
        return (sum(sc_list)/len(sc_list))*100, len(sc_list)

    z_pct, z_tot = eval_ki(z_nurs, [])
    f_pct, f_tot = eval_ki(f_nurs, FS_NURS_PROMPT_EX)
    t_pct, t_tot = eval_ki(t_nurs, [])

    return {
        "is_ordinal": True,
        "y_max": 100,
        "y_label": "Durchschnittlicher Ordinal Score (%)",
        "left_labels": ["Random\nBaseline", "Majority\nBaseline"],
        "left_values": [random_pct, majority_pct],
        "left_eval_counts": [len(rand_scores), len(maj_scores)],
        "right_labels": ["Zero-Shot\nNursIT", "Few-Shot\nNursIT", "Two-Stage\nNursIT"],
        "right_values": [z_pct, f_pct, t_pct],
        "right_eval_counts": [z_tot, f_tot, t_tot]
    }


def calculate_exsudat_consensus_ordinal_scores():
    """
    Calculates Ordinal Scores on the 6 wounds where ALL 3 experts agree 100%.
    """
    gt1_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv"), sep=";")
    gt2_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv"), sep=";")
    gtn_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/allgemeine_verbandsklassen_normalised.csv"))

    z_lr = load_ki_exsudat("zero_shot_lr")
    f_lr = load_ki_exsudat("few_shot_lr")
    t_lr = load_ki_exsudat("two_stage_lr")

    z_nurs = load_ki_exsudat("zero_shot")
    f_nurs = load_ki_exsudat("few_shot")
    t_nurs = load_ki_exsudat("two_stage")

    consensus_wounds = {}
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        r1 = gt1_norm[gt1_norm["image_id"] == img_id]
        r2 = gt2_norm[gt2_norm["image_id"] == img_id]
        r3 = gtn_norm[gtn_norm["image_id"] == img_id]

        v1_raw = parse_val_str(r1["exsudat"].values[0]) if len(r1) > 0 and "exsudat" in r1.columns else ""
        v2_raw = parse_val_str(r2["exsudat"].values[0]) if len(r2) > 0 and "exsudat" in r2.columns else ""
        v3_raw = parse_val_str(r3["exsudat"].values[0]) if len(r3) > 0 and "exsudat" in r3.columns else ""

        m1 = map_exsudat_explicit(v1_raw)
        m2 = map_exsudat_explicit(v2_raw)
        m3 = map_exsudat_explicit(v3_raw)

        if m1 != "Enthaltung / keine Angabe" and m1 == m2 == m3:
            consensus_wounds[img_id] = m1

    total_consensus = len(consensus_wounds) # 6

    def eval_consensus(ki_dict, p_ex):
        sc_list = []
        for img_id, target in consensus_wounds.items():
            if img_id in p_ex: continue
            ki_m = map_exsudat_explicit(ki_dict.get(img_id, ""))
            sc = calculate_ordinal_score(ki_m, target)
            if sc is not None: sc_list.append(sc)
        return (sum(sc_list)/len(sc_list))*100 if sc_list else 0.0, len(sc_list)

    z_lr_pct, z_lr_tot = eval_consensus(z_lr, [])
    f_lr_pct, f_lr_tot = eval_consensus(f_lr, FS_LR_PROMPT_EX)
    t_lr_pct, t_lr_tot = eval_consensus(t_lr, [])

    z_nurs_pct, z_nurs_tot = eval_consensus(z_nurs, [])
    f_nurs_pct, f_nurs_tot = eval_consensus(f_nurs, FS_NURS_PROMPT_EX)
    t_nurs_pct, t_nurs_tot = eval_consensus(t_nurs, [])

    return {
        "is_ordinal": True,
        "total_consensus": total_consensus,
        "left_labels": ["Zero-Shot\nL&R", "Few-Shot\nL&R", "Two-Stage\nL&R"],
        "left_pcts": [z_lr_pct, f_lr_pct, t_lr_pct],
        "left_eval_counts": [z_lr_tot, f_lr_tot, t_lr_tot],
        "right_labels": ["Zero-Shot\nNursIT", "Few-Shot\nNursIT", "Two-Stage\nNursIT"],
        "right_pcts": [z_nurs_pct, f_nurs_pct, t_nurs_pct],
        "right_eval_counts": [z_nurs_tot, f_nurs_tot, t_nurs_tot]
    }
