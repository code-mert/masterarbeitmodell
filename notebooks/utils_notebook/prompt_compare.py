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

