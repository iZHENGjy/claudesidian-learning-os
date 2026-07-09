"""chemeng_plots 验证 + 示例脚本。

拿 CME214 三份 tutorial 的真实数据跑每个画图函数：
1. 存参考 PNG 到 figures/（用户可直接看风格、当手画前的对照标准答案）
2. 同时当回归测试 —— assert 卡 tutorial 已知答案：
   三元点三组分和≈100% / 阶梯≈3级 / 干燥积分≈0.1276 / 过滤拟合对得上

跑法：
    python examples_cme214.py
全部 PASS = 库准确。
"""

import os
import sys

# Windows 控制台默认 GBK，打不出 ✓ 和部分中文 —— 强制 utf-8 输出
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np
import matplotlib

matplotlib.use("Agg")  # 无窗口后端，纯存文件
import chemeng_plots as cp

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(FIG_DIR, exist_ok=True)


def _save(fig, name):
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path)
    print(f"  saved -> figures/{name}")
    return path


# ============================================================
# T01 数据：(溶质 Acetone, 载体 Water, 溶剂) wt%
# ============================================================
# 体系 1：三氯乙烷 / 水 / 丙酮。原表列序 (Cl3, Water, Acetone) → 这里重排成 (A,B,C)
# 萃余相=水层，萃取相=三氯乙烷层
sys1_raff = [(5.96, 93.52, 0.52), (17.04, 82.23, 0.73), (26.92, 72.06, 1.02),
             (30.88, 67.95, 1.17), (35.73, 62.67, 1.60), (40.90, 57.00, 2.10),
             (46.05, 50.20, 3.75), (51.78, 41.70, 6.52)]
sys1_extr = [(8.75, 0.32, 90.93), (25.14, 1.10, 73.76), (38.52, 2.27, 59.21),
             (42.97, 3.11, 53.92), (48.21, 4.26, 47.53), (53.95, 6.05, 40.00),
             (57.40, 8.90, 33.70), (60.34, 13.40, 26.26)]

# 体系 2：异丙醚 / 水 / 丙酮。原表列序 (Acetone, Water, Ether) = 已是 (A,B,C)
sys2_raff = [(0.69, 98.1, 1.2), (2.89, 95.5, 1.6), (6.42, 91.7, 1.9),
             (13.30, 84.4, 2.3), (25.50, 71.7, 3.4), (36.70, 58.9, 4.4),
             (44.30, 45.1, 10.6), (46.40, 37.1, 16.5)]
sys2_extr = [(0.18, 0.5, 99.3), (0.79, 0.8, 98.4), (1.93, 1.0, 97.1),
             (4.82, 1.9, 93.3), (11.40, 3.9, 84.7), (21.60, 6.9, 71.5),
             (31.10, 10.8, 58.1), (36.20, 15.1, 48.7)]


def test_ternary():
    print("[1] plot_ternary (T01)")
    # 断言：每个数据点三组分和 ≈ 100%
    for name, pts in [("sys1_raff", sys1_raff), ("sys1_extr", sys1_extr),
                      ("sys2_raff", sys2_raff), ("sys2_extr", sys2_extr)]:
        for p in pts:
            s = sum(p)
            assert abs(s - 100) < 1.0, f"{name} 点 {p} 三组分和={s:.2f} 偏离 100 太多"
    print("  ✓ 所有数据点三组分和 ≈ 100%")

    fig, ax, res = cp.plot_ternary(sys1_raff, sys1_extr,
                                   labels=("Acetone", "Water", "Trichloroethane"),
                                   title="体系 1：三氯乙烷-水-丙酮 三元相图")
    _save(fig, "ternary_sys1_trichloroethane.png")
    # 演示坐标输出（只打第一张）
    print(cp.coords_table(res))

    fig, ax, res = cp.plot_ternary(sys2_raff, sys2_extr,
                                   labels=("Acetone", "Water", "Isopropyl ether"),
                                   title="体系 2：异丙醚-水-丙酮 三元相图")
    _save(fig, "ternary_sys2_ether.png")


def test_lever_rule():
    print("[1b] lever_rule (T01 Q7 几何)")
    # W=50kg, X=100kg 混合 → M。质量1/质量2 = mass_W/mass_X = 50/100 = 0.5
    W = np.array(cp.ternary_to_xy(21.2, 7.5, 71.5))   # (A,B,C)=(丙酮,水,Cl3)
    X = np.array(cp.ternary_to_xy(36.9, 58.6, 4.5))
    M = (50 * W + 100 * X) / 150
    ratio = cp.lever_rule(M, W, X)
    assert abs(ratio - 0.5) < 0.02, f"lever_rule={ratio:.3f}, 期望 0.5"
    print(f"  ✓ lever_rule(M,W,X)={ratio:.3f} ≈ 0.5 (= 50/100)")


