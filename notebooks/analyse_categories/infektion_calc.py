import os
import sys
import pandas as pd

SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../scripts"))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from create_wundtyp_excel import parse_val_str
from create_exsudat_excel import load_ki_exsudat

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

FS_LR_PROMPT_EX = ["wunde_04", "wunde_18"]
FS_NURS_PROMPT_EX = ["wunde_18", "wunde_28"]


def load_ki_field(sd_name, key_name):
    """
    Loads raw KI parsed output field for a given run folder and key.
    """
    import json
    sd_path = os.path.join(BASE_DIR, "runs/gpt-5", sd_name)
    results = {}
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        bd = f"Bild{i}"
        b_path = os.path.join(sd_path, bd)
        if not os.path.exists(b_path):
            results[img_id] = "N/A"
            continue
        json_files = sorted([f for f in os.listdir(b_path) if f.startswith("run_") and f.endswith(".json")])
        if not json_files:
            results[img_id] = "N/A"
            continue
        with open(os.path.join(b_path, json_files[-1])) as f:
            data = json.load(f)
        po = data.get("parsed_output", {})
        if not po or not isinstance(po, dict):
            results[img_id] = "N/A"
            continue
        val = po.get(key_name)
        results[img_id] = str(val).strip() if val is not None else "N/A"
    return results


def map_nursit_to_binary(val):
    val_str = str(val).strip()
    if val_str == "Keine Infektionszeichen":
        return "Nein"
    if val_str in ["Verdacht auf Infektion / kritische Kolonisation", "Deutliche Infektionszeichen"]:
        return "Ja"
    return "N/A"


def classify_spuelloesung(val):
    s = str(val).lower()
    if any(k in s for k in ["antimikrobiell", "phmb", "octenidin", "octenisept", "hypochlorit", "silber"]):
        return "Antimikrobiell"
    if any(k in s for k in ["neutral", "nacl", "ringer"]):
        return "Neutral"
    if "keine" in s or s in ["n/a", "none", "[]", ""]:
        return "Keine"
    return "Neutral"


def calculate_infektion_lr_scores():
    """
    Calculates L&R Infektionsstatus Exact Match % for Baselines and KI models (Best of Both).
    """
    gt1_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv"), sep=";")
    gt2_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv"), sep=";")

    z_lr = load_ki_field("zero_shot_lr", "infektion_vorhanden")
    f_lr = load_ki_field("few_shot_lr", "infektion_vorhanden")
    t_lr = load_ki_field("two_stage_lr", "infektion_vorhanden")

    exp_data = []
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        r1 = gt1_norm[gt1_norm["image_id"] == img_id]
        r2 = gt2_norm[gt2_norm["image_id"] == img_id]
        v1 = parse_val_str(r1["infektion"].values[0]) if len(r1) > 0 and "infektion" in r1.columns else ""
        v2 = parse_val_str(r2["infektion"].values[0]) if len(r2) > 0 and "infektion" in r2.columns else ""
        exp_data.append({"img_id": img_id, "v1": v1, "v2": v2})

    # 1. Random Baseline (50.0% for binary 50/50 chance)
    random_pct = 50.0

    # 2. Majority Baseline (predicting Nein or Ja)
    maj_ja = sum([1 for r in exp_data if r["v1"].lower() == "ja" or r["v2"].lower() == "ja"]) / len(exp_data)
    maj_nein = sum([1 for r in exp_data if r["v1"].lower() == "nein" or r["v2"].lower() == "nein"]) / len(exp_data)
    majority_pct = max(maj_ja, maj_nein) * 100

    # 3. Inter-Rater Agreement (E1 vs E2)
    inter_valid = [r for r in exp_data if r["v1"] in ["Ja", "Nein"] and r["v2"] in ["Ja", "Nein"]]
    inter_hits = [r for r in inter_valid if r["v1"] == r["v2"]]
    inter_pct = (len(inter_hits) / len(inter_valid)) * 100

    # 4. KI Best of Both
    def eval_ki(ki_dict, p_ex):
        hits, tot = 0, 0
        for r in exp_data:
            if r["img_id"] in p_ex: continue
            ki_v = ki_dict.get(r["img_id"], "").lower()
            if ki_v not in ["ja", "nein"]: continue
            tot += 1
            if ki_v == r["v1"].lower() or ki_v == r["v2"].lower():
                hits += 1
        return (hits / tot) * 100, hits, tot

    z_pct, z_hits, z_tot = eval_ki(z_lr, [])
    f_pct, f_hits, f_tot = eval_ki(f_lr, FS_LR_PROMPT_EX)
    t_pct, t_hits, t_tot = eval_ki(t_lr, [])

    return {
        "is_ordinal": False,
        "total_wounds": 60,
        "left_labels": ["Random\nBaseline", "Majority\nBaseline", "Inter-Rater\nAgreement"],
        "left_values": [random_pct, majority_pct, inter_pct],
        "left_counts": [30.0, max(maj_ja*60, maj_nein*60), len(inter_hits)],
        "left_totals": [60, 60, len(inter_valid)],
        "right_labels": ["Zero-Shot\nL&R", "Few-Shot\nL&R", "Two-Stage\nL&R"],
        "right_values": [z_pct, f_pct, t_pct],
        "right_counts": [z_hits, f_hits, t_hits],
        "right_totals": [z_tot, f_tot, t_tot]
    }


