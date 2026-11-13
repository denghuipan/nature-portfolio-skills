"""
nature_charts.py
================
Reusable chart builders on top of ``nature_style`` (house rcParams, palette, sizes) and ``nature_cmaps``
(colour maps, colour bars). Each function draws into an existing Axes so that panels can be combined freely
in a composite figure; none of them creates a figure or changes global rcParams.

Grouped by job:
    annotation      direct_label, end_label, ref_line, regime, band, double_arrow, callout, stats_text,
                    place_labels
    axes            secondary_unit_axis, broken_windows, share_labels,
                    inset_zoom, scale_bar, despine_inner
    lines / bands   ci_band, step_series
    distributions   boxplot, jitter, half_violin, mean_sd, hist_step, kde_line, ecdf, ridgeline
    comparison      bars, grouped_bars, stacked_barh, lollipop, dumbbell, waterfall, forest, radar
    matrices        heatmap, corr_triangle
    relationships   parity, fit_line, landscape
    export          export

Author: Denghui Pan
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
import matplotlib.transforms as mtransforms
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon

from nature_style import (PALETTE, CYCLE, MM_PER_IN, SAVE_DPI, style_axes, save_fig, save_fig_exact,
                          audit_text, gradient_fill)
from nature_cmaps import lighten, darken, HOUSE, HOUSE_DARK

__all__ = [
    "direct_label", "end_label", "ref_line", "regime", "band", "double_arrow", "callout", "stats_text",
    "place_labels", "secondary_unit_axis", "broken_windows", "share_labels",
    "inset_zoom", "scale_bar", "despine_inner", "ci_band", "step_series", "boxplot", "jitter", "half_violin",
    "mean_sd", "hist_step", "kde_line", "ecdf", "ridgeline", "bars", "grouped_bars", "stacked_barh",
    "lollipop", "dumbbell", "waterfall", "forest", "radar", "heatmap", "corr_triangle", "parity",
    "fit_line", "landscape", "export", "pt",
]


def pt(v):
    """Points -> inches (for offsets in mm/pt-based layouts)."""
    return v / 72.0


def _fs(kind="legend"):
    return mpl.rcParams[{"legend": "legend.fontsize", "label": "axes.labelsize", "tick": "xtick.labelsize"}[kind]]


# =================================================================================================== annotation
def direct_label(ax, x, y, text, color="k", dx=2.0, dy=0.0, ha="left", va="center", fontsize=None, **kw):
    """Text next to a data point, offset by (dx, dy) points -- the Nature preference over a detached legend."""
    tr = ax.transData + mtransforms.ScaledTranslation(pt(dx), pt(dy), ax.figure.dpi_scale_trans)
    return ax.text(x, y, text, color=color, transform=tr, ha=ha, va=va, fontsize=fontsize or _fs(), **kw)


def end_label(ax, line, text=None, dx=2.0, dy=0.0, where="end", **kw):
    """Label a Line2D at its last (or first) point in the line's own colour."""
    xd, yd = np.asarray(line.get_xdata(), float), np.asarray(line.get_ydata(), float)
    ok = np.isfinite(xd) & np.isfinite(yd)
    xd, yd = xd[ok], yd[ok]
    i = -1 if where == "end" else 0
    ha = kw.pop("ha", "left" if where == "end" else "right")
    return direct_label(ax, xd[i], yd[i], text or line.get_label(), color=line.get_color(),
                        dx=dx if where == "end" else -dx, dy=dy, ha=ha, **kw)


def ref_line(ax, value, axis="x", label=None, color="0.35", ls=":", lw=None, pos=0.97, side="right",
             fontsize=None, zorder=1.5):
    """Reference / threshold line with its label placed beside (never on top of) the line.
    axis='x' -> vertical line at x=value; label rotated 90 deg, offset 2 pt to `side` ('right'|'left').
    axis='y' -> horizontal line; label just above it at `pos` (axes fraction along x), ha from side."""
    lw = lw or mpl.rcParams["axes.linewidth"]
    fs = fontsize or _fs()
    if axis == "x":
        ln = ax.axvline(value, color=color, ls=ls, lw=lw, zorder=zorder)
        if label:
            dx = 2.0 if side == "right" else -2.0
            tr = mtransforms.blended_transform_factory(ax.transData, ax.transAxes) + \
                mtransforms.ScaledTranslation(pt(dx), 0, ax.figure.dpi_scale_trans)
            ax.text(value, pos, label, rotation=90, transform=tr, color=color, fontsize=fs,
                    ha="left" if side == "right" else "right", va="top")
    else:
        ln = ax.axhline(value, color=color, ls=ls, lw=lw, zorder=zorder)
        if label:
            tr = mtransforms.blended_transform_factory(ax.transAxes, ax.transData) + \
                mtransforms.ScaledTranslation(0, pt(1.5), ax.figure.dpi_scale_trans)
            ax.text(pos, value, label, transform=tr, color=color, fontsize=fs,
                    ha="right" if side == "right" else "left", va="bottom")
    return ln


def regime(ax, x0, x1, color="0.45", gradient=True, fade="in", alpha=(0.0, 0.45), label=None,
           label_color=None, label_rot=90, label_x=None, zorder=0.5):
    """Shade an x-interval spanning the full height: a 'below detection limit', 'failure' or 'not accessible' zone.
    gradient=True draws a horizontal alpha ramp (fade='in': transparent at x0 -> alpha[1] at x1; 'out' reverse),
    which reads as 'getting worse towards the edge' without a hard boundary."""
    rgb = mcolors.to_rgb(color)
    if gradient:
        a = np.linspace(alpha[0], alpha[1], 256)      # transparent at x0 -> strong at x1 (data order)
        if fade == "out":
            a = a[::-1]
        if x1 < x0:                                   # image columns run from min(x) to max(x)
            a = a[::-1]
        img = np.ones((1, 256, 4)); img[..., :3] = rgb; img[0, :, 3] = a
        yl = ax.get_ylim(); xl = ax.get_xlim()
        ax.imshow(img, extent=(min(x0, x1), max(x0, x1), 0, 1), transform=ax.get_xaxis_transform(),
                  aspect="auto", interpolation="bilinear", zorder=zorder)
        ax.set_xlim(xl); ax.set_ylim(yl)
    else:
        ax.axvspan(x0, x1, color=rgb, alpha=alpha[1], lw=0, zorder=zorder)
    if label:
        lx = label_x if label_x is not None else (x0 + x1) / 2
        ax.text(lx, 0.5, label, rotation=label_rot, transform=ax.get_xaxis_transform(),
                ha="center", va="center", color=label_color or darken(color, 0.25), fontsize=_fs())
    return ax


