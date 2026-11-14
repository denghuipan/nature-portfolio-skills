"""
nature_schematic.py
===================
Primitives for simple concept diagrams drawn in matplotlib (so they share fonts, line weights and colours
with the data panels and stay vector in the PDF): flow charts, optical set-ups in line art, device top views
and cross-sections, isometric blocks, neural-network sketches, matrix and curve icons, sketch-style concept
plots.

Coordinates are millimetres on a canvas created with ``canvas(ax, width_mm, height_mm)``; if the axes is
drawn at that physical size, 1 data unit = 1 mm on paper, so line widths and gaps can be reasoned about
directly. Text uses the current rcParams (5-7 pt).

For photo-real renders (Blender / KeyShot) keep this module for labels, arrows and insets on top.

Author: Denghui Pan
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import matplotlib as mpl
import matplotlib.colors as mcolors
from matplotlib.patches import (FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon, Circle, Ellipse,
                                PathPatch, ConnectionPatch)
from matplotlib.path import Path as MPath

import nature_style as _ns
from nature_style import PALETTE, gradient_image, _mix
from nature_cmaps import lighten, darken, NS_EMBER

__all__ = [
    "Box", "canvas", "box", "arrow", "elbow", "label", "section_header", "divider", "beam", "cone",
    "lens", "objective", "beamsplitter", "mirror", "nd_filter", "fiber", "fiber_coil", "camera",
    "random_field", "periodic_field", "region_topview", "layer_stack", "dimension", "iso", "iso_block", "nn_diagram",
    "conv_blocks", "matrix_icon", "mini_plot", "image_icon", "concept_axes", "brace", "zoom_connector",
    "LINE", "FILL", "EDGE", "PASTEL", "pastel", "group_frame", "pbox", "cylinder", "circle_node", "plus_node",
    "route", "chevrons", "cycle_diagram", "icon_graph", "icon_stack", "icon_bars", "icon_person", "icon_cells",
    "timeline", "letter", "GRADIENT_FILLS",
]

LINE = "0.2"          # default stroke for diagram lines
EDGE = "0.45"         # box edges
FILL = "#EEEEEE"      # neutral component fill (Fig. 3a style)
BEAM = "#7CCB7C"      # default beam colour; use wavelength colours when meaningful


GRADIENT_FILLS = True   # pastel boxes, frames, nodes, chevrons and cylinders get soft vertical gradients


def _fs(scale=1.0):
    """House font size. *scale* is accepted for old calls but ignored: every diagram label uses one size."""
    return mpl.rcParams["font.size"]


def _grad_fill(ax, patch, fc, top=0.55, bottom=0.0, direction="up", zorder=None):
    """Gradient inside *patch*: fc slightly deepened at the bottom -> fc lightened by *top* at the top."""
    if not GRADIENT_FILLS:
        return None
    ext = patch.get_path().get_extents(patch.get_patch_transform())
    c_bot = _mix(fc, bottom, "#000000") if bottom > 0 else mcolors.to_rgba(fc)
    return gradient_image(ax, (ext.x0, ext.x1, ext.y0, ext.y1), [c_bot, _mix(fc, top)], direction=direction,
                          clip=patch, zorder=(patch.get_zorder() + 0.01) if zorder is None else zorder)


def letter(ax, x, y, text, **kw):
    """Bold panel letter on a mm canvas (same size as nature_style.panel_label)."""
    return ax.text(x, y, text, ha="left", va="top", fontsize=_ns._PANEL_LABEL_SIZE, fontweight="bold", **kw)


def _lw(scale=1.0):
    return mpl.rcParams["axes.linewidth"] * scale


# ------------------------------------------------------------------------------------------------- canvas / boxes
def canvas(ax, width_mm, height_mm):
    """Turn an axes into a mm-scaled drawing area (no frame, equal aspect)."""
    ax.set_xlim(0, width_mm)
    ax.set_ylim(0, height_mm)
    ax.set_aspect("equal")
    ax.axis("off")
    return ax


@dataclass
class Box:
    x: float
    y: float
    w: float
    h: float

    @property
    def l(self):
        return (self.x, self.y + self.h / 2)

    @property
    def r(self):
        return (self.x + self.w, self.y + self.h / 2)

    @property
    def t(self):
        return (self.x + self.w / 2, self.y + self.h)

    @property
    def b(self):
        return (self.x + self.w / 2, self.y)

    @property
    def c(self):
        return (self.x + self.w / 2, self.y + self.h / 2)


def box(ax, x, y, w, h, text=None, sub=None, fc=FILL, ec=EDGE, lw=None, r=0.8, fontsize=None, color="k",
        sub_color="0.4", bold=False, zorder=2, ls="-", grad=True):
    """Rounded component box with a title line and an optional grey second line; filled boxes get a soft
    vertical gradient (grad=False for flat). Returns a Box (anchors l/r/t/b/c)."""
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec="none",
                       lw=0, zorder=zorder)
    ax.add_patch(p)
    if grad and fc not in ("none", "white", "#FFFFFF", "w"):
        _grad_fill(ax, p, fc, top=0.6, bottom=0.03)
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc="none", ec=ec,
                                lw=lw if lw is not None else _lw(0.8), zorder=zorder + 0.02, ls=ls))
    fs = fontsize or _fs(1.1)
    if text and sub:
        ax.text(x + w / 2, y + h * 0.60, text, ha="center", va="center", fontsize=fs, color=color,
                fontweight="bold" if bold else "normal", zorder=zorder + 1)
        ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center", fontsize=fs, color=sub_color,
                zorder=zorder + 1)
    elif text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color,
                fontweight="bold" if bold else "normal", zorder=zorder + 1)
    return Box(x, y, w, h)


def arrow(ax, p0, p1, color=LINE, lw=None, style="-|>", head=5.0, ls="-", rad=0.0, shrink=0.6, zorder=3):
    """Straight or gently curved arrow between two points (mm)."""
    a = FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=head, color=color, lw=lw or _lw(0.9),
                        linestyle=ls, connectionstyle=f"arc3,rad={rad}", shrinkA=shrink, shrinkB=shrink,
                        zorder=zorder, joinstyle="miter", capstyle="butt")
    ax.add_patch(a)
    return a


def elbow(ax, points, color=LINE, lw=None, dashed=False, head=5.0, arrow_end=True, zorder=3):
    """Orthogonal routed connector through the given points; arrow head on the last segment."""
    pts = np.asarray(points, float)
    ls = (0, (2.5, 1.5)) if dashed else "-"
    ax.plot(pts[:-1, 0], pts[:-1, 1], color=color, lw=lw or _lw(0.8), ls=ls, zorder=zorder,
            solid_capstyle="butt", dash_capstyle="butt")
    ax.plot(pts[-2:, 0], pts[-2:, 1], color=color, lw=lw or _lw(0.8), ls=ls, zorder=zorder) if not arrow_end else None
    if arrow_end:
        arrow(ax, tuple(pts[-2]), tuple(pts[-1]), color=color, lw=lw or _lw(0.8), head=head,
              ls="--" if dashed else "-", shrink=0, zorder=zorder)


def label(ax, x, y, text, ha="center", va="center", color="k", size=1.0, **kw):
    """Plain diagram label (size relative to the legend font, i.e. 6 pt in np_final)."""
    return ax.text(x, y, text, ha=ha, va=va, color=color, fontsize=_fs(size), **kw)


def section_header(ax, x0, x1, y, text, color="k", rule_color="0.6", gap=1.2, bold=True, size=1.15):
    """Bold section title over a thin grey rule ('Stage 1' | 'Stage 2')."""
    ax.text((x0 + x1) / 2, y + gap, text, ha="center", va="bottom", fontsize=_fs(size),
            fontweight="bold" if bold else "normal", color=color)
    ax.plot([x0, x1], [y, y], color=rule_color, lw=_lw(0.6))


def divider(ax, x, y0, y1, color="0.45", dashed=True):
    """Vertical dashed divider between diagram sections."""
    ax.plot([x, x], [y0, y1], color=color, lw=_lw(0.7), ls=(0, (3, 2)) if dashed else "-")


# ------------------------------------------------------------------------------------------------- optics
def beam(ax, points, color=BEAM, width=1.6, alpha=0.85, zorder=1):
    """Collimated beam as a thick translucent polyline (width in points)."""
    pts = np.asarray(points, float)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=width, alpha=alpha, solid_capstyle="butt", zorder=zorder)


def cone(ax, apex, base, half_width, color=BEAM, alpha=0.35, zorder=1):
    """Focusing / diverging beam: triangle from apex (point) to a base segment centred at `base`,
    perpendicular to the apex-base line."""
    a = np.asarray(apex, float); b = np.asarray(base, float)
    d = b - a
    n = np.array([-d[1], d[0]]) / (np.hypot(*d) + 1e-12)
    poly = Polygon([a, b + n * half_width, b - n * half_width], closed=True, fc=color, ec="none", alpha=alpha,
                   zorder=zorder)
    ax.add_patch(poly)
    return poly


def lens(ax, x, y, h, w=1.0, fc="#DDEBF7", ec="0.35", zorder=4):
    """Bi-convex lens (vertical, centred at x, y; height h, centre thickness w)."""
    t = np.linspace(-1, 1, 40)
    yy = y + t * h / 2
    bulge = w / 2 * np.sqrt(1 - t ** 2)
    xs = np.r_[x - bulge, (x + bulge)[::-1]]
    ys = np.r_[yy, yy[::-1]]
    p = Polygon(np.column_stack([xs, ys]), closed=True, fc=fc, ec=ec, lw=_lw(0.7), zorder=zorder)
    ax.add_patch(p)
    return p


def objective(ax, x, y, h=4.0, L=6.0, facing="right", fc="#E6E6E6", ec="0.35", label_text=None, zorder=4):
    """Microscope objective in line art: barrel + tapered nose. (x, y) = tip of the nose."""
    s = 1 if facing == "right" else -1
    nose = [(x, y - h * 0.18), (x, y + h * 0.18), (x - s * L * 0.38, y + h * 0.42), (x - s * L * 0.38, y - h * 0.42)]
    barrel = [(x - s * L * 0.38, y - h / 2), (x - s * L * 0.38, y + h / 2), (x - s * L, y + h / 2), (x - s * L, y - h / 2)]
    for pts in (barrel, nose):
        ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=ec, lw=_lw(0.7), zorder=zorder))
    if label_text:
        label(ax, x - s * L * 0.55, y + h / 2 + 1.2, label_text, va="bottom")
    return (x, y)


def beamsplitter(ax, x, y, s=3.0, fc="#DDEBF7", ec="0.3", label_text=None, label_below=True, zorder=4):
    """Cube beam splitter centred at (x, y) with its diagonal."""
    ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc=fc, ec=ec, lw=_lw(0.7), zorder=zorder))
    ax.plot([x - s / 2, x + s / 2], [y - s / 2, y + s / 2], color=ec, lw=_lw(0.7), zorder=zorder + 0.1)
    if label_text:
        label(ax, x, y - s / 2 - 1.0 if label_below else y + s / 2 + 1.0, label_text,
              va="top" if label_below else "bottom", color="0.35")


def mirror(ax, x, y, L=4.0, angle=45.0, color="0.25", zorder=4):
    """Plane mirror (thick line) with short hatch marks on the back side."""
    a = np.radians(angle)
    d = np.array([np.cos(a), np.sin(a)]) * L / 2
    p0, p1 = np.array([x, y]) - d, np.array([x, y]) + d
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=color, lw=_lw(1.8), solid_capstyle="butt", zorder=zorder)
    n = np.array([np.sin(a), -np.cos(a)]) * 0.6
    for t in np.linspace(0.1, 0.9, 6):
        q = p0 + (p1 - p0) * t
        ax.plot([q[0], q[0] + n[0] + d[0] * 0.12], [q[1], q[1] + n[1] + d[1] * 0.12], color=color, lw=_lw(0.5),
                zorder=zorder)


def nd_filter(ax, x, y, h=4.0, gap=0.8, w=0.6, fc="0.35", label_text=None):
    """Pair of neutral-density plates."""
    for dx in (-gap / 2 - w, gap / 2):
        ax.add_patch(Rectangle((x + dx, y - h / 2), w, h, fc=fc, ec="0.2", lw=_lw(0.5), zorder=4))
    if label_text:
        label(ax, x, y - h / 2 - 1.0, label_text, va="top", color="0.35")


def fiber(ax, points, color="#C9A227", lw=None, zorder=2):
    """Smooth fibre path through control points (quadratic Bezier chain)."""
    pts = np.asarray(points, float)
    verts = [tuple(pts[0])]
    codes = [MPath.MOVETO]
    for i in range(1, len(pts) - 1):
        mid = (pts[i] + pts[i + 1]) / 2
        verts += [tuple(pts[i]), tuple(mid)]
        codes += [MPath.CURVE3, MPath.CURVE3]
    verts.append(tuple(pts[-1])); codes.append(MPath.LINETO)
    ax.add_patch(PathPatch(MPath(verts, codes), fc="none", ec=color, lw=lw or _lw(1.6), zorder=zorder,
                           capstyle="round"))


def fiber_coil(ax, x, y, r=2.0, loops=2, color="#C9A227", lw=None, sep=None, zorder=3):
    """Fibre spool drawn as overlapping loops centred at (x, y)."""
    sep = sep if sep is not None else r * 0.9
    for k in range(loops):
        cx = x + (k - (loops - 1) / 2) * sep
        ax.add_patch(Circle((cx, y), r, fc="none", ec=color, lw=lw or _lw(1.6), zorder=zorder))


def camera(ax, x, y, w=8.0, h=6.0, fc="#3A3F47", facing="left", label_text=None, zorder=4):
    """Camera body (dark rounded box) with a lens mount on the input side. (x, y) = lower-left corner."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.8", fc=fc, ec="none",
                                zorder=zorder))
    mw, mh = w * 0.14, h * 0.42
    mx = x - mw if facing == "left" else x + w
    ax.add_patch(Rectangle((mx, y + h / 2 - mh / 2), mw, mh, fc=darken(fc, 0.3), ec="none", zorder=zorder))
    if label_text:
        label(ax, x + w / 2, y + h + 1.0, label_text, va="bottom")
    return Box(x, y, w, h)


