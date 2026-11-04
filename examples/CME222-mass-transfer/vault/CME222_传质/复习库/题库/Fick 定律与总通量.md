---
type: question-bank
course: "CME222"
topic: "Fick 定律与总通量"
sources: ["[[L02_diffusive_mass_transfer]]", "[[T01_membrane_diffusion]]"]
---

# Fick 定律与总通量 · 题库（10 题）

> [!hint]- 本主题核心套路（先自己想，再点开）
> | 看到 | 想到 |
> |---|---|
> | 两端浓度 + 距离 | $J = D\Delta c/L$（稳态线性分布） |
> | 相对静止点 | 用总通量 $N_A$ |
> | 稀溶液 | 对流项可忽略，$N_A \approx J_A$ |

---

## 第 1 题 [记忆] Fick 第一定律
写出 z 方向一维 Fick 第一定律。

> [!answer]- 看答案
> $J_{A,z} = -D_{AB}\,dc_A/dz$。

考点：[[L02_diffusive_mass_transfer#知识块 5 — Fick 第一定律:从历史定义出发]]

---

## 第 2 题 [记忆] 适用条件
课件给出的 Fick 第一定律适用于什么体系？

> [!answer]- 看答案
> 等温、等压的二元体系。

考点：[[L02_diffusive_mass_transfer#知识块 5 — Fick 第一定律:从历史定义出发]]

---

## 第 3 题 [记忆] 用摩尔分数写
用摩尔分数梯度写摩尔扩散通量。

> [!answer]- 看答案
> $J_{A,z} = -cD_{AB}\,dy_A/dz$。

考点：[[L02_diffusive_mass_transfer#知识块 6 — Fick 第一定律的 4 种等价形式]]

---

## 第 4 题 [记忆] 两种贡献
通量由哪两部分贡献？

> [!answer]- 看答案
> 浓度梯度（扩散）和整体流动（对流）。

考点：[[L02_diffusive_mass_transfer#知识块 9 — 通量两个来源:扩散贡献 + 对流贡献]]

---

## 第 5 题 [记忆] 总通量公式
写出摩尔总通量的向量形式。

> [!answer]- 看答案
> $\mathbf N_A = -cD_{AB}\nabla y_A + y_A(\mathbf N_A + \mathbf N_B)$。

考点：[[L02_diffusive_mass_transfer#知识块 9 — 通量两个来源:扩散贡献 + 对流贡献]]

---

## 第 6 题 [记忆] 致密膜
致密膜的溶解-扩散模型中，通量公式是什么？

> [!answer]- 看答案
> $J_A = D_{AB}S\Delta p/L$，其中 $S$ 为溶解度系数。

考点：[[T01_membrane_diffusion#Problem 1 — 氢气穿过 4 bar / 1 bar 的膜]]

---

## 第 7 题 [应用] 管长加倍
298 K、1 atm，He 两端分压 0.6 atm 和 0.2 atm，$D = 0.687\times10^{-4}$ m²/s，管长 0.4 m。求 He 的摩尔通量。

> [!answer]- 看答案
> ① 公式：$c = P/RT$，$J = D\Delta c/L$
> ② 代数：$c_1 = 24.54$，$c_2 = 8.18$ mol/m³；$J = 0.687\times10^{-4}\times16.36/0.4$
> ③ 结果：$J = 2.81\times10^{-3}$ mol/(m²·s)

考点：[[L02_diffusive_mass_transfer#知识块 7 — Example 3:He-N₂ 管中扩散]]

---

## 第 8 题 [应用] 质量通量的单位
碳在铁中 $D = 5\times10^{-11}$ m²/s，相距 4 mm 的两点浓度差 40 mol/m³。求碳的质量扩散通量（kg/(m²·s)）。

> [!answer]- 看答案
> ① 公式：$J = D\Delta c/\Delta z$，$j = JM$
> ② 代数：$J = 5\times10^{-11}\times40/0.004 = 5\times10^{-7}$ mol/(m²·s)；$M_C = 0.012$ kg/mol
> ③ 结果：$j = 6\times10^{-9}$ kg/(m²·s)

考点：[[L02_diffusive_mass_transfer#知识块 8 — Example 4:钢板渗碳扩散]]

---

## 第 9 题 [分析] 均匀组成的流动
组成处处相同的气体以 0.03 m/s 流过管道。$J_A$ 是否为零？$N_A$ 呢？

> [!answer]- 看答案
> $J_A = 0$（没有浓度梯度），但 $N_A \ne 0$：A 全部被整体流动带走，$N_A = y_A(N_A + N_B)$。

考点：[[L02_diffusive_mass_transfer#知识块 9 — 通量两个来源:扩散贡献 + 对流贡献]]

---

## 第 10 题 [分析] 何时 N_A ≈ J_A
大气中的微量污染物扩散，和水蒸发进静止空气，哪种情况可以用 $N_A \approx J_A$？为什么？

> [!answer]- 看答案
> 微量污染物可以：$y_A \to 0$，对流项可忽略。蒸发时水蒸气不稀、空气 $N_B = 0$，对流项不能忽略（单向扩散）。

考点：[[L02_diffusive_mass_transfer#知识块 11 — 何时简化(后面常用)]]
