"""Quick visual test for nature_style np_final preset."""
import sys
from pathlib import Path

PLOTTING = Path(r"D:\OneDrive\UCSC\Paper\End-facet\plotting")
sys.path.insert(0, str(PLOTTING))
import matplotlib.pyplot as plt
from nature_style import (
    PALETTE,
    TBL,
    figsize_2col,
    panel_label,
    style_axes,
    save_fig,
    active_preset,
)

OUT = Path(__file__).resolve().parent.parent / "test_output"
OUT.mkdir(exist_ok=True)

wl = TBL["wl"]
eta = TBL["eta_sys"]
mae = TBL["mae_20f"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize_2col())
for ax in (ax1, ax2):
    style_axes(ax)

ax1.plot(wl, eta, "o-", color=PALETTE["blue"], lw=1.5, ms=4, markeredgecolor="white", markeredgewidth=0.5)
ax1.set_xlabel("Wavelength (nm)")
ax1.set_ylabel(r"System efficiency $\eta_{\mathrm{sys}}$ (%)")
ax1.set_xlim(480, 870)
panel_label(ax1, "a")

ax2.plot(wl, mae, "s-", color=PALETTE["green"], lw=1.5, ms=4, markeredgecolor="white", markeredgewidth=0.5)
ax2.axhline(0.1, color="0.65", ls="--", lw=1.0, label="0.1 nm guide")
ax2.set_xlabel("Wavelength (nm)")
ax2.set_ylabel("MAE (nm, 20-frame avg)")
ax2.set_xlim(480, 870)
ax2.legend(loc="upper right")
panel_label(ax2, "b")

fig.suptitle("Nature style test (End-facet TBL)", fontsize=7, y=1.02)
fig.tight_layout()
save_fig(fig, "np_final_test", outdir=OUT)
print("preset:", active_preset())
print("saved:", OUT / "np_final_test.png")
