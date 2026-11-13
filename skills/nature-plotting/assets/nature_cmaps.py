"""
nature_cmaps.py
===============
House colour maps, categorical palettes and Nature-style colour bars.

Rules this module is built around (Nature figure guide + Crameri et al., Nat. Commun. 11, 5444, 2020):
  * no rainbow / jet maps for ordered data; lightness must change monotonically (sequential) or
    symmetrically about a neutral centre (diverging);
  * no red-green pairs for categories that must be told apart;
  * colour bars are part of the data: slim, labelled with quantity and unit, ticks inward,
    outline at the axes line width, extend triangles when values are clipped.

Usage
-----
    from nature_style import *
    from nature_cmaps import *

    im = ax.imshow(z, cmap=NS_EMBER)
    cb = cbar_side(ax, im, "Intensity (norm.)", extend="max")

Every ``NS_*`` map is also registered with matplotlib as ``"ns_<name>"`` (e.g. ``cmap="ns_ember"``),
and has a reversed twin ``"ns_<name>_r"``.

Author: Denghui Pan
"""
from __future__ import annotations

import numpy as np
import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.cm as mcm
import matplotlib.ticker as mticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from nature_style import (PALETTE, CYCLE, SPECTRUM_VNIR, SPECTRUM_VNIR_SAT, SPECTRUM_VNIR_SOFT, VNIR_RANGE,
                          NATURE_DIV, NATURE_SEQ, NATURE_COOL)

__all__ = [
    # maps
    "NS_REDS", "NS_BLUES", "NS_GREENS", "NS_PURPLES", "NS_GRAYS",
    "NS_EMBER", "NS_GLACIER", "NS_SUNSET",
    "NS_DIV_BR", "NS_DIV_PG", "NS_DIV_BO", "NS_DIV_DARK",
    "NS_PHASE", "NS_VISIBLE",
    "SEQUENTIAL", "DIVERGING", "CYCLIC", "SPECIAL", "ALL_CMAPS",
    # palettes
    "HOUSE", "HOUSE_DARK", "OKABE_ITO", "PAIRED", "GRAYS", "METHOD_COLORS",
    # colour science
    "srgb_to_lab", "lightness", "is_monotonic", "simulate_cvd", "wavelength_rgb",
    "discrete_cmap", "truncate_cmap", "lighten", "darken",
    # colour bars
    "style_cbar", "cbar_side", "cbar_inset", "cbar_top", "cbar_span", "cbar_discrete",
    "cbar_endlabels", "line_mappable", "spectrum_strip", "center_norm", "log_ticks",
]


# ----------------------------------------------------------------------------------- colour science
def _srgb_to_linear(c):
    c = np.asarray(c, dtype=float)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _linear_to_srgb(c):
    c = np.clip(np.asarray(c, dtype=float), 0, 1)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * c ** (1 / 2.4) - 0.055)


def srgb_to_lab(rgb):
    """sRGB (N x 3, 0-1) -> CIE L*a*b* (D65)."""
    rgb = np.atleast_2d(np.asarray(rgb, dtype=float))[:, :3]
    lin = _srgb_to_linear(rgb)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = lin @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > (6 / 29) ** 3, np.cbrt(xyz), xyz / (3 * (6 / 29) ** 2) + 4 / 29)
    L = 116 * f[:, 1] - 16
    a = 500 * (f[:, 0] - f[:, 1])
    b = 200 * (f[:, 1] - f[:, 2])
    return np.column_stack([L, a, b])


def lightness(cmap, n=256):
    """CIE L* along a colour map (0 = black, 100 = white)."""
    cmap = mpl.colormaps[cmap] if isinstance(cmap, str) else cmap
    return srgb_to_lab(cmap(np.linspace(0, 1, n)))[:, 0]


def is_monotonic(cmap, tol=0.5):
    """True if L* rises or falls monotonically (within tol) -- the test a sequential map must pass."""
    d = np.diff(lightness(cmap))
    return bool(np.all(d >= -tol) or np.all(d <= tol))


