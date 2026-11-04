"""CME222 复习库 — 题库所有应用题答案验算（build-review-vault Step 5）"""
import math
from fractions import Fraction as F

# 题库/浓度与速度 第 7 题：50/50 mol% H2–CO2 中 H2 的质量分数
w = F(1, 2) * 2 / (F(1, 2) * 2 + F(1, 2) * 44)
assert w == F(1, 23) and round(float(w), 4) == 0.0435

# 题库/浓度与速度 第 8 题：80 mol% N2 @0.020 m/s，20 mol% H2 @0.050 m/s
V = F(8, 10) * F(2, 100) + F(2, 10) * F(5, 100)
assert V == F(26, 1000)
wN2 = F(8, 10) * 28 / (F(8, 10) * 28 + F(2, 10) * 2)
wH2 = 1 - wN2
v = wN2 * F(2, 100) + wH2 * F(5, 100)
assert round(float(v), 4) == 0.0205

# 题库/Fick 定律与总通量 第 7 题：He–N2 管长加倍到 0.4 m
R, ATM = 8.314, 101325.0
c1, c2 = 0.6 * ATM / (R * 298), 0.2 * ATM / (R * 298)
J = 0.687e-4 * (c1 - c2) / 0.4
assert round(J * 1e3, 2) == 2.81

# 题库/Fick 定律与总通量 第 8 题：D = 5e-11 m2/s，Δc = 40 mol/m3，Δz = 4 mm，碳
J = 5e-11 * 40 / 0.004
assert math.isclose(J, 5e-7)
assert math.isclose(J * 0.012, 6e-9)

# 题库/气体扩散系数 第 7 题：CO2–空气 1 atm 时 0.147 cm2/s，2 atm 同温
assert round(0.147 / 2, 4) == 0.0735

# 题库/气体扩散系数 第 8 题：Fuller，300 K → 600 K
assert round(0.10 * 2**1.75, 3) == 0.336

# 题库/液体扩散系数 第 7 题：Stokes–Einstein，r = 2 nm，298 K，水 0.89 mPa·s
D = 1.38e-23 * 298 / (6 * math.pi * 2e-9 * 0.89e-3)
assert round(D * 1e10, 2) == 1.23

# 题库/液体扩散系数 第 8 题：Wilke–Chang，水 Φ=2.26，M=18，298 K，μ=0.89 cP，V_A=75.6 cm3/mol
D = 7.4e-8 * 298 * (2.26 * 18) ** 0.5 / (75.6**0.6 * 0.89)
assert round(D * 1e5, 2) == 1.18

# 题库/固体与多孔介质 第 7 题：Knudsen，d = 10 nm = 1e-6 cm，300 K，M = 28
DK = 4850 * 1e-6 * math.sqrt(300 / 28)
assert round(DK, 4) == 0.0159

# 题库/固体与多孔介质 第 8 题：受阻扩散 φ = 0.2
phi = 0.2
F1 = (1 - phi) ** 2
F2 = 1 - 2.104 * phi + 2.09 * phi**3 - 0.95 * phi**5
assert round(F1, 2) == 0.64 and round(F2, 4) == 0.5956 and round(F1 * F2, 3) == 0.381

print("复习库 verify.py: 全部通过")
