from typing import Tuple, Dict, Any, List
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

COLORS_PROMPTS = {
    "Zero-Shot": "#2a9d8f",
    "Few-Shot": "#e76f51",
    "2-Stage CoT": "#e9c46a"
}

def prepare_combined_dataframe(sum_zs_norm: pd.DataFrame, sum_fs_norm: pd.DataFrame, sum_2s_norm: pd.DataFrame) -> pd.DataFrame:
    """
    Fügt die normalisierten Summary-DataFrames der 3 Prompting-Ansätze 
    mit entsprechenden Ansatz-Labels zusammen.
    """
    zs_labeled = sum_zs_norm.copy()
    zs_labeled["Ansatz"] = "Zero-Shot"

    fs_labeled = sum_fs_norm.copy()
    fs_labeled["Ansatz"] = "Few-Shot"

    ts_labeled = sum_2s_norm.copy()
    ts_labeled["Ansatz"] = "2-Stage CoT"

    return pd.concat([zs_labeled, fs_labeled, ts_labeled], ignore_index=True)


def plot_all_prompts_comparison(
    sum_zs_norm: pd.DataFrame, 
    sum_fs_norm: pd.DataFrame, 
    sum_2s_norm: pd.DataFrame, 
    title: str = "Gesamtvergleich aller 17 Kategorien über alle 3 Prompting-Ansätze (F1-Score / Mean Score)"
):
    """
    Erstellt ein gruppiertes Balkendiagramm, das die normalisierten F1-Scores / Mean Scores
    aller 17 Kategorien für Zero-Shot, Few-Shot und 2-Stage CoT nebeneinander vergleicht.
    """
    df_all_prompts = prepare_combined_dataframe(sum_zs_norm, sum_fs_norm, sum_2s_norm)

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(14, 10))

    category_order = df_all_prompts.groupby("Kategorie")["Score / F1-Score (Mean)"].mean().sort_values(ascending=False).index

    sns.barplot(
        data=df_all_prompts,
        y="Kategorie",
        x="Score / F1-Score (Mean)",
        hue="Ansatz",
        order=category_order,
        palette=COLORS_PROMPTS,
        ax=ax,
        edgecolor="black",
        linewidth=0.8
    )

    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Prozentualer F1-Score / Mean Score", fontsize=12)
    ax.set_ylabel("Kategorie", fontsize=12)
    ax.set_xlim(0, 1.12)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.legend(title="Prompting-Ansatz", title_fontsize="11", fontsize="10", loc="lower right")

    for container in ax.containers:
        labels = [f"{v*100:.1f}%" if v > 0 else "0.0%" for v in container.datavalues]
        ax.bar_label(container, labels=labels, padding=3, fontsize=8)

    plt.tight_layout()
    try:
        plt.show()
    except Exception:
        pass


def plot_product_prompts_comparison(
    sum_zs_norm: pd.DataFrame, 
    sum_fs_norm: pd.DataFrame, 
    sum_2s_norm: pd.DataFrame, 
    title: str = "Fokus-Vergleich der Produktempfehlungen (Primär- & Sekundärverband)"
):
    """
    Erstellt ein gruppiertes Balkendiagramm für den Direktvergleich der 3 Ansätze 
    ausschließlich für Primär- und Sekundärverband.
    """
    df_all_prompts = prepare_combined_dataframe(sum_zs_norm, sum_fs_norm, sum_2s_norm)
    df_products_only = df_all_prompts[df_all_prompts["Kategorie"].isin(["primaerverband", "sekundaerverband"])].copy()

    category_labels = {
        "primaerverband": "1. Primärverband (Best-Path F1)",
        "sekundaerverband": "4. Sekundärverband / Fixierung"
    }
    df_products_only["Kategorie_Label"] = df_products_only["Kategorie"].map(category_labels)

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        data=df_products_only,
        x="Kategorie_Label",
        y="Score / F1-Score (Mean)",
        hue="Ansatz",
        palette=COLORS_PROMPTS,
        ax=ax,
        edgecolor="black",
        linewidth=0.8
    )

    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Produktkategorie", fontsize=12)
    ax.set_ylabel("F1-Score (Mean Score)", fontsize=12)
    ax.set_ylim(0, 1.15)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.legend(title="Prompting-Ansatz", title_fontsize="11", fontsize="10", loc="upper right")

    for container in ax.containers:
        labels = [f"{v*100:.1f}%" if v > 0 else "0.0%" for v in container.datavalues]
        ax.bar_label(container, labels=labels, padding=4, fontsize=10, fontweight="bold")

    plt.tight_layout()
    try:
        plt.show()
    except Exception:
        pass