# Machado, Oliveira & Fernandes (2009), severity 1.0, applied in linear RGB
_CVD = {
    "protan": np.array([[0.152286, 1.052583, -0.204868],
                        [0.114503, 0.786281, 0.099216],
                        [-0.003882, -0.048116, 1.051998]]),
    "deutan": np.array([[0.367322, 0.860646, -0.227968],
                        [0.280085, 0.672501, 0.047413],
                        [-0.011820, 0.042940, 0.968881]]),
    "tritan": np.array([[1.255528, -0.076749, -0.178779],
                        [-0.078411, 0.930809, 0.147602],
                        [0.004733, 0.691367, 0.303900]]),
}


def simulate_cvd(rgb, kind="deutan"):
    """Simulate colour-vision deficiency ('protan', 'deutan', 'tritan') on sRGB colours or an RGB(A) image."""
    a = np.asarray(rgb, dtype=float)
    shape = a.shape
    flat = a.reshape(-1, shape[-1])
    out = flat.copy()
    out[:, :3] = _linear_to_srgb(_srgb_to_linear(flat[:, :3]) @ _CVD[kind].T)
    return out.reshape(shape)


def wavelength_rgb(wl_nm, gamma=0.8):
    """Approximate perceived colour of monochromatic light (380-780 nm; black outside).
    Use for true-colour spectrum strips, not as a data colour map (it is not perceptually uniform)."""
    w = np.atleast_1d(np.asarray(wl_nm, dtype=float))
    r = np.zeros_like(w); g = np.zeros_like(w); b = np.zeros_like(w)
    m = (w >= 380) & (w < 440); r[m] = -(w[m] - 440) / 60; b[m] = 1
    m = (w >= 440) & (w < 490); g[m] = (w[m] - 440) / 50; b[m] = 1
    m = (w >= 490) & (w < 510); g[m] = 1; b[m] = -(w[m] - 510) / 20
    m = (w >= 510) & (w < 580); r[m] = (w[m] - 510) / 70; g[m] = 1
    m = (w >= 580) & (w < 645); r[m] = 1; g[m] = -(w[m] - 645) / 65
    m = (w >= 645) & (w <= 780); r[m] = 1
    f = np.ones_like(w)
    m = (w >= 380) & (w < 420); f[m] = 0.3 + 0.7 * (w[m] - 380) / 40
    m = (w > 700) & (w <= 780); f[m] = 0.3 + 0.7 * (780 - w[m]) / 80
    f[(w < 380) | (w > 780)] = 0
    rgb = np.column_stack([(r * f) ** gamma, (g * f) ** gamma, (b * f) ** gamma])
    return rgb[0] if np.ndim(wl_nm) == 0 else rgb


# ----------------------------------------------------------------------------------- building maps
def _make(name, stops, register=True):
    """LinearSegmentedColormap from colour stops (list of hex, or list of (pos, hex)); registered as ns_<name>."""
    cmap = mcolors.LinearSegmentedColormap.from_list(f"ns_{name}", stops, N=256)
    if register:
        for c in (cmap, cmap.reversed()):
            if c.name not in mpl.colormaps:
                mpl.colormaps.register(c)
    return cmap


def lighten(color, k=0.5):
    """Mix a colour with white (k=0: unchanged, k=1: white)."""
    c = np.array(mcolors.to_rgb(color))
    return tuple(c + (1 - c) * k)


def darken(color, k=0.3):
    """Mix a colour with black (k=0: unchanged, k=1: black)."""
    c = np.array(mcolors.to_rgb(color))
    return tuple(c * (1 - k))


def truncate_cmap(cmap, lo=0.0, hi=1.0, n=256):
    """Use only the [lo, hi] part of a map (e.g. drop the near-white end of a sequential map for lines)."""
    cmap = mpl.colormaps[cmap] if isinstance(cmap, str) else cmap
    return mcolors.ListedColormap(cmap(np.linspace(lo, hi, n)), name=f"{cmap.name}_{lo:.2f}_{hi:.2f}")


def discrete_cmap(cmap, n):
    """n equal bins of a continuous map (binned colour bar, ordered categories)."""
    cmap = mpl.colormaps[cmap] if isinstance(cmap, str) else cmap
    return mcolors.ListedColormap(cmap(np.linspace(0, 1, n)), name=f"{cmap.name}_{n}")