def band(ax, y0, y1, color="0.85", alpha=0.6, label=None, label_pos=0.98, zorder=0.4):
    """Horizontal tolerance band (e.g. +-5 %) with an optional label at the top right inside it."""
    ax.axhspan(y0, y1, color=color, alpha=alpha, lw=0, zorder=zorder)
    if label:
        tr = mtransforms.blended_transform_factory(ax.transAxes, ax.transData)
        ax.text(label_pos, y1, label, transform=tr, ha="right", va="bottom", fontsize=_fs(), color="0.35")


def double_arrow(ax, p0, p1, text=None, color="0.15", lw=None, text_offset=2.0, text_side="above",
                 fontsize=None, mutation_scale=6, shrink=0.0):
    """Measurement arrow <-> between two data points (a gap, a width, a distance)."""
    lw = lw or mpl.rcParams["axes.linewidth"]
    arr = FancyArrowPatch(p0, p1, arrowstyle="<|-|>", mutation_scale=mutation_scale, color=color, lw=lw,
                          shrinkA=shrink, shrinkB=shrink, zorder=4)
    ax.add_patch(arr)
    if text:
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        dy = text_offset if text_side == "above" else -text_offset
        direct_label(ax, mx, my, text, color=color, dx=0, dy=dy, ha="center",
                     va="bottom" if text_side == "above" else "top", fontsize=fontsize)
    return arr


def callout(ax, xy, xytext, text, color="0.2", fontsize=None, arrow=True, ha="left", va="center", **kw):
    """Text with a thin leader line to a data point (xytext in data coordinates)."""
    props = dict(arrowstyle="-", lw=mpl.rcParams["axes.linewidth"] * 0.8, color=color,
                 shrinkA=1.5, shrinkB=1.5) if arrow else None
    return ax.annotate(text, xy=xy, xytext=xytext, color=color, fontsize=fontsize or _fs(),
                       ha=ha, va=va, arrowprops=props, **kw)


def stats_text(ax, lines, loc="upper left", color="0.15", fontsize=None, pad=0.04, linespacing=1.25):
    """Small block of statistics ('MAE 0.05', 'n = 600', 'R^2 = 0.998') in a corner, no box."""
    pos = {"upper left": (pad, 1 - pad, "left", "top"), "upper right": (1 - pad, 1 - pad, "right", "top"),
           "lower left": (pad, pad, "left", "bottom"), "lower right": (1 - pad, pad, "right", "bottom")}[loc]
    return ax.text(pos[0], pos[1], "\n".join(lines), transform=ax.transAxes, ha=pos[2], va=pos[3],
                   color=color, fontsize=fontsize or _fs(), linespacing=linespacing)


def place_labels(ax, xs, ys, texts, colors=None, fontsize=None, offsets=None, avoid_points=True, pad_px=1.0):
    """Put a label next to every point without overlapping other labels or points (greedy, 8 candidate offsets).
    Good for literature 'landscape' plots with numbered references. Returns the Text artists."""
    fig = ax.figure
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    fs = fontsize or _fs()
    offsets = offsets or [(3, 0, "left", "center"), (-3, 0, "right", "center"), (0, 3, "center", "bottom"),
                          (0, -3, "center", "top"), (3, 3, "left", "bottom"), (-3, 3, "right", "bottom"),
                          (3, -3, "left", "top"), (-3, -3, "right", "top"), (6, 0, "left", "center"),
                          (-6, 0, "right", "center")]
    colors = colors or ["0.2"] * len(texts)
    pts_disp = ax.transData.transform(np.column_stack([xs, ys]))
    marker_r = 3.0 * fig.dpi / 72
    taken = []
    out = []
    axbox = ax.get_window_extent(r)
    for (x, y), t, c, (px, py) in zip(zip(xs, ys), texts, colors, pts_disp):
        best = None
        for dx, dy, ha, va in offsets:
            tx = direct_label(ax, x, y, t, color=c, dx=dx, dy=dy, ha=ha, va=va, fontsize=fs)
            bb = tx.get_window_extent(r).expanded(1.0, 1.0)
            bb = mtransforms.Bbox.from_extents(bb.x0 - pad_px, bb.y0 - pad_px, bb.x1 + pad_px, bb.y1 + pad_px)
            clash = any(bb.overlaps(o) for o in taken) or not (axbox.contains(bb.x0, bb.y0) and
                                                               axbox.contains(bb.x1, bb.y1))
            if avoid_points and not clash:
                for (qx, qy) in pts_disp:
                    if (qx, qy) == (px, py):
                        continue
                    if bb.x0 - marker_r < qx < bb.x1 + marker_r and bb.y0 - marker_r < qy < bb.y1 + marker_r:
                        clash = True
                        break
            if not clash:
                best = (tx, bb)
                break
            tx.remove()
        if best is None:  # fall back to the first offset
            dx, dy, ha, va = offsets[0]
            tx = direct_label(ax, x, y, t, color=c, dx=dx, dy=dy, ha=ha, va=va, fontsize=fs)
            best = (tx, tx.get_window_extent(r))
        taken.append(best[1])
        out.append(best[0])
    return out


