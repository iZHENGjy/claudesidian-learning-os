"""homework-coach 绘图规范工具。

提供两个函数：
- apply_chemeng_style(): 给 matplotlib 配中文字体 + 黑白工程图风格 + 规范的 axes/tick
- check_axis_range(ax, data): 检测 outlier 压扁主趋势

用法（在 calc.py 顶部）:
    import sys
    sys.path.insert(0, '.claude/plugins/chemeng-coursework/skills/homework-coach/scripts')
    from plot_setup import apply_chemeng_style, check_axis_range

    apply_chemeng_style()
    fig, ax = plt.subplots()
    ax.plot(x, y)
    check_axis_range(ax, y)  # 警告 outlier 占据主视野
"""

from __future__ import annotations
import sys
import matplotlib as mpl
import numpy as np


def apply_chemeng_style() -> None:
    """配化工报告标准 matplotlib 样式。

    - 中文字体: 优先 Microsoft YaHei, fallback 系统 sans-serif
    - 配色: 黑白工程图 (黑 + 灰阶 + 线型变化, 不靠彩色)
    - 字号: title 14, label 12, tick 10
    - tick 朝内 + 显示 minor tick
    - savefig: 200 dpi, bbox=tight
    """
    # 中文字体 fallback 链
    mpl.rcParams["font.sans-serif"] = [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "DejaVu Sans",
    ]
    mpl.rcParams["axes.unicode_minus"] = False  # 防负号变方框

    # 黑白工程图配色: 黑 -> 深灰 -> 中灰 -> 浅灰, 同时换线型
    mpl.rcParams["axes.prop_cycle"] = (
        mpl.cycler(color=["#000000", "#555555", "#888888", "#BBBBBB"])
        + mpl.cycler(linestyle=["-", "--", ":", "-."])
    )

    # 字号
    mpl.rcParams["axes.titlesize"] = 14
    mpl.rcParams["axes.labelsize"] = 12
    mpl.rcParams["xtick.labelsize"] = 10
    mpl.rcParams["ytick.labelsize"] = 10
    mpl.rcParams["legend.fontsize"] = 10

    # tick 朝内 + minor
    mpl.rcParams["xtick.direction"] = "in"
    mpl.rcParams["ytick.direction"] = "in"
    mpl.rcParams["xtick.minor.visible"] = True
    mpl.rcParams["ytick.minor.visible"] = True

    # axes 边框 + grid 虚线浅淡
    mpl.rcParams["axes.linewidth"] = 1.0
    mpl.rcParams["grid.linestyle"] = ":"
    mpl.rcParams["grid.alpha"] = 0.4

    # 图保存
    mpl.rcParams["figure.dpi"] = 100
    mpl.rcParams["savefig.dpi"] = 200
    mpl.rcParams["savefig.bbox"] = "tight"


def check_axis_range(ax, data, threshold: float = 0.05) -> bool:
    """检测 outlier 是否压扁主趋势。

    用 IQR (25-75 分位) 衡量"数据主体"的范围, 跟当前 y 轴 span 比。
    如果主体只占轴的 < threshold (默认 5%), 说明 outlier 把主趋势压扁了。

    Args:
        ax: matplotlib Axes 对象
        data: 1D array-like, 实际画的 y 数据
        threshold: 主体 / 轴 比例阈值, 低于这个就警告

    Returns:
        True = OK, False = 警告 (已 print stderr)
    """
    arr = np.asarray(data, dtype=float).ravel()
    arr = arr[~np.isnan(arr)]
    if len(arr) < 4:
        return True  # 数据太少, 不判断

    ymin, ymax = ax.get_ylim()
    axis_span = ymax - ymin
    if axis_span <= 0:
        return True

    q25, q75 = np.percentile(arr, [25, 75])
    iqr_span = q75 - q25

    ratio = iqr_span / axis_span
    if ratio < threshold:
        print(
            f"[WARN] check_axis_range: 数据主体 (IQR) 只占 y 轴 {ratio:.1%}, "
            f"主趋势被 outlier 压扁。建议 ax.set_ylim(...) 限制范围或用 ax.set_yscale('log')。",
            file=sys.stderr,
        )
        return False
    return True