def evaluate_and_plot_combined_product_set(
    csv_path: str,
    json_dir_zs: str,
    json_dir_fs: str,
    json_dir_2s: str,
    title: str = "Vergleich des Gesamt-Produktsets (Primär- + Sekundärverband + Hautschutz) pro Wundbild"
) -> pd.DataFrame:
    """
    Fügt für jedes Wundbild alle empfohlenen Produkte aus Primärverband, Sekundärverband und Hautschutz
    zu einem einzigen Gesamt-Set zusammen und vergleicht das LLM-Gesamtset mit dem GT-Gesamtset.
    Plottet Phase 0 (Roh) vs Phase 1 (Normalisiert) für alle 3 Ansätze.
    """
    from eval.loaders import load_ground_truth, load_llm_outputs, matched_image_ids
    from utils_notebook import clean, metrics

    gt_data = load_ground_truth(csv_path)

    def _eval_dir(json_dir, raw=False):
        llm_data = load_llm_outputs(json_dir)
        matched_ids = matched_image_ids(gt_data, llm_data)
        f1_list = []
        for img_id in matched_ids:
            gt_rec = gt_data[img_id]
            llm_rec = llm_data[img_id]

            gt_p = gt_rec.get("praeferenz_produkt") or []
            gt_a = gt_rec.get("alternative_produkt") or []
            gt_s = gt_rec.get("sekundaerverband") or []
            gt_h = gt_rec.get("hautschutz") or []

            llm_p = llm_rec.get("praeferenz_verbandklasse") or []
            llm_a = llm_rec.get("alternativ_verbandklasse") or []
            llm_s = llm_rec.get("sekundaerverband_fixierung") or []
            llm_h = llm_rec.get("wundrand_hautschutz") or []

            if raw:
                gt_set = metrics.to_clean_set(gt_p) | metrics.to_clean_set(gt_a) | metrics.to_clean_set(gt_s) | metrics.to_clean_set(gt_h)
                llm_set = metrics.to_clean_set(llm_p) | metrics.to_clean_set(llm_a) | metrics.to_clean_set(llm_s) | metrics.to_clean_set(llm_h)
            else:
                gt_set = (
                    metrics.to_clean_set(clean.normalise_produkt(gt_p)) |
                    metrics.to_clean_set(clean.normalise_produkt(gt_a)) |
                    metrics.to_clean_set(clean.normalise_sekundaerverband(gt_s)) |
                    metrics.to_clean_set(clean.normalise_hautschutz(gt_h))
                )
                llm_set = (
                    metrics.to_clean_set(clean.normalise_produkt(llm_p)) |
                    metrics.to_clean_set(clean.normalise_produkt(llm_a)) |
                    metrics.to_clean_set(clean.normalise_sekundaerverband(llm_s)) |
                    metrics.to_clean_set(clean.normalise_hautschutz(llm_h))
                )
            f1_list.append(metrics.calculate_f1(gt_set, llm_set))
        return pd.Series(f1_list).mean()

    results = []
    for label, json_dir in [("Zero-Shot", json_dir_zs), ("Few-Shot", json_dir_fs), ("2-Stage CoT", json_dir_2s)]:
        f1_r = _eval_dir(json_dir, raw=True)
        f1_n = _eval_dir(json_dir, raw=False)
        results.append({"Ansatz": label, "Phase 0 (Roh)": f1_r, "Phase 1 (Normalisiert)": f1_n})

    df_res = pd.DataFrame(results)

    df_plot = pd.melt(df_res, id_vars=["Ansatz"], var_name="Phase", value_name="F1-Score")
    
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))

    colors_phase = {"Phase 0 (Roh)": "#e76f51", "Phase 1 (Normalisiert)": "#2a9d8f"}
    sns.barplot(
        data=df_plot,
        x="Ansatz",
        y="F1-Score",
        hue="Phase",
        palette=colors_phase,
        ax=ax,
        edgecolor="black",
        linewidth=0.8
    )

    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Prompting-Ansatz", fontsize=12)
    ax.set_ylabel("Gesamt-Set F1-Score (Mean)", fontsize=12)
    ax.set_ylim(0, 1.15)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.legend(title="Bereinigung", title_fontsize="11", fontsize="10", loc="upper right")

    for container in ax.containers:
        labels = [f"{v*100:.1f}%" if v > 0 else "0.0%" for v in container.datavalues]
        ax.bar_label(container, labels=labels, padding=4, fontsize=10, fontweight="bold")

    plt.tight_layout()
    try:
        plt.show()
    except Exception:
        pass

    return df_res


def plot_combined_product_set_comparison(
    csv_path: str,
    json_dir_zs: str,
    json_dir_fs: str,
    json_dir_2s: str,
    title: str = "Vergleich des Gesamt-Produktsets (Primär- + Sekundärverband + Hautschutz) pro Wundbild"
):
    """
    Funktion zum direkten Rendern des Gesamt-Set Plots in Jupyter Notebooks.
    """
    evaluate_and_plot_combined_product_set(
        csv_path=csv_path,
        json_dir_zs=json_dir_zs,
        json_dir_fs=json_dir_fs,
        json_dir_2s=json_dir_2s,
        title=title
    )


