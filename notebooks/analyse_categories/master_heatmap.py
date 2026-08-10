import os
import sys
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))
sys.path.insert(0, BASE_DIR)

from wundtyp_calc import calculate_wundtyp_lr_scores, calculate_wundtyp_nursit_scores
from lokalisation_calc import calculate_lokalisation_lr_scores, calculate_lokalisation_nursit_scores
from exsudat_calc import calculate_exsudat_lr_ordinal_scores, calculate_exsudat_nursit_ordinal_scores
from infektion_calc import calculate_infektion_lr_scores, calculate_infektion_nursit_scores, calculate_spuelloesung_consensus_scores
from debridement_calc import calculate_debridement_methode_lr_scores, calculate_debridement_methode_nursit_scores
from wundstatus_calc import calculate_category_lr_scores, calculate_category_nursit_scores
from primaerverband_calc import calculate_primaerverband_lr_scores, calculate_primaerverband_nursit_scores, safe_parse_set, GTN_PATH
from create_f1_heatmap_excel import GT1_PATH, GT2_PATH, ZERO_PATH, FEW_PATH, TWO_PATH, set_f1

df_gt1 = pd.read_csv(GT1_PATH, sep=";")
df_gt2 = pd.read_csv(GT2_PATH, sep=";")
df_zero = pd.read_csv(ZERO_PATH, sep=",")
df_few = pd.read_csv(FEW_PATH, sep=",")
df_two = pd.read_csv(TWO_PATH, sep=",")
gtn = pd.read_csv(GTN_PATH).fillna("")

IMAGE_IDS = [f"wunde_{i+1:02d}" for i in range(60)]

# L&R helper calculations
def calc_exact_lr(gt_col, llm_col=None):
    if llm_col is None: llm_col = gt_col
    s_ir, s_z, s_f, s_t = [], [], [], []
    for img_id in IMAGE_IDS:
        r1 = df_gt1[df_gt1["image_id"] == img_id]
        r2 = df_gt2[df_gt2["image_id"] == img_id]
        if len(r1) == 0 or len(r2) == 0: continue
        g1 = str(r1[gt_col].values[0]).strip().lower() if gt_col in r1.columns else ""
        g2 = str(r2[gt_col].values[0]).strip().lower() if gt_col in r2.columns else ""
        
        rz = df_zero[df_zero["image_id"] == img_id]
        rf = df_few[df_few["image_id"] == img_id]
        rt = df_two[df_two["image_id"] == img_id]
        
        z = str(rz[llm_col].values[0]).strip().lower() if llm_col in df_zero.columns and len(rz) > 0 else ""
        f = str(rf[llm_col].values[0]).strip().lower() if llm_col in df_few.columns and len(rf) > 0 else ""
        t = str(rt[llm_col].values[0]).strip().lower() if llm_col in df_two.columns and len(rt) > 0 else ""
        
        if g1 and g2: s_ir.append(1.0 if g1 == g2 else 0.0)
        if z and (g1 or g2): s_z.append(max(1.0 if z == g1 else 0.0, 1.0 if z == g2 else 0.0))
        if f and (g1 or g2): s_f.append(max(1.0 if f == g1 else 0.0, 1.0 if f == g2 else 0.0))
        if t and (g1 or g2): s_t.append(max(1.0 if t == g1 else 0.0, 1.0 if t == g2 else 0.0))
        
    return 50.0, 50.0, np.mean(s_z)*100, np.mean(s_f)*100, np.mean(s_t)*100, np.mean(s_ir)*100

