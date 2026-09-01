import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Add project root and analyse_categories to sys.path so calc modules can be imported
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
ANALYSE_CAT_DIR = os.path.join(PROJECT_ROOT, "notebooks", "analyse_categories")

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if ANALYSE_CAT_DIR not in sys.path:
    sys.path.insert(0, ANALYSE_CAT_DIR)

from primaerverband_calc import (
    calculate_primaerverband_lr_scores,
    calculate_primaerverband_lr_expert_scores,
    calculate_primaerverband_nursit_scores,
    calculate_primaerverband_lr_level2_high_agreement_scores,
    calculate_3_expert_inter_rater_level3
)
from wundtyp_calc import (
    calculate_wundtyp_lr_scores,
    calculate_wundtyp_nursit_scores,
    calculate_wundtyp_consensus_scores
)
from lokalisation_calc import calculate_lokalisation_consensus_scores


def plot_category_diagram(
    title: str,
    data: dict,
    save_path: str = None,
    bar_spacing: float = 0.54,
    bar_width: float = 0.36,
    figsize: tuple = (7.0, 4.6),
    use_comma_decimal: bool = True
):
    """
    Renders a category comparison bar plot with closer, slimmer bar spacing, matching original design elements.

    Parameters:
    -----------
    title : str
        Chart title.
    data : dict
        Data dictionary containing 'left_labels', 'left_values', 'right_labels', 'right_values', etc.
    save_path : str
        File path to save the generated figure.
    bar_spacing : float
        Distance between center of adjacent bars (default 0.54).
    bar_width : float
        Width of individual bars (default 0.36 vs original 0.45).
    figsize : tuple
        Figure size in inches (default 7.0 x 4.6).
    use_comma_decimal : bool
        Whether to format numbers with commas (e.g., 47,7) as in German standard.
    """
    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["font.size"] = 10

    left_labels = [str(l) for l in data.get("left_labels", [])]
    right_labels = [str(l) for l in data.get("right_labels", [])]
    left_values = data.get("left_values", [])
    right_values = data.get("right_values", [])

    baseline_lines = []
    bar_labels = []
    bar_values = []
    bar_colors = []

    # Original blue shade for Inter-Rater
    ir_blue_shades = ["#2563EB", "#1D4ED8", "#3B82F6", "#1E40AF"]
    # Original green shades for KI models
    ki_green_shades = ["#2E7D32", "#1B5E20", "#0D3813", "#388E3C"]

    ir_idx = 0
    for idx, (lbl, val) in enumerate(zip(left_labels, left_values)):
        lbl_lower = lbl.lower()
        if "random" in lbl_lower or "majority" in lbl_lower:
            baseline_lines.append((lbl.replace("\n", " "), val))
        else:
            bar_labels.append(lbl)
            bar_values.append(val)
            bar_colors.append(ir_blue_shades[ir_idx % len(ir_blue_shades)])
            ir_idx += 1

    for idx, (lbl, val) in enumerate(zip(right_labels, right_values)):
        bar_labels.append(lbl)
        bar_values.append(val)
        bar_colors.append(ki_green_shades[idx % len(ki_green_shades)])

    num_bars = len(bar_labels)
    fig, ax = plt.subplots(figsize=figsize, dpi=300)

    # Compute closer x positions
    x_pos = np.arange(num_bars) * bar_spacing

    bars = ax.bar(
        x_pos,
        bar_values,
        width=bar_width,
        color=bar_colors,
        edgecolor="#111111",
        linewidth=0.8,
        zorder=3,
        alpha=0.9
    )

    # Value annotations on top of bars
    for bar, val in zip(bars, bar_values):
        val_fmt = f"{val:.1f}".replace(".", ",") if use_comma_decimal else f"{val:.1f}"
        ax.annotate(
            val_fmt,
            xy=(bar.get_x() + bar.get_width() / 2, val),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10.5,
            fontweight="bold",
            color="#1E293B"
        )

    # Y-axis styling
    max_val = max(max(bar_values), max([v for _, v in baseline_lines]) if baseline_lines else 0)
    ax.set_ylim(0, 100 if max_val <= 85 else max_val + 15)
    y_lbl = data.get("y_label", "Durchschnittlicher F1-Score (%)")
    ax.set_ylabel(y_lbl, fontsize=11.5, fontweight="bold", labelpad=10)

    # X-axis ticks & labels
    ax.set_xticks(x_pos)
    ax.set_xticklabels(bar_labels, fontsize=10.0, fontweight="bold")

    # Tight x-limits to remove excessive white space on left and right
    margin = 0.5 * bar_width + 0.22
    ax.set_xlim(-margin, (num_bars - 1) * bar_spacing + margin)

    # Baseline reference lines (matching original colors & styles)
    line_styles = [
        {"color": "#D97706", "ls": "--", "lw": 2.0},   # Warm Amber / Yellow for Random Baseline
        {"color": "#EA580C", "ls": "-.", "lw": 2.0}    # Deep Orange for Majority Baseline
    ]

    for i, (lbl, val) in enumerate(baseline_lines):
        style = line_styles[i if i < len(line_styles) else 0]
        c = style["color"]
        ls = style["ls"]
        lw = style["lw"]

        line = ax.axhline(y=val, color=c, linestyle=ls, linewidth=lw, alpha=0.25, zorder=4)

        val_str = f"{val:.1f}".replace(".", ",") if use_comma_decimal else f"{val:.1f}"
        line.set_label(f"{lbl}: {val_str}")

    # Title & Legend
    formatted_title = title.replace(": ", ":\n") if (": " in title and "\n" not in title) else title
    ax.set_title(formatted_title, fontsize=12.0, fontweight="bold", pad=15)

    if baseline_lines:
        ax.legend(
            loc="upper right",
            frameon=True,
            facecolor="#FFFFFF",
            edgecolor="#CBD5E1",
            fontsize=9.5,
            shadow=False
        )

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Diagramm erfolgreich gespeichert unter: {save_path}")

    plt.close(fig)
    return fig, ax


