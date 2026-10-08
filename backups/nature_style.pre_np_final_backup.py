"""
BACKUP — nature_style.py before np_final preset (2026-04-08).
Active module is nature_style.py; use this file only to restore legacy mock sizing (9 pt, 4.3 in panels).

Original header and body preserved from pre-migration version.
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Polygon, Rectangle
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from pathlib import Path

OUTDIR = Path("figure_mock")
OUTDIR.mkdir(exist_ok=True)

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
CYCLE = ["#2C6AB4", "#E84143", "#39AF6B", "#B69BC8", "#5AB2E4", "#EA998F", "#9ED0C6", "#F5DEA8"]
mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=CYCLE)

BAND_WL = np.array([500, 550, 600, 650, 700, 750, 800, 850])
SPECTRAL = mcolors.LinearSegmentedColormap.from_list(
    "spectral_vis", ["#2C2C8F", "#2C6AB4", "#39AF6B", "#9ED0C6", "#F5DEA8", "#EA998F", "#E84143", "#8B1A1C"])
BAND_COLORS = [SPECTRAL(i / (len(BAND_WL) - 1)) for i in range(len(BAND_WL))]

NATURE_DIV = mcolors.LinearSegmentedColormap.from_list(
    "nature_div", ["#2C6AB4", "#8DCCF0", "#FFFFFF", "#EE8284", "#E84143"])
NATURE_SEQ = mcolors.LinearSegmentedColormap.from_list(
    "nature_seq", ["#FCEDEC", "#F8B3B0", "#EA998F", "#E84143", "#A3201F"])
NATURE_COOL = mcolors.LinearSegmentedColormap.from_list(
    "nature_cool", ["#EAF3FB", "#BAE1F3", "#5AB2E4", "#2C6AB4", "#173A66"])


def style_axes(ax):
    for s in ax.spines.values():
        s.set_linewidth(1.0)
    ax.tick_params(which="both", direction="in", top=True, right=True)


def panel_label(ax, letter, dx=-0.16, dy=1.04, size=13):
    ax.text(dx, dy, letter, transform=ax.transAxes, fontsize=size,
            fontweight="bold", va="top", ha="left")


def save(fig, name, outdir=OUTDIR, transparent=False):
    outdir = Path(outdir)
    outdir.mkdir(exist_ok=True)
    fig.savefig(outdir / (name + ".png"), transparent=transparent)
    fig.savefig(outdir / (name + ".pdf"), transparent=transparent)


def gradient_bars(ax, x, heights, width=0.62, c_bottom="#D9E8F5", c_top="#2C6AB4",
                  edge="#1F4E85", lw=1.0, zorder=2, ymax=None):
    cmap = mcolors.LinearSegmentedColormap.from_list("barcmap", [c_bottom, c_top])
    grad = np.linspace(0, 1, 256).reshape(-1, 1)
    x = np.asarray(x, dtype=float)
    heights = np.asarray(heights, dtype=float)
    for xi, h in zip(x, heights):
        ax.imshow(grad, extent=(xi - width / 2, xi + width / 2, 0, h), origin="lower",
                  aspect="auto", cmap=cmap, vmin=0, vmax=1, zorder=zorder)
        ax.add_patch(Rectangle((xi - width / 2, 0), width, h, fill=False,
                               edgecolor=edge, linewidth=lw, zorder=zorder + 1))
    ax.set_xlim(x.min() - 0.7, x.max() + 0.7)
    ax.set_ylim(0, (ymax if ymax else heights.max() * 1.18))


def gradient_fill(ax, x, y, color="#E84143", alpha=0.40, ymin=0.0, zorder=1):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    rgb = mcolors.to_rgb(color)
    grad = np.empty((256, 1, 4))
    grad[:, :, 0] = rgb[0]
    grad[:, :, 1] = rgb[1]
    grad[:, :, 2] = rgb[2]
    grad[:, :, 3] = np.linspace(0, alpha, 256)[:, None]
    im = ax.imshow(grad, aspect="auto", origin="lower",
                   extent=(x.min(), x.max(), ymin, y.max()), zorder=zorder)
    verts = np.column_stack([np.concatenate([x, x[::-1]]),
                             np.concatenate([y, np.full_like(y, ymin)])])
    clip = Polygon(verts, closed=True, facecolor="none", edgecolor="none",
                   transform=ax.transData)
    ax.add_patch(clip)
    im.set_clip_path(clip)
    return im


def gauss(x, c, A=1.0, w=1.5):
    return A * np.exp(-0.5 * ((x - c) / w) ** 2)


def make_spectrum(x, peaks, noise=0.0, rng=None):
    y = np.zeros_like(x, dtype=float)
    for c, A, w in peaks:
        y += gauss(x, c, A, w)
    if noise > 0:
        if rng is None:
            rng = np.random.default_rng(0)
        y = y + noise * rng.standard_normal(x.size)
    return y


TBL = {
    "wl":        np.array([500, 550, 600, 650, 700, 750, 800, 850]),
    "device":    ["A", "A", "A", "B", "B", "B", "B", "B"],
    "chip_IL":   np.array([11.8, 9.5, 6.8, 4.5, 4.1, 3.9, 3.9, 3.8]),
    "T_fiber":   np.array([0.82, 0.92, 0.97, 0.98, 0.99, 0.99, 0.99, 0.93]),
    "QE":        np.array([0.53, 0.58, 0.61, 0.63, 0.62, 0.58, 0.52, 0.46]),
    "eta_sys":   np.array([3.1, 4.8, 5.8, 5.2, 5.5, 5.1, 4.5, 3.4]),
    "snr120":    np.array([0.95, 1.05, 1.15, 1.23, 1.18, 1.20, 1.22, 1.15]),
    "Ngamma":    np.array([4.2, 6.5, 7.9, 7.1, 7.5, 7.0, 6.2, 4.7]) * 1e3,
    "mae_1f":    np.array([0.68, 0.61, 0.55, 0.98, 0.52, 0.45, 0.38, 0.48]),
    "mae_20f":   np.array([0.07, 0.06, 0.05, 0.04, 0.06, 0.05, 0.04, 0.06]),
    "sf_limit":  np.array([-117, -116, -116, -115, -117, -118, -119, -119]),
}

SNR3_THRESHOLD = -110.44
HENE_TRUE = 632.8164
HENE_MEAS = 632.842
HENE_OFFSET_PM = 25.6
HENE_SIGMA_SHORT_PM = 14.2
HENE_THERMAL_PM_PER_K = 8.6

print("nature_style LEGACY BACKUP loaded")