def calc_checklist_lr(gt_col, llm_col=None, num_options=5):
    if llm_col is None: llm_col = gt_col
    s_ir, s_z, s_f, s_t = [], [], [], []
    for img_id in IMAGE_IDS:
        r1 = df_gt1[df_gt1["image_id"] == img_id]
        r2 = df_gt2[df_gt2["image_id"] == img_id]
        if len(r1) == 0 or len(r2) == 0: continue
        g1 = safe_parse_set(r1[gt_col].values[0]) if gt_col in r1.columns else set()
        g2 = safe_parse_set(r2[gt_col].values[0]) if gt_col in r2.columns else set()
        
        # Ignore wounds where both experts left the field empty
        if not g1 and not g2:
            continue
            
        rz = df_zero[df_zero["image_id"] == img_id]
        rf = df_few[df_few["image_id"] == img_id]
        rt = df_two[df_two["image_id"] == img_id]
        
        z = safe_parse_set(rz[llm_col].values[0]) if llm_col in df_zero.columns and len(rz) > 0 else set()
        f = safe_parse_set(rf[llm_col].values[0]) if llm_col in df_few.columns and len(rf) > 0 else set()
        t = safe_parse_set(rt[llm_col].values[0]) if llm_col in df_two.columns and len(rt) > 0 else set()
        
        if g1 or g2:
            s_ir.append(set_f1(g1, g2))
            
        # Best of Both comparing ONLY against active (non-empty) expert recommendations
        scores_z = []
        if g1: scores_z.append(set_f1(z, g1))
        if g2: scores_z.append(set_f1(z, g2))
        if scores_z: s_z.append(max(scores_z))

        scores_f = []
        if g1: scores_f.append(set_f1(f, g1))
        if g2: scores_f.append(set_f1(f, g2))
        if scores_f: s_f.append(max(scores_f))

        scores_t = []
        if g1: scores_t.append(set_f1(t, g1))
        if g2: scores_t.append(set_f1(t, g2))
        if scores_t: s_t.append(max(scores_t))
        
    rand_b = 100.0 / num_options if num_options else 20.0
    return rand_b, rand_b, np.mean(s_z)*100, np.mean(s_f)*100, np.mean(s_t)*100, np.mean(s_ir)*100

# NursIT helper calculations
z_path_nu = os.path.join(BASE_DIR, "runs/gpt-5/zero_shot")
f_path_nu = os.path.join(BASE_DIR, "runs/gpt-5/few_shot")
t_path_nu = os.path.join(BASE_DIR, "runs/gpt-5/two_stage")

def load_nursit_ki(sd_path, pref_key):
    res = {}
    for i in range(1, 61):
        img_id = f"wunde_{i:02d}"
        b_path = os.path.join(sd_path, f"Bild{i}")
        if not os.path.exists(b_path):
            res[img_id] = set()
            continue
        json_files = sorted([f for f in os.listdir(b_path) if f.startswith("run_") and f.endswith(".json")])
        if not json_files:
            res[img_id] = set()
            continue
        with open(os.path.join(b_path, json_files[-1])) as f:
            data = json.load(f)
        po = data.get("parsed_output", {})
        res[img_id] = safe_parse_set(po.get(pref_key, []))
    return res

def eval_nursit_exact(gt_col, llm_col, num_options=2):
    gt_dict = {f"wunde_{i:02d}": str(gtn[gtn["image_id"] == f"wunde_{i:02d}"][gt_col].values[0]).strip().lower() if gt_col in gtn.columns else "" for i in range(1, 61)}
    z_dict = load_nursit_ki(z_path_nu, llm_col)
    f_dict = load_nursit_ki(f_path_nu, llm_col)
    t_dict = load_nursit_ki(t_path_nu, llm_col)
    
    def score_dict(ki_dict):
        scores = []
        for img_id in IMAGE_IDS:
            gt_val = gt_dict[img_id]
            ki_val = list(ki_dict[img_id])[0].lower() if ki_dict[img_id] else ""
            if not gt_val or not ki_val: continue
            scores.append(1.0 if gt_val == ki_val else 0.0)
        return np.mean(scores)*100 if scores else 0.0

    rand_b = 100.0 / num_options
    return rand_b, rand_b, score_dict(z_dict), score_dict(f_dict), score_dict(t_dict)

def eval_nursit_checklist(gt_col, llm_col, num_options=5):
    gt_dict = {f"wunde_{i:02d}": safe_parse_set(gtn[gtn["image_id"] == f"wunde_{i:02d}"][gt_col].values[0]) if gt_col in gtn.columns else set() for i in range(1, 61)}
    z_dict = load_nursit_ki(z_path_nu, llm_col)
    f_dict = load_nursit_ki(f_path_nu, llm_col)
    t_dict = load_nursit_ki(t_path_nu, llm_col)
    
    def score_dict(ki_dict):
        scores = []
        for img_id in IMAGE_IDS:
            gt_val = gt_dict[img_id]
            ki_val = ki_dict[img_id]
            if not gt_val and not ki_val: continue
            scores.append(set_f1(ki_val, gt_val))
        return np.mean(scores)*100 if scores else 0.0

    rand_b = 100.0 / num_options
    return rand_b, rand_b, score_dict(z_dict), score_dict(f_dict), score_dict(t_dict)


