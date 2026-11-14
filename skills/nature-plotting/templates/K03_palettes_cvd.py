"""K03 -- Categorical palettes as seen with normal vision and the three colour-vision deficiencies.
Use when: picking series colours. If two colours merge in a CVD column, give the series different marker
shapes or line styles as well, or pick another pair.
Look: one row per palette, four columns (normal, deuteranopia, protanopia, tritanopia), square swatches.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels

# ---------------- MOCK DATA ----------------
palettes = {"EDITORIAL": EDITORIAL, "HOUSE_DARK": HOUSE_DARK, "OKABE_ITO": OKABE_ITO,
            "PAIRED": [c for pair in PAIRED for c in pair][:8], "THEMES['soft']": THEMES["soft"],
            "THEMES['fan']": THEMES["fan"], "THEMES['signal']": THEMES["signal"],
            "THEMES['updown']": THEMES["updown"], "THEMES['earth']": THEMES["earth"], "GRAYS": GRAYS}
kinds = [(None, "Normal"), ("deutan", "Deuteranopia"), ("protan", "Protanopia"), ("tritan", "Tritanopia")]
# -------------------------------------------
fig, axs = plt.subplots(len(palettes), 4, figsize=figsize_2col(92))
fig.subplots_adjust(left=0.13, right=0.99, top=0.95, bottom=0.02, wspace=0.08, hspace=0.35)
for r, (nm, pal) in enumerate(palettes.items()):
    rgb = np.array([mcolors.to_rgb(c) for c in pal])
    for k, (kind, title) in enumerate(kinds):
        ax = axs[r, k]
        img = rgb if kind is None else simulate_cvd(rgb, kind)
        ax.imshow(img[None, :, :], aspect="auto", extent=(0, len(pal), 0, 1))
        for i in range(1, len(pal)):
            ax.axvline(i, color="white", lw=1.2)
        ax.set_xlim(0, len(pal)); ax.set_xticks([]); ax.set_yticks([])
        if r == 0:
            ax.set_title(title, pad=3)
    axs[r, 0].text(-0.03, 0.5, nm, transform=axs[r, 0].transAxes, ha="right", va="center")
export(fig, "K03_palettes_cvd")
