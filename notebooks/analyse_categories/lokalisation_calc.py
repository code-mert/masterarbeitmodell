import os
import sys
import pandas as pd

# Ensure scripts folder is in sys.path
SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../scripts"))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from create_wundtyp_excel import parse_val_str
from create_lokalisation_excel import load_ki_lokalisation
try:
    from notebooks.utils_notebook.clean import normalise_by_mapping
    from notebooks.utils_notebook.mappings import LOKALISATION_GT_MAPPING
except ImportError:
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../utils_notebook")))
    from clean import normalise_by_mapping
    from mappings import LOKALISATION_GT_MAPPING

def map_lokalisation_explicit(val):
    if not val or str(val).strip() in ["keine Angabe", "nan", "?", "???", "keine Angabe möglich", "nicht beurteilbar", "nicht genau definierbar", "lokalisation nicht genau zu definieren", "N/A"]:
        return "Enthaltung / keine Angabe"
    clean_val = str(val).strip()
    if clean_val in LOKALISATION_GT_MAPPING:
        return LOKALISATION_GT_MAPPING[clean_val][0]
    for k, v in LOKALISATION_GT_MAPPING.items():
        if k.lower() == clean_val.lower():
            return v[0]
    v = clean_val.lower()
    if "abdomen" in v or "bauch" in v or "stoma" in v or "peristoma" in v or "unterbauch" in v:
        return "Abdomen"
    if "gesäß" in v or "sakral" in v or "sacral" in v or "steiß" in v or "sacrum" in v or "glutä" in v or "paraglutäal" in v or "os sacrum" in v or "intergluteal" in v or "sakrokokzygeal" in v:
        return "Gesäß / Sakral"
    if "fuß" in v or "fuss" in v or "fers" in v or "zeh" in v or "plantar" in v or "malleol" in v or "vorfuß" in v or "außenknöchel" in v or "innenknöchel" in v or "mittfuß" in v or "zehe" in v or "knöchel" in v:
        return "Fuß"
    if "bein" in v or "unterschenkel" in v or "oberschenkel" in v or "knie" in v or "femur" in v or "schienbein" in v or "wade" in v or "untere extremität" in v or "untere extremitaet" in v:
        return "Bein"
    if "arm" in v or "hand" in v or "oberarm" in v or "unterarm" in v or "ellenbeug" in v or "finger" in v or "handrücken" in v or "obere extremität" in v or "obere extremitaet" in v:
        return "Arm / Hand"
    return "Enthaltung / keine Angabe"

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Few-Shot Prompt Example Wounds to exclude
FS_LR_PROMPT_EX = ["wunde_04", "wunde_18"]
FS_NURS_PROMPT_EX = ["wunde_18", "wunde_28"]