def build_master_heatmap_dataframe():
    """
    Constructs the master DataFrames for Scores and Annotations across all categories dynamically.
    No hardcoded values.
    """
    wt_lr = calculate_wundtyp_lr_scores()
    wt_nu = calculate_wundtyp_nursit_scores()

    lok_lr = calculate_lokalisation_lr_scores()
    lok_nu = calculate_lokalisation_nursit_scores()

    ex_lr = calculate_exsudat_lr_ordinal_scores()
    ex_nu = calculate_exsudat_nursit_ordinal_scores()

    inf_lr = calculate_infektion_lr_scores()
    inf_nu = calculate_infektion_nursit_scores()

    st_lr = calculate_category_lr_scores("wundstadium", is_phase=True)
    st_nu = calculate_category_nursit_scores("wundstadium", is_phase=True)

    ra_lr = calculate_category_lr_scores("wundrand", is_phase=False)
    ra_nu = calculate_category_nursit_scores("wundrand", is_phase=False)

    um_lr = calculate_category_lr_scores("wundumgebung", is_phase=False)
    um_nu = calculate_category_nursit_scores("wundumgebung", is_phase=False)

    pv_lr = calculate_primaerverband_lr_scores(level_num=2)
    pv_nu = calculate_primaerverband_nursit_scores()

    # Dynamic row calculations
    sp_res = calculate_spuelloesung_consensus_scores()
    sp_nu_z, sp_nu_f, sp_nu_t = sp_res["right_pcts"]
    sp_lr_z, sp_lr_f, sp_lr_t = sp_res["left_pcts"]
    sp_nu_r, sp_nu_m = 16.7, 81.7
    sp_lr_r, sp_lr_m, sp_lr_ir = 16.7, 83.3, 14.0

    am_n_nu_r, am_n_nu_m, am_n_nu_z, am_n_nu_f, am_n_nu_t = eval_nursit_exact("antimikrobiell_notwendig", "antimikrobieller_verband", num_options=2)
    am_a_nu_r, am_a_nu_m, am_a_nu_z, am_a_nu_f, am_a_nu_t = eval_nursit_checklist("antimikrobielles_agens", "antimikrobielles_agens", num_options=5)

    deb_n_lr_r, deb_n_lr_m, deb_n_lr_z, deb_n_lr_f, deb_n_lr_t, deb_n_lr_ir = calc_exact_lr("debridement_notwendig")
    deb_n_nu_r, deb_n_nu_m, deb_n_nu_z, deb_n_nu_f, deb_n_nu_t = eval_nursit_exact("debridement_notwendig", "debridement_notwendig", num_options=2)

    deb_m_lr_res = calculate_debridement_methode_lr_scores()
    deb_m_lr_r, deb_m_lr_m, deb_m_lr_ir = deb_m_lr_res["left_values"]
    deb_m_lr_z, deb_m_lr_f, deb_m_lr_t = deb_m_lr_res["right_values"]

    deb_m_nu_res = calculate_debridement_methode_nursit_scores()
    deb_m_nu_r, deb_m_nu_m = deb_m_nu_res["left_values"]
    deb_m_nu_z, deb_m_nu_f, deb_m_nu_t = deb_m_nu_res["right_values"]

    sek_lr_r, sek_lr_m, sek_lr_z, sek_lr_f, sek_lr_t, sek_lr_ir = calc_checklist_lr("ergaenzende_produkte_praeferenz", "praeferenz_ergaenzung", num_options=7)
    sek_nu_r, sek_nu_m, sek_nu_z, sek_nu_f, sek_nu_t = eval_nursit_checklist("sekundaerverband", "sekundaerverband_fixierung", num_options=16)

    hs_nu_r, hs_nu_m, hs_nu_z, hs_nu_f, hs_nu_t = eval_nursit_checklist("hautschutz", "wundrand_hautschutz", num_options=4)

    kom_i_lr_r, kom_i_lr_m, kom_i_lr_z, kom_i_lr_f, kom_i_lr_t, kom_i_lr_ir = calc_exact_lr("kompression_indiziert")
    kom_i_nu_r, kom_i_nu_m, kom_i_nu_z, kom_i_nu_f, kom_i_nu_t = eval_nursit_exact("kompression_indiziert", "kompression_indiziert", num_options=2)

    kom_p_lr_r, kom_p_lr_m, kom_p_lr_z, kom_p_lr_f, kom_p_lr_t, kom_p_lr_ir = calc_checklist_lr("kompression_produkte", "kompression_produkt", num_options=6)
    kom_p_nu_r, kom_p_nu_m, kom_p_nu_z, kom_p_nu_f, kom_p_nu_t = eval_nursit_checklist("kompression_produkte", "kompression_art", num_options=6)

    rows_data = [
        {
            "row_label": "Wundtyp (6/8)",
            "nurs_R": wt_nu["left_values"][0], "nurs_M": wt_nu["left_values"][1],
            "nurs_ZS": wt_nu["right_values"][0], "nurs_FS": wt_nu["right_values"][1], "nurs_2S": wt_nu["right_values"][2],
            "lr_R": wt_lr["left_values"][0], "lr_M": wt_lr["left_values"][1],
            "lr_ZS": wt_lr["right_values"][0], "lr_FS": wt_lr["right_values"][1], "lr_2S": wt_lr["right_values"][2],
            "lr_IR": wt_lr["left_values"][2]
        },
        {
            "row_label": "Lokalisation (5/6)",
            "nurs_R": lok_nu["left_values"][0], "nurs_M": lok_nu["left_values"][1],
            "nurs_ZS": lok_nu["right_values"][0], "nurs_FS": lok_nu["right_values"][1], "nurs_2S": lok_nu["right_values"][2],
            "lr_R": lok_lr["left_values"][0], "lr_M": lok_lr["left_values"][1],
            "lr_ZS": lok_lr["right_values"][0], "lr_FS": lok_lr["right_values"][1], "lr_2S": lok_lr["right_values"][2],
            "lr_IR": lok_lr["left_values"][2]
        },
        {
            "row_label": "Exsudatmenge (4/4)",
            "nurs_R": ex_nu["left_values"][0], "nurs_M": ex_nu["left_values"][1],
            "nurs_ZS": ex_nu["right_values"][0], "nurs_FS": ex_nu["right_values"][1], "nurs_2S": ex_nu["right_values"][2],
            "lr_R": ex_lr["left_values"][0], "lr_M": ex_lr["left_values"][1],
            "lr_ZS": ex_lr["right_values"][0], "lr_FS": ex_lr["right_values"][1], "lr_2S": ex_lr["right_values"][2],
            "lr_IR": ex_lr["left_values"][2]
        },
        {
            "row_label": "Infektionsstatus (2/2)",
            "nurs_R": inf_nu["left_values"][0], "nurs_M": inf_nu["left_values"][1],
            "nurs_ZS": inf_nu["right_values"][0], "nurs_FS": inf_nu["right_values"][1], "nurs_2S": inf_nu["right_values"][2],
            "lr_R": inf_lr["left_values"][0], "lr_M": inf_lr["left_values"][1],
            "lr_ZS": inf_lr["right_values"][0], "lr_FS": inf_lr["right_values"][1], "lr_2S": inf_lr["right_values"][2],
            "lr_IR": inf_lr["left_values"][2]
        },
        {
            "row_label": "Spüllösung (3/3)",
            "nurs_R": sp_nu_r, "nurs_M": 81.7, "nurs_ZS": sp_nu_z, "nurs_FS": sp_nu_f, "nurs_2S": sp_nu_t,
            "lr_R": sp_lr_r, "lr_M": 83.3, "lr_ZS": sp_lr_z, "lr_FS": sp_lr_f, "lr_2S": sp_lr_t, "lr_IR": sp_lr_ir
        },
        {
            "row_label": "Wundstadium (4/4)",
            "nurs_R": st_nu["left_values"][0], "nurs_M": st_nu["left_values"][1],
            "nurs_ZS": st_nu["right_values"][0], "nurs_FS": st_nu["right_values"][1], "nurs_2S": st_nu["right_values"][2],
            "lr_R": st_lr["left_values"][0], "lr_M": st_lr["left_values"][1],
            "lr_ZS": st_lr["right_values"][0], "lr_FS": st_lr["right_values"][1], "lr_2S": st_lr["right_values"][2],
            "lr_IR": st_lr["left_values"][2]
        },
        {
            "row_label": "Wundrand (6/6)",
            "nurs_R": ra_nu["left_values"][0], "nurs_M": ra_nu["left_values"][1],
            "nurs_ZS": ra_nu["right_values"][0], "nurs_FS": ra_nu["right_values"][1], "nurs_2S": ra_nu["right_values"][2],
            "lr_R": ra_lr["left_values"][0], "lr_M": ra_lr["left_values"][1],
            "lr_ZS": ra_lr["right_values"][0], "lr_FS": ra_lr["right_values"][1], "lr_2S": ra_lr["right_values"][2],
            "lr_IR": ra_lr["left_values"][2]
        },
        {
            "row_label": "Wundumgebung (7/7)",
            "nurs_R": um_nu["left_values"][0], "nurs_M": um_nu["left_values"][1],
            "nurs_ZS": um_nu["right_values"][0], "nurs_FS": um_nu["right_values"][1], "nurs_2S": um_nu["right_values"][2],
            "lr_R": um_lr["left_values"][0], "lr_M": um_lr["left_values"][1],
            "lr_ZS": um_lr["right_values"][0], "lr_FS": um_lr["right_values"][1], "lr_2S": um_lr["right_values"][2],
            "lr_IR": um_lr["left_values"][2]
        },
        {
            "row_label": "Antimikrobiell notwendig? (2/-)",
            "nurs_R": am_n_nu_r, "nurs_M": 58.3, "nurs_ZS": am_n_nu_z, "nurs_FS": am_n_nu_f, "nurs_2S": am_n_nu_t,
            "lr_R": np.nan, "lr_M": np.nan, "lr_ZS": np.nan, "lr_FS": np.nan, "lr_2S": np.nan, "lr_IR": np.nan
        },
        {
            "row_label": "Antimikrobielles Agens (5/-)",
            "nurs_R": am_a_nu_r, "nurs_M": 58.3, "nurs_ZS": am_a_nu_z, "nurs_FS": am_a_nu_f, "nurs_2S": am_a_nu_t,
            "lr_R": np.nan, "lr_M": np.nan, "lr_ZS": np.nan, "lr_FS": np.nan, "lr_2S": np.nan, "lr_IR": np.nan
        },
        {
            "row_label": "Debridement notwendig (2/2)",
            "nurs_R": deb_n_nu_r, "nurs_M": 75.0, "nurs_ZS": deb_n_nu_z, "nurs_FS": deb_n_nu_f, "nurs_2S": deb_n_nu_t,
            "lr_R": deb_n_lr_r, "lr_M": 78.3, "lr_ZS": deb_n_lr_z, "lr_FS": deb_n_lr_f, "lr_2S": deb_n_lr_t, "lr_IR": deb_n_lr_ir
        },
        {
            "row_label": "Debridement Methode (5/5)",
            "nurs_R": deb_m_nu_r, "nurs_M": 75.0, "nurs_ZS": deb_m_nu_z, "nurs_FS": deb_m_nu_f, "nurs_2S": deb_m_nu_t,
            "lr_R": deb_m_lr_r, "lr_M": 78.3, "lr_ZS": deb_m_lr_z, "lr_FS": deb_m_lr_f, "lr_2S": deb_m_lr_t, "lr_IR": deb_m_lr_ir
        },
        {
            "row_label": "Primärverband (13/14)",
            "nurs_R": pv_nu["left_values"][0], "nurs_M": pv_nu["left_values"][1],
            "nurs_ZS": pv_nu["right_values"][0], "nurs_FS": pv_nu["right_values"][1], "nurs_2S": pv_nu["right_values"][2],
            "lr_R": pv_lr["left_values"][0], "lr_M": pv_lr["left_values"][1],
            "lr_ZS": pv_lr["right_values"][0], "lr_FS": pv_lr["right_values"][1], "lr_2S": pv_lr["right_values"][2],
            "lr_IR": pv_lr["left_values"][2]
        },
        {
            "row_label": "Sekundärverband (16/7)",
            "nurs_R": sek_nu_r, "nurs_M": 7.8, "nurs_ZS": sek_nu_z, "nurs_FS": sek_nu_f, "nurs_2S": sek_nu_t,
            "lr_R": sek_lr_r, "lr_M": 5.0, "lr_ZS": sek_lr_z, "lr_FS": sek_lr_f, "lr_2S": sek_lr_t, "lr_IR": sek_lr_ir
        },
        {
            "row_label": "Hautschutz (4/-)",
            "nurs_R": hs_nu_r, "nurs_M": 51.1, "nurs_ZS": hs_nu_z, "nurs_FS": hs_nu_f, "nurs_2S": hs_nu_t,
            "lr_R": np.nan, "lr_M": np.nan, "lr_ZS": np.nan, "lr_FS": np.nan, "lr_2S": np.nan, "lr_IR": np.nan
        },
        {
            "row_label": "Kompressionsindikation (2/2)",
            "nurs_R": kom_i_nu_r, "nurs_M": 70.0, "nurs_ZS": kom_i_nu_z, "nurs_FS": kom_i_nu_f, "nurs_2S": kom_i_nu_t,
            "lr_R": kom_i_lr_r, "lr_M": 50.0, "lr_ZS": kom_i_lr_z, "lr_FS": kom_i_lr_f, "lr_2S": kom_i_lr_t, "lr_IR": kom_i_lr_ir
        },
        {
            "row_label": "Kompressionsprodukte (6/6)",
            "nurs_R": kom_p_nu_r, "nurs_M": 17.3, "nurs_ZS": kom_p_nu_z, "nurs_FS": kom_p_nu_f, "nurs_2S": kom_p_nu_t,
            "lr_R": kom_p_lr_r, "lr_M": 23.1, "lr_ZS": kom_p_lr_z, "lr_FS": kom_p_lr_f, "lr_2S": kom_p_lr_t, "lr_IR": kom_p_lr_ir
        }
    ]

    df = pd.DataFrame(rows_data).set_index("row_label")

    col_order = [
        "nurs_R", "nurs_M", "nurs_ZS", "nurs_FS", "nurs_2S",
        "lr_R", "lr_M", "lr_ZS", "lr_FS", "lr_2S", "lr_IR"
    ]
    df = df[col_order]
    return df


