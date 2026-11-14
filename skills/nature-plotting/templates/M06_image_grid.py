"""M06 -- Image grid: conditions in rows, channels in columns, a merge column, a scale bar and a zoom inset.
Use when: micrographs / camera frames / maps from several conditions and channels are compared; every
panel must share the same intensity scale per channel (state it).
Look: no axes, thin white gutters, channel names over the columns in the channel colour, condition names
at the left, grey single channels with a green-magenta merge (colour-blind safe), scale bar in white,
dashed zoom box with its enlargement in the last column.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
from scipy.ndimage import gaussian_filter

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(83)
N = 200


def blobs(n, sigma, seed):
    r = np.random.default_rng(seed)
    im = np.zeros((N, N))
    im[r.integers(0, N, n), r.integers(0, N, n)] = r.uniform(0.5, 1.0, n)
    im = gaussian_filter(im, sigma)
    return im / im.max()


conds = ["Condition 1", "Condition 2"]
ch1 = [blobs(60, 4, 1), blobs(120, 4, 2)]                       # channel 1 (e.g. a structure)
ch2 = [0.6 * ch1[0] + 0.4 * blobs(40, 5, 3), 0.15 * ch1[1] + 0.85 * blobs(80, 5, 4)]
ch2 = [c / c.max() for c in ch2]
zoom = (110, 160, 60, 110)                                      # x0, x1, y0, y1 in pixels
px_um = 0.1                                                    # micrometres per pixel
# -------------------------------------------
green = np.array(mcolors.to_rgb("#3FBF5F")); magenta = np.array(mcolors.to_rgb("#D24BD2"))
fig, axs = plt.subplots(2, 4, figsize=figsize_mm(120, 64))
fig.subplots_adjust(left=0.08, right=0.995, top=0.9, bottom=0.01, wspace=0.03, hspace=0.04)
for r in range(2):
    a, b = ch1[r], ch2[r]
    merge = np.clip(a[..., None] * green + b[..., None] * magenta, 0, 1)
    x0, x1, y0, y1 = zoom
    imgs = [(a, "gray"), (b, "gray"), (merge, None), (merge[y0:y1, x0:x1], None)]
    for c, (img, cm) in enumerate(imgs):
        ax = axs[r, c]
        ax.imshow(img, cmap=cm, vmin=0, vmax=1, interpolation="bilinear")
        ax.set_xticks([]); ax.set_yticks([])
    axs[r, 2].add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, ec="white", lw=0.6, ls=(0, (2, 1.5))))
    axs[r, 0].set_ylabel(conds[r])
    scale_bar(axs[r, 2], 5 / px_um, "5 µm", loc="lower right", color="w")
    scale_bar(axs[r, 3], 1 / px_um, "1 µm", loc="lower right", color="w")
for c, (t, col) in enumerate([("Channel 1", "#2E8F47"), ("Channel 2", "#A83AA8"), ("Merge", "0.1"), ("Zoom", "0.1")]):
    axs[0, c].set_title(t, color=col, pad=3)
export(fig, "M06_image_grid")
