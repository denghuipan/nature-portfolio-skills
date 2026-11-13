"""Smoke test for the nature-plotting skill: loads the modules through the portable loader, draws one
two-panel figure with mock data, saves PNG + PDF to ./test_output and prints the text-size audit."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "nature-plotting" / "assets"))
import load_nature_style  # noqa: F401  (resolves the plotting folder)

import numpy as np
from nature_style import PALETTE, figsize_2col, panel_label, style_axes, save_fig, active_preset, audit_text
from nature_charts import direct_label, ci_band

OUT = ROOT / "test_output"
x = np.linspace(0, 10, 40)
rng = np.random.default_rng(0)
y1 = np.exp(-x / 4) + rng.normal(0, 0.02, x.size)
y2 = np.exp(-x / 2.5) + rng.normal(0, 0.02, x.size)

import matplotlib.pyplot as plt
fig, (a, b) = plt.subplots(1, 2, figsize=figsize_2col())
for ax in (a, b):
    style_axes(ax)
a.plot(x, y1, color=PALETTE["blue"]); a.plot(x, y2, color=PALETTE["red"])
direct_label(a, 6, y1[24], "Data 1", color=PALETTE["blue"], dy=3, va="bottom")
direct_label(a, 6, y2[24], "Data 2", color=PALETTE["red"], dy=-3, va="top")
a.set_xlabel("Variable x (unit)"); a.set_ylabel("Response (a.u.)"); panel_label(a, "a")
ci_band(b, x, y1 - 0.05, y1 + 0.05, PALETTE["blue"]); b.plot(x, y1, color=PALETTE["blue"])
b.set_xlabel("Variable x (unit)"); b.set_ylabel("Response (a.u.)"); panel_label(b, "b")
fig.tight_layout()
audit_text(fig)
save_fig(fig, "smoke_test", outdir=OUT)
print("plotting_dir:", load_nature_style.resolve_plotting_dir())
print("preset:", active_preset())
print("saved:", OUT / "smoke_test.png")