def calculate_lokalisation_lr_scores():
    """
    Calculates L&R Baselines, Inter-Rater Agreement, and KI Model Scores for Lokalisation.
    All strings map 1-to-1 via lokalisation_mapping_dictionary.py.
    Best of Both checks if KI mapped output matches mapped Experte 1 OR mapped Experte 2.
    """
    gt1_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv"), sep=";")
    gt2_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv"), sep=";")

    z_lr = load_ki_lokalisation("zero_shot_lr")
    f_lr = load_ki_lokalisation("few_shot_lr")
    t_lr = load_ki_lokalisation("two_stage_lr")

    exp_data = []
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        r1 = gt1_norm[gt1_norm["image_id"] == img_id]
        r2 = gt2_norm[gt2_norm["image_id"] == img_id]

        v1_raw = parse_val_str(r1["lokalisation"].values[0]) if len(r1) > 0 and "lokalisation" in r1.columns else ""
        v2_raw = parse_val_str(r2["lokalisation"].values[0]) if len(r2) > 0 and "lokalisation" in r2.columns else ""

        m1 = map_lokalisation_explicit(v1_raw)
        m2 = map_lokalisation_explicit(v2_raw)

        exp_data.append({
            "img_id": img_id,
            "m1": m1,
            "m2": m2
        })

    df_exp = pd.DataFrame(exp_data)
    total_wounds = 60

    # 1. Random Baseline (Strictly 1 out of 6 categories = 10.0 / 60 = 16.7%)
    random_cnt = 10.0
    random_pct = (1.0 / 6.0) * 100

    # 2. Majority Baseline on Best of Both (Always predicting Fuß)
    majority_cat = "Fuß"
    best_maj_hits = 0
    for row in exp_data:
        if row["m1"] == majority_cat or row["m2"] == majority_cat:
            best_maj_hits += 1
    majority_best_pct = (best_maj_hits / total_wounds) * 100

    # 3. Inter-Rater Agreement (Experte 1 == Experte 2)
    inter_hits = sum(df_exp["m1"] == df_exp["m2"])
    inter_rater_pct = (inter_hits / total_wounds) * 100

    # 4. KI Models on Best of Both (ki_mapped == m1 or ki_mapped == m2)
    # Zero-Shot L&R
    z_hits = sum(1 for r in exp_data if map_lokalisation_explicit(z_lr.get(r["img_id"], "")) in (r["m1"], r["m2"]))
    z_pct = (z_hits / total_wounds) * 100

    # Few-Shot L&R (excl. prompt examples 04 & 18 -> 58 wounds)
    f_hits = sum(1 for r in exp_data if r["img_id"] not in FS_LR_PROMPT_EX and map_lokalisation_explicit(f_lr.get(r["img_id"], "")) in (r["m1"], r["m2"]))
    f_tot = 58
    f_pct = (f_hits / f_tot) * 100

    # Two-Stage L&R
    t_hits = sum(1 for r in exp_data if map_lokalisation_explicit(t_lr.get(r["img_id"], "")) in (r["m1"], r["m2"]))
    t_pct = (t_hits / total_wounds) * 100

    return {
        "total_wounds": total_wounds,
        "left_labels": ["Random\nBaseline", "Majority\nBaseline", "Inter-Rater\nAgreement"],
        "left_counts": [random_cnt, best_maj_hits, inter_hits],
        "left_values": [random_pct, majority_best_pct, inter_rater_pct],
        "left_totals": [60, 60, 60],
        "right_labels": ["Zero-Shot\nL&R", "Few-Shot\nL&R", "Two-Stage\nL&R"],
        "right_counts": [z_hits, f_hits, t_hits],
        "right_values": [z_pct, f_pct, t_pct],
        "right_totals": [60, f_tot, 60]
    }


def calculate_lokalisation_nursit_scores():
    """
    Calculates NursIT Baselines and KI Model Scores for Lokalisation (Experte 3, 60 Wounds total).
    """
    gtn_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/allgemeine_verbandsklassen_normalised.csv"))

    z_nurs = load_ki_lokalisation("zero_shot")
    f_nurs = load_ki_lokalisation("few_shot")
    t_nurs = load_ki_lokalisation("two_stage")

    exp3_mapped = {}
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        r3 = gtn_norm[gtn_norm["image_id"] == img_id]
        v3_raw = parse_val_str(r3["lokalisation"].values[0]) if len(r3) > 0 and "lokalisation" in r3.columns else ""
        exp3_mapped[img_id] = map_lokalisation_explicit(v3_raw)

    s_exp3 = pd.Series(exp3_mapped)
    total_wounds = 60

    # 1. Random Baseline (1/6 of 60 = 10.0 = 16.7%)
    random_cnt = 10.0
    random_acc = (1.0 / 6.0) * 100

    # 2. Majority Baseline (Fuß = 29 / 60 = 48.3%)
    majority_cat = "Fuß"
    majority_cnt = (s_exp3 == majority_cat).sum()
    majority_acc = (majority_cnt / total_wounds) * 100

    # 3. NursIT AI Models
    z_hits = sum(1 for img_id, m3 in exp3_mapped.items() if map_lokalisation_explicit(z_nurs.get(img_id, "")) == m3)
    z_pct = (z_hits / total_wounds) * 100

    # Few-Shot NursIT (excl. 18 & 28 -> 58 wounds)
    f_hits = sum(1 for img_id, m3 in exp3_mapped.items() if img_id not in FS_NURS_PROMPT_EX and map_lokalisation_explicit(f_nurs.get(img_id, "")) == m3)
    f_tot = 58
    f_pct = (f_hits / f_tot) * 100

    t_hits = sum(1 for img_id, m3 in exp3_mapped.items() if map_lokalisation_explicit(t_nurs.get(img_id, "")) == m3)
    t_pct = (t_hits / total_wounds) * 100

    return {
        "total_wounds": total_wounds,
        "left_labels": ["Random\nBaseline", "Majority\nBaseline"],
        "left_counts": [random_cnt, majority_cnt],
        "left_values": [random_acc, majority_acc],
        "left_totals": [60, 60],
        "right_labels": ["Zero-Shot\nNursIT", "Few-Shot\nNursIT", "Two-Stage\nNursIT"],
        "right_counts": [z_hits, f_hits, t_hits],
        "right_values": [z_pct, f_pct, t_pct],
        "right_totals": [60, f_tot, 60]
    }


