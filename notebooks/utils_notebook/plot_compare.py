import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

def plot_gt_comparison(df_summary_raw: pd.DataFrame, df_summary_norm: pd.DataFrame):
    """
    Erstellt ein zweigeteiltes, gruppiertes Balkendiagramm, das den F1-Score/Haupt-Score 
    und die Exact-Match-Rate zwischen Phase 0 (Roh) und Phase 1 (Normalisiert) vergleicht.
    """
    # 1. Daten zusammenführen
    df_compare = pd.merge(
        df_summary_raw,
        df_summary_norm,
        on=["Kategorie", "Typ"],
        suffixes=("_raw", "_norm")
    )
    
    # Daten für Score/F1-Score vorbereiten
    plot_data_score = []
    # Daten für Exact Match vorbereiten
    plot_data_exact = []
    
    for _, row in df_compare.iterrows():
        # F1 / Mean Score
        plot_data_score.append({
            "Kategorie": row["Kategorie"],
            "Phase": "Phase 0 (Roh)",
            "Wert": row["Score / F1-Score (Mean)_raw"]
        })
        plot_data_score.append({
            "Kategorie": row["Kategorie"],
            "Phase": "Phase 1 (Normalisiert)",
            "Wert": row["Score / F1-Score (Mean)_norm"]
        })
        # Exact Match Rate
        plot_data_exact.append({
            "Kategorie": row["Kategorie"],
            "Phase": "Phase 0 (Roh)",
            "Wert": row["Exact-Match-Rate_raw"]
        })
        plot_data_exact.append({
            "Kategorie": row["Kategorie"],
            "Phase": "Phase 1 (Normalisiert)",
            "Wert": row["Exact-Match-Rate_norm"]
        })
        
    df_plot_score = pd.DataFrame(plot_data_score)
    df_plot_exact = pd.DataFrame(plot_data_exact)
    
    # 2. Design-Setup
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(18, 9), sharey=True)
    
    # Schöne HSL-kompatible Farben für die Phasen
    colors = {"Phase 0 (Roh)": "#e76f51", "Phase 1 (Normalisiert)": "#2a9d8f"}
    
    # --- Linker Plot: Score / F1-Score (Mean) ---
    sns.barplot(
        data=df_plot_score,
        x="Wert",
        y="Kategorie",
        hue="Phase",
        palette=colors,
        ax=axes[0],
        edgecolor="black",
        linewidth=0.8
    )
    axes[0].set_title("Haupt-Metrik: Score / F1-Score (Mean)", fontsize=13, fontweight="bold", pad=12)
    axes[0].set_xlabel("Prozentualer Score", fontsize=11, labelpad=8)
    axes[0].set_ylabel("Kategorie", fontsize=11)
    axes[0].set_xlim(0.0, 1.08)
    axes[0].xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    axes[0].get_legend().remove()
    
    # Beschriftung der Balken links
    for container in axes[0].containers:
        labels = [f"{v*100:.1f}%" if v > 0 else "0.0%" for v in container.datavalues]
        axes[0].bar_label(container, labels=labels, padding=3, fontsize=8.5)
        
    # --- Rechter Plot: Exact-Match-Rate ---
    sns.barplot(
        data=df_plot_exact,
        x="Wert",
        y="Kategorie",
        hue="Phase",
        palette=colors,
        ax=axes[1],
        edgecolor="black",
        linewidth=0.8
    )
    axes[1].set_title("Genauigkeit: Exact-Match-Rate", fontsize=13, fontweight="bold", pad=12)
    axes[1].set_xlabel("Prozentualer Score", fontsize=11, labelpad=8)
    axes[1].set_ylabel("")
    axes[1].set_xlim(0.0, 1.08)
    axes[1].xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    axes[1].get_legend().remove()
    
    # Beschriftung der Balken rechts
    for container in axes[1].containers:
        labels = [f"{v*100:.1f}%" if v > 0 else "0.0%" for v in container.datavalues]
        axes[1].bar_label(container, labels=labels, padding=3, fontsize=8.5)
        
    # Globale Legende und Titel
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.95), ncol=2, frameon=True, fontsize=11)
    fig.suptitle("Visualisierter Vergleich des Gewinns: Phase 0 (Roh) vs. Phase 1 (Normalisiert)", fontsize=16, fontweight="bold", y=0.99)
    
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.show()