def test_distribution():
    print("[2] plot_distribution (T01 Q4)")
    # 体系1 分配曲线：x=水层丙酮%, y=Cl3层丙酮%
    x1 = [p[0] for p in sys1_raff]
    y1 = [p[0] for p in sys1_extr]
    fig, ax, res = cp.plot_distribution(x1, y1, label="体系1 三氯乙烷",
                                        title="分配曲线 — 体系1 (K>1)")
    # 断言：体系1 曲线在 y=x 上方（y>x）
    assert all(b > a for a, b in zip(x1, y1)), "体系1 应 y>x（K>1）"
    _save(fig, "distribution_sys1.png")

    x2 = [p[0] for p in sys2_raff]
    y2 = [p[0] for p in sys2_extr]
    # 断言：体系2 曲线在 y=x 下方（y<x）
    assert all(b < a for a, b in zip(x2, y2)), "体系2 应 y<x（K<1）"
    print("  ✓ 体系1 在 y=x 上方、体系2 在下方")


def test_mccabe_thiele():
    print("[3] plot_mccabe_thiele (T02 Q1c 逆流)")
    # 平衡曲线（×10⁻³）
    eq_x = np.array([0, 1.011, 2.460, 5.02, 7.51, 9.98, 12.4]) * 1e-3
    eq_y = np.array([0, 1.907, 3.961, 5.96, 7.86, 9.31, 9.7]) * 1e-3
    # 逆流操作线：raffinate 端 (X_3, 0)=(1.058e-3, 0)，feed 端 (X_f, Y_1)=(10.101e-3, 7.461e-3)
    op_lo = (1.058e-3, 0.0)
    op_hi = (10.101e-3, 7.461e-3)
    fig, ax, res = cp.plot_mccabe_thiele(eq_x, eq_y, op_lo, op_hi, n_stages=3,
                                         title="T02 Q1(c) 逆流 3 级阶梯法")
    # 断言：走 3 级后最终 X ≈ X_3 = 1.058e-3（容差 25%，图解精度）
    xf = res["x_final"]
    assert res["n_stages"] == 3
    assert abs(xf - 1.058e-3) < 0.25 * 1.058e-3, \
        f"3 级后 X_final={xf*1e3:.3f}e-3，期望 ≈1.058e-3"
    print(f"  ✓ 3 级阶梯 → X_final={xf*1e3:.3f}×10⁻³ ≈ 1.058×10⁻³")
    _save(fig, "mccabe_thiele_countercurrent.png")


def test_drying_curve():
    print("[4] plot_drying_curve (T03)")
    # R-X 差分数据（X_avg, R）
    X = [0.2548, 0.2368, 0.2121, 0.1784, 0.1392, 0.0976, 0.0639, 0.0344, 0.0116, 0.0031]
    R = [0.79, 1.03, 0.98, 0.97, 1.01, 0.73, 0.61, 0.35, 0.11, 0.04]
    fig, ax, res = cp.plot_drying_curve(X, R, X_c=0.14, X_2=0.05, R_c=1.0,
                                        title="T03 干燥速率曲线 R-X")
    integ = res["falling_integral"]
    # 断言：降速段积分 ≈ 0.1276（笔记梯形答案，容差 15%）
    assert abs(integ - 0.1276) < 0.15 * 0.1276, \
        f"降速段积分={integ:.4f}，期望 ≈0.1276"
    print(f"  ✓ 降速段 ∫dX/R={integ:.4f} ≈ 0.1276")
    _save(fig, "drying_curve.png")


def test_filtration():
    print("[5] plot_filtration_linear (合成线性数据)")
    # 构造 t/V = 2.0·V + 5.0 + 小噪声
    rng = np.random.default_rng(0)
    V = np.linspace(0.1, 1.0, 8)
    tV = 2.0 * V + 5.0 + rng.normal(0, 0.02, len(V))
    fig, ax, res = cp.plot_filtration_linear(V, tV)
    assert abs(res["slope"] - 2.0) < 0.1, f"斜率={res['slope']:.3f}，期望 2.0"
    assert abs(res["intercept"] - 5.0) < 0.1, f"截距={res['intercept']:.3f}，期望 5.0"
    print(f"  ✓ 拟合斜率={res['slope']:.3f}≈2.0, 截距={res['intercept']:.3f}≈5.0")
    _save(fig, "filtration_linear.png")