def calculate_infektion_nursit_scores():
    """
    Calculates NursIT 3-tier Ordinal Score % for Baselines and KI models (Experte 3).
    """
    gtn_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/allgemeine_verbandsklassen_normalised.csv"))

    z_nurs = load_ki_field("zero_shot", "infektionsstatus")
    f_nurs = load_ki_field("few_shot", "infektionsstatus")
    t_nurs = load_ki_field("two_stage", "infektionsstatus")

    ranks = {
        "Keine Infektionszeichen": 0,
        "Verdacht auf Infektion / kritische Kolonisation": 1,
        "Deutliche Infektionszeichen": 2
    }

    exp3_data = {}
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        r3 = gtn_norm[gtn_norm["image_id"] == img_id]
        v3 = parse_val_str(r3["infektion"].values[0]) if len(r3) > 0 and "infektion" in r3.columns else ""
        exp3_data[img_id] = v3

    # 1. Random Baseline (uniform choices over 3 ranks)
    rand_scores = []
    for img_id, v3 in exp3_data.items():
        if v3 in ranks:
            r_target = ranks[v3]
            scores_for_target = [1.0 - (abs(r_target - g) / 2.0) for g in [0, 1, 2]]
            rand_scores.append(sum(scores_for_target) / 3.0)
    random_pct = (sum(rand_scores) / len(rand_scores)) * 100

    # 2. Majority Baseline (predicting Rank 1: Verdacht)
    maj_scores = []
    for img_id, v3 in exp3_data.items():
        if v3 in ranks:
            r_target = ranks[v3]
            sc = 1.0 - (abs(r_target - 1) / 2.0)
            maj_scores.append(sc)
    majority_pct = (sum(maj_scores) / len(maj_scores)) * 100

    # 3. NursIT KI Models (Ordinal Score)
    def eval_ki(ki_dict, p_ex):
        sc_list = []
        for img_id, v3 in exp3_data.items():
            if img_id in p_ex: continue
            ki_v = ki_dict.get(img_id, "")
            if v3 in ranks and ki_v in ranks:
                d = abs(ranks[v3] - ranks[ki_v])
                sc_list.append(1.0 - (d / 2.0))
        return (sum(sc_list) / len(sc_list)) * 100, len(sc_list)

    z_pct, z_tot = eval_ki(z_nurs, [])
    f_pct, f_tot = eval_ki(f_nurs, FS_NURS_PROMPT_EX)
    t_pct, t_tot = eval_ki(t_nurs, [])

    return {
        "is_ordinal": True,
        "y_max": 100,
        "left_labels": ["Random\nBaseline", "Majority\nBaseline"],
        "left_values": [random_pct, majority_pct],
        "left_eval_counts": [len(rand_scores), len(maj_scores)],
        "right_labels": ["Zero-Shot\nNursIT", "Few-Shot\nNursIT", "Two-Stage\nNursIT"],
        "right_values": [z_pct, f_pct, t_pct],
        "right_eval_counts": [z_tot, f_tot, t_tot]
    }