# ------------------------------------------------------------------------------------------------- waveguides
def random_field(nx=200, ny=200, corr=6.0, seed=3, positive=True):
    """Smooth random 2-D field (Gaussian-filtered noise), normalised to [0, 1]; a neutral placeholder image
    for icons (micrograph, map, camera frame). For illustration only."""
    from scipy.ndimage import gaussian_filter
    rng = np.random.default_rng(seed)
    f = gaussian_filter(rng.normal(size=(ny, nx)), corr)
    f = (f - f.min()) / (f.max() - f.min())
    return f ** 2 if positive else f


def periodic_field(nx=200, ny=200, kx=6, ky=6, seed=0):
    """Periodic 2-D intensity pattern (lattice of spots) normalised to [0, 1] -- placeholder for a structured
    sample or a diffraction-like image in diagrams."""
    yv, xv = np.mgrid[0:1:complex(ny), 0:1:complex(nx)]
    f = (np.cos(2 * np.pi * kx * xv) * np.cos(2 * np.pi * ky * yv) + 1) / 2
    return f ** 3


def region_topview(ax, x, y, L=30.0, W=12.0, image=None, cmap=NS_EMBER, ec="0.25", substrate_pad=2.0,
                   zorder=2, seed=3):
    """Top view of a rectangular active region on a substrate, filled with an image (pass `image`; default:
    random_field). (x, y) = lower-left corner of the region. Returns Box of the region."""
    ax.add_patch(Rectangle((x - substrate_pad, y - substrate_pad), L + 2 * substrate_pad, W + 2 * substrate_pad,
                           fc="#F2F2F2", ec="0.7", lw=_lw(0.5), zorder=zorder - 1))
    img = image if image is not None else random_field(seed=seed)
    ax.imshow(img, extent=(x, x + L, y, y + W), cmap=cmap, origin="lower", aspect="auto",
              interpolation="bilinear", zorder=zorder)
    ax.add_patch(Rectangle((x, y), L, W, fc="none", ec=ec, lw=_lw(0.6), zorder=zorder + 0.5))
    return Box(x, y, L, W)


