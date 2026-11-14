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
    matrices        heatmap, corr_triangle, dot_matrix
    relationships   parity, fit_line, landscape, binned_stat, highlight_points, volcano, zoom_to
    statistics      sig_bracket, p_to_stars, n_ticklabels, mean_sem, kaplan_meier, km_curve, at_risk_table,
                    hill, fit_hill
    editorial       butterfly, bracket_label, fan, legend_box, dashed_frame, arrow_note, size_legend,
                    square_legend, overlay_bars, area_stack, donut, waffle, zebra_table, beeswarm, paired_lines
    flows / graphs  alluvial, node_link
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

from nature_style import (PALETTE, CYCLE, THEMES, MM_PER_IN, SAVE_DPI, style_axes, save_fig, save_fig_exact,
                          audit_text, gradient_image, apply_backgrounds, _mix)
from nature_cmaps import lighten, darken, HOUSE, HOUSE_DARK

__all__ = [
    "direct_label", "end_label", "ref_line", "regime", "band", "double_arrow", "callout", "stats_text",
    "place_labels", "end_labels", "secondary_unit_axis", "broken_windows", "share_labels",
    "inset_zoom", "scale_bar", "despine_inner", "ci_band", "step_series", "boxplot", "jitter", "half_violin",
    "mean_sd", "hist_step", "kde_line", "ecdf", "ridgeline", "bars", "grouped_bars", "stacked_barh",
    "lollipop", "dumbbell", "waterfall", "forest", "radar", "heatmap", "corr_triangle", "parity",
    "fit_line", "landscape", "export", "pt",
    # editorial helpers
    "sig_bracket", "p_to_stars", "n_ticklabels", "butterfly", "bracket_label", "fan", "binned_stat",
    "legend_box", "dashed_frame", "arrow_note", "kaplan_meier", "km_curve", "at_risk_table", "volcano",
    "dot_matrix", "size_legend", "alluvial", "beeswarm_x", "beeswarm", "paired_lines", "donut", "waffle",
    "zebra_table", "zoom_to", "highlight_points", "node_link", "hill", "fit_hill", "mean_sem", "overlay_bars",
    "square_legend", "area_stack", "gradient_fill", "gradient_patch", "gradient_patches", "gbarh", "gradient_band",
    "cbar_box",
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


def regime(ax, x0, x1, color="0.5", gradient=True, fade="in", alpha=(0.0, 0.28), label=None,
           label_color=None, label_rot=90, label_x=None, zorder=0.5):
    """Shade an x-interval over the full height: a window, a 'below limit' or 'not accessible' zone.
    gradient=True (default) ramps the tint along x: fade='in' clear at x0 -> alpha[1] at x1, 'out' the reverse,
    'center' strongest in the middle, 'up' a vertical ramp (strongest at the bottom). gradient=False: flat band."""
    lo, hi = min(x0, x1), max(x0, x1)
    c0, c1 = mcolors.to_rgba(color, alpha[0]), mcolors.to_rgba(color, alpha[1])
    if gradient:
        if fade == "center":
            stops, d = [c0, c1, c0], "right"
        elif fade == "up":
            stops, d = [c1, c0], "up"
        else:
            stops, d = ([c0, c1] if (fade == "in") == (x1 >= x0) else [c1, c0]), "right"
        gradient_image(ax, (lo, hi, 0, 1), stops, direction=d, coords="x", zorder=zorder)
    else:
        ax.axvspan(x0, x1, color=color, alpha=alpha[1], lw=0, zorder=zorder)
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


def end_labels(ax, x, ys, texts, colors=None, dx=3.0, min_gap=7.0, fontsize=None, ha="left", **kw):
    """Labels at the right end of several lines (x, ys[i]) pushed apart vertically so that no two are closer than
    min_gap points (they may sit outside the axes, as in most Nature line charts). Returns the Text artists."""
    fig = ax.figure
    fig.canvas.draw()
    ys = np.asarray(ys, float)
    disp = ax.transData.transform(np.column_stack([np.full(ys.size, x), ys]))[:, 1]
    gap = min_gap * fig.dpi / 72
    order = np.argsort(disp)
    pos = disp[order].copy()
    for _ in range(50):                                   # relax: push neighbours apart symmetrically
        moved = False
        for i in range(1, pos.size):
            d = pos[i] - pos[i - 1]
            if d < gap:
                sh = (gap - d) / 2
                pos[i - 1] -= sh; pos[i] += sh; moved = True
        if not moved:
            break
    new = np.empty_like(pos); new[order] = pos
    inv = ax.transData.inverted()
    colors = colors or ["0.2"] * len(texts)
    out = []
    for yd, t, c in zip(new, texts, colors):
        yy = inv.transform((ax.transData.transform((x, 0))[0], yd))[1]
        out.append(ax.annotate(t, (x, yy), xytext=(dx, 0), textcoords="offset points", ha=ha, va="center",
                               color=c, fontsize=fontsize or _fs(), annotation_clip=False, **kw))
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
    up = bottom                     # label inside the image: above a bar at the bottom, below one at the top
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
    fill: 'gradient' (alpha ramp, default), 'solid' (light tint), or None. Returns list of y-offsets."""
    lw = lw or mpl.rcParams["lines.linewidth"] * 0.8
    offs = []
    n = len(ys)
    for i, (y, c) in enumerate(zip(ys, colors)):
        off = i * offset
        yy = np.asarray(y, float) * scale + off
        z = 10 + (n - i) * zorder_step  # lower curves in front
        if fill == "gradient":
            _ramp_fill(ax, x, yy, color=c, alpha=fill_alpha, ymin=off, zorder=z - 0.5)
        elif fill == "solid":
            ax.fill_between(x, off, yy, color=lighten(c, 1 - fill_alpha), lw=0, zorder=z - 0.5)
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
def bars(ax, x, heights, colors=None, err=None, width=0.62, alpha=1.0, edge="none", points=None, point_color="0.2",
         labels=None, label_fmt="{:.2g}", hatch=None, capsize=0.0, gradient=True, light=0.62):
    """Bars with optional error bars, overlaid individual points and value labels. gradient=True (default)
    fills each bar from a light tint at the base to its colour at the top; edge='auto' adds a darker outline."""
    colors = colors or [HOUSE[0]] * len(heights)
    lw = mpl.rcParams["axes.linewidth"]
    b = ax.bar(x, heights, width=width, color=[mcolors.to_rgba(c, alpha) for c in colors],
               edgecolor=[darken(c, 0.25) for c in colors] if edge == "auto" else edge,
               lw=lw if edge != "none" else 0, zorder=2, hatch=hatch)
    if gradient:
        for p, c, h in zip(b.patches, colors, heights):
            gradient_patch(ax, p, mcolors.to_rgba(c, alpha), light=light, direction="up" if h >= 0 else "down")
    if err is not None:
        ax.errorbar(x, heights, yerr=err, fmt="none", ecolor="0.15", elinewidth=lw, capsize=capsize,
                    capthick=lw, zorder=4)
    if points is not None:
        for xi, pts_ in zip(x, points):
            jitter(ax, xi, pts_, point_color, width=width * 0.22, size=4, alpha=0.55, zorder=5)
    if labels:
        for xi, h in zip(x, heights):
            direct_label(ax, xi, h, label_fmt.format(h), dx=0, dy=2, ha="center", va="bottom")
    return b


def gradient_patches(ax, patches, color, light=0.7, direction="up", zorder=None):
    """One shared gradient across many patches (histogram bars, a bar series): light tint at the bottom of the
    tallest patch -> *color* at its top, so heights read against a single colour scale."""
    from matplotlib.path import Path as _P
    from matplotlib.patches import PathPatch as _PP
    paths = [p.get_path().transformed(p.get_patch_transform()) for p in patches if p.get_height() != 0]
    if not paths:
        return None
    comp = _P.make_compound_path(*paths)
    clip = _PP(comp, facecolor="none", edgecolor="none", transform=ax.transData)
    ax.add_patch(clip)
    ext = comp.get_extents()
    z = patches[0].get_zorder() + 0.01 if zorder is None else zorder
    if ax.get_yscale() == "log":                 # log counts: start the ramp at the visible bottom
        lo_ = min(p.get_y() + p.get_height() for p in patches if p.get_height() > 0) * 0.5
        ylo = ax.get_ylim()[0]
        ext = mtransforms.Bbox.from_extents(ext.x0, max(ext.y0, ylo if ylo > 0 else lo_), ext.x1, ext.y1)
    return gradient_image(ax, (ext.x0, ext.x1, ext.y0, ext.y1), [_mix(color, light), mcolors.to_rgba(color)],
                          direction=direction, clip=clip, zorder=z)


def cbar_box(ax, mappable, label=None, loc="lower left", width_mm=22.0, bar_mm=1.6, ticks=None, extend=None,
             pad_mm=1.0, margin_mm=1.2, fc="white", alpha=0.88, fmt=None):
    """Horizontal colour bar on a small white card inside the panel (maps, spectrograms, dense scatters):
    the key never changes the frame size and stays readable over busy data. Sizes in mm.
    loc: 'lower left' | 'lower right' | 'upper left' | 'upper right'. Returns the Colorbar."""
    fig = ax.figure
    bb = ax.get_position()
    W, H = (v * MM_PER_IN for v in fig.get_size_inches())
    aw, ah = bb.width * W, bb.height * H
    fmm = mpl.rcParams["font.size"] / 72 * MM_PER_IN
    lab_h = fmm * 1.15 if label else 0.0
    tick_h = fmm * 1.15
    over = 2.2                                           # tick labels overhang the bar ends
    bw = width_mm + 2 * (pad_mm + over)
    bh = pad_mm + lab_h + 0.6 + bar_mm + 0.5 + tick_h + pad_mm
    x0 = margin_mm if "left" in loc else aw - margin_mm - bw
    y0 = margin_mm if "lower" in loc else ah - margin_mm - bh
    ax.add_patch(Rectangle((x0 / aw, y0 / ah), bw / aw, bh / ah, transform=ax.transAxes, facecolor=fc, alpha=alpha,
                           edgecolor="none", zorder=4.9))
    cax = ax.inset_axes([(x0 + pad_mm + over) / aw, (y0 + pad_mm + tick_h + 0.5) / ah, width_mm / aw, bar_mm / ah],
                        zorder=5)
    kw = dict(cax=cax, orientation="horizontal", ticks=ticks, format=fmt)
    if extend:
        kw["extend"] = extend
    cb = fig.colorbar(mappable, **kw)
    from nature_cmaps import style_cbar
    style_cbar(cb)
    cax.tick_params(pad=1.0)
    if label:
        cax.set_title(label, pad=1.2)
    return cb


def gbarh(ax, y, widths, colors, height=0.6, left=0.0, light=0.62, **kw):
    """Horizontal bars with a left-to-right gradient (light tint at the base -> colour at the end)."""
    widths = np.atleast_1d(widths); y = np.atleast_1d(y)
    colors = [colors] * len(widths) if isinstance(colors, str) or np.ndim(colors) == 1 and len(colors) in (3, 4) \
        and not isinstance(colors[0], str) else colors
    b = ax.barh(y, widths, left=left, height=height, color=colors, lw=0, **kw)
    for p, c, w in zip(b.patches, colors, widths):
        gradient_patch(ax, p, c, light=light, direction="right" if w >= 0 else "left")
    return b


def gradient_band(ax, y0, y1, color, alpha=(0.0, 0.3), direction="up", zorder=0.4):
    """Full-width horizontal band between y0 and y1 (data units) with a vertical gradient."""
    return gradient_image(ax, (0, 1, y0, y1), [mcolors.to_rgba(color, alpha[0]), mcolors.to_rgba(color, alpha[1])],
                          direction=direction, coords="y", zorder=zorder)


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


def lollipop(ax, labels, values, color="0.55", highlight=None, highlight_color="#3A6EA5", sort=True, ms=4.0,
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


def dumbbell(ax, labels, a, b, colors=("#B5B5B5", "#3A6EA5"), names=("before", "after"), ms=4.0, sort=True):
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


def waterfall(ax, labels, deltas, start=None, start_label="Source", end_label="Total", gain_color="#6E9A5E",
              loss_color="#B8503A", total_color="#3A6EA5", width=0.62, fmt="{:+.1f}", connector=True, base=0.0):
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
def parity(ax, y_true, y_pred, color="#3A6EA5", tol=None, lims=None, density=False, s=6, stats=True, units="",
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
    this_work: dict(x, y, label, marker='*', color='#3A6EA5'); target: (x0, x1, y0, y1) region to shade."""
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
                    mfc=this_work.get("color", "#3A6EA5"), mec="k", mew=0.6, zorder=5,
                    label=this_work.get("label", "This work"))[0]
        handles["__this__"] = h
    texts = [str(e.get(label_key, "")) for e in entries]
    if any(texts):
        place_labels(ax, [e["x"] for e in entries], [e["y"] for e in entries], texts,
                     colors=[number_color] * len(entries))
    leg = ax.legend(handles=list(handles.values()), loc=legend_loc, ncols=legend_ncols, handletextpad=0.3,
                    borderaxespad=0.4, labelspacing=0.3)
    return leg


