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
    plt.close('all')
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
    plt.close(fig)


def plot_sorted_norm_comparison(df_summary_norm: pd.DataFrame):
    """
    Erstellt ein gruppiertes Balkendiagramm (einzelnes Diagramm), das für jede Kategorie
    den normalisierten F1-Score/Score und die normalisierte Exact-Match-Rate vergleicht.
    Die Kategorien sind absteigend nach dem Score/F1-Score sortiert.
    """
    # 1. Daten sortieren nach Haupt-Score absteigend
    df_sorted = df_summary_norm.sort_values(
        by="Score / F1-Score (Mean)", 
        ascending=False
    ).copy()
    
    # 2. DataFrame für Seaborn "schmelzen" (melt), um gruppiertes Balkendiagramm zu erhalten
    plot_data = []
    for _, row in df_sorted.iterrows():
        plot_data.append({
            "Kategorie": row["Kategorie"],
            "Metrik": "F1-Score / Score (normalisiert)",
            "Wert": row["Score / F1-Score (Mean)"]
        })
        plot_data.append({
            "Kategorie": row["Kategorie"],
            "Metrik": "Exact-Match-Rate (normalisiert)",
            "Wert": row["Exact-Match-Rate"]
        })
        
    df_plot = pd.DataFrame(plot_data)
    
    # 3. Design-Setup
    plt.close('all')
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Schöne HSL-kompatible Farben für die beiden Metriken
    colors = {
        "F1-Score / Score (normalisiert)": "#2a9d8f",     # Schönes Teal
        "Exact-Match-Rate (normalisiert)": "#e76f51"       # Schönes Terracotta / Orange
    }
    
    # Gruppiertes Balkendiagramm zeichnen
    sns.barplot(
        data=df_plot,
        x="Wert",
        y="Kategorie",
        hue="Metrik",
        palette=colors,
        ax=ax,
        edgecolor="black",
        linewidth=0.8
    )
    
    # Formatierung
    ax.set_title("Vergleich der normalisierten Metriken (absteigend nach Haupt-Score sortiert)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Prozentualer Wert", fontsize=11, labelpad=8)
    ax.set_ylabel("Kategorie", fontsize=11)
    ax.set_xlim(0.0, 1.08)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    
    # Legende positionieren
    ax.legend(loc="lower left", frameon=True, fontsize=10)
    
    # Balkenbeschriftungen hinzufügen
    for container in ax.containers:
        labels = [f"{v*100:.1f}%" if v > 0 else "0.0%" for v in container.datavalues]
        ax.bar_label(container, labels=labels, padding=3, fontsize=9)
        
    plt.tight_layout()
    plt.show()
    plt.close(fig)


def plot_combined_single_chart(df_experts_norm: pd.DataFrame, df_llm_norm: pd.DataFrame, expert_label: str = "Experte 1"):
    """
    Erstellt ein einzelnes gruppiertes Balkendiagramm, das für jede Kategorie 
    die Experteneinigkeit (Experte 1 vs. 2) und den LLM-Score für einen spezifischen Experten gegenüberstellt.
    Die Kategorien sind absteigend nach dem jeweiligen LLM-Experten-Score sortiert (höchste zuerst).
    """
    llm_col_name = f"LLM vs. {expert_label}"
    exp_col_name = "Experteneinigkeit (Ex1 vs. Ex2)"

    # 1. Mergen und Sortieren nach dem ausgewählten LLM-Score (höchste zuerst)
    df_merged = pd.merge(
        df_llm_norm[["Kategorie", "Score / F1-Score (Mean)"]].rename(columns={"Score / F1-Score (Mean)": llm_col_name}),
        df_experts_norm[["Kategorie", "Score / F1-Score (Mean)"]].rename(columns={"Score / F1-Score (Mean)": exp_col_name}),
        on="Kategorie"
    )

    df_sorted = df_merged.sort_values(
        by=llm_col_name, 
        ascending=False
    ).copy()

    # 2. Ins Long-Format bringen für Seaborn barplot
    plot_data = []
    for _, row in df_sorted.iterrows():
        plot_data.append({
            "Kategorie": row["Kategorie"],
            "Metrik": llm_col_name,
            "Wert": row[llm_col_name]
        })
        plot_data.append({
            "Kategorie": row["Kategorie"],
            "Metrik": exp_col_name,
            "Wert": row[exp_col_name]
        })
        
    df_plot = pd.DataFrame(plot_data)

    # 3. Einzelnen Plot erstellen
    plt.close('all')
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(13, 8))

    colors = {
        llm_col_name: "#2a9d8f",          # Schönes Teal
        exp_col_name: "#1d3557"           # Dunkelblau
    }

    sns.barplot(
        data=df_plot,
        x="Wert",
        y="Kategorie",
        hue="Metrik",
        palette=colors,
        ax=ax,
        edgecolor="black",
        linewidth=0.8
    )

    ax.set_title(f"Vergleich: Experteneinigkeit vs. {llm_col_name} (sortiert nach LLM-Score, höchste zuerst)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Prozentualer Score / F1-Score", fontsize=11, labelpad=8)
    ax.set_ylabel("Kategorie", fontsize=11)
    ax.set_xlim(0.0, 1.08)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.legend(loc="lower right", frameon=True, fontsize=10)

    for container in ax.containers:
        labels = [f"{v*100:.1f}%" if not pd.isna(v) and v > 0 else "0.0%" for v in container.datavalues]
        ax.bar_label(container, labels=labels, padding=3, fontsize=9)

    plt.tight_layout()
    plt.show()
    plt.close(fig)