def display_product_comparison_table(
    csv_path: str,
    json_dir: str,
    approach_name: str = "Zero-Shot"
):
    """
    Rendert eine farblich formatierte HTML-Tabelle in Jupyter, die für jedes Wundbild 
    die normalisierten Primärverbände, Sekundärverbände und Hautschutz von GT und LLM gegenüberstellt.
    - Grün (100%): Exakte Übereinstimmung (F1 = 1.0)
    - Orange (Teil-Match): Überlappung vorhanden (0.0 < F1 < 1.0)
    - Rot (0%): Keine Übereinstimmung (F1 = 0.0)
    """
    from IPython.display import display, HTML
    from eval.loaders import load_ground_truth, load_llm_outputs, matched_image_ids
    from utils_notebook import clean, metrics

    gt_data = load_ground_truth(csv_path)
    llm_data = load_llm_outputs(json_dir)
    matched_ids = matched_image_ids(gt_data, llm_data)

    def get_color_style(f1_val):
        if f1_val == 1.0:
            return "background-color: #d4edda; color: #155724; font-weight: bold; border: 1px solid #c3e6cb;"
        elif f1_val > 0.0:
            return "background-color: #fff3cd; color: #856404; font-weight: bold; border: 1px solid #ffeeba;"
        else:
            return "background-color: #f8d7da; color: #721c24; font-weight: bold; border: 1px solid #f5c6cb;"

    rows_html = []
    for img_id in matched_ids:
        gt_rec = gt_data[img_id]
        llm_rec = llm_data[img_id]

        # 1. Primärverband
        gt_p_raw = gt_rec.get("praeferenz_produkt") or []
        gt_a_raw = gt_rec.get("alternative_produkt") or []
        gt_p_set = metrics.to_clean_set(clean.normalise_produkt(gt_p_raw)) | metrics.to_clean_set(clean.normalise_produkt(gt_a_raw))
        
        llm_p_raw = llm_rec.get("praeferenz_verbandklasse") or []
        llm_a_raw = llm_rec.get("alternativ_verbandklasse") or []
        llm_p_set = metrics.to_clean_set(clean.normalise_produkt(llm_p_raw)) | metrics.to_clean_set(clean.normalise_produkt(llm_a_raw))
        f1_p = metrics.calculate_f1(gt_p_set, llm_p_set)

        # 2. Sekundärverband
        gt_s_raw = gt_rec.get("sekundaerverband") or []
        gt_s_set = metrics.to_clean_set(clean.normalise_sekundaerverband(gt_s_raw))
        
        llm_s_raw = llm_rec.get("sekundaerverband_fixierung") or []
        llm_s_set = metrics.to_clean_set(clean.normalise_sekundaerverband(llm_s_raw))
        f1_s = metrics.calculate_f1(gt_s_set, llm_s_set)

        # 3. Hautschutz
        gt_h_raw = gt_rec.get("hautschutz") or []
        gt_h_set = metrics.to_clean_set(clean.normalise_hautschutz(gt_h_raw))
        
        llm_h_raw = llm_rec.get("wundrand_hautschutz") or []
        llm_h_set = metrics.to_clean_set(clean.normalise_hautschutz(llm_h_raw))
        f1_h = metrics.calculate_f1(gt_h_set, llm_h_set)

        gt_p_str = ", ".join(sorted(gt_p_set)) if gt_p_set else "—"
        llm_p_str = ", ".join(sorted(llm_p_set)) if llm_p_set else "—"
        style_p = get_color_style(f1_p)

        gt_s_str = ", ".join(sorted(gt_s_set)) if gt_s_set else "—"
        llm_s_str = ", ".join(sorted(llm_s_set)) if llm_s_set else "—"
        style_s = get_color_style(f1_s)

        gt_h_str = ", ".join(sorted(gt_h_set)) if gt_h_set else "—"
        llm_h_str = ", ".join(sorted(llm_h_set)) if llm_h_set else "—"
        style_h = get_color_style(f1_h)

        rows_html.append(f"""
        <tr>
            <td style="font-weight: bold; text-align: center; border: 1px solid #ddd; padding: 6px;">{img_id}</td>
            <td style="border: 1px solid #ddd; padding: 6px; font-size: 11px;"><b>GT:</b> {gt_p_str}<br><span style="color:#0056b3;"><b>LLM:</b> {llm_p_str}</span></td>
            <td style="{style_p} text-align: center; font-size: 12px; padding: 6px;">{f1_p*100:.0f}%</td>
            <td style="border: 1px solid #ddd; padding: 6px; font-size: 11px;"><b>GT:</b> {gt_s_str}<br><span style="color:#0056b3;"><b>LLM:</b> {llm_s_str}</span></td>
            <td style="{style_s} text-align: center; font-size: 12px; padding: 6px;">{f1_s*100:.0f}%</td>
            <td style="border: 1px solid #ddd; padding: 6px; font-size: 11px;"><b>GT:</b> {gt_h_str}<br><span style="color:#0056b3;"><b>LLM:</b> {llm_h_str}</span></td>
            <td style="{style_h} text-align: center; font-size: 12px; padding: 6px;">{f1_h*100:.0f}%</td>
        </tr>
        """)

    table_html = f"""
    <div style="font-family: Arial, sans-serif; margin: 15px 0;">
        <h3 style="color: #1d3557;">Detailvergleich Produktempfehlungen ({approach_name})</h3>
        <p style="font-size: 12px; color: #555;">
            <span style="background-color: #d4edda; color: #155724; padding: 3px 8px; border-radius: 4px; font-weight: bold;">Grün (100%)</span> = Exakter Match | 
            <span style="background-color: #fff3cd; color: #856404; padding: 3px 8px; border-radius: 4px; font-weight: bold;">Orange (Teil-Match)</span> = Überlappung vorhanden | 
            <span style="background-color: #f8d7da; color: #721c24; padding: 3px 8px; border-radius: 4px; font-weight: bold;">Rot (0%)</span> = Keine Überlappung
        </p>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px;">
            <thead>
                <tr style="background-color: #1d3557; color: white; text-align: left;">
                    <th style="padding: 8px; border: 1px solid #ddd; text-align: center; width: 70px;">Bild</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">1. Primärverband (GT vs LLM)</th>
                    <th style="padding: 8px; border: 1px solid #ddd; text-align: center; width: 50px;">F1</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">2. Sekundärverband (GT vs LLM)</th>
                    <th style="padding: 8px; border: 1px solid #ddd; text-align: center; width: 50px;">F1</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">3. Hautschutz (GT vs LLM)</th>
                    <th style="padding: 8px; border: 1px solid #ddd; text-align: center; width: 50px;">F1</th>
                </tr>
            </thead>
            <tbody>
                {"".join(rows_html)}
            </tbody>
        </table>
    </div>
    """
    display(HTML(table_html))


