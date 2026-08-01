# 分离过程图解法画图库用法

**这文件给谁看**：做分离过程 / 单元操作课（作者这边是 CME214 单元操作 II）的题要画图时，AI 和我自己照着喂数据。
**解决什么问题**：三元相图 / 阶梯法 / 干燥曲线这几种图，AI 临时画又慢又错，这里有测好的函数直接用。

库在 `scripts/chemeng_plots.py`，跑通验证 + 参考图在 `scripts/examples_cme214.py`（`python examples_cme214.py` 一跑就出 6 张样图在 `figures/`）。

> 下面每个函数末尾的"对应：T01 Q4"、"L02 §[C2]"是作者自己课程的题号和讲义节号（T=tutorial，L=lecture），只是告诉你这函数当初为哪类题写的。换成你的课直接忽略这些编号，看"喂什么、出什么"就够。

---

## 怎么引入

```python
import sys
sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/skills/homework-coach/scripts')
from chemeng_plots import plot_ternary, plot_drying_curve, coords_table  # 按需引
```

每个函数都返回 `(fig, ax, result)`。`result` 是字典，里面：
- `result["coords"]` —— **画图坐标**（誊方格纸 / 三角网格纸 / 核对用），`print(coords_table(result))` 打成表
- 各函数额外的算出值（级数 / 积分 / 斜率，见下）

画完照常 `fig.savefig('figures/xxx.png')` + Read 一眼自查。

**所有图都自带浅网格**：XY 图是淡方格，三元图是 10% 间隔的浅三角网格（对应你打印的三角网格纸）。

---

## 5 个函数：喂什么、出什么

### 1. `plot_ternary(raffinate, extract, ...)` — 三元相图（LLE）
- **喂**：两组平衡点。`raffinate` = 萃余相（水层）列表，`extract` = 萃取相（溶剂层）列表，**一一对应**（同一行 = 一条 tie line）。每个点写成 `(溶质, 载体, 溶剂)`，传 wt% 或分数都行（内部自动归一）。
- **出**：等边三角形 + binodal 曲线 + tie line + plait point 星标。
- **可选**：`mix=(a,b,c)` 标混合点 M；`FS=((F点),(S点))` 画 F-S 杠杆线；`labels=(顶点名,左下名,右下名)`。
- 对应：T01 Q1/Q2/Q7、T02 Q2。

### 2. `plot_distribution(x_raff, y_ext, ...)` — 分配曲线
- **喂**：两个等长数组，`x_raff` = 溶质在萃余相含量，`y_ext` = 在萃取相含量。
- **出**：y vs x 曲线 + `y=x` 参考线。曲线在 y=x 上方 = K>1（好），下方 = K<1（差）。
- **可选**：`op_point=(x,y)` 标一个工作点。
- 对应：T01 Q4/Q5。

### 3. `plot_mccabe_thiele(eq_x, eq_y, op_xy1, op_xy2, n_stages=)` — 逆流阶梯法
- **喂**：平衡曲线 `eq_x, eq_y`（X 升序）；操作线两端点 `op_xy1`=(X小那端) `op_xy2`=(X大/feed 那端)。
- **`n_stages` 给数**：只走这么多级，返回 `x_final`（验证够不够）。**不给**：一直走到 raffinate 端，返回 `n_stages`（求需要几级）。
- **出**：平衡曲线 + 操作线 + 阶梯台阶 + 级数标号。返回 dict 里 `n_stages` / `x_final` / `stage_x`。
- 对应：T02 Q1(c) 逆流。⚠️ 错流是另一种构造（多条操作线），这函数只管逆流阶梯。

### 4. `plot_drying_curve(X, R, X_c, X_2=, R_c=)` — 干燥速率曲线
- **喂**：`X` 平均含水率、`R` 对应干燥速率（差分算出来的那些点）；`X_c` 临界含水率。
- **算积分要给 `X_2`**（降速段终点），返回 dict 里 `falling_integral` = ∫dX/R（乘 L_s/A 得降速段时间）。`R_c` 不给会自动取 X_c 处的 R。
- **出**：R-X 曲线 + X_c 竖线 + 恒速段水平线 + 降速段积分阴影。
- 对应：T03 Q1。

### 5. `plot_filtration_linear(V, t_over_V)` — 恒压过滤线性图
- **喂**：`V` 滤液体积、`t_over_V` = t/V。
- **出**：散点 + 最小二乘拟合线。返回 dict 里 `slope`（=K_p/2）、`intercept`（=B）、`K_p`。
- 对应：Ch4 过滤恒压模式。