def generate_primaerverband_level1(output_filename="primaerverband_level1_lr.png", bar_spacing=0.52, bar_width=0.20):
    """
    Generates Primärverband Level 1 chart with slimmer bars and compact margins.
    """
    data = calculate_primaerverband_lr_scores(level_num=1)
    save_path = os.path.join(SCRIPT_DIR, output_filename)
    plot_category_diagram(
        title="Primärverband (Level 1 Produkt-Ebene): Lohmann & Rauscher Experten vs. KI-Ansätze",
        data=data,
        save_path=save_path,
        bar_spacing=bar_spacing,
        bar_width=bar_width,
        figsize=(6.8, 4.6)
    )
    return save_path


def generate_primaerverband_level2(output_filename="primaerverband_level2_lr.png", bar_spacing=0.52, bar_width=0.20):
    """
    Generates Primärverband Level 2 chart with slimmer bars and compact margins.
    """
    data = calculate_primaerverband_lr_scores(level_num=2)
    save_path = os.path.join(SCRIPT_DIR, output_filename)
    plot_category_diagram(
        title="Primärverband (Level 2 Unterkategorie-Ebene): Lohmann & Rauscher Experten vs. KI-Ansätze",
        data=data,
        save_path=save_path,
        bar_spacing=bar_spacing,
        bar_width=bar_width,
        figsize=(6.8, 4.6)
    )
    return save_path


def generate_primaerverband_level2_experte1(output_filename="primaerverband_level2_experte1.png", bar_spacing=0.52, bar_width=0.20):
    """
    Generates Primärverband Level 2 chart for Experte 1.
    """
    data = calculate_primaerverband_lr_expert_scores(level_num=2, expert_id=1)
    save_path = os.path.join(SCRIPT_DIR, output_filename)
    plot_category_diagram(
        title="Primärverband (Level 2 Unterkategorie-Ebene): KI-Ansätze vs. Experte 1",
        data=data,
        save_path=save_path,
        bar_spacing=bar_spacing,
        bar_width=bar_width,
        figsize=(6.8, 4.6)
    )
    return save_path