def plot_combined_stage_chart(df_experts_norm: pd.DataFrame, df_llm_norm: pd.DataFrame, expert_label: str = "Experte 1"):
    """
    Erstellt ein gruppiertes Balkendiagramm, das die Kategorien nach Stage 1 (Wundbeschreibung)
    oben und Stage 2 (Wundbehandlung) unten unterteilt und für jede Kategorie die Experteneinigkeit 
    sowie den LLM-Score vergleicht.
    """
    llm_col_name = f"LLM vs. {expert_label}"
    exp_col_name = "Experteneinigkeit (Ex1 vs. Ex2)"

    stage1_cats = ["Wundtyp", "Lokalisation", "Wundstadium", "Wundgrund", "Wundrand", "Wundumgebung", "Exsudat"]
    stage2_cats = ["Debridement notwendig", "Debridement Methode", "Infektionsverdacht", "Spüllösung", "Primärverband", "Sekundärverband", "Kompression indiziert", "Kompression Produkt"]

    df_merged = pd.merge(
        df_llm_norm[["Kategorie", "Score / F1-Score (Mean)"]].rename(columns={"Score / F1-Score (Mean)": llm_col_name}),
        df_experts_norm[["Kategorie", "Score / F1-Score (Mean)"]].rename(columns={"Score / F1-Score (Mean)": exp_col_name}),
        on="Kategorie"
    )

    df_stage1 = df_merged[df_merged["Kategorie"].isin(stage1_cats)].sort_values(by=llm_col_name, ascending=False)
    df_stage2 = df_merged[df_merged["Kategorie"].isin(stage2_cats)].sort_values(by=llm_col_name, ascending=False)

    df_sorted = pd.concat([df_stage1, df_stage2]).copy()

    plot_data = []
    for _, row in df_sorted.iterrows():
        plot_data.append({
            "Kategorie": row["Kategorie"],
            "Metrik": llm_col_name,
            "Wert": row[llm_col_name]
        })
        plot_data.append({
            "Kategorie": row["Kategorie"],
            "Metrik": exp_col_name,
            "Wert": row[exp_col_name]
        })
        
    df_plot = pd.DataFrame(plot_data)

    plt.close('all')
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(13, 9))

    colors = {
        llm_col_name: "#2a9d8f",          # Teal
        exp_col_name: "#1d3557"           # Dunkelblau
    }

    sns.barplot(
        data=df_plot,
        x="Wert",
        y="Kategorie",
        hue="Metrik",
        palette=colors,
        ax=ax,
        edgecolor="black",
        linewidth=0.8
    )

    # Trennlinie zwischen Stage 1 und Stage 2
    n_stage1 = len(df_stage1)
    if n_stage1 > 0 and len(df_stage2) > 0:
        ax.axhline(n_stage1 - 0.5, color="#e76f51", linestyle="--", linewidth=1.5)

    ax.set_title(f"2-Stage Vergleich: Experteneinigkeit vs. {llm_col_name}\n(Oben: Stage 1 Wundbeschreibung | Unten: Stage 2 Wundbehandlung)", fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("Prozentualer Score / F1-Score", fontsize=11, labelpad=8)
    ax.set_ylabel("Kategorie", fontsize=11)
    ax.set_xlim(0.0, 1.08)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.legend(loc="lower right", frameon=True, fontsize=10)

    for container in ax.containers:
        labels = [f"{v*100:.1f}%" if not pd.isna(v) and v > 0 else "0.0%" for v in container.datavalues]
        ax.bar_label(container, labels=labels, padding=3, fontsize=9)

    plt.tight_layout()
    plt.show()
    plt.close(fig)


def plot_all_prompts_comparison(
    df_zero_norm: pd.DataFrame,
    df_few_norm: pd.DataFrame,
    df_two_norm: pd.DataFrame,
    df_experts_norm: pd.DataFrame = None,
    expert_label: str = "Experte 1",
    by_stage: bool = True
):
    """
    Erstellt ein gruppiertes Balkendiagramm, das die 3 Prompting-Ansätze (Zero-Shot, Few-Shot, 2-Stage CoT)
    sowie optional die Experteneinigkeit für alle 15 Kategorien vergleicht.
    """
    label_zero = "Zero-Shot"
    label_few = "Few-Shot"
    label_two = "Two-Stage"
    label_exp = "Experteneinigkeit (Ex1 vs. Ex2)"

    df_merged = pd.merge(
        df_zero_norm[["Kategorie", "Score / F1-Score (Mean)"]].rename(columns={"Score / F1-Score (Mean)": label_zero}),
        df_few_norm[["Kategorie", "Score / F1-Score (Mean)"]].rename(columns={"Score / F1-Score (Mean)": label_few}),
        on="Kategorie"
    )
    df_merged = pd.merge(
        df_merged,
        df_two_norm[["Kategorie", "Score / F1-Score (Mean)"]].rename(columns={"Score / F1-Score (Mean)": label_two}),
        on="Kategorie"
    )

    if df_experts_norm is not None:
        df_merged = pd.merge(
            df_merged,
            df_experts_norm[["Kategorie", "Score / F1-Score (Mean)"]].rename(columns={"Score / F1-Score (Mean)": label_exp}),
            on="Kategorie"
        )

    stage1_cats = ["Wundtyp", "Lokalisation", "Wundstadium", "Wundgrund", "Wundrand", "Wundumgebung", "Exsudat"]
    stage2_cats = ["Debridement notwendig", "Debridement Methode", "Infektionsverdacht", "Spüllösung", "Primärverband", "Sekundärverband", "Kompression indiziert", "Kompression Produkt"]

    if by_stage:
        df_stage1 = df_merged[df_merged["Kategorie"].isin(stage1_cats)].sort_values(by=label_two, ascending=False)
        df_stage2 = df_merged[df_merged["Kategorie"].isin(stage2_cats)].sort_values(by=label_two, ascending=False)
        df_sorted = pd.concat([df_stage1, df_stage2]).copy()
    else:
        df_sorted = df_merged.sort_values(by=label_two, ascending=False).copy()

    plot_cols = [label_zero, label_few, label_two]
    if df_experts_norm is not None:
        plot_cols.append(label_exp)

    plot_data = []
    for _, row in df_sorted.iterrows():
        for col in plot_cols:
            plot_data.append({
                "Kategorie": row["Kategorie"],
                "Ansatz": col,
                "Wert": row[col]
            })

    df_plot = pd.DataFrame(plot_data)

    plt.close('all')
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(14, 11))

    colors = {
        label_zero: "#e76f51",   # Orange/Terracotta
        label_few: "#f4a261",    # Helles Orange/Gelb
        label_two: "#2a9d8f",    # Teal/Grün
        label_exp: "#1d3557"     # Dunkelblau
    }

    sns.barplot(
        data=df_plot,
        x="Wert",
        y="Kategorie",
        hue="Ansatz",
        palette=colors,
        ax=ax,
        edgecolor="black",
        linewidth=0.7
    )

    if by_stage:
        n_stage1 = len(df_stage1)
        if n_stage1 > 0 and len(df_stage2) > 0:
            ax.axhline(n_stage1 - 0.5, color="#e76f51", linestyle="--", linewidth=1.5)

    title_subtitle = f"Vergleich aller Prompt-Ansätze (Zero-Shot vs. Few-Shot vs. 2-Stage CoT) vs. {expert_label}"
    if by_stage:
        title_subtitle += "\n(Oben: Stage 1 Wundbeschreibung | Unten: Stage 2 Wundbehandlung)"

    ax.set_title(title_subtitle, fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("Prozentualer Score / F1-Score", fontsize=11, labelpad=8)
    ax.set_ylabel("Kategorie", fontsize=11)
    ax.set_xlim(0.0, 1.08)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.legend(loc="lower right", frameon=True, fontsize=10)

    for container in ax.containers:
        labels = [f"{v*100:.1f}%" if not pd.isna(v) and v > 0 else "0.0%" for v in container.datavalues]
        ax.bar_label(container, labels=labels, padding=2, fontsize=8)

    plt.tight_layout()
    plt.show()
    plt.close(fig)