def layer_stack(ax, x, y, width, layers, ridge=None, labels=True, label_x=None, fontsize=None, edge="0.3"):
    """Cross-section: layers bottom -> top as dicts {name, h, color}; optional ridge dict {name, w, h, color}
    centred on the top layer. Returns the y of the top surface and the ridge Box (if any)."""
    yy = y
    lx = label_x if label_x is not None else x + width + 1.0
    for L_ in layers:
        ax.add_patch(Rectangle((x, yy), width, L_["h"], fc=L_["color"], ec=edge, lw=_lw(0.5), zorder=2))
        if labels and L_.get("name"):
            ax.text(lx, yy + L_["h"] / 2, L_["name"], ha="left", va="center", fontsize=fontsize or _fs())
        yy += L_["h"]
    rb = None
    if ridge:
        rx = x + width / 2 - ridge["w"] / 2
        ax.add_patch(Rectangle((rx, yy), ridge["w"], ridge["h"], fc=ridge["color"], ec=edge, lw=_lw(0.5), zorder=3))
        rb = Box(rx, yy, ridge["w"], ridge["h"])
        if labels and ridge.get("name"):
            ax.text(lx, yy + ridge["h"] / 2, ridge["name"], ha="left", va="center", fontsize=fontsize or _fs())
    return yy, rb


