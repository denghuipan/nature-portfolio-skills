"""
nature_style.py
================
Shared Nature / Nature Photonics plotting style + helpers for MMI end-facet
femtowatt-spectrometer figures.

Default preset ``np_final`` matches Nature Portfolio print widths (89 / 183 mm)
and 5–7 pt typography at that size. Use ``apply_preset("mock")`` for legacy
large mock-ups (group meetings).

Usage:
    from nature_style import *
    fig, ax = plt.subplots(figsize=figsize_1col())
    ...
    save_fig(fig, "panel_a")
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

# ---------------- Nature Portfolio layout (Nature Photonics uses same guide) ----------------
MM_PER_IN = 25.4
WIDTH_1COL_MM = 89
WIDTH_2COL_MM = 183
MAX_FIG_HEIGHT_MM = 170

# Common panel heights (mm), scaled from earlier mock aspect ratios at 89 mm width
HEIGHT_1COL_STD_MM = 66
HEIGHT_2COL_STD_MM = 76
HEIGHT_1COL_TALL_MM = 100

SAVE_DPI = 600

_PRESETS = {
    "np_final": {
        "font.size": 7,
        "axes.labelsize": 7,
        "axes.titlesize": 7,
        "xtick.labelsize": 6,
        "ytick.labelsize": 6,
        "legend.fontsize": 6,
        "lines.linewidth": 1.5,
        "axes.linewidth": 0.8,
        "xtick.major.size": 3.5,
        "ytick.major.size": 3.5,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "panel_label_size": 8,
    },
    "mock": {
        "font.size": 9,
        "axes.labelsize": 11,
        "axes.titlesize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 8,
        "lines.linewidth": 1.8,
        "axes.linewidth": 1.0,
        "xtick.major.size": 4,
        "ytick.major.size": 4,
        "xtick.major.width": 1.0,
        "ytick.major.width": 1.0,
        "panel_label_size": 11,
    },
}

_ACTIVE_PRESET = "np_final"
_PANEL_LABEL_SIZE = _PRESETS["np_final"]["panel_label_size"]

_BASE_RCPARAMS = {
    "font.family": ["Arial", "DejaVu Sans"],
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.minor.visible": True,
    "ytick.minor.visible": True,
    "xtick.top": True,
    "ytick.right": True,
    "legend.frameon": False,
    "figure.dpi": 120,
    "savefig.dpi": SAVE_DPI,
    "savefig.bbox": "tight",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
}


def mm_to_in(mm):
    return float(mm) / MM_PER_IN


def figsize_mm(width_mm, height_mm):
    """Return (width, height) in inches for ``plt.subplots(figsize=...)``."""
    return (mm_to_in(width_mm), mm_to_in(height_mm))


def figsize_1col(height_mm=HEIGHT_1COL_STD_MM):
    return figsize_mm(WIDTH_1COL_MM, height_mm)


def figsize_2col(height_mm=HEIGHT_2COL_STD_MM):
    return figsize_mm(WIDTH_2COL_MM, height_mm)


def figsize_1col_tall(height_mm=HEIGHT_1COL_TALL_MM):
    return figsize_mm(WIDTH_1COL_MM, height_mm)


def apply_preset(name="np_final"):
    """Switch typography / line weights. ``np_final`` = Nature Portfolio submission."""
    global _ACTIVE_PRESET, _PANEL_LABEL_SIZE
    if name not in _PRESETS:
        raise ValueError(f"Unknown preset {name!r}; choose from {list(_PRESETS)}")
    _ACTIVE_PRESET = name
    p = _PRESETS[name]
    _PANEL_LABEL_SIZE = p["panel_label_size"]
    update = {k: v for k, v in p.items() if k != "panel_label_size"}
    mpl.rcParams.update(update)


def active_preset():
    return _ACTIVE_PRESET


# ---------------- palette (from reference cards) ----------------
PALETTE = {
    "red": "#E84143", "rose": "#EE8284", "salmon": "#EA998F",
    "blue": "#2C6AB4", "navy": "#7491C9", "skyblue": "#5AB2E4", "lightblue": "#8DCCF0",
    "green": "#39AF6B", "teal": "#92CCBB", "mint": "#9ED0C6",
    "purple": "#B69BC8", "pink": "#EDA2C5",
    "sand": "#F5DEA8", "olive": "#D3E2B4", "gray": "#807979",
}
CYCLE = ["#2C6AB4", "#E84143", "#39AF6B", "#B69BC8", "#5AB2E4", "#EA998F", "#9ED0C6", "#F5DEA8"]

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


def _init_rcparams():
    mpl.rcParams.update(_BASE_RCPARAMS)
    mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=CYCLE)
    apply_preset("np_final")


_init_rcparams()


# ---------------- helpers ----------------
def style_axes(ax):
    lw = mpl.rcParams["axes.linewidth"]
    for s in ax.spines.values():
        s.set_linewidth(lw)
    ax.tick_params(which="both", direction="in", top=True, right=True)


def panel_label(ax, letter, dx=-0.16, dy=1.04, size=None):
    if size is None:
        size = _PANEL_LABEL_SIZE
    ax.text(
        dx, dy, str(letter).lower(), transform=ax.transAxes, fontsize=size,
        fontweight="bold", va="top", ha="left",
    )


def save(fig, name, outdir=OUTDIR, transparent=False):
    """Save PNG (600 dpi) + PDF vector to *outdir*."""
    save_fig(fig, name, outdir=outdir, transparent=transparent)


def save_fig(fig, name, outdir=OUTDIR, transparent=False, dpi=SAVE_DPI):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    fig.savefig(outdir / (name + ".png"), dpi=dpi, bbox_inches="tight", transparent=transparent)
    fig.savefig(outdir / (name + ".pdf"), bbox_inches="tight", transparent=transparent)


def gradient_bars(ax, x, heights, width=0.62, c_bottom="#D9E8F5", c_top="#2C6AB4",
                  edge="#1F4E85", lw=1.0, zorder=2, ymax=None):
    """Vertical-gradient-filled bars (bottom -> top)."""
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
    """Vertical alpha-gradient fill under a curve."""
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
    """Single Gaussian line (w = sigma)."""
    return A * np.exp(-0.5 * ((x - c) / w) ** 2)


def make_spectrum(x, peaks, noise=0.0, rng=None):
    """Sum of Gaussian peaks. peaks = list of (center, amplitude, sigma)."""
    y = np.zeros_like(x, dtype=float)
    for c, A, w in peaks:
        y += gauss(x, c, A, w)
    if noise > 0:
        if rng is None:
            rng = np.random.default_rng(0)
        y = y + noise * rng.standard_normal(x.size)
    return y


# ---------------- manuscript target numbers (single source of truth) ----------------
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

print(
    "nature_style loaded:",
    f"preset={_ACTIVE_PRESET}",
    f"1col={WIDTH_1COL_MM}mm",
    len(PALETTE), "palette colors;",
    "bands", list(BAND_WL),
)
