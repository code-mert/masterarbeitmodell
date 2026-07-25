import os
import sys
import pandas as pd
import numpy as np
from IPython.display import display

# Pfad-Setup
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__)) if '__file__' in globals() else os.path.abspath('')
NOTEBOOKS_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

for p in [NOTEBOOKS_DIR, BASE_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from analyse_prompts.prompt_analysis import PromptAnalysis
from eval.baselines import calc_baselines_with_exact


def create_headline_table_LR(normalised=True, display_table=True):
    """
    Erstellt die finale Headline-Tabelle für die Masterarbeit mit 4 Auswertungsspalten:
    Spalten:
      - Macro-F1 (Experte 1)
      - Exact Match (Experte 1)
      - Macro-F1 (Experte 2)
      - Exact Match (Experte 2)
    """
    pa = PromptAnalysis(normalised=normalised)

    # GT1 & GT2 Dataframes für Baselines
    gt1_df = pd.read_csv(os.path.join(BASE_DIR, "data", "ground_truth", "lohmann_rauscher", "Experte1_LR_GroundTruth_normalised.csv"), sep=";").fillna("")
    gt2_df = pd.read_csv(os.path.join(BASE_DIR, "data", "ground_truth", "lohmann_rauscher", "Experte2_LR_GroundTruth_normalised.csv"), sep=";").fillna("")

    # Baselines via eval/baselines.py
    r_f1_e1, r_ex_e1, m_f1_e1, m_ex_e1 = calc_baselines_with_exact(gt1_df)
    r_f1_e2, r_ex_e2, m_f1_e2, m_ex_e2 = calc_baselines_with_exact(gt2_df)

    # Inter-Rater
    inter_f1 = pa.df_experts['Score / F1-Score (Mean)'].mean()
    inter_ex = pa.df_experts['Exact-Match-Rate'].mean()

    # Zero-Shot
    zero_f1_e1 = pa.df_zero_exp1['Score / F1-Score (Mean)'].mean()
    zero_ex_e1 = pa.df_zero_exp1['Exact-Match-Rate'].mean()
    zero_f1_e2 = pa.df_zero_exp2['Score / F1-Score (Mean)'].mean()
    zero_ex_e2 = pa.df_zero_exp2['Exact-Match-Rate'].mean()

    # Few-Shot
    few_f1_e1 = pa.df_few_exp1['Score / F1-Score (Mean)'].mean()
    few_ex_e1 = pa.df_few_exp1['Exact-Match-Rate'].mean()
    few_f1_e2 = pa.df_few_exp2['Score / F1-Score (Mean)'].mean()
    few_ex_e2 = pa.df_few_exp2['Exact-Match-Rate'].mean()

    # 2-Stage CoT
    two_f1_e1 = pa.df_two_exp1['Score / F1-Score (Mean)'].mean()
    two_ex_e1 = pa.df_two_exp1['Exact-Match-Rate'].mean()
    two_f1_e2 = pa.df_two_exp2['Score / F1-Score (Mean)'].mean()
    two_ex_e2 = pa.df_two_exp2['Exact-Match-Rate'].mean()

    # DataFrame aufbauen
    table_data = [
        {
            "Ansatz / Baseline": "Random Baseline",
            "Macro-F1 (Experte 1)": r_f1_e1,
            "Exact Match (Experte 1)": r_ex_e1,
            "Macro-F1 (Experte 2)": r_f1_e2,
            "Exact Match (Experte 2)": r_ex_e2,
        },
        {
            "Ansatz / Baseline": "Majority Baseline",
            "Macro-F1 (Experte 1)": m_f1_e1,
            "Exact Match (Experte 1)": m_ex_e1,
            "Macro-F1 (Experte 2)": m_f1_e2,
            "Exact Match (Experte 2)": m_ex_e2,
        },
        {
            "Ansatz / Baseline": "Zero-Shot",
            "Macro-F1 (Experte 1)": zero_f1_e1,
            "Exact Match (Experte 1)": zero_ex_e1,
            "Macro-F1 (Experte 2)": zero_f1_e2,
            "Exact Match (Experte 2)": zero_ex_e2,
        },
        {
            "Ansatz / Baseline": "Few-Shot",
            "Macro-F1 (Experte 1)": few_f1_e1,
            "Exact Match (Experte 1)": few_ex_e1,
            "Macro-F1 (Experte 2)": few_f1_e2,
            "Exact Match (Experte 2)": few_ex_e2,
        },
        {
            "Ansatz / Baseline": "2-Stage CoT",
            "Macro-F1 (Experte 1)": two_f1_e1,
            "Exact Match (Experte 1)": two_ex_e1,
            "Macro-F1 (Experte 2)": two_f1_e2,
            "Exact Match (Experte 2)": two_ex_e2,
        },
        {
            "Ansatz / Baseline": "Inter-Rater (Experte 1 vs. 2)",
            "Macro-F1 (Experte 1)": inter_f1,
            "Exact Match (Experte 1)": inter_ex,
            "Macro-F1 (Experte 2)": inter_f1,
            "Exact Match (Experte 2)": inter_ex,
        }
    ]

    df_headline = pd.DataFrame(table_data)

    if display_table:
        styler = df_headline.style.format({
            "Macro-F1 (Experte 1)": "{:.1%}",
            "Exact Match (Experte 1)": "{:.1%}",
            "Macro-F1 (Experte 2)": "{:.1%}",
            "Exact Match (Experte 2)": "{:.1%}"
        }).hide(axis="index")
        
        styler = styler.set_table_styles([
            {"selector": "th", "props": [
                ("background-color", "#1d3557"), ("color", "white"),
                ("font-family", "Segoe UI, Arial, sans-serif"), ("font-size", "13px"),
                ("font-weight", "bold"), ("padding", "10px 12px"), ("border", "1px solid #d3d3d3"),
                ("text-align", "center")
            ]},
            {"selector": "td", "props": [
                ("font-family", "Segoe UI, Arial, sans-serif"), ("font-size", "13px"),
                ("padding", "8px 12px"), ("border", "1px solid #e0e0e0"),
                ("text-align", "center")
            ]},
            {"selector": "td:first-child", "props": [("text-align", "left"), ("font-weight", "bold")]},
            {"selector": "table", "props": [("border-collapse", "collapse"), ("width", "95%"), ("margin", "15px 0")]}
        ])
        
        display(styler)

    return df_headline


def get_latex_headline_table_LR(normalised=True):
    """
    Generiert einsatzbereiten LaTeX-Code für die Masterarbeit.
    """
    df = create_headline_table_LR(normalised=normalised, display_table=False)
    
    df_latex = df.copy()
    for col in ["Macro-F1 (Experte 1)", "Exact Match (Experte 1)", "Macro-F1 (Experte 2)", "Exact Match (Experte 2)"]:
        df_latex[col] = df_latex[col].apply(lambda x: f"{x*100:.1f}\\%")

    latex_str = """\\begin{table}[htbp]
\\centering
\\caption{Evaluierungsergebnisse aller Baseline-Modelle und Prompting-Ansätze im Vergleich zur Experteneinigkeit (Macro-F1 und Exact Match).}
\\label{tab:headline_results_lr}
\\begin{tabular}{lcccc}
\\hline
\\textbf{Ansatz / Baseline} & \\textbf{Macro-F1 (Exp. 1)} & \\textbf{Exact Match (Exp. 1)} & \\textbf{Macro-F1 (Exp. 2)} & \\textbf{Exact Match (Exp. 2)} \\\\
\\hline
"""
    for _, row in df_latex.iterrows():
        latex_str += f"{row['Ansatz / Baseline']} & {row['Macro-F1 (Experte 1)']} & {row['Exact Match (Experte 1)']} & {row['Macro-F1 (Experte 2)']} & {row['Exact Match (Experte 2)']} \\\\\n"
    
    latex_str += """\\hline
\\end{tabular}
\\end{table}"""
    return latex_str


if __name__ == "__main__":
    print(get_latex_headline_table_LR())
