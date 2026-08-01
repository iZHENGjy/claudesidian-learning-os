"""分离过程 / 单元操作图解法专用画图库（作者用在 CME214 单元操作 II 上）。

这类课的题大半要画图：三元相图、阶梯法、干燥曲线。以前 AI 临时画每次都从零
推坐标变换 / stepping / 积分，又慢又错。这里把这几种图写成测好的函数，喂干净
数据就出正确的图。准确率靠 examples_cme214.py 拿 tutorial 已知答案当基准卡死。

复用 plot_setup.py 的样式（中文字体 + 黑白工程图 + outlier 检查），不另配。

五个画图函数（每个返回 (fig, ax) + 算出来的关键数值）：
- plot_ternary           三元相图（binodal + tie line + 杠杆规则 + plait point）
- plot_distribution      分配曲线（y vs x + y=x 参考线）
- plot_mccabe_thiele     逆流阶梯法（操作线↔平衡曲线走台阶数级数）
- plot_drying_curve      干燥速率曲线 R-X（标 X_c + 降速段积分阴影）
- plot_filtration_linear 过滤 t/V vs V 线性回归

辅助函数（被上面调用、单独可测）：
- ternary_to_xy          三角坐标 (a,b,c) → 直角坐标 (x,y)
- lever_rule             杠杆规则求质量比
- falling_rate_integral  降速段梯形积分 ∫dX/R

用法（在 calc.py 里）:
    import sys
    sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/skills/homework-coach/scripts')  # 换成本机实际路径
    from chemeng_plots import plot_ternary, plot_drying_curve, ...
"""

from __future__ import annotations
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# 复用现有样式工具（同目录）—— 用 os.path 兼容 Windows 反斜杠路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plot_setup import apply_chemeng_style, check_axis_range  # noqa: E402

# np.trapezoid 是 numpy>=2.0 的名字，旧版叫 np.trapz —— 兜底兼容
_trapz = getattr(np, "trapezoid", None) or np.trapz


# ============================================================
# 辅助函数（纯计算，可单独测试）
# ============================================================

# 等边三角形三个顶点（直角坐标）
_TOP = np.array([0.5, np.sqrt(3) / 2])   # 顶点 = 溶质 A (acetone)
_LEFT = np.array([0.0, 0.0])             # 左下 = 载体 B (water)
_RIGHT = np.array([1.0, 0.0])            # 右下 = 溶剂 C (solvent)