def generate_primaerverband_level2_experte2(output_filename="primaerverband_level2_experte2.png", bar_spacing=0.52, bar_width=0.20):
    """
    Generates Primärverband Level 2 chart for Experte 2.
    """
    data = calculate_primaerverband_lr_expert_scores(level_num=2, expert_id=2)
    save_path = os.path.join(SCRIPT_DIR, output_filename)
    plot_category_diagram(
        title="Primärverband (Level 2 Unterkategorie-Ebene): KI-Ansätze vs. Experte 2",
        data=data,
        save_path=save_path,
        bar_spacing=bar_spacing,
        bar_width=bar_width,
        figsize=(6.8, 4.6)
    )
    return save_path


def generate_primaerverband_level2_experten_vergleich(output_filename="primaerverband_level2_experten_vergleich.png", bar_width=0.20):
    """
    Generates Primärverband Level 2 chart comparing Experte 1 vs Experte 2 side-by-side for Zero-Shot, Few-Shot, and Two-Stage.
    """
    e1_data = calculate_primaerverband_lr_expert_scores(level_num=2, expert_id=1)
    e2_data = calculate_primaerverband_lr_expert_scores(level_num=2, expert_id=2)

    rand_baseline = e1_data["left_values"][0]
    maj_baseline = e1_data["left_values"][1]
    ir_f1 = e1_data["left_values"][2]

    paired_data = [
        ("Exp 1", e1_data["right_values"][0], "#2563EB"),
        ("Exp 2", e2_data["right_values"][0], "#7C3AED"),
        ("Exp 1", e1_data["right_values"][1], "#2563EB"),
        ("Exp 2", e2_data["right_values"][1], "#7C3AED"),
        ("Exp 1", e1_data["right_values"][2], "#2563EB"),
        ("Exp 2", e2_data["right_values"][2], "#7C3AED"),
    ]

    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["font.size"] = 10

    figsize = (7.2, 4.8)
    fig, ax = plt.subplots(figsize=figsize, dpi=300)

    pair_centers = [0.0, 0.62, 1.24]
    pair_names = ["Zero-Shot", "Few-Shot", "Two-Stage"]

    x_positions = []
    bar_values = []
    bar_colors = []
    bar_labels = []

    for pair_idx in range(3):
        c = pair_centers[pair_idx]
        item_left = paired_data[pair_idx * 2]
        item_right = paired_data[pair_idx * 2 + 1]

        x_left = c - bar_width / 2
        x_right = c + bar_width / 2

        x_positions.extend([x_left, x_right])
        bar_values.extend([item_left[1], item_right[1]])
        bar_colors.extend([item_left[2], item_right[2]])
        bar_labels.extend([item_left[0], item_right[0]])

    bars = ax.bar(
        x_positions,
        bar_values,
        width=bar_width,
        color=bar_colors,
        edgecolor="#111111",
        linewidth=0.8,
        zorder=3,
        alpha=0.9
    )

    for bar, val in zip(bars, bar_values):
        val_fmt = f"{val:.1f}".replace(".", ",")
        ax.annotate(
            val_fmt,
            xy=(bar.get_x() + bar.get_width() / 2, val),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold",
            color="#1E293B"
        )

    ax.set_ylim(0, 100)
    ax.set_ylabel("Durchschnittlicher F1-Score (%)", fontsize=11.5, fontweight="bold", labelpad=10)

    ax.set_xticks(x_positions)
    ax.set_xticklabels(bar_labels, fontsize=9.0, fontweight="bold")

    for c, group_name in zip(pair_centers, pair_names):
        ax.text(
            c, -11.0, group_name,
            ha="center", va="top",
            fontsize=10.5, fontweight="bold", color="#0F172A"
        )

    margin = bar_width + 0.25
    ax.set_xlim(x_positions[0] - margin, x_positions[-1] + margin)

    line_styles = [
        {"lbl": f"Random Baseline: {rand_baseline:.1f}".replace(".", ","), "val": rand_baseline, "color": "#D97706", "ls": "--"},
        {"lbl": f"Majority Baseline: {maj_baseline:.1f}".replace(".", ","), "val": maj_baseline, "color": "#EA580C", "ls": "-."},
        {"lbl": f"Inter-Rater Agreement: {ir_f1:.1f}".replace(".", ","), "val": ir_f1, "color": "#1E40AF", "ls": ":"}
    ]

    for item in line_styles:
        line = ax.axhline(y=item["val"], color=item["color"], linestyle=item["ls"], linewidth=1.8, alpha=0.35, zorder=4)
        line.set_label(item["lbl"])

    ax.set_title("Primärverband (Level 2 Unterkategorie-Ebene):\nVergleich Experte 1 vs. Experte 2", fontsize=12.0, fontweight="bold", pad=15)

    ax.legend(
        loc="upper left",
        frameon=True,
        facecolor="#FFFFFF",
        edgecolor="#CBD5E1",
        fontsize=9.0,
        shadow=False
    )

    plt.tight_layout()

    save_path = os.path.join(SCRIPT_DIR, output_filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"Diagramm erfolgreich gespeichert unter: {save_path}")
    plt.close(fig)
    return save_path