def calculate_lokalisation_consensus_scores():
    """
    Calculates AI Model performance on the 40 wounds where ALL 3 experts agree 100%.
    """
    gt1_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv"), sep=";")
    gt2_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv"), sep=";")
    gtn_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/allgemeine_verbandsklassen_normalised.csv"))

    z_lr = load_ki_lokalisation("zero_shot_lr")
    f_lr = load_ki_lokalisation("few_shot_lr")
    t_lr = load_ki_lokalisation("two_stage_lr")

    z_nurs = load_ki_lokalisation("zero_shot")
    f_nurs = load_ki_lokalisation("few_shot")
    t_nurs = load_ki_lokalisation("two_stage")

    consensus_wounds = {}
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        r1 = gt1_norm[gt1_norm["image_id"] == img_id]
        r2 = gt2_norm[gt2_norm["image_id"] == img_id]
        r3 = gtn_norm[gtn_norm["image_id"] == img_id]

        v1_raw = parse_val_str(r1["lokalisation"].values[0]) if len(r1) > 0 and "lokalisation" in r1.columns else ""
        v2_raw = parse_val_str(r2["lokalisation"].values[0]) if len(r2) > 0 and "lokalisation" in r2.columns else ""
        v3_raw = parse_val_str(r3["lokalisation"].values[0]) if len(r3) > 0 and "lokalisation" in r3.columns else ""

        m1 = map_lokalisation_explicit(v1_raw)
        m2 = map_lokalisation_explicit(v2_raw)
        m3 = map_lokalisation_explicit(v3_raw)

        if m1 != "Enthaltung / keine Angabe" and m1 == m2 == m3:
            consensus_wounds[img_id] = m1

    total_consensus = len(consensus_wounds) # 40

    # L&R Models
    z_lr_hits = sum(1 for img_id, target in consensus_wounds.items() if map_lokalisation_explicit(z_lr.get(img_id, "")) == target)
    f_lr_hits = sum(1 for img_id, target in consensus_wounds.items() if img_id not in FS_LR_PROMPT_EX and map_lokalisation_explicit(f_lr.get(img_id, "")) == target)
    f_lr_tot = len([w for w in consensus_wounds if w not in FS_LR_PROMPT_EX]) # 39
    t_lr_hits = sum(1 for img_id, target in consensus_wounds.items() if map_lokalisation_explicit(t_lr.get(img_id, "")) == target)

    # NursIT Models
    z_nurs_hits = sum(1 for img_id, target in consensus_wounds.items() if map_lokalisation_explicit(z_nurs.get(img_id, "")) == target)
    f_nurs_hits = sum(1 for img_id, target in consensus_wounds.items() if img_id not in FS_NURS_PROMPT_EX and map_lokalisation_explicit(f_nurs.get(img_id, "")) == target)
    f_nurs_tot = len([w for w in consensus_wounds if w not in FS_NURS_PROMPT_EX]) # 39
    t_nurs_hits = sum(1 for img_id, target in consensus_wounds.items() if map_lokalisation_explicit(t_nurs.get(img_id, "")) == target)

    return {
        "total_consensus": total_consensus,
        "left_labels": ["Zero-Shot\nL&R", "Few-Shot\nL&R", "Two-Stage\nL&R"],
        "left_counts": [z_lr_hits, f_lr_hits, t_lr_hits],
        "left_pcts": [(z_lr_hits/40)*100, (f_lr_hits/f_lr_tot)*100, (t_lr_hits/40)*100],
        "left_totals": [40, f_lr_tot, 40],
        "right_labels": ["Zero-Shot\nNursIT", "Few-Shot\nNursIT", "Two-Stage\nNursIT"],
        "right_counts": [z_nurs_hits, f_nurs_hits, t_nurs_hits],
        "right_pcts": [(z_nurs_hits/40)*100, (f_nurs_hits/f_nurs_tot)*100, (t_nurs_hits/40)*100],
        "right_totals": [40, f_nurs_tot, 40]
    }