def dimension(ax, p0, p1, text, offset=1.2, color="0.25", fontsize=None, text_pad=0.6, tick=0.6):
    """Engineering dimension line between p0 and p1, offset perpendicular by `offset` mm, with end ticks."""
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float)
    d = p1 - p0
    n = np.array([-d[1], d[0]]) / (np.hypot(*d) + 1e-12)
    a, b = p0 + n * offset, p1 + n * offset
    arr = FancyArrowPatch(tuple(a), tuple(b), arrowstyle="<|-|>", mutation_scale=4, color=color, lw=_lw(0.6),
                          shrinkA=0, shrinkB=0, zorder=5)
    ax.add_patch(arr)
    for q, e in ((p0, a), (p1, b)):
        ax.plot([q[0] + n[0] * 0.3, e[0] + n[0] * tick], [q[1] + n[1] * 0.3, e[1] + n[1] * tick], color=color,
                lw=_lw(0.4), zorder=5)
    mid = (a + b) / 2 + n * text_pad
    ang = np.degrees(np.arctan2(d[1], d[0]))
    if ang > 90 or ang < -90:
        ang += 180
    ax.text(mid[0], mid[1], text, rotation=ang, ha="center", va="center", fontsize=fontsize or _fs(), color=color,
            rotation_mode="anchor")


# ------------------------------------------------------------------------------------------------- isometric
_ISO = np.radians(30)


def iso(x, y, z, ox=0.0, oy=0.0, s=1.0):
    """Isometric projection of (x, y, z) (x to the lower right, y to the upper right, z up) -> 2-D mm."""
    X = ox + s * (x * np.cos(_ISO) + y * np.cos(_ISO))
    Y = oy + s * (-x * np.sin(_ISO) + y * np.sin(_ISO) + z)
    return X, Y


def iso_block(ax, x, y, z, dx, dy, dz, color="#9AA3AD", ox=0.0, oy=0.0, s=1.0, shade=(1.0, 0.82, 0.66),
              ec="0.3", lw=None, zorder=2, alpha=1.0):
    """Isometric cuboid with three shaded visible faces (top light, front mid, side dark)."""
    P = lambda a, b, c: iso(a, b, c, ox, oy, s)
    top = [P(x, y, z + dz), P(x + dx, y, z + dz), P(x + dx, y + dy, z + dz), P(x, y + dy, z + dz)]
    front = [P(x, y, z), P(x + dx, y, z), P(x + dx, y, z + dz), P(x, y, z + dz)]       # face at y = y (lower left)
    side = [P(x + dx, y, z), P(x + dx, y + dy, z), P(x + dx, y + dy, z + dz), P(x + dx, y, z + dz)]  # x = x+dx
    # shade = (top lightening, front scale, side scale): top lighter, front = colour, side darker
    faces = [(front, darken(color, 1 - shade[1])), (side, darken(color, 1 - shade[2])),
             (top, lighten(color, 0.3 * shade[0]))]
    for pts, c in faces:
        ax.add_patch(Polygon(pts, closed=True, fc=c, ec=ec, lw=lw if lw is not None else _lw(0.5), zorder=zorder,
                             alpha=alpha, joinstyle="round"))
    return top


# ------------------------------------------------------------------------------------------------- networks / icons
def nn_diagram(ax, x, y, w, h, layers=(6, 9, 9, 7, 5), colors=None, edge_color="0.78", node_r=None, edge_lw=0.25,
               zorder=3):
    """Fully-connected network sketch: columns of nodes joined by thin grey edges."""
    n = len(layers)
    colors = colors or (["#9DBCDD"] + ["#C4C4C4"] * (n - 2) + ["#D08C34"])
    xs = np.linspace(x, x + w, n)
    node_r = node_r or min(w / (n * 6), h / (max(layers) * 2.6))
    cols = []
    for k, (nk, xk) in enumerate(zip(layers, xs)):
        ys = y + h / 2 + (np.arange(nk) - (nk - 1) / 2) * (h / max(layers))
        cols.append((xk, ys))
    for (x0, y0s), (x1, y1s) in zip(cols[:-1], cols[1:]):
        for a in y0s:
            for b in y1s:
                ax.plot([x0, x1], [a, b], color=edge_color, lw=edge_lw, zorder=zorder - 1)
    for (xk, ys), c in zip(cols, colors):
        for yk in ys:
            ax.add_patch(Circle((xk, yk), node_r, fc=c, ec=darken(c, 0.3), lw=_lw(0.4), zorder=zorder))
    return cols


def conv_blocks(ax, x, y, specs, gap=2.0, depth_scale=0.5, ec="0.3", label_size=0.9):
    """Pseudo-3-D feature-map blocks for a CNN sketch. specs: list of dicts {w, h, d, color, label}.
    Blocks are bottom-aligned at y and drawn left to right."""
    cx = x
    boxes = []
    for sp in specs:
        w, h, d = sp["w"], sp["h"], sp.get("d", 2.0)
        c = sp.get("color", "#9DBCDD")
        dx, dy = d * depth_scale, d * depth_scale
        y0 = y + (max(s["h"] for s in specs) - h) / 2
        front = Rectangle((cx, y0), w, h, fc=c, ec=ec, lw=_lw(0.5), zorder=3)
        top = Polygon([(cx, y0 + h), (cx + dx, y0 + h + dy), (cx + w + dx, y0 + h + dy), (cx + w, y0 + h)],
                      closed=True, fc=lighten(c, 0.35), ec=ec, lw=_lw(0.5), zorder=3)
        side = Polygon([(cx + w, y0), (cx + w + dx, y0 + dy), (cx + w + dx, y0 + h + dy), (cx + w, y0 + h)],
                       closed=True, fc=darken(c, 0.2), ec=ec, lw=_lw(0.5), zorder=3)
        for p in (front, top, side):
            ax.add_patch(p)
        if sp.get("label"):
            label(ax, cx + w / 2, y - 1.0, sp["label"], va="top", size=label_size)
        boxes.append(Box(cx, y0, w + dx, h + dy))
        cx += w + dx + gap
    return boxes