def generate_primaerverband_level3(output_filename="primaerverband_level3_combined.png", bar_width=0.20):
    """
    Generates Primärverband Level 3 chart comparing 3 Experten, L&R AI, and NursIT AI.
    Pairs corresponding L&R and NursIT approaches side-by-side without any gap between paired bars.
    """
    lr3 = calculate_primaerverband_lr_scores(level_num=3)
    nu3 = calculate_primaerverband_nursit_scores()
    best_3exp, mean_3exp = calculate_3_expert_inter_rater_level3()

    rand_baseline = lr3["left_values"][0]  # 37.6
    maj_baseline = lr3["left_values"][1]   # 69.5

    paired_data = [
        ("Best-\nPath", best_3exp, "#2563EB"),
        ("Ø Mean", mean_3exp, "#3B82F6"),
        ("L&R", lr3["right_values"][0], "#1B5E20"),
        ("NursIT", nu3["right_values"][0], "#4E9F3D"),
        ("L&R", lr3["right_values"][1], "#1B5E20"),
        ("NursIT", nu3["right_values"][1], "#4E9F3D"),
        ("L&R", lr3["right_values"][2], "#1B5E20"),
        ("NursIT", nu3["right_values"][2], "#4E9F3D"),
    ]

    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["font.size"] = 10

    figsize = (7.6, 4.8)
    fig, ax = plt.subplots(figsize=figsize, dpi=300)

    # 4 pair centers (closer pair spacing)
    pair_centers = [0.0, 0.62, 1.24, 1.86]
    pair_names = ["3 Experten", "Zero-Shot", "Few-Shot", "Two-Stage"]

    x_positions = []
    bar_values = []
    bar_colors = []
    bar_labels = []

    for pair_idx in range(4):
        c = pair_centers[pair_idx]
        item_left = paired_data[pair_idx * 2]
        item_right = paired_data[pair_idx * 2 + 1]

        # Left bar in pair (starts at c - bar_width, ends at c)
        x_left = c - bar_width / 2.0
        # Right bar in pair (starts at c, ends at c + bar_width) -> EXACTLY 0 gap!
        x_right = c + bar_width / 2.0

        x_positions.extend([x_left, x_right])
        bar_labels.extend([item_left[0], item_right[0]])
        bar_values.extend([item_left[1], item_right[1]])
        bar_colors.extend([item_left[2], item_right[2]])

    bars = ax.bar(
        x_positions,
        bar_values,
        width=bar_width,
        color=bar_colors,
        edgecolor="#111111",
        linewidth=0.8,
        zorder=3,
        alpha=0.9
    )

    # Value annotations on top of bars
    for bar, val in zip(bars, bar_values):
        val_fmt = f"{val:.1f}".replace(".", ",")
        ax.annotate(
            val_fmt,
            xy=(bar.get_x() + bar.get_width() / 2, val),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold",
            color="#1E293B"
        )

    # Y-axis
    ax.set_ylim(0, 100)
    ax.set_ylabel("Durchschnittlicher F1-Score (%)", fontsize=11.5, fontweight="bold", labelpad=10)

    # X-axis ticks (sub-labels for individual bars)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(bar_labels, fontsize=8.5, fontweight="bold")

    # Add group category headers under each pair
    for c, group_name in zip(pair_centers, pair_names):
        ax.text(
            c, -16.0, group_name,
            ha="center", va="top",
            fontsize=10.0, fontweight="bold", color="#0F172A"
        )

    # Tight x-limits to remove extra white space on left and right
    margin = bar_width + 0.15
    ax.set_xlim(x_positions[0] - margin, x_positions[-1] + margin)

    # Baseline reference lines (alpha=0.25)
    line_styles = [
        {"color": "#D97706", "ls": "--", "lw": 2.0, "lbl": f"Random Baseline: {rand_baseline:.1f}".replace(".", ",")},
        {"color": "#EA580C", "ls": "-.", "lw": 2.0, "lbl": f"Majority Baseline: {maj_baseline:.1f}".replace(".", ",")}
    ]

    for style, val in zip(line_styles, [rand_baseline, maj_baseline]):
        line = ax.axhline(y=val, color=style["color"], linestyle=style["ls"], linewidth=style["lw"], alpha=0.25, zorder=4)
        line.set_label(style["lbl"])

    # Title & Legend
    title = "Primärverband (Level 3 Verbandsklassen-Ebene):\n3 Experten vs. KI-Ansätze"
    ax.set_title(title, fontsize=12.0, fontweight="bold", pad=15)

    ax.legend(
        loc="upper right",
        frameon=True,
        facecolor="#FFFFFF",
        edgecolor="#CBD5E1",
        fontsize=9.5,
        shadow=False
    )

    plt.tight_layout()

    save_path = os.path.join(SCRIPT_DIR, output_filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"Diagramm erfolgreich gespeichert unter: {save_path}")
    plt.close(fig)
    return save_path