def display_combined_set_table(
    csv_path: str,
    json_dir: str,
    approach_name: str = "Zero-Shot"
):
    """
    Rendert eine übersichtliche HTML-Tabelle mit 4 Spalten (Bild, GT Produktset, LLM Produktset, F1-Score).
    - Grün: Exakte Übereinstimmung (F1 = 1.0)
    - Orange: Teilweise Übereinstimmung (0.0 < F1 < 1.0)
    - Rot: Keine Übereinstimmung (F1 = 0.0)
    """
    from IPython.display import display, HTML
    from eval.loaders import load_ground_truth, load_llm_outputs, matched_image_ids
    from utils_notebook import clean, metrics

    gt_data = load_ground_truth(csv_path)
    llm_data = load_llm_outputs(json_dir)
    matched_ids = matched_image_ids(gt_data, llm_data)

    def get_color_style(f1_val):
        if f1_val == 1.0:
            return "background-color: #d4edda; color: #155724; font-weight: bold; border: 1px solid #c3e6cb;"
        elif f1_val > 0.0:
            return "background-color: #fff3cd; color: #856404; font-weight: bold; border: 1px solid #ffeeba;"
        else:
            return "background-color: #f8d7da; color: #721c24; font-weight: bold; border: 1px solid #f5c6cb;"

    rows_html = []
    for img_id in matched_ids:
        gt_rec = gt_data[img_id]
        llm_rec = llm_data[img_id]

        gt_p_raw = gt_rec.get("praeferenz_produkt") or []
        gt_a_raw = gt_rec.get("alternative_produkt") or []
        gt_s_raw = gt_rec.get("sekundaerverband") or []
        gt_h_raw = gt_rec.get("hautschutz") or []

        gt_set = (
            metrics.to_clean_set(clean.normalise_produkt(gt_p_raw)) |
            metrics.to_clean_set(clean.normalise_produkt(gt_a_raw)) |
            metrics.to_clean_set(clean.normalise_sekundaerverband(gt_s_raw)) |
            metrics.to_clean_set(clean.normalise_hautschutz(gt_h_raw))
        )

        llm_p_raw = llm_rec.get("praeferenz_verbandklasse") or []
        llm_a_raw = llm_rec.get("alternativ_verbandklasse") or []
        llm_s_raw = llm_rec.get("sekundaerverband_fixierung") or []
        llm_h_raw = llm_rec.get("wundrand_hautschutz") or []

        llm_set = (
            metrics.to_clean_set(clean.normalise_produkt(llm_p_raw)) |
            metrics.to_clean_set(clean.normalise_produkt(llm_a_raw)) |
            metrics.to_clean_set(clean.normalise_sekundaerverband(llm_s_raw)) |
            metrics.to_clean_set(clean.normalise_hautschutz(llm_h_raw))
        )

        f1 = metrics.calculate_f1(gt_set, llm_set)
        style = get_color_style(f1)

        gt_str = "<br>• ".join([""] + sorted(gt_set)) if gt_set else "—"
        llm_str = "<br>• ".join([""] + sorted(llm_set)) if llm_set else "—"

        rows_html.append(f"""
        <tr>
            <td style="font-weight: bold; text-align: center; border: 1px solid #ddd; padding: 8px;">{img_id}</td>
            <td style="border: 1px solid #ddd; padding: 8px; font-size: 12px; line-height: 1.4;"><b>GT Gesamt-Set:</b>{gt_str}</td>
            <td style="border: 1px solid #ddd; padding: 8px; font-size: 12px; line-height: 1.4; color: #0056b3;"><b>LLM Gesamt-Set:</b>{llm_str}</td>
            <td style="{style} text-align: center; font-size: 14px; padding: 8px;">{f1*100:.1f}%</td>
        </tr>
        """)

    table_html = f"""
    <div style="font-family: Arial, sans-serif; margin: 15px 0;">
        <h3 style="color: #1d3557;">Gesamt-Produktset Vergleich ({approach_name})</h3>
        <p style="font-size: 12px; color: #555;">
            <span style="background-color: #d4edda; color: #155724; padding: 3px 8px; border-radius: 4px; font-weight: bold;">Grün (100%)</span> = Exakter Match | 
            <span style="background-color: #fff3cd; color: #856404; padding: 3px 8px; border-radius: 4px; font-weight: bold;">Orange (Teil-Match)</span> = Überlappung vorhanden | 
            <span style="background-color: #f8d7da; color: #721c24; padding: 3px 8px; border-radius: 4px; font-weight: bold;">Rot (0%)</span> = Keine Überlappung
        </p>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px;">
            <thead>
                <tr style="background-color: #1d3557; color: white; text-align: left;">
                    <th style="padding: 10px; border: 1px solid #ddd; text-align: center; width: 90px;">Bild</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">Produktset Ground Truth (GT)</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">Produktset LLM Output</th>
                    <th style="padding: 10px; border: 1px solid #ddd; text-align: center; width: 100px;">F1-Score</th>
                </tr>
            </thead>
            <tbody>
                {"".join(rows_html)}
            </tbody>
        </table>
    </div>
    """
    display(HTML(table_html))


def get_word_counts_series(json_dir: str) -> pd.Series:
    """Berechnet die Wortanzahl der Roh-Antwort für jedes Wundbild in einem Run-Verzeichnis."""
    from pathlib import Path
    import json

    word_counts = {}
    p_dir = Path(json_dir)
    for bild_dir in sorted(p_dir.glob("Bild*")):
        if not bild_dir.is_dir():
            continue
        run_file = bild_dir / "run_001.json"
        if not run_file.exists():
            continue
        data = json.loads(run_file.read_text())
        raw_resp = data.get("raw_response", "")
        if not raw_resp:
            parsed = data.get("parsed_output", {})
            raw_resp = json.dumps(parsed, ensure_ascii=False)
        img_id = f"wunde_{bild_dir.name.replace('Bild', '').zfill(2)}"
        word_counts[img_id] = len(raw_resp.split())
    return pd.Series(word_counts)


