"""
nature_layout.py
================
Millimetre page layout for multi-panel main figures: every frame is placed at an exact position on the
printed page, so frames line up across rows and columns, panel letters sit at one offset from their frames,
and the saved PDF is exactly the page size (183 mm wide for a double-column figure).

    from nature_layout import Page, columns

    pg = Page(183, 150)                                   # width, height in mm
    cols = columns(12, 181, 3, gap=13.5)                  # [(x, w), ...] three equal columns
    a = pg.canvas(0, 2, 183, 30)                          # schematic band (1 data unit = 1 mm)
    b, c, d = pg.row(44, 38, cols)                        # three plotting frames, same top and height
    pg.letter(a, "a"); pg.letters([b, c, d], "bcd")
    pg.check()                                            # lists frame edges that are close but not equal
    pg.save("Fig1")                                       # exact page size (PNG 600 dpi + PDF)

Coordinates: x from the left page edge, y from the TOP page edge (as on paper), both in mm; (x, y) is the
top-left corner of the frame. Leave ~11-12 mm left of a frame for its y tick labels and y label, ~9-10 mm
under it for x tick labels and x label, and ~4 mm above it for a panel letter or subtitle.

Author: Denghui Pan
"""
from __future__ import annotations

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import nature_style as _ns
from nature_style import figsize_mm, MM_PER_IN

__all__ = ["Page", "columns", "split"]


def columns(x0, x1, n, gap=13.5, ratios=None):
    """n frames between x0 and x1 (mm) separated by *gap* (mm, room for the next frame's y labels).
    ratios: relative widths. Returns [(x, w), ...]."""
    ratios = np.ones(n) if ratios is None else np.asarray(ratios, float)
    total = x1 - x0 - gap * (n - 1)
    ws = total * ratios / ratios.sum()
    xs = x0 + np.r_[0, np.cumsum(ws[:-1] + gap)]
    return [(float(x), float(w)) for x, w in zip(xs, ws)]


def split(x, w, n, gap=2.0, ratios=None):
    """Split one column (x, w) into n sub-frames (e.g. two small panels or a panel plus its side strip)."""
    return columns(x, x + w, n, gap=gap, ratios=ratios)


