import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_single_bar_category_comparison(title, data, save_path=None):
    """
    Renders category comparison plot showing Inter-Rater & KI Model results as vertical bars,
    and Random & Majority Baselines as horizontal reference lines (alpha=0.5).
    """
    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["font.size"] = 10

    left_labels = [str(l) for l in data["left_labels"]]
    right_labels = [str(l) for l in data["right_labels"]]
    left_values = data["left_values"]
    right_values = data["right_values"]
    is_ordinal = data.get("is_ordinal", False)

    # Separate Baselines (Random, Majority) from Inter-Rater Agreement bars
    baseline_lines = []
    bar_labels = []
    bar_values = []
    bar_colors = []
    bar_counts = []
    bar_totals = []

    left_counts = data.get("left_counts", [])
    right_counts = data.get("right_counts", [])
    left_totals = data.get("left_totals", [data.get("total_wounds", 60)] * len(left_labels))
    right_totals = data.get("right_totals", [data.get("total_wounds", 60)] * len(right_labels))

    ir_blue_shades = ["#1D4ED8", "#2563EB", "#3B82F6", "#1E40AF"]
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
            if not is_ordinal and idx < len(left_counts):
                bar_counts.append(left_counts[idx])
                bar_totals.append(left_totals[idx])

    for idx, (lbl, val) in enumerate(zip(right_labels, right_values)):
        bar_labels.append(lbl)
        bar_values.append(val)
        bar_colors.append(ki_green_shades[idx % len(ki_green_shades)])
        if not is_ordinal and idx < len(right_counts):
            bar_counts.append(right_counts[idx])
            bar_totals.append(right_totals[idx])

    num_bars = len(bar_labels)
    fig_width = 11.5 if num_bars >= 6 else 10.0
    fig, ax = plt.subplots(figsize=(fig_width, 5.8), dpi=300)

    bar_width = 0.48 if num_bars >= 6 else 0.45
    bar_fontsize = 9.5 if num_bars >= 6 else 10.5
    xtick_fontsize = 8.5 if num_bars >= 8 else (9.0 if num_bars >= 6 else 10.5)

    if is_ordinal:
        bars = ax.bar(x_pos := np.arange(num_bars), bar_values, width=bar_width, color=bar_colors, edgecolor="#111111", linewidth=0.8, zorder=3, alpha=0.9)

        for bar, val in zip(bars, bar_values):
            val_fmt = f"{val:.1f}".replace(".", ",")
            ax.annotate(val_fmt,
                        xy=(bar.get_x() + bar.get_width() / 2, val),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=bar_fontsize, fontweight="bold", color="#1E293B")

        max_val = max(max(bar_values), max([v for _, v in baseline_lines]) if baseline_lines else 0)
        ax.set_ylim(0, max(100, max_val + 15))
        y_lbl = data.get("y_label", "Durchschnittlicher F1-Score (%)" if ("F1-Score" in title or data.get("is_f1", False)) else "Durchschnittlicher Ordinal Score (%)")
        ax.set_ylabel(y_lbl, fontsize=11.5, fontweight="bold", labelpad=10)

    else:
        bars = ax.bar(x_pos := np.arange(num_bars), bar_counts, width=bar_width, color=bar_colors, edgecolor="#111111", linewidth=0.8, zorder=3, alpha=0.9)

        for i, (bar, cnt, val) in enumerate(zip(bars, bar_counts, bar_values)):
            tot = bar_totals[i] if i < len(bar_totals) else 60
            cnt_str = f"{cnt:g}" if isinstance(cnt, float) and cnt.is_integer() else f"{cnt}"
            val_fmt = f"{val:.1f}".replace(".", ",")
            ax.annotate(f"{cnt_str} / {tot}\n({val_fmt}%)",
                        xy=(bar.get_x() + bar.get_width() / 2, cnt),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=bar_fontsize, fontweight="bold", color="#1E293B")

        max_val = max(max(bar_counts), max([v for _, v in baseline_lines]) if baseline_lines else 0)
        ax.set_ylim(0, max_val * 1.25)
        ax.set_ylabel("Anzahl getroffener Wunden", fontsize=11.5, fontweight="bold", labelpad=10)

    ax.set_xticks(x_pos)
    ax.set_xticklabels(bar_labels, fontsize=xtick_fontsize, fontweight="bold")

    # Warm yellow/orange horizontal baseline reference lines (alpha=0.5)
    line_styles = [
        {"color": "#D97706", "ls": "--", "lw": 2.0},   # Warm Gold / Yellow-Amber for Random
        {"color": "#EA580C", "ls": "-.", "lw": 2.0}    # Deep Orange for Majority
    ]

    for i, (lbl, val) in enumerate(baseline_lines):
        style = line_styles[i if i < len(line_styles) else 0]
        c = style["color"]
        ls = style["ls"]
        lw = style["lw"]

        line = ax.axhline(y=val, color=c, linestyle=ls, linewidth=lw, alpha=0.5, zorder=4)

        val_str = f"{val:.1f}".replace(".", ",") if is_ordinal else (f"{val:g}" if isinstance(val, float) and val.is_integer() else f"{val:.1f}".replace(".", ","))
        line.set_label(f"{lbl}: {val_str}")

    ax.set_title(title, fontsize=12.5, fontweight="bold", pad=20)

    if baseline_lines:
        ax.legend(loc="upper right", frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1", fontsize=9.5, shadow=False)

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Plot erfolgreich gespeichert unter: {save_path}")

    try:
        plt.show()
    except:
        pass
    plt.close("all")


def plot_consensus_category_comparison(title, data, save_path=None):
    """
    Renders count or Ordinal Score comparison plot on 100% consensus wounds.
    Left Group: L&R AI Models, Right Group: NursIT AI Models.
    """
    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["font.size"] = 10

    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)

    x_left = np.array([0.0, 1.0, 2.0])
    x_right = np.array([3.8, 4.8, 5.8])
    x_all = np.concatenate([x_left, x_right])
    labels_all = data["left_labels"] + data["right_labels"]

    width = 0.55
    is_ordinal = data.get("is_ordinal", False)

    colors_left = ["#1F4E78", "#2F5597", "#1B365D"]
    colors_right = ["#2E7D32", "#1B5E20", "#388E3C"]

    if is_ordinal:
        left_vals = data["left_pcts"]
        right_vals = data["right_pcts"]

        rects_left = ax.bar(x_left, left_vals, width, color=colors_left, edgecolor="black", linewidth=0.8, alpha=0.9)
        rects_right = ax.bar(x_right, right_vals, width, color=colors_right, edgecolor="black", linewidth=0.8, alpha=0.9)

        for i, rect in enumerate(rects_left):
            val = left_vals[i]
            ax.annotate(f"{val:.1f}%",
                        xy=(rect.get_x() + rect.get_width() / 2, val),
                        xytext=(0, 4),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=9.5, fontweight="bold")

        for i, rect in enumerate(rects_right):
            val = right_vals[i]
            ax.annotate(f"{val:.1f}%",
                        xy=(rect.get_x() + rect.get_width() / 2, val),
                        xytext=(0, 4),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=9.5, fontweight="bold")

        y_lbl = data.get("y_label", "Durchschnittlicher F1-Score (%)" if ("F1-Score" in title or data.get("is_f1", False)) else "Durchschnittlicher Ordinal Score (%)")
        ax.set_ylabel(y_lbl, fontsize=12, fontweight="bold")
        ax.set_ylim(0, 120)
        y_pos = 112
    else:
        left_counts = data["left_counts"]
        right_counts = data["right_counts"]
        left_pcts = data["left_pcts"]
        right_pcts = data["right_pcts"]
        left_totals = data.get("left_totals", [data.get("total_consensus", 40)] * 3)
        right_totals = data.get("right_totals", [data.get("total_consensus", 40)] * 3)

        rects_left = ax.bar(x_left, left_counts, width, color=colors_left, edgecolor="black", linewidth=0.8, alpha=0.9)
        rects_right = ax.bar(x_right, right_counts, width, color=colors_right, edgecolor="black", linewidth=0.8, alpha=0.9)

        for i, rect in enumerate(rects_left):
            cnt = left_counts[i]
            pct = left_pcts[i]
            tot = left_totals[i]
            ax.annotate(f"{cnt} / {tot}\n({pct:.1f}%)",
                        xy=(rect.get_x() + rect.get_width() / 2, cnt),
                        xytext=(0, 4),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=9.5, fontweight="bold")

        for i, rect in enumerate(rects_right):
            cnt = right_counts[i]
            pct = right_pcts[i]
            tot = right_totals[i]
            ax.annotate(f"{cnt} / {tot}\n({pct:.1f}%)",
                        xy=(rect.get_x() + rect.get_width() / 2, cnt),
                        xytext=(0, 4),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=9.5, fontweight="bold")

        max_tot = max(max(left_totals), max(right_totals))
        ax.set_ylabel(f"Anzahl getroffener Wunden (max. {max_tot})", fontsize=12, fontweight="bold")
        ax.set_ylim(0, max_tot + 11)
        y_pos = max_tot + 6.0

    ax.set_title(title, fontsize=13, fontweight="bold", pad=20)
    ax.set_xticks(x_all)
    ax.set_xticklabels(labels_all, fontsize=10, fontweight="bold")

    ax.axvline(x=2.9, color="gray", linestyle="--", linewidth=1.5, alpha=0.7)
    
    ax.text(1.0, y_pos, "Lohmann & Rauscher Ansätze", ha="center", va="center", fontsize=11, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#E6EEF8", edgecolor="#1F4E78", alpha=0.9))
    ax.text(4.8, y_pos, "NursIT Ansätze", ha="center", va="center", fontsize=11, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#E8F5E9", edgecolor="#2E7D32", alpha=0.9))

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Konsens-Plot erfolgreich gespeichert unter: {save_path}")

    plt.show()
