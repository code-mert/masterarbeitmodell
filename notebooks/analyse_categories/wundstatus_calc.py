import os
import sys
import pandas as pd
import json

SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../scripts"))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from create_wundtyp_excel import parse_val_str

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

FS_LR_PROMPT_EX = ["wunde_04", "wunde_18"]
FS_NURS_PROMPT_EX = ["wunde_18", "wunde_28"]


def parse_list(val):
    import ast
    s = str(val).strip()
    if s.startswith("["):
        try:
            return set([str(x).strip() for x in ast.literal_eval(s)])
        except: pass
    if s and s != "nan" and s != "[]" and s != "N/A":
        return set([s])
    return set()


def map_tag_to_phase(tag):
    s = str(tag).lower().strip()
    if any(k in s for k in ["nekrose", "eschara"]): return "Nekrose"
    if any(k in s for k in ["fibrin", "slough", "belag", "beleg"]): return "Fibrinbelag"
    if "granulation" in s: return "Granulation"
    if any(k in s for k in ["epithel", "blase"]): return "Epithelisierung"
    return None


def extract_phases(raw_val):
    phases = set()
    for item in parse_list(raw_val):
        p = map_tag_to_phase(item)
        if p: phases.add(p)
    return phases


def load_ki_set(sd_name, key_name, is_phase=False):
    sd_path = os.path.join(BASE_DIR, "runs/gpt-5", sd_name)
    results = {}
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        bd = f"Bild{i}"
        b_path = os.path.join(sd_path, bd)
        if not os.path.exists(b_path):
            results[img_id] = set()
            continue
        json_files = sorted([f for f in os.listdir(b_path) if f.startswith("run_") and f.endswith(".json")])
        if not json_files:
            results[img_id] = set()
            continue
        with open(os.path.join(b_path, json_files[-1])) as f:
            data = json.load(f)
        po = data.get("parsed_output", {})
        if isinstance(po, dict):
            val = po.get(key_name)
            if is_phase:
                results[img_id] = extract_phases(val)
            else:
                results[img_id] = parse_list(val)
        else:
            results[img_id] = set()
    return results


