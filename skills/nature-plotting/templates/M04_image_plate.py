"""M04 -- Image plate: rows = samples, columns = channels / time points, on a dark background.
Use when: microscopy, camera frames or field maps that are compared side by side.
Nature notes: black only behind the images; identical crop, scale and display range per column; white scale
bar (not a magnification); labels written on the plate; one colour bar per display range, with end labels
when the scale is normalised.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, PALETTE, figsize_*, panel_label, style_axes
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(54)
def blobs(n, size=96, seed=0):
    r = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:size, 0:size]
    img = np.zeros((size, size))
    for _ in range(n):
        cx, cy, s = r.uniform(10, size - 10), r.uniform(10, size - 10), r.uniform(2, 6)
        img += r.uniform(0.4, 1) * np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * s ** 2))
    return img + 0.05 * r.random((size, size))
rows = ["Sample A", "Sample B"]
cols = ["Channel 1", "Channel 2", "Merged"]
images = [[blobs(25, seed=10 * i + j) for j in range(2)] for i in range(2)]
um_per_px = 0.25
# -------------------------------------------

fig, axes = plt.subplots(2, 3, figsize=figsize_mm(89, 62), gridspec_kw=dict(wspace=0.04, hspace=0.04))
fig.patch.set_facecolor("white")
c1, c2 = np.array([0.0, 0.85, 0.95]), np.array([0.95, 0.2, 0.75])   # cyan / magenta (colour-blind safe pair)
for i in range(2):
    a, b = images[i]
    a, b = a / a.max(), b / b.max()
    rgb1 = a[..., None] * c1; rgb2 = b[..., None] * c2
    for j, img in enumerate([rgb1, rgb2, np.clip(rgb1 + rgb2, 0, 1)]):
        ax = axes[i, j]
        ax.imshow(img, extent=(0, 96 * um_per_px, 0, 96 * um_per_px), origin="lower")
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
        if i == 0:
            ax.text(0.04, 0.96, cols[j], transform=ax.transAxes, color="w", ha="left", va="top", fontsize=5.5)
        if j == 0:
            ax.text(0.04, 0.04, rows[i], transform=ax.transAxes, color="w", ha="left", va="bottom", fontsize=5.5)
scale_bar(axes[1, 2], 5, "5 µm", loc="lower right", color="w", lw=1.4)
export(fig, "M04_image_plate")
