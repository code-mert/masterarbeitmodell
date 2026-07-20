import os
import sys
import random
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
    calculate_consensus_summary_LR,
    load_csv,
    normalize_image_id
)
from utils_notebook import metrics

# Relativer Pfad vom analyse_prompts-Ordner aus
BASE_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "llm_outputs"))
GT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "ground_truth", "lohmann_rauscher"))

ZERO_RAW = os.path.join(BASE_DATA_DIR, "zero_shot_lr", "zero_shot_lr_raw.csv")
ZERO_NORM = os.path.join(BASE_DATA_DIR, "zero_shot_lr", "zero_shot_lr_normalised.csv")

FEW_RAW = os.path.join(BASE_DATA_DIR, "few_shot_lr", "few_shot_lr_raw.csv")
FEW_NORM = os.path.join(BASE_DATA_DIR, "few_shot_lr", "few_shot_lr_normalised.csv")

TWO_RAW = os.path.join(BASE_DATA_DIR, "two_stage_lr", "two_stage_lr_raw.csv")
TWO_NORM = os.path.join(BASE_DATA_DIR, "two_stage_lr", "two_stage_lr_normalised.csv")

GT1_PATH = os.path.join(GT_DIR, "Experte1_LR_GroundTruth_normalised.csv")
GT2_PATH = os.path.join(GT_DIR, "Experte2_LR_GroundTruth_normalised.csv")


