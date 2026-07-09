# -*- coding: utf-8 -*-
"""专业彩色绘图风格 (plot_setup.py 灰阶工程图风的彩色替代)。

什么时候用哪个:
- `plot_setup.apply_chemeng_style()` —— 黑白灰阶, 适合纯工程图 / 要打印省墨 / 老师要黑白。
- `plot_pro.apply_pro_style()` (本文件) —— Okabe-Ito 色盲友好彩色, 适合报告里要好看、要区分多条线、
  英文报告封面级图。源自 CME222 报告实战图。

用法:
    import sys
    sys.path.insert(0, '.claude/plugins/chemeng-coursework/skills/homework-coach/scripts')
    from plot_pro import apply_pro_style, PALETTE, mark_points, shade_spans
    apply_pro_style()
    fig, ax = plt.subplots(figsize=(6.4, 4.4), constrained_layout=True)
    ax.plot(x, y, color=PALETTE['blue'], lw=2.4, label='...')
    mark_points(ax, x_design, y_design, PALETTE['blue'])   # 标设计点
    fig.savefig('figures/fig.png')

⚠️ 中文标签: apply_pro_style 用 Arial (无中文)。要中文图另设 font.sans-serif=['Microsoft YaHei']。
⚠️ 画完每张图必 Read PNG 做 vision 核对 (查 outlier 压扁 / 标签溢出 / 中文方框)。
"""
from __future__ import annotations
import matplotlib as mpl

# Okabe-Ito 色盲友好色板 (8 色, 学术界标准)
PALETTE = {
    "blue":   "#0072B2",   # 主色 (如 CO2)
    "orange": "#D55E00",   # 朱 (如 N2)
    "green":  "#009E73",   # 绿 (如 O2)
    "purple": "#CC79A7",   # 选中点 / 强调
    "yellow": "#E69F00",
    "sky":    "#56B4E9",
    "gray":   "#555555",   # 辅助线
    "black":  "#000000",
}


def apply_pro_style() -> None:
    """配专业彩色报告图样式 (Okabe-Ito + 加粗标题 + 淡网格 + 200 dpi 存图)。"""
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans", "Helvetica"],
        "mathtext.fontset": "dejavusans",
        "axes.titlesize": 13, "axes.titleweight": "bold",
        "axes.labelsize": 11, "xtick.labelsize": 10, "ytick.labelsize": 10,
        "legend.fontsize": 9.5, "legend.frameon": True,
        "legend.framealpha": 0.9, "legend.edgecolor": "0.8",
        "axes.linewidth": 1.0, "axes.edgecolor": "0.3",
        "xtick.direction": "out", "ytick.direction": "out",
        "axes.grid": True, "grid.linestyle": "-",
        "grid.linewidth": 0.5, "grid.alpha": 0.35,
        "axes.unicode_minus": False,
        "figure.dpi": 110, "savefig.dpi": 200, "savefig.bbox": "tight",
    })
    # 默认配色循环走 Okabe-Ito
    mpl.rcParams["axes.prop_cycle"] = mpl.cycler(
        color=[PALETTE["blue"], PALETTE["orange"], PALETTE["green"],
               PALETTE["purple"], PALETTE["yellow"], PALETTE["sky"]]
    )


def mark_points(ax, xs, ys, color, size=46):
    """在 ax 上把一组 (xs, ys) 画成带白边的圆点标记 (标设计点 / 选中点)。"""
    ax.scatter(xs, ys, s=size, color=color, edgecolor="white",
               linewidth=1.2, zorder=6, clip_on=False)


def shade_spans(ax, spans):
    """给 ax 加若干竖向淡色带, 区分区间 (如不同机制区)。
    spans: [(x0, x1, color, alpha), ...]。
    """
    x0, x1 = ax.get_xlim()
    for a, b, c, al in spans:
        ax.axvspan(a, b, color=c, alpha=al)
    ax.set_xlim(x0, x1)
