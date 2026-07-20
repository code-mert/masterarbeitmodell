import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
from IPython.display import display

# Pfad anpassen, um utils_notebook importieren zu können
notebooks_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if notebooks_dir not in sys.path:
    sys.path.insert(0, notebooks_dir)

from utils_notebook.LR_utils_notebook.compare_LR import (
    calculate_summary_LR,
    calculate_experts_summary_LR,
    calculate_consensus_summary_LR
)
from utils_notebook.plot_compare import plot_all_prompts_comparison

# Relativer Pfad vom analyse_prompts-Ordner aus
BASE_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "llm_outputs"))

ZERO_RAW = os.path.join(BASE_DATA_DIR, "zero_shot_lr", "zero_shot_lr_raw.csv")
ZERO_NORM = os.path.join(BASE_DATA_DIR, "zero_shot_lr", "zero_shot_lr_normalised.csv")

FEW_RAW = os.path.join(BASE_DATA_DIR, "few_shot_lr", "few_shot_lr_raw.csv")
FEW_NORM = os.path.join(BASE_DATA_DIR, "few_shot_lr", "few_shot_lr_normalised.csv")

TWO_RAW = os.path.join(BASE_DATA_DIR, "two_stage_lr", "two_stage_lr_raw.csv")
TWO_NORM = os.path.join(BASE_DATA_DIR, "two_stage_lr", "two_stage_lr_normalised.csv")


