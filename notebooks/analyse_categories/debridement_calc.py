import os
import sys
import pandas as pd

SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../scripts"))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from create_f1_heatmap_excel import GT1_PATH, GT2_PATH, ZERO_PATH, FEW_PATH, TWO_PATH, parse_set, set_f1
from create_wundtyp_excel import parse_val_str

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
GTN_PATH = os.path.join(BASE_DIR, "data/ground_truth/allgemeine_verbandsklassen_normalised.csv")

FS_LR_PROMPT_EX = ["wunde_04", "wunde_18"]
FS_NURS_PROMPT_EX = ["wunde_18", "wunde_28"]


def norm_debridement_set(s_set):
    """
    Normalizes raw debridement method strings into 5 macro categories:
    Autolytisch, Mechanisch, Chirurgisch, Enzymatisch, Biochirurgisch.
    """
    res = set()
    for item in s_set:
        s = str(item).lower()
        if "autolyt" in s:
            res.add("Autolytisch")
        elif "mechan" in s or "debrisoft" in s or "monofilament" in s or "pad" in s or "lolly" in s:
            res.add("Mechanisch")
        elif "chirurg" in s or "scharf" in s or "skalpell" in s:
            res.add("Chirurgisch")
        elif "enzym" in s or "kollagenase" in s:
            res.add("Enzymatisch")
        elif "biochirurg" in s or "maden" in s:
            res.add("Biochirurgisch")
    return res


def calculate_debridement_notwendig_lr_scores():
    """
    Calculates L&R Debridement Notwendig (Ja/Nein Exact Match %) for Baselines and KI models (Best of Both).
    """
    gt1_norm = pd.read_csv(GT1_PATH, sep=";")
    gt2_norm = pd.read_csv(GT2_PATH, sep=";")
    df_zero = pd.read_csv(ZERO_PATH, sep=",")
    df_few = pd.read_csv(FEW_PATH, sep=",")
    df_two = pd.read_csv(TWO_PATH, sep=",")

    exp_data = []
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        r1 = gt1_norm[gt1_norm["image_id"] == img_id]
        r2 = gt2_norm[gt2_norm["image_id"] == img_id]
        v1 = parse_val_str(r1["debridement_notwendig"].values[0]) if len(r1) > 0 and "debridement_notwendig" in r1.columns else ""
        v2 = parse_val_str(r2["debridement_notwendig"].values[0]) if len(r2) > 0 and "debridement_notwendig" in r2.columns else ""
        exp_data.append({"img_id": img_id, "v1": v1, "v2": v2})

    random_pct = 50.0

    maj_ja = sum([1 for r in exp_data if r["v1"].lower() == "ja" or r["v2"].lower() == "ja"]) / len(exp_data)
    maj_nein = sum([1 for r in exp_data if r["v1"].lower() == "nein" or r["v2"].lower() == "nein"]) / len(exp_data)
    majority_pct = max(maj_ja, maj_nein) * 100

    inter_valid = [r for r in exp_data if r["v1"] in ["Ja", "Nein"] and r["v2"] in ["Ja", "Nein"]]
    inter_hits = [r for r in inter_valid if r["v1"] == r["v2"]]
    inter_pct = (len(inter_hits) / len(inter_valid)) * 100

    def eval_ki(df_m, p_ex):
        hits, tot = 0, 0
        for r in exp_data:
            if r["img_id"] in p_ex: continue
            rm = df_m[df_m["image_id"] == r["img_id"]]
            if len(rm) == 0: continue
            ki_v = str(rm["debridement_notwendig"].values[0]).strip().lower()
            if ki_v not in ["ja", "nein"]: continue
            tot += 1
            if ki_v == r["v1"].lower() or ki_v == r["v2"].lower():
                hits += 1
        return (hits / tot) * 100, hits, tot

    z_pct, z_hits, z_tot = eval_ki(df_zero, [])
    f_pct, f_hits, f_tot = eval_ki(df_few, FS_LR_PROMPT_EX)
    t_pct, t_hits, t_tot = eval_ki(df_two, [])

    return {
        "is_ordinal": False,
        "total_wounds": 60,
        "left_labels": ["Random\nBaseline", "Majority\nBaseline", "Inter-Rater\nAgreement"],
        "left_values": [random_pct, majority_pct, inter_pct],
        "left_counts": [30.0, max(maj_ja * 60, maj_nein * 60), len(inter_hits)],
        "left_totals": [60, 60, len(inter_valid)],
        "right_labels": ["Zero-Shot\nL&R", "Few-Shot\nL&R", "Two-Stage\nL&R"],
        "right_values": [z_pct, f_pct, t_pct],
        "right_counts": [z_hits, f_hits, t_hits],
        "right_totals": [z_tot, f_tot, t_tot]
    }


