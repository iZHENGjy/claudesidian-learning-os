"""CME222 L03 — 所有实例数字验算（ingest-lecture Step 4.5）"""
import math

# Neufeld 碰撞积分关联式，常数取自课件 p.26
A, B, C, D = 1.06036, 0.15610, 0.19300, 0.47635
E, F, G, H = 1.03587, 1.52996, 1.76474, 3.89411


def omega(ts):
    return A / ts**B + C / math.exp(D * ts) + E / math.exp(F * ts) + G / math.exp(H * ts)


def hirschfelder(T, P_atm, MA, MB, sAB, om):
    """课件 p.18：D [cm2/s]，T [K]，P [atm]，M [g/mol]，sigma [Å]"""
    return 0.001858 * T**1.5 * (1 / MA + 1 / MB) ** 0.5 / (P_atm * sAB**2 * om)


# Neufeld 对照课件 p.19 曲线：T*=2 时约 1.07、T*=10 时约 0.75
assert abs(omega(2.0) - 1.075) < 0.01 and abs(omega(10.0) - 0.742) < 0.01

# 实例 1：CO2–空气，293 K，1 atm（LJ 参数：CO2 3.996 Å / 190 K；空气 3.617 Å / 97.0 K）
sAB1 = (3.996 + 3.617) / 2
eAB1 = math.sqrt(190 * 97.0)
ts1 = 293 / eAB1
om1 = omega(ts1)
D1 = hirschfelder(293, 1, 44, 29, sAB1, om1)
assert round(sAB1, 3) == 3.806 and round(eAB1, 1) == 135.8 and round(ts1, 3) == 2.158
assert round(om1, 3) == 1.048
assert round(D1, 4) == 0.1468
# 表 J.1：CO2–空气 273 K，D·P = 0.136 cm2·atm/s，用课件 p.20 外推到 293 K
om273 = omega(273 / eAB1)
D1_exp = 0.136 * (293 / 273) ** 1.5 * om273 / om1
assert round(D1_exp, 4) == 0.1549
assert round(abs(D1 - D1_exp) / D1_exp * 100, 1) == 5.2   # 估算比实验外推值低约 5.2%

# 实例 2：苯–空气，303 K，1 atm，Fuller（扩散体积取自课件 p.23）
v_benzene = 6 * 16.5 + 6 * 1.98 - 20.2
assert round(v_benzene, 2) == 90.68
D2 = 1e-3 * 303**1.75 * (1 / 78 + 1 / 29) ** 0.5 / (1 * (v_benzene ** (1 / 3) + 20.1 ** (1 / 3)) ** 2)
assert round(D2, 4) == 0.0920
# 表 J.1：苯–空气 298 K 为 0.0962 cm2/s；Fuller 的 T^1.75 外推到 303 K
D2_exp = 0.0962 * (303 / 298) ** 1.75
assert round(D2_exp, 4) == 0.0990

# 实例 3：NH3–空气，373 K，101325 Pa，Brokaw（Vb：NH3 25.8、空气 29.9 cm3/mol，待核实）
delta_A = 1.94e3 * 1.46**2 / (25.8 * 239.81)
assert round(delta_A, 3) == 0.668
sA = (1.585 * 25.8 / (1 + 1.3 * delta_A**2)) ** (1 / 3)
sB = (1.585 * 29.9) ** (1 / 3)
eA = 1.18 * (1 + 1.3 * delta_A**2) * 239.81
eB = 1.18 * 78.8
assert round(sA, 3) == 2.958 and round(sB, 3) == 3.619 and round(math.sqrt(sA * sB), 3) == 3.272
assert round(eA, 1) == 447.3 and round(eB, 1) == 93.0
delta_AB = math.sqrt(delta_A * 0.0)
sAB3 = math.sqrt(sA * sB)          # Brokaw：几何平均（课件 p.26），不是算术平均
ts3 = 373 / math.sqrt(eA * eB)
om3 = omega(ts3) + 0.196 * delta_AB**2 / ts3
D3 = hirschfelder(373, 1, 17, 29, sAB3, om3)
assert round(ts3, 3) == 1.829 and round(om3, 3) == 1.110
assert round(D3, 3) == 0.344

# 实例 4：SiH4 在 H2/N2 混合气中，900 K，100 Pa（H2 2.968 Å / 33.3 K；N2 3.681 Å / 91.5 K）
P4 = 100 / 101325
D_SiH4_H2 = hirschfelder(900, P4, 32.1, 2.016, (4.08 + 2.968) / 2, omega(900 / math.sqrt(207.6 * 33.3)))
D_SiH4_N2 = hirschfelder(900, P4, 32.1, 28, (4.08 + 3.681) / 2, omega(900 / math.sqrt(207.6 * 91.5)))
yH2p = 0.015 / (1 - 0.0075)
yN2p = 0.9775 / (1 - 0.0075)
assert round(yH2p, 4) == 0.0151 and round(yN2p, 4) == 0.9849
D_mix = 1 / (yH2p / D_SiH4_H2 + yN2p / D_SiH4_N2)
assert round(D_SiH4_H2) == 4059 and round(D_SiH4_N2) == 1091
assert round(D_mix) == 1104

print("verify.py: 全部通过")
for k, v in [("D1", D1), ("D1_exp", D1_exp), ("D2", D2), ("D2_exp", D2_exp), ("D3", D3),
             ("D_SiH4_H2", D_SiH4_H2), ("D_SiH4_N2", D_SiH4_N2), ("D_mix", D_mix), ("om3", om3)]:
    print(f"{k} = {v:.4f}")