def calculate_infektion_consensus_scores():
    """
    Calculates binary consensus accuracy on wounds with >= 2/3 expert agreement.
    (NursIT mapped to binary: Verdacht/Deutlich -> Ja, Keine -> Nein).
    """
    gt1_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv"), sep=";")
    gt2_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv"), sep=";")
    gtn_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/allgemeine_verbandsklassen_normalised.csv"))

    z_lr = load_ki_field("zero_shot_lr", "infektion_vorhanden")
    f_lr = load_ki_field("few_shot_lr", "infektion_vorhanden")
    t_lr = load_ki_field("two_stage_lr", "infektion_vorhanden")

    z_nurs = load_ki_field("zero_shot", "infektionsstatus")
    f_nurs = load_ki_field("few_shot", "infektionsstatus")
    t_nurs = load_ki_field("two_stage", "infektionsstatus")

    consensus_wounds = {}
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        r1 = gt1_norm[gt1_norm["image_id"] == img_id]
        r2 = gt2_norm[gt2_norm["image_id"] == img_id]
        r3 = gtn_norm[gtn_norm["image_id"] == img_id]

        v1 = parse_val_str(r1["infektion"].values[0]) if len(r1) > 0 and "infektion" in r1.columns else ""
        v2 = parse_val_str(r2["infektion"].values[0]) if len(r2) > 0 and "infektion" in r2.columns else ""
        v3_raw = parse_val_str(r3["infektion"].values[0]) if len(r3) > 0 and "infektion" in r3.columns else ""
        v3_bin = map_nursit_to_binary(v3_raw)

        valid = [v for v in [v1, v2, v3_bin] if v in ["Ja", "Nein"]]
        if len(valid) >= 2:
            if valid.count("Ja") >= 2:
                consensus_wounds[img_id] = "Ja"
            elif valid.count("Nein") >= 2:
                consensus_wounds[img_id] = "Nein"

    total_consensus = len(consensus_wounds) # 58 Wunden

    def eval_consensus(ki_dict, p_ex, is_nursit=False):
        hits, tot = 0, 0
        for img_id, target in consensus_wounds.items():
            if img_id in p_ex: continue
            raw_ki = ki_dict.get(img_id, "")
            ki_bin = map_nursit_to_binary(raw_ki) if is_nursit else ("Ja" if raw_ki.lower() == "ja" else ("Nein" if raw_ki.lower() == "nein" else "N/A"))
            if ki_bin in ["Ja", "Nein"]:
                tot += 1
                if ki_bin == target:
                    hits += 1
        return (hits / tot) * 100, hits, tot

    z_lr_pct, z_lr_h, z_lr_t = eval_consensus(z_lr, [], False)
    f_lr_pct, f_lr_h, f_lr_t = eval_consensus(f_lr, FS_LR_PROMPT_EX, False)
    t_lr_pct, t_lr_h, t_lr_t = eval_consensus(t_lr, [], False)

    z_n_pct, z_n_h, z_n_t = eval_consensus(z_nurs, [], True)
    f_n_pct, f_n_h, f_n_t = eval_consensus(f_nurs, FS_NURS_PROMPT_EX, True)
    t_n_pct, t_n_h, t_n_t = eval_consensus(t_nurs, [], True)

    return {
        "is_ordinal": False,
        "total_consensus": total_consensus,
        "left_labels": ["Zero-Shot\nL&R", "Few-Shot\nL&R", "Two-Stage\nL&R"],
        "left_counts": [z_lr_h, f_lr_h, t_lr_h],
        "left_pcts": [z_lr_pct, f_lr_pct, t_lr_pct],
        "left_totals": [z_lr_t, f_lr_t, t_lr_t],
        "right_labels": ["Zero-Shot\nNursIT", "Few-Shot\nNursIT", "Two-Stage\nNursIT"],
        "right_counts": [z_n_h, f_n_h, t_n_h],
        "right_pcts": [z_n_pct, f_n_pct, t_n_pct],
        "right_totals": [z_n_t, f_n_t, t_n_t]
    }