# Sequential, single hue (white -> house colour -> near black). L* falls monotonically.
NS_REDS = _make("reds", ["#FFF6F4", "#F9C9C3", "#F08A82", "#E84143", "#A3201F", "#4A0C0D"])
NS_BLUES = _make("blues", ["#F4F8FC", "#C9DDF0", "#86B4DE", "#2C6AB4", "#173A66", "#0A1A30"])
NS_GREENS = _make("greens", ["#F3FAF5", "#C5E7D1", "#7CC79B", "#39AF6B", "#1C6B3F", "#0B2E1B"])
NS_PURPLES = _make("purples", ["#F7F3FA", "#DDD0E9", "#B69BC8", "#7E5AA6", "#4B2A79", "#1F0F36"])
NS_GRAYS = _make("grays", ["#F7F7F7", "#CFCFCF", "#9A9A9A", "#666666", "#333333", "#0D0D0D"])

# Sequential, multi hue.
#   EMBER   dark -> purple -> red -> gold -> cream : intensity images, camera frames (inferno-like, house hues)
#   GLACIER navy -> blue -> teal -> mint -> cream  : densities, maps on white pages (cool counterpart)
#   SUNSET  cream -> sand -> salmon -> red -> wine : error / loss heat maps (light = good, dark = bad)
NS_EMBER = _make("ember", ["#07071A", "#2B1250", "#6B1F6E", "#B2304F", "#E84143", "#F2853A", "#F8C45C", "#FCF1C8"])
NS_GLACIER = _make("glacier", ["#0B1730", "#173A66", "#2C6AB4", "#3E9BC9", "#6CC3C1", "#A8DCC5", "#E2F2DE", "#FBFDF5"])
NS_SUNSET = _make("sunset", ["#FFF9EC", "#F7E3B5", "#F2C08F", "#EC8E77", "#E84143", "#A3201F", "#4A0C0D"])

# Diverging: neutral light centre, matched lightness on both arms.
NS_DIV_BR = _make("div_br", ["#14305A", "#2C6AB4", "#8DBEE6", "#F5F5F5", "#F2A19C", "#D03A3C", "#6B1214"])
NS_DIV_PG = _make("div_pg", ["#3A1E5C", "#7E5AA6", "#D6C4E3", "#F5F5F5", "#A9D9B9", "#2E8F57", "#0B3D20"])
NS_DIV_BO = _make("div_bo", ["#14305A", "#2C6AB4", "#9CC6E8", "#F5F5F5", "#F6C48F", "#C96A22", "#5A2606"])
# dark centre (for signed data shown on a black image plate)
NS_DIV_DARK = _make("div_dark", ["#9CD3F5", "#2C6AB4", "#0D1626", "#000000", "#2A0A0B", "#E84143", "#F7B4AE"])

# Cyclic (phase, angle): same colour at 0 and 2*pi, light at 0, dark at pi.
NS_PHASE = _make("phase", ["#EDEDED", "#8DBEE6", "#2C6AB4", "#1B1B33", "#A3201F", "#E84143", "#F2A19C", "#EDEDED"])

# True visible colours 380-780 nm (labels / strips only; not perceptually uniform)
_vis_wl = np.linspace(380, 780, 256)
NS_VISIBLE = mcolors.ListedColormap(wavelength_rgb(_vis_wl), name="ns_visible")
if "ns_visible" not in mpl.colormaps:
    mpl.colormaps.register(NS_VISIBLE)

for _c in (SPECTRUM_VNIR, SPECTRUM_VNIR_SAT, SPECTRUM_VNIR_SOFT):
    if _c.name not in mpl.colormaps:
        mpl.colormaps.register(_c)

SEQUENTIAL = {"NS_REDS": NS_REDS, "NS_BLUES": NS_BLUES, "NS_GREENS": NS_GREENS, "NS_PURPLES": NS_PURPLES,
              "NS_GRAYS": NS_GRAYS, "NS_EMBER": NS_EMBER, "NS_GLACIER": NS_GLACIER, "NS_SUNSET": NS_SUNSET}