class PromptAnalysis:
    """
    Klasse zur zentralen Steuerung der Auswertung aller 3 Prompting-Ansätze
    (Zero-Shot, Two-Stage, Few-Shot).
    """

    def __init__(self, normalised=True):
        self.normalised = normalised
        self._load_data()

    def _load_data(self):
        # 1. Experteneinigkeit
        self.df_experts = calculate_experts_summary_LR(normalised=self.normalised)

        # 2. Experte 1
        self.df_zero_exp1 = calculate_summary_LR(1, normalised=self.normalised, path_llm_raw=ZERO_RAW, path_llm_norm=ZERO_NORM)
        self.df_few_exp1 = calculate_summary_LR(1, normalised=self.normalised, path_llm_raw=FEW_RAW, path_llm_norm=FEW_NORM)
        self.df_two_exp1 = calculate_summary_LR(1, normalised=self.normalised, path_llm_raw=TWO_RAW, path_llm_norm=TWO_NORM)

        # 3. Experte 2
        self.df_zero_exp2 = calculate_summary_LR(2, normalised=self.normalised, path_llm_raw=ZERO_RAW, path_llm_norm=ZERO_NORM)
        self.df_few_exp2 = calculate_summary_LR(2, normalised=self.normalised, path_llm_raw=FEW_RAW, path_llm_norm=FEW_NORM)
        self.df_two_exp2 = calculate_summary_LR(2, normalised=self.normalised, path_llm_raw=TWO_RAW, path_llm_norm=TWO_NORM)

        # 4. Konsens (Best of Both)
        self.df_zero_cons = calculate_consensus_summary_LR(normalised=self.normalised, path_llm_raw=ZERO_RAW, path_llm_norm=ZERO_NORM)
        self.df_few_cons = calculate_consensus_summary_LR(normalised=self.normalised, path_llm_raw=FEW_RAW, path_llm_norm=FEW_NORM)
        self.df_two_cons = calculate_consensus_summary_LR(normalised=self.normalised, path_llm_raw=TWO_RAW, path_llm_norm=TWO_NORM)

        # 5. Durchschnitte berechnen (Experte 1 & Experte 2 kombiniert)
        self.df_avg = pd.DataFrame({
            'Zero-Shot': (self.df_zero_exp1.set_index('Kategorie')['Score / F1-Score (Mean)'] + self.df_zero_exp2.set_index('Kategorie')['Score / F1-Score (Mean)']) / 2.0,
            'Few-Shot': (self.df_few_exp1.set_index('Kategorie')['Score / F1-Score (Mean)'] + self.df_few_exp2.set_index('Kategorie')['Score / F1-Score (Mean)']) / 2.0,
            'Two-Stage': (self.df_two_exp1.set_index('Kategorie')['Score / F1-Score (Mean)'] + self.df_two_exp2.set_index('Kategorie')['Score / F1-Score (Mean)']) / 2.0,
        })

        self.wund_beschr_cats = [
            'Wundtyp', 'Lokalisation', 'Wundstadium', 'Wundrand', 'Wundumgebung',
            'Exsudat', 'Debridement notwendig', 'Infektionsverdacht', 'Spüllösung', 'Kompression indiziert'
        ]
        self.produkt_cats = [
            'Debridement Methode', 'Primärverband', 'Sekundärverband', 'Kompression Produkt'
        ]

    def plot_expert1(self):
        """Plot: Detail-Vergleich aller 15 Kategorien bezogen auf Experte 1."""
        plot_all_prompts_comparison(
            self.df_zero_exp1, self.df_few_exp1, self.df_two_exp1, self.df_experts,
            expert_label="Experte 1", by_stage=True
        )

    def plot_expert2(self):
        """Plot: Detail-Vergleich aller 15 Kategorien bezogen auf Experte 2."""
        plot_all_prompts_comparison(
            self.df_zero_exp2, self.df_few_exp2, self.df_two_exp2, self.df_experts,
            expert_label="Experte 2", by_stage=True
        )

    def plot_consensus(self):
        """Plot: Detail-Vergleich aller 15 Kategorien bezogen auf Konsens (Best-of-Both)."""
        plot_all_prompts_comparison(
            self.df_zero_cons, self.df_few_cons, self.df_two_cons, self.df_experts,
            expert_label="Konsens (Best-of-Both)", by_stage=True
        )

    def plot_overview_groups(self):
        """Plot: Gegenüberstellung Wundbeschreibung vs. Produktempfehlungen & Gesamtergebnis."""
        plt.close('all')
        sns.set_theme(style='whitegrid', font_scale=1.0)
        fig, axes = plt.subplots(1, 2, figsize=(20, 9), gridspec_kw={'width_ratios': [1.4, 1]})

        colors = {'Zero-Shot': '#457b9d', 'Few-Shot': '#e76f51', 'Two-Stage': '#2a9d8f'}

        # Subplot 1: Wundbeschreibung
        df_wund = self.df_avg.loc[self.wund_beschr_cats].copy()
        df_wund.loc['--> Ø WUNDBESCHREIBUNG'] = self.df_avg.loc[self.wund_beschr_cats].mean()
        df_wund_reset = df_wund.reset_index()
        idx_c = df_wund_reset.columns[0]
        df_wund_m = df_wund_reset.melt(id_vars=idx_c, var_name='Ansatz', value_name='Score').rename(columns={idx_c: 'Kategorie'})

        sns.barplot(data=df_wund_m, x='Score', y='Kategorie', hue='Ansatz', palette=colors, ax=axes[0], edgecolor='black', linewidth=0.7)
        axes[0].set_title('Wundbeschreibung (10 Kategorien + Mittelwert)', fontsize=13, fontweight='bold', pad=12)
        axes[0].set_xlabel('Score / F1-Score (Mean)', fontsize=11)
        axes[0].set_ylabel('')
        axes[0].set_xlim(0.0, 1.05)
        axes[0].xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        for c in axes[0].containers:
            axes[0].bar_label(c, labels=[f'{v*100:.1f}%' for v in c.datavalues], padding=3, fontsize=8.5, fontweight='bold')

        # Subplot 2: Produktempfehlungen & Gesamt
        df_prod = self.df_avg.loc[self.produkt_cats].copy()
        df_prod.loc['--> Ø PRODUKTEMPFEHLUNGEN'] = self.df_avg.loc[self.produkt_cats].mean()
        df_prod.loc['===> Ø GESAMT (14 KAT.)'] = self.df_avg.loc[self.wund_beschr_cats + self.produkt_cats].mean()
        df_prod_reset = df_prod.reset_index()
        idx_cp = df_prod_reset.columns[0]
        df_prod_m = df_prod_reset.melt(id_vars=idx_cp, var_name='Ansatz', value_name='Score').rename(columns={idx_cp: 'Kategorie'})

        sns.barplot(data=df_prod_m, x='Score', y='Kategorie', hue='Ansatz', palette=colors, ax=axes[1], edgecolor='black', linewidth=0.7)
        axes[1].set_title('Produktempfehlungen & Gesamtergebnis', fontsize=13, fontweight='bold', pad=12)
        axes[1].set_xlabel('Score / F1-Score (Mean)', fontsize=11)
        axes[1].set_ylabel('')
        axes[1].set_xlim(0.0, 1.05)
        axes[1].xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        for c in axes[1].containers:
            axes[1].bar_label(c, labels=[f'{v*100:.1f}%' for v in c.datavalues], padding=3, fontsize=8.5, fontweight='bold')

        axes[0].get_legend().remove()
        axes[1].legend(title='LLM Ansatz', frameon=True, facecolor='white', framealpha=0.9, fontsize=11)
        fig.suptitle('Performance-Vergleich der 3 LLM-Ansätze (Lohmann & Rauscher Evaluierung)', fontsize=16, fontweight='bold', y=0.98)

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()

    def show_summary_table(self):
        """Zeigt die Übersichtstabelle mit Prozentwerten für alle Kategorien & Gruppen an."""
        df_summary = self.df_avg.copy()
        df_summary.loc['--- Ø WUNDBESCHREIBUNG ---'] = self.df_avg.loc[self.wund_beschr_cats].mean()
        df_summary.loc['--- Ø PRODUKTEMPFEHLUNGEN ---'] = self.df_avg.loc[self.produkt_cats].mean()
        df_summary.loc['=== Ø GESAMTDURCHSCHNITT ==='] = self.df_avg.loc[self.wund_beschr_cats + self.produkt_cats].mean()
        display(df_summary.map(lambda x: f"{x*100:.1f}%"))