def generate_wundtyp_diagram(output_filename="wundtyp_klassifikation.png", bar_width=0.20):
    """
    Generates Wundtyp-Klassifikation diagram combining L&R and NursIT results into a single plot.
    Bars for the same approach (Zero-Shot, Few-Shot, Two-Stage) are paired side-by-side with 0 gap.
    Y-axis represents "Getroffene Wunden in Prozent (%)".
    Annotations above each bar show:
      - Line 1: Truncated integer percentage (e.g. 66%)
      - Line 2: (counts / total) in parentheses (e.g. (40 / 60))
    Random and Majority Baselines are omitted.
    """
    lr_wt = calculate_wundtyp_lr_scores()
    nu_wt = calculate_wundtyp_nursit_scores()

    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["font.size"] = 10

    figsize = (7.6, 4.8)
    fig, ax = plt.subplots(figsize=figsize, dpi=300)

    pair_centers = [0.0, 0.62, 1.24, 1.86]
    pair_names = ["Zero-Shot", "Few-Shot", "Two-Stage"]

    # Bar data: (sublabel, pct_val, count, total, color, x_pos)
    bars_data = [
        ("Inter-Rater\nAgreement", lr_wt["left_values"][2], lr_wt["left_counts"][2], 60, "#2563EB", pair_centers[0]),
        
        ("L&R", lr_wt["right_values"][0], lr_wt["right_counts"][0], lr_wt["right_totals"][0], "#1B5E20", pair_centers[1] - bar_width / 2.0),
        ("NursIT", nu_wt["right_values"][0], nu_wt["right_counts"][0], nu_wt["right_totals"][0], "#4E9F3D", pair_centers[1] + bar_width / 2.0),

        ("L&R", lr_wt["right_values"][1], lr_wt["right_counts"][1], lr_wt["right_totals"][1], "#1B5E20", pair_centers[2] - bar_width / 2.0),
        ("NursIT", nu_wt["right_values"][1], nu_wt["right_counts"][1], nu_wt["right_totals"][1], "#4E9F3D", pair_centers[2] + bar_width / 2.0),

        ("L&R", lr_wt["right_values"][2], lr_wt["right_counts"][2], lr_wt["right_totals"][2], "#1B5E20", pair_centers[3] - bar_width / 2.0),
        ("NursIT", nu_wt["right_values"][2], nu_wt["right_counts"][2], nu_wt["right_totals"][2], "#4E9F3D", pair_centers[3] + bar_width / 2.0),
    ]

    x_positions = [b[5] for b in bars_data]
    bar_labels = [b[0] for b in bars_data]
    bar_pcts = [b[1] for b in bars_data]
    bar_colors = [b[4] for b in bars_data]

    bars = ax.bar(
        x_positions,
        bar_pcts,
        width=bar_width,
        color=bar_colors,
        edgecolor="#111111",
        linewidth=0.8,
        zorder=3,
        alpha=0.9
    )

    # Value annotations above each bar
    for b_item, bar in zip(bars_data, bars):
        pct_val = b_item[1]
        cnt = int(b_item[2])
        tot = int(b_item[3])

        # Truncated integer percentage (no rounding)
        pct_int = int(pct_val)

        # Line 1: percentage, Line 2: (counts / total) in parentheses
        annot_text = f"{pct_int}%\n({cnt} / {tot})"

        ax.annotate(
            annot_text,
            xy=(bar.get_x() + bar.get_width() / 2, pct_val),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.0,
            fontweight="bold",
            color="#1E293B"
        )

    # Y-axis scaling & label
    ax.set_ylim(0, 100)
    ax.set_ylabel("Getroffene Wunden in Prozent (%)", fontsize=11.5, fontweight="bold", labelpad=10)

    # X-axis ticks
    ax.set_xticks(x_positions)
    ax.set_xticklabels(bar_labels, fontsize=8.5, fontweight="bold")

    # Add group category headers under each pair
    for c, group_name in zip(pair_centers[1:], pair_names):
        ax.text(
            c, -16.0, group_name,
            ha="center", va="top",
            fontsize=10.0, fontweight="bold", color="#0F172A"
        )

    # Tight x-limits
    margin = bar_width + 0.15
    ax.set_xlim(x_positions[0] - margin, x_positions[-1] + margin)

    # Title
    title = "Wundtyp-Klassifikation:\nExperten vs. KI-Ansätze"
    ax.set_title(title, fontsize=12.0, fontweight="bold", pad=15)

    plt.tight_layout()

    save_path = os.path.join(SCRIPT_DIR, output_filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"Diagramm erfolgreich gespeichert unter: {save_path}")
    plt.close(fig)
    return save_path