DIVERGING = {"NS_DIV_BR": NS_DIV_BR, "NS_DIV_PG": NS_DIV_PG, "NS_DIV_BO": NS_DIV_BO, "NS_DIV_DARK": NS_DIV_DARK}
CYCLIC = {"NS_PHASE": NS_PHASE}
SPECIAL = {"SPECTRUM_VNIR_SAT": SPECTRUM_VNIR_SAT, "SPECTRUM_VNIR_SOFT": SPECTRUM_VNIR_SOFT,
           "NS_VISIBLE": NS_VISIBLE}
ALL_CMAPS = {**SEQUENTIAL, **DIVERGING, **CYCLIC, **SPECIAL}

# ----------------------------------------------------------------------------------- categorical palettes
# HOUSE: default series colours (same as nature_style.CYCLE). First four are distinct for deutan/protan readers
# when paired with different markers or line styles.
HOUSE = list(CYCLE)
# HOUSE_DARK: line colours with enough contrast on white for thin (0.75-1 pt) lines and small text.
HOUSE_DARK = ["#2C6AB4", "#D03A3C", "#2E8F57", "#6A4C93", "#C99A1E", "#2A8C8C", "#8C5A2B", "#555555"]
# Okabe & Ito (2008): the reference colour-blind-safe set (use when > 4 categories must be separable by colour alone)
OKABE_ITO = ["#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"]
# PAIRED: (light, dark) of one hue -- raw vs processed, train vs test, before vs after
PAIRED = [("#8DCCF0", "#2C6AB4"), ("#F2A19C", "#E84143"), ("#9ED0C6", "#2E8F57"),
          ("#D6C4E3", "#6A4C93"), ("#F5DEA8", "#C99A1E"), ("#CFCFCF", "#555555")]
GRAYS = ["#1A1A1A", "#4D4D4D", "#808080", "#A6A6A6", "#CCCCCC", "#E6E6E6"]
# Fixed roles: "this work" is always the saturated red; references / baselines stay in blues and greys.
METHOD_COLORS = {"this_work": "#E84143", "ours": "#E84143", "baseline": "#808080", "baseline2": "#2C6AB4",
                 "reference": "#000000", "ground_truth": "#000000", "simulation": "#7F7F7F", "model": "#5B2C91"}


# ----------------------------------------------------------------------------------- colour bars
def style_cbar(cb, label=None, labelpad=2.0, ticks_in=True, minor=False, outline_lw=None, label_loc=None):
    """House look for a colour bar: outline = axes line width, short inward ticks, optional label."""
    lw = outline_lw if outline_lw is not None else mpl.rcParams["axes.linewidth"]
    cb.outline.set_linewidth(lw)
    ax = cb.ax
    ax.tick_params(which="both", direction="in" if ticks_in else "out",
                   length=mpl.rcParams["xtick.major.size"] * 0.6, width=lw,
                   labelsize=mpl.rcParams["ytick.labelsize"])
    ax.tick_params(which="minor", length=mpl.rcParams["xtick.major.size"] * 0.35)
    if not minor:
        ax.minorticks_off()
    # colour bars must not inherit the four-sided-tick default
    if cb.orientation == "vertical":
        ax.tick_params(left=False, labelleft=False, right=True, labelright=True)
    else:
        ax.tick_params(top=False, labeltop=False, bottom=True, labelbottom=True)
    if label is not None:
        if label_loc is None:
            cb.set_label(label, labelpad=labelpad, fontsize=mpl.rcParams["axes.labelsize"])
        else:
            cb.set_label(label, labelpad=labelpad, fontsize=mpl.rcParams["axes.labelsize"], loc=label_loc)
    return cb


