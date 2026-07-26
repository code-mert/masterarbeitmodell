import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import seaborn as sns

# Pfad-Setup
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__)) if '__file__' in globals() else os.path.abspath('')
NOTEBOOKS_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

for p in [NOTEBOOKS_DIR, BASE_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from analyse_prompts.prompt_analysis import PromptAnalysis
from eval.baselines import calc_baselines_with_exact

def plot_results_heatmap_LR(
    expert_id: int = 2,
    metric_type: str = "f1",  # "f1" oder "exact"
    normalised: bool = True,
    cmap: str = "Blues"
):
    """
    Erstellt eine dreigeteilte wissenschaftliche Ergebnis-Heatmap (Baselines | LLM-Ansätze | Referenz)
    mit physischem Spaltabstand und optischer Hervorhebung des LLM-Zentrums.
    
    Arguments:
        expert_id: 1 oder 2 (Scoring gegen Experte 1 oder Experte 2)
        metric_type: "f1" (Macro-F1) oder "exact" (Exact Match Rate)
        normalised: True für normalisierte Daten
        cmap: Matplotlib/Seaborn Colormap Name (Default: "Blues")
        
    Returns:
        matplotlib.figure.Figure
    """
    pa = PromptAnalysis(normalised=normalised)
    
    # 1. Clusters & Kategorien definieren
    clusters = [
        ("Wundcharakterisierung", ["Wundtyp", "Lokalisation", "Wundstadium", "Wundrand", "Wundumgebung", "Exsudat"]),
        ("Debridement & Reinigung", ["Debridement notwendig", "Debridement Methode", "Infektionsverdacht", "Spüllösung"]),
        ("Verband", ["Primärverband", "Sekundärverband"]),
        ("Kompression", ["Kompression indiziert", "Kompression Produkt"])
    ]
    
    cat_order = []
    cluster_ranges = {}
    idx = 0
    for c_name, c_cats in clusters:
        start_idx = idx
        for cat in c_cats:
            cat_order.append((cat, c_name))
            idx += 1
        end_idx = idx
        cluster_ranges[c_name] = (start_idx, end_idx)

    # 2. GT & Baselines laden
    gt_filename = f"Experte{expert_id}_LR_GroundTruth_normalised.csv" if normalised else f"Experte{expert_id}_LR_GroundTruth.csv"
    gt_df = pd.read_csv(os.path.join(BASE_DIR, "data", "ground_truth", "lohmann_rauscher", gt_filename), sep=";").fillna("")
    
    r_f1_d, r_ex_d, m_f1_d, m_ex_d = calc_baselines_with_exact(gt_df, return_dicts=True)
    rand_dict = r_ex_d if metric_type == "exact" else r_f1_d
    maj_dict = m_ex_d if metric_type == "exact" else m_f1_d
    
    # Prompting Ansätze laden
    if expert_id == 1:
        df_zero = pa.df_zero_exp1
        df_few = pa.df_few_exp1
        df_two = pa.df_two_exp1
    else:
        df_zero = pa.df_zero_exp2
        df_few = pa.df_few_exp2
        df_two = pa.df_two_exp2
        
    val_col = "Exact-Match-Rate" if metric_type == "exact" else "Score / F1-Score (Mean)"
    
    s_zero = df_zero.set_index("Kategorie")[val_col]
    s_few = df_few.set_index("Kategorie")[val_col]
    s_two = df_two.set_index("Kategorie")[val_col]
    s_exp = pa.df_experts.set_index("Kategorie")[val_col]
    
    # 3. Heatmap Dataframes für die 3 optischen Gruppen erzeugen
    row_labels = [cat for cat, _ in cat_order]
    
    base_rows, llm_rows, ref_rows = [], [], []
    for cat, c_name in cat_order:
        base_rows.append({
            "Random": rand_dict.get(cat, 0.0),
            "Majority": maj_dict.get(cat, 0.0)
        })
        llm_rows.append({
            "Zero-Shot": s_zero.get(cat, 0.0),
            "Few-Shot": s_few.get(cat, 0.0),
            "2-Stage CoT": s_two.get(cat, 0.0)
        })
        ref_rows.append({
            "Inter-Rater": s_exp.get(cat, 0.0)
        })
        
    df_base = pd.DataFrame(base_rows, index=row_labels)
    df_llm = pd.DataFrame(llm_rows, index=row_labels)
    df_ref = pd.DataFrame(ref_rows, index=row_labels)
    
    # Macro-Ø Fußzeile berechnen (Mittelwerte entsprechen exakt der Headline-Tabelle)
    df_base.loc["Macro-Ø"] = df_base.mean(axis=0)
    df_llm.loc["Macro-Ø"] = df_llm.mean(axis=0)
    df_ref.loc["Macro-Ø"] = df_ref.mean(axis=0)

    # 4. Dreigeteiltes Grid aufbauen (mit echtem Spalt-Abstand wspace)
    sns.set_theme(style="white")
    fig = plt.figure(figsize=(11, 13), dpi=300)
    
    gs = gridspec.GridSpec(
        1, 4,
        width_ratios=[2, 3, 1, 0.15], # Spaltenverhältnis: Baselines(2) | LLMs(3) | Referenz(1) | Colorbar
        wspace=0.10 # Physischer Spalt-Abstand zwischen den 3 Gruppen
    )
    
    ax_base = fig.add_subplot(gs[0, 0])
    ax_llm = fig.add_subplot(gs[0, 1], sharey=ax_base)
    ax_ref = fig.add_subplot(gs[0, 2], sharey=ax_base)
    cbar_ax = fig.add_subplot(gs[0, 3])
    
    norm_kwargs = dict(
        annot=True,
        fmt=".1f",
        annot_kws={"size": 9.5, "weight": "normal"},
        cmap=cmap,
        linewidths=0.5,
        linecolor="white",
        vmin=0.0,
        vmax=100.0
    )
    
    # Heatmaps zeichnen
    sns.heatmap(df_base * 100.0, ax=ax_base, cbar=False, **norm_kwargs)
    sns.heatmap(df_llm * 100.0, ax=ax_llm, cbar=False, **norm_kwargs)
    sns.heatmap(
        df_ref * 100.0,
        ax=ax_ref,
        cbar=True,
        cbar_ax=cbar_ax,
        cbar_kws={"label": "Score in %", "orientation": "vertical", "shrink": 0.8},
        **norm_kwargs
    )
    
    # Text-Luminanz & Lesbarkeit in allen 3 Subplots anpassen
    for ax in [ax_base, ax_llm, ax_ref]:
        for text in ax.texts:
            val_str = text.get_text()
            try:
                val = float(val_str)
                text.set_text(f"{val:.1f}")
                if val >= 55.0:
                    text.set_color("#ffffff")
                else:
                    text.set_color("#222222")
                text.set_weight("normal")
                text.set_fontsize(9.5)
            except ValueError:
                pass

    # 5. Gruppen-Super-Header & Spalten-Dämpfung
    ax_base.set_title("Baselines", fontsize=11, fontweight="bold", color="#666666", pad=12)
    ax_llm.set_title("LLM-Ansätze", fontsize=12, fontweight="bold", color="#1d3557", pad=12)
    ax_ref.set_title("Referenz", fontsize=11, fontweight="bold", color="#666666", pad=12)
    
    # Spaltenbeschriftungen stylen (Gedämpft für Baselines/Referenz, im Fokus für LLMs)
    for t in ax_base.get_xticklabels():
        t.set_color("#666666")
        t.set_fontsize(9.5)
    for t in ax_llm.get_xticklabels():
        t.set_color("#1d3557")
        t.set_fontweight("bold")
        t.set_fontsize(10.5)
    for t in ax_ref.get_xticklabels():
        t.set_color("#666666")
        t.set_fontsize(9.5)
        
    # Y-Achsen Labels nur links (ax_base) anzeigen, bei den anderen ausblenden
    ax_base.set_yticklabels(row_labels + ["Macro-Ø"], rotation=0, fontsize=10)
    ax_base.get_yticklabels()[14].set_weight("bold")
    ax_base.get_yticklabels()[14].set_color("#1d3557")
    
    ax_llm.yaxis.set_visible(False)
    ax_ref.yaxis.set_visible(False)

    # 6. Trennlinien & Verband-Highlight über alle 3 Subplots zeichnen
    verband_start, verband_end = cluster_ranges["Verband"]
    
    for ax_sub, num_cols in [(ax_base, 2), (ax_llm, 3), (ax_ref, 1)]:
        # Trennlinie über Macro-Ø
        ax_sub.axhline(14, color="#111111", linewidth=1.8)
        
        # Cluster-Trennlinien
        for c_name, (start_idx, end_idx) in cluster_ranges.items():
            if end_idx < 14:
                ax_sub.axhline(end_idx, color="#888888", linestyle="-", linewidth=0.8)

        # Highlight-Rahmen für Verband-Cluster
        is_center = (ax_sub == ax_llm)
        rect = patches.Rectangle(
            (0, verband_start),
            num_cols,
            (verband_end - verband_start),
            linewidth=2.2 if is_center else 1.2,
            edgecolor="#2b5c8f", # Dezentes Marineblau
            facecolor="none",
            zorder=10
        )
        ax_sub.add_patch(rect)
        ax_sub.tick_params(left=False)

    # Haupttitel
    metric_label = "Exact Match" if metric_type == "exact" else "Macro-F1"
    fig.suptitle(f"Ansatzvergleich – {metric_label} vs. Experte {expert_id}", fontsize=13, fontweight="bold", y=0.98)
    
    plt.show()
    return fig

if __name__ == "__main__":
    plot_results_heatmap_LR(expert_id=2, metric_type="f1")