def generate_wundtyp_consensus_diagram(output_filename="wundtyp_konsens.png", bar_width=0.20):
    """
    Generates Wundtyp Consensus diagram on 29 consensus wounds (100% expert agreement).
    Pairs L&R and NursIT bars side-by-side with 0 gap for each approach.
    Y-axis represents "Getroffene Wunden in Prozent (%)" from 0 to 100%.
    Colors: Dark Green (#1B5E20) for L&R, Medium Green (#4E9F3D) for NursIT (no blue).
    Floating boxes and vertical dashed divider line are removed.
    Annotations:
      - Line 1: Truncated integer percentage (e.g. 68%)
      - Line 2: (counts / total) in parentheses (e.g. (20 / 29))
    """
    cs = calculate_wundtyp_consensus_scores()

    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["font.size"] = 10

    figsize = (7.2, 4.8)
    fig, ax = plt.subplots(figsize=figsize, dpi=300)

    # 3 pair centers
    pair_centers = [0.0, 0.62, 1.24]
    pair_names = ["Zero-Shot", "Few-Shot", "Two-Stage"]

    # Bar data: (sublabel, pct_val, count, total, color, x_pos)
    bars_data = [
        ("L&R", cs["left_pcts"][0], cs["left_counts"][0], cs["left_totals"][0], "#1B5E20", pair_centers[0] - bar_width / 2.0),
        ("NursIT", cs["right_pcts"][0], cs["right_counts"][0], cs["right_totals"][0], "#4E9F3D", pair_centers[0] + bar_width / 2.0),

        ("L&R", cs["left_pcts"][1], cs["left_counts"][1], cs["left_totals"][1], "#1B5E20", pair_centers[1] - bar_width / 2.0),
        ("NursIT", cs["right_pcts"][1], cs["right_counts"][1], cs["right_totals"][1], "#4E9F3D", pair_centers[1] + bar_width / 2.0),

        ("L&R", cs["left_pcts"][2], cs["left_counts"][2], cs["left_totals"][2], "#1B5E20", pair_centers[2] - bar_width / 2.0),
        ("NursIT", cs["right_pcts"][2], cs["right_counts"][2], cs["right_totals"][2], "#4E9F3D", pair_centers[2] + bar_width / 2.0),
    ]

    x_positions = [b[5] for b in bars_data]
    bar_labels = [b[0] for b in bars_data]
    bar_pcts = [b[1] for b in bars_data]
    bar_colors = [b[4] for b in bars_data]

    bars = ax.bar(
        x_positions,
        bar_pcts,
        width=bar_width,
        color=bar_colors,
        edgecolor="#111111",
        linewidth=0.8,
        zorder=3,
        alpha=0.9
    )

    # Value annotations above each bar
    for b_item, bar in zip(bars_data, bars):
        pct_val = b_item[1]
        cnt = int(b_item[2])
        tot = int(b_item[3])

        # Truncated integer percentage (no rounding)
        pct_int = int(pct_val)

        # Line 1: percentage, Line 2: (counts / total) in parentheses
        annot_text = f"{pct_int}%\n({cnt} / {tot})"

        ax.annotate(
            annot_text,
            xy=(bar.get_x() + bar.get_width() / 2, pct_val),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            color="#1E293B",
            clip_on=False
        )

    # Y-axis scaling & label
    ax.set_ylim(0, 100)
    ax.set_ylabel("Getroffene Wunden in Prozent (%)", fontsize=11.5, fontweight="bold", labelpad=10)

    # X-axis ticks (sub-labels L&R / NursIT)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(bar_labels, fontsize=8.5, fontweight="bold")

    # Add group category headers under each pair
    for c, group_name in zip(pair_centers, pair_names):
        ax.text(
            c, -16.0, group_name,
            ha="center", va="top",
            fontsize=10.0, fontweight="bold", color="#0F172A"
        )

    # Tight x-limits
    margin = bar_width + 0.15
    ax.set_xlim(x_positions[0] - margin, x_positions[-1] + margin)

    # Title with extra padding above 100% limit
    title = "Wundtyp-Klassifikation bei 100% Experten-Einigkeit:\n(29 Konsens-Wunden)"
    ax.set_title(title, fontsize=12.0, fontweight="bold", pad=28)

    plt.tight_layout()

    save_path = os.path.join(SCRIPT_DIR, output_filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"Diagramm erfolgreich gespeichert unter: {save_path}")
    plt.close(fig)
    return save_path


