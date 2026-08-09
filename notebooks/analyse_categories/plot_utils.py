import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_single_bar_category_comparison(title, data, save_path=None):
    """
    Renders a single-bar category comparison plot with absolute wound counts or Ordinal Scores (%) on Y-axis.
    """
    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["font.size"] = 10

    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)

    left_labels = data["left_labels"]
    right_labels = data["right_labels"]
    left_values = data["left_values"]
    right_values = data["right_values"]
    is_ordinal = data.get("is_ordinal", False)

    num_left = len(left_labels)
    num_right = len(right_labels)

    x_left = np.arange(0, num_left, 1.0)
    gap = 1.6
    start_right = x_left[-1] + gap
    x_right = np.arange(start_right, start_right + num_right, 1.0)
    
    x_all = np.concatenate([x_left, x_right])
    labels_all = left_labels + right_labels

    width = 0.55

    colors_left_all = ["#334E68", "#243B53", "#102A43"]
    colors_left = colors_left_all[:num_left]
    colors_right = ["#2E7D32", "#1B5E20", "#388E3C"]

    if is_ordinal:
        rects_left = ax.bar(x_left, left_values, width, color=colors_left, edgecolor="black", linewidth=0.8, alpha=0.9)
        rects_right = ax.bar(x_right, right_values, width, color=colors_right, edgecolor="black", linewidth=0.8, alpha=0.9)

        for i, rect in enumerate(rects_left):
            val = left_values[i]
            ax.annotate(f"{val:.1f}%",
                        xy=(rect.get_x() + rect.get_width() / 2, val),
                        xytext=(0, 4),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=9.5, fontweight="bold")

        for i, rect in enumerate(rects_right):
            val = right_values[i]
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
        left_totals = data.get("left_totals", [data.get("total_wounds", 60)] * len(left_labels))
        right_totals = data.get("right_totals", [data.get("total_wounds", 60)] * len(right_labels))

        rects_left = ax.bar(x_left, left_counts, width, color=colors_left, edgecolor="black", linewidth=0.8, alpha=0.9)
        rects_right = ax.bar(x_right, right_counts, width, color=colors_right, edgecolor="black", linewidth=0.8, alpha=0.9)

        for i, rect in enumerate(rects_left):
            cnt = left_counts[i]
            pct = left_values[i]
            tot = left_totals[i]
            cnt_str = f"{cnt:g}" if isinstance(cnt, float) and cnt.is_integer() else f"{cnt}"
            ax.annotate(f"{cnt_str} / {tot}\n({pct:.1f}%)",
                        xy=(rect.get_x() + rect.get_width() / 2, cnt),
                        xytext=(0, 4),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=9.5, fontweight="bold")

        for i, rect in enumerate(rects_right):
            cnt = right_counts[i]
            pct = right_values[i]
            tot = right_totals[i]
            ax.annotate(f"{cnt} / {tot}\n({pct:.1f}%)",
                        xy=(rect.get_x() + rect.get_width() / 2, cnt),
                        xytext=(0, 4),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=9.5, fontweight="bold")

        max_tot = max(max(left_totals), max(right_totals))
        ax.set_ylabel(f"Anzahl getroffener Wunden (max. {max_tot})", fontsize=12, fontweight="bold")
        ax.set_ylim(0, max_tot + 10)
        y_pos = max_tot + 5.5

    ax.set_title(title, fontsize=13, fontweight="bold", pad=20)
    ax.set_xticks(x_all)
    ax.set_xticklabels(labels_all, fontsize=10, fontweight="bold")

    divider_x = (x_left[-1] + x_right[0]) / 2.0
    ax.axvline(x=divider_x, color="gray", linestyle="--", linewidth=1.5, alpha=0.7)
    
    mid_left = (x_left[0] + x_left[-1]) / 2.0
    mid_right = (x_right[0] + x_right[-1]) / 2.0

    ax.text(mid_left, y_pos, "Baselines", ha="center", va="center", fontsize=11, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#E6EEF8", edgecolor="#102A43", alpha=0.9))
    ax.text(mid_right, y_pos, "KI-Ansätze (GPT-5)", ha="center", va="center", fontsize=11, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#E8F5E9", edgecolor="#2E7D32", alpha=0.9))

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Plot erfolgreich gespeichert unter: {save_path}")

    plt.show()


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