# =================================================================================================== editorial helpers
# Patterns that recur across recent Nature-family figures: significance brackets and n under categories,
# mirrored (left/right) bar charts, scenario fans, binned trends, dashed legend boxes, survival curves,
# volcano and dot-matrix plots, flows between stages, swarms, part-of-whole charts and table figures.

def gradient_fill(ax, x, y, color, alpha=0.45, ymin=None, zorder=1, alpha_bottom=0.0):
    """Area under a curve filled with a vertical gradient: alpha at the curve's top fading to alpha_bottom at
    ymin (default: the current lower y limit). Does not change the data limits."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    ymin = ax.get_ylim()[0] if ymin is None else ymin
    clip = Polygon(np.column_stack([np.r_[x, x[::-1]], np.r_[y, np.full_like(y, ymin)]]), closed=True,
                   facecolor="none", edgecolor="none", transform=ax.transData)
    ax.add_patch(clip)
    return gradient_image(ax, (x.min(), x.max(), min(ymin, y.min()), y.max()),
                          [mcolors.to_rgba(color, alpha_bottom), mcolors.to_rgba(color, alpha)], direction="up",
                          clip=clip, zorder=zorder)


_ramp_fill = gradient_fill


def _log_safe(ax, x0, x1, y0, y1):
    """Bars on a log axis start at 0; move that edge to a small positive value so the gradient has an extent."""
    if ax.get_yscale() == "log" and y0 <= 0:
        y0 = (y1 if y1 > 0 else 1.0) * 1e-3
    if ax.get_xscale() == "log" and x0 <= 0:
        x0 = (x1 if x1 > 0 else 1.0) * 1e-3
    return x0, x1, y0, y1


def gradient_patch(ax, patch, color, light=0.6, direction="up", zorder=None):
    """Fill an existing patch (bar, wedge, box) with a gradient from a light tint (bottom / left) to *color*."""
    ext = patch.get_path().get_extents(patch.get_patch_transform())
    lo = _mix(color, light)
    return gradient_image(ax, _log_safe(ax, ext.x0, ext.x1, ext.y0, ext.y1), [lo, mcolors.to_rgba(color)],
                          direction=direction, clip=patch, zorder=(patch.get_zorder() + 0.01) if zorder is None else zorder)


def sig_bracket(ax, x0, x1, y, text="***", h=None, color="0.15", lw=None, fontsize=None, vertical=False,
                text_pad=1.0):
    """Significance bracket between two categories (x0, x1 at height y, data units) with stars or a P value.
    vertical=True draws it at x=y between heights x0 and x1 (for curves compared at the right edge)."""
    lw = lw or mpl.rcParams["axes.linewidth"]
    fs = fontsize or _fs()
    if not vertical:
        h = h if h is not None else 0.02 * np.ptp(ax.get_ylim())
        ax.plot([x0, x0, x1, x1], [y - h, y, y, y - h], color=color, lw=lw, solid_capstyle="butt",
                clip_on=False)
        tr = ax.transData + mtransforms.ScaledTranslation(0, pt(text_pad - (2.0 if "*" in text else 0)),
                                                          ax.figure.dpi_scale_trans)
        return ax.text((x0 + x1) / 2, y, text, ha="center", va="bottom", fontsize=fs, color=color,
                       transform=tr, clip_on=False)
    h = h if h is not None else 0.012 * np.ptp(ax.get_xlim())
    ax.plot([y - h, y, y, y - h], [x0, x0, x1, x1], color=color, lw=lw, solid_capstyle="butt", clip_on=False)
    tr = ax.transData + mtransforms.ScaledTranslation(pt(text_pad), 0, ax.figure.dpi_scale_trans)
    return ax.text(y, (x0 + x1) / 2, text, ha="left", va="center", rotation=90 if "*" in text else 0,
                   fontsize=fs, color=color, transform=tr, clip_on=False)


def p_to_stars(p):
    """P value -> '***' (< 0.001), '**' (< 0.01), '*' (< 0.05) or 'NS'."""
    return "***" if p < 1e-3 else "**" if p < 1e-2 else "*" if p < 0.05 else "NS"


def n_ticklabels(ax, labels, ns, axis="x", fmt="n = {:,}"):
    """Category tick labels with the sample size on a second line ('Group A\\nn = 428')."""
    lab = [f"{l}\n{fmt.format(n)}" for l, n in zip(labels, ns)]
    if axis == "x":
        ax.set_xticklabels(lab)
    else:
        ax.set_yticklabels(lab)
    return lab


def butterfly(ax, labels, left, right, colors=None, gap=0.22, height=0.62, fmt="{:,}", separators=(),
              sep_style=(0, (4, 3)), label_color="0.15", xmax=None, fontsize=None, headers=("Left", "Right"),
              header_y=None, log=False):
    """Mirrored horizontal bars: one category per row, labels in the centre column, left values growing to the
    left and right values to the right, counts written at the bar ends. Draws into a single axes whose x runs
    from -1 to 1 (bars are scaled to xmax, linear or log). separators: row indices *below* which a dashed rule
    is drawn (group breaks). Returns the y positions (top row = 0)."""
    n = len(labels)
    y = np.arange(n)
    left = np.asarray(left, float); right = np.asarray(right, float)
    xmax = xmax or max(left.max(), right.max())
    fs = fontsize or _fs()
    if colors is None:
        colors = ["0.15"] * n
    elif isinstance(colors, str) or (len(colors) in (3, 4) and not isinstance(colors[0], (str, tuple, list))):
        colors = [colors] * n

    span = (1 - gap) * 0.72                               # leave room for the count labels

    def scale(v):
        if log:
            return span * np.log10(1 + v) / np.log10(1 + xmax)
        return span * v / xmax
    for yi, l, r, c in zip(y, left, right, colors):
        wl, wr = scale(l), scale(r)
        bl = ax.barh(yi, -wl, left=-gap, height=height, color=c, lw=0)
        br = ax.barh(yi, wr, left=gap, height=height, color=c, lw=0)
        if wl > 0:
            gradient_patch(ax, bl.patches[0], c, light=0.6, direction="left")
        if wr > 0:
            gradient_patch(ax, br.patches[0], c, light=0.6, direction="right")
        ax.text(-gap - wl - 0.015, yi, fmt.format(int(l)), ha="right", va="center", fontsize=fs, color="0.1")
        ax.text(gap + wr + 0.015, yi, fmt.format(int(r)), ha="left", va="center", fontsize=fs, color="0.1")
    for yi, lab in zip(y, labels):
        ax.text(0, yi, lab, ha="center", va="center", fontsize=fs, color=label_color)
    for s in separators:
        ax.axhline(s + 0.5, color="0.25", lw=mpl.rcParams["axes.linewidth"], ls=sep_style)
    if headers:
        hy = header_y if header_y is not None else -0.9
        ax.text(-gap - 0.02, hy, headers[0], ha="right", va="bottom", fontsize=fs)
        ax.text(gap + 0.02, hy, headers[1], ha="left", va="bottom", fontsize=fs)
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(n - 0.5, -1.0)
    ax.axis("off")
    return y


def bracket_label(ax, y0, y1, text, x=1.02, w=0.015, color="0.15", fontsize=None, side="right",
                  transform="axes_x"):
    """Square bracket spanning rows y0..y1 (data units) at axes-fraction x, with a label beside it:
    groups rows of a table-like chart ('Afferent', 'Intrinsic' ...)."""
    fs = fontsize or _fs()
    tr = mtransforms.blended_transform_factory(ax.transAxes, ax.transData)
    sgn = 1 if side == "right" else -1
    xs = [x, x + sgn * w, x + sgn * w, x]
    ax.plot(xs, [y0, y0, y1, y1], color=color, lw=mpl.rcParams["axes.linewidth"], transform=tr, clip_on=False)
    ax.plot([x + sgn * w, x + sgn * 2 * w], [(y0 + y1) / 2] * 2, color=color,
            lw=mpl.rcParams["axes.linewidth"], transform=tr, clip_on=False)
    ax.text(x + sgn * 2.6 * w, (y0 + y1) / 2, text, transform=tr, ha="left" if side == "right" else "right",
            va="center", fontsize=fs, color=color, clip_on=False)


def fan(ax, x, center, bands, color, alphas=None, lw=None, label=None, zorder=2, ls="-"):
    """Scenario fan: central line plus nested percentile bands. bands = [(lo, hi), ...] from the narrowest
    (e.g. 17-83 %) to the widest (e.g. 5-95 %); each wider band is lighter."""
    alphas = alphas or [0.32, 0.16, 0.08][:len(bands)]
    for (lo, hi), a in zip(bands, alphas):
        ax.fill_between(x, lo, hi, color=color, alpha=a, lw=0, zorder=zorder - 0.5)
    return ax.plot(x, center, color=color, lw=lw or mpl.rcParams["lines.linewidth"], label=label,
                   zorder=zorder, ls=ls)[0]


def binned_stat(ax, x, y, bins, color="k", err="sem", ms=None, marker="o", line=False, label=None,
                min_count=3, capsize=0, zorder=3, **kw):
    """Mean of y in bins of x with s.e.m. (err='sem'), s.d. ('sd') or 95 % CI ('ci') bars: a readable summary
    of a dense cloud. Returns (centres, means, errors, counts)."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    idx = np.digitize(x, bins) - 1
    c, m, e, n = [], [], [], []
    for i in range(len(bins) - 1):
        v = y[idx == i]
        if v.size < min_count:
            continue
        c.append(0.5 * (bins[i] + bins[i + 1])); m.append(v.mean()); n.append(v.size)
        sd = v.std(ddof=1)
        e.append(sd if err == "sd" else sd / np.sqrt(v.size) * (1.96 if err == "ci" else 1.0))
    c, m, e, n = map(np.asarray, (c, m, e, n))
    ax.errorbar(c, m, yerr=e, fmt=marker + ("-" if line else ""), color=color, ms=ms or mpl.rcParams["lines.markersize"],
                elinewidth=mpl.rcParams["axes.linewidth"], capsize=capsize, label=label, zorder=zorder,
                lw=mpl.rcParams["lines.linewidth"] * 0.8, **kw)
    return c, m, e, n