class PromptAnalysis:
    """
    Klasse zur zentralen Steuerung der Auswertung aller 3 Prompting-Ansätze
    (Zero-Shot, Few-Shot, Two-Stage) im Vergleich zu Baselines und Experteneinigkeit
    mittels zweigeteiltem Dashboard (Balkendiagramm + Scorecard-Heatmap).
    """

    def __init__(self, normalised=True):
        self.normalised = normalised
        self.wund_beschr_cats = [
            'Wundtyp', 'Lokalisation', 'Wundstadium', 'Wundrand', 'Wundumgebung',
            'Exsudat', 'Debridement notwendig', 'Infektionsverdacht', 'Spüllösung', 'Kompression indiziert'
        ]
        self.produkt_cats = [
            'Debridement Methode', 'Primärverband', 'Sekundärverband', 'Kompression Produkt'
        ]
        self.all_categories = self.wund_beschr_cats + self.produkt_cats
        self._load_data()

    def _calc_baselines(self, exp_df, n_runs=100, seed=42):
        random.seed(seed)
        np.random.seed(seed)
        
        categories_config = [
            ('Wundtyp', 'wundtyp', 'exact'),
            ('Lokalisation', 'lokalisation', 'exact'),
            ('Wundstadium', 'wundstadium', 'checklist'),
            ('Wundgrund', 'wundgrund', 'checklist'),
            ('Wundrand', 'wundrand', 'checklist'),
            ('Wundumgebung', 'wundumgebung', 'checklist'),
            ('Exsudat', 'exsudat', 'ordinal'),
            ('Infektionsverdacht', 'infektion', 'exact'),
            ('Spüllösung', 'spuelloesung', 'exact'),
            ('Debridement notwendig', 'debridement_notwendig', 'exact'),
            ('Debridement Methode', 'debridement', 'checklist'),
            ('Primärverband', 'primaerverband', 'best_path'),
            ('Sekundärverband', 'sekundaerverband', 'best_path'),
            ('Kompression indiziert', 'kompression_indiziert', 'exact'),
            ('Kompression Produkt', 'kompression_produkte', 'checklist')
        ]
        
        maj_dict = {}
        rand_dict = {}
        
        for cat_name, gt_k, mtype in categories_config:
            if mtype == 'best_path':
                g_p = 'praeferenz_produkt' if cat_name == 'Primärverband' else 'ergaenzende_produkte_praeferenz'
                g_a = 'alternative_produkt' if cat_name == 'Primärverband' else 'ergaenzende_produkte_alternativ'
                
                pool = [x for x in exp_df[g_p].dropna().tolist() if str(x).strip() not in ['', '[]', '—']]
                if not pool: pool = ['suprasorb p']
                maj_pref = pd.Series(pool).value_counts().index[0] if len(pool) > 0 else ''
                
                # Majority
                m_scores = []
                for _, r in exp_df.iterrows():
                    gt_p = metrics.to_clean_set(r.get(g_p, ''))
                    gt_a = metrics.to_clean_set(r.get(g_a, ''))
                    f1, _ = metrics.best_path_f1(metrics.to_clean_set(maj_pref), set(), gt_p, gt_a)
                    m_scores.append(f1)
                maj_dict[cat_name] = float(np.mean(m_scores))
                
                # Random
                r_runs = []
                for _ in range(n_runs):
                    r_scores = []
                    for _, r in exp_df.iterrows():
                        gt_p = metrics.to_clean_set(r.get(g_p, ''))
                        gt_a = metrics.to_clean_set(r.get(g_a, ''))
                        f1, _ = metrics.best_path_f1(metrics.to_clean_set(random.choice(pool)), set(), gt_p, gt_a)
                        r_scores.append(f1)
                    r_runs.append(float(np.mean(r_scores)))
                rand_dict[cat_name] = float(np.mean(r_runs))
            else:
                pool = [x for x in exp_df[gt_k].dropna().tolist() if str(x).strip() not in ['', '[]', '—']]
                if not pool: pool = ['nein']
                maj_val = pd.Series(pool).value_counts().index[0] if len(pool) > 0 else ''
                
                # Majority
                m_scores = []
                for _, r in exp_df.iterrows():
                    gt_v = r.get(gt_k, '')
                    if mtype == 'exact': s = metrics.score_exact(gt_v, maj_val)
                    elif mtype == 'ordinal': s, _ = metrics.score_ordinal('exsudat', gt_v, maj_val)
                    elif mtype == 'checklist': s, _ = metrics.evaluate_checklist(gt_v, maj_val)
                    m_scores.append(s)
                maj_dict[cat_name] = float(np.mean(m_scores))
                
                # Random
                r_runs = []
                for _ in range(n_runs):
                    r_scores = []
                    for _, r in exp_df.iterrows():
                        gt_v = r.get(gt_k, '')
                        rand_v = random.choice(pool)
                        if mtype == 'exact': s = metrics.score_exact(gt_v, rand_v)
                        elif mtype == 'ordinal': s, _ = metrics.score_ordinal('exsudat', gt_v, rand_v)
                        elif mtype == 'checklist': s, _ = metrics.evaluate_checklist(gt_v, rand_v)
                        r_scores.append(s)
                    r_runs.append(float(np.mean(r_scores)))
                rand_dict[cat_name] = float(np.mean(r_runs))
                
        return pd.Series(rand_dict), pd.Series(maj_dict)

    def _load_data(self):
        # 1. Experteneinigkeit
        self.df_experts = calculate_experts_summary_LR(normalised=self.normalised)

        # 2. Experte 1 LLM Scores
        self.df_zero_exp1 = calculate_summary_LR(1, normalised=self.normalised, path_llm_raw=ZERO_RAW, path_llm_norm=ZERO_NORM)
        self.df_few_exp1 = calculate_summary_LR(1, normalised=self.normalised, path_llm_raw=FEW_RAW, path_llm_norm=FEW_NORM)
        self.df_two_exp1 = calculate_summary_LR(1, normalised=self.normalised, path_llm_raw=TWO_RAW, path_llm_norm=TWO_NORM)

        # 3. Experte 2 LLM Scores
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

        # 6. Baselines berechnen
        exp1_df = load_csv(GT1_PATH)
        exp2_df = load_csv(GT2_PATH)
        for df in [exp1_df, exp2_df]:
            if 'image_id' in df.columns:
                df['image_id'] = df['image_id'].apply(normalize_image_id)

        self.rand_exp1, self.maj_exp1 = self._calc_baselines(exp1_df)
        self.rand_exp2, self.maj_exp2 = self._calc_baselines(exp2_df)

    def plot_approach_expert(self, approach_name: str, expert_id: int):
        """
        Erstellt ein zweigeteiltes Dashboard (Option C):
        Links: Gruppiertes Balkendiagramm (LLM, Random, Majority, Experteneinigkeit).
        Rechts: Color-codierte Baseline Scorecard (Heatmap mit JA/NEIN für geschlagene Baselines).
        """
        if expert_id == 1:
            if approach_name == 'Zero-Shot': df_llm = self.df_zero_exp1
            elif approach_name == 'Few-Shot': df_llm = self.df_few_exp1
            else: df_llm = self.df_two_exp1
            r_base = self.rand_exp1
            m_base = self.maj_exp1
            exp_title = "Experte 1"
        else:
            if approach_name == 'Zero-Shot': df_llm = self.df_zero_exp2
            elif approach_name == 'Few-Shot': df_llm = self.df_few_exp2
            else: df_llm = self.df_two_exp2
            r_base = self.rand_exp2
            m_base = self.maj_exp2
            exp_title = "Experte 2"

        df_llm_s = df_llm.set_index('Kategorie')['Score / F1-Score (Mean)']
        df_exp_s = self.df_experts.set_index('Kategorie')['Score / F1-Score (Mean)']

        # 1. Bar Plot Daten
        plot_data = []
        for cat in self.all_categories:
            plot_data.append({'Kategorie': cat, 'Metrik': f'{approach_name} (LLM)', 'Wert': df_llm_s.get(cat, 0.0)})
            plot_data.append({'Kategorie': cat, 'Metrik': 'Random Baseline', 'Wert': r_base.get(cat, 0.0)})
            plot_data.append({'Kategorie': cat, 'Metrik': 'Majority Baseline', 'Wert': m_base.get(cat, 0.0)})
            plot_data.append({'Kategorie': cat, 'Metrik': 'Experteneinigkeit (Ex1 vs Ex2)', 'Wert': df_exp_s.get(cat, 0.0)})

        df_plot = pd.DataFrame(plot_data)

        # 2. Scorecard Matrix (Heatmap)
        heatmap_matrix = []
        text_matrix = []
        c_rand, c_maj, c_exp = 0, 0, 0

        for cat in self.all_categories:
            s_llm = df_llm_s.get(cat, 0.0)
            s_rand = r_base.get(cat, 0.0)
            s_maj = m_base.get(cat, 0.0)
            s_exp = df_exp_s.get(cat, 0.0)

            b_rand = s_llm >= s_rand
            b_maj = s_llm >= s_maj
            b_exp = s_llm >= s_exp

            if b_rand: c_rand += 1
            if b_maj: c_maj += 1
            if b_exp: c_exp += 1

            heatmap_matrix.append([1 if b_rand else 0, 1 if b_maj else 0, 1 if b_exp else 0])
            text_matrix.append(['JA' if b_rand else 'NEIN', 'JA' if b_maj else 'NEIN', 'JA' if b_exp else 'NEIN'])

        heatmap_df = pd.DataFrame(heatmap_matrix, index=self.all_categories, columns=['> Random', '> Majority', '> Experte'])
        text_df = pd.DataFrame(text_matrix, index=self.all_categories, columns=['> Random', '> Majority', '> Experte'])

        # Layout
        plt.close('all')
        sns.set_theme(style='whitegrid')
        fig, axes = plt.subplots(1, 2, figsize=(18, 11), gridspec_kw={'width_ratios': [3.0, 1.0]})

        # Subplot 1: Balkendiagramm
        llm_color = '#2a9d8f' if approach_name == 'Two-Stage' else ('#457b9d' if approach_name == 'Zero-Shot' else '#e76f51')
        colors = {
            f'{approach_name} (LLM)': llm_color,
            'Random Baseline': '#e9c46a',
            'Majority Baseline': '#f4a261',
            'Experteneinigkeit (Ex1 vs Ex2)': '#1d3557'
        }

        sns.barplot(data=df_plot, x='Wert', y='Kategorie', hue='Metrik', palette=colors, ax=axes[0], edgecolor='black', linewidth=0.7)
        axes[0].axhline(9.5, color='#e76f51', linestyle='--', linewidth=1.5)
        axes[0].set_title(f'Performance: {approach_name} vs. Baselines ({exp_title})', fontsize=13, fontweight='bold', pad=15)
        axes[0].set_xlabel('Prozentualer Score / F1-Score', fontsize=11, labelpad=8)
        axes[0].set_ylabel('')
        axes[0].set_xlim(0.0, 1.08)
        axes[0].xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        axes[0].legend(loc='lower right', frameon=True, fontsize=10)

        for container in axes[0].containers:
            labels = [f'{v*100:.1f}%' if not pd.isna(v) and v > 0 else '0.0%' for v in container.datavalues]
            axes[0].bar_label(container, labels=labels, padding=2, fontsize=7.5)

        # Subplot 2: Scorecard Heatmap
        cmap = sns.color_palette(['#e57373', '#81c784']) # Rot für NEIN, Grün für JA
        sns.heatmap(heatmap_df, annot=text_df, fmt='', cmap=cmap, cbar=False, ax=axes[1], linewidths=1.2, linecolor='white', annot_kws={'fontsize': 11, 'fontweight': 'bold'})
        axes[1].axhline(9.5, color='#e76f51', linestyle='--', linewidth=1.5)
        axes[1].set_title(f'Baseline-Scorecard\n(JA: Geschlagen | NEIN: Verfehlt)', fontsize=12, fontweight='bold', pad=15)
        axes[1].set_yticklabels([]) # Y-Achsen-Labels ausblenden, da sie links stehen
        axes[1].tick_params(axis='x', rotation=0, labelsize=10)

        # Zusatztext unten für Zusammenfassung
        n_cat = len(self.all_categories)
        fig.text(0.5, 0.01, f'Zusammenfassung {approach_name} ({exp_title}): Random geschlagen: {c_rand}/{n_cat} | Majority geschlagen: {c_maj}/{n_cat} | Experteneinigkeit übertroffen: {c_exp}/{n_cat}', 
                 ha='center', fontsize=11, fontweight='bold', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'))

        plt.tight_layout(rect=[0, 0.03, 1, 0.97])
        plt.show()

    # Convenience Methods
    def plot_zero_shot_exp1(self):
        self.plot_approach_expert('Zero-Shot', 1)

    def plot_zero_shot_exp2(self):
        self.plot_approach_expert('Zero-Shot', 2)

    def plot_few_shot_exp1(self):
        self.plot_approach_expert('Few-Shot', 1)

    def plot_few_shot_exp2(self):
        self.plot_approach_expert('Few-Shot', 2)

    def plot_two_stage_exp1(self):
        self.plot_approach_expert('Two-Stage', 1)

    def plot_two_stage_exp2(self):
        self.plot_approach_expert('Two-Stage', 2)

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