def generate_lokalisation_consensus_diagram(output_filename="lokalisation_konsens.png", bar_width=0.20):
    """
    Generates Wundlokalisation Consensus diagram on 40 consensus wounds (100% expert agreement).
    Pairs L&R and NursIT bars side-by-side with 0 gap for each approach.
    Y-axis represents "Getroffene Wunden in Prozent (%)" from 0 to 100%.
    Colors: Dark Green (#1B5E20) for L&R, Medium Green (#4E9F3D) for NursIT (no blue).
    Floating boxes and vertical dashed divider line are removed.
    Annotations:
      - Line 1: Truncated integer percentage (e.g. 95%)
      - Line 2: (counts / total) in parentheses (e.g. (38 / 40))
    """
    cs = calculate_lokalisation_consensus_scores()

    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["font.size"] = 10

    figsize = (7.2, 4.8)
    fig, ax = plt.subplots(figsize=figsize, dpi=300)

    # 3 pair centers
    pair_centers = [0.0, 0.62, 1.24]
    pair_names = ["Zero-Shot", "Few-Shot", "Two-Stage"]

    # Bar data: (sublabel, pct_val, count, total, color, x_pos)
    bars_data = [
        ("L&R", cs["left_pcts"][0], cs["left_counts"][0], cs["left_totals"][0], "#1B5E20", pair_centers[0] - bar_width / 2.0),
        ("NursIT", cs["right_pcts"][0], cs["right_counts"][0], cs["right_totals"][0], "#4E9F3D", pair_centers[0] + bar_width / 2.0),

        ("L&R", cs["left_pcts"][1], cs["left_counts"][1], cs["left_totals"][1], "#1B5E20", pair_centers[1] - bar_width / 2.0),
        ("NursIT", cs["right_pcts"][1], cs["right_counts"][1], cs["right_totals"][1], "#4E9F3D", pair_centers[1] + bar_width / 2.0),

        ("L&R", cs["left_pcts"][2], cs["left_counts"][2], cs["left_totals"][2], "#1B5E20", pair_centers[2] - bar_width / 2.0),
        ("NursIT", cs["right_pcts"][2], cs["right_counts"][2], cs["right_totals"][2], "#4E9F3D", pair_centers[2] + bar_width / 2.0),
    ]

    x_positions = [b[5] for b in bars_data]
    bar_labels = [b[0] for b in bars_data]
    bar_pcts = [b[1] for b in bars_data]
    bar_colors = [b[4] for b in bars_data]

    bars = ax.bar(
        x_positions,
        bar_pcts,
        width=bar_width,
        color=bar_colors,
        edgecolor="#111111",
        linewidth=0.8,
        zorder=3,
        alpha=0.9
    )

    # Value annotations above each bar
    for b_item, bar in zip(bars_data, bars):
        pct_val = b_item[1]
        cnt = int(b_item[2])
        tot = int(b_item[3])

        # Truncated integer percentage (no rounding)
        pct_int = int(pct_val)

        # Line 1: percentage, Line 2: (counts/total) in parentheses
        annot_text = f"{pct_int}%\n({cnt}/{tot})"

        ax.annotate(
            annot_text,
            xy=(bar.get_x() + bar.get_width() / 2, pct_val),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.2,
            fontweight="bold",
            color="#1E293B",
            clip_on=False
        )

    # Y-axis scaling & label
    ax.set_ylim(0, 100)
    ax.set_ylabel("Getroffene Wunden in Prozent (%)", fontsize=11.5, fontweight="bold", labelpad=10)

    # X-axis ticks (sub-labels L&R / NursIT)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(bar_labels, fontsize=8.5, fontweight="bold")

    # Add group category headers under each pair
    for c, group_name in zip(pair_centers, pair_names):
        ax.text(
            c, -16.0, group_name,
            ha="center", va="top",
            fontsize=10.0, fontweight="bold", color="#0F172A"
        )

    # Tight x-limits
    margin = bar_width + 0.15
    ax.set_xlim(x_positions[0] - margin, x_positions[-1] + margin)

    # Title with extra padding above 100% limit
    title = "Wundlokalisation bei 100% Experten-Einigkeit:\n(40 Konsens-Wunden)"
    ax.set_title(title, fontsize=12.0, fontweight="bold", pad=28)

    plt.tight_layout()

    save_path = os.path.join(SCRIPT_DIR, output_filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"Diagramm erfolgreich gespeichert unter: {save_path}")
    plt.close(fig)
    return save_path


