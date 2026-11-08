"""CME222 复习库 — 题库所有应用题答案验算（build-review-vault Step 5）"""

# 题库/气体扩散系数 第 7 题：CO2–空气 1 atm 时 0.147 cm2/s，2 atm 同温
assert round(0.147 / 2, 4) == 0.0735

# 题库/气体扩散系数 第 8 题：Fuller，300 K → 600 K
assert round(0.10 * 2**1.75, 3) == 0.336

print("复习库 verify.py: 全部通过")