def matrix_icon(ax, x, y, w, h, data=None, cmap="magma", grid_color="w", grid_lw=0.5, shape=(12, 14), seed=1,
                axis_labels=None):
    """Small coloured matrix icon (any 2-D table / operator). axis_labels=('i', 'j')
    draws arrows along the top and left edges with italic labels."""
    if data is None:
        rng = np.random.default_rng(seed)
        data = rng.random(shape)
    ny, nx = data.shape
    ax.imshow(data, extent=(x, x + w, y, y + h), cmap=cmap, origin="upper", aspect="auto",
              interpolation="nearest", zorder=2)
    for i in range(1, nx):
        ax.plot([x + w * i / nx] * 2, [y, y + h], color=grid_color, lw=grid_lw, zorder=3)
    for j in range(1, ny):
        ax.plot([x, x + w], [y + h * j / ny] * 2, color=grid_color, lw=grid_lw, zorder=3)
    if axis_labels:
        arrow(ax, (x, y + h + 1.0), (x + w, y + h + 1.0), lw=_lw(0.6), head=4, shrink=0)
        arrow(ax, (x - 1.0, y + h), (x - 1.0, y), lw=_lw(0.6), head=4, shrink=0)
        label(ax, x + w + 0.8, y + h + 1.0, axis_labels[0], ha="left", style="italic")
        label(ax, x - 1.0, y - 0.8, axis_labels[1], va="top", style="italic")
    return Box(x, y, w, h)


def mini_plot(ax, x, y, w, h, xdata, ydata, color="#3A6EA5", fill=True, ls="-", lw=None, frame=True, ticks=3,
              ylim=None, zorder=3):
    """Framed miniature plot inside a diagram (curve icons). Data are mapped into the box."""
    xd = np.asarray(xdata, float); yd = np.asarray(ydata, float)
    lo, hi = ylim if ylim else (min(0, yd.min()), yd.max() * 1.12)
    X = x + (xd - xd.min()) / (xd.max() - xd.min()) * w
    Y = y + (yd - lo) / (hi - lo) * h
    if fill:
        clip = Polygon(np.column_stack([np.r_[X, X[::-1]], np.r_[Y, np.full_like(Y, y)]]), closed=True, fc="none",
                       ec="none")
        ax.add_patch(clip)
        gradient_image(ax, (X.min(), X.max(), y, Y.max()), [mcolors.to_rgba(color, 0.0), mcolors.to_rgba(color, 0.4)],
                       clip=clip, zorder=zorder)
    ax.plot(X, Y, color=color, lw=lw or _lw(1.1), ls=ls, zorder=zorder + 0.1)
    if frame:
        ax.add_patch(Rectangle((x, y), w, h, fc="none", ec="k", lw=_lw(0.6), zorder=zorder + 0.2))
        for k in range(1, ticks + 1):
            tx = x + w * k / (ticks + 1)
            ax.plot([tx, tx], [y, y + h * 0.05], color="k", lw=_lw(0.4), zorder=zorder + 0.2)
            ax.plot([tx, tx], [y + h, y + h * 0.95], color="k", lw=_lw(0.4), zorder=zorder + 0.2)
            ty = y + h * k / (ticks + 1)
            ax.plot([x, x + w * 0.04], [ty, ty], color="k", lw=_lw(0.4), zorder=zorder + 0.2)
            ax.plot([x + w, x + w * 0.96], [ty, ty], color="k", lw=_lw(0.4), zorder=zorder + 0.2)
    return Box(x, y, w, h)


def image_icon(ax, x, y, w, h, img, cmap=NS_EMBER, frame=False, zorder=2):
    """Place an image (micrograph, field map) into the diagram at (x, y, w, h)."""
    ax.imshow(img, extent=(x, x + w, y, y + h), cmap=cmap, origin="lower", aspect="auto",
              interpolation="bilinear", zorder=zorder)
    if frame:
        ax.add_patch(Rectangle((x, y), w, h, fc="none", ec="k", lw=_lw(0.5), zorder=zorder + 0.1))
    return Box(x, y, w, h)


# ------------------------------------------------------------------------------------------------- concept plots
def concept_axes(ax, xlabel=None, ylabel=None, color="k", head=5.0):
    """Sketch-style axes for qualitative concept plots: only left/bottom spines, arrow heads, no ticks/numbers.
    Use for trade-off and regime diagrams where numbers would claim precision that is not there."""
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(which="both", left=False, bottom=False, top=False, right=False, labelleft=False,
                   labelbottom=False)
    ax.spines["left"].set_visible(False); ax.spines["bottom"].set_visible(False)
    lw = mpl.rcParams["axes.linewidth"]
    ax.annotate("", xy=(1.0, 0), xytext=(0, 0), xycoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=color, mutation_scale=head, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=(0, 1.0), xytext=(0, 0), xycoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=color, mutation_scale=head, shrinkA=0, shrinkB=0))
    if xlabel:
        ax.text(1.0, -0.04, xlabel, transform=ax.transAxes, ha="right", va="top",
                fontsize=mpl.rcParams["axes.labelsize"])
    if ylabel:
        ax.text(-0.04, 1.0, ylabel, transform=ax.transAxes, ha="right", va="top", rotation=90,
                fontsize=mpl.rcParams["axes.labelsize"])
    return ax


def brace(ax, x0, x1, y, text=None, height=1.2, color="0.25", up=True, fontsize=None):
    """Horizontal curly brace from x0 to x1 at y (pointing up or down) with a label."""
    s = 1 if up else -1
    xm = (x0 + x1) / 2
    q = height
    verts = [(x0, y), (x0, y + s * q * 0.6), (x0 + 0.2 * (xm - x0), y + s * q * 0.6), (xm - 0.6, y + s * q * 0.6),
             (xm, y + s * q * 0.6), (xm, y + s * q)]
    v2 = [(x1, y), (x1, y + s * q * 0.6), (x1 - 0.2 * (x1 - xm), y + s * q * 0.6), (xm + 0.6, y + s * q * 0.6),
          (xm, y + s * q * 0.6), (xm, y + s * q)]
    for v in (verts, v2):
        codes = [MPath.MOVETO, MPath.CURVE3, MPath.CURVE3, MPath.LINETO, MPath.CURVE3, MPath.CURVE3]
        ax.add_patch(PathPatch(MPath(v, codes), fc="none", ec=color, lw=_lw(0.7)))
    if text:
        ax.text(xm, y + s * (q + 0.5), text, ha="center", va="bottom" if up else "top", color=color,
                fontsize=fontsize or _fs())