def legend_box(ax, *args, ls=(0, (3, 2)), edgecolor="0.35", lw=None, pad=0.5, **kw):
    """Legend inside a dashed rectangle (the 'key box' used for experiment-vs-model plots)."""
    kw.setdefault("frameon", True)
    kw.setdefault("borderpad", pad)
    kw.setdefault("fancybox", False)
    leg = ax.legend(*args, **kw)
    fr = leg.get_frame()
    fr.set_edgecolor(edgecolor); fr.set_linestyle(ls); fr.set_linewidth(lw or mpl.rcParams["axes.linewidth"])
    fr.set_facecolor("white"); fr.set_alpha(1.0)
    return leg


def dashed_frame(ax, x0, y0, x1, y1, color="0.35", ls=(0, (3, 2)), lw=None, transform=None, zorder=5, fill="white"):
    """Dashed rectangle (axes fraction by default) to box an inset, a key or a group of items."""
    tr = transform or ax.transAxes
    r = Rectangle((x0, y0), x1 - x0, y1 - y0, transform=tr, fill=fill is not None, facecolor=fill or "none",
                  edgecolor=color, ls=ls, lw=lw or mpl.rcParams["axes.linewidth"], zorder=zorder, clip_on=False)
    ax.add_patch(r)
    return r


def arrow_note(ax, x, y_from, y_to, text, color="0.2", fontsize=None, lw=None, va="bottom", text_pad=1.0):
    """Vertical arrow from y_from down (or up) to y_to at x with a label above its tail (cost / time notes on
    a curve). Works on log axes (positions in data units)."""
    lw = lw or mpl.rcParams["axes.linewidth"]
    ax.annotate("", xy=(x, y_to), xytext=(x, y_from),
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=color, mutation_scale=5, shrinkA=0, shrinkB=1))
    tr = ax.transData + mtransforms.ScaledTranslation(0, pt(text_pad), ax.figure.dpi_scale_trans)
    return ax.text(x, y_from, text, ha="center", va=va, fontsize=fontsize or _fs(), color=color, transform=tr)