### 6. `plot_sle_right_triangle(...)` — 固液萃取直角三角图
- ⚠️ **跟 1. 的等边三角图不是一回事**：LLE（L01）用等边三元相图，**SLE（L02）用直角三角图**。x 轴=溶质分数 x_A、y 轴=溶剂分数 x_S、固体= 1−x_A−x_S（斜边=固体0）。
- **喂**：`under_n`（溶液中溶质分数）+ `under_r`（夹带量 kg溶液/kg固体）定义 underflow 夹带线；四个终端组成 `feed_underflow`(x₀)、`exit_overflow`(y₁)、`final_underflow`(xₙ)、`fresh_solvent`(默认纯溶剂 (0,1))，都写成 (x_A, x_S)。
- **出**：直角三角 + underflow 线 + overflow 线（斜边）+ 净流点 Δ + 七步 stepping 阶梯，返回 `n_stages`（理论级数）。
- 辅助 `entrainment_to_xy(n, r)` 把夹带数据转直角三角坐标。
- 加 `show_construction=True` 画出全部构造射线（定 Δ 的终端线、过固体顶点的平衡射线、指向 Δ 的操作射线）= 七步法"不跳步"教学图。⚠️ 高纯度/高洗比题后几级浓度几何衰减会挤在角落，线性坐标分不开，精确记录看返回的 coords 表。
- 对应：L02 §[C2] 变夹带图解法。⚠️ 大多数 SLE 题用闭式 R=w/W 公式就行（纯算数），只有夹带随浓度变才需要这个图。

### 7. `plot_psychrometric_chart(points=)` — 湿度图（干燥）
- ⚠️ 这是张"读图"用的标准工程图，不是从题目数据画的。用 `psychrolib` 库算物性（要 `pip install psychrolib`）。
- **喂**：`points` 列表，每个状态点给 `Tdb`（干球℃）+ 下面之一：`RH`(0-1) / `Twb`(湿球℃) / `Hr`(湿度比)。
- **出**：饱和线 + RH 曲线族 + 等湿球/焓斜线，每个状态点标 (Tdb, Twb, RH, H, 焓)。返回 `coords` 含各点算全的物性。
- 对应：L03 知识块3 湿度图读图（example-4 套路）。

### 8. `plot_lle_d_system(raffinate, extract, F, S, RN, ...)` — LLE [D] 差点图解
- ⚠️ **期末最高频题型**（知识块13）：部分互溶逆流，在**等边**三元相图上用差点 P + stepping 数级数。
- **喂**：`raffinate`/`extract` tie-line 配对数据 + 进料 `F` + 溶剂 `S` + 目标萃余 `RN`（都 (A,B,C)）+ **`S_over_F`（溶剂/进料比）**自动算 E1（或直接给 `E1=`）。
- **出**：等边三角 + binodal + tie line + 混合点 M + 差点 P + stepping 阶梯，返回 `n_stages`。差点 P 常落在三角外（正常）。
- 算法跟 SLE 净流点同一套，只是三角形不同。⚠️ T02 Q2 是这类题但没给数据；用别的体系数据喂就能跑。

---

## 出"图解题完整解答"时的格式（用户要这个）

图解题（三角图 / 阶梯 / SLE）写 `solution.md` 时，**不能只给数字或只给图**，要四层都有：

1. **计算步骤**：物料衡算定终端流，每个数字带代入 + 单位
2. **画图指示**：用 `🖉 画图①②…` 标记，手把手写"方格纸上先画啥、再标啥、怎么连线定下一个点"，对应讲义七步法 —— 让人能**手工复现**
3. **画图结果**：`![](figures/xxx.png)` 把函数出的图嵌进去（三角图加 `show_construction=True` 显示构造射线）
4. **数字表**：逐级 n / r / 坐标 / 纯度，作为"一步不跳"的精确记录（图会因几何压缩看不清，表才精确）

解答范例可以自己攒一份放在课程目录的 `_drafts/` 里（例如固液萃取那道颜料洗涤题的完整解答），下次同类题直接照抄结构。

## 三句话总结

1. **这文件说了什么**：分离过程常考的几种图解题，各有一个测好的画图函数，喂干净数据就出正确图。
2. **我什么时候回来看**：做单元操作 / 分离过程课任何要画三元图 / 阶梯 / 干燥曲线 / 过滤线性图的题时。
3. **看完能做什么**：照"喂什么出什么"调函数，不用再让 AI 从零推坐标变换和 stepping。