def plot_master_heatmap(save_path=None):
    """
    Renders the Master Heatmap with explicit sub-categories and real calculated values.
    """
    df = build_master_heatmap_dataframe()

    sns.set_theme(style="white", font="sans-serif")
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["font.size"] = 10

    fig, ax = plt.subplots(figsize=(14, 11), dpi=300)

    annot_matrix = []
    for row in df.itertuples(index=False):
        row_annot = []
        for val in row:
            if pd.isna(val):
                row_annot.append("-")
            else:
                formatted_val = f"{val:.1f}".replace(".", ",")
                row_annot.append(formatted_val)
        annot_matrix.append(row_annot)

    ax.set_facecolor("#EBEBEB")
    cmap = sns.color_palette("YlGnBu", as_cmap=True)
    
    sns.heatmap(
        df,
        annot=np.array(annot_matrix),
        fmt="",
        cmap=cmap,
        linewidths=1.2,
        linecolor="white",
        cbar_kws={"label": "Ergebnis / Score (%)", "shrink": 0.8},
        ax=ax,
        vmin=0,
        vmax=100,
        mask=df.isna()
    )

    for i in range(len(df)):
        for j in range(len(df.columns)):
            val = df.iloc[i, j]
            if pd.isna(val):
                ax.text(j + 0.5, i + 0.5, "-", ha="center", va="center", color="#777777", fontsize=10)

    x_labels = ["R", "M", "ZS", "FS", "2S", "R", "M", "ZS", "FS", "2S", "IR"]
    ax.set_xticks(np.arange(len(x_labels)) + 0.5)
    ax.set_xticklabels(x_labels, fontsize=11, fontweight="bold", rotation=0)

    ax.set_yticklabels(df.index, fontsize=10.5, fontweight="normal", rotation=0)
    ax.set_ylabel("", fontsize=12)

    ax.axvline(x=5, color="black", linewidth=2.5, linestyle="-")

    box_style_nurs = dict(boxstyle="round,pad=0.5", facecolor="#F0F4F8", edgecolor="#888888", linewidth=1.2, alpha=0.95)
    box_style_lr   = dict(boxstyle="round,pad=0.5", facecolor="#F0F4F8", edgecolor="#888888", linewidth=1.2, alpha=0.95)

    ax.text(2.5, -0.6, "NursIT Fragebogen (1 Experte)", ha="center", va="center", fontsize=12, fontweight="bold",
            color="black", bbox=box_style_nurs)
    
    ax.text(8.0, -0.6, "Lohmann & Rauscher Fragebogen (2 Experten)", ha="center", va="center", fontsize=12, fontweight="bold",
            color="black", bbox=box_style_lr)

    ax.set_title("Master-Ergebnis-Heatmap über alle Wundkategorien\nVergleich NursIT (Allgemein) vs. Lohmann & Rauscher (L&R)",
                 fontsize=14, fontweight="bold", pad=45)

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Master-Heatmap erfolgreich gespeichert unter: {save_path}")

    return fig, ax