# =================================================================================================== axes
def secondary_unit_axis(ax, which="x", functions=None, label=None, ticks=None, ticklabels=None, location=None,
                        color=None):
    """Second axis showing the same quantity in other units (nm <-> THz, K <-> eV, s <-> min).
    functions = (forward, inverse). Returns the secondary axis, styled with inward ticks."""
    if which == "x":
        sec = ax.secondary_xaxis(location or "top", functions=functions)
        axis = sec.xaxis
    else:
        sec = ax.secondary_yaxis(location or "right", functions=functions)
        axis = sec.yaxis
    if ticks is not None:
        axis.set_ticks(ticks)
        if ticklabels is not None:
            axis.set_ticklabels(ticklabels)
    sec.tick_params(which="both", direction="in")
    if label:
        (sec.set_xlabel if which == "x" else sec.set_ylabel)(label)
    if color:
        sec.tick_params(colors=color)
        sec.spines[location or ("top" if which == "x" else "right")].set_color(color)
        axis.label.set_color(color)
    if which == "x":
        ax.tick_params(top=False, which="both")
    else:
        ax.tick_params(right=False, which="both")
    sec.minorticks_off()
    return sec


def broken_windows(fig, subplotspec, windows, gap=0.012, sharey=True, mark_size=3.0, wspace=None):
    """Side-by-side axes that show separate x windows of one continuous axis (narrow features far apart),
    with '//' break marks on the frame. windows = [(x0, x1), ...]. Returns list of axes."""
    n = len(windows)
    gs = subplotspec.subgridspec(1, n, wspace=wspace if wspace is not None else gap * n)
    axes = []
    for i, (a, b) in enumerate(windows):
        ax = fig.add_subplot(gs[0, i], sharey=axes[0] if (sharey and axes) else None)
        ax.set_xlim(a, b)
        if i > 0:
            ax.spines["left"].set_visible(False)
            ax.tick_params(which="both", left=False, labelleft=False)
        if i < n - 1:
            ax.spines["right"].set_visible(False)
            ax.tick_params(which="both", right=False)
        axes.append(ax)
    d = mark_size / 72 * fig.dpi  # px
    kw = dict(marker=[(-1, -1.6), (1, 1.6)], markersize=mark_size * 1.6, linestyle="none", color="k",
              mec="k", mew=mpl.rcParams["axes.linewidth"], clip_on=False)
    for i, ax in enumerate(axes):
        if i < n - 1:
            ax.plot([1, 1], [0, 1], transform=ax.transAxes, **kw)
        if i > 0:
            ax.plot([0, 0], [0, 1], transform=ax.transAxes, **kw)
    return axes


