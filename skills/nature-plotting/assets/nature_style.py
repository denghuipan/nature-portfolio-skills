"""
nature_style.py
================
House plotting style for Nature-family journals (Nature, Nature Communications, Nature Methods ...):
rcParams, print sizes, palettes, axis "looks", export and pre-submission checks.

Default look: every panel in a full frame (0.6 pt), short inward ticks on the bottom and left axes, no minor
ticks, ~1 pt data lines, frameless legends, muted colours, ONE font size for all text (7 pt Arial; panel
letters 8 pt bold) and a soft vertical gradient behind the data of every plotting panel. Other looks:

    set_look("boxed")     default: full frame, inward ticks (bottom / left), gradient panel background
    set_look("open")      L-shaped axes, outward ticks
    set_look("grid")      boxed + faint horizontal grid (dense bar charts, time series)
    set_look("framed")    full frame, outward ticks, faint grid (log-log physics / benchmark plots)
    set_look("classic")   full frame, inward ticks on four sides, minor ticks, older bright palette, no gradient

Panel backgrounds: set_background("gradient" | "none", color=..., strength=...) for the whole figure set,
bg_gradient(ax, color) for one panel, no_background(ax) to keep one panel plain. Backgrounds are added when
the figure is saved (save_fig / save_fig_exact / nature_charts.export), to every axes with a frame that is not
an image, a heat map, a colour bar, a polar or a 3-D axes.

Print sizes use the Nature Portfolio guide: 89 mm (single column) / 183 mm (double), at most 170 mm tall,
5-7 pt Arial. ``apply_preset("preview")`` gives large type (one size, 9 pt) for slides.

Usage:
    from nature_style import *
    fig, ax = plt.subplots(figsize=figsize_1col())
    ...
    save_fig(fig, "panel_a")

Author: Denghui Pan
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from pathlib import Path

OUTDIR = Path("figure_preview")      # default output folder of save*(); created only when a figure is saved into it

# ---------------- Nature Portfolio layout ----------------
MM_PER_IN = 25.4
WIDTH_1COL_MM = 89
WIDTH_2COL_MM = 183
MAX_FIG_HEIGHT_MM = 170

# Common panel heights (mm)
HEIGHT_1COL_STD_MM = 62
HEIGHT_2COL_STD_MM = 72
HEIGHT_1COL_TALL_MM = 100

SAVE_DPI = 600

# One font size for every piece of text (labels, ticks, legends, titles, annotations, colour bars); only the
# panel letters differ (8 pt bold, Nature rule).
FONT_PT = {"np_final": 7.0, "preview": 9.0}


def _sizes(pt):
    return {k: pt for k in ("font.size", "axes.labelsize", "axes.titlesize", "xtick.labelsize", "ytick.labelsize",
                            "legend.fontsize", "legend.title_fontsize", "figure.titlesize")}


_PRESETS = {
    "np_final": {
        **_sizes(FONT_PT["np_final"]),
        "lines.linewidth": 1.0,
        "lines.markersize": 3.5,
        "axes.linewidth": 0.6,
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.minor.size": 1.5,
        "ytick.minor.size": 1.5,
        "xtick.minor.width": 0.5,
        "ytick.minor.width": 0.5,
        "patch.linewidth": 0.5,
        "hatch.linewidth": 0.5,
        "grid.linewidth": 0.4,
        "panel_label_size": 8,
    },
    "preview": {
        **_sizes(FONT_PT["preview"]),
        "lines.linewidth": 1.5,
        "lines.markersize": 5,
        "axes.linewidth": 0.9,
        "xtick.major.size": 3.5,
        "ytick.major.size": 3.5,
        "xtick.major.width": 0.9,
        "ytick.major.width": 0.9,
        "xtick.minor.size": 2.0,
        "ytick.minor.size": 2.0,
        "xtick.minor.width": 0.7,
        "ytick.minor.width": 0.7,
        "patch.linewidth": 0.8,
        "hatch.linewidth": 0.7,
        "grid.linewidth": 0.6,
        "panel_label_size": 11,
    },
}

_PRESET_ALIASES = {"mock": "preview"}          # old name kept so earlier scripts still run

_ACTIVE_PRESET = "np_final"
_PANEL_LABEL_SIZE = _PRESETS["np_final"]["panel_label_size"]

# Arial everywhere (Nature house face). Where Arial is not installed (most Linux servers) its metric clones
# Liberation Sans / Arimo take its place with identical glyph widths, so layouts do not move; Windows and
# macOS always use Arial itself. Only installed families are listed (no "findfont" warnings).
_FONT_PREFS = ["Arial", "Liberation Sans", "Arimo", "Helvetica", "DejaVu Sans"]


def _available_fonts(prefs=_FONT_PREFS):
    from matplotlib import font_manager
    have = {f.name for f in font_manager.fontManager.ttflist}
    out = [f for f in prefs if f in have]
    return (out[:1] + [f for f in out[1:] if f == "DejaVu Sans"]) or ["DejaVu Sans"]   # one face (+ glyph fallback)


FONT_FAMILY = _available_fonts()
SANS = FONT_FAMILY[0]          # the face actually used (Arial on Windows / macOS)

_BASE_RCPARAMS = {
    "font.family": FONT_FAMILY,
    "axes.labelpad": 2.5,
    "axes.titlepad": 4.0,
    "axes.titleweight": "normal",
    "axes.axisbelow": True,
    "axes.edgecolor": "0.15",
    "axes.labelcolor": "0.1",
    "xtick.color": "0.15",
    "ytick.color": "0.15",
    "xtick.major.pad": 2.0,
    "ytick.major.pad": 2.0,
    "grid.color": "0.89",
    "legend.frameon": False,
    "legend.handlelength": 1.4,
    "legend.handleheight": 0.7,
    "legend.handletextpad": 0.5,
    "legend.borderaxespad": 0.3,
    "legend.borderpad": 0.3,
    "legend.labelspacing": 0.35,
    "legend.columnspacing": 1.0,
    "errorbar.capsize": 0.0,
    "scatter.edgecolors": "none",
    "image.interpolation": "nearest",
    "figure.dpi": 120,
    "savefig.dpi": SAVE_DPI,
    "savefig.bbox": "tight",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
}

# axis looks: which spines, tick direction / sides, minor ticks, grid
_LOOKS = {
    "boxed": {
        "axes.spines.top": True, "axes.spines.right": True,
        "xtick.direction": "in", "ytick.direction": "in",
        "xtick.top": False, "ytick.right": False,
        "xtick.minor.visible": False, "ytick.minor.visible": False,
        "axes.grid": False,
    },
    "open": {
        "axes.spines.top": False, "axes.spines.right": False,
        "xtick.direction": "out", "ytick.direction": "out",
        "xtick.top": False, "ytick.right": False,
        "xtick.minor.visible": False, "ytick.minor.visible": False,
        "axes.grid": False,
    },
    "grid": {
        "axes.spines.top": True, "axes.spines.right": True,
        "xtick.direction": "in", "ytick.direction": "in",
        "xtick.top": False, "ytick.right": False,
        "xtick.minor.visible": False, "ytick.minor.visible": False,
        "axes.grid": True, "axes.grid.axis": "y", "axes.grid.which": "major",
    },
    "framed": {
        "axes.spines.top": True, "axes.spines.right": True,
        "xtick.direction": "out", "ytick.direction": "out",
        "xtick.top": False, "ytick.right": False,
        "xtick.minor.visible": False, "ytick.minor.visible": False,
        "axes.grid": True, "axes.grid.axis": "both", "axes.grid.which": "major",
    },
    "classic": {
        "axes.spines.top": True, "axes.spines.right": True,
        "xtick.direction": "in", "ytick.direction": "in",
        "xtick.top": True, "ytick.right": True,
        "xtick.minor.visible": True, "ytick.minor.visible": True,
        "axes.grid": False,
    },
}
_ACTIVE_LOOK = "boxed"


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
    """Switch typography / line weights. ``np_final`` = Nature Portfolio submission, ``preview`` = slides."""
    global _ACTIVE_PRESET, _PANEL_LABEL_SIZE
    if name not in _PRESETS and name not in _PRESET_ALIASES:
        raise ValueError(f"Unknown preset {name!r}; choose from {list(_PRESETS)}")
    name = _PRESET_ALIASES.get(name, name)
    _ACTIVE_PRESET = name
    p = _PRESETS[name]
    _PANEL_LABEL_SIZE = p["panel_label_size"]
    update = {k: v for k, v in p.items() if k != "panel_label_size"}
    mpl.rcParams.update(update)


def active_preset():
    return _ACTIVE_PRESET


# ---------------- palettes ----------------
# EDITORIAL (default): muted mid-tone hues that read on white at 1 pt and stay apart for most colour-vision
# deficiencies when combined with marker shape or line style. Order = the order to use them in.
EDITORIAL = ["#3A6EA5", "#D08C34", "#3E9A8E", "#7A5BA8", "#B8503A", "#6E9A5E", "#C9708A", "#8A8A8A"]
_EDITORIAL_NAMES = ["blue", "ochre", "teal", "plum", "brick", "sage", "rose", "grey"]

PALETTE_EDITORIAL = dict(zip(_EDITORIAL_NAMES, EDITORIAL))
PALETTE_EDITORIAL.update({
    "ink": "#1F2A3A", "navy": "#24466E", "sky": "#9DBCDD", "lavender": "#B9ABDA", "mint": "#A9D6CB",
    "peach": "#EFC29A", "sand": "#E8D6A8", "lightgrey": "#C8C8C8", "darkgrey": "#4D4D4D",
    # aliases so older scripts keep running
    "red": "#B8503A", "green": "#6E9A5E", "purple": "#7A5BA8", "orange": "#D08C34", "gray": "#8A8A8A",
    "skyblue": "#9DBCDD", "lightblue": "#C7D9EC", "salmon": "#E7B39E", "pink": "#E3B4C3", "olive": "#A9B97A",
    "brown": "#8A5A35",
})

# the older bright set (kept for set_look("classic") and the paper-figure-style skill)
CLASSIC_CYCLE = ["#2C6AB4", "#E84143", "#39AF6B", "#B69BC8", "#5AB2E4", "#EA998F", "#9ED0C6", "#F5DEA8"]
PALETTE_CLASSIC = {
    "red": "#E84143", "rose": "#EE8284", "salmon": "#EA998F",
    "blue": "#2C6AB4", "navy": "#7491C9", "skyblue": "#5AB2E4", "lightblue": "#8DCCF0",
    "green": "#39AF6B", "teal": "#92CCBB", "mint": "#9ED0C6",
    "purple": "#B69BC8", "pink": "#EDA2C5",
    "sand": "#F5DEA8", "olive": "#D3E2B4", "gray": "#807979", "grey": "#807979", "brown": "#8B5A2B",
}

# THEMES: small palettes for one figure's job (all hex, all used by the templates)
THEMES = {
    # two tones of one hue: "reference set" (light) vs "new set" (dark)
    "duo_purple": ["#3E1F63", "#8E80CF"],
    "duo_blue": ["#1F3E68", "#8DB0D8"],
    "duo_teal": ["#155E57", "#8CCBBE"],
    # soft fills for bars: tool of interest in light blue, baselines in greys
    "soft": ["#A9C9EC", "#6F98C9", "#C9C9C9", "#8F8F8F"],
    # scenario fans (low / mid / high)
    "fan": ["#4FA67A", "#7769B5", "#B9772F"],
    # hollow-marker trio for experiment-vs-model plots
    "signal": ["#C0504D", "#4E9A47", "#5470B5"],
    # earthy categorical set for field / ecology data
    "earth": ["#5B7F3A", "#C49A3A", "#7A4E2D", "#4F7FA0", "#A5583F", "#8C8C6E"],
    # up / down / not significant (volcano, gain vs loss)
    "updown": ["#B8503A", "#3A6EA5", "#C8C8C8"],
}

PALETTE = dict(PALETTE_EDITORIAL)
CYCLE = list(EDITORIAL)


def n_colors(cmap, n, lo=0.0, hi=1.0):
    """n evenly spaced colours from a colour map (one per ordered series)."""
    cmap = mpl.colormaps[cmap] if isinstance(cmap, str) else cmap
    return [cmap(v) for v in np.linspace(lo, hi, n)]


def desaturate_cmap(cmap, k, n=256):
    """cmap with its HLS saturation scaled by k (k < 1: softer)."""
    import colorsys
    cmap = mpl.colormaps[cmap] if isinstance(cmap, str) else cmap
    rgb = [colorsys.hls_to_rgb(h, l, min(1.0, s * k)) for h, l, s in
           (colorsys.rgb_to_hls(*cmap(i / (n - 1))[:3]) for i in range(n))]
    return mcolors.ListedColormap(rgb, name=f"{cmap.name}_x{k}")


def set_look(name="boxed", palette=None, background=None):
    """Switch the axis look for every figure made afterwards: boxed | open | grid | framed | classic.
    ``classic`` also switches PALETTE / CYCLE to the older bright set and turns panel backgrounds off (unless
    palette= / background= say otherwise); the others use EDITORIAL with gradient backgrounds.
    PALETTE and CYCLE are changed in place, so names imported earlier stay valid."""
    global _ACTIVE_LOOK
    if name not in _LOOKS:
        raise ValueError(f"Unknown look {name!r}; choose from {list(_LOOKS)}")
    _ACTIVE_LOOK = name
    mpl.rcParams.update(_LOOKS[name])
    if palette is None:
        palette = "classic" if name == "classic" else "editorial"
    src_p, src_c = (PALETTE_CLASSIC, CLASSIC_CYCLE) if palette == "classic" else (PALETTE_EDITORIAL, EDITORIAL)
    PALETTE.clear(); PALETTE.update(src_p)
    CYCLE[:] = src_c
    mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=CYCLE)
    if background is None:
        background = "none" if name == "classic" else "gradient"
    set_background(background)
    if name == "classic":
        mpl.rcParams.update({"xtick.major.size": 3.5, "ytick.major.size": 3.5,
                             "axes.linewidth": 0.8, "xtick.major.width": 0.8, "ytick.major.width": 0.8,
                             "lines.linewidth": 1.5})
    else:
        apply_preset(_ACTIVE_PRESET)


# ---------------- gradients and panel backgrounds ----------------
from matplotlib.image import BboxImage as _BboxImage
from matplotlib.transforms import Bbox as _Bbox, TransformedBbox as _TBbox
from matplotlib.transforms import blended_transform_factory as mtransforms_blend

_BACKGROUND = {"mode": "gradient", "color": "#D3DFEE", "strength": 1.0, "direction": "up", "to": "#FCFDFE"}


def _mix(c, k, other="#FFFFFF"):
    """Blend colour c with *other* (k = 0: c, k = 1: other)."""
    a, b = np.array(mcolors.to_rgba(c)), np.array(mcolors.to_rgba(other))
    return tuple(a * (1 - k) + b * k)


def gradient_array(stops, n=256, direction="up"):
    """RGBA array for a linear gradient through *stops* (colours, or (position, colour) pairs).
    direction: 'up' (first stop at the bottom), 'down', 'right' (first stop at the left), 'left'."""
    if not isinstance(stops[0], (tuple, list)) or isinstance(stops[0][0], str) or len(stops[0]) != 2:
        stops = [(i / (len(stops) - 1), c) for i, c in enumerate(stops)]
    pos = np.array([p for p, _ in stops]); cols = np.array([mcolors.to_rgba(c) for _, c in stops])
    t = np.linspace(0, 1, n)
    g = np.stack([np.interp(t, pos, cols[:, k]) for k in range(4)], axis=1)
    if direction in ("down", "left"):
        g = g[::-1]
    return g[:, None, :] if direction in ("up", "down") else g[None, :, :]


def gradient_image(ax, extent, stops, direction="up", coords="data", clip=None, zorder=0.5, alpha=None):
    """Paint a linear gradient into a rectangle of *ax* without touching its data limits.
    extent = (x0, x1, y0, y1) in data units (coords='data'), axes fraction (coords='axes'), x in data and y in
    axes fraction (coords='x': a full-height window) or the reverse (coords='y': a full-width band).
    clip: a Patch (in the same coordinates, added to ax or with its transform set) to cut the gradient to
    (bar outline, area under a curve, rounded box). Returns the BboxImage."""
    x0, x1, y0, y1 = extent
    tr = {"data": ax.transData, "axes": ax.transAxes,
          "x": mtransforms_blend(ax.transData, ax.transAxes), "y": mtransforms_blend(ax.transAxes, ax.transData)}[coords]
    im = _BboxImage(_TBbox(_Bbox.from_extents(x0, y0, x1, y1), tr), data=gradient_array(stops, direction=direction),
                    origin="lower", interpolation="bilinear", zorder=zorder)
    if alpha is not None:
        im.set_alpha(alpha)
    im.set_clip_path(clip if clip is not None else ax.patch)
    im.set_clip_box(ax.bbox)                     # never paint outside the panel
    ax.add_artist(im)
    return im


def bg_gradient(ax, color=None, strength=None, direction=None, to=None):
    """Soft gradient behind the data of one panel: *color* (default: the house cool grey-blue) at the bottom
    fading to white at the top. A colour name from PALETTE is lightened automatically. Returns the image."""
    color = color or _BACKGROUND["color"]
    k = _BACKGROUND["strength"] if strength is None else strength
    c = mcolors.to_rgba(color)
    if sum(c[:3]) / 3 < 0.8:                    # a full-strength hue -> its very light tint
        c = _mix(c, 0.86)
    c0 = _mix(c, 1 - k, to or _BACKGROUND["to"])
    im = gradient_image(ax, (0, 1, 0, 1), [c0, to or _BACKGROUND["to"]], direction=direction or _BACKGROUND["direction"],
                        coords="axes", zorder=-100)
    ax._ns_bg = im
    return im


def no_background(ax):
    """Keep this panel plain when backgrounds are added at save time."""
    ax._ns_nobg = True
    if getattr(ax, "_ns_bg", None) is not None and ax._ns_bg is not True:
        ax._ns_bg.remove()
    ax._ns_bg = None


def set_background(mode="gradient", color=None, strength=None, direction=None, to=None):
    """Panel backgrounds for figures saved afterwards: mode 'gradient' or 'none'; color = tint at the start of the
    gradient (default '#DCE6F2'), strength 0-1, direction 'up' | 'down' | 'right' | 'left'."""
    _BACKGROUND["mode"] = mode
    for k, v in (("color", color), ("strength", strength), ("direction", direction), ("to", to)):
        if v is not None:
            _BACKGROUND[k] = v


def _wants_background(ax):
    import matplotlib.collections as mcoll
    if getattr(ax, "_ns_nobg", False) or getattr(ax, "_ns_bg", None) is not None:
        return False
    if not ax.get_visible() or not ax.axison or ax.name != "rectilinear" or hasattr(ax, "_colorbar"):
        return False
    if ax.images:
        return False
    for c in ax.collections:
        if isinstance(c, mcoll.QuadMesh):
            return False
        if isinstance(c, mcoll.PolyCollection) and c.get_array() is not None and len(c.get_offsets()) > 1:
            return False                         # hexbin
    fc = mcolors.to_rgba(ax.get_facecolor())
    if fc[3] > 0 and sum(fc[:3]) < 2.97:        # panel already has its own colour
        return False
    bb = ax.get_position()
    W, H = ax.figure.get_size_inches()
    return bb.width * W * MM_PER_IN >= 10 and bb.height * H * MM_PER_IN >= 8


def apply_backgrounds(fig):
    """Add the current panel background to every eligible axes of *fig* (idempotent). Called by the savers."""
    if _BACKGROUND["mode"] != "gradient":
        return fig
    for ax in fig.axes:
        if _wants_background(ax):
            bg_gradient(ax)
    return fig


def active_look():
    return _ACTIVE_LOOK


def _init_rcparams():
    mpl.rcParams.update(_BASE_RCPARAMS)
    apply_preset("np_final")
    set_look("boxed")


_init_rcparams()


# ---------------- helpers ----------------
def style_axes(ax, look=None):
    """Apply a look to one existing Axes (e.g. axes made before set_look, or one framed panel in an open figure)."""
    look = look or _ACTIVE_LOOK
    p = _LOOKS[look]
    lw = mpl.rcParams["axes.linewidth"]
    for side, s in ax.spines.items():
        s.set_linewidth(lw)
        if side in ("top", "right"):
            s.set_visible(p[f"axes.spines.{side}"])
    ax.tick_params(which="both", direction=p["xtick.direction"], top=p["xtick.top"], right=p["ytick.right"])
    if p["xtick.minor.visible"]:
        ax.minorticks_on()
    else:
        ax.minorticks_off()
    if p["axes.grid"]:
        ax.grid(True, axis=p.get("axes.grid.axis", "both"))
    else:
        ax.grid(False)


def despine(ax, left=False, bottom=False, top=True, right=True):
    """Hide spines (True = hide). Horizontal bar charts: despine(ax, left=True) and drop the y ticks."""
    for side, hide in (("left", left), ("bottom", bottom), ("top", top), ("right", right)):
        ax.spines[side].set_visible(not hide)
    if left:
        ax.tick_params(axis="y", left=False)
    if bottom:
        ax.tick_params(axis="x", bottom=False)


def offset_spines(ax, mm=1.2, sides=("left", "bottom"), trim=False):
    """Move spines outward by *mm* (detached-axes look). trim=True ends each spine at the outer major ticks."""
    pts = mm / MM_PER_IN * 72
    for s in sides:
        ax.spines[s].set_position(("outward", pts))
    if trim:
        ax.figure.canvas.draw()
        xt = [t for t in ax.get_xticks() if ax.get_xlim()[0] <= t <= ax.get_xlim()[1]]
        yt = [t for t in ax.get_yticks() if ax.get_ylim()[0] <= t <= ax.get_ylim()[1]]
        if xt and "bottom" in sides:
            ax.spines["bottom"].set_bounds(min(xt), max(xt))
        if yt and "left" in sides:
            ax.spines["left"].set_bounds(min(yt), max(yt))


def thousands(ax, axis="y", decimals=0):
    """Comma thousands separators on tick labels (1,000 / 20,000 / 400,000), the Nature number style."""
    f = mticker.FuncFormatter(lambda v, _: f"{v:,.{decimals}f}")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(f)


def percent(ax, axis="y", decimals=0, scale=100.0):
    """Tick labels as percentages; scale=100 when data are fractions, scale=1 when data are already in %."""
    f = mticker.FuncFormatter(lambda v, _: f"{v * scale:.{decimals}f}%")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(f)


def fmt_int(v):
    """1234567 -> '1,234,567' (for n = labels and in-figure counts)."""
    return f"{int(round(v)):,}"


def subtitle(ax, text, pad=None, **kw):
    """Centred panel subtitle above the axes, regular weight (Nature uses bold only for panel letters)."""
    kw.setdefault("fontsize", mpl.rcParams["axes.titlesize"])
    return ax.set_title(text, pad=pad if pad is not None else mpl.rcParams["axes.titlepad"], **kw)


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
    apply_backgrounds(fig)
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    fig.savefig(outdir / (name + ".png"), dpi=dpi, bbox_inches="tight", transparent=transparent)
    fig.savefig(outdir / (name + ".pdf"), bbox_inches="tight", transparent=transparent)


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


# ---------------- typography, exact canvas, text audit ----------------
def use_arial_math():
    """Render mathtext in Arial (same face as the labels) instead of the DejaVu/Computer-Modern default.
    Missing glyphs (rare: \\propto, \\int) fall back to DejaVu Sans."""
    mpl.rcParams.update({
        "mathtext.fontset": "custom",
        "mathtext.rm": SANS,
        "mathtext.it": f"{SANS}:italic",
        "mathtext.bf": f"{SANS}:bold",
        "mathtext.sf": SANS,
        "mathtext.cal": SANS,
        "mathtext.fallback": "stixsans",
    })


# Nature: no text below 5 pt. matplotlib shrinks super- and subscripts to 0.7 of the base size (6 pt tick -> 4.2 pt
# exponent); 0.84 keeps a 6 pt label's exponent at 5.0 pt. Read at render time by mathtext.
try:
    import matplotlib._mathtext as _mt
    _mt.SHRINK_FACTOR = 0.84
    # and never below 5 pt, also in 5-5.5 pt text (same rule as ed_finish, which sees the flag)
    if not getattr(_mt.Char, "_ed_floor", False):
        def _shrink_floor(self, _min=5.0):
            _mt.Node.shrink(self)
            if self.size < _mt.NUM_SIZE_LEVELS:
                f = min(1.0, max(_mt.SHRINK_FACTOR, _min / self.fontsize))
                self.fontsize *= f; self.width *= f; self.height *= f; self.depth *= f
        _mt.Char.shrink = _shrink_floor
        _mt.Char._ed_floor = True
except (ImportError, AttributeError):
    pass


def center_subtitles(fig, specs, below_mm=30.0, pad_mm=3.0, min_w_mm=3.0):
    """Centre panel subtitles over their frames (same rule as center_titles for Extended Data).
    specs = {prefix: span_mm}: every fig.text whose string starts with prefix is centred over the axes that start no
    more than pad_mm left of it, end within span_mm of it, are at least min_w_mm wide and whose top lies within
    below_mm under it."""
    W, H = (v * 25.4 for v in fig.get_size_inches())
    for t in fig.texts:
        s = t.get_text()
        span = next((v for k, v in specs.items() if s.startswith(k)), None)
        if span is None:
            continue
        x, y = t.get_position()
        if t.get_ha() == "center":
            continue
        xs = []
        for ax in fig.axes:
            p = ax.get_position()
            if ax.get_visible() and p.x0 >= x - pad_mm / W and p.x1 <= x + span / W and \
                    (p.x1 - p.x0) * W >= min_w_mm and y - below_mm / H < p.y1 <= y + 1e-3:
                xs += [p.x0, p.x1]
        if xs:
            t.set_ha("center"); t.set_x((min(xs) + max(xs)) / 2)


def pin_top_letters(fig, top_mm=1.0, band_mm=3.0):
    """Panel letters (bold, single lowercase, >= 7.5 pt, va='top') whose anchor lies within band_mm of the top edge
    are moved to top_mm below it, so that the top row of letters sits at the same height in every figure
    (anchor 1.0 mm -> glyph box 0.5 mm below the page edge in the PDF)."""
    H = fig.get_figheight() * 25.4
    for t in fig.texts:
        s = t.get_text()
        if len(s) == 1 and s.islower() and t.get_fontweight() in ("bold", 700) and t.get_fontsize() >= 7.5 \
                and t.get_va() == "top" and (1 - t.get_position()[1]) * H <= band_mm:
            t.set_y(1 - top_mm / H)


def fs():
    """The single font size of the active preset (7 pt in np_final, 9 pt in preview)."""
    return mpl.rcParams["font.size"]


def audit_text(fig, min_pt=5.0, max_pt=8.0, show=True, uniform=False):
    """List every text artist of *fig* (labels, ticks, legends, annotations) whose font size is outside
    [min_pt, max_pt] (Nature: >= 5 pt, panel letters 8 pt). uniform=True also lists any text that is not at the
    house size fs() (bold one-letter panel labels excepted) and any text not set in the house face.
    Returns [(size, text), ...]."""
    fig.canvas.draw()
    bad = []
    base = fs()
    face = FONT_FAMILY[0]
    for t in fig.findobj(mpl.text.Text):
        s = t.get_text().strip()
        if not s or not t.get_visible():
            continue
        size = float(t.get_fontsize())
        letter = len(s) == 1 and s.isalpha() and t.get_fontweight() in ("bold", 700)
        if size < min_pt - 1e-6 or size > max_pt + 1e-6:
            bad.append((size, s))
        elif uniform and not letter and abs(size - base) > 1e-6:
            bad.append((size, s))
        elif uniform and t.get_fontname() != face and not s.startswith("$"):
            bad.append((size, f"[{t.get_fontname()}] {s}"))
    if show:
        print(f"[audit_text] {len(bad)} text items to check")
        for size, s in sorted(bad):
            print(f"   {size:4.1f} pt  {s[:70]!r}")
    return bad


def save_fig_exact(fig, name, outdir=OUTDIR, dpi=SAVE_DPI, warn_mm=0.3):
    """Save PNG + PDF at the exact canvas size (no tight bbox), so a 183 mm layout is 183 mm wide.
    Warns when the tight bounding box of the drawn content sticks out of the canvas by more than *warn_mm*."""
    apply_backgrounds(fig)
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    tb = fig.get_tightbbox(r)                       # inches, figure coords
    w, h = fig.get_size_inches()
    over = {"left": -tb.x0, "bottom": -tb.y0, "right": tb.x1 - w, "top": tb.y1 - h}
    out = {k: v * MM_PER_IN for k, v in over.items() if v * MM_PER_IN > warn_mm}
    if out:
        print(f"[save_fig_exact] {name}: content sticks out of the canvas by (mm) " +
              ", ".join(f"{k} {v:.1f}" for k, v in out.items()))
    with mpl.rc_context({"savefig.bbox": "standard"}):          # bbox_inches=None would fall back to rc "tight"
        fig.savefig(outdir / (name + ".png"), dpi=dpi)
        fig.savefig(outdir / (name + ".pdf"))

# ---------------------------------------------------------------- Extended Data finishing
# Nature ED: page at most 180 mm wide (x 170 mm), text 5-7 pt sans serif, lines 0.25-1 pt, files JPEG / TIFF / EPS,
# rasterized, <= 10 MB. ed_finish() is called on a finished ED figure just before saving:
#   * the canvas shrinks to ED_MAX_W (axes and fig.text are in figure fractions, so the layout scales; type keeps its
#     point size);
#   * mathtext super/subscripts keep the usual shrink but are floored at 5 pt;
#   * every stroke is clamped to 0.25-1 pt.
ED_MAX_W = 180.0
ED_MIN_PT = 5.0


def center_titles(fig, titles, below_mm=25.0, pad_mm=8.0):
    """centre each panel subtitle (figure-coordinate Text) over its panel.
    Panel = from the subtitle's x - pad_mm to the next subtitle on the same row (or the page edge); the subtitle is
    centred over the axes (or, for tables, the figure-level lines) that lie in that span within below_mm under it."""
    import matplotlib.lines as mlines
    W, H = (v * MM_PER_IN for v in fig.get_size_inches())
    pos = [(t, *t.get_position()) for t in titles]
    for t, x, y in pos:
        nxt = [x2 for t2, x2, y2 in pos if t2 is not t and abs(y2 - y) * H < 8.0 and x2 > x]   # same row, or a subtitle set lower to follow its frame
        left, right = x - pad_mm / W, (min(nxt) - 3.0 / W) if nxt else 1.0
        xs = []
        for ax in fig.axes:
            p = ax.get_position()
            if ax.get_visible() and p.x0 >= left - 1e-3 and p.x1 <= right + 1e-3 and y - below_mm / H < p.y1 <= y + 1e-3:
                xs += [p.x0, p.x1]
        if not xs:
            for ln in fig.lines + fig.artists:
                if isinstance(ln, mlines.Line2D) and ln.get_transform() == fig.transFigure:
                    lx, ly = ln.get_xdata(), ln.get_ydata()
                    if min(lx) >= left - 1e-3 and max(lx) <= right + 1e-3 and y - below_mm / H < max(ly) <= y + 1e-3:
                        xs += [min(lx), max(lx)]
        cx = (min(xs) + max(xs)) / 2 if xs else (x + right) / 2
        t.set_ha("center")
        hw = t.get_window_extent(fig.canvas.get_renderer()).width / fig.bbox.width / 2
        cx = min(max(cx, left + hw), 1 - 0.5 / W - hw)          # keep the subtitle on the page and in its panel
        t.set_x(cx)
    return fig


def ed_finish(fig, max_w=ED_MAX_W, lw_min=0.25, lw_max=1.0):
    import matplotlib.lines as mlines
    import matplotlib.patches as mpatches
    import matplotlib.collections as mcoll
    w, h = fig.get_size_inches()
    if w * MM_PER_IN > max_w + 1e-6:
        k = max_w / (w * MM_PER_IN)
        fig.set_size_inches(w * k, h * k)
    try:                                                # scripts keep the 0.84 shrink but never go below 5 pt
        import matplotlib._mathtext as _m
        if not getattr(_m.Char, "_ed_floor", False):
            def _shrink(self, _min=ED_MIN_PT):
                _m.Node.shrink(self)
                if self.size < _m.NUM_SIZE_LEVELS:
                    f = min(1.0, max(_m.SHRINK_FACTOR, _min / self.fontsize))
                    self.fontsize *= f; self.width *= f; self.height *= f; self.depth *= f
            _m.Char.shrink = _shrink
            _m.Char._ed_floor = True
    except (ImportError, AttributeError):
        pass

    def clamp(v):
        return v if v == 0 else min(max(v, lw_min), lw_max)
    for a in fig.findobj():
        if isinstance(a, mlines.Line2D):
            a.set_linewidth(clamp(a.get_linewidth()))
            if a.get_markeredgewidth():
                a.set_markeredgewidth(min(a.get_markeredgewidth(), lw_max))
        elif isinstance(a, mpatches.Patch):
            if a.get_linewidth():
                a.set_linewidth(clamp(a.get_linewidth()))
        elif isinstance(a, mcoll.Collection):
            lws = a.get_linewidths()
            if len(lws):
                a.set_linewidths([clamp(v) for v in lws])
    for ax in fig.axes:
        for sp in ax.spines.values():
            sp.set_linewidth(clamp(sp.get_linewidth()))
        for t in ("major", "minor"):
            for tl in ax.xaxis.get_ticklines(minor=t == "minor") + ax.yaxis.get_ticklines(minor=t == "minor"):
                tl.set_markeredgewidth(clamp(tl.get_markeredgewidth()))
    return fig


def ed_tiff(png_path, max_mb=10.0):
    """TIFF (LZW, RGB, 600 dpi) next to an ED PNG; drops to 450 / 300 dpi if the file would exceed max_mb."""
    from PIL import Image
    png_path = Path(png_path)
    im = Image.open(png_path).convert("RGB")
    dpi0 = im.info.get("dpi", (SAVE_DPI, SAVE_DPI))[0]
    out = png_path.with_suffix(".tif")
    for dpi in (600, 450, 300):
        k = dpi / dpi0
        img = im if abs(k - 1) < 1e-3 else im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
        img.save(out, compression="tiff_lzw", dpi=(dpi, dpi))
        if out.stat().st_size <= max_mb * 1e6:
            break
    return out, dpi, out.stat().st_size / 1e6