def calculate_spuelloesung_consensus_scores():
    """
    Calculates Spüllösung hit rate on the >= 2/3 consensus infection wounds.
    """
    gt1_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv"), sep=";")
    gt2_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv"), sep=";")
    gtn_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/allgemeine_verbandsklassen_normalised.csv"))

    z_lr = load_ki_field("zero_shot_lr", "spuelloesung")
    f_lr = load_ki_field("few_shot_lr", "spuelloesung")
    t_lr = load_ki_field("two_stage_lr", "spuelloesung")

    z_nurs = load_ki_field("zero_shot", "spuelloesung")
    f_nurs = load_ki_field("few_shot", "spuelloesung")
    t_nurs = load_ki_field("two_stage", "spuelloesung")

    consensus_info = {}
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        r1 = gt1_norm[gt1_norm["image_id"] == img_id]
        r2 = gt2_norm[gt2_norm["image_id"] == img_id]
        r3 = gtn_norm[gtn_norm["image_id"] == img_id]

        v1 = parse_val_str(r1["infektion"].values[0]) if len(r1) > 0 and "infektion" in r1.columns else ""
        v2 = parse_val_str(r2["infektion"].values[0]) if len(r2) > 0 and "infektion" in r2.columns else ""
        v3_raw = parse_val_str(r3["infektion"].values[0]) if len(r3) > 0 and "infektion" in r3.columns else ""
        v3_bin = map_nursit_to_binary(v3_raw)

        s1 = classify_spuelloesung(parse_val_str(r1["spuelloesung"].values[0])) if len(r1) > 0 and "spuelloesung" in r1.columns else ""
        s2 = classify_spuelloesung(parse_val_str(r2["spuelloesung"].values[0])) if len(r2) > 0 and "spuelloesung" in r2.columns else ""
        s3 = classify_spuelloesung(parse_val_str(r3["spuelloesung"].values[0])) if len(r3) > 0 and "spuelloesung" in r3.columns else ""

        valid = [v for v in [v1, v2, v3_bin] if v in ["Ja", "Nein"]]
        if len(valid) >= 2:
            maj_val = "Ja" if valid.count("Ja") >= 2 else ("Nein" if valid.count("Nein") >= 2 else None)
            if maj_val:
                consensus_info[img_id] = {"maj_val": maj_val, "s1": s1, "s2": s2, "s3": s3}

    total_consensus = len(consensus_info) # 58 Wunden

    def eval_lr_spuel(ki_dict, p_ex):
        hits, tot = 0, 0
        for img_id, info in consensus_info.items():
            if img_id in p_ex: continue
            ki_spuel = classify_spuelloesung(ki_dict.get(img_id, ""))
            tot += 1
            if ki_spuel == info["s1"] or ki_spuel == info["s2"]:
                hits += 1
        return (hits / tot) * 100, hits, tot

    def eval_nurs_spuel(ki_dict, p_ex):
        hits, tot = 0, 0
        for img_id, info in consensus_info.items():
            if img_id in p_ex: continue
            ki_spuel = classify_spuelloesung(ki_dict.get(img_id, ""))
            tot += 1
            if ki_spuel == info["s3"]:
                hits += 1
            elif info["maj_val"] == "Ja" and ki_spuel == "Antimikrobiell":
                hits += 1
            elif info["maj_val"] == "Nein" and ki_spuel in ["Neutral", "Keine"]:
                hits += 1
        return (hits / tot) * 100, hits, tot

    z_lr_pct, z_lr_h, z_lr_t = eval_lr_spuel(z_lr, [])
    f_lr_pct, f_lr_h, f_lr_t = eval_lr_spuel(f_lr, FS_LR_PROMPT_EX)
    t_lr_pct, t_lr_h, t_lr_t = eval_lr_spuel(t_lr, [])

    z_n_pct, z_n_h, z_n_t = eval_nurs_spuel(z_nurs, [])
    f_n_pct, f_n_h, f_n_t = eval_nurs_spuel(f_nurs, FS_NURS_PROMPT_EX)
    t_n_pct, t_n_h, t_n_t = eval_nurs_spuel(t_nurs, [])

    return {
        "is_ordinal": False,
        "total_consensus": total_consensus,
        "left_labels": ["Zero-Shot\nL&R", "Few-Shot\nL&R", "Two-Stage\nL&R"],
        "left_counts": [z_lr_h, f_lr_h, t_lr_h],
        "left_pcts": [z_lr_pct, f_lr_pct, t_lr_pct],
        "left_totals": [z_lr_t, f_lr_t, t_lr_t],
        "right_labels": ["Zero-Shot\nNursIT", "Few-Shot\nNursIT", "Two-Stage\nNursIT"],
        "right_counts": [z_n_h, f_n_h, t_n_h],
        "right_pcts": [z_n_pct, f_n_pct, t_n_pct],
        "right_totals": [z_n_t, f_n_t, t_n_t]
    }