def calculate_debridement_notwendig_nursit_scores():
    """
    Calculates NursIT Debridement Notwendig (Ja/Nein Exact Match %) vs Experte 3.
    """
    gtn_norm = pd.read_csv(GTN_PATH)
    df_zero = pd.read_csv(ZERO_PATH, sep=",")
    df_few = pd.read_csv(FEW_PATH, sep=",")
    df_two = pd.read_csv(TWO_PATH, sep=",")

    exp3_data = {}
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        r3 = gtn_norm[gtn_norm["image_id"] == img_id]
        v3 = parse_val_str(r3["debridement_notwendig"].values[0]) if len(r3) > 0 and "debridement_notwendig" in r3.columns else ""
        exp3_data[img_id] = v3

    random_pct = 50.0
    maj_ja = sum([1 for v in exp3_data.values() if v.lower() == "ja"]) / len(exp3_data)
    maj_nein = sum([1 for v in exp3_data.values() if v.lower() == "nein"]) / len(exp3_data)
    majority_pct = max(maj_ja, maj_nein) * 100

    def eval_ki(df_m, p_ex):
        hits, tot = 0, 0
        for img_id, v3 in exp3_data.items():
            if img_id in p_ex: continue
            rm = df_m[df_m["image_id"] == img_id]
            if len(rm) == 0: continue
            ki_v = str(rm["debridement_notwendig"].values[0]).strip().lower()
            if ki_v not in ["ja", "nein"]: continue
            tot += 1
            if ki_v == v3.lower():
                hits += 1
        return (hits / tot) * 100, hits, tot

    z_pct, z_hits, z_tot = eval_ki(df_zero, [])
    f_pct, f_hits, f_tot = eval_ki(df_few, FS_NURS_PROMPT_EX)
    t_pct, t_hits, t_tot = eval_ki(df_two, [])

    return {
        "is_ordinal": False,
        "total_wounds": 60,
        "left_labels": ["Random\nBaseline", "Majority\nBaseline"],
        "left_values": [random_pct, majority_pct],
        "left_counts": [30.0, max(maj_ja * 60, maj_nein * 60)],
        "left_totals": [60, 60],
        "right_labels": ["Zero-Shot\nNursIT", "Few-Shot\nNursIT", "Two-Stage\nNursIT"],
        "right_values": [z_pct, f_pct, t_pct],
        "right_counts": [z_hits, f_hits, t_hits],
        "right_totals": [z_tot, f_tot, t_tot]
    }