def cbar_side(ax, mappable, label=None, size="4%", pad=0.05, side="right", extend=None, ticks=None,
              fmt=None, minor=False, **kw):
    """Slim colour bar glued to one side of *ax* (keeps the panel frame aligned with its neighbours).
    side: 'right' | 'left' | 'top' | 'bottom'. For log maps pass a LogNorm in the mappable; ticks stay decades."""
    fig = ax.figure
    cax = make_axes_locatable(ax).append_axes(side, size=size, pad=pad)
    orient = "vertical" if side in ("right", "left") else "horizontal"
    kwargs = dict(cax=cax, orientation=orient, ticks=ticks, format=fmt)
    if extend:
        kwargs["extend"] = extend
    cb = fig.colorbar(mappable, **kwargs, **kw)
    style_cbar(cb, label, minor=minor)
    if side == "left":
        cax.yaxis.set_ticks_position("left"); cax.yaxis.set_label_position("left")
        cax.tick_params(left=True, labelleft=True, right=False, labelright=False)
    if side == "top":
        cax.xaxis.set_ticks_position("top"); cax.xaxis.set_label_position("top")
        cax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
    return cb


def cbar_top(ax, mappable, label=None, size="5%", pad=0.04, **kw):
    """Horizontal colour bar above the panel, ticks and label on top (good for wide maps)."""
    return cbar_side(ax, mappable, label, size=size, pad=pad, side="top", **kw)


def cbar_inset(ax, mappable, label=None, loc="upper right", width="30%", height="4%", orientation="horizontal",
               borderpad=1.2, label_above=True, ticks=None, fmt=None, extend=None, bbox=None):
    """Small colour bar inside the panel (Nature style for a colour key that would otherwise eat a column).
    For a horizontal bar the label sits above it; tick labels below."""
    kw = dict(width=width, height=height, loc=loc, borderpad=borderpad)
    if bbox is not None:
        kw.update(bbox_to_anchor=bbox, bbox_transform=ax.transAxes)
    cax = inset_axes(ax, **kw)
    kwargs = dict(cax=cax, orientation=orientation, ticks=ticks, format=fmt)
    if extend:
        kwargs["extend"] = extend
    cb = ax.figure.colorbar(mappable, **kwargs)
    style_cbar(cb)
    if label is not None:
        if orientation == "horizontal" and label_above:
            cax.set_title(label, fontsize=mpl.rcParams["legend.fontsize"], pad=1.5)
        else:
            cb.set_label(label, fontsize=mpl.rcParams["legend.fontsize"], labelpad=1.5)
    return cb


def cbar_span(fig, axes, mappable, label=None, width_mm=2.0, pad_mm=1.5, extend=None, ticks=None, side="right"):
    """One colour bar spanning several panels (same norm), placed in figure mm units next to their union box.
    Call after the layout is final (after fig.subplots_adjust / before save)."""
    W, H = (v * 25.4 for v in fig.get_size_inches())
    boxes = [a.get_position() for a in np.ravel(axes)]
    x0 = min(b.x0 for b in boxes); x1 = max(b.x1 for b in boxes)
    y0 = min(b.y0 for b in boxes); y1 = max(b.y1 for b in boxes)
    if side == "right":
        cax = fig.add_axes([x1 + pad_mm / W, y0, width_mm / W, y1 - y0])
        orient = "vertical"
    else:  # top
        cax = fig.add_axes([x0, y1 + pad_mm / H, x1 - x0, width_mm / H])
        orient = "horizontal"
    kwargs = dict(cax=cax, orientation=orient, ticks=ticks)
    if extend:
        kwargs["extend"] = extend
    cb = fig.colorbar(mappable, **kwargs)
    style_cbar(cb, label)
    if side == "top":
        cax.xaxis.set_ticks_position("top"); cax.xaxis.set_label_position("top")
        cax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
    return cb


def cbar_discrete(ax, cmap, bounds=None, categories=None, label=None, side="right", size="4%", pad=0.05):
    """Binned or categorical colour bar.
    bounds: bin edges for a binned quantity (ticks on the edges);
    categories: names for an ordinal/categorical map (ticks centred on each block).
    Returns (norm, cmap, cb) -- use norm/cmap for the plot itself."""
    if categories is not None:
        n = len(categories)
        cm_ = discrete_cmap(cmap, n)
        norm = mcolors.BoundaryNorm(np.arange(n + 1) - 0.5, n)
        sm = mcm.ScalarMappable(norm=norm, cmap=cm_)
        cb = cbar_side(ax, sm, label, side=side, size=size, pad=pad, ticks=np.arange(n))
        (cb.ax.set_yticklabels if cb.orientation == "vertical" else cb.ax.set_xticklabels)(categories)
        cb.ax.tick_params(length=0)
    else:
        bounds = np.asarray(bounds, dtype=float)
        n = len(bounds) - 1
        cm_ = discrete_cmap(cmap, n)
        norm = mcolors.BoundaryNorm(bounds, n)
        sm = mcm.ScalarMappable(norm=norm, cmap=cm_)
        cb = cbar_side(ax, sm, label, side=side, size=size, pad=pad, ticks=bounds)
    return norm, cm_, cb


