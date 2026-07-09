# 化工作业绘图规范

这份给 Claude 在 Phase 1 写画图代码时按需读。**任何画图都要按这套来**, 否则八成会踩中文字体 / 配色 / outlier 压扁 / label 不规范的坑。

## 必做 5 件事

1. **顶部 import + 调 style**:
   ```python
   import sys
   sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/skills/homework-coach/scripts')
   from plot_setup import apply_chemeng_style, check_axis_range

   apply_chemeng_style()  # 中文字体 + 黑白工程图 + tick 规范
   ```

2. **每条线带 label + 加 legend**:
   ```python
   ax.plot(x, y1, label='Reactor outlet')
   ax.plot(x, y2, label='Heat exchanger outlet')
   ax.legend(loc='best')
   ```

3. **轴 label 带单位**:
   ```python
   ax.set_xlabel('Temperature (K)')
   ax.set_ylabel('Conversion (%)')
   ```
   单位用括号包, 不要写 "Temperature, K" 这种。

4. **画完 check axis 范围**:
   ```python
   check_axis_range(ax, y_data)
   ```
   warn 了就 `ax.set_ylim(...)` 或 `ax.set_yscale('log')`。

5. **标题 / label 用本科生口吻**:
   - 中文作业 → 中文 label, 不要中英混 (除了单位)
   - 英文作业 → 全英, 单词用 "Conversion" 不用 "Conv."

## 黑白工程图风格

`apply_chemeng_style()` 已经配好:
- color cycle: `#000000` -> `#555555` -> `#888888` -> `#BBBBBB`
- linestyle cycle: `-` -> `--` -> `:` -> `-.`
- 区分多条线靠 **线型 + 灰度阶梯**, 不靠彩色

化工报告 / 论文几乎都用这种, 老师看着舒服。不要用 `plt.style.use('seaborn')` 之类的彩色 preset。

## CME214 图解法专用图 → 用 chemeng_plots，别手写

单元操作 II 的三元相图 / 阶梯法 / 干燥曲线，**坐标变换、stepping、积分这些 AI 临时写必踩坑**。已经写成测好的函数，直接喂数据，别从零推：

```python
from chemeng_plots import plot_ternary, plot_distribution, \
    plot_mccabe_thiele, plot_drying_curve, plot_filtration_linear
```

所有函数返回 `(fig, ax, result)`，`result["coords"]` 是画图坐标（`print(coords_table(result))` 打表），
所有图自带浅网格（XY 淡方格 / 三元浅三角网格）。

| 题型 | 函数 | result 额外返回 |
|---|---|---|
| LLE 三元相图（**等边**三角 binodal + tie line + 杠杆 + plait） | `plot_ternary(raffinate, extract, mix=, FS=)` | `plait_xy` |
| SLE 直角三角图（**直角**三角 + underflow/overflow + Δ + 七步 stepping） | `plot_sle_right_triangle(under_n, under_r, x0, y1, xn)` | `n_stages` |
| LLE [D] 部分互溶逆流（等边三角 + 差点 P stepping，**期末高频**） | `plot_lle_d_system(raffinate, extract, F, S, RN, S_over_F=)` | `n_stages` |
| 湿度图（饱和线 + RH 曲线 + 状态点，需 `pip install psychrolib`） | `plot_psychrometric_chart(points=)` | 状态点物性 |
| 分配曲线（y vs x + y=x 线） | `plot_distribution(x_raff, y_ext)` | — |
| 逆流阶梯法数级数 | `plot_mccabe_thiele(eq_x, eq_y, op_xy1, op_xy2, n_stages=)` | `n_stages` / `x_final` |
| 干燥速率曲线 + 降速段积分 | `plot_drying_curve(X, R, X_c, X_2=)` | `falling_integral` |
| 恒压过滤 t/V vs V 线性拟合 | `plot_filtration_linear(V, t_over_V)` | `slope` / `intercept` / `K_p` |

详细用法（喂什么数据、返回什么）→ 读 `references/chemeng-plots.md`。
准确率已用 `examples_cme214.py` 拿 tutorial 已知答案卡死（三元和≈100%、阶梯≈3级、干燥积分≈0.1276）。

## 常见图型套路

### 转化率 / 收率 vs T 或 t
```python
ax.set_ylim(0, 100)  # 强制 0-100%, 防 outlier
ax.set_xlabel('Temperature (K)')
ax.set_ylabel('Conversion X_A (%)')
```

### 焓 / 物性 vs T (多 phase)
- 不同 phase 用不同 linestyle (style 已配好), 不要用不同颜色
- 在 legend 写清楚 `'Liquid'` / `'Vapor'` 等

### 量级跨多个数量级 (K_eq, 扩散系数, 反应速率)
```python
ax.set_yscale('log')  # 必须 log, 不然小值压成 0
```

### Arrhenius 图 (ln k vs 1/T)
- x 轴用 `1000/T (K^{-1})`, 不是裸 `1/T`
- y 轴 `ln k`, 不要 `log10 k` (除非题目要求)

### BFD / 流程图
- **不要用 matplotlib 画 BFD**, 用 draw.io / Visio / Inkscape 手画, 导 PNG
- matplotlib 画 BFD 的代码必然丑且不专业

## 反例 (不要这样画)

- 默认 tab10 彩色 (一眼 AI 输出)
- 不带 axis label / 不带单位
- 一两个 outlier 把主数据压成水平线
- 中文 label 显示成方框 (没跑 apply_chemeng_style)
- legend 遮住数据线 (用 `loc='best'` 或挪到图外 `bbox_to_anchor`)
- tick 加密一堆 minor 把图弄花 (默认就行, 别手动 set_minor_locator)
- 标题字号比 axis label 还小

## 输出文件

```python
fig.savefig('figures/conversion_vs_T.png')
# apply_chemeng_style 已经设 savefig.dpi=200, bbox='tight'
```

文件名: `<物理量>_vs_<自变量>.png`, 不要 `figure1.png` / `output.png` 这种没意义的。

## 画完必做 vision check

按 user 的 [feedback_vision_check_figures](memory) 规则, 画完必须 Read 一下 PNG 自查:
- outlier 有没有压扁主趋势 (check_axis_range 是机器判断, vision 是兜底)
- 中文有没有显示正常
- legend 有没有遮数据