def test_sle_right_triangle():
    print("[6] plot_sle_right_triangle (SLE 直角三角图)")
    # 构造恒定夹带逆流洗涤：r=0.4 恒定，feed 浓度 0.5，目标 0.05，R=w/W=1.5
    r_const = 0.4
    under_n = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
    under_r = np.full_like(under_n, r_const)
    x0 = tuple(float(v) for v in cp.entrainment_to_xy(0.5, r_const))   # feed underflow
    xn = tuple(float(v) for v in cp.entrainment_to_xy(0.05, r_const))  # final underflow
    # 浓度空间操作线斜率 = W/w = 1/R = 0.667；y1 浓度 = 0 + (1/R)(0.5-0.05) = 0.30
    y1 = (0.30, 0.70)            # 出口 overflow（斜边上）
    solv = (0.0, 1.0)           # 纯溶剂

    fig, ax, res = cp.plot_sle_right_triangle(under_n, under_r, x0, y1, xn, solv,
                                              title="SLE 直角三角图（恒定夹带逆流）")
    n_tri = res["n_stages"]

    # 交叉验证：同一问题在浓度空间 = 平衡线45° 的 McCabe 阶梯
    fig2, ax2, res2 = cp.plot_mccabe_thiele([0, 1], [0, 1], (0.05, 0.0), (0.5, 0.30),
                                            title="SLE 浓度空间等价 McCabe（验证用）")
    n_mcc = res2["n_stages"]

    assert n_tri == n_mcc, f"直角三角 stepping={n_tri} 级，但浓度空间 McCabe={n_mcc} 级，不一致"
    # 几何自检：underflow 阶梯点应落在恒定夹带线 x_A+x_S = r/(1+r)
    line_val = r_const / (1 + r_const)
    for a, b in res["coords"]["Underflow 阶梯点 (x_A, x_S)"]["rows"]:
        assert abs((a + b) - line_val) < 1e-6, f"underflow 点 ({a},{b}) 不在夹带线上"
    print(f"  ✓ 直角三角 stepping={n_tri} 级 == 浓度空间 McCabe={n_mcc} 级（两套独立实现对上）")
    print(f"  ✓ underflow 阶梯点都落在恒定夹带线 x_A+x_S={line_val:.3f} 上")
    _save(fig, "sle_right_triangle.png")


def test_lle_d_system():
    print("[8] plot_lle_d_system (L01 [D] 差点 stepping)")
    # 近不互溶合成体系，K=2 → 极限下应与 [C] McCabe 一致
    ms = 0.005
    xs = [0.02, 0.04, 0.06, 0.08, 0.10, 0.12]
    raff = [(x, 1 - x - ms, ms) for x in xs]
    extr = [(2 * x, ms, 1 - 2 * x - ms) for x in xs]
    F = (0.12, 0.88, 0); S = (0, 0, 1)
    E1 = (0.18, ms, 1 - 0.18 - ms); RN = (0.02, 1 - 0.02 - ms, ms)

    fig, ax, res = cp.plot_lle_d_system(raff, extr, F, S, RN, E1=E1,
                                        labels=("Solute", "Carrier", "Solvent"),
                                        title="[D] 部分互溶逆流 — 差点 P 图解")
    n_d = res["n_stages"]
    # 交叉验证：溶质空间 = eq(y=2x) 的 McCabe 阶梯
    fig2, ax2, r2 = cp.plot_mccabe_thiele([0, 0.12], [0, 0.24], (0.02, 0.0), (0.12, 0.18))
    n_m = r2["n_stages"]
    assert n_d == n_m, f"[D] 差点 stepping={n_d} 级，但近不互溶 McCabe={n_m} 级，不一致"
    print(f"  ✓ [D] 差点 stepping={n_d} 级 == 近不互溶 McCabe={n_m} 级（交叉验证）")

    # 用 T01 真实三氯乙烷体系画一张清晰可读的 demo：给溶剂比，E1 自动算
    fig_d, ax_d, res_d = cp.plot_lle_d_system(
        sys1_raff, sys1_extr, F=(40, 60, 0), S=(0, 0, 100),
        RN=(5.96, 93.52, 0.52), S_over_F=0.5,
        labels=("Acetone", "Water", "Trichloroethane"),
        title="[D] 差点图解 demo（三氯乙烷-水-丙酮）")
    print(f"  · T01 体系 demo（S/F=0.5）：{res_d['n_stages']} 级")
    _save(fig_d, "lle_d_system.png")


def test_psychrometric():
    print("[7] plot_psychrometric_chart (L03 湿度图)")
    fig, ax, res = cp.plot_psychrometric_chart(
        points=[{"Tdb": 30, "RH": 0.5}, {"Tdb": 40, "Twb": 25}],
        title="湿度图 — 示例两个状态点")
    # 断言：30℃/50%RH 的湿度比 ≈ 0.0133（标准湿度图读数）
    Tdb, Twb, RH, Hr, h, Tdew = res["coords"]["状态点物性"]["rows"][0]
    assert abs(Hr - 0.0133) < 0.001, f"30℃/50%RH 湿度比={Hr}，期望 ≈0.0133"
    assert 60 < h < 70, f"30℃/50%RH 焓={h} kJ/kg，期望 ~64"
    print(f"  ✓ 30℃/50%RH → H={Hr*1000:.1f} g/kg, 焓={h:.1f} kJ/kg（对标准湿度图）")
    _save(fig, "psychrometric_chart.png")


if __name__ == "__main__":
    test_ternary()
    test_lever_rule()
    test_distribution()
    test_mccabe_thiele()
    test_drying_curve()
    test_filtration()
    test_sle_right_triangle()
    test_lle_d_system()
    test_psychrometric()
    print("\n所有验证 PASS ✓  参考图在 figures/")
