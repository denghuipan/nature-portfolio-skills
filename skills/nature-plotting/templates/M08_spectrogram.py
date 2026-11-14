"""M08 -- Time-frequency map under its raw trace, with an event marker and a log-power colour bar.
Use when: a signal's spectral content changes over time (vibration, neural recordings, audio, sensor
streams) and a transient event must be located in both views.
Look: trace without frame above (scale bars), map with open axes and log frequency, sequential dark-to-
light map (dark = low power), colour bar glued to the right in dB, event as a dashed line through both.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_style import *      # noqa: F401,F403  rcParams, palettes, sizes, set_look, panel_label
from nature_cmaps import *      # noqa: F401,F403  NS_* colour maps, palettes, colour-bar helpers
from nature_charts import *     # noqa: F401,F403  chart builders, export()
use_arial_math()                # maths ($x$, $\mu$) in the same sans face as the labels
from scipy.signal import spectrogram, chirp

# ---------------- MOCK DATA ----------------
rng = np.random.default_rng(97)
fs = 1000.0
t = np.arange(0, 10, 1 / fs)
sig = 0.6 * np.sin(2 * np.pi * 8 * t) + 0.4 * chirp(t, 20, 10, 140) + 0.3 * rng.normal(0, 1, t.size)
burst = (t > 6.0) & (t < 6.6)
sig[burst] += 1.2 * np.sin(2 * np.pi * 60 * t[burst])
event = 6.0
# -------------------------------------------
f, tt, S = spectrogram(sig, fs, nperseg=512, noverlap=448)
fig = plt.figure(figsize=figsize_mm(110, 68))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 2.6], hspace=0.16, left=0.1, right=0.88, top=0.97, bottom=0.14)
a0 = fig.add_subplot(gs[0]); a1 = fig.add_subplot(gs[1], sharex=a0)
a0.plot(t, sig, color=PALETTE["ink"], lw=0.3); a0.axis("off"); a0.set_xlim(0, 10)
a0.axvline(event, color=PALETTE["brick"], lw=0.6, ls=(0, (3, 2)))
a0.plot([0.1, 1.1], [-2.6, -2.6], color="0.1", lw=1.0); a0.text(0.6, -2.8, "1 s", ha="center", va="top", fontsize=6)
P = 10 * np.log10(S + 1e-12)
m = (f >= 2) & (f <= 300)
pm = a1.pcolormesh(tt, f[m], P[m], cmap=NS_EMBER, vmin=np.percentile(P[m], 5), vmax=np.percentile(P[m], 99.5),
                   shading="gouraud", rasterized=True)
a1.set_yscale("log"); a1.set_ylim(2, 300)
a1.set_yticks([3, 10, 30, 100, 300], ["3", "10", "30", "100", "300"]); a1.yaxis.set_minor_locator(mticker.NullLocator())
a1.axvline(event, color="white", lw=0.6, ls=(0, (3, 2)))
a1.text(event + 0.1, 220, "Event", color="white", fontsize=6, va="top")
a1.set_xlabel("Time (s)"); a1.set_ylabel("Frequency (Hz)")
cbar_side(a1, pm, "Power (dB)", size="2.5%", pad=0.06)
export(fig, "M08_spectrogram")