def zoom_connector(fig, ax_src, xy0_src, xy1_src, ax_dst, color="0.4", ls=(0, (3, 2)), corners=("left", "right")):
    """Dashed lines from two points of a source axes (data coords) to the left/right top corners of a target
    axes (axes fraction) -- the 'zoomed region' cue of composite schematic figures."""
    lw = _lw(0.7)
    dst = {"left": (0, 1), "right": (1, 1), "bl": (0, 0), "br": (1, 0)}
    for p, c in zip((xy0_src, xy1_src), corners):
        con = ConnectionPatch(xyA=p, coordsA=ax_src.transData, xyB=dst.get(c, c), coordsB=ax_dst.transAxes,
                              color=color, lw=lw, ls=ls)
        fig.add_artist(con)


# ------------------------------------------------------------------------------------------------- pipeline diagrams
# Pastel fill / edge pairs for block diagrams: one colour per stage or module family, never more than four.
PASTEL = {
    "blue": ("#EAF0F8", "#7C9CC6"), "green": ("#E8F3EC", "#7FB394"), "orange": ("#FBF0E2", "#D3A066"),
    "purple": ("#F0ECF7", "#9C8BC4"), "grey": ("#F3F3F3", "#A3A3A3"), "rose": ("#F8EBEE", "#C98E9C"),
    "teal": ("#E5F2F1", "#6FAAA3"),
}


def pastel(name):
    """(fill, edge) pair from PASTEL."""
    return PASTEL[name]


def group_frame(ax, x, y, w, h, title=None, color="blue", r=1.6, lw=None, title_side="top", fill="white",
                ls="-", zorder=1, title_size=1.05):
    """Rounded frame around a group of boxes (a pipeline, a module), coloured edge, title centred above it."""
    ec = PASTEL[color][1] if color in PASTEL else color
    fp = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fill, ec="none", lw=0,
                        zorder=zorder)
    ax.add_patch(fp)
    if GRADIENT_FILLS:
        gradient_image(ax, (x, x + w, y, y + h), [_mix(ec, 0.88), mcolors.to_rgba(fill)], direction="up", clip=fp,
                       zorder=zorder + 0.01)
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc="none", ec=ec,
                                lw=lw or _lw(1.0), ls=ls, zorder=zorder + 0.02))
    if title:
        ty = y + h + 0.9 if title_side == "top" else y - 0.9
        ax.text(x + w / 2, ty, title, ha="center", va="bottom" if title_side == "top" else "top",
                fontsize=_fs(title_size), zorder=zorder + 1)
    return Box(x, y, w, h)


def pbox(ax, x, y, w, h, text=None, color="grey", sub=None, r=0.8, bold=False, fontsize=None, zorder=2, ls="-",
         grad=True):
    """Pastel module box: box() with fill/edge from PASTEL[color] (gradient fill by default)."""
    fc, ec = PASTEL[color]
    if grad:                                  # a little more colour at the bottom so the gradient shows
        fc = _mix(ec, 0.72)
    return box(ax, x, y, w, h, text=text, sub=sub, fc=fc, ec=ec, r=r, bold=bold, fontsize=fontsize, zorder=zorder,
               ls=ls, grad=grad)


def cylinder(ax, x, y, w, h, text=None, fc="#F3F3F3", ec="0.45", lw=None, cap=0.18, fontsize=None, zorder=3):
    """Database / storage icon: a cylinder with elliptical caps. (x, y) = bottom-left of the body."""
    lw = lw or _lw(0.8)
    ch = h * cap
    body = Rectangle((x, y + ch / 2), w, h - ch, fc=fc, ec="none", zorder=zorder)
    ax.add_patch(body)
    if GRADIENT_FILLS:
        gradient_image(ax, (x, x + w, y, y + h), [_mix(fc, 0.06, "#000000"), _mix(fc, 0.7), _mix(fc, 0.12, "#000000")],
                       direction="right", clip=body, zorder=zorder + 0.01)
    ax.plot([x, x], [y + ch / 2, y + h - ch / 2], color=ec, lw=lw, zorder=zorder + 0.2)
    ax.plot([x + w, x + w], [y + ch / 2, y + h - ch / 2], color=ec, lw=lw, zorder=zorder + 0.2)
    ax.add_patch(Ellipse((x + w / 2, y + ch / 2), w, ch, fc=fc, ec=ec, lw=lw, zorder=zorder - 0.1))
    ax.add_patch(Rectangle((x, y + ch / 2), w, ch / 2, fc=fc, ec="none", zorder=zorder))
    ax.add_patch(Ellipse((x + w / 2, y + h - ch / 2), w, ch, fc=lighten(fc, 0.3), ec=ec, lw=lw, zorder=zorder + 0.3))
    if text:
        ax.text(x + w / 2, y + (h - ch) / 2, text, ha="center", va="center", fontsize=fontsize or _fs(1.0),
                zorder=zorder + 0.5, linespacing=1.1)
    return Box(x, y, w, h)


def circle_node(ax, x, y, r=1.6, text=None, fc="white", ec="0.3", lw=None, fontsize=None, zorder=3):
    """Circle node (junction, merge point, state). Returns a Box around it for anchors."""
    c = Circle((x, y), r, fc=fc, ec=ec, lw=lw or _lw(0.8), zorder=zorder)
    ax.add_patch(c)
    if fc not in ("white", "w", "#FFFFFF", "none"):
        _grad_fill(ax, c, fc, top=0.6)
    if text:
        ax.text(x, y, text, ha="center", va="center", fontsize=fontsize or _fs(1.0), zorder=zorder + 1)
    return Box(x - r, y - r, 2 * r, 2 * r)


def plus_node(ax, x, y, r=1.0, ec="0.3", lw=None, zorder=4):
    """Small circled plus (residual addition / sum junction)."""
    circle_node(ax, x, y, r, ec=ec, lw=lw, zorder=zorder)
    k = r * 0.55
    ax.plot([x - k, x + k], [y, y], color=ec, lw=lw or _lw(0.7), zorder=zorder + 1)
    ax.plot([x, x], [y - k, y + k], color=ec, lw=lw or _lw(0.7), zorder=zorder + 1)
    return Box(x - r, y - r, 2 * r, 2 * r)