def kaplan_meier(t, event):
    """Kaplan-Meier estimate. t: times, event: 1 = event, 0 = censored.
    Returns (times, survival, lower95, upper95, censor_times, censor_surv) with Greenwood log-log CI."""
    t = np.asarray(t, float); e = np.asarray(event, int)
    order = np.argsort(t); t, e = t[order], e[order]
    uniq = np.unique(t[e == 1])
    s, var_acc, ts, ss, lo, hi = 1.0, 0.0, [0.0], [1.0], [1.0], [1.0]
    for u in uniq:
        n_at = np.sum(t >= u); d = np.sum((t == u) & (e == 1))
        s *= 1 - d / n_at
        if n_at > d:
            var_acc += d / (n_at * (n_at - d))
        ts.append(u); ss.append(s)
        if 0 < s < 1:
            se = np.sqrt(var_acc) / abs(np.log(s))
            lo.append(s ** np.exp(1.96 * se)); hi.append(s ** np.exp(-1.96 * se))
        else:
            lo.append(s); hi.append(s)
    ts, ss = np.array(ts), np.array(ss)
    ct = t[e == 0]
    cs = np.array([ss[np.searchsorted(ts, c, side="right") - 1] for c in ct])
    return ts, ss, np.array(lo), np.array(hi), ct, cs