class Page:
    """A figure of exactly width_mm x height_mm with helpers to place frames in mm."""

    def __init__(self, width_mm=183.0, height_mm=170.0, letter_dx=-10.0, letter_dy=-3.2):
        self.W, self.H = float(width_mm), float(height_mm)
        self.fig = plt.figure(figsize=figsize_mm(self.W, self.H))
        self.letter_dx, self.letter_dy = letter_dx, letter_dy
        self._frames = []

    # ------------------------------------------------------------------ placement
    def rect(self, x, y, w, h):
        """mm (top-left origin) -> figure fraction [left, bottom, width, height]."""
        return [x / self.W, 1 - (y + h) / self.H, w / self.W, h / self.H]

    def ax(self, x, y, w, h, frame=True, **kw):
        """Plotting frame at (x, y) with size w x h mm. frame=False: not used in the alignment audit."""
        a = self.fig.add_axes(self.rect(x, y, w, h), **kw)
        a._ns_mm = (x, y, w, h)
        if frame:
            self._frames.append(a)
        return a

    def row(self, y, h, cols, **kw):
        """One frame per (x, w) in *cols*, all with top y and height h. Returns the list of axes."""
        return [self.ax(x, y, w, h, **kw) for x, w in cols]

    def grid(self, x, y, w, h, nrows, ncols, wgap=2.0, hgap=2.0, sharex=False, sharey=False):
        """nrows x ncols small frames filling the box (x, y, w, h) -- small multiples inside one panel.
        Returns a 2-D array of axes; only the bottom row / left column keep tick labels when shared."""
        cw = (w - wgap * (ncols - 1)) / ncols
        rh = (h - hgap * (nrows - 1)) / nrows
        out = np.empty((nrows, ncols), dtype=object)
        for i in range(nrows):
            for j in range(ncols):
                kw = {}
                if sharex and (i or j):
                    kw["sharex"] = out[0, 0]
                if sharey and (i or j):
                    kw["sharey"] = out[0, 0]
                out[i, j] = self.ax(x + j * (cw + wgap), y + i * (rh + hgap), cw, rh, frame=False, **kw)
                if sharex and i < nrows - 1:
                    out[i, j].tick_params(labelbottom=False)
                if sharey and j > 0:
                    out[i, j].tick_params(labelleft=False)
        return out

    def canvas(self, x, y, w, h):
        """Schematic band: an axes of w x h mm whose data units are millimetres (see nature_schematic)."""
        from nature_schematic import canvas as _canvas
        a = self.ax(x, y, w, h, frame=False)
        _canvas(a, w, h)
        a._ns_canvas = True
        return a

    def cax(self, x, y, w, h, mappable, label=None, orientation=None, ticks=None, extend=None, **kw):
        """Colour bar in a fixed mm rectangle (keeps every plotting frame its planned size)."""
        from nature_cmaps import style_cbar
        orientation = orientation or ("vertical" if h > w else "horizontal")
        c = self.fig.add_axes(self.rect(x, y, w, h))
        args = dict(cax=c, orientation=orientation, ticks=ticks)
        if extend:
            args["extend"] = extend
        cb = self.fig.colorbar(mappable, **args, **kw)
        style_cbar(cb)
        if label:
            if orientation == "horizontal":
                c.set_title(label, pad=2)
            else:
                cb.set_label(label)
        return cb

    # ------------------------------------------------------------------ letters and text
    def letter(self, ax, text, dx=None, dy=None):
        """Panel letter at a fixed mm offset from the frame's top-left corner (canvases: just inside it)."""
        x, y, w, h = ax._ns_mm
        if getattr(ax, "_ns_canvas", False):
            dx = 1.0 if dx is None else dx
            dy = 1.0 if dy is None else dy
        else:
            dx = self.letter_dx if dx is None else dx
            dy = self.letter_dy if dy is None else dy
        return self.fig.text((x + dx) / self.W, 1 - (y + dy) / self.H, text, fontsize=_ns._PANEL_LABEL_SIZE,
                             fontweight="bold", ha="left", va="top")

    def letters(self, axes, texts, **kw):
        return [self.letter(a, t, **kw) for a, t in zip(axes, texts)]

    def text(self, x, y, s, **kw):
        """Free text at (x, y) mm (top-left origin)."""
        kw.setdefault("va", "top")
        return self.fig.text(x / self.W, 1 - y / self.H, s, **kw)

    # ------------------------------------------------------------------ QA and export
    def check(self, tol=1.5, show=True):
        """Report frame edges that are within *tol* mm of each other but not equal (almost aligned = looks
        misaligned in print). Returns a list of (edge, value_a, value_b)."""
        edges = {"left": [], "right": [], "top": [], "bottom": []}
        for a in self._frames:
            x, y, w, h = a._ns_mm
            edges["left"].append(x); edges["right"].append(x + w)
            edges["top"].append(y); edges["bottom"].append(y + h)
        bad = []
        for k, vals in edges.items():
            u = sorted(set(round(v, 3) for v in vals))
            for v1, v2 in zip(u[:-1], u[1:]):
                if 0 < v2 - v1 < tol:
                    bad.append((k, v1, v2))
        if show:
            print(f"[layout] {len(self._frames)} frames, {len(bad)} near-misses" +
                  ("" if not bad else ": " + ", ".join(f"{k} {a:.1f}/{b:.1f} mm" for k, a, b in bad)))
        return bad

    def guides(self, color="#E84143"):
        """Draw the frame edges as thin dashed lines over the page (use while laying out; remove before saving)."""
        for a in self._frames:
            x, y, w, h = a._ns_mm
            for xx in (x, x + w):
                self.fig.add_artist(mpl.lines.Line2D([xx / self.W] * 2, [0, 1], color=color, lw=0.3, ls=":"))
            for yy in (y, y + h):
                self.fig.add_artist(mpl.lines.Line2D([0, 1], [1 - yy / self.H] * 2, color=color, lw=0.3, ls=":"))

    def save(self, name, **kw):
        """Exact-size export (nature_charts.export(..., exact=True)) after the alignment audit."""
        from nature_charts import export
        self.check()
        return export(self.fig, name, exact=True, **kw)