def ternary_to_xy(a, b, c):
    """三角坐标 → 直角坐标。

    输入三组分分数 (a, b, c)，自动归一化（允许传 wt%，内部除以总和）。
    约定：a=顶点(溶质)、b=左下(载体)、c=右下(溶剂)。

    返回 (x, y)。支持标量或等长数组。
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    c = np.asarray(c, dtype=float)
    total = a + b + c
    a, b, c = a / total, b / total, c / total
    x = 0.5 * a + c          # = a*0.5 + b*0 + c*1
    y = a * (np.sqrt(3) / 2)  # = a*顶点y
    return x, y


def lever_rule(xy_M, xy_1, xy_2):
    """杠杆规则：M = 物流1 + 物流2，求 质量1 / 质量2。

    杠杆规则：质量与到 M 的臂长成反比 → 质量1/质量2 = dist(M,2) / dist(M,1)。
    （重的物流离 M 近，臂短。）

    输入三个点的直角坐标 (x,y)，返回 mass1/mass2。
    """
    M = np.asarray(xy_M, dtype=float)
    p1 = np.asarray(xy_1, dtype=float)
    p2 = np.asarray(xy_2, dtype=float)
    d1 = np.linalg.norm(M - p1)
    d2 = np.linalg.norm(M - p2)
    return d2 / d1


def falling_rate_integral(X, R):
    """降速段梯形积分 ∫ dX/R（从小 X 到大 X）。

    输入：X 含水率数组、R 对应干燥速率数组（同长，至少 2 点）。
    返回积分值（= L_s/A 之外的那部分，乘 L_s/A 得降速段时间）。

    内部按 X 升序排好再积，所以传入顺序无所谓。
    """
    X = np.asarray(X, dtype=float)
    R = np.asarray(R, dtype=float)
    order = np.argsort(X)
    X, R = X[order], R[order]
    inv_R = 1.0 / R
    return float(_trapz(inv_R, X))


def entrainment_to_xy(n, r):
    """SLE 夹带数据 → 直角三角图坐标。

    n = 溶液中溶质质量分数 (kg 溶质 / kg 溶液)；r = 夹带量 (kg 溶液 / kg 固体)。
    以 1 kg 固体为基准：溶质 = r·n，溶剂 = r·(1-n)，固体 = 1，总 = 1+r。
    返回 (x_A, x_S) = (溶质分数, 溶剂分数)，固体分数 = 1 - x_A - x_S。
    """
    n = np.asarray(n, dtype=float)
    r = np.asarray(r, dtype=float)
    tot = 1.0 + r
    return r * n / tot, r * (1 - n) / tot


def _line_intersect(p1, p2, p3, p4):
    """两条直线 (p1p2) 与 (p3p4) 的交点。平行返回 None。"""
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-15:
        return None
    a = x1 * y2 - y1 * x2
    b = x3 * y4 - y3 * x4
    px = (a * (x3 - x4) - (x1 - x2) * b) / den
    py = (a * (y3 - y4) - (y1 - y2) * b) / den
    return (px, py)


def _interp_on_curve(x_query, xs, ys):
    """在折线 (xs, ys) 上按 x 线性插值求 y。xs 需单调递增。"""
    return float(np.interp(x_query, xs, ys))


def _smooth_branch(xy_points):
    """对一条曲线分支的 xy 点做轻度平滑。点太少就原样返回。

    用参数样条（按累计弧长参数化），避免 binodal 这种非函数曲线插值失败。
    """
    pts = np.asarray(xy_points, dtype=float)
    if len(pts) < 4:
        return pts[:, 0], pts[:, 1]
    try:
        from scipy.interpolate import splprep, splev
        # s 给一点平滑量，k=3 三次样条
        tck, _ = splprep([pts[:, 0], pts[:, 1]], s=1e-4, k=3)
        u = np.linspace(0, 1, 200)
        xs, ys = splev(u, tck)
        return np.asarray(xs), np.asarray(ys)
    except Exception:
        return pts[:, 0], pts[:, 1]


def _light_grid(ax):
    """XY 图加一层浅网格（主刻度虚线 + 更淡的次刻度）。"""
    ax.grid(True, which="major", ls=":", lw=0.6, color="#999999", alpha=0.5)
    ax.grid(True, which="minor", ls=":", lw=0.4, color="#CCCCCC", alpha=0.4)


def _triangular_grid(ax, step=0.1):
    """三元图加浅三角网格：平行三条边、每 step（默认 10%）一条线。"""
    ks = np.arange(step, 1.0, step)
    for k in ks:
        # 平行底边（a=常数）：从 (a=k,b=1-k,c=0) 到 (a=k,b=0,c=1-k)
        p1 = ternary_to_xy(k, 1 - k, 0)
        p2 = ternary_to_xy(k, 0, 1 - k)
        # 平行右边（b=常数）：从 (a=1-k,b=k,c=0) 到 (a=0,b=k,c=1-k)
        p3 = ternary_to_xy(1 - k, k, 0)
        p4 = ternary_to_xy(0, k, 1 - k)
        # 平行左边（c=常数）：从 (a=1-k,b=0,c=k) 到 (a=0,b=1-k,c=k)
        p5 = ternary_to_xy(1 - k, 0, k)
        p6 = ternary_to_xy(0, 1 - k, k)
        for (xa, ya), (xb, yb) in [(p1, p2), (p3, p4), (p5, p6)]:
            ax.plot([xa, xb], [ya, yb], color="#CCCCCC", lw=0.5, ls="-", zorder=0)


def _triangular_ticks(ax, step=0.2):
    """给三元图三条边标刻度数字（每条边对应一个组分，平行于它的网格线）。

    约定（与 _TOP=A顶 / _LEFT=B左下 / _RIGHT=C右下 一致）：
    - 左边 AB → A(溶质)刻度：B 端 0% → A 端 100%
    - 底边 BC → B(载体)刻度：C 端 0% → B 端 100%
    - 右边 AC → C(溶剂)刻度：A 端 0% → C 端 100%
    每条边的刻度正好落在平行于它的那族网格线上，便于读数。
    """
    ks = np.arange(0.0, 1.0 + 1e-9, step)
    for k in ks:
        kp = int(round(k * 100))
        # 左边 AB：A 刻度。点 (a=k, b=1-k, c=0)，数字放左外侧
        xa, ya = ternary_to_xy(k, 1 - k, 0)
        ax.text(xa - 0.025, ya, f"{kp}", ha="right", va="center",
                fontsize=7, color="#555555")
        # 底边 BC：B 刻度。点 (a=0, b=k, c=1-k)，数字放正下方
        xb, yb = ternary_to_xy(0, k, 1 - k)
        ax.text(xb, yb - 0.028, f"{kp}", ha="center", va="top",
                fontsize=7, color="#555555")
        # 右边 AC：C 刻度。点 (a=1-k, b=0, c=k)，数字放右外侧
        xc, yc = ternary_to_xy(1 - k, 0, k)
        ax.text(xc + 0.025, yc, f"{kp}", ha="left", va="center",
                fontsize=7, color="#555555")


def _coord_block(columns, rows):
    """打包一段坐标表：列名 + 各行。"""
    return {"columns": list(columns), "rows": [list(r) for r in rows]}


def coords_table(result):
    """把 plot_* 返回的 result["coords"] 格式化成可打印的坐标表字符串。

    用法：print(coords_table(result))
    """
    coords = result.get("coords", {})
    out = []
    for name, block in coords.items():
        out.append(f"# {name}")
        cols = block["columns"]
        out.append("  ".join(f"{str(c):>11}" for c in cols))
        for row in block["rows"]:
            cells = []
            for v in row:
                cells.append(f"{v:>11.4g}" if isinstance(v, (int, float)) else f"{str(v):>11}")
            out.append("  ".join(cells))
        out.append("")
    return "\n".join(out)


# ============================================================
# 1. 三元相图（LLE）
# ============================================================

def plot_ternary(raffinate, extract, labels=("Acetone (A)", "Water (B)", "Solvent (C)"),
                 mix=None, FS=None, title="三元相图"):
    """画 LLE 三元相图：binodal 曲线 + tie line + 可选混合点/杠杆线。

    参数
    ----
    raffinate : list[(a,b,c)]   萃余相（水层）各平衡点，(溶质, 载体, 溶剂)，wt% 或分数皆可
    extract   : list[(a,b,c)]   萃取相（溶剂层）各平衡点，与 raffinate 一一对应（同行 = 一条 tie line）
    labels    : (顶点名, 左下名, 右下名)
    mix       : (a,b,c) 可选，混合点 M，画一个标记
    FS        : ((a,b,c)_F, (a,b,c)_S) 可选，画 F-S 连线（杠杆规则用）
    title     : 图标题

    返回 (fig, ax, result)，result["coords"] 含每个点的 (a,b,c) 组成 + (x,y) 直角坐标。
    """
    apply_chemeng_style()
    fig, ax = plt.subplots(figsize=(6.5, 6))

    raff = np.asarray(raffinate, dtype=float)
    extr = np.asarray(extract, dtype=float)

    # 浅三角网格（每 10% 一条，平行三边）+ 三条边刻度数字（每 20%）
    _triangular_grid(ax, step=0.1)
    _triangular_ticks(ax, step=0.2)

    # 三角形外框
    tri = np.array([_TOP, _LEFT, _RIGHT, _TOP])
    ax.plot(tri[:, 0], tri[:, 1], color="black", lw=1.2, ls="-")
    # 顶点标注（括号里注明该组分刻度读哪条边，对应 _triangular_ticks）
    ax.text(_TOP[0], _TOP[1] + 0.05, f"{labels[0]}\n(左边刻度 ↗ wt%)",
            ha="center", va="bottom", fontsize=10)
    ax.text(_LEFT[0] - 0.04, _LEFT[1] - 0.04, f"{labels[1]}\n(底边刻度 wt%)",
            ha="right", va="top", fontsize=10)
    ax.text(_RIGHT[0] + 0.04, _RIGHT[1] - 0.04, f"{labels[2]}\n(右边刻度 wt%)",
            ha="left", va="top", fontsize=10)

    # 数据点转 xy
    xr, yr = ternary_to_xy(raff[:, 0], raff[:, 1], raff[:, 2])
    xe, ye = ternary_to_xy(extr[:, 0], extr[:, 1], extr[:, 2])

    # tie line（每对连线，浅灰）
    for i in range(len(xr)):
        ax.plot([xr[i], xe[i]], [yr[i], ye[i]], color="#888888", lw=0.8, ls="-", zorder=1)

    # 两条 binodal 分支平滑（按溶质含量排序后接成 dome）
    raff_sorted = raff[np.argsort(raff[:, 0])]
    extr_sorted = extr[np.argsort(extr[:, 0])]
    rb_xy = np.column_stack(ternary_to_xy(raff_sorted[:, 0], raff_sorted[:, 1], raff_sorted[:, 2]))
    eb_xy = np.column_stack(ternary_to_xy(extr_sorted[:, 0], extr_sorted[:, 1], extr_sorted[:, 2]))
    # 拼成一条完整 binodal：萃余分支(溶质升) + 萃取分支(溶质降)
    dome = np.vstack([rb_xy, eb_xy[::-1]])
    bx, by = _smooth_branch(dome)
    ax.plot(bx, by, color="black", lw=1.4, ls="--", label="Binodal 曲线", zorder=2)

    # 数据点
    ax.scatter(xr, yr, s=28, facecolors="white", edgecolors="black", marker="o",
               label="萃余相 (R)", zorder=3)
    ax.scatter(xe, ye, s=28, facecolors="black", edgecolors="black", marker="^",
               label="萃取相 (E)", zorder=3)

    # plait point 估计 = binodal 顶部（y 最大处）
    pi = int(np.argmax(by))
    ax.scatter([bx[pi]], [by[pi]], s=60, marker="*", color="black", zorder=4)
    ax.annotate("Plait point P", (bx[pi], by[pi]),
                textcoords="offset points", xytext=(8, 6), fontsize=9)

    # 可选混合点 M
    if mix is not None:
        mx, my = ternary_to_xy(*mix)
        ax.scatter([mx], [my], s=50, marker="x", color="black", zorder=5)
        ax.annotate("M", (mx, my), textcoords="offset points", xytext=(6, -10), fontsize=10)

    # 可选 F-S 连线
    if FS is not None:
        fx, fy = ternary_to_xy(*FS[0])
        sx, sy = ternary_to_xy(*FS[1])
        ax.plot([fx, sx], [fy, sy], color="#555555", lw=1.0, ls="--", label="F-S 线")
        ax.annotate("F", (fx, fy), textcoords="offset points", xytext=(4, 4), fontsize=9)
        ax.annotate("S", (sx, sy), textcoords="offset points", xytext=(4, 4), fontsize=9)

    ax.set_title(title)
    ax.set_aspect("equal")
    # 留边距，别把三角形外侧的刻度数字裁掉
    ax.set_xlim(-0.12, 1.12)
    ax.set_ylim(-0.12, np.sqrt(3) / 2 + 0.12)
    ax.axis("off")
    ax.legend(loc="upper right", fontsize=9)

    # 坐标输出：每个点的 (溶质 a, 载体 b, 溶剂 c) 归一化% + 直角 (x,y)
    def _rows(pts, xs, ys, tag):
        rows = []
        for i, p in enumerate(pts):
            s = sum(p)
            rows.append([f"{tag}{i+1}", 100 * p[0] / s, 100 * p[1] / s,
                         100 * p[2] / s, xs[i], ys[i]])
        return rows
    cols = ["点", f"{labels[0][:6]}%", f"{labels[1][:6]}%", f"{labels[2][:6]}%", "x", "y"]
    coords = {
        "萃余相 R（水层）": _coord_block(cols, _rows(raff, xr, yr, "R")),
        "萃取相 E（溶剂层）": _coord_block(cols, _rows(extr, xe, ye, "E")),
        "Plait point P (x,y)": _coord_block(["x", "y"], [[bx[pi], by[pi]]]),
    }
    return fig, ax, {"coords": coords, "plait_xy": (float(bx[pi]), float(by[pi]))}


# ============================================================
# 2. 分配曲线
# ============================================================

def plot_distribution(x_raff, y_ext, label="体系", op_point=None,
                      title="分配曲线", xlabel="溶质 in 萃余相 x (wt%)",
                      ylabel="溶质 in 萃取相 y (wt%)"):
    """画分配曲线 y vs x，带 y=x 参考线。

    参数
    ----
    x_raff, y_ext : 各 tie line 两端的溶质含量（萃余 / 萃取）
    label         : 曲线名（多体系叠加时区分）
    op_point      : (x, y) 可选，标一个工作点（如 Q2 的 tie line 投影）
    返回 (fig, ax, result)，result["coords"] 含每个 (x, y) 数据点。
    """
    apply_chemeng_style()
    fig, ax = plt.subplots(figsize=(6, 6))

    x = np.asarray(x_raff, dtype=float)
    y = np.asarray(y_ext, dtype=float)
    order = np.argsort(x)
    x, y = x[order], y[order]

    # y=x 参考线
    lim = max(x.max(), y.max()) * 1.05
    ax.plot([0, lim], [0, lim], color="#888888", ls=":", lw=1.0, label="y = x")

    ax.plot(x, y, color="black", marker="o", ms=4, lw=1.4, label=label)

    if op_point is not None:
        ax.scatter([op_point[0]], [op_point[1]], s=60, marker="s",
                   facecolors="none", edgecolors="black", zorder=5, label="工作点")

    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    ax.set_aspect("equal")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    _light_grid(ax)
    ax.legend(loc="best")

    coords = {"分配曲线数据点": _coord_block(["x (萃余%)", "y (萃取%)"],
                                       [[xi, yi] for xi, yi in zip(x, y)])}
    return fig, ax, {"coords": coords}


# ============================================================
# 3. 逆流阶梯法（McCabe-Thiele）
# ============================================================

def plot_mccabe_thiele(eq_x, eq_y, op_xy1, op_xy2, n_stages=None,
                       title="逆流多级萃取 — 阶梯法",
                       xlabel="X = 溶质/载体 (kg/kg)", ylabel="Y = 溶质/溶剂 (kg/kg)"):
    """逆流阶梯法：在平衡曲线和操作线之间走台阶，数理论级数。

    几何：从 feed 端（op_xy2，X 大的那端）开始，水平走到平衡曲线 = 一个理论级，
    再竖直走回操作线，交替直到到达 raffinate 端（op_xy1，X 小的那端）。

    参数
    ----
    eq_x, eq_y : 平衡曲线数据点（X, Y），X 升序
    op_xy1     : (X_lo, Y_lo) 操作线 raffinate 端（X 小）
    op_xy2     : (X_hi, Y_hi) 操作线 feed 端（X 大）
    n_stages   : 给定就只走这么多级（forward 模式，返回最终 X）；
                 None 就一直走到 X<=X_lo（design 模式，返回所需级数）

    返回 (fig, ax, result)，result = {"n_stages": 级数, "x_final": 最终X, "stage_x": [...]}
    """
    apply_chemeng_style()
    fig, ax = plt.subplots(figsize=(6.5, 6))

    ex = np.asarray(eq_x, dtype=float)
    ey = np.asarray(eq_y, dtype=float)

    x_lo, y_lo = op_xy1
    x_hi, y_hi = op_xy2
    slope = (y_hi - y_lo) / (x_hi - x_lo)

    def op_line(xq):
        return y_lo + slope * (xq - x_lo)

    def eq_inv(yq):
        # 给定 Y，在平衡曲线上反查 X（eq_y 需随 eq_x 单调增）
        return float(np.interp(yq, ey, ex))

    # 画平衡曲线 + 操作线
    xx = np.linspace(ex.min(), ex.max(), 200)
    ax.plot(ex, ey, color="black", marker="o", ms=3, lw=1.4, label="平衡曲线")
    ax.plot([x_lo, x_hi], [y_lo, y_hi], color="#555555", ls="--", lw=1.2, label="操作线")

    # stepping：从 feed 端开始
    stage_x = []
    corners = [(x_hi, y_hi)]   # 阶梯顶点（誊到方格纸用）
    cur_x, cur_y = x_hi, y_hi
    max_iter = 50
    count = 0
    while count < max_iter:
        # 水平走到平衡曲线（一个理论级）
        nx = eq_inv(cur_y)
        ax.plot([cur_x, nx], [cur_y, cur_y], color="black", lw=0.8, ls="-")
        count += 1
        stage_x.append(nx)
        corners.append((nx, cur_y))
        ax.annotate(str(count), (nx, cur_y), textcoords="offset points",
                    xytext=(-10, 4), fontsize=8)
        cur_x = nx
        # 停止条件
        if n_stages is not None:
            if count >= n_stages:
                break
        else:
            if cur_x <= x_lo:
                break
        # 竖直走回操作线
        ny = op_line(cur_x)
        ax.plot([cur_x, cur_x], [cur_y, ny], color="black", lw=0.8, ls="-")
        corners.append((cur_x, ny))
        cur_y = ny

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    _light_grid(ax)
    ax.legend(loc="best")

    coords = {
        "平衡曲线点 (X, Y)": _coord_block(["X", "Y"], [[a, b] for a, b in zip(ex, ey)]),
        "操作线两端 (X, Y)": _coord_block(["X", "Y"], [[x_lo, y_lo], [x_hi, y_hi]]),
        "阶梯顶点 (X, Y)": _coord_block(["X", "Y"], [[a, b] for a, b in corners]),
    }
    result = {"n_stages": count, "x_final": stage_x[-1] if stage_x else None,
              "stage_x": stage_x, "coords": coords}
    return fig, ax, result


# ============================================================
# 4. 干燥速率曲线 R-X
# ============================================================

def plot_drying_curve(X, R, X_c, X_2=None, R_c=None,
                      title="干燥速率曲线 R-X",
                      xlabel="自由含水率 X (kg/kg 干基)",
                      ylabel="干燥速率 R (kg/(m²·h))"):
    """画干燥速率曲线 R vs X，标临界含水率 X_c，阴影降速段积分区。

    参数
    ----
    X, R : 各区间的平均含水率与干燥速率
    X_c  : 临界含水率（恒速段末端）
    X_2  : 可选，降速段终点（要算 ∫dX/R 时给）
    R_c  : 可选，恒速段速率（画水平线，不给就取 X_c 附近的 R）

    返回 (fig, ax, result)，result 含 falling_integral（若给了 X_2）。
    """
    apply_chemeng_style()
    fig, ax = plt.subplots(figsize=(6.5, 5))

    X = np.asarray(X, dtype=float)
    R = np.asarray(R, dtype=float)
    order = np.argsort(X)
    Xs, Rs = X[order], R[order]

    ax.plot(Xs, Rs, color="black", marker="o", ms=4, lw=1.4, label="R-X 数据")

    # 恒速段速率
    if R_c is None:
        R_c = _interp_on_curve(X_c, Xs, Rs)
    # 临界点竖线 + 恒速水平线
    ax.axvline(X_c, color="#888888", ls=":", lw=1.0)
    ax.annotate(f"$X_c$ = {X_c:g}", (X_c, R_c), textcoords="offset points",
                xytext=(6, 6), fontsize=9)
    ax.plot([X_c, Xs.max()], [R_c, R_c], color="#555555", ls="--", lw=1.0,
            label=f"恒速段 $R_c$ ≈ {R_c:.2f}")

    result = {"R_c": R_c}

    # 降速段积分阴影
    if X_2 is not None:
        mask = (Xs >= X_2) & (Xs <= X_c)
        fx = Xs[mask]
        fr = Rs[mask]
        # 补端点（线性插值到 X_2 和 X_c）
        if fx.size == 0 or fx.min() > X_2:
            fx = np.insert(fx, 0, X_2)
            fr = np.insert(fr, 0, _interp_on_curve(X_2, Xs, Rs))
        if fx.max() < X_c:
            fx = np.append(fx, X_c)
            fr = np.append(fr, R_c)
        ax.fill_between(fx, fr, color="#BBBBBB", alpha=0.5, label="降速段积分区")
        result["falling_integral"] = falling_rate_integral(fx, fr)

    ax.set_ylim(0, Rs.max() * 1.15)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    _light_grid(ax)
    ax.legend(loc="best")
    check_axis_range(ax, Rs)

    result["coords"] = {
        "R-X 数据点 (X, R)": _coord_block(["X", "R"], [[a, b] for a, b in zip(Xs, Rs)]),
        "临界点": _coord_block(["X_c", "R_c"], [[X_c, R_c]]),
    }
    return fig, ax, result


# ============================================================
# 5. 过滤 t/V vs V 线性回归
# ============================================================

def plot_filtration_linear(V, t_over_V, title="恒压过滤 t/V vs V",
                           xlabel="滤液体积 V (m³)", ylabel="t/V (s/m³)"):
    """恒压过滤线性图：t/V = (K_p/2)·V + B，最小二乘拟合求斜率和截距。

    参数
    ----
    V        : 滤液体积数组
    t_over_V : 对应的 t/V 数组
    返回 (fig, ax, result)，result = {"slope": K_p/2, "intercept": B, "K_p": K_p}
    """
    apply_chemeng_style()
    fig, ax = plt.subplots(figsize=(6, 5))

    V = np.asarray(V, dtype=float)
    y = np.asarray(t_over_V, dtype=float)

    slope, intercept = np.polyfit(V, y, 1)

    ax.scatter(V, y, s=30, facecolors="white", edgecolors="black", marker="o",
               label="实验数据", zorder=3)
    xx = np.linspace(0, V.max() * 1.05, 50)
    ax.plot(xx, slope * xx + intercept, color="black", lw=1.4,
            label=f"拟合：斜率={slope:.3g}, 截距={intercept:.3g}")

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    _light_grid(ax)
    ax.legend(loc="best")

    coords = {"过滤数据点 (V, t/V)": _coord_block(["V", "t/V"],
                                            [[vi, yi] for vi, yi in zip(V, y)])}
    result = {"slope": float(slope), "intercept": float(intercept),
              "K_p": float(2 * slope), "coords": coords}
    return fig, ax, result


# ============================================================
# 6. 固液萃取（SLE）直角三角图 + 七步 stepping
# ============================================================

def plot_sle_right_triangle(under_n, under_r, feed_underflow, exit_overflow,
                            final_underflow, fresh_solvent=(0.0, 1.0),
                            labels=("Solute A", "Solvent S", "Solid B"),
                            title="SLE 直角三角图 — 逆流多级", show_construction=False):
    """固液萃取（SLE）直角三角图 + 净流点 Δ + 七步图解 stepping 数级数。

    跟 LLE 的等边三元相图不同：这是直角三角图，x 轴=溶质分数 x_A，y 轴=溶剂分数 x_S，
    固体分数 = 1 - x_A - x_S（斜边 = 固体0）。逆流各级在 underflow 线和 overflow 线
    （斜边）之间走台阶，台阶数 = 理论级数。

    参数
    ----
    under_n  : underflow 夹带数据 —— 溶液中溶质分数 n (kg 溶质/kg 溶液)，升序
    under_r  : 对应夹带量 r (kg 溶液/kg 固体)；恒定夹带就传同一个值的数组
    feed_underflow   : (x_A, x_S) 进料 underflow 组成 x_0
    exit_overflow    : (x_A, x_S) 出口浓 overflow 组成 y_1（落在斜边上）
    final_underflow  : (x_A, x_S) 最终 underflow 组成 x_n（目标）
    fresh_solvent    : (x_A, x_S) 新鲜溶剂 y_{n+1}，默认纯溶剂顶点 (0, 1)
    show_construction : True 时画出全部构造射线（定 Δ 的两条终端线、每条过固体顶点 B
                        的平衡射线、每条指向 Δ 的操作射线）—— 七步法"不跳步"教学图

    返回 (fig, ax, result)，result 含 n_stages / net_flow_point / coords。
    """
    apply_chemeng_style()
    fig, ax = plt.subplots(figsize=(6.5, 6))

    under_n = np.asarray(under_n, dtype=float)
    under_r = np.asarray(under_r, dtype=float)

    # 直角三角三顶点
    V_B = (0.0, 0.0)   # 原点 = 100% 固体 B
    V_A = (1.0, 0.0)   # = 100% 溶质 A
    V_S = (0.0, 1.0)   # = 100% 溶剂 S
    # 三条边
    ax.plot([V_B[0], V_A[0]], [V_B[1], V_A[1]], color="black", lw=1.2, ls="-")  # 溶剂=0
    ax.plot([V_B[0], V_S[0]], [V_B[1], V_S[1]], color="black", lw=1.2, ls="-")  # 溶质=0
    ax.plot([V_A[0], V_S[0]], [V_A[1], V_S[1]], color="black", lw=1.2, ls="-")  # 斜边 固体=0 = overflow 线
    _light_grid(ax)

    # underflow 线：对一串 n 求 U(n)
    def U(n):
        r = float(np.interp(n, under_n, under_r))
        xa, xs = entrainment_to_xy(n, r)
        return (float(xa), float(xs))

    ns = np.linspace(under_n.min(), under_n.max(), 100)
    uxy = np.array([U(n) for n in ns])
    ax.plot(uxy[:, 0], uxy[:, 1], color="black", lw=1.4, ls="--", label="Underflow 线（夹带）")
    # overflow 线 = 斜边
    ax.plot([V_A[0], V_S[0]], [V_A[1], V_S[1]], color="#555555", lw=1.0, ls=":",
            label="Overflow 线（斜边）")

    # 净流点 Δ = 两条端点操作线的交点
    delta = _line_intersect(feed_underflow, exit_overflow, final_underflow, fresh_solvent)

    # 终端点标注
    for p, name in [(feed_underflow, "$x_0$"), (exit_overflow, "$y_1$"),
                    (final_underflow, "$x_n$"), (fresh_solvent, "$y_{n+1}$")]:
        ax.scatter([p[0]], [p[1]], s=40, facecolors="white", edgecolors="black", zorder=4)
        ax.annotate(name, p, textcoords="offset points", xytext=(5, 5), fontsize=9)

    def conc(p):
        s = p[0] + p[1]
        return p[0] / s if s > 1e-12 else 0.0

    n_target = conc(final_underflow)

    # show_construction：画出定 Δ 的两条终端操作线（淡虚线），展示 Δ 怎么来的
    if show_construction and delta is not None:
        for a, b in [(feed_underflow, exit_overflow), (final_underflow, fresh_solvent)]:
            ax.plot([a[0], delta[0]], [a[1], delta[1]], color="#999999", lw=0.6, ls="--", zorder=1)

    # 七步 stepping：从 y_1 开始，平衡(同浓度) ↔ 过 Δ 操作线 交替
    HYP1, HYP2 = V_A, V_S
    corners_under, corners_over = [], [exit_overflow]
    y = exit_overflow
    count = 0
    while count < 50:
        n_y = conc(y)
        x = U(n_y)                      # 平衡：同浓度的 underflow = 一个理论级
        count += 1
        corners_under.append(x)
        # 平衡 tie line：完全混合→同浓度→过固体顶点 B(0,0) 的射线
        if show_construction:
            ax.plot([0, y[0]], [0, y[1]], color="#BBBBBB", lw=0.5, ls=":", zorder=1)  # 过 B 全射线
        ax.plot([y[0], x[0]], [y[1], x[1]], color="black", lw=0.9, ls="-")  # tie line（实段）
        ax.annotate(str(count), x, textcoords="offset points", xytext=(-12, 2), fontsize=8)
        if n_y <= n_target + 1e-9:
            break
        ny = _line_intersect(delta, x, HYP1, HYP2)   # 过 Δ 操作线 ∩ overflow 线
        if ny is None:
            break
        # 操作线：过 Δ —— show_construction 时延长到 Δ（画外会自动裁剪）展示收敛
        if show_construction and delta is not None:
            ax.plot([x[0], delta[0]], [x[1], delta[1]], color="#999999", lw=0.5, ls="--", zorder=1)
        ax.plot([x[0], ny[0]], [x[1], ny[1]], color="black", lw=0.9, ls="-")  # 操作线（实段）
        corners_over.append(ny)
        y = ny

    # Δ 点（可能在三角外）
    if delta is not None:
        ax.scatter([delta[0]], [delta[1]], s=50, marker="x", color="black", zorder=5)
        ax.annotate("Δ", delta, textcoords="offset points", xytext=(6, 4), fontsize=10)

    # 轴范围默认罩住三角形；Δ 在三角形外时扩展到包含 Δ（否则净流点被裁掉，图上看不到）
    x_lo, x_hi, y_lo, y_hi = -0.05, 1.05, -0.05, 1.05
    if delta is not None and np.all(np.isfinite(delta)):
        x_lo = min(x_lo, delta[0] - 0.08)
        x_hi = max(x_hi, delta[0] + 0.08)
        y_lo = min(y_lo, delta[1] - 0.12)
        y_hi = max(y_hi, delta[1] + 0.12)
    ax.set_xlim(x_lo, x_hi)
    ax.set_ylim(y_lo, y_hi)
    ax.set_aspect("equal")
    # 跨度悬殊时按比例拉长画布，防止等比例轴把三角形挤小
    xspan, yspan = x_hi - x_lo, y_hi - y_lo
    if yspan > 1.6 * xspan:
        fig.set_size_inches(6.5, min(12.0, 6.0 * yspan / xspan))
    elif xspan > 1.6 * yspan:
        fig.set_size_inches(min(12.0, 6.5 * xspan / yspan), 6.0)
    ax.set_title(title)
    ax.set_xlabel(f"$x_A$ = {labels[0]} 质量分数")
    ax.set_ylabel(f"$x_S$ = {labels[1]} 质量分数")
    ax.legend(loc="upper right", fontsize=9)

    coords = {
        "Underflow 阶梯点 (x_A, x_S)": _coord_block(["x_A", "x_S"],
                                                 [[a, b] for a, b in corners_under]),
        "Overflow 阶梯点 (x_A, x_S)": _coord_block(["x_A", "x_S"],
                                                [[a, b] for a, b in corners_over]),
        "净流点 Δ (x_A, x_S)": _coord_block(["x_A", "x_S"],
                                          [[delta[0], delta[1]]] if delta else []),
    }
    result = {"n_stages": count, "net_flow_point": delta, "coords": coords}
    return fig, ax, result


# ============================================================
# 7. 湿度图（Psychrometric Chart）
# ============================================================

def plot_psychrometric_chart(points=None, P=101325.0, t_range=(0.0, 50.0),
                             title="湿度图 Psychrometric Chart"):
    """画湿度图：饱和线 + RH 曲线族 + 等湿球/焓斜线，可标状态点并标注读数。

    跟其它函数不同：这是张"读图"用的标准工程图（不是从题目数据画曲线）。
    用 psychrolib（ASHRAE 公式）算物性，1 atm 基准。

    参数
    ----
    points : list[dict] 可选，每个状态点给 Tdb（干球℃）+ 下面之一：
             {"Tdb":30, "RH":0.5}      相对湿度 0-1
             {"Tdb":30, "Twb":22}      湿球温度 ℃
             {"Tdb":30, "Hr":0.012}    湿度比 kg/kg
             会在图上标点 + 标注 (Tdb, Twb, RH, Hr, 焓)。
    P       : 大气压 Pa（默认 101325）
    t_range : 干球温度范围 ℃

    返回 (fig, ax, result)，result["coords"] 含各状态点算全的物性。
    """
    import psychrolib
    psychrolib.SetUnitSystem(psychrolib.SI)

    apply_chemeng_style()
    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    T = np.linspace(t_range[0], t_range[1], 200)

    # 饱和线 (RH=100%)
    Hr_sat = np.array([psychrolib.GetHumRatioFromRelHum(t, 1.0, P) for t in T])
    ax.plot(T, Hr_sat, color="black", lw=1.6, ls="-", label="饱和线 (RH=100%)")

    # RH 曲线族
    for rh in [0.1, 0.2, 0.4, 0.6, 0.8]:
        Hr = np.array([psychrolib.GetHumRatioFromRelHum(t, rh, P) for t in T])
        ax.plot(T, Hr, color="#888888", lw=0.7, ls="-")
        # 在曲线右端标 RH%
        ax.annotate(f"{int(rh*100)}%", (T[-1], Hr[-1]), fontsize=7, color="#888888",
                    textcoords="offset points", xytext=(2, 0))

    # 等湿球/焓斜线（恒 Twb）
    Hr_max = Hr_sat.max()
    for twb in np.arange(np.ceil(t_range[0] / 5) * 5, t_range[1], 5):
        Tline = np.linspace(twb, t_range[1], 30)
        Hr_wb = []
        for t in Tline:
            try:
                Hr_wb.append(psychrolib.GetHumRatioFromTWetBulb(t, twb, P))
            except Exception:
                Hr_wb.append(np.nan)
        ax.plot(Tline, Hr_wb, color="#BBBBBB", lw=0.5, ls="--")

    # 状态点
    rows = []
    if points:
        for pt in points:
            Tdb = pt["Tdb"]
            if "RH" in pt:
                Hr = psychrolib.GetHumRatioFromRelHum(Tdb, pt["RH"], P)
            elif "Twb" in pt:
                Hr = psychrolib.GetHumRatioFromTWetBulb(Tdb, pt["Twb"], P)
            elif "Hr" in pt:
                Hr = pt["Hr"]
            else:
                continue
            RH = psychrolib.GetRelHumFromHumRatio(Tdb, Hr, P)
            Twb = psychrolib.GetTWetBulbFromHumRatio(Tdb, Hr, P)
            h = psychrolib.GetMoistAirEnthalpy(Tdb, Hr) / 1000.0  # J/kg → kJ/kg
            Tdew = psychrolib.GetTDewPointFromHumRatio(Tdb, Hr, P)
            ax.scatter([Tdb], [Hr], s=55, marker="o", color="black", zorder=5)
            ax.annotate(f"Tdb={Tdb}℃\nTwb={Twb:.1f}℃\nRH={RH*100:.0f}%\nH={Hr*1000:.1f}g/kg\nh={h:.1f}kJ/kg",
                        (Tdb, Hr), fontsize=7, textcoords="offset points", xytext=(6, 6),
                        bbox=dict(boxstyle="round", fc="white", ec="#888888", lw=0.5))
            rows.append([Tdb, round(Twb, 2), round(RH, 3), round(Hr, 5), round(h, 2), round(Tdew, 2)])

    ax.set_xlim(*t_range)
    ax.set_ylim(0, Hr_max * 1.05)
    ax.set_title(title)
    ax.set_xlabel("干球温度 Dry-bulb T (℃)")
    ax.set_ylabel("湿度比 Humidity ratio H (kg/kg 干空气)")
    ax.legend(loc="upper left", fontsize=9)

    coords = {"状态点物性": _coord_block(
        ["Tdb℃", "Twb℃", "RH", "H(kg/kg)", "h(kJ/kg)", "Tdew℃"], rows)}
    return fig, ax, {"coords": coords}


# ============================================================
# 8. LLE [D] 系统：部分互溶逆流，等边三角差点 P stepping
# ============================================================

def _cross2d(u, v):
    return u[0] * v[1] - u[1] * v[0]


def plot_lle_d_system(raffinate, extract, F, S, RN, E1=None, S_over_F=None,
                      labels=("Solute A", "Carrier B", "Solvent C"),
                      n_max=30, title="LLE [D] 部分互溶逆流 — 差点 P 图解"):
    """LLE [D] 系统（部分互溶逆流）等边三角差点 P 图解 stepping，数理论级数。

    跟 SLE 净流点同一套思路，但画在 LLE 的等边三元相图上：
    差点 P = line(E1,F) 与 line(RN,S) 的交点；从 E1 起，tie line（平衡）↔ 过 P 射线
    （操作）交替走阶梯，数到 RN 为止。期末最高频题型（知识块 13）。

    参数
    ----
    raffinate, extract : tie-line 配对数据，每点 (A,B,C)，同行 = 一条 tie line
    F  : 进料组成 (A,B,C)（通常在 A-B 边，无溶剂）
    S  : 溶剂组成 (A,B,C)（通常纯溶剂角 (0,0,1)）
    RN : 萃余相离开第 N 级的组成 (A,B,C)（目标，在萃余支上）
    E1 : 萃取相离开第 1 级的组成 (A,B,C)；不给就由 S_over_F 自动算
    S_over_F : 溶剂/进料质量比（E1 没给时必给）—— 定混合点 M → 算 E1

    返回 (fig, ax, result)，result 含 n_stages / difference_point / coords。
    """
    apply_chemeng_style()
    fig, ax = plt.subplots(figsize=(6.5, 6))

    def norm(p):
        p = np.asarray(p, dtype=float)
        return p / p.sum()

    raff = np.array([norm(p) for p in raffinate])
    extr = np.array([norm(p) for p in extract])

    # --- 画三角框 + 网格 + 刻度 + binodal + tie line（同 plot_ternary 风格） ---
    _triangular_grid(ax, step=0.1)
    _triangular_ticks(ax, step=0.2)
    tri = np.array([_TOP, _LEFT, _RIGHT, _TOP])
    ax.plot(tri[:, 0], tri[:, 1], color="black", lw=1.2, ls="-")
    ax.text(_TOP[0], _TOP[1] + 0.05, f"{labels[0]}\n(左边刻度 ↗ wt%)",
            ha="center", va="bottom", fontsize=9)
    ax.text(_LEFT[0] - 0.04, _LEFT[1] - 0.04, f"{labels[1]}\n(底边刻度 wt%)",
            ha="right", va="top", fontsize=9)
    ax.text(_RIGHT[0] + 0.04, _RIGHT[1] - 0.04, f"{labels[2]}\n(右边刻度 wt%)",
            ha="left", va="top", fontsize=9)

    xr, yr = ternary_to_xy(raff[:, 0], raff[:, 1], raff[:, 2])
    xe, ye = ternary_to_xy(extr[:, 0], extr[:, 1], extr[:, 2])
    for i in range(len(xr)):
        ax.plot([xr[i], xe[i]], [yr[i], ye[i]], color="#CCCCCC", lw=0.6, ls="-", zorder=1)
    dome = np.vstack([np.column_stack([xr, yr])[np.argsort(raff[:, 0])],
                      np.column_stack([xe, ye])[np.argsort(extr[:, 0])][::-1]])
    bx, by = _smooth_branch(dome)
    ax.plot(bx, by, color="black", lw=1.2, ls="--", label="Binodal", zorder=2)

    # --- 共轭映射 + 支曲线（按溶质分数 A 参数化） ---
    raA, exA = raff[:, 0], extr[:, 0]
    o_r = np.argsort(raA)
    o_e = np.argsort(exA)
    raA_s, rxy_s = raA[o_r], np.column_stack([xr, yr])[o_r]
    exA_s, exy_s = exA[o_e], np.column_stack([xe, ye])[o_e]

    def raff_xy(xa):
        return np.array([np.interp(xa, raA_s, rxy_s[:, 0]), np.interp(xa, raA_s, rxy_s[:, 1])])

    def extr_xy(ya):
        return np.array([np.interp(ya, exA_s, exy_s[:, 0]), np.interp(ya, exA_s, exy_s[:, 1])])

    def conj_inv(ya):  # 萃取溶质 ya → 共轭萃余溶质 xa（tie line 配对）
        return float(np.interp(ya, exA[o_e], raA[o_e]))

    ya_grid = np.linspace(exA_s.min(), exA_s.max(), 400)

    def _ray_hit_extract(A_pt, B_pt, upper=None):
        """从 A 过 B 的直线与萃取支的交点（按 ya 参数找变号）。"""
        gs = np.array([_cross2d(extr_xy(y) - A_pt, B_pt - A_pt) for y in ya_grid])
        mask = ya_grid < upper if upper is not None else np.ones_like(ya_grid, bool)
        yg, gg = ya_grid[mask], gs[mask]
        if len(yg) < 2:
            return None
        idx = np.where(np.diff(np.sign(gg)) != 0)[0]
        if len(idx) == 0:
            return None
        i0 = idx[-1]
        ya_hit = yg[i0] - gg[i0] * (yg[i0 + 1] - yg[i0]) / (gg[i0 + 1] - gg[i0])
        return ya_hit

    F_xy = np.array(ternary_to_xy(*norm(F)))
    S_xy = np.array(ternary_to_xy(*norm(S)))
    RN_xy = np.array(ternary_to_xy(*norm(RN)))

    # E1：若没给，就由 溶剂比 S_over_F 定混合点 M，再 line(RN,M) ∩ 萃取支求 E1
    if E1 is None:
        if S_over_F is None:
            raise ValueError("E1 和 S_over_F 至少给一个")
        Fn, Sn = norm(F), norm(S)
        M = (Fn + S_over_F * Sn) / (1 + S_over_F)       # 混合点组成
        M_xy = np.array(ternary_to_xy(*M))
        ya_E1 = _ray_hit_extract(RN_xy, M_xy)
        E1_xy = extr_xy(ya_E1)
        ax.scatter([M_xy[0]], [M_xy[1]], s=30, marker="s", color="#555555", zorder=4)
        ax.annotate("M", M_xy, textcoords="offset points", xytext=(4, -10), fontsize=8)
    else:
        ya_E1 = norm(E1)[0]
        E1_xy = np.array(ternary_to_xy(*norm(E1)))

    # --- 差点 P = line(E1,F) ∩ line(RN,S) ---
    P = _line_intersect(E1_xy, F_xy, RN_xy, S_xy)
    P = np.array(P) if P is not None else None

    for pt, name in [(F_xy, "F"), (S_xy, "S"), (E1_xy, "$E_1$"), (RN_xy, "$R_N$")]:
        ax.scatter([pt[0]], [pt[1]], s=40, facecolors="white", edgecolors="black", zorder=4)
        ax.annotate(name, pt, textcoords="offset points", xytext=(5, 4), fontsize=9)

    # --- stepping ---
    ya = ya_E1                       # E1 溶质分数（给的或算的）
    xa_target = norm(RN)[0]          # RN 溶质分数
    stages = 0
    under_pts = []

    xa = conj_inv(ya)
    stages = 1
    ax.plot([extr_xy(ya)[0], raff_xy(xa)[0]], [extr_xy(ya)[1], raff_xy(xa)[1]],
            color="black", lw=0.8, ls="-")
    ax.annotate("1", raff_xy(xa), textcoords="offset points", xytext=(-12, 2), fontsize=8)
    under_pts.append(tuple(raff_xy(xa)))

    while xa > xa_target + 1e-9 and stages < n_max and P is not None:
        R = raff_xy(xa)
        # 操作：过 P 射线与萃取支共线 → 下一个 ya
        gs = np.array([_cross2d(extr_xy(y) - P, R - P) for y in ya_grid])
        mask = ya_grid < ya
        yg, gg = ya_grid[mask], gs[mask]
        sign = np.sign(gg)
        idx = np.where(np.diff(sign) != 0)[0]
        if len(idx) == 0:
            break
        i0 = idx[-1]
        ya_next = yg[i0] - gg[i0] * (yg[i0 + 1] - yg[i0]) / (gg[i0 + 1] - gg[i0])
        E_next = extr_xy(ya_next)
        ax.plot([R[0], E_next[0]], [R[1], E_next[1]], color="black", lw=0.8, ls="-")
        ya = ya_next
        xa = conj_inv(ya)
        stages += 1
        ax.plot([E_next[0], raff_xy(xa)[0]], [E_next[1], raff_xy(xa)[1]],
                color="black", lw=0.8, ls="-")
        ax.annotate(str(stages), raff_xy(xa), textcoords="offset points", xytext=(-12, 2), fontsize=8)
        under_pts.append(tuple(raff_xy(xa)))

    if P is not None:
        ax.scatter([P[0]], [P[1]], s=50, marker="x", color="black", zorder=5)
        ax.annotate("P", P, textcoords="offset points", xytext=(6, 4), fontsize=10)

    # 钳住视图到三角形（差点 P 常落在三角外很远，裁掉不让它撑大画布）
    # 留边距给三条边的刻度数字 + 顶点标注
    ax.set_xlim(-0.14, 1.14)
    ax.set_ylim(-0.14, np.sqrt(3) / 2 + 0.12)
    if P is not None and not (-0.08 <= P[0] <= 1.08 and -0.08 <= P[1] <= 0.95):
        ax.annotate(f"(差点 P 在画外: {P[0]:.2f}, {P[1]:.2f})", (0.02, 0.92),
                    fontsize=8, color="#555555")
    ax.set_title(title)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.legend(loc="upper right", fontsize=9)

    coords = {"萃余阶梯点 R (x,y)": _coord_block(["x", "y"], [[a, b] for a, b in under_pts]),
              "差点 P (x,y)": _coord_block(["x", "y"], [[P[0], P[1]]] if P is not None else [])}
    result = {"n_stages": stages, "difference_point": tuple(P) if P is not None else None,
              "coords": coords}
    return fig, ax, result