def cbar_endlabels(cb, lo_text, hi_text, fontsize=None):
    """Replace ticks by two end labels ('0' ... 'max') -- for normalised image colour bars."""
    fs = fontsize or mpl.rcParams["legend.fontsize"]
    ax = cb.ax
    ax.tick_params(which="both", length=0, labelbottom=False, labelleft=False, labelright=False, labeltop=False)
    if cb.orientation == "horizontal":
        ax.text(-0.03, 0.5, lo_text, transform=ax.transAxes, ha="right", va="center", fontsize=fs)
        ax.text(1.03, 0.5, hi_text, transform=ax.transAxes, ha="left", va="center", fontsize=fs)
    else:
        ax.text(0.5, -0.03, lo_text, transform=ax.transAxes, ha="center", va="top", fontsize=fs)
        ax.text(0.5, 1.03, hi_text, transform=ax.transAxes, ha="center", va="bottom", fontsize=fs)
    return cb


def line_mappable(cmap, vmin=None, vmax=None, norm=None):
    """ScalarMappable for colour-coding a family of lines/markers by a parameter (then pass to a cbar_* helper).
    Returns (sm, color_of) where color_of(value) gives the line colour."""
    cmap = mpl.colormaps[cmap] if isinstance(cmap, str) else cmap
    norm = norm or mcolors.Normalize(vmin, vmax)
    sm = mcm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])
    return sm, (lambda v: cmap(norm(v)))


def spectrum_strip(ax, lo=None, hi=None, height=0.035, cmap=None, where="bottom", alpha=1.0, zorder=3):
    """Colour strip along the x axis inside the frame (wavelength key under a spectrum).
    Default map: SPECTRUM_VNIR_SAT over the current x range; pass cmap=NS_VISIBLE + lo/hi in nm for true colour."""
    x0, x1 = ax.get_xlim()
    lo = x0 if lo is None else lo
    hi = x1 if hi is None else hi
    cmap = cmap or SPECTRUM_VNIR_SAT
    if cmap is NS_VISIBLE:
        cols = wavelength_rgb(np.linspace(lo, hi, 512))
        img = cols[None, :, :]
    else:
        frac = (np.linspace(lo, hi, 512) - VNIR_RANGE[0]) / (VNIR_RANGE[1] - VNIR_RANGE[0])
        img = cmap(np.clip(frac, 0, 1))[None, :, :3]
    y0, y1 = (0, height) if where == "bottom" else (1 - height, 1)
    ax.imshow(img, extent=(lo, hi, y0, y1), transform=ax.get_xaxis_transform(), aspect="auto",
              alpha=alpha, zorder=zorder, interpolation="bilinear")
    ax.set_xlim(x0, x1)
    return ax


def center_norm(vmin, vcenter, vmax):
    """Diverging norm with the neutral colour pinned to vcenter (asymmetric ranges allowed)."""
    return mcolors.TwoSlopeNorm(vcenter=vcenter, vmin=vmin, vmax=vmax)


def log_ticks(axis, base=10, minor=True):
    """Decade majors (10^k) and 2-9 minors on a log axis or log colour bar axis."""
    axis.set_major_locator(mticker.LogLocator(base=base))
    axis.set_major_formatter(mticker.LogFormatterSciNotation(base=base))
    if minor:
        axis.set_minor_locator(mticker.LogLocator(base=base, subs=np.arange(2, 10)))
        axis.set_minor_formatter(mticker.NullFormatter())
    return axis
