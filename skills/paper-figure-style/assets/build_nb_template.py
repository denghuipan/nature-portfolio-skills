"""
Builder-script template for producing an analysis notebook in the house style.

The builder is the source of truth. Never hand-edit the generated .ipynb —
edit this script and rebuild.

Cycle:
    python build_nb.py                    # assemble the .ipynb
    python -c "<execute snippet below>"   # run it with nbclient
    <Read the rendered PNGs and look at them>
    <fix here, repeat>
"""
from pathlib import Path

import nbformat as nbf

OUT = Path(r"...\your_analysis.ipynb")

nb = nbf.v4.new_notebook()
C = []
md = lambda s: C.append(nbf.v4.new_markdown_cell(s))      # noqa: E731
co = lambda s: C.append(nbf.v4.new_code_cell(s))          # noqa: E731


# ------------------------------------------------------------------ title
md(r"""# <标题>

> 一句话说明这份 notebook 回答什么问题、方法沿用哪份既有分析。

| 项 | 值 |
|---|---|
| 数据 | ... |
| 参数 | ... |

产出：`figX_...`（Nature 风格，PNG 600 dpi + PDF 矢量）、`*.csv`、`*_summary.md`。""")


# ------------------------------------------------------------------ setup
md("## 0. 配置")

co(r'''%matplotlib inline
from __future__ import annotations

import csv
import sys
import time
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

# 从任意 cwd 启动都能定位数据
HERE = Path.cwd()
if not (HERE / "<anchor_file>").exists():
    cand = Path(r"<absolute fallback dir>")
    if (cand / "<anchor_file>").exists():
        HERE = cand

# ---- 房屋样式：load_nature_style（见 nature-portfolio-skills） ----
ASSETS = Path.home() / ".cursor" / "skills" / "nature-plotting" / "assets"
if not (ASSETS / "load_nature_style.py").is_file():
    raise FileNotFoundError("Run nature-portfolio install.ps1 or set NATURE_PLOTTING_DIR")
sys.path.insert(0, str(ASSETS))
import load_nature_style  # noqa: F401
from nature_style import *  # noqa: F401,F403

_mock = Path("figure_mock")           # 模块 import 时的副作用，清理掉
if _mock.exists() and not any(_mock.iterdir()):
    _mock.rmdir()

FIGSIZE_1COL = (4.3, 3.2)
FIGSIZE_2COL = (7.0, 2.9)


def save_fig(fig, name):
    """PNG 600 dpi + PDF 矢量，两份都要。"""
    fig.savefig(HERE / (name + ".png"), dpi=600, bbox_inches="tight")
    fig.savefig(HERE / (name + ".pdf"), bbox_inches="tight")


print("HERE:", HERE)''')


# ------------------------------------------------------------------ load
md("## 1. 载入数据")
co(r'''# 载入，并把关键参数打印出来核对
...''')


# ------------------------------------------------------------------ compute
md("## 2. 计算")
co(r'''# 重活缓存到 .npz，重跑样式时不要重新解析原始数据
CACHE = HERE / "<name>_cache.npz"
if CACHE.exists():
    z = np.load(CACHE)
    ...
else:
    ...
    np.savez_compressed(CACHE, ...)''')


# ------------------------------------------------------------------ figure
md("## 3. 图 1 — <说明这张图证明什么>")

co(r'''fig, ax = plt.subplots(figsize=FIGSIZE_1COL)

# 参考线先画（压在数据下面），数据后画
ax.axhline(<ref>, color="0.65", ls=":", lw=1.2)
ax.plot(x, y_main, "-", lw=1.8, color=PALETTE["blue"], label="<main>")
ax.plot(x, y_alt, "-", lw=1.2, color=PALETTE["red"], alpha=0.9, label="<alt>")

ax.set_xlabel(r"<x> (unit)")
ax.set_ylabel(r"<y>")
ax.set_title("<short English title>", fontsize=10)
ax.set_ylim(<lo>, <hi>)          # 显式留出图例余量，别让峰顶顶到图例
ax.text(0.03, 0.95, "<key number>", transform=ax.transAxes, fontsize=7, va="top")
ax.legend(fontsize=7, loc="lower right", handlelength=1.8, labelspacing=0.3)
style_axes(ax)
save_fig(fig, "figX_<name>")
plt.show()''')


# ---- 两联图：panel label a/b ----
co(r'''fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGSIZE_2COL)

# ... ax1 ...
panel_label(ax1, "a", dx=-0.20, dy=1.08, size=11)
style_axes(ax1)

# ... ax2 ...
panel_label(ax2, "b", dx=-0.22, dy=1.08, size=11)
style_axes(ax2)

fig.tight_layout()
save_fig(fig, "figY_<name>")
plt.show()''')


# ------------------------------------------------------------------ export
md("## 4. 导出")
co(r'''# 曲线存 csv，所有数字汇总成 md，便于引用时不必重跑
...''')


# ------------------------------------------------------------------ write
nb["cells"] = C
nb.metadata.update({
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.12.10"},
})
OUT.parent.mkdir(parents=True, exist_ok=True)
nbf.write(nb, OUT)
print("wrote", OUT, f"({len(C)} cells)")


# ======================================================================
# 执行片段（在 notebook 所在目录运行）：
#
# import nbformat
# from nbclient import NotebookClient
# nb = nbformat.read("your_analysis.ipynb", as_version=4)
# NotebookClient(nb, timeout=1800, kernel_name="python3",
#                resources={"metadata": {"path": "."}}).execute()
# nbformat.write(nb, "your_analysis.ipynb")
# print("errors:", sum(1 for c in nb.cells for o in c.get("outputs", [])
#                      if o.output_type == "error"))
#
# 然后用 Read 工具逐张打开生成的 PNG 看一遍。这一步不能跳。
# ======================================================================
