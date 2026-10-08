"""
Standalone fallback for the house figure style.

Preferred path is always:

    import sys; from pathlib import Path
    sys.path.insert(0, r"D:\\OneDrive\\UCSC\\Paper\\End-facet\\plotting")
    from nature_style import *

Use this file only when that module is unreachable (different machine or repo).
The settings below are byte-for-byte the ones nature_style.py applies, so figures
produced either way are indistinguishable.
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

# ---------------- global rcParams ----------------
mpl.rcParams.update({
    "font.family": ["Arial", "DejaVu Sans"],
    "font.size": 9,
    "axes.linewidth": 1.0,
    "axes.labelsize": 11,
    "axes.titlesize": 10,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.size": 4, "ytick.major.size": 4,
    "xtick.major.width": 1.0, "ytick.major.width": 1.0,
    "xtick.minor.visible": True, "ytick.minor.visible": True,
    "xtick.top": True, "ytick.right": True,
    "legend.frameon": False, "legend.fontsize": 8,
    "lines.linewidth": 1.8,
    "figure.dpi": 120, "savefig.dpi": 600, "savefig.bbox": "tight",
    "pdf.fonttype": 42, "ps.fonttype": 42,
})

PALETTE = {
    "red": "#E84143", "rose": "#EE8284", "salmon": "#EA998F",
    "blue": "#2C6AB4", "navy": "#7491C9", "skyblue": "#5AB2E4", "lightblue": "#8DCCF0",
    "green": "#39AF6B", "teal": "#92CCBB", "mint": "#9ED0C6",
    "purple": "#B69BC8", "pink": "#EDA2C5",
    "sand": "#F5DEA8", "olive": "#D3E2B4", "gray": "#807979",
}
CYCLE = ["#2C6AB4", "#E84143", "#39AF6B", "#B69BC8",
         "#5AB2E4", "#EA998F", "#9ED0C6", "#F5DEA8"]
mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=CYCLE)

# ---------------- canonical figure sizes (inches) ----------------
FIGSIZE_1COL = (4.3, 3.2)      # single column, one panel
FIGSIZE_2COL = (7.0, 2.9)      # double column, two panels side by side
FIGSIZE_1COL_STACK = (4.3, 4.8)  # single column, two panels stacked


def style_axes(ax):
    """Enforce spine width + inward four-sided ticks. Call on every axes."""
    for s in ax.spines.values():
        s.set_linewidth(1.0)
    ax.tick_params(which="both", direction="in", top=True, right=True)


def panel_label(ax, letter, dx=-0.20, dy=1.08, size=11):
    """Bold lowercase panel label in Nature style."""
    ax.text(dx, dy, letter, transform=ax.transAxes, fontsize=size,
            fontweight="bold", va="top", ha="left")


def make_save_fig(out_dir):
    """Return a save_fig(fig, name) writing PNG 600 dpi + vector PDF into out_dir."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    def save_fig(fig, name):
        fig.savefig(out_dir / (name + ".png"), dpi=600, bbox_inches="tight")
        fig.savefig(out_dir / (name + ".pdf"), bbox_inches="tight")

    return save_fig


# ---------------- minimal usage example ----------------
if __name__ == "__main__":
    import numpy as np

    save_fig = make_save_fig(".")
    x = np.logspace(-2, 1, 200)

    fig, ax = plt.subplots(figsize=FIGSIZE_1COL)
    ax.loglog(x, x ** 2, "-", lw=1.8, color=PALETTE["blue"], label="signal")
    ax.loglog(x, x ** 2 * 1.4, "-", lw=1.2, color=PALETTE["red"], label="reference")
    ax.axhline(1e-3, color="0.65", ls=":", lw=1.2)
    ax.set_xlabel(r"$\Delta\lambda$ (nm)")
    ax.set_ylabel(r"$1-\gamma$")
    ax.set_title("example panel", fontsize=10)
    ax.legend(fontsize=7, loc="lower right", handlelength=1.8, labelspacing=0.3)
    style_axes(ax)
    save_fig(fig, "example_panel")