def route(ax, points, color=LINE, lw=None, dashed=False, arrow_end=True, head=4.5, radius=0.0, zorder=3,
          label_text=None, label_at=0.5, label_side="below", label_color=None):
    """Orthogonal connector through *points* (mm) with optional dashed style, rounded corners (radius, mm),
    arrow head and a label on its longest segment (feedback loops such as 'Repeat for 5 rounds')."""
    pts = np.asarray(points, float)
    if radius > 0 and len(pts) > 2:
        verts, codes = [tuple(pts[0])], [MPath.MOVETO]
        for i in range(1, len(pts) - 1):
            p0, p1, p2 = pts[i - 1], pts[i], pts[i + 1]
            d0 = (p1 - p0) / max(np.linalg.norm(p1 - p0), 1e-9); d1 = (p2 - p1) / max(np.linalg.norm(p2 - p1), 1e-9)
            verts += [tuple(p1 - d0 * radius), tuple(p1), tuple(p1 + d1 * radius)]
            codes += [MPath.LINETO, MPath.CURVE3, MPath.CURVE3]
        stop = pts[-1] if not arrow_end else pts[-1] - (pts[-1] - pts[-2]) / max(np.linalg.norm(pts[-1] - pts[-2]), 1e-9) * 0.01
        verts.append(tuple(stop)); codes.append(MPath.LINETO)
        ax.add_patch(PathPatch(MPath(verts, codes), fc="none", ec=color, lw=lw or _lw(0.8),
                               ls=(0, (2.5, 1.5)) if dashed else "-", zorder=zorder))
        if arrow_end:
            arrow(ax, tuple(pts[-2] + (pts[-1] - pts[-2]) * 0.6), tuple(pts[-1]), color=color, lw=lw or _lw(0.8),
                  head=head, shrink=0, zorder=zorder)
    else:
        elbow(ax, pts, color=color, lw=lw, dashed=dashed, head=head, arrow_end=arrow_end, zorder=zorder)
    if label_text:
        segs = [(np.linalg.norm(pts[i + 1] - pts[i]), i) for i in range(len(pts) - 1)]
        _, i = max(segs)
        p = pts[i] + (pts[i + 1] - pts[i]) * label_at
        horiz = abs(pts[i + 1][1] - pts[i][1]) < 1e-9
        off = {"below": (0, -0.8), "above": (0, 0.8), "left": (-0.8, 0), "right": (0.8, 0)}[label_side]
        ax.text(p[0] + off[0], p[1] + off[1], label_text, fontsize=_fs(1.0), color=label_color or color,
                ha="center" if horiz else ("right" if label_side == "left" else "left"),
                va=("top" if label_side == "below" else "bottom") if horiz else "center", zorder=zorder + 1)


def chevrons(ax, x, y, w, h, labels, colors=None, tip=2.0, gap=0.6, fontsize=None, text_color="0.1"):
    """Row of chevron arrows for ordered stages (first one flat on the left). colors: list of fills."""
    n = len(labels)
    colors = colors or [PASTEL[k][0] for k in ("blue", "green", "orange", "purple", "rose", "teal")][:n]
    cw = (w - gap * (n - 1)) / n
    out = []
    for i, (lab, c) in enumerate(zip(labels, colors)):
        x0 = x + i * (cw + gap)
        notch = 0 if i == 0 else tip
        pts = [(x0, y), (x0 + cw, y), (x0 + cw + tip, y + h / 2), (x0 + cw, y + h), (x0, y + h),
               (x0 + notch, y + h / 2)]
        pg = Polygon(pts, closed=True, fc=c, ec="none", zorder=2)
        ax.add_patch(pg)
        if GRADIENT_FILLS:
            gradient_image(ax, (x0, x0 + cw + tip, y, y + h), [_mix(c, 0.10, "#000000"), _mix(c, 0.55)],
                           direction="up", clip=pg, zorder=2.01)
        ax.text(x0 + (cw + notch) / 2 + tip * 0.25, y + h / 2, lab, ha="center", va="center",
                fontsize=fontsize or _fs(1.0), color=text_color, zorder=3, linespacing=1.1)
        out.append(Box(x0, y, cw + tip, h))
    return out


def cycle_diagram(ax, cx, cy, R, labels, colors=None, node_r=None, arc_color="0.35", start=90.0, fontsize=None,
                  text_r=None, clockwise=True, node_text=None):
    """Circular process: n nodes on a circle joined by curved arrows (iterative loops, life cycles).
    node_text: optional short text inside each node (e.g. step numbers); labels sit outside the circle."""
    n = len(labels)
    colors = colors or [PASTEL[k][1] for k in ("blue", "green", "orange", "purple", "rose", "teal")][:n]
    node_r = node_r or R * 0.22
    sgn = -1 if clockwise else 1
    angs = np.deg2rad(start + sgn * 360.0 * np.arange(n) / n)
    P = np.c_[cx + R * np.cos(angs), cy + R * np.sin(angs)]
    for i in range(n):
        a0, a1 = angs[i], angs[(i + 1) % n]
        if clockwise and a1 > a0:
            a1 -= 2 * np.pi
        if not clockwise and a1 < a0:
            a1 += 2 * np.pi
        da = node_r / R * 1.35
        t = np.linspace(a0 + sgn * da, a1 - sgn * da, 40)
        xs, ys = cx + R * np.cos(t), cy + R * np.sin(t)
        ax.plot(xs[:-1], ys[:-1], color=arc_color, lw=_lw(0.9), zorder=2)
        arrow(ax, (xs[-3], ys[-3]), (xs[-1], ys[-1]), color=arc_color, lw=_lw(0.9), head=4.5, shrink=0)
    tr = text_r or R + node_r + 2.2
    for i, (p, lab, c) in enumerate(zip(P, labels, colors)):
        cc = Circle(p, node_r, fc=lighten(c, 0.55), ec=c, lw=_lw(1.0), zorder=3)
        ax.add_patch(cc)
        _grad_fill(ax, cc, lighten(c, 0.35), top=0.75)
        if node_text:
            ax.text(*p, node_text[i], ha="center", va="center", fontsize=_fs(1.1), zorder=4)
        a = angs[i]
        ha = "center" if abs(np.cos(a)) < 0.3 else ("left" if np.cos(a) > 0 else "right")
        va = "center" if abs(np.sin(a)) < 0.3 else ("bottom" if np.sin(a) > 0 else "top")
        ax.text(cx + tr * np.cos(a), cy + tr * np.sin(a), lab, ha=ha, va=va, fontsize=fontsize or _fs(1.0),
                linespacing=1.1)
    return P