def plot_word_count_analysis(
    json_dir_zs: str,
    json_dir_fs: str,
    json_dir_2s: str,
    title: str = "Wortanzahl & Effizienz-Analyse pro Wundbild"
):
    """
    Erstellt ein 2-teiliges Diagramm:
    1. Durchschnittliche Wortanzahl pro Wundbild für alle 3 Ansätze.
    2. Token- / Wort-Effizienz (Gesamt-Set F1 % pro Wort).
    """
    wc_zs = get_word_counts_series(json_dir_zs)
    wc_fs = get_word_counts_series(json_dir_fs)
    wc_2s = get_word_counts_series(json_dir_2s)

    avg_wc = {
        "Zero-Shot": wc_zs.mean(),
        "Few-Shot": wc_fs.mean(),
        "2-Stage CoT": wc_2s.mean()
    }

    # F1-Scores für Effizienz (Gesamt-Set F1-Scores in Phase 1)
    f1_scores = {"Zero-Shot": 49.7, "Few-Shot": 47.8, "2-Stage CoT": 51.6}
    efficiency = {k: f1_scores[k] / avg_wc[k] for k in avg_wc}

    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Subplot 1: Ø Wortanzahl pro Wundbild
    df_wc = pd.DataFrame({"Ansatz": list(avg_wc.keys()), "Ø Wortanzahl": list(avg_wc.values())})
    sns.barplot(
        data=df_wc,
        x="Ansatz",
        y="Ø Wortanzahl",
        hue="Ansatz",
        legend=False,
        palette=COLORS_PROMPTS,
        ax=axes[0],
        edgecolor="black",
        linewidth=0.8
    )
    axes[0].set_title("Durchschnittliche Textlänge (Wortanzahl pro Wundbild)", fontsize=13, fontweight="bold", pad=12)
    axes[0].set_xlabel("Prompting-Ansatz", fontsize=11)
    axes[0].set_ylabel("Ø Wortanzahl", fontsize=11)
    axes[0].set_ylim(0, max(avg_wc.values()) * 1.25)

    for container in axes[0].containers:
        labels = [f"{v:.1f} Wörter" for v in container.datavalues]
        axes[0].bar_label(container, labels=labels, padding=4, fontsize=10, fontweight="bold")

    # Subplot 2: Token-Effizienz Index
    df_eff = pd.DataFrame({"Ansatz": list(efficiency.keys()), "Effizienz-Index": list(efficiency.values())})
    sns.barplot(
        data=df_eff,
        x="Ansatz",
        y="Effizienz-Index",
        hue="Ansatz",
        legend=False,
        palette=COLORS_PROMPTS,
        ax=axes[1],
        edgecolor="black",
        linewidth=0.8
    )
    axes[1].set_title("Token-Effizienz (Gesamt-Set F1 % / Ø Wortanzahl)", fontsize=13, fontweight="bold", pad=12)
    axes[1].set_xlabel("Prompting-Ansatz", fontsize=11)
    axes[1].set_ylabel("F1 % pro Wort", fontsize=11)
    axes[1].set_ylim(0, max(efficiency.values()) * 1.25)

    for container in axes[1].containers:
        labels = [f"{v:.3f}" for v in container.datavalues]
        axes[1].bar_label(container, labels=labels, padding=4, fontsize=10, fontweight="bold")

    plt.tight_layout()
    try:
        plt.show()
    except Exception:
        pass


def display_word_count_table(
    json_dir_zs: str,
    json_dir_fs: str,
    json_dir_2s: str
):
    """
    Rendert eine übersichtliche HTML-Tabelle in Jupyter, welche die genaue Wortanzahl 
    der Roh-Antwort für jedes einzelne Wundbild über alle 3 Ansätze zeigt.
    """
    from IPython.display import display, HTML

    wc_zs = get_word_counts_series(json_dir_zs)
    wc_fs = get_word_counts_series(json_dir_fs)
    wc_2s = get_word_counts_series(json_dir_2s)

    all_ids = sorted(list(set(wc_zs.index) | set(wc_fs.index) | set(wc_2s.index)))

    rows_html = []
    for img_id in all_ids:
        zs_val = wc_zs.get(img_id, "—")
        fs_val = wc_fs.get(img_id, "—")
        ts_val = wc_2s.get(img_id, "—")

        zs_str = f"{int(zs_val)} Wörter" if isinstance(zs_val, (int, float)) and not pd.isna(zs_val) else "—"
        fs_str = f"{int(fs_val)} Wörter" if isinstance(fs_val, (int, float)) and not pd.isna(fs_val) else "—"
        ts_str = f"{int(ts_val)} Wörter" if isinstance(ts_val, (int, float)) and not pd.isna(ts_val) else "—"

        rows_html.append(f"""
        <tr>
            <td style="font-weight: bold; text-align: center; border: 1px solid #ddd; padding: 6px;">{img_id}</td>
            <td style="border: 1px solid #ddd; padding: 6px; text-align: center;">{zs_str}</td>
            <td style="border: 1px solid #ddd; padding: 6px; text-align: center;">{fs_str}</td>
            <td style="border: 1px solid #ddd; padding: 6px; text-align: center;">{ts_str}</td>
        </tr>
        """)

    summary_html = f"""
    <tr style="background-color: #f2f2f2; font-weight: bold; border-top: 2px solid #1d3557;">
        <td style="text-align: center; padding: 8px;">DURCHSCHNITT</td>
        <td style="text-align: center; padding: 8px; color: #2a9d8f;">Ø {wc_zs.mean():.1f} Wörter</td>
        <td style="text-align: center; padding: 8px; color: #e76f51;">Ø {wc_fs.mean():.1f} Wörter</td>
        <td style="text-align: center; padding: 8px; color: #e9c46a;">Ø {wc_2s.mean():.1f} Wörter</td>
    </tr>
    """

    table_html = f"""
    <div style="font-family: Arial, sans-serif; margin: 15px 0;">
        <h3 style="color: #1d3557;">Wortanzahl pro Wundbild (Roh-Antworten)</h3>
        <table style="width: 100%; max-width: 700px; border-collapse: collapse; margin-top: 10px; font-size: 12px;">
            <thead>
                <tr style="background-color: #1d3557; color: white; text-align: center;">
                    <th style="padding: 8px; border: 1px solid #ddd; width: 100px;">Bild</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Zero-Shot</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Few-Shot</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">2-Stage CoT</th>
                </tr>
            </thead>
            <tbody>
                {"".join(rows_html)}
                {summary_html}
            </tbody>
        </table>
    </div>
    """
    display(HTML(table_html))


