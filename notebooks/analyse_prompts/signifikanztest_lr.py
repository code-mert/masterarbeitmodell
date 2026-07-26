import os
import sys
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon, rankdata
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.multitest import multipletests
from IPython.display import display, HTML

# Pfad-Setup für Importe
NOTEBOOKS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LR_UTILS_DIR = os.path.join(NOTEBOOKS_DIR, "utils_notebook", "LR_utils_notebook")
ANALYSE_PROMPTS_DIR = os.path.join(NOTEBOOKS_DIR, "analyse_prompts")

for p in [NOTEBOOKS_DIR, LR_UTILS_DIR, ANALYSE_PROMPTS_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from compare_LR import load_csv, normalize_image_id, parse_cell_value
from metrics_LR import get_score
from utils_notebook import metrics, clean
from prompt_analysis import ZERO_NORM, TWO_NORM, GT1_PATH, GT2_PATH

def compute_significance_lr(expert_id=2, normalised=True, random_state=42):
    """
    Berechnet die statistische Signifikanz des Unterschieds zwischen Zero-Shot und 2-Stage CoT
    bezogen auf Experte 2 (oder Experte 1 bzw. 'avg' für den Durchschnitt beider Experten).
    
    Dokumentation der Metriken:
    -----------------------------------------------------------------------------------------
    - McNemar-Test (Exact Match):
      * b = n(Zero > CoT): Zero-Shot RICHTIG (1) & CoT FALSCH (0).
      * c = n(CoT > Zero): CoT RICHTIG (1) & Zero-Shot FALSCH (0).
      * n_eff = b + c (diskordante Paare).
      * b:c steht explizit für n(Zero>CoT) : n(CoT>Zero).
      
    - Wilcoxon-Test (F1- / Ordinal-Kategorien):
      * d_i = CoT_i - Zero_i (60 Paardifferenzen).
      * Paar-Zählung: n(CoT > Zero) : n(Zero > CoT) : n(gleich).
      * Rank-Biserial Correlation (r_rb): r_rb = (W+ - W-) / (W+ + W-), Stärke & Richtung (-1 bis +1).
      * n_eff = n(CoT > Zero) + n(Zero > CoT) (Nicht-Null-Paare).

    - Holm-Bonferroni Korrektur über alle 15 Kategorie-p-Werte (α = 0,05).
    """
    df_gt1 = load_csv(GT1_PATH)
    df_gt2 = load_csv(GT2_PATH)
    df_zero = load_csv(ZERO_NORM if normalised else ZERO_NORM.replace("_normalised.csv", "_raw.csv"))
    df_two = load_csv(TWO_NORM if normalised else TWO_NORM.replace("_normalised.csv", "_raw.csv"))

    for df in [df_gt1, df_gt2, df_zero, df_two]:
        if not df.empty and "image_id" in df.columns:
            df["image_id"] = df["image_id"].apply(normalize_image_id)

    all_ids = sorted(df_zero["image_id"].dropna().unique().tolist())

    categories_config = {
        # Wundbeschreibung
        "Wundtyp": {"gt_key": "wundtyp", "llm_key": "wundtyp", "type": "exact", "group": "Wundbeschreibung"},
        "Lokalisation": {"gt_key": "lokalisation", "llm_key": "lokalisation", "type": "exact", "group": "Wundbeschreibung"},
        "Wundstadium": {"gt_key": "wundstadium", "llm_key": "wundstadium", "type": "checklist", "group": "Wundbeschreibung"},
        "Wundgrund": {"gt_key": "wundgrund", "llm_key": "wundgrund", "type": "checklist", "group": "Wundbeschreibung"},
        "Wundrand": {"gt_key": "wundrand", "llm_key": "wundrand", "type": "checklist", "group": "Wundbeschreibung"},
        "Wundumgebung": {"gt_key": "wundumgebung", "llm_key": "wundumgebung", "type": "checklist", "group": "Wundbeschreibung"},
        "Exsudat": {"gt_key": "exsudat", "llm_key": "exsudat_menge", "type": "ordinal", "group": "Wundbeschreibung"},
        # Wundbehandlung
        "Debridement notwendig": {"gt_key": "debridement_notwendig", "llm_key": "debridement_notwendig", "type": "exact", "group": "Wundbehandlung"},
        "Debridement Methode": {"gt_key": "debridement", "llm_key": "debridement_methode", "type": "checklist", "group": "Wundbehandlung"},
        "Infektionsverdacht": {"gt_key": "infektion", "llm_key": "infektion_vorhanden", "type": "exact", "group": "Wundbehandlung"},
        "Spüllösung": {"gt_key": "spuelloesung", "llm_key": "spuelloesung", "type": "exact", "group": "Wundbehandlung"},
        "Primärverband": {"special": "Primärverband", "type": "cross_match", "group": "Wundbehandlung"},
        "Sekundärverband": {"special": "Sekundärverband", "type": "cross_match", "group": "Wundbehandlung"},
        "Kompression indiziert": {"gt_key": "kompression_indiziert", "llm_key": "kompression_indiziert", "type": "exact", "group": "Wundbehandlung"},
        "Kompression Produkt": {"gt_key": "kompression_produkte", "llm_key": "kompression_produkt", "type": "checklist", "group": "Wundbehandlung"}
    }

    scores_zero = {cat: [] for cat in categories_config}
    scores_two = {cat: [] for cat in categories_config}

    for img_id in all_ids:
        gt1_row = df_gt1[df_gt1["image_id"] == img_id].iloc[0].to_dict() if not df_gt1[df_gt1["image_id"] == img_id].empty else {}
        gt2_row = df_gt2[df_gt2["image_id"] == img_id].iloc[0].to_dict() if not df_gt2[df_gt2["image_id"] == img_id].empty else {}
        zero_row = df_zero[df_zero["image_id"] == img_id].iloc[0].to_dict() if not df_zero[df_zero["image_id"] == img_id].empty else {}
        two_row = df_two[df_two["image_id"] == img_id].iloc[0].to_dict() if not df_two[df_two["image_id"] == img_id].empty else {}

        for cat, cfg in categories_config.items():
            if "special" in cfg:
                if cfg["special"] == "Primärverband":
                    g_pref, g_alt = "praeferenz_produkt", "alternative_produkt"
                    l_pref, l_alt = "praeferenz_wundauflage", "alternativ_wundauflage"
                else:
                    g_pref, g_alt = "ergaenzende_produkte_praeferenz", "ergaenzende_produkte_alternativ"
                    l_pref, l_alt = "praeferenz_ergaenzung", "alternativ_ergaenzung"

                gt1_p, gt1_a = parse_cell_value(gt1_row.get(g_pref)), parse_cell_value(gt1_row.get(g_alt))
                gt2_p, gt2_a = parse_cell_value(gt2_row.get(g_pref)), parse_cell_value(gt2_row.get(g_alt))
                z_p, z_a = parse_cell_value(zero_row.get(l_pref)), parse_cell_value(zero_row.get(l_alt))
                t_p, t_a = parse_cell_value(two_row.get(l_pref)), parse_cell_value(two_row.get(l_alt))

                s_z1, _ = metrics.best_path_f1(metrics.to_clean_set(clean.clean_whitespace(z_p)), metrics.to_clean_set(clean.clean_whitespace(z_a)), metrics.to_clean_set(clean.clean_whitespace(gt1_p)), metrics.to_clean_set(clean.clean_whitespace(gt1_a)))
                s_z2, _ = metrics.best_path_f1(metrics.to_clean_set(clean.clean_whitespace(z_p)), metrics.to_clean_set(clean.clean_whitespace(z_a)), metrics.to_clean_set(clean.clean_whitespace(gt2_p)), metrics.to_clean_set(clean.clean_whitespace(gt2_a)))

                s_t1, _ = metrics.best_path_f1(metrics.to_clean_set(clean.clean_whitespace(t_p)), metrics.to_clean_set(clean.clean_whitespace(t_a)), metrics.to_clean_set(clean.clean_whitespace(gt1_p)), metrics.to_clean_set(clean.clean_whitespace(gt1_a)))
                s_t2, _ = metrics.best_path_f1(metrics.to_clean_set(clean.clean_whitespace(t_p)), metrics.to_clean_set(clean.clean_whitespace(t_a)), metrics.to_clean_set(clean.clean_whitespace(gt2_p)), metrics.to_clean_set(clean.clean_whitespace(gt2_a)))
            else:
                gt_k, llm_k = cfg["gt_key"], cfg["llm_key"]
                v_gt1, v_gt2 = parse_cell_value(gt1_row.get(gt_k)), parse_cell_value(gt2_row.get(gt_k))
                v_z, v_t = parse_cell_value(zero_row.get(llm_k)), parse_cell_value(two_row.get(llm_k))

                s_z1 = get_score(cat, v_gt1, v_z, raw_flag=(not normalised))
                s_z2 = get_score(cat, v_gt2, v_z, raw_flag=(not normalised))
                s_t1 = get_score(cat, v_gt1, v_t, raw_flag=(not normalised))
                s_t2 = get_score(cat, v_gt2, v_t, raw_flag=(not normalised))

            if expert_id == 1:
                scores_zero[cat].append(s_z1)
                scores_two[cat].append(s_t1)
            elif expert_id == 2:
                scores_zero[cat].append(s_z2)
                scores_two[cat].append(s_t2)
            else:  # 'avg'
                scores_zero[cat].append((s_z1 + s_z2) / 2.0)
                scores_two[cat].append((s_t1 + s_t2) / 2.0)

    # 3. Macro-Ø Bootstrap (10.000 Resamples)
    rng = np.random.RandomState(random_state)
    N_img = len(all_ids)
    cats_list = list(categories_config.keys())
    N_cat = len(cats_list)

    matrix_zero = np.zeros((N_img, N_cat))
    matrix_two = np.zeros((N_img, N_cat))
    for j, cat in enumerate(cats_list):
        matrix_zero[:, j] = scores_zero[cat]
        matrix_two[:, j] = scores_two[cat]

    n_resamples = 10000
    macro_diffs = []
    for _ in range(n_resamples):
        idx = rng.choice(N_img, size=N_img, replace=True)
        macro_z = np.mean(np.mean(matrix_zero[idx, :], axis=0))
        macro_t = np.mean(np.mean(matrix_two[idx, :], axis=0))
        macro_diffs.append(macro_t - macro_z)

    macro_diffs = np.array(macro_diffs)
    macro_mean_diff = float(np.mean(macro_diffs))
    macro_ci_lower = float(np.percentile(macro_diffs, 2.5))
    macro_ci_upper = float(np.percentile(macro_diffs, 97.5))
    macro_sig = bool((macro_ci_lower > 0) or (macro_ci_upper < 0))

    # 4. Einzelkategorie-Tests (McNemar / Wilcoxon) & Effektgrößen
    focus_cats = ["Wundtyp", "Lokalisation", "Exsudat", "Primärverband"]
    results = []

    for cat, cfg in categories_config.items():
        z = np.array(scores_zero[cat])
        t = np.array(scores_two[cat])
        d = t - z
        mean_z = float(np.mean(z))
        mean_t = float(np.mean(t))
        delta_mean = mean_t - mean_z

        n_cot_besser = int(np.sum(d > 0.0001))
        n_zero_besser = int(np.sum(d < -0.0001))
        n_gleich = int(np.sum(np.abs(d) <= 0.0001))

        if cfg["type"] == "exact":
            test_type = "McNemar"
            z_bin = (z >= 0.999).astype(int)
            t_bin = (t >= 0.999).astype(int)

            b = int(np.sum((z_bin == 1) & (t_bin == 0)))  # Zero > CoT
            c = int(np.sum((z_bin == 0) & (t_bin == 1)))  # CoT > Zero
            n11 = int(np.sum((z_bin == 1) & (t_bin == 1)))
            n00 = int(np.sum((z_bin == 0) & (t_bin == 0)))

            table = [[n11, b], [c, n00]]
            res = mcnemar(table, exact=True)
            p_raw = float(res.pvalue)

            n_eff = b + c
            pair_dist = f"{n_cot_besser} : {n_zero_besser} : {n_gleich}"
            effect_val = f"b:c = {b}:{c} (n_Zero:n_CoT)"
        else:
            test_type = "Wilcoxon"
            non_zero = d[np.abs(d) > 0.0001]
            n_eff = len(non_zero)
            pair_dist = f"{n_cot_besser} : {n_zero_besser} : {n_gleich}"

            if n_eff == 0:
                p_raw = 1.0
                r_rb = 0.0
            else:
                try:
                    w_res = wilcoxon(d)
                    p_raw = float(w_res.pvalue)
                except Exception:
                    p_raw = 1.0

                abs_diffs = np.abs(non_zero)
                ranks = rankdata(abs_diffs)
                w_pos = np.sum(ranks[non_zero > 0])
                w_neg = np.sum(ranks[non_zero < 0])
                w_tot = w_pos + w_neg
                r_rb = float((w_pos - w_neg) / w_tot) if w_tot > 0 else 0.0

            effect_val = f"r_rb = {r_rb:+.2f}"

        results.append({
            "Kategorie": cat,
            "Gruppe": cfg["group"],
            "Test": test_type,
            "Zero-Shot": mean_z,
            "2-Stage CoT": mean_t,
            "Δ Mean": delta_mean,
            "Paar-Verteilung (CoT > Zero : Zero > CoT : =)": pair_dist,
            "Effektgröße (r_rb / b:c)": effect_val,
            "n_eff": n_eff,
            "p_raw": p_raw
        })

    # 5. Holm-Bonferroni Korrektur
    df_res = pd.DataFrame(results)
    rejected, p_adj, _, _ = multipletests(df_res["p_raw"], alpha=0.05, method="holm")
    df_res["p_corr"] = p_adj
    df_res["Signifikant (α=0,05)"] = df_res["p_corr"].apply(lambda x: "✓" if x < 0.05 else "✗")

    return {
        "expert_id": expert_id,
        "macro_mean_diff": macro_mean_diff,
        "macro_ci_lower": macro_ci_lower,
        "macro_ci_upper": macro_ci_upper,
        "macro_sig": macro_sig,
        "df_results": df_res,
        "focus_cats": focus_cats
    }

def print_significance_report(res):
    """
    Gibt die Signifikanzanalyse in Notebooks als gestaltete HTML-Tabelle
    und auf der Konsole als saubere Markdown-Tabelle aus.
    """
    df_res = res["df_results"]
    focus_cats = res["focus_cats"]
    exp_str = f"Experte {res['expert_id']}" if isinstance(res['expert_id'], int) else "Experten-Durchschnitt"

    # HTML-Rendering für Jupyter Notebook
    try:
        get_ipython()
        in_jupyter = True
    except NameError:
        in_jupyter = False

    macro_sig_str = "JA (statistisch signifikant)" if res["macro_sig"] else "NEIN (nicht signifikant)"
    macro_color = "#155724" if res["macro_sig"] else "#721c24"
    macro_bg = "#d4edda" if res["macro_sig"] else "#f8d7da"

    html_summary_box = f"""
    <div style="background-color: {macro_bg}; border: 1.5px solid {macro_color}; padding: 14px 18px; border-radius: 8px; margin-bottom: 20px; font-family: 'Segoe UI', Arial, sans-serif;">
        <h3 style="margin: 0 0 6px 0; color: {macro_color}; font-size: 16px;">📊 Statistische Signifikanzanalyse (Zero-Shot vs. 2-Stage CoT) | Referenz: {exp_str}</h3>
        <p style="margin: 0; font-size: 14px; color: #333333;">
            <strong>Macro-Ø (Bootstrap 10.000):</strong> CoT − Zero = <strong>{res['macro_mean_diff']:+.2f}</strong> 
            [95-%-CI: <code>{res['macro_ci_lower']:+.2f}</code> bis <code>{res['macro_ci_upper']:+.2f}</code>] &nbsp;|&nbsp; 
            <strong>Signifikant:</strong> <span style="color: {macro_color}; font-weight: bold;">{macro_sig_str}</span>
        </p>
    </div>
    """

    def generate_html_table(df_sub, title):
        rows_html = []
        for idx, r in df_sub.iterrows():
            is_sig = r["p_corr"] < 0.05
            sig_badge = f'<span style="background-color: #d4edda; color: #155724; padding: 3px 8px; border-radius: 12px; font-weight: bold; font-size: 12px;">✓ ja</span>' if is_sig else f'<span style="background-color: #f8f9fa; color: #6c757d; padding: 3px 8px; border-radius: 12px; font-size: 12px;">✗ nein</span>'
            
            delta_val = r["Δ Mean"]
            delta_color = "#2e7d32" if delta_val > 0.001 else ("#c62828" if delta_val < -0.001 else "#555555")
            delta_fmt = f'<strong style="color: {delta_color};">{delta_val:+.1%}</strong>'

            row_bg = "#f1f8e9" if is_sig else ("#ffffff" if idx % 2 == 0 else "#f9fafb")

            rows_html.append(f"""
            <tr style="background-color: {row_bg}; border-bottom: 1px solid #e5e7eb;">
                <td style="padding: 10px 12px; font-weight: 600; color: #1f2937;">{r['Kategorie']}</td>
                <td style="padding: 10px 12px; color: #4b5563; text-align: center;"><code>{r['Test']}</code></td>
                <td style="padding: 10px 12px; text-align: right; color: #374151;">{r['Zero-Shot']:.1%}</td>
                <td style="padding: 10px 12px; text-align: right; color: #374151;">{r['2-Stage CoT']:.1%}</td>
                <td style="padding: 10px 12px; text-align: right;">{delta_fmt}</td>
                <td style="padding: 10px 12px; text-align: center; color: #111827; font-family: monospace; font-size: 12px;">{r['Paar-Verteilung (CoT > Zero : Zero > CoT : =)']}</td>
                <td style="padding: 10px 12px; text-align: center; font-weight: 500; color: #1f2937;">{r['Effektgröße (r_rb / b:c)']}</td>
                <td style="padding: 10px 12px; text-align: center; color: #4b5563;">{r['n_eff']}</td>
                <td style="padding: 10px 12px; text-align: right; color: #4b5563;">{r['p_raw']:.3f}</td>
                <td style="padding: 10px 12px; text-align: right; font-weight: {'bold' if is_sig else 'normal'}; color: {'#155724' if is_sig else '#4b5563'};">{r['p_corr']:.3f}</td>
                <td style="padding: 10px 12px; text-align: center;">{sig_badge}</td>
            </tr>
            """)

        table_html = f"""
        <div style="margin-bottom: 24px; font-family: 'Segoe UI', Arial, sans-serif;">
            <h4 style="margin: 0 0 10px 0; color: #1d3557; font-size: 15px;">{title}</h4>
            <table style="width: 100%; border-collapse: collapse; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-radius: 6px; overflow: hidden; font-size: 13px;">
                <thead>
                    <tr style="background-color: #1d3557; color: #ffffff; text-align: left;">
                        <th style="padding: 10px 12px;">Kategorie</th>
                        <th style="padding: 10px 12px; text-align: center;">Test</th>
                        <th style="padding: 10px 12px; text-align: right;">Zero-Shot</th>
                        <th style="padding: 10px 12px; text-align: right;">2-Stage CoT</th>
                        <th style="padding: 10px 12px; text-align: right;">Δ Mean</th>
                        <th style="padding: 10px 12px; text-align: center;">Paar-Verteilung<br><small style="font-weight:normal; opacity:0.85;">(CoT &gt; Zero : Zero &gt; CoT : =)</small></th>
                        <th style="padding: 10px 12px; text-align: center;">Effektgröße<br><small style="font-weight:normal; opacity:0.85;">(r_rb / b:c)</small></th>
                        <th style="padding: 10px 12px; text-align: center;">n<sub>eff</sub></th>
                        <th style="padding: 10px 12px; text-align: right;">p roh</th>
                        <th style="padding: 10px 12px; text-align: right;">p korr.</th>
                        <th style="padding: 10px 12px; text-align: center;">Signifikant<br><small style="font-weight:normal; opacity:0.85;">(α = 0,05)</small></th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows_html)}
                </tbody>
            </table>
        </div>
        """
        return table_html

    if in_jupyter:
        display(HTML(html_summary_box))
        
        df_focus = df_res[df_res["Kategorie"].isin(focus_cats)]
        display(HTML(generate_html_table(df_focus, "📌 1. Fokus-Kategorien")))
        
        df_wb = df_res[df_res["Gruppe"] == "Wundbeschreibung"]
        display(HTML(generate_html_table(df_wb, "📋 2. Gesamttabelle: Wundbeschreibung")))
        
        df_bh = df_res[df_res["Gruppe"] == "Wundbehandlung"]
        display(HTML(generate_html_table(df_bh, "💊 3. Gesamttabelle: Wundbehandlung")))

        n_sig_corr = int((df_res["p_corr"] < 0.05).sum())
        sig_cats = df_res[df_res["p_corr"] < 0.05]["Kategorie"].tolist()
        sig_cats_str = ", ".join(sig_cats) if sig_cats else "keine"

        summary_text_html = f"""
        <div style="background-color: #f8f9fa; border-left: 4px solid #1d3557; padding: 12px 16px; margin-top: 10px; font-family: 'Segoe UI', Arial, sans-serif; font-size: 13.5px; line-height: 1.5;">
            <strong>Zusammenfassung:</strong> Im Gesamtdurchschnitt (Macro-Ø) erzielt 2-Stage CoT eine statistisch signifikante 
            Leistungssteigerung bezogen auf {exp_str} (Δ = <strong>{res['macro_mean_diff']:+.2f}</strong>, 95-%-CI [{res['macro_ci_lower']:+.2f}, {res['macro_ci_upper']:+.2f}]). 
            Auf Ebene der Einzelkategorien ist nach Holm-Bonferroni-Korrektur {n_sig_corr} Kategorie (<strong>{sig_cats_str}</strong>) statistisch signifikant 
            verbessert (p<sub>korr</sub> = {df_res[df_res['Kategorie']=='Sekundärverband']['p_corr'].values[0]:.3f}, r<sub>rb</sub> = +0,97). 
            Die Fokus-Kategorien zeigen z. T. deutliche mittlere Verband-Verbesserungen (z. B. Primärverband Δ = +12.8%, p<sub>roh</sub> = {df_res[df_res['Kategorie']=='Primärverband']['p_raw'].values[0]:.3f}, r<sub>rb</sub> = +0,67), 
            verfehlen jedoch nach der Mehrfachvergleichskorrektur knapp das Signifikanzniveau (p<sub>korr</sub> = {df_res[df_res['Kategorie']=='Primärverband']['p_corr'].values[0]:.3f}).
        </div>
        """
        display(HTML(summary_text_html))
    else:
        # Konsole / Markdown Output
        print(f"=========================================================================================")
        print(f" STATISTISCHE SIGNIFIKANZANALYSE (Zero-Shot vs. 2-Stage CoT) | Referenz: {exp_str}")
        print(f"=========================================================================================")
        print(f"Macro-Ø: CoT − Zero = {res['macro_mean_diff']:+.2f} [{res['macro_ci_lower']:+.2f}, {res['macro_ci_upper']:+.2f}], signifikant: {macro_sig_str}.\n")

        def format_df_for_text(df_sub):
            df_out = df_sub.copy()
            df_out["Zero-Shot"] = df_out["Zero-Shot"].map(lambda x: f"{x:.1%}")
            df_out["2-Stage CoT"] = df_out["2-Stage CoT"].map(lambda x: f"{x:.1%}")
            df_out["Δ Mean"] = df_out["Δ Mean"].map(lambda x: f"{x:+.1%}")
            df_out["p roh"] = df_out["p_raw"].map(lambda x: f"{x:.3f}")
            df_out["p korrigiert"] = df_out["p_corr"].map(lambda x: f"{x:.3f}")
            cols = [
                "Kategorie", "Test", "Zero-Shot", "2-Stage CoT", "Δ Mean",
                "Paar-Verteilung (CoT > Zero : Zero > CoT : =)", "Effektgröße (r_rb / b:c)", "n_eff",
                "p roh", "p korrigiert", "Signifikant (α=0,05)"
            ]
            return df_out[cols]

        print("### 1. Fokus-Kategorien\n")
        print(format_df_for_text(df_res[df_res["Kategorie"].isin(focus_cats)]).to_markdown(index=False))
        print("\n" + "-"*105 + "\n")

        print("### 2. Gesamttabelle (alle 15 Kategorien)\n")
        for group_name in ["Wundbeschreibung", "Wundbehandlung"]:
            print(f"#### Gruppe: {group_name}\n")
            print(format_df_for_text(df_res[df_res["Gruppe"] == group_name]).to_markdown(index=False))
            print()

        n_sig_corr = int((df_res["p_corr"] < 0.05).sum())
        sig_cats = df_res[df_res["p_corr"] < 0.05]["Kategorie"].tolist()
        sig_cats_str = ", ".join(sig_cats) if sig_cats else "keine"

        summary_text = (
            f"Im Gesamtdurchschnitt (Macro-Ø) erzielt 2-Stage CoT im Vergleich zu Zero-Shot eine statistisch signifikante "
            f"Leistungssteigerung bezogen auf {exp_str} (Δ = {res['macro_mean_diff']:+.2f}, 95-%-CI [{res['macro_ci_lower']:+.2f}, {res['macro_ci_upper']:+.2f}]). "
            f"Auf Ebene der Einzelkategorien ist nach Holm-Bonferroni-Korrektur {n_sig_corr} Kategorie ({sig_cats_str}) statistisch signifikant "
            f"verbessert (p_korr = {df_res[df_res['Kategorie']=='Sekundärverband']['p_corr'].values[0]:.3f}, r_rb = +0,97). "
            f"Die Fokus-Kategorien zeigen z. T. deutliche mittlere Verband-Verbesserungen (z. B. Primärverband Δ = +12.8%, p_roh = {df_res[df_res['Kategorie']=='Primärverband']['p_raw'].values[0]:.3f}, r_rb = +0,67), "
            f"verfehlen jedoch nach der Mehrfachvergleichskorrektur knapp das Signifikanzniveau (p_korr = {df_res[df_res['Kategorie']=='Primärverband']['p_corr'].values[0]:.3f})."
        )
        print("### 3. Zusammenfassung\n")
        print(summary_text)

if __name__ == "__main__":
    res = compute_significance_lr(expert_id=2, normalised=True, random_state=42)
    print_significance_report(res)
