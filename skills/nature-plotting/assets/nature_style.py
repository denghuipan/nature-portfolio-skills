"""
nature_style.py
================
House plotting style for Nature-family journals (Nature, Nature Photonics, Nature Communications ...):
rcParams, print sizes, palette, wavelength colour maps, export and pre-submission checks.

Default preset ``np_final`` matches Nature Portfolio print widths (89 / 183 mm)
and 5–7 pt typography at that size. Use ``apply_preset("preview")`` for large
group-meeting previews.

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

OUTDIR = Path("figure_preview")      # default output folder of save*(); created only when a figure is saved into it

# ---------------- Nature Portfolio layout (Nature Photonics uses same guide) ----------------
MM_PER_IN = 25.4
WIDTH_1COL_MM = 89
WIDTH_2COL_MM = 183
MAX_FIG_HEIGHT_MM = 170

# Common panel heights (mm), scaled from earlier preview aspect ratios at 89 mm width
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
    "preview": {
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

_PRESET_ALIASES = {"mock": "preview"}          # old name kept so earlier scripts still run

_ACTIVE_PRESET = "np_final"
_PANEL_LABEL_SIZE = _PRESETS["np_final"]["panel_label_size"]

# Arial first (Nature house face); Helvetica / Liberation Sans (metric clone of Arial on Linux) as fall-backs.
# Only installed families are listed, so matplotlib does not print "findfont" warnings on machines without Arial.
_FONT_PREFS = ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"]


def _available_fonts(prefs=_FONT_PREFS):
    from matplotlib import font_manager
    have = {f.name for f in font_manager.fontManager.ttflist}
    out = [f for f in prefs if f in have]
    return out or ["DejaVu Sans"]


FONT_FAMILY = _available_fonts()
SANS = FONT_FAMILY[0]          # the face actually used (Arial on Windows / macOS)

_BASE_RCPARAMS = {
    "font.family": FONT_FAMILY,
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


# ---------------- palette (from reference cards) ----------------
PALETTE = {
    "red": "#E84143", "rose": "#EE8284", "salmon": "#EA998F",
    "blue": "#2C6AB4", "navy": "#7491C9", "skyblue": "#5AB2E4", "lightblue": "#8DCCF0",
    "green": "#39AF6B", "teal": "#92CCBB", "mint": "#9ED0C6",
    "purple": "#B69BC8", "pink": "#EDA2C5",
    "sand": "#F5DEA8", "olive": "#D3E2B4", "gray": "#807979", "brown": "#8B5A2B",
}
CYCLE = ["#2C6AB4", "#E84143", "#39AF6B", "#B69BC8", "#5AB2E4", "#EA998F", "#9ED0C6", "#F5DEA8"]

SPECTRAL = mcolors.LinearSegmentedColormap.from_list(
    "spectral_vis", ["#2C2C8F", "#2C6AB4", "#39AF6B", "#9ED0C6", "#F5DEA8", "#EA998F", "#E84143", "#8B1A1C"])


def n_colors(cmap, n, lo=0.0, hi=1.0):
    """n evenly spaced colours from a colour map (one per ordered series)."""
    cmap = mpl.colormaps[cmap] if isinstance(cmap, str) else cmap
    return [cmap(v) for v in np.linspace(lo, hi, n)]

# wavelength colour map, visible to near-infrared (480-920 nm): blue -> cyan -> green -> yellow -> red -> dark red
VNIR_RANGE = (480, 920)                          # nm; use Normalize(*VNIR_RANGE) with SPECTRUM_VNIR
SPECTRUM_VNIR = mcolors.LinearSegmentedColormap.from_list("spectrum_vnir", [
    ((w - VNIR_RANGE[0]) / (VNIR_RANGE[1] - VNIR_RANGE[0]), c) for w, c in [
        (480, "#283A6E"), (500, "#3A64A3"), (550, "#5AAABF"), (600, "#71AE78"), (650, "#E0C063"),
        (700, "#C8423A"), (800, "#842022"), (920, "#2A0A0B")]])
# same stops with HLS saturation x1.4: for thin lines and small markers
SPECTRUM_VNIR_SAT = mcolors.LinearSegmentedColormap.from_list("spectrum_vnir_sat", [
    ((w - VNIR_RANGE[0]) / (VNIR_RANGE[1] - VNIR_RANGE[0]), c) for w, c in [
        (480, "#1A337C"), (500, "#2560B8"), (550, "#46B6D3"), (600, "#65BA6F"), (650, "#F9CC4A"),
        (700, "#E4291E"), (800, "#980C0F"), (920, "#300405")]])


def desaturate_cmap(cmap, k, n=256):
    """cmap with its HLS saturation scaled by k (k < 1: softer)."""
    import colorsys
    rgb = [colorsys.hls_to_rgb(h, l, min(1.0, s * k)) for h, l, s in
           (colorsys.rgb_to_hls(*cmap(i / (n - 1))[:3]) for i in range(n))]
    return mcolors.ListedColormap(rgb, name=f"{cmap.name}_x{k}")


# HLS saturation x0.75: muted version for large fills and many overlapping curves
SPECTRUM_VNIR_SOFT = desaturate_cmap(SPECTRUM_VNIR, 0.75)


def wl_color(w, cmap=None):
    """Colour of wavelength w (nm) in SPECTRUM_VNIR_SAT (or cmap) over VNIR_RANGE."""
    lo, hi = VNIR_RANGE
    return (cmap or SPECTRUM_VNIR_SAT)(float(np.clip((w - lo) / (hi - lo), 0, 1)))

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


def tint_axes(ax, color, a_bottom=0.22, a_top=0.03, n=256):
    """Soft vertical colour wash behind the data of ax (strongest at the bottom), in the panel's own colour --
    the 'tinted panel' style. Data limits are left untouched."""
    xl, yl = ax.get_xlim(), ax.get_ylim()
    img = np.ones((n, 2, 4)); img[:, :, :3] = mcolors.to_rgb(color)
    img[:, :, 3] = np.linspace(a_bottom, a_top, n)[:, None]
    ax.imshow(img, origin="lower", aspect="auto", interpolation="bilinear", transform=ax.transAxes,
              extent=(0, 1, 0, 1), zorder=0)
    ax.set_xlim(xl); ax.set_ylim(yl)


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


def audit_text(fig, min_pt=5.0, max_pt=8.0, show=True):
    """List every text artist of *fig* (labels, ticks, legends, annotations) whose font size is outside
    [min_pt, max_pt] (Nature: >= 5 pt, panel letters 8 pt). Returns [(size, text), ...]."""
    fig.canvas.draw()
    bad = []
    for t in fig.findobj(mpl.text.Text):
        s = t.get_text().strip()
        if not s or not t.get_visible():
            continue
        fs = float(t.get_fontsize())
        if fs < min_pt - 1e-6 or fs > max_pt + 1e-6:
            bad.append((fs, s))
    if show:
        print(f"[audit_text] {len(bad)} text items outside {min_pt}-{max_pt} pt")
        for fs, s in sorted(bad):
            print(f"   {fs:4.1f} pt  {s[:70]!r}")
    return bad


def save_fig_exact(fig, name, outdir=OUTDIR, dpi=SAVE_DPI, warn_mm=0.3):
    """Save PNG + PDF at the exact canvas size (no tight bbox), so a 183 mm layout is 183 mm wide.
    Warns when the tight bounding box of the drawn content sticks out of the canvas by more than *warn_mm*."""
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

