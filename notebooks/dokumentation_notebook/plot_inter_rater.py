import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

# Pfad-Setup
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__)) if '__file__' in globals() else os.path.abspath('')
NOTEBOOKS_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

for p in [NOTEBOOKS_DIR, BASE_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from utils_notebook.LR_utils_notebook.compare_LR import calculate_experts_summary_LR

def plot_expert_inter_rater(df_experts=None, normalised=True):
    """
    Erstellt ein horizontales Balkendiagramm der Experten-Inter-Rater-Reliabilität (Experte 1 vs. Experte 2)
    über alle 15 Lohmann & Rauscher Kategorien, aufgeteilt nach Wundbeschreibung und Wundbehandlung.
    """
    if df_experts is None:
        df_experts = calculate_experts_summary_LR(normalised=normalised)
        
    wundbeschreibung_cats = [
        "Wundtyp", "Lokalisation", "Wundstadium", 
        "Wundgrund", "Wundrand", "Wundumgebung", "Exsudat"
    ]
    wundbehandlung_cats = [
        "Debridement notwendig", "Debridement Methode", "Infektionsverdacht", 
        "Spüllösung", "Primärverband", "Sekundärverband", 
        "Kompression indiziert", "Kompression Produkt"
    ]

    def assign_category_group(cat):
        if cat in wundbeschreibung_cats:
            return "Wundbeschreibung"
        elif cat in wundbehandlung_cats:
            return "Wundbehandlung"
        return "Sonstige"

    df_plot_data = df_experts.copy()
    df_plot_data["Gruppe"] = df_plot_data["Kategorie"].apply(assign_category_group)

    # Sortierung innerhalb der Gruppen nach Score absteigend
    df_wb = df_plot_data[df_plot_data["Kategorie"].isin(wundbeschreibung_cats)].sort_values(by="Score / F1-Score (Mean)", ascending=False)
    df_bh = df_plot_data[df_plot_data["Kategorie"].isin(wundbehandlung_cats)].sort_values(by="Score / F1-Score (Mean)", ascending=False)
    df_sorted = pd.concat([df_wb, df_bh]).copy()

    # Diagramm erstellen
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)

    group_colors = {
        "Wundbeschreibung": "#1f77b4",  # Blau
        "Wundbehandlung": "#2ca02c"    # Grün
    }

    sns.barplot(
        data=df_sorted,
        x="Score / F1-Score (Mean)",
        y="Kategorie",
        hue="Gruppe",
        palette=group_colors,
        ax=ax,
        edgecolor="black",
        linewidth=0.8,
        dodge=False
    )

    # Durchgezogene Trennlinie zwischen Wundbeschreibung und Wundbehandlung
    n_wb = len(df_wb)
    if n_wb > 0 and len(df_bh) > 0:
        ax.axhline(n_wb - 0.5, color="#d62728", linestyle="-", linewidth=1.8, label="Grenze Wundbeschreibung / Wundbehandlung")

    # Prozent-Labels an den Balken
    for p in ax.patches:
        width = p.get_width()
        if not np.isnan(width) and width > 0:
            y_coord = p.get_y() + p.get_height() / 2.0
            ax.text(
                width + 0.01,
                y_coord,
                f"{width * 100:.1f}%",
                va="center",
                ha="left",
                fontsize=9.5,
                fontweight="bold",
                color="#222222"
            )

    # Formatierung
    ax.set_title("Experten Inter-Rater-Reliabilität (Experte 1 vs. Experte 2)\nÜbereinstimmung über alle 15 L&R Kategorien", fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("Durchschnittlicher Score / F1-Score", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_ylabel("Kategorie", fontsize=11, fontweight="bold")
    ax.set_xlim(0.0, 1.15)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.legend(loc="lower right", frameon=True, framealpha=0.95, fontsize=10)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_expert_inter_rater()