def calculate_baselines_summary(csv_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Berechnet die Leave-One-Out Majority Baseline und die Random Baseline 
    für alle 17 Kategorien der allgemeinen Verbandsklassen 100% deterministisch.
    
    Returns:
        (sum_majority, sum_random) als DataFrames von calculate_summary()
    """
    import random, json, tempfile, os
    from eval.loaders import load_ground_truth
    from utils_notebook.metrics_explorer import calculate_scores, calculate_summary, COLUMN_MAPPING

    gt_data = load_ground_truth(csv_path)
    image_ids = sorted(list(gt_data.keys()))

    # 1. Leave-One-Out Majority Baseline
    majority_preds = {}
    for target_id in image_ids:
        train_ids = [i for i in image_ids if i != target_id]
        col_counts = {}
        for col in sorted(COLUMN_MAPPING.keys()):
            col_counts[col] = {}
            for tr_id in train_ids:
                gt_val = gt_data[tr_id].get(col)
                if gt_val is not None:
                    val_str = str(gt_val).strip()
                    if val_str and val_str not in ["[]", "nan", "None"]:
                        col_counts[col][val_str] = col_counts[col].get(val_str, 0) + 1

        fake_rec = {"image_id": target_id}
        for col in sorted(col_counts.keys()):
            counts = col_counts[col]
            if counts:
                top_val = sorted(counts.items(), key=lambda x: (-x[1], x[0]))[0][0]
                fake_rec[COLUMN_MAPPING[col]] = top_val
            else:
                fake_rec[COLUMN_MAPPING[col]] = ""
        majority_preds[target_id] = fake_rec

    # 2. Random Baseline (Deterministischer lokaler RNG)
    candidate_pools = {}
    for col in sorted(COLUMN_MAPPING.keys()):
        vals = set()
        for img_id in image_ids:
            v = gt_data[img_id].get(col)
            if v is not None:
                v_str = str(v).strip()
                if v_str and v_str not in ["[]", "nan", "None"]:
                    vals.add(v_str)
        candidate_pools[col] = sorted(list(vals))

    rng = random.Random(42)
    random_preds = {}
    for target_id in image_ids:
        fake_rec = {"image_id": target_id}
        for col in sorted(candidate_pools.keys()):
            pool = candidate_pools[col]
            if pool:
                fake_rec[COLUMN_MAPPING[col]] = rng.choice(pool)
            else:
                fake_rec[COLUMN_MAPPING[col]] = ""
        random_preds[target_id] = fake_rec

    def _eval_fake_dict(pred_dict):
        with tempfile.TemporaryDirectory() as tmp_dir:
            for img_id, rec in pred_dict.items():
                b_dir = os.path.join(tmp_dir, img_id.replace("wunde_", "Bild"))
                os.makedirs(b_dir, exist_ok=True)
                with open(os.path.join(b_dir, "run_001.json"), "w", encoding="utf-8") as f:
                    json.dump({"image_id": img_id, "parsed_output": rec}, f, ensure_ascii=False)
            df_sc = calculate_scores(csv_path, tmp_dir, raw=False)
            return calculate_summary(df_sc)

    sum_maj = _eval_fake_dict(majority_preds)
    sum_rnd = _eval_fake_dict(random_preds)
    return sum_maj, sum_rnd


def plot_overall_scores_with_baselines(
    csv_path: str,
    json_dir_zs: str,
    json_dir_fs: str,
    json_dir_2s: str,
    title: str = "Gesamtdurchschnitt aller 17 Kategorien im Vergleich mit Baselines"
):
    """
    Plottet den Gesamtdurchschnitts-Score aller 17 Kategorien für die 3 LLM-Ansätze 
    (Zero-Shot, Few-Shot, 2-Stage CoT) sowie Majority Baseline (LOO) und Random Baseline.
    """
    from utils_notebook.metrics_explorer import calculate_scores, calculate_summary

    sum_zs = calculate_summary(calculate_scores(csv_path, json_dir_zs, raw=False))
    sum_fs = calculate_summary(calculate_scores(csv_path, json_dir_fs, raw=False))
    sum_2s = calculate_summary(calculate_scores(csv_path, json_dir_2s, raw=False))
    sum_maj, sum_rnd = calculate_baselines_summary(csv_path)

    df_bar = pd.DataFrame([
        {"Ansatz": "Zero-Shot", "Score": sum_zs["Score / F1-Score (Mean)"].mean(), "Typ": "LLM Modell"},
        {"Ansatz": "Few-Shot", "Score": sum_fs["Score / F1-Score (Mean)"].mean(), "Typ": "LLM Modell"},
        {"Ansatz": "2-Stage CoT", "Score": sum_2s["Score / F1-Score (Mean)"].mean(), "Typ": "LLM Modell"},
        {"Ansatz": "Majority Baseline", "Score": sum_maj["Score / F1-Score (Mean)"].mean(), "Typ": "Baseline"},
        {"Ansatz": "Random Baseline", "Score": sum_rnd["Score / F1-Score (Mean)"].mean(), "Typ": "Baseline"}
    ])

    colors_5 = {
        "Zero-Shot": "#2a9d8f",
        "Few-Shot": "#e76f51",
        "2-Stage CoT": "#e9c46a",
        "Majority Baseline": "#457b9d",
        "Random Baseline": "#8d99ae"
    }

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        data=df_bar,
        x="Ansatz",
        y="Score",
        hue="Ansatz",
        legend=False,
        palette=colors_5,
        ax=ax,
        edgecolor="black",
        linewidth=0.8
    )

    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Ansatz / Baseline-Modell", fontsize=12)
    ax.set_ylabel("Gesamtdurchschnitt Score (Mean)", fontsize=12)
    ax.set_ylim(0, 0.7)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    # Reference lines for baselines
    maj_val = df_bar[df_bar["Ansatz"] == "Majority Baseline"]["Score"].values[0]
    rnd_val = df_bar[df_bar["Ansatz"] == "Random Baseline"]["Score"].values[0]
    ax.axhline(maj_val, color="#457b9d", linestyle="--", linewidth=1.2, label=f"Majority Baseline ({maj_val*100:.1f}%)")
    ax.axhline(rnd_val, color="#8d99ae", linestyle=":", linewidth=1.2, label=f"Random Baseline ({rnd_val*100:.1f}%)")

    for container in ax.containers:
        labels = [f"{v*100:.2f}%" for v in container.datavalues]
        ax.bar_label(container, labels=labels, padding=4, fontsize=10, fontweight="bold")

    ax.legend(loc="lower right", fontsize=10)
    plt.tight_layout()
    try:
        plt.show()
    except Exception:
        pass


def plot_exact_match_overall_comparison(
    csv_path: str,
    json_dir_zs: str,
    json_dir_fs: str,
    json_dir_2s: str,
    title: str = "Aggregierter Exact Match (Macro-Ø) aller 17 Kategorien im Vergleich mit Baselines"
):
    """
    Plottet die aggregierte Macro-Ø Exact-Match-Rate aller 17 Kategorien für die 3 LLM-Ansätze 
    (Zero-Shot, Few-Shot, 2-Stage CoT) sowie Majority Baseline (LOO) und Random Baseline.
    """
    from utils_notebook.metrics_explorer import calculate_scores, calculate_summary

    sum_zs = calculate_summary(calculate_scores(csv_path, json_dir_zs, raw=False))
    sum_fs = calculate_summary(calculate_scores(csv_path, json_dir_fs, raw=False))
    sum_2s = calculate_summary(calculate_scores(csv_path, json_dir_2s, raw=False))
    sum_maj, sum_rnd = calculate_baselines_summary(csv_path)

    df_bar = pd.DataFrame([
        {"Ansatz": "Zero-Shot", "Exact Match": sum_zs["Exact-Match-Rate"].mean(), "Typ": "LLM Modell"},
        {"Ansatz": "Few-Shot", "Exact Match": sum_fs["Exact-Match-Rate"].mean(), "Typ": "LLM Modell"},
        {"Ansatz": "2-Stage CoT", "Exact Match": sum_2s["Exact-Match-Rate"].mean(), "Typ": "LLM Modell"},
        {"Ansatz": "Majority Baseline", "Exact Match": sum_maj["Exact-Match-Rate"].mean(), "Typ": "Baseline"},
        {"Ansatz": "Random Baseline", "Exact Match": sum_rnd["Exact-Match-Rate"].mean(), "Typ": "Baseline"}
    ])

    colors_5 = {
        "Zero-Shot": "#2a9d8f",
        "Few-Shot": "#e76f51",
        "2-Stage CoT": "#e9c46a",
        "Majority Baseline": "#457b9d",
        "Random Baseline": "#8d99ae"
    }

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        data=df_bar,
        x="Ansatz",
        y="Exact Match",
        hue="Ansatz",
        legend=False,
        palette=colors_5,
        ax=ax,
        edgecolor="black",
        linewidth=0.8
    )

    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Ansatz / Baseline-Modell", fontsize=12)
    ax.set_ylabel("Macro-Ø Exact-Match-Rate", fontsize=12)
    ax.set_ylim(0, 0.6)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    # Reference lines for baselines
    maj_val = df_bar[df_bar["Ansatz"] == "Majority Baseline"]["Exact Match"].values[0]
    rnd_val = df_bar[df_bar["Ansatz"] == "Random Baseline"]["Exact Match"].values[0]
    ax.axhline(maj_val, color="#457b9d", linestyle="--", linewidth=1.2, label=f"Majority Baseline ({maj_val*100:.1f}%)")
    ax.axhline(rnd_val, color="#8d99ae", linestyle=":", linewidth=1.2, label=f"Random Baseline ({rnd_val*100:.1f}%)")

    for container in ax.containers:
        labels = [f"{v*100:.2f}%" for v in container.datavalues]
        ax.bar_label(container, labels=labels, padding=4, fontsize=10, fontweight="bold")

    ax.legend(loc="upper right", fontsize=10)
    plt.tight_layout()
    try:
        plt.show()
    except Exception:
        pass


def plot_results_heatmap_general(
    csv_path: str,
    json_dir_zs: str,
    json_dir_fs: str,
    json_dir_2s: str,
    metric_type: str = "exact",
    raw: bool = False,
    cmap: str = "Blues"
):
    """
    Erstellt eine zweigeteilte wissenschaftliche Ergebnis-Heatmap (Baselines | LLM-Ansätze)
    für alle 17 Kategorien der allgemeinen Verbandsklassen analog zu heatmap_lr.py, 
    inklusive klinischen Clustern und Macro-Ø Fußzeile.
    
    Arguments:
        metric_type: "exact" (Exact-Match-Rate) oder "f1" (Score / F1-Score (Mean))
        raw: False für normalisierte Daten (Phase 1), True für rohe Daten (Phase 0)
        cmap: Seaborn Colormap Name (Default: "Blues")
    """
    import matplotlib.gridspec as gridspec
    from utils_notebook.metrics_explorer import calculate_scores, calculate_summary

    sum_zs = calculate_summary(calculate_scores(csv_path, json_dir_zs, raw=raw))
    sum_fs = calculate_summary(calculate_scores(csv_path, json_dir_fs, raw=raw))
    sum_2s = calculate_summary(calculate_scores(csv_path, json_dir_2s, raw=raw))
    sum_maj, sum_rnd = calculate_baselines_summary(csv_path)

    clusters = [
        ("Wundcharakterisierung", [
            ("lokalisation", "Lokalisation"),
            ("wundtyp", "Wundtyp"),
            ("wundstadium", "Wundstadium"),
            ("wundrand", "Wundrand"),
            ("wundumgebung", "Wundumgebung"),
            ("exsudat", "Exsudatmenge")
        ]),
        ("Infektion, Spüllösung & Debridement", [
            ("infektion", "Infektionsverdacht"),
            ("antimikrobiell_notwendig", "Antimikrobiell indiziert"),
            ("antimikrobielles_agens", "Antimikrobielles Agens"),
            ("spuelloesung", "Spüllösung"),
            ("debridement_notwendig", "Debridement notwendig"),
            ("debridement", "Debridement Methode")
        ]),
        ("Verband & Hautschutz", [
            ("primaerverband", "Primärverband"),
            ("sekundaerverband", "Sekundärverband"),
            ("hautschutz", "Wundrand / Hautschutz")
        ]),
        ("Kompression", [
            ("kompression_indiziert", "Kompression indiziert"),
            ("kompression_produkte", "Kompression Produkte")
        ])
    ]

    cat_order = []
    cluster_ranges = {}
    idx = 0
    for c_name, c_cats in clusters:
        start_idx = idx
        for k, lab in c_cats:
            cat_order.append((k, lab, c_name))
            idx += 1
        end_idx = idx
        cluster_ranges[c_name] = (start_idx, end_idx)

    val_col = "Exact-Match-Rate" if metric_type == "exact" else "Score / F1-Score (Mean)"

    s_maj = sum_maj.set_index("Kategorie")[val_col]
    s_rnd = sum_rnd.set_index("Kategorie")[val_col]
    s_zs = sum_zs.set_index("Kategorie")[val_col]
    s_fs = sum_fs.set_index("Kategorie")[val_col]
    s_2s = sum_2s.set_index("Kategorie")[val_col]

    row_labels = [lab for _, lab, _ in cat_order]
    base_rows, llm_rows = [], []
    for k, lab, _ in cat_order:
        base_rows.append({
            "Random": s_rnd.get(k, 0.0),
            "Majority": s_maj.get(k, 0.0)
        })
        llm_rows.append({
            "Zero-Shot": s_zs.get(k, 0.0),
            "Few-Shot": s_fs.get(k, 0.0),
            "2-Stage CoT": s_2s.get(k, 0.0)
        })

    df_base = pd.DataFrame(base_rows, index=row_labels)
    df_llm = pd.DataFrame(llm_rows, index=row_labels)

    df_base.loc["Macro-Ø"] = df_base.mean(axis=0)
    df_llm.loc["Macro-Ø"] = df_llm.mean(axis=0)

    sns.set_theme(style="white")
    fig = plt.figure(figsize=(10, 13), dpi=300)

    gs = gridspec.GridSpec(
        1, 3,
        width_ratios=[2, 3, 0.15],
        wspace=0.12
    )

    ax_base = fig.add_subplot(gs[0, 0])
    ax_llm = fig.add_subplot(gs[0, 1], sharey=ax_base)
    cbar_ax = fig.add_subplot(gs[0, 2])

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

    metric_label = "Exact Match Rate in %" if metric_type == "exact" else "Macro F1 / Mean Score in %"

    sns.heatmap(df_base * 100.0, ax=ax_base, cbar=False, **norm_kwargs)
    sns.heatmap(
        df_llm * 100.0,
        ax=ax_llm,
        cbar=True,
        cbar_ax=cbar_ax,
        cbar_kws={"label": metric_label, "orientation": "vertical", "shrink": 0.8},
        **norm_kwargs
    )

    # Luminance styling
    for ax in [ax_base, ax_llm]:
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

    ax_base.set_title("Baselines", fontsize=11, fontweight="bold", color="#666666", pad=12)
    ax_llm.set_title("LLM-Ansätze", fontsize=12, fontweight="bold", color="#1d3557", pad=12)

    for t in ax_base.get_xticklabels():
        t.set_color("#666666")
        t.set_fontsize(9.5)
    for t in ax_llm.get_xticklabels():
        t.set_color("#1d3557")
        t.set_fontweight("bold")
        t.set_fontsize(10.5)

    ax_base.set_yticklabels(row_labels + ["Macro-Ø"], rotation=0, fontsize=10)
    ax_base.get_yticklabels()[17].set_weight("bold")
    ax_base.get_yticklabels()[17].set_color("#1d3557")
    ax_llm.yaxis.set_visible(False)

    for ax_sub in [ax_base, ax_llm]:
        ax_sub.axhline(17, color="#111111", linewidth=1.8)
        for c_name, (start, end) in cluster_ranges.items():
            if end < len(row_labels):
                ax_sub.axhline(end, color="#666666", linewidth=1.0, linestyle="--")

    try:
        plt.show()
    except Exception:
        pass


