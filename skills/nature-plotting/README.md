# nature-plotting 模板库

Nature 系列期刊风格的 matplotlib 绘图模板。共 53 个模板，覆盖常见数据图表、Nature 风格色条和简单概念图。
图里的数据全部是虚拟的（Data 1、Data 2、Group A……），换成自己的数据即可。

## 用法

```bash
python templates/L01_regime_lines.py          # 运行单个模板，输出到 ./figure_preview/（PNG 600 dpi + PDF）
python scripts/render_gallery.py              # 重新生成本页全部预览图
python scripts/audit_layout.py fig.pdf        # 检查 PDF：尺寸、字体、字号、面板字母、对齐、分辨率
```

1. 按要回答的问题选模板（见下表或 `references/chart-chooser.md`）。
2. 复制模板，只替换 `MOCK DATA` 这一段数据，其余保持不变。
3. 运行，打开 PNG 逐个面板检查，再跑 `audit_layout.py`。

模块：`assets/nature_style.py`（样式、尺寸、导出）、`assets/nature_charts.py`（图表构件）、
`assets/nature_cmaps.py`（色图、配色、色条）、`assets/nature_schematic.py`（示意图元件）。

规范：单栏 89 mm，双栏 183 mm，高度 ≤ 170 mm；Arial 5–7 pt；刻度朝内、四边、无网格；
避免彩虹色图和红绿对比。详见 `references/nature-rules.md`。

## 折线与趋势

| **L01_regime_lines**<br>两条曲线 + 失效区渐变 + 阈值线 + 双单位横轴 | **L02_sigmoid_fit**<br>S 形拟合、阈值交点、两曲线平移量（双箭头） |
|---|---|
| ![L01_regime_lines](gallery/L01_regime_lines.png) | ![L02_sigmoid_fit](gallery/L02_sigmoid_fit.png) |

| **L03_hue_lines**<br>按连续参数着色的曲线族 + 色条 + 检出下限渐变区 | **L04_loglog_powerlaw**<br>双对数幂律参考线；排序谱与截断点标注 |
|---|---|
| ![L03_hue_lines](gallery/L03_hue_lines.png) | ![L04_loglog_powerlaw](gallery/L04_loglog_powerlaw.png) |

| **L05_ci_band**<br>多方法 vs 条件，5–95 % 区间带、外推虚线、特殊标记 | **L06_dual_axis**<br>左右双 y 轴，轴色与曲线色一致 |
|---|---|
| ![L05_ci_band](gallery/L05_ci_band.png) | ![L06_dual_axis](gallery/L06_dual_axis.png) |

| **L07_broken_windows**<br>断轴：多个窄窗口并排，// 断点标记 | **L08_inset_zoom**<br>全局 + 局部放大插图 + 宽度双箭头 |
|---|---|
| ![L07_broken_windows](gallery/L07_broken_windows.png) | ![L08_inset_zoom](gallery/L08_inset_zoom.png) |

| **L09_step_series**<br>阶梯曲线（设定值/搜索过程），上下共享时间轴 | **L10_stacked_metrics**<br>多个指标共享 x 轴纵向堆叠 |
|---|---|
| ![L09_step_series](gallery/L09_step_series.png) | ![L10_stacked_metrics](gallery/L10_stacked_metrics.png) |

## 曲线组与剖面

| **P01_small_multiples**<br>3×3 小多图，共用坐标标签，面板内标注 | **P02_offset_curves**<br>偏移堆叠曲线 + 共同特征虚线 |
|---|---|
| ![P01_small_multiples](gallery/P01_small_multiples.png) | ![P02_offset_curves](gallery/P02_offset_curves.png) |

| **P03_uncertainty_bands**<br>均值 ± σ 不确定度带，三种条件 | **P04_difference_curves**<br>差值曲线 + 低置信区阴影 |
|---|---|
| ![P03_uncertainty_bands](gallery/P03_uncertainty_bands.png) | ![P04_difference_curves](gallery/P04_difference_curves.png) |

## 比较

| **C01_bar_points**<br>柱状图 + 误差棒 + 每个样本点（小 n） | **C02_grouped_stacked**<br>分组柱状图；100 % 堆叠条形图 |
|---|---|
| ![C01_bar_points](gallery/C01_bar_points.png) | ![C02_grouped_stacked](gallery/C02_grouped_stacked.png) |

| **C03_lollipop_dumbbell**<br>排序棒棒糖图；前后对比哑铃图 | **C04_waterfall_budget**<br>瀑布 / 预算图（增减与总量） |
|---|---|
| ![C03_lollipop_dumbbell](gallery/C03_lollipop_dumbbell.png) | ![C04_waterfall_budget](gallery/C04_waterfall_budget.png) |

| **C05_landscape**<br>文献对比图：形状区分类别、编号不重叠、目标区、This work | **C06_range_rows**<br>对数轴区间图，按行分组，内嵌色条 |
|---|---|
| ![C05_landscape](gallery/C05_landscape.png) | ![C06_range_rows](gallery/C06_range_rows.png) |

| **C07_forest**<br>森林图：效应量与 95 % CI | **C08_radar**<br>雷达图（4–8 个归一化指标） |
|---|---|
| ![C07_forest](gallery/C07_forest.png) | ![C08_radar](gallery/C08_radar.png) |