if __name__ == "__main__":
    out1 = generate_primaerverband_level1()
    out2 = generate_primaerverband_level2()
    out2_e1 = generate_primaerverband_level2_experte1()
    out2_e2 = generate_primaerverband_level2_experte2()
    out2_comp = generate_primaerverband_level2_experten_vergleich()
    out3 = generate_primaerverband_level3()
    out4 = generate_wundtyp_diagram()
    out5 = generate_wundtyp_consensus_diagram()
    out6 = generate_lokalisation_consensus_diagram()

    # Also copy generated PNGs to exports/pngs
    import shutil
    exports_png_dir = os.path.join(PROJECT_ROOT, "exports", "pngs")
    os.makedirs(exports_png_dir, exist_ok=True)
    for p in [out1, out2, out2_e1, out2_e2, out2_comp, out3, out4, out5, out6]:
        if p and os.path.exists(p):
            shutil.copy(p, exports_png_dir)

    print("Level 1 Diagramm generiert:", out1)
    print("Level 2 Diagramm generiert:", out2)
    print("Level 2 Experte 1 Diagramm generiert:", out2_e1)
    print("Level 2 Experte 2 Diagramm generiert:", out2_e2)
    print("Level 2 Experten Vergleich Diagramm generiert:", out2_comp)
    print("Level 3 Diagramm generiert:", out3)
    print("Wundtyp Diagramm generiert:", out4)
    print("Wundtyp Konsens Diagramm generiert:", out5)
    print("Lokalisation Konsens Diagramm generiert:", out6)