def km_curve(ax, t, event, color, label=None, ci=True, censor=True, lw=None, ci_alpha=0.15, tick_h=0.018):
    """Kaplan-Meier survival step curve with log-log 95 % CI band and '|' ticks at censoring times."""
    ts, ss, lo, hi, ct, cs = kaplan_meier(t, event)
    tmax = np.max(t)
    ts_ = np.r_[ts, tmax]; ss_ = np.r_[ss, ss[-1]]
    ln = ax.step(ts_, ss_, where="post", color=color, lw=lw or mpl.rcParams["lines.linewidth"], label=label,
                 zorder=3)[0]
    if ci:
        ax.fill_between(np.r_[ts, tmax], np.r_[lo, lo[-1]], np.r_[hi, hi[-1]], step="post", color=color,
                        alpha=ci_alpha, lw=0, zorder=1)
    if censor and ct.size:
        ax.vlines(ct, cs - tick_h, cs + tick_h, color=color, lw=mpl.rcParams["axes.linewidth"], zorder=4)
    return ln


def at_risk_table(ax, groups, times, labels, colors, row_h=0.11, y0=-0.30, title="No. at risk", fontsize=None):
    """Numbers at risk under a survival plot (placed in axes-fraction rows below the x axis).
    groups = [(t, event), ...] in the same order as labels/colors; times = x positions of the columns."""
    fs = fontsize or _fs()
    tr = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
    tl = mtransforms.blended_transform_factory(ax.transAxes, ax.transAxes)
    ax.text(-0.09, y0 + row_h * 0.9, title, transform=tl, ha="right", va="center", fontsize=fs, color="0.2")
    for i, ((t, _), lab, c) in enumerate(zip(groups, labels, colors)):
        yy = y0 - i * row_h
        ax.text(-0.09, yy, lab, transform=tl, ha="right", va="center", fontsize=fs, color=c)
        t = np.asarray(t, float)
        for x in times:
            ax.text(x, yy, f"{int(np.sum(t >= x)):,}", transform=tr, ha="center", va="center", fontsize=fs,
                    color="0.1")


def volcano(ax, effect, pval, effect_thr=1.0, p_thr=0.05, colors=None, s=4, names=None, label_top=0,
            label_fontsize=None, alpha=0.85, thr_style=(0, (3, 2))):
    """Volcano plot: effect size vs -log10 P. Points beyond both thresholds coloured up/down, the rest grey;
    dashed threshold lines; the label_top most significant hits labelled from *names*.
    Returns boolean masks (up, down)."""
    colors = colors or ["#B8503A", "#3A6EA5", "#C8C8C8"]
    e = np.asarray(effect, float); q = -np.log10(np.asarray(pval, float))
    up = (e >= effect_thr) & (q >= -np.log10(p_thr))
    dn = (e <= -effect_thr) & (q >= -np.log10(p_thr))
    ns = ~(up | dn)
    ax.scatter(e[ns], q[ns], s=s, color=colors[2], lw=0, zorder=1, rasterized=True)
    ax.scatter(e[up], q[up], s=s * 1.3, color=colors[0], lw=0, alpha=alpha, zorder=2)
    ax.scatter(e[dn], q[dn], s=s * 1.3, color=colors[1], lw=0, alpha=alpha, zorder=2)
    lw = mpl.rcParams["axes.linewidth"]
    for v in (-effect_thr, effect_thr):
        ax.axvline(v, color="0.45", ls=thr_style, lw=lw, zorder=0)
    ax.axhline(-np.log10(p_thr), color="0.45", ls=thr_style, lw=lw, zorder=0)
    if label_top and names is not None:
        sig = np.where(up | dn)[0]
        top = sig[np.argsort(-(q[sig] * np.abs(e[sig])))][:label_top]
        place_labels(ax, e[top], q[top], [names[i] for i in top], fontsize=label_fontsize,
                     colors=[colors[0] if e[i] > 0 else colors[1] for i in top])
    return up, dn


def dot_matrix(ax, frac, value, xlabels, ylabels, cmap="ns_purples", smax=38.0, vmin=None, vmax=None,
               rotate=90, edge="0.35", min_frac=0.0):
    """Dot plot matrix: dot area = fraction (0-1), dot colour = value. frac/value shape (n_rows, n_cols).
    Rows read top to bottom in ylabels order. Returns the PathCollection (pass to a colour bar)."""
    frac = np.asarray(frac, float); value = np.asarray(value, float)
    nr, nc = frac.shape
    X, Y = np.meshgrid(np.arange(nc), np.arange(nr))
    m = frac.ravel() > min_frac
    sc = ax.scatter(X.ravel()[m], Y.ravel()[m], s=smax * frac.ravel()[m], c=value.ravel()[m], cmap=cmap,
                    vmin=vmin, vmax=vmax, edgecolors=edge, linewidths=0.3, zorder=3)
    ax.set_xticks(np.arange(nc), xlabels, rotation=rotate, ha="center" if rotate in (0, 90) else "right")
    ax.set_yticks(np.arange(nr), ylabels)
    ax.set_xlim(-0.6, nc - 0.4); ax.set_ylim(nr - 0.4, -0.6)
    ax.tick_params(length=0)
    return sc