def calculate_debridement_methode_lr_scores():
    """
    Calculates L&R Debridement Methode (Best-of-Both Set-F1 Score %).
    """
    gt1_norm = pd.read_csv(GT1_PATH, sep=";")
    gt2_norm = pd.read_csv(GT2_PATH, sep=";")
    df_zero = pd.read_csv(ZERO_PATH, sep=",")
    df_few = pd.read_csv(FEW_PATH, sep=",")
    df_two = pd.read_csv(TWO_PATH, sep=",")

    random_pct = 20.0
    # Single-product Majority Baseline (predicting single top item: 'Chirurgisches Debridement')
    top_lr_single = {"Chirurgisches Debridement"}
    scores_maj_lr = []
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        r1 = gt1_norm[gt1_norm["image_id"] == img_id]
        r2 = gt2_norm[gt2_norm["image_id"] == img_id]
        g1 = parse_set(r1["debridement"].values[0]) if len(r1) > 0 and "debridement" in r1.columns else set()
        g2 = parse_set(r2["debridement"].values[0]) if len(r2) > 0 and "debridement" in r2.columns else set()
        if not g1 and not g2: continue
        sc = []
        if g1: sc.append(set_f1(top_lr_single, g1))
        if g2: sc.append(set_f1(top_lr_single, g2))
        if sc: scores_maj_lr.append(max(sc))
    majority_pct = (sum(scores_maj_lr) / len(scores_maj_lr)) * 100 if scores_maj_lr else 0.0

    s_ir = []
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        r1 = gt1_norm[gt1_norm["image_id"] == img_id]
        r2 = gt2_norm[gt2_norm["image_id"] == img_id]
        g1 = parse_set(r1["debridement"].values[0]) if len(r1) > 0 and "debridement" in r1.columns else set()
        g2 = parse_set(r2["debridement"].values[0]) if len(r2) > 0 and "debridement" in r2.columns else set()
        if g1 or g2:
            s_ir.append(set_f1(g1, g2))
    inter_pct = (sum(s_ir) / len(s_ir)) * 100 if s_ir else 0.0

    def eval_ki(df_m, p_ex):
        s_ki = []
        for i in range(1, 61):
            img_id = f"wunde_{i:02d}"
            if img_id in p_ex: continue
            r1 = gt1_norm[gt1_norm["image_id"] == img_id]
            r2 = gt2_norm[gt2_norm["image_id"] == img_id]
            g1 = parse_set(r1["debridement"].values[0]) if len(r1) > 0 and "debridement" in r1.columns else set()
            g2 = parse_set(r2["debridement"].values[0]) if len(r2) > 0 and "debridement" in r2.columns else set()
            
            rm = df_m[df_m["image_id"] == img_id]
            if len(rm) == 0: continue
            ki_set = parse_set(rm["debridement_methode"].values[0]) if "debridement_methode" in rm.columns else set()
            
            if not g1 and not g2: continue
            
            scores = []
            if g1: scores.append(set_f1(ki_set, g1))
            if g2: scores.append(set_f1(ki_set, g2))
            if scores:
                s_ki.append(max(scores))
        return (sum(s_ki) / len(s_ki)) * 100, len(s_ki)

    z_pct, z_tot = eval_ki(df_zero, [])
    f_pct, f_tot = eval_ki(df_few, FS_LR_PROMPT_EX)
    t_pct, t_tot = eval_ki(df_two, [])

    return {
        "is_ordinal": True,
        "y_max": 100,
        "left_labels": ["Random\nBaseline", "Majority\nBaseline", "Inter-Rater\nAgreement"],
        "left_values": [random_pct, majority_pct, inter_pct],
        "left_eval_counts": [60, 60, len(s_ir)],
        "right_labels": ["Zero-Shot\nL&R", "Few-Shot\nL&R", "Two-Stage\nL&R"],
        "right_values": [z_pct, f_pct, t_pct],
        "right_eval_counts": [z_tot, f_tot, t_tot]
    }


def calculate_debridement_methode_nursit_scores():
    """
    Calculates NursIT Debridement Methode (Set-F1 Score %) vs Experte 3.
    """
    gtn_norm = pd.read_csv(GTN_PATH)
    df_zero = pd.read_csv(ZERO_PATH, sep=",")
    df_few = pd.read_csv(FEW_PATH, sep=",")
    df_two = pd.read_csv(TWO_PATH, sep=",")

    random_pct = 20.0
    # Single-product Majority Baseline (predicting single top item: 'Autolytisch')
    top_nurs_single = {"Autolytisch"}
    scores_maj_nurs = []
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        r3 = gtn_norm[gtn_norm["image_id"] == img_id]
        g3 = norm_debridement_set(parse_set(r3["debridement"].values[0])) if len(r3) > 0 and "debridement" in r3.columns else set()
        if not g3: continue
        scores_maj_nurs.append(set_f1(top_nurs_single, g3))
    majority_pct = (sum(scores_maj_nurs) / len(scores_maj_nurs)) * 100 if scores_maj_nurs else 0.0

    def eval_ki(df_m, p_ex):
        s_ki = []
        for i in range(1, 61):
            img_id = f"wunde_{i:02d}"
            if img_id in p_ex: continue
            r3 = gtn_norm[gtn_norm["image_id"] == img_id]
            g3 = norm_debridement_set(parse_set(r3["debridement"].values[0])) if len(r3) > 0 and "debridement" in r3.columns else set()
            
            rm = df_m[df_m["image_id"] == img_id]
            if len(rm) == 0: continue
            ki_set = norm_debridement_set(parse_set(rm["debridement_methode"].values[0])) if "debridement_methode" in rm.columns else set()
            
            if not g3 and not ki_set: continue
            s_ki.append(set_f1(ki_set, g3))
        return (sum(s_ki) / len(s_ki)) * 100, len(s_ki)

    z_pct, z_tot = eval_ki(df_zero, [])
    f_pct, f_tot = eval_ki(df_few, FS_NURS_PROMPT_EX)
    t_pct, t_tot = eval_ki(df_two, [])

    return {
        "is_ordinal": True,
        "y_max": 100,
        "left_labels": ["Random\nBaseline", "Majority\nBaseline"],
        "left_values": [random_pct, majority_pct],
        "left_eval_counts": [60, 60],
        "right_labels": ["Zero-Shot\nNursIT", "Few-Shot\nNursIT", "Two-Stage\nNursIT"],
        "right_values": [z_pct, f_pct, t_pct],
        "right_eval_counts": [z_tot, f_tot, t_tot]
    }