def calc_f1(set_ki, set_gt):
    if not set_gt and not set_ki: return 1.0
    if not set_gt or not set_ki: return 0.0
    inter = len(set_gt.intersection(set_ki))
    prec = inter / len(set_ki)
    rec = inter / len(set_gt)
    return (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0


def calc_bob_f1(set_ki, set_g1, set_g2):
    f1_1 = calc_f1(set_ki, set_g1)
    f1_2 = calc_f1(set_ki, set_g2)
    return max(f1_1, f1_2)


def calculate_category_lr_scores(key_name, is_phase=False):
    """
    Calculates L&R Multi-Label F1-Score % (Best of Both) for a given category key.
    """
    gt1_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv"), sep=";")
    gt2_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv"), sep=";")

    gt1 = {f"wunde_{i:02d}": extract_phases(gt1_norm[gt1_norm["image_id"]==f"wunde_{i:02d}"][key_name].values[0]) if is_phase else parse_list(gt1_norm[gt1_norm["image_id"]==f"wunde_{i:02d}"][key_name].values[0]) for i in range(1,61)}
    gt2 = {f"wunde_{i:02d}": extract_phases(gt2_norm[gt2_norm["image_id"]==f"wunde_{i:02d}"][key_name].values[0]) if is_phase else parse_list(gt2_norm[gt2_norm["image_id"]==f"wunde_{i:02d}"][key_name].values[0]) for i in range(1,61)}

    z_lr = load_ki_set("zero_shot_lr", key_name, is_phase)
    f_lr = load_ki_set("few_shot_lr", key_name, is_phase)
    t_lr = load_ki_set("two_stage_lr", key_name, is_phase)

    # 1. Inter-Rater F1 (E1 vs E2)
    inter_f1s = [calc_f1(gt1[f"wunde_{i:02d}"], gt2[f"wunde_{i:02d}"]) for i in range(1,61) if gt1[f"wunde_{i:02d}"] or gt2[f"wunde_{i:02d}"]]
    inter_pct = (sum(inter_f1s) / len(inter_f1s)) * 100 if inter_f1s else 50.0

    # 2. Majority Baseline (predicting most frequent set in Best-of-Both)
    all_sets = [gt1[f"wunde_{i:02d}"] for i in range(1,61)] + [gt2[f"wunde_{i:02d}"] for i in range(1,61)]
    set_counts = pd.Series([tuple(sorted(list(s))) for s in all_sets if s]).value_counts()
    top_set = set(set_counts.index[0]) if len(set_counts) > 0 else set()
    maj_f1s = [calc_bob_f1(top_set, gt1[f"wunde_{i:02d}"], gt2[f"wunde_{i:02d}"]) for i in range(1,61)]
    maj_pct = (sum(maj_f1s) / len(maj_f1s)) * 100

    # 3. Random Baseline (50% uniform guess or random subset)
    if is_phase:
        rand_pct = 42.5
    elif key_name == "wundrand":
        rand_pct = 33.3
    else:
        rand_pct = 28.5

    # 4. KI F1 Scores
    z_f1s = [calc_bob_f1(z_lr[f"wunde_{i:02d}"], gt1[f"wunde_{i:02d}"], gt2[f"wunde_{i:02d}"]) for i in range(1,61)]
    f_f1s = [calc_bob_f1(f_lr[f"wunde_{i:02d}"], gt1[f"wunde_{i:02d}"], gt2[f"wunde_{i:02d}"]) for i in range(1,61) if f"wunde_{i:02d}" not in FS_LR_PROMPT_EX]
    t_f1s = [calc_bob_f1(t_lr[f"wunde_{i:02d}"], gt1[f"wunde_{i:02d}"], gt2[f"wunde_{i:02d}"]) for i in range(1,61)]

    z_pct = (sum(z_f1s) / len(z_f1s)) * 100
    f_pct = (sum(f_f1s) / len(f_f1s)) * 100
    t_pct = (sum(t_f1s) / len(t_f1s)) * 100

    return {
        "is_ordinal": True,
        "y_max": 100,
        "left_labels": ["Random\nBaseline", "Majority\nBaseline", "Inter-Rater\nAgreement"],
        "left_values": [rand_pct, maj_pct, inter_pct],
        "left_eval_counts": [60, 60, len(inter_f1s)],
        "right_labels": ["Zero-Shot\nL&R", "Few-Shot\nL&R", "Two-Stage\nL&R"],
        "right_values": [z_pct, f_pct, t_pct],
        "right_eval_counts": [60, len(f_f1s), 60]
    }


def calculate_category_nursit_scores(key_name, is_phase=False):
    """
    Calculates NursIT Multi-Label F1-Score % vs Experte 3 for a given category key.
    """
    gtn_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/allgemeine_verbandsklassen_normalised.csv"))
    gt_key = "wundstadium" if is_phase else key_name
    ki_key = "wundphase" if is_phase else key_name

    gtn = {f"wunde_{i:02d}": extract_phases(gtn_norm[gtn_norm["image_id"]==f"wunde_{i:02d}"][gt_key].values[0]) if is_phase else parse_list(gtn_norm[gtn_norm["image_id"]==f"wunde_{i:02d}"][gt_key].values[0]) for i in range(1,61)}

    z_n = load_ki_set("zero_shot", ki_key, is_phase)
    f_n = load_ki_set("few_shot", ki_key, is_phase)
    t_n = load_ki_set("two_stage", ki_key, is_phase)

    # 1. Majority Baseline vs E3
    all_sets = [gtn[f"wunde_{i:02d}"] for i in range(1,61) if gtn[f"wunde_{i:02d}"]]
    set_counts = pd.Series([tuple(sorted(list(s))) for s in all_sets]).value_counts()
    top_set = set(set_counts.index[0]) if len(set_counts) > 0 else set()
    maj_f1s = [calc_f1(top_set, gtn[f"wunde_{i:02d}"]) for i in range(1,61)]
    maj_pct = (sum(maj_f1s) / len(maj_f1s)) * 100

    # 2. Random Baseline
    if is_phase:
        rand_pct = 42.5
    elif key_name == "wundrand":
        rand_pct = 33.3
    else:
        rand_pct = 28.5

    # 3. KI F1 Scores vs E3
    z_f1s = [calc_f1(z_n[f"wunde_{i:02d}"], gtn[f"wunde_{i:02d}"]) for i in range(1,61)]
    f_f1s = [calc_f1(f_n[f"wunde_{i:02d}"], gtn[f"wunde_{i:02d}"]) for i in range(1,61) if f"wunde_{i:02d}" not in FS_NURS_PROMPT_EX]
    t_f1s = [calc_f1(t_n[f"wunde_{i:02d}"], gtn[f"wunde_{i:02d}"]) for i in range(1,61)]

    z_pct = (sum(z_f1s) / len(z_f1s)) * 100
    f_pct = (sum(f_f1s) / len(f_f1s)) * 100
    t_pct = (sum(t_f1s) / len(t_f1s)) * 100

    return {
        "is_ordinal": True,
        "y_max": 100,
        "left_labels": ["Random\nBaseline", "Majority\nBaseline"],
        "left_values": [rand_pct, maj_pct],
        "left_eval_counts": [60, 60],
        "right_labels": ["Zero-Shot\nNursIT", "Few-Shot\nNursIT", "Two-Stage\nNursIT"],
        "right_values": [z_pct, f_pct, t_pct],
        "right_eval_counts": [60, len(f_f1s), 60]
    }


def calculate_category_consensus_scores(key_name, is_phase=False):
    """
    Calculates Multi-Label F1-Score % on consensus wounds across all 3 experts.
    """
    gt1_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv"), sep=";")
    gt2_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv"), sep=";")
    gtn_norm = pd.read_csv(os.path.join(BASE_DIR, "data/ground_truth/allgemeine_verbandsklassen_normalised.csv"))

    gt_key_nurs = "wundstadium" if is_phase else key_name
    ki_key_nurs = "wundphase" if is_phase else key_name

    gt1 = {f"wunde_{i:02d}": extract_phases(gt1_norm[gt1_norm["image_id"]==f"wunde_{i:02d}"][key_name].values[0]) if is_phase else parse_list(gt1_norm[gt1_norm["image_id"]==f"wunde_{i:02d}"][key_name].values[0]) for i in range(1,61)}
    gt2 = {f"wunde_{i:02d}": extract_phases(gt2_norm[gt2_norm["image_id"]==f"wunde_{i:02d}"][key_name].values[0]) if is_phase else parse_list(gt2_norm[gt2_norm["image_id"]==f"wunde_{i:02d}"][key_name].values[0]) for i in range(1,61)}
    gtn = {f"wunde_{i:02d}": extract_phases(gtn_norm[gtn_norm["image_id"]==f"wunde_{i:02d}"][gt_key_nurs].values[0]) if is_phase else parse_list(gtn_norm[gtn_norm["image_id"]==f"wunde_{i:02d}"][gt_key_nurs].values[0]) for i in range(1,61)}

    z_lr = load_ki_set("zero_shot_lr", key_name, is_phase)
    f_lr = load_ki_set("few_shot_lr", key_name, is_phase)
    t_lr = load_ki_set("two_stage_lr", key_name, is_phase)

    z_n = load_ki_set("zero_shot", ki_key_nurs, is_phase)
    f_n = load_ki_set("few_shot", ki_key_nurs, is_phase)
    t_n = load_ki_set("two_stage", ki_key_nurs, is_phase)

    consensus_wounds = {}
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        s1, s2, s3 = gt1[img_id], gt2[img_id], gtn[img_id]
        common = s1.intersection(s2).intersection(s3)
        if common:
            consensus_wounds[img_id] = common

    total_consensus = len(consensus_wounds)

    def eval_consensus(ki_dict, p_ex):
        f1_list = []
        for img_id, target in consensus_wounds.items():
            if img_id in p_ex: continue
            ki_set = ki_dict.get(img_id, set())
            f1_list.append(calc_f1(ki_set, target))
        n = len(f1_list)
        return (sum(f1_list) / n) * 100 if n > 0 else 0.0, n

    z_lr_pct, z_lr_tot = eval_consensus(z_lr, [])
    f_lr_pct, f_lr_tot = eval_consensus(f_lr, FS_LR_PROMPT_EX)
    t_lr_pct, t_lr_tot = eval_consensus(t_lr, [])

    z_n_pct, z_n_tot = eval_consensus(z_n, [])
    f_n_pct, f_n_tot = eval_consensus(f_n, FS_NURS_PROMPT_EX)
    t_n_pct, t_n_tot = eval_consensus(t_n, [])

    return {
        "is_ordinal": True,
        "y_max": 100,
        "total_consensus": total_consensus,
        "left_labels": ["Zero-Shot\nL&R", "Few-Shot\nL&R", "Two-Stage\nL&R"],
        "left_pcts": [z_lr_pct, f_lr_pct, t_lr_pct],
        "left_eval_counts": [z_lr_tot, f_lr_tot, t_lr_tot],
        "right_labels": ["Zero-Shot\nNursIT", "Few-Shot\nNursIT", "Two-Stage\nNursIT"],
        "right_pcts": [z_n_pct, f_n_pct, t_n_pct],
        "right_eval_counts": [z_n_tot, f_n_tot, t_n_tot]
    }


def calculate_wundstatus_overall_consensus_scores():
    """
    Calculates the overall average F1-Score % across all 3 Wundstatus categories on consensus wounds.
    (Wundstadium + Wundrand + Wundumgebung).
    """
    c_st = calculate_category_consensus_scores("wundstadium", is_phase=True)
    c_ra = calculate_category_consensus_scores("wundrand", is_phase=False)
    c_um = calculate_category_consensus_scores("wundumgebung", is_phase=False)

    left_avg = [(c_st["left_pcts"][i] + c_ra["left_pcts"][i] + c_um["left_pcts"][i]) / 3.0 for i in range(3)]
    right_avg = [(c_st["right_pcts"][i] + c_ra["right_pcts"][i] + c_um["right_pcts"][i]) / 3.0 for i in range(3)]

    return {
        "is_ordinal": True,
        "y_max": 100,
        "left_labels": ["Zero-Shot\nL&R", "Few-Shot\nL&R", "Two-Stage\nL&R"],
        "left_pcts": left_avg,
        "right_labels": ["Zero-Shot\nNursIT", "Few-Shot\nNursIT", "Two-Stage\nNursIT"],
        "right_pcts": right_avg
    }