def size_legend(ax, values, sizes, title=None, color="0.55", edge="0.35", loc="upper left", bbox=None,
                fmt="{:g}", ncols=1, **kw):
    """Legend for marker area (scatter s=) -- one entry per value."""
    hs = [ax.scatter([], [], s=s, color=color, edgecolors=edge, linewidths=0.3) for s in sizes]
    kw.setdefault("handletextpad", 0.2)
    kw.setdefault("labelspacing", 0.6)
    kw.setdefault("borderpad", 0.2)
    leg = ax.legend(hs, [fmt.format(v) for v in values], title=title, loc=loc, bbox_to_anchor=bbox, ncols=ncols,
                    title_fontsize=_fs(), **kw)
    leg._legend_box.align = "left"
    return leg


def _band_path(x0, x1, y0a, y0b, y1a, y1b, curv=0.5):
    """Closed path of a flow ribbon from [y0a, y0b] at x0 to [y1a, y1b] at x1 (cubic Bezier edges)."""
    from matplotlib.path import Path as MPath
    dx = (x1 - x0) * curv
    verts = [(x0, y0a), (x0 + dx, y0a), (x1 - dx, y1a), (x1, y1a), (x1, y1b),
             (x1 - dx, y1b), (x0 + dx, y0b), (x0, y0b), (x0, y0a)]
    codes = [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4, MPath.LINETO,
             MPath.CURVE4, MPath.CURVE4, MPath.CURVE4, MPath.CLOSEPOLY]
    return MPath(verts, codes)


def alluvial(ax, stages, flows, colors, node_w=0.05, gap=0.03, flow_alpha=0.38, color_by="source",
             label_fmt="{name}", fontsize=None, stage_titles=None):
    """Alluvial (Sankey-like) diagram between consecutive stages.
    stages: [[names of stage 0], [names of stage 1], ...]; flows: list of 2-D arrays, flows[k][i, j] = amount
    from item i of stage k to item j of stage k+1; colors: {name: colour} for every item.
    Nodes are bars whose heights are proportional to their totals (one scale for all stages); ribbons keep the
    source (color_by='source') or target colour. label_fmt may use {name} and {value}."""
    from matplotlib.patches import PathPatch
    fs = fontsize or _fs()
    flows = [np.asarray(f, float) for f in flows]
    ns = len(stages)
    xs = np.linspace(0, 1, ns)
    totals = [flows[k].sum(axis=1) if k < ns - 1 else flows[k - 1].sum(axis=0) for k in range(ns)]
    nmax = max(len(n) for n in stages)
    scale = (1 - gap * (nmax - 1)) / max(t.sum() for t in totals)
    nodes = []
    for k, names in enumerate(stages):
        used = totals[k].sum() * scale + gap * (len(names) - 1)
        y = 1 - (1 - used) / 2
        pos = []
        for i, nm in enumerate(names):
            h = totals[k][i] * scale
            pos.append((y - h, y))
            ax.add_patch(Rectangle((xs[k] - node_w / 2, y - h), node_w, h, color=colors[nm], lw=0, zorder=3))
            txt = label_fmt.format(name=nm, value=totals[k][i])
            if k == 0:
                ax.text(xs[k] - node_w / 2 - 0.012, y - h / 2, txt, ha="right", va="center", fontsize=fs)
            elif k == ns - 1:
                ax.text(xs[k] + node_w / 2 + 0.012, y - h / 2, txt, ha="left", va="center", fontsize=fs)
            else:
                ax.text(xs[k] + node_w / 2 + 0.008, y - h / 2, txt, ha="left", va="center", fontsize=fs,
                        bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none", alpha=0.7), zorder=4)
            y -= h + gap
        nodes.append(pos)
    for k in range(ns - 1):
        F = flows[k]
        out_c = [p[1] for p in nodes[k]]
        in_c = [p[1] for p in nodes[k + 1]]
        for i in range(F.shape[0]):
            for j in range(F.shape[1]):
                if F[i, j] <= 0:
                    continue
                h = F[i, j] * scale
                path = _band_path(xs[k] + node_w / 2, xs[k + 1] - node_w / 2, out_c[i], out_c[i] - h,
                                  in_c[j], in_c[j] - h)
                c = colors[stages[k][i]] if color_by == "source" else colors[stages[k + 1][j]]
                ax.add_patch(PathPatch(path, facecolor=c, alpha=flow_alpha, lw=0, zorder=2))
                out_c[i] -= h; in_c[j] -= h
    if stage_titles:
        for x, t in zip(xs, stage_titles):
            ax.text(x, 1.03, t, ha="center", va="bottom", fontsize=mpl.rcParams["axes.labelsize"])
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.08)
    ax.axis("off")
    return nodes