def icon_graph(ax, x, y, s=4.0, color="#7A5BA8", seed=2, n=5, node_r=None, edge="0.35"):
    """Tiny node-link icon (graph / molecule / network input) in a square of side s at (x, y)."""
    rng = np.random.default_rng(seed)
    ang = np.sort(rng.uniform(0, 2 * np.pi, n))
    rr = s * (0.28 + 0.14 * rng.random(n))
    P = np.c_[x + s / 2 + rr * np.cos(ang), y + s / 2 + rr * np.sin(ang)]
    for i in range(n):
        j = (i + 1) % n
        ax.plot([P[i, 0], P[j, 0]], [P[i, 1], P[j, 1]], color=edge, lw=_lw(0.6), zorder=3)
    ax.plot([P[0, 0], P[2, 0]], [P[0, 1], P[2, 1]], color=edge, lw=_lw(0.6), zorder=3)
    r = node_r or s * 0.09
    cols = [color, lighten(color, 0.45), darken(color, 0.15)]
    for i, p in enumerate(P):
        ax.add_patch(Circle(p, r, fc=cols[i % 3], ec="white", lw=_lw(0.3), zorder=4))
    return Box(x, y, s, s)


def icon_stack(ax, x, y, w, h, n=3, fc="white", ec="0.45", dx=0.7, dy=0.7, lines=3):
    """Stack of pages / samples / frames (front page bottom-left at (x, y))."""
    for k in range(n - 1, -1, -1):
        ax.add_patch(Rectangle((x + k * dx, y + k * dy), w, h, fc=fc, ec=ec, lw=_lw(0.6), zorder=3 + (n - k)))
    for j in range(lines):
        yy = y + h * (0.72 - j * 0.2)
        ax.plot([x + w * 0.15, x + w * (0.85 if j < lines - 1 else 0.55)], [yy, yy], color="0.6", lw=_lw(0.6),
                zorder=3 + n + 1)
    return Box(x, y, w + (n - 1) * dx, h + (n - 1) * dy)


def icon_bars(ax, x, y, w, h, values=(0.45, 0.8, 0.6, 1.0), colors=None, baseline=True):
    """Miniature bar chart icon (results / scores)."""
    v = np.asarray(values, float) / max(values)
    n = len(v)
    colors = colors or ["#9DBCDD"] * (n - 1) + ["#3A6EA5"]
    bw = w / (n * 1.4)
    for i, (vi, c) in enumerate(zip(v, colors)):
        rb = Rectangle((x + i * bw * 1.4 + bw * 0.2, y), bw, vi * h, fc=c, ec="none", zorder=3)
        ax.add_patch(rb)
        if GRADIENT_FILLS:
            gradient_image(ax, (rb.get_x(), rb.get_x() + bw, y, y + vi * h), [_mix(c, 0.6), mcolors.to_rgba(c)],
                           clip=rb, zorder=3.01)
    if baseline:
        ax.plot([x, x + w], [y, y], color="0.3", lw=_lw(0.6), zorder=4)
    return Box(x, y, w, h)


def icon_person(ax, x, y, h=5.0, color="#7C9CC6"):
    """Simple person glyph (participants, cohorts): head + rounded body, feet at (x, y)."""
    r = h * 0.17
    ax.add_patch(Circle((x, y + h - r), r, fc=color, ec="none", zorder=3))
    body = FancyBboxPatch((x - h * 0.22, y), h * 0.44, h * 0.56, boxstyle=f"round,pad=0,rounding_size={h * 0.18}",
                          fc=color, ec="none", zorder=3)
    ax.add_patch(body)
    return Box(x - h * 0.22, y, h * 0.44, h)


def icon_cells(ax, x, y, w, h, n=14, color="#6FAAA3", seed=4, r=None):
    """Field of round 'cells' / particles / samples inside a rounded dish outline."""
    rng = np.random.default_rng(seed)
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={min(w, h) * 0.2}",
                                fc="white", ec="0.5", lw=_lw(0.6), zorder=2))
    r = r or min(w, h) * 0.07
    pts = []
    tries = 0
    while len(pts) < n and tries < 2000:
        p = (x + r * 1.6 + rng.random() * (w - 3.2 * r), y + r * 1.6 + rng.random() * (h - 3.2 * r))
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > (2.2 * r) ** 2 for q in pts):
            pts.append(p)
        tries += 1
    for p in pts:
        ax.add_patch(Circle(p, r, fc=lighten(color, 0.35), ec=color, lw=_lw(0.5), zorder=3))
    return Box(x, y, w, h)


def timeline(ax, x0, x1, y, ticks, labels=None, color="0.25", tick_h=0.8, fontsize=None, above=False):
    """Horizontal time axis with ticks at *ticks* (mm) and labels below (or above)."""
    ax.plot([x0, x1], [y, y], color=color, lw=_lw(0.9), zorder=2)
    arrow(ax, (x1 - 1.5, y), (x1 + 0.5, y), color=color, lw=_lw(0.9), head=4, shrink=0)
    for i, t in enumerate(ticks):
        ax.plot([t, t], [y - tick_h / 2, y + tick_h / 2], color=color, lw=_lw(0.8), zorder=2)
        if labels:
            ax.text(t, y + (tick_h if above else -tick_h), labels[i], ha="center", va="bottom" if above else "top",
                    fontsize=fontsize or _fs(0.95), color="0.15")