## 分布

| **D01_box_jitter**<br>箱线图 + 散点 | **D02_raincloud**<br>雨云图：半密度 + IQR + 原始点 |
|---|---|
| ![D01_box_jitter](gallery/D01_box_jitter.png) | ![D02_raincloud](gallery/D02_raincloud.png) |

| **D03_strip_mean_twin**<br>按步骤的散点 + 均值±s.d. + 第二指标双轴 | **D04_hist_kde_ecdf**<br>阶梯直方图 + 核密度；累积分布 ECDF |
|---|---|
| ![D03_strip_mean_twin](gallery/D03_strip_mean_twin.png) | ![D04_hist_kde_ecdf](gallery/D04_hist_kde_ecdf.png) |

| **D05_ridgeline**<br>山脊图：分布随有序因子变化 | **D06_joint_hexbin**<br>六边形密度图 + 边缘直方图 + 对数色条 |
|---|---|
| ![D05_ridgeline](gallery/D05_ridgeline.png) | ![D06_joint_hexbin](gallery/D06_joint_hexbin.png) |

## 关系

| **R01_parity_residual**<br>预测–真值对角图 + 残差子图 + MAE/RMSE/R² | **R02_scatter_color_size**<br>散点：颜色 = 第三变量（色条），大小 = 第四变量 |
|---|---|
| ![R01_parity_residual](gallery/R01_parity_residual.png) | ![R02_scatter_color_size](gallery/R02_scatter_color_size.png) |

| **R03_fit_ci**<br>误差棒 + 拟合线 + 95 % 置信带 + 沿线公式 + 第二单位轴 | **R04_category_scatter**<br>按类别区分形状与颜色的散点 + 超限区 |
|---|---|
| ![R03_fit_ci](gallery/R03_fit_ci.png) | ![R04_category_scatter](gallery/R04_category_scatter.png) |

## 矩阵、二维场与图像

| **M01_heatmap_annotated**<br>白色网格热图 + 对数色条 + 独立汇总行 | **M02_corr_triangle**<br>下三角相关矩阵，中心固定的发散色条 |
|---|---|
| ![M01_heatmap_annotated](gallery/M01_heatmap_annotated.png) | ![M02_corr_triangle](gallery/M02_corr_triangle.png) |

| **M03_confusion**<br>混淆矩阵（行归一化 % + 计数） | **M04_image_plate**<br>图像拼板：黑底、通道标注、比例尺 |
|---|---|
| ![M03_confusion](gallery/M03_confusion.png) | ![M04_image_plate](gallery/M04_image_plate.png) |

| **M05_map_extend**<br>二维图：extend 三角色条、区域标签；对数图 | **M06_contour_sweep**<br>参数扫描等高线 + 约束区 + 最优点 |
|---|---|
| ![M05_map_extend](gallery/M05_map_extend.png) | ![M06_contour_sweep](gallery/M06_contour_sweep.png) |

| **M07_phase_vector**<br>相位图（循环色图）；矢量场流线 | **M08_surface3d**<br>三维曲面 + 底面投影（慎用） |
|---|---|
| ![M07_phase_vector](gallery/M07_phase_vector.png) | ![M08_surface3d](gallery/M08_surface3d.png) |

| **M09_cluster_heatmap**<br>聚类热图 + 双向树状图 | |
|---|---|
| ![M09_cluster_heatmap](gallery/M09_cluster_heatmap.png) | |

## 机器学习

| **N01_training_curves**<br>训练/验证损失（多种子 ± s.d.）+ 选定 epoch | **N02_roc_pr**<br>ROC 与 PR 曲线，AUC / AP |
|---|---|
| ![N01_training_curves](gallery/N01_training_curves.png) | ![N02_roc_pr](gallery/N02_roc_pr.png) |

## 色图、色条与配色

**K01_colormaps** — 全部内置色图及其明度 L* 曲线

![K01_colormaps](gallery/K01_colormaps.png)

**K02_colorbar_styles** — 九种 Nature 风格色条

![K02_colorbar_styles](gallery/K02_colorbar_styles.png)

**K03_palettes_cvd** — 离散配色在色觉缺陷下的模拟

![K03_palettes_cvd](gallery/K03_palettes_cvd.png)

## 示意图与概念图

**S01_flowchart** — 两阶段流程示意图（图标化）

![S01_flowchart](gallery/S01_flowchart.png)

**S02_optical_setup** — 光路 / 实验装置线稿

![S02_optical_setup](gallery/S02_optical_setup.png)

**S03_device_concept** — 结构示意：等轴测 + 截面尺寸 + 俯视图

![S03_device_concept](gallery/S03_device_concept.png)

**S04_network** — 神经网络：全连接 + 卷积块

![S04_network](gallery/S04_network.png)

**S05_concept_sketch** — 定性概念图：权衡、区域图、前后对比

![S05_concept_sketch](gallery/S05_concept_sketch.png)

**S06_process_flow** — 工艺 / 流程步骤截面图

![S06_process_flow](gallery/S06_process_flow.png)

## 组合图

**F01_composite_figure** — 完整双栏组合图（183 mm）：示意 + 5 个数据面板

![F01_composite_figure](gallery/F01_composite_figure.png)