def beeswarm_x(values, x=0.0, width=0.35, size_pt=3.0, ax=None, nbins=None):
    """x positions of a simple beeswarm: points binned along y, each bin spread symmetrically around x and
    squeezed to *width*. Returns an array of x."""
    v = np.asarray(values, float)
    nb = nbins or max(8, int(np.sqrt(v.size) * 2.2))
    edges = np.linspace(v.min(), v.max() + 1e-12, nb + 1)
    idx = np.clip(np.digitize(v, edges) - 1, 0, nb - 1)
    xs = np.zeros_like(v)
    counts = np.bincount(idx, minlength=nb)
    step = width / max(1, counts.max() / 2)
    for b in range(nb):
        ii = np.where(idx == b)[0]
        ii = ii[np.argsort(v[ii])]
        k = np.arange(ii.size)
        off = ((k + 1) // 2) * np.where(k % 2 == 0, 1, -1) * step
        if ii.size % 2 == 0:
            off = off + step / 2
        xs[ii] = x + np.clip(off, -width, width)
    return xs


def beeswarm(ax, x, values, color, width=0.32, s=6, alpha=0.9, edge=None, zorder=3, **kw):
    """Beeswarm (non-overlapping strip): every observation visible, the distribution shape kept."""
    xs = beeswarm_x(values, x, width)
    return ax.scatter(xs, values, s=s, color=color, alpha=alpha, edgecolors=edge or "none",
                      linewidths=0.3 if edge else 0, zorder=zorder, **kw)


def paired_lines(ax, x0, x1, a, b, color="0.65", lw=0.5, alpha=0.7, ms=0, zorder=1):
    """Thin lines joining paired observations (same subject before / after)."""
    for ai, bi in zip(a, b):
        ax.plot([x0, x1], [ai, bi], color=color, lw=lw, alpha=alpha, zorder=zorder, marker="o" if ms else None,
                ms=ms)


def donut(ax, values, colors, labels=None, width=0.34, start=90, center_text=None, label_pct=True,
          pct_min=4.0, fontsize=None, counterclock=False, label_dist=1.16):
    """Donut chart (part of a whole, <= 6 parts). Labels outside with percentages; optional centre text."""
    fs = fontsize or _fs()
    v = np.asarray(values, float)
    wedges, _ = ax.pie(v, colors=colors, startangle=start, counterclock=counterclock,
                       wedgeprops=dict(width=width, edgecolor="white", linewidth=0.8))
    tot = v.sum()
    for w, val, lab in zip(wedges, v, labels or [None] * len(v)):
        ang = np.deg2rad((w.theta1 + w.theta2) / 2)
        pct = 100 * val / tot
        if lab is None and not label_pct:
            continue
        txt = (lab + ("\n" if lab else "") if lab else "") + (f"{pct:.0f}%" if label_pct and pct >= pct_min else "")
        ax.text(label_dist * np.cos(ang), label_dist * np.sin(ang), txt, ha="center", va="center", fontsize=fs)
    if center_text:
        ax.text(0, 0, center_text, ha="center", va="center", fontsize=mpl.rcParams["axes.labelsize"])
    ax.set_aspect("equal"); ax.axis("off")
    return wedges


def waffle(ax, counts, colors, ncols=10, nrows=10, gap=0.12, labels=None, legend=True):
    """Waffle chart: ncols x nrows squares filled in order of *counts* (counts should sum to ncols*nrows)."""
    cells = []
    for i, c in enumerate(counts):
        cells += [i] * int(c)
    cells += [-1] * (ncols * nrows - len(cells))
    for k, ci in enumerate(cells[:ncols * nrows]):
        r, cc = divmod(k, ncols)
        ax.add_patch(Rectangle((cc, nrows - 1 - r), 1 - gap, 1 - gap,
                               color=colors[ci] if ci >= 0 else "0.92", lw=0))
    ax.set_xlim(-0.2, ncols); ax.set_ylim(-0.2, nrows); ax.set_aspect("equal"); ax.axis("off")
    if legend and labels:
        hs = [Rectangle((0, 0), 1, 1, color=c) for c in colors[:len(labels)]]
        ax.legend(hs, labels, loc="upper left", bbox_to_anchor=(1.0, 1.0), handlelength=0.8, handleheight=0.8)


def zebra_table(ax, cells, col_labels, col_x, col_ha=None, stripe="0.93", row_h=1.0, header_lines=True,
                colors=None, fontsize=None, group_breaks=(), bold_header=False):
    """Table figure: text cells on alternating light stripes, header row with rules, optional double rule at
    group breaks (row indices below which a break is drawn). cells[r][c] strings; colors[r][c] text colours.
    col_x: x centre (or left edge) of each column in axes fraction. Returns the axes."""
    fs = fontsize or _fs("label")
    nr = len(cells)
    col_ha = col_ha or ["center"] * len(col_labels)
    ax.set_xlim(0, 1); ax.set_ylim(nr + 0.2, -2.3)
    for r in range(nr):
        if r % 2 == 1:
            ax.add_patch(Rectangle((0, r - 0.5), 1, row_h, color=stripe, lw=0, zorder=0))
        for c, txt in enumerate(cells[r]):
            ax.text(col_x[c], r, txt, ha=col_ha[c], va="center", fontsize=fs,
                    color=(colors[r][c] if colors else "0.1"), zorder=2)
    for c, lab in enumerate(col_labels):
        ax.text(col_x[c], -1.25, lab, ha=col_ha[c], va="center", fontsize=fs, zorder=2,
                fontweight="bold" if bold_header else "normal", linespacing=1.1)
    lw = mpl.rcParams["axes.linewidth"]
    if header_lines:
        ax.axhline(-2.2, color="0.1", lw=lw); ax.axhline(-0.5, color="0.1", lw=lw * 0.8)
        ax.axhline(nr - 0.5, color="0.1", lw=lw)
    for g in group_breaks:
        ax.axhline(g + 0.5 - 0.06, color="0.1", lw=lw * 0.6); ax.axhline(g + 0.5 + 0.06, color="0.1", lw=lw * 0.6)
    ax.axis("off")
    return ax


def zoom_to(ax, ax_zoom, xlim, ylim, color="0.1", lw=None, corners=("upper", "lower")):
    """Mark a region of *ax* with a rectangle and connect two of its corners to *ax_zoom* (which shows the same
    data at xlim/ylim): the 'magnified region' layout with the enlarged panel beside the main one."""
    from matplotlib.patches import ConnectionPatch
    lw = lw or mpl.rcParams["axes.linewidth"]
    ax.add_patch(Rectangle((xlim[0], ylim[0]), xlim[1] - xlim[0], ylim[1] - ylim[0], fill=False,
                           edgecolor=color, lw=lw, zorder=6))
    ax_zoom.set_xlim(xlim); ax_zoom.set_ylim(ylim)
    for sp in ax_zoom.spines.values():
        sp.set_visible(True); sp.set_linewidth(lw); sp.set_edgecolor(color)
    for (xa, ya), (xb, yb) in (((xlim[0], ylim[1]), (0, 1)), ((xlim[0], ylim[0]), (0, 0))):
        con = ConnectionPatch(xyA=(xa, ya), coordsA=ax.transData, xyB=(xb, yb), coordsB=ax_zoom.transAxes,
                              color=color, lw=lw * 0.8)
        ax.figure.add_artist(con)
    return ax_zoom


def highlight_points(ax, x, y, mask, labels=None, base_color="#B8503A", hl_color=None, s=10, hl_s=26,
                     edge="0.05", fontsize=None, offsets=None):
    """Scatter where a subset is emphasised by a larger, black-edged marker and labelled (all others plain)."""
    x = np.asarray(x, float); y = np.asarray(y, float); mask = np.asarray(mask, bool)
    ax.scatter(x[~mask], y[~mask], s=s, color=base_color, lw=0, zorder=2)
    ax.scatter(x[mask], y[mask], s=hl_s, color=hl_color or base_color, edgecolors=edge, linewidths=0.8, zorder=3)
    if labels is not None:
        place_labels(ax, x[mask], y[mask], labels, fontsize=fontsize, offsets=offsets)


def node_link(ax, pos, sizes, edges, edge_w, node_colors, size_scale=1.0, edge_color="0.25", curved=0.0,
              labels=None, label_offset=(0, 0), fontsize=None, edge_alpha=0.9, wmax=2.2):
    """Node-link diagram. pos {node: (x, y)}, sizes {node: value} -> marker area, edges [(a, b)],
    edge_w [weights] -> line width (scaled to wmax pt). Draw order: edges, then nodes."""
    from matplotlib.patches import FancyArrowPatch as FAP
    w = np.asarray(edge_w, float)
    lw = 0.3 + (wmax - 0.3) * (w - w.min()) / max(1e-12, np.ptp(w))
    for (a, b), l in zip(edges, lw):
        p = FAP(pos[a], pos[b], connectionstyle=f"arc3,rad={curved}", arrowstyle="-", lw=l, color=edge_color,
                alpha=edge_alpha, zorder=1, shrinkA=0, shrinkB=0)
        ax.add_patch(p)
    for nd, (x, y) in pos.items():
        ax.scatter([x], [y], s=sizes[nd] * size_scale, color=node_colors[nd], edgecolors="white", linewidths=0.5,
                   zorder=3)
        if labels and nd in labels:
            ax.annotate(labels[nd], (x, y), xytext=label_offset, textcoords="offset points", ha="center",
                        va="center", fontsize=fontsize or _fs(), zorder=4)
    ax.set_aspect("equal"); ax.axis("off")


def hill(x, bottom, top, ec50, n):
    """Four-parameter logistic (Hill) dose-response curve."""
    return bottom + (top - bottom) / (1 + (ec50 / np.asarray(x, float)) ** n)


def fit_hill(x, y, p0=None):
    """Least-squares fit of hill() (scipy). Returns (bottom, top, ec50, n)."""
    from scipy.optimize import curve_fit
    x = np.asarray(x, float); y = np.asarray(y, float)
    p0 = p0 or [y.min(), y.max(), np.exp(np.mean(np.log(x))), 1.0]
    p, _ = curve_fit(hill, x, y, p0=p0, maxfev=20000)
    return p


def mean_sem(ax, x, data, color, marker="o", ms=None, label=None, lw=None, line=True, capsize=0, mfc=None,
             zorder=3, **kw):
    """Mean +- s.e.m. per x for repeated measurements data[i] (list of replicate arrays)."""
    m = np.array([np.mean(d) for d in data]); e = np.array([np.std(d, ddof=1) / np.sqrt(len(d)) for d in data])
    ax.errorbar(x, m, yerr=e, fmt=marker + ("-" if line else ""), color=color, ms=ms or mpl.rcParams["lines.markersize"],
                lw=lw or mpl.rcParams["lines.linewidth"], elinewidth=mpl.rcParams["axes.linewidth"], capsize=capsize,
                mfc=mfc or color, label=label, zorder=zorder, **kw)
    return m, e


def overlay_bars(ax, x, front, back, colors, labels=None, width=0.8, log=False):
    """Two bar series drawn on top of each other at the same x (back = total, front = subset), e.g. a reference
    set inside a larger new set. Works on a log axis (bars start at the axis bottom)."""
    b0 = ax.bar(x, back, width=width, color=colors[0], lw=0, zorder=2, label=labels[0] if labels else None)
    b1 = ax.bar(x, front, width=width, color=colors[1], zorder=3, label=labels[1] if labels else None,
                edgecolor="white", linewidth=0.6)
    if log:
        ax.set_yscale("log")
    for bb, c in ((b0, colors[0]), (b1, colors[1])):
        for p in bb.patches:
            if p.get_height() > 0:
                gradient_patch(ax, p, c, light=0.35)
    if log:
        ax.set_yscale("log")
    return b0, b1


def square_legend(ax, labels, colors, loc="upper left", bbox=None, ncols=1, size=0.8, **kw):
    """Legend with small square colour patches (the usual key for bars and areas)."""
    hs = [Rectangle((0, 0), 1, 1, color=c, lw=0) for c in colors]
    return ax.legend(hs, labels, loc=loc, bbox_to_anchor=bbox, ncols=ncols, handlelength=size, handleheight=size,
                     **kw)


def area_stack(ax, x, ys, colors, labels=None, alpha=1.0, edge="white", lw=0.4, direct=True, fontsize=None,
               label_x=None, gradient=True, light=0.45):
    """Stacked areas (composition over time) with thin white separators and optional direct labels placed in
    the middle of each layer at label_x (default: 85 % along x). gradient=True shades every layer from a light
    tint (bottom of the plot) to its colour (top)."""
    ys = np.asarray(ys, float)
    cum = np.cumsum(ys, axis=0)
    base = np.zeros_like(cum[0])
    for i, (top, c) in enumerate(zip(cum, colors)):
        poly = ax.fill_between(x, base, top, color=c, alpha=alpha, lw=0, zorder=1)
        if gradient:
            clip = Polygon(np.column_stack([np.r_[x, np.asarray(x)[::-1]], np.r_[top, base[::-1]]]), closed=True,
                           facecolor="none", edgecolor="none", transform=ax.transData)
            ax.add_patch(clip)
            gradient_image(ax, (np.min(x), np.max(x), 0, cum[-1].max()), [_mix(c, light), mcolors.to_rgba(c)],
                           clip=clip, zorder=1.01)
        ax.plot(x, top, color=edge, lw=lw, zorder=2)
        if direct and labels:
            xi = label_x if label_x is not None else x[0] + 0.85 * (x[-1] - x[0])
            k = np.argmin(np.abs(np.asarray(x) - xi))
            if top[k] - base[k] > 0.04 * cum[-1].max():
                ax.text(x[k], (top[k] + base[k]) / 2, labels[i], ha="center", va="center",
                        fontsize=fontsize or _fs(), color="white" if sum(mcolors.to_rgb(c)) < 1.6 else "0.1")
        base = top
    return cum


# =================================================================================================== export
def export(fig, name, outdir=None, exact=False, audit=True):
    """Save a finished figure.
    * normal use: PNG (600 dpi) + PDF via nature_style.save_fig (or save_fig_exact for full-page layouts);
    * gallery build (env NATURE_GALLERY=<dir>): one 200-dpi PNG preview into that folder.
    Prints any text outside 5-8 pt (Nature minimum 5 pt) when audit=True."""
    apply_backgrounds(fig)
    if audit:
        bad = audit_text(fig, show=False, uniform=True)
        if bad:
            print(f"[export] {name}: {len(bad)} text items off the house size / face -> " +
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