def share_labels(fig, axes, xlabel=None, ylabel=None, xpad_mm=1.0, ypad_mm=1.0, fontsize=None):
    """One x label under and one y label left of a block of small multiples (instead of repeating them).
    Call after the layout is fixed; positions use the tight boxes of the tick labels."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    axes = list(np.ravel(axes))
    W, H = fig.bbox.width, fig.bbox.height
    tb = [a.get_tightbbox(r) for a in axes]
    pos = [a.get_position() for a in axes]
    x0 = min(p.x0 for p in pos); x1 = max(p.x1 for p in pos)
    y0 = min(p.y0 for p in pos); y1 = max(p.y1 for p in pos)
    fs = fontsize or mpl.rcParams["axes.labelsize"]
    out = []
    if xlabel:
        ybot = min(b.y0 for b in tb) / H - xpad_mm / 25.4 * fig.dpi / H
        out.append(fig.text((x0 + x1) / 2, ybot, xlabel, ha="center", va="top", fontsize=fs))
    if ylabel:
        xleft = min(b.x0 for b in tb) / W - ypad_mm / 25.4 * fig.dpi / W
        out.append(fig.text(xleft, (y0 + y1) / 2, ylabel, ha="right", va="center", rotation=90, fontsize=fs))
    return out


def inset_zoom(ax, bounds, xlim, ylim, label=None, edgecolor="0.35", ls="--", connect=False):
    """Inset axes (bounds in axes fraction [x, y, w, h]) showing a zoom of the parent, with a dashed box on the
    parent. Returns the inset axes; plot into it like any other axes."""
    axins = ax.inset_axes(bounds)
    axins.set_xlim(*xlim); axins.set_ylim(*ylim)
    style_axes(axins)
    axins.tick_params(labelsize=mpl.rcParams["xtick.labelsize"] * 0.9)
    rect = Rectangle((xlim[0], ylim[0]), xlim[1] - xlim[0], ylim[1] - ylim[0], fill=False,
                     ec=edgecolor, ls=ls, lw=mpl.rcParams["axes.linewidth"] * 0.8, zorder=5)
    ax.add_patch(rect)
    if label:
        ax.text(xlim[1], ylim[1], label, ha="left", va="bottom", fontsize=_fs(), color=edgecolor)
    if connect:
        ax.indicate_inset_zoom(axins, edgecolor=edgecolor, lw=mpl.rcParams["axes.linewidth"] * 0.6)
    for sp in axins.spines.values():
        sp.set_edgecolor(edgecolor)
    return axins


def scale_bar(ax, length, label, loc="lower right", color="w", lw=1.5, pad=0.06, fontsize=None, text_gap=1.5):
    """Scale bar in data units for images (Nature: scale bars, not magnifications)."""
    xl, yl = ax.get_xlim(), ax.get_ylim()
    w = abs(xl[1] - xl[0]); h = abs(yl[1] - yl[0])
    right = "right" in loc
    bottom = "lower" in loc
    xa = (max(xl) - pad * w - length) if right else (min(xl) + pad * w)
    flip_y = yl[0] > yl[1]  # imshow origin='upper'
    if bottom:
        ya = (max(yl) - pad * h) if flip_y else (min(yl) + pad * h)
    else:
        ya = (min(yl) + pad * h) if flip_y else (max(yl) - pad * h)
    ax.plot([xa, xa + length], [ya, ya], color=color, lw=lw, solid_capstyle="butt", zorder=6)
    up = (not flip_y) == bottom
    direct_label(ax, xa + length / 2, ya, label, color=color, dx=0, dy=text_gap if up else -text_gap,
                 ha="center", va="bottom" if up else "top", fontsize=fontsize)
    return ax


def despine_inner(axes_grid):
    """Hide tick labels on inner edges of a 2-D array of small multiples (keep ticks)."""
    axes_grid = np.atleast_2d(axes_grid)
    nr, nc = axes_grid.shape
    for i in range(nr):
        for j in range(nc):
            a = axes_grid[i, j]
            if i < nr - 1:
                a.tick_params(labelbottom=False)
            if j > 0:
                a.tick_params(labelleft=False)


# =================================================================================================== lines
def ci_band(ax, x, lo, hi, color, alpha=0.22, zorder=1, **kw):
    """Confidence / percentile band (no edge) under a line."""
    return ax.fill_between(x, lo, hi, color=color, alpha=alpha, lw=0, zorder=zorder, **kw)


def step_series(ax, t, y, color="0.45", lw=None, where="post", markers=None, hollow_until=None, ms=3.0):
    """Step trace for set-points / control loops; markers optional (hollow until index hollow_until, then filled)."""
    lw = lw or mpl.rcParams["lines.linewidth"] * 0.6
    ax.step(t, y, where=where, color=color, lw=lw, zorder=2)
    if markers:
        for i, (ti, yi) in enumerate(zip(t, y)):
            filled = hollow_until is not None and i >= hollow_until
            ax.plot(ti, yi, markers, ms=ms, mfc="k" if filled else "w", mec="k" if filled else color,
                    mew=0.6, zorder=3)


# =================================================================================================== distributions
def boxplot(ax, data, positions=None, colors=None, width=0.55, alpha=0.55, showfliers=False, median_color="k",
            whisker=(5, 95), edge="0.35"):
    """House box plot: light filled box, black median, whiskers at percentiles (default 5-95 %), no fliers
    (overlay the points with jitter() instead). Returns the bxp dict."""
    data = [np.asarray(d, float) for d in data]
    positions = positions if positions is not None else np.arange(1, len(data) + 1)
    colors = colors or HOUSE
    lw = mpl.rcParams["axes.linewidth"]
    bp = ax.boxplot(data, positions=positions, widths=width, patch_artist=True, showfliers=showfliers,
                    whis=whisker, manage_ticks=False,
                    medianprops=dict(color=median_color, lw=lw * 1.6),
                    whiskerprops=dict(color="k", lw=lw), capprops=dict(color="k", lw=lw),
                    boxprops=dict(lw=lw))
    for patch, c in zip(bp["boxes"], colors):
        patch.set_facecolor(mcolors.to_rgba(c, alpha))
        patch.set_edgecolor(edge)
    return bp


def jitter(ax, x, values, color, width=0.18, size=6, alpha=0.45, hollow=False, seed=0, zorder=3, **kw):
    """Individual observations as a jittered strip (always show n when n is small)."""
    rng = np.random.default_rng(seed)
    v = np.asarray(values, float)
    xs = x + rng.uniform(-width, width, v.size)
    if hollow:
        return ax.scatter(xs, v, s=size, facecolors="none", edgecolors=mcolors.to_rgba(color, alpha),
                          lw=0.6, zorder=zorder, **kw)
    return ax.scatter(xs, v, s=size, color=mcolors.to_rgba(color, alpha), lw=0, zorder=zorder, **kw)


def half_violin(ax, data, positions, colors, width=0.4, side="left", alpha=0.45, bw=None, cut=0.0):
    """Half violin (KDE) for raincloud plots. side='left' | 'right'."""
    from scipy.stats import gaussian_kde
    out = []
    for d, p, c in zip(data, positions, colors):
        d = np.asarray(d, float)
        kde = gaussian_kde(d, bw_method=bw)
        lo, hi = d.min() - cut * d.std(), d.max() + cut * d.std()
        y = np.linspace(lo, hi, 200)
        dens = kde(y)
        dens = dens / dens.max() * width
        xs = p - dens if side == "left" else p + dens
        poly = ax.fill_betweenx(y, p, xs, color=c, alpha=alpha, lw=0, zorder=1)
        ax.plot(xs, y, color=c, lw=mpl.rcParams["axes.linewidth"], zorder=2)
        out.append(poly)
    return out


def mean_sd(ax, x, values, color="k", capw=0.16, lw=None, center="mean", zorder=4):
    """Crossbar: mean (or median) as a wide tick, +-1 s.d. (or IQR) as a vertical bar."""
    v = np.asarray(values, float)
    lw = lw or mpl.rcParams["lines.linewidth"]
    if center == "mean":
        c, lo, hi = v.mean(), v.mean() - v.std(ddof=1), v.mean() + v.std(ddof=1)
    else:
        c, lo, hi = np.median(v), *np.percentile(v, [25, 75])
    ax.plot([x, x], [lo, hi], color=color, lw=lw, zorder=zorder, solid_capstyle="butt")
    ax.plot([x - capw, x + capw], [c, c], color=color, lw=lw * 1.3, zorder=zorder, solid_capstyle="butt")
    return c, lo, hi


def hist_step(ax, values, bins, color, label=None, density=True, fill_alpha=0.18, lw=None):
    """Outline histogram (overlays cleanly) with a light fill."""
    lw = lw or mpl.rcParams["lines.linewidth"] * 0.8
    h, e = np.histogram(values, bins=bins, density=density)
    ax.stairs(h, e, color=color, lw=lw, label=label, zorder=3)
    if fill_alpha:
        ax.stairs(h, e, color=color, alpha=fill_alpha, fill=True, lw=0, zorder=2)
    return h, e


def kde_line(ax, values, grid, color, lw=None, bw=None, scale=1.0, **kw):
    """Smooth density line (scipy gaussian_kde)."""
    from scipy.stats import gaussian_kde
    lw = lw or mpl.rcParams["lines.linewidth"]
    y = gaussian_kde(values, bw_method=bw)(grid) * scale
    return ax.plot(grid, y, color=color, lw=lw, **kw)[0]


def ecdf(ax, values, color, label=None, lw=None, **kw):
    """Empirical cumulative distribution (no binning choice to defend)."""
    v = np.sort(np.asarray(values, float))
    y = np.arange(1, v.size + 1) / v.size
    lw = lw or mpl.rcParams["lines.linewidth"]
    return ax.step(np.r_[v[0], v], np.r_[0, y], where="post", color=color, lw=lw, label=label, **kw)[0]


def ridgeline(ax, x, ys, colors, offset=1.0, scale=1.0, fill="gradient", fill_alpha=0.45, lw=None,
              labels_left=None, labels_right=None, label_colors=None, baseline=False, zorder_step=1):
    """Offset stack of curves (spectra, distributions, profiles). Bottom curve = first item.
    fill: 'gradient' (alpha ramp, house look), 'solid', or None. Returns list of y-offsets."""
    lw = lw or mpl.rcParams["lines.linewidth"] * 0.8
    offs = []
    n = len(ys)
    for i, (y, c) in enumerate(zip(ys, colors)):
        off = i * offset
        yy = np.asarray(y, float) * scale + off
        z = 10 + (n - i) * zorder_step  # lower curves in front
        if fill == "gradient":
            gradient_fill(ax, x, yy, color=c, alpha=fill_alpha, ymin=off, zorder=z - 0.5)
        elif fill == "solid":
            ax.fill_between(x, off, yy, color=lighten(c, 0.6), lw=0, zorder=z - 0.5)
        ax.plot(x, yy, color=c, lw=lw, zorder=z)
        if baseline:
            ax.plot([x[0], x[-1]], [off, off], color=c, lw=lw * 0.5, alpha=0.6, zorder=z)
        offs.append(off)
        lc = (label_colors or colors)[i]
        if labels_left:
            direct_label(ax, x[0], off + 0.35 * offset, labels_left[i], color=lc, dx=-3, ha="right")
        if labels_right:
            direct_label(ax, x[-1], yy[-20:].mean() + 0.12 * offset, labels_right[i], color="0.25", dx=-1,
                         ha="right", va="bottom")
    return offs


# =================================================================================================== comparison
def bars(ax, x, heights, colors=None, err=None, width=0.62, alpha=1.0, edge=None, points=None, point_color="k",
         labels=None, label_fmt="{:.2g}", hatch=None, capsize=2.0):
    """Bars with optional error bars, overlaid individual points and value labels."""
    colors = colors or [HOUSE[0]] * len(heights)
    lw = mpl.rcParams["axes.linewidth"]
    b = ax.bar(x, heights, width=width, color=[mcolors.to_rgba(c, alpha) for c in colors],
               edgecolor=edge or [darken(c, 0.25) for c in colors], lw=lw, zorder=2, hatch=hatch)
    if err is not None:
        ax.errorbar(x, heights, yerr=err, fmt="none", ecolor="k", elinewidth=lw, capsize=capsize,
                    capthick=lw, zorder=4)
    if points is not None:
        for xi, pts_ in zip(x, points):
            jitter(ax, xi, pts_, point_color, width=width * 0.25, size=5, alpha=0.7, zorder=5)
    if labels:
        for xi, h in zip(x, heights):
            direct_label(ax, xi, h, label_fmt.format(h), dx=0, dy=2, ha="center", va="bottom")
    return b


def grouped_bars(ax, groups, series, values, err=None, colors=None, width=0.8, points=None, legend=True,
                 alpha=1.0):
    """Grouped bar chart. values[s][g]; err same shape; points[s][g] -> list of observations."""
    ns = len(series)
    colors = colors or HOUSE
    w = width / ns
    x = np.arange(len(groups))
    handles = []
    for i, s in enumerate(series):
        xi = x - width / 2 + w * (i + 0.5)
        b = bars(ax, xi, values[i], colors=[colors[i]] * len(groups), err=None if err is None else err[i],
                 width=w * 0.92, alpha=alpha, points=None if points is None else points[i])
        b.set_label(s)
        handles.append(b)
    ax.set_xticks(x, groups)
    ax.tick_params(axis="x", which="minor", bottom=False, top=False)
    if legend:
        ax.legend(handles=handles, loc="upper left", ncols=min(ns, 3), handlelength=1.0, columnspacing=0.8)
    return x


def stacked_barh(ax, categories, parts, colors=None, percent=True, label_min=8.0, height=0.66, label_parts=True):
    """Horizontal stacked (100 %) bars for composition. parts = {name: values per category}.
    Segment labels are written inside segments wider than label_min (in %)."""
    names = list(parts)
    vals = np.array([parts[n] for n in names], float)
    if percent:
        vals = vals / vals.sum(axis=0, keepdims=True) * 100
    colors = colors or HOUSE
    y = np.arange(len(categories))[::-1]
    left = np.zeros(len(categories))
    for i, n in enumerate(names):
        ax.barh(y, vals[i], left=left, height=height, color=colors[i], edgecolor="w", lw=0.6, label=n, zorder=2)
        if label_parts:
            for yi, l, v in zip(y, left, vals[i]):
                if v >= label_min:
                    lum = np.dot(mcolors.to_rgb(colors[i]), [0.299, 0.587, 0.114])
                    ax.text(l + v / 2, yi, f"{v:.0f}", ha="center", va="center", fontsize=_fs(),
                            color="k" if lum > 0.6 else "w", zorder=3)
        left += vals[i]
    ax.set_yticks(y, categories)
    ax.tick_params(axis="y", which="both", left=False, right=False)
    if percent:
        ax.set_xlim(0, 100)
    return y


def lollipop(ax, labels, values, color="0.55", highlight=None, highlight_color="#E84143", sort=True, ms=4.0,
             value_fmt=None, baseline=0.0):
    """Ranked horizontal lollipop (cleaner than bars when there are many categories)."""
    labels = np.asarray(labels); values = np.asarray(values, float)
    if sort:
        o = np.argsort(values)
        labels, values = labels[o], values[o]
    y = np.arange(len(values))
    for yi, l, v in zip(y, labels, values):
        c = highlight_color if (highlight is not None and l in np.atleast_1d(highlight)) else color
        ax.plot([baseline, v], [yi, yi], color=c, lw=mpl.rcParams["axes.linewidth"] * 1.2, zorder=2)
        ax.plot(v, yi, "o", ms=ms, color=c, mec="w", mew=0.5, zorder=3)
        if value_fmt:
            direct_label(ax, v, yi, value_fmt.format(v), color=c, dx=4)
    ax.set_yticks(y, labels)
    ax.tick_params(axis="y", which="both", left=False, right=False)
    return y


def dumbbell(ax, labels, a, b, colors=("#9A9A9A", "#E84143"), names=("before", "after"), ms=4.0, sort=True):
    """Paired change per category (before -> after, baseline -> ours)."""
    labels = np.asarray(labels); a = np.asarray(a, float); b = np.asarray(b, float)
    if sort:
        o = np.argsort(b - a)
        labels, a, b = labels[o], a[o], b[o]
    y = np.arange(len(a))
    ax.hlines(y, np.minimum(a, b), np.maximum(a, b), color="0.75", lw=mpl.rcParams["axes.linewidth"] * 2.2, zorder=1)
    h1 = ax.plot(a, y, "o", ms=ms, color=colors[0], mec="w", mew=0.5, label=names[0], zorder=2)[0]
    h2 = ax.plot(b, y, "o", ms=ms, color=colors[1], mec="w", mew=0.5, label=names[1], zorder=3)[0]
    ax.set_yticks(y, labels)
    ax.tick_params(axis="y", which="both", left=False, right=False)
    return h1, h2


def waterfall(ax, labels, deltas, start=None, start_label="Source", end_label="Total", gain_color="#39AF6B",
              loss_color="#E84143", total_color="#2C6AB4", width=0.62, fmt="{:+.1f}", connector=True, base=0.0):
    """Budget / waterfall chart (loss budget in dB, error budget, ablation contributions).
    start: level of the first bar (None -> start at 0, no first bar). Total bars rise from `base`
    (set it below the data, e.g. the axis floor, for log-unit budgets where 0 has no meaning)."""
    lw = mpl.rcParams["axes.linewidth"]
    segs, cols, lbls, txts = [], [], [], []
    level = 0.0 if start is None else start
    if start is not None:
        segs.append((base, start)); cols.append(total_color); lbls.append(start_label); txts.append(f"{start:.1f}")
    for l, d in zip(labels, deltas):
        segs.append((level, level + d)); cols.append(gain_color if d >= 0 else loss_color); lbls.append(l)
        txts.append(fmt.format(d)); level += d
    segs.append((base, level)); cols.append(total_color); lbls.append(end_label); txts.append(f"{level:.1f}")
    x = np.arange(len(segs))
    for xi, (a, b), c in zip(x, segs, cols):
        ax.bar(xi, b - a, bottom=a, width=width, color=c, edgecolor=darken(c, 0.25), lw=lw, zorder=2)
    if connector:
        for i in range(len(segs) - 1):
            yv = segs[i][1]
            ax.plot([x[i] + width / 2, x[i + 1] - width / 2], [yv, yv], color="0.5", lw=lw * 0.6,
                    ls=(0, (2, 1.5)), zorder=1)
    for xi, (a, b), t in zip(x, segs, txts):
        top = max(a, b)
        direct_label(ax, xi, top, t.replace("-", "\u2212"), dx=0, dy=1.5, ha="center", va="bottom")
    ax.set_xticks(x, lbls)
    ax.tick_params(axis="x", which="both", bottom=False, top=False)
    if base == 0:
        ax.axhline(0, color="k", lw=lw)
    return x


def forest(ax, labels, est, lo, hi, ref=0.0, colors=None, ms=4.0, marker="s", sizes=None, ref_label=None):
    """Forest plot: estimate +- interval per row, vertical reference line."""
    y = np.arange(len(est))[::-1]
    colors = colors or ["k"] * len(est)
    lw = mpl.rcParams["axes.linewidth"]
    for yi, e, l, h, c, k in zip(y, est, lo, hi, colors, range(len(est))):
        ax.plot([l, h], [yi, yi], color=c, lw=lw * 1.2, zorder=2)
        s = ms if sizes is None else sizes[k]
        ax.plot(e, yi, marker, ms=s, color=c, mec="w", mew=0.4, zorder=3)
    ax.axvline(ref, color="0.4", ls=(0, (3, 2)), lw=lw)
    if ref_label:
        ref_line(ax, ref, "x", None)
    ax.set_yticks(y, labels)
    ax.tick_params(axis="y", which="both", left=False, right=False)
    return y


def radar(ax, labels, series, colors=None, rmax=1.0, rticks=(0.25, 0.5, 0.75, 1.0), fill_alpha=0.15, lw=None):
    """Radar chart on a polar axes (create with subplot_kw={'projection': 'polar'}).
    series = {name: values in [0, rmax]}. Use only for 4-8 normalised metrics."""
    n = len(labels)
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
    ang_c = np.r_[ang, ang[0]]
    colors = colors or HOUSE_DARK
    lw = lw or mpl.rcParams["lines.linewidth"] * 0.8
    ax.set_theta_offset(np.pi / 2); ax.set_theta_direction(-1)
    ax.set_xticks(ang, labels)
    ax.set_ylim(0, rmax); ax.set_yticks(rticks)
    ax.set_yticklabels([f"{t:g}" for t in rticks], fontsize=_fs("tick") * 0.9, color="0.45")
    ax.grid(True, color="0.85", lw=0.5)
    ax.spines["polar"].set_linewidth(mpl.rcParams["axes.linewidth"])
    ax.tick_params(axis="x", pad=5)
    for (name, v), c in zip(series.items(), colors):
        vv = np.r_[v, v[0]]
        ax.plot(ang_c, vv, color=c, lw=lw, label=name)
        ax.fill(ang_c, vv, color=c, alpha=fill_alpha, lw=0)
    return ang


# =================================================================================================== matrices
def heatmap(ax, Z, xlabels=None, ylabels=None, cmap="ns_reds", norm=None, annotate=False, fmt="{:.2f}",
            grid_color="w", grid_lw=0.6, text_colors=("k", "w"), text_threshold=None, fontsize=None,
            x=None, y=None):
    """Cell heat map with white cell borders (pcolormesh), optional value text that flips colour on dark cells.
    Returns the QuadMesh (pass to a colour-bar helper)."""
    Z = np.asarray(Z, float)
    ny, nx = Z.shape
    xe = np.arange(nx + 1) - 0.5 if x is None else x
    ye = np.arange(ny + 1) - 0.5 if y is None else y
    m = ax.pcolormesh(xe, ye, Z, cmap=cmap, norm=norm, edgecolors=grid_color, linewidth=grid_lw, shading="flat")
    if xlabels is not None:
        ax.set_xticks(np.arange(nx), xlabels)
    if ylabels is not None:
        ax.set_yticks(np.arange(ny), ylabels)
    ax.tick_params(which="both", length=0)
    ax.minorticks_off()
    for s in ax.spines.values():
        s.set_visible(False)
    if annotate:
        cm_ = mpl.colormaps[cmap] if isinstance(cmap, str) else cmap
        nrm = m.norm
        for i in range(ny):
            for j in range(nx):
                v = Z[i, j]
                if not np.isfinite(v):
                    continue
                rgb = cm_(nrm(v))[:3]
                lum = np.dot(rgb, [0.299, 0.587, 0.114])
                dark = lum < (text_threshold if text_threshold is not None else 0.5)
                ax.text(j, i, fmt.format(v), ha="center", va="center", fontsize=fontsize or _fs() * 0.95,
                        color=text_colors[1] if dark else text_colors[0])
    ax.set_xlim(xe[0], xe[-1]); ax.set_ylim(ye[0], ye[-1])
    return m


def corr_triangle(ax, C, labels, cmap="ns_div_br", annotate=True, fmt="{:.2f}", vmin=-1, vmax=1):
    """Lower-triangle correlation matrix (diagonal and upper half hidden), centred diverging map."""
    C = np.array(C, float)
    n = C.shape[0]
    mask = np.triu(np.ones_like(C, bool), k=0)
    Cm = np.where(mask, np.nan, C)
    m = heatmap(ax, Cm[::-1], labels, labels[::-1], cmap=cmap, norm=mcolors.Normalize(vmin, vmax),
                annotate=annotate, fmt=fmt)
    ax.set_xlim(-0.5, n - 1.5)
    ax.set_ylim(-0.5, n - 1.5)
    ax.set_xticks(np.arange(n - 1), labels[:-1])
    ax.set_yticks(np.arange(n - 1), labels[::-1][:-1])
    return m


# =================================================================================================== relationships
def parity(ax, y_true, y_pred, color="#2C6AB4", tol=None, lims=None, density=False, s=6, stats=True, units="",
           alpha=0.6, cmap="ns_glacier", stats_loc="upper left"):
    """Predicted vs true with the identity line, optional +-tol band and MAE / RMSE / R^2 text."""
    t = np.asarray(y_true, float); p = np.asarray(y_pred, float)
    lo, hi = lims or (min(t.min(), p.min()), max(t.max(), p.max()))
    pad = 0.04 * (hi - lo)
    lo, hi = lo - pad, hi + pad
    lw = mpl.rcParams["axes.linewidth"]
    if tol:
        ax.fill_between([lo, hi], [lo - tol, hi - tol], [lo + tol, hi + tol], color="0.88", lw=0, zorder=0)
    ax.plot([lo, hi], [lo, hi], color="0.25", ls=(0, (3, 2)), lw=lw, zorder=1)
    if density:
        from scipy.stats import gaussian_kde
        z = gaussian_kde(np.vstack([t, p]))(np.vstack([t, p]))
        o = np.argsort(z)
        sc = ax.scatter(t[o], p[o], c=z[o], s=s, cmap=cmap, lw=0, zorder=2)
    else:
        sc = ax.scatter(t, p, s=s, color=mcolors.to_rgba(color, alpha), lw=0, zorder=2)
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi); ax.set_aspect("equal", adjustable="box")
    if stats:
        err = p - t
        mae = np.abs(err).mean(); rmse = np.sqrt((err ** 2).mean())
        r2 = 1 - (err ** 2).sum() / ((t - t.mean()) ** 2).sum()
        u = f" {units}" if units else ""
        stats_text(ax, [f"MAE {mae:.3g}{u}", f"RMSE {rmse:.3g}{u}", f"$R^2$ = {r2:.4f}", f"n = {t.size}"],
                   loc=stats_loc)
    return sc


def fit_line(ax, x, y, kind="linear", color="0.3", ci=0.95, ls=(0, (4, 2)), lw=None, n=200, xfit=None,
             label_fmt=None, label_pos=0.6, rotate_label=True, fontsize=None, label_offset=2.0):
    """Least-squares fit with a confidence band. kind: 'linear' (y = a + b x), 'power' (log y vs log x),
    'exp' (log y vs x). The equation label is written along the line when label_fmt is given
    (format keys: a, b). Returns (a, b)."""
    from scipy import stats
    x = np.asarray(x, float); y = np.asarray(y, float)
    X = np.log10(x) if kind == "power" else x
    Y = np.log10(y) if kind in ("power", "exp") else y
    res = stats.linregress(X, Y)
    xf = np.linspace(x.min(), x.max(), n) if xfit is None else np.asarray(xfit, float)
    Xf = np.log10(xf) if kind == "power" else xf
    Yf = res.intercept + res.slope * Xf
    # CI of the mean
    nobs = X.size
    tcrit = stats.t.ppf(0.5 + ci / 2, nobs - 2)
    resid = Y - (res.intercept + res.slope * X)
    s_err = np.sqrt((resid ** 2).sum() / (nobs - 2))
    se = s_err * np.sqrt(1 / nobs + (Xf - X.mean()) ** 2 / ((X - X.mean()) ** 2).sum())
    lo, hi = Yf - tcrit * se, Yf + tcrit * se
    tf = (lambda v: 10 ** v) if kind in ("power", "exp") else (lambda v: v)
    lw = lw or mpl.rcParams["lines.linewidth"] * 0.7
    ax.plot(xf, tf(Yf), color=color, ls=ls, lw=lw, zorder=2)
    if ci:
        ax.fill_between(xf, tf(lo), tf(hi), color=color, alpha=0.12, lw=0, zorder=1)
    if label_fmt:
        k = int(label_pos * (len(xf) - 1))
        x0, y0 = xf[k], tf(Yf[k])
        rot = 0
        if rotate_label:
            p1 = ax.transData.transform((xf[k], tf(Yf[k])))
            p2 = ax.transData.transform((xf[min(k + 5, len(xf) - 1)], tf(Yf[min(k + 5, len(xf) - 1)])))
            rot = np.degrees(np.arctan2(p2[1] - p1[1], p2[0] - p1[0]))
        ax.text(x0, y0, label_fmt.format(a=res.intercept, b=res.slope), rotation=rot, rotation_mode="anchor",
                ha="center", va="bottom", color=color, fontsize=fontsize or _fs(),
                transform=ax.transData + mtransforms.ScaledTranslation(0, pt(label_offset), ax.figure.dpi_scale_trans))
    return res.intercept, res.slope


def landscape(ax, entries, styles, this_work=None, label_key="ref", number_color="0.25", ms=4.5,
              target=None, target_color="0.93", legend_loc="upper left", legend_ncols=1):
    """Literature comparison ('where does this work sit'): one marker style per category, numbered references
    placed without overlap, shaded target region, highlighted 'this work'.
    entries: list of dicts {x, y, cat, ref}; styles: {cat: dict(marker=..., color=..., label=...)};
    this_work: dict(x, y, label, marker='*', color='#E84143'); target: (x0, x1, y0, y1) region to shade."""
    if target is not None:
        x0, x1, y0, y1 = target
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, color=target_color, lw=0, zorder=0))
    handles = {}
    for e in entries:
        st = styles[e["cat"]]
        h = ax.plot(e["x"], e["y"], st.get("marker", "o"), ms=st.get("ms", ms),
                    mfc=st.get("mfc", st["color"]), mec=st.get("mec", "k"), mew=0.5, zorder=3,
                    label=st.get("label", e["cat"]))[0]
        handles.setdefault(e["cat"], h)
    if this_work:
        h = ax.plot(this_work["x"], this_work["y"], this_work.get("marker", "*"), ms=this_work.get("ms", ms * 2),
                    mfc=this_work.get("color", "#E84143"), mec="k", mew=0.6, zorder=5,
                    label=this_work.get("label", "This work"))[0]
        handles["__this__"] = h
    texts = [str(e.get(label_key, "")) for e in entries]
    if any(texts):
        place_labels(ax, [e["x"] for e in entries], [e["y"] for e in entries], texts,
                     colors=[number_color] * len(entries))
    leg = ax.legend(handles=list(handles.values()), loc=legend_loc, ncols=legend_ncols, handletextpad=0.3,
                    borderaxespad=0.4, labelspacing=0.3)
    return leg


# =================================================================================================== export
def export(fig, name, outdir=None, exact=False, audit=True):
    """Save a finished figure.
    * normal use: PNG (600 dpi) + PDF via nature_style.save_fig (or save_fig_exact for full-page layouts);
    * gallery build (env NATURE_GALLERY=<dir>): one 200-dpi PNG preview into that folder.
    Prints any text outside 5-8 pt (Nature minimum 5 pt) when audit=True."""
    if audit:
        bad = audit_text(fig, show=False)
        if bad:
            print(f"[export] {name}: {len(bad)} text items outside 5-8 pt -> " +
                  ", ".join(f"{s:.1f} pt '{t[:18]}'" for s, t in bad[:6]))
    gal = os.environ.get("NATURE_GALLERY")
    if gal:
        Path(gal).mkdir(parents=True, exist_ok=True)
        if exact:
            with mpl.rc_context({"savefig.bbox": "standard"}):
                fig.savefig(Path(gal) / f"{name}.png", dpi=int(os.environ.get("NATURE_GALLERY_DPI", 200)))
        else:
            fig.savefig(Path(gal) / f"{name}.png", dpi=int(os.environ.get("NATURE_GALLERY_DPI", 200)),
                        bbox_inches="tight", pad_inches=0.02)
        plt.close(fig)
        return Path(gal) / f"{name}.png"
    outdir = Path(outdir or os.environ.get("NATURE_OUT", "figure_preview"))
    (save_fig_exact if exact else save_fig)(fig, name, outdir=outdir)
    return outdir / f"{name}.pdf"
