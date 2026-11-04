---
type: tutorial
course: "CME222"
week: 6
tutorial: 3
topics: ["液相 D 估算", "固相 Arrhenius", "Knudsen + 多孔扩散", "Hindered diffusion"]
related_lectures: ["[[L03_diffusion_coefficient_estimation]]", "[[L04_liquid_solid_pore_diffusivity]]"]
---

# Tutorial 3 — 液相 / 固相 / 多孔扩散综合题

> [!info]
> - **所属课程**: [[CME222]]
> - **关联笔记**: [[L04_liquid_solid_pore_diffusivity]]（覆盖 9 题里 8 题的核心公式）
> - **核心主题**: 这是 L04 全部公式的"实战练习"

---

## 本次公式速查

| 公式 | 用途 | 来源 |
|---|---|---|
| $D_{AB} = \dfrac{kT}{6\pi r \mu_B}$ | Stokes-Einstein，球形大分子 | [[L04_liquid_solid_pore_diffusivity]] 知识块 2 |
| $D_{AB} = 7.4\times 10^{-8}\dfrac{T(\Phi_B M_B)^{1/2}}{V_A^{0.6}\mu_B}$ | Wilke-Chang | 知识块 3 |
| $D_{AB} = \dfrac{KT}{\mu_B V_A^{1/3}}$, $K = 8.2\times 10^{-8}[1+(3V_B/V_A)^{2/3}]$ | Scheibel | 知识块 5 |
| $D\mu = (D^\circ_{AB}\mu_B)^{x_B}(D^\circ_{BA}\mu_A)^{x_A}$ | Leffler-Cullinan（浓溶液） | 知识块 5 |
| $\dfrac{D_1}{D_2} = \left(\dfrac{T_c-T_2}{T_c-T_1}\right)^n$ | Tyn-Calus 温度外推 | 知识块 5 |
| $D = \dfrac{2RT}{(1/\lambda^\circ_+ + 1/\lambda^\circ_-)F^2}$ | Nernst（一价电解质） | 知识块 6 |
| $D = D_o e^{-Q/RT}$；$\ln D = \ln D_o - (Q/R)/T$ | Arrhenius 固相 | 知识块 8 |
| $D_{KA} = 4850\, d_{pore} \sqrt{T/M_A}$（cgs） | Knudsen | 知识块 11 |
| $\dfrac{1}{D_{Ae}} = \dfrac{1-\alpha y_A}{D_{AB}} + \dfrac{1}{D_{KA}}$，$\alpha = 1+N_B/N_A$ | 混合扩散 | 知识块 12 |
| $D'_{Ae} = \varepsilon^2 D_{Ae}$ | 多孔曲折修正 | 知识块 13 |
| $D_{Ae} = D^\circ_{AB} F_1(\phi) F_2(\phi)$；$\phi = d_s/d_{pore}$ | Hindered | 知识块 14 |
| $F_1 = (1-\phi)^2$；$F_2 = 1 - 2.104\phi + 2.09\phi^3 - 0.95\phi^5$ | Hindered 因子 | 知识块 14 |

## 本次数据与常数

| 量 | 值 |
|---|---|
| $k$（Boltzmann） | $1.38\times 10^{-23}$ J/K |
| $R$ | 8.314 J/(mol·K) |
| $F$（Faraday） | 96500 C/mol |
| $\Phi_{water}$ | 2.26 |
| $\Phi_{methanol}$ | 1.9 |
| $\Phi_{ethanol}$ | 1.5 |
| $V_b$（water） | 18.9 cm³/mol |
| $V_b$（methanol） | 42 cm³/mol（查 Welty 附录） |

---

## Problem 1 — Stokes-Einstein 反推蛋白直径

> (原题) 血清白蛋白（serum albumin）在水中无限稀释扩散系数 = $5.94\times 10^{-7}$ cm²/s at 293 K。$\mu_{water} = 1$ cP。求白蛋白分子的平均直径。

**思路**：球形大分子 → Stokes-Einstein。反推 $r$ 然后乘 2 得直径。

### 解答

$$r = \frac{kT}{6\pi \mu_B D_{AB}}$$

**单位 SI**：$\mu_B = 1$ cP = $10^{-3}$ Pa·s；$D = 5.94\times 10^{-7}$ cm²/s = $5.94\times 10^{-11}$ m²/s

$$r = \frac{1.38\times 10^{-23} \times 293}{6\pi \times 10^{-3} \times 5.94\times 10^{-11}}$$

$$= \frac{4.043\times 10^{-21}}{1.120\times 10^{-12}} = 3.61\times 10^{-9} \text{ m} = 3.61 \text{ nm}$$

**直径**：$\boxed{d = 2r \approx 7.2 \text{ nm}}$

> 实际血清白蛋白直径约 7-8 nm（hydrodynamic radius），结果合理。

### 易错

> [!warning]
> - $\mu$ 单位：1 cP = $10^{-3}$ Pa·s（不是 1 Pa·s）
> - $D$ 单位：题目 cm²/s，套 SI 公式要换 m²/s（÷ $10^4$）
> - 求"直径"不是"半径"（× 2）

---

## Problem 2 — 三个液相 D 估算

> (原题) 估下列稀溶液 D：
> (a) Methanol 在 water 中, 283 K
> (b) Chloroform 在 ethanol 中：293 K 时 $D = 1.25\times 10^{-5}$ cm²/s，预测 400 K
> (c) KOH 在 water 中, 298 K
>
> 数据：$\mu_{ethanol}(293)=1.188$ cP，$\mu_{water}(283)=1.3133$ cP，$T_c$(ethanol) = 516.3 K，$\Delta H_v$(ethanol) = 38.58 kJ/mol

### (a) Methanol → water at 283 K：Wilke-Chang

**数据**：$M_B = 18$, $\Phi_B = 2.26$, $V_A$(methanol) = 42 cm³/mol（Welty 附录），$\mu_B = 1.3133$ cP

$$D = \frac{7.4\times 10^{-8} \times 283 \times (2.26 \times 18)^{1/2}}{42^{0.6} \times 1.3133}$$

$$= \frac{7.4\times 10^{-8} \times 283 \times 6.382}{9.587 \times 1.3133} = \frac{7.4\times 10^{-8} \times 1806.1}{12.59}$$

$$\boxed{D \approx 1.06\times 10^{-5} \text{ cm}^2/\text{s}}$$

### (b) Chloroform-ethanol：Tyn-Calus 温度外推

**数据**：$T_1 = 293$, $T_2 = 400$, $T_c = 516.3$, $\Delta H_v = 38580$ J/mol

$\Delta H_v$ 在 30,000–39,000 范围 → **$n = 4$**

$$\frac{D_1}{D_2} = \left(\frac{T_c - T_2}{T_c - T_1}\right)^n = \left(\frac{516.3 - 400}{516.3 - 293}\right)^4 = \left(\frac{116.3}{223.3}\right)^4$$

$$= (0.5208)^4 = 0.0735$$

$$D_2 = \frac{D_1}{0.0735} = \frac{1.25\times 10^{-5}}{0.0735}$$

$$\boxed{D(400 \text{ K}) \approx 1.70\times 10^{-4} \text{ cm}^2/\text{s}}$$

> 升温 100 K 让 D 增大约 14 倍 — 因为 400 K 接近溶剂临界温度 516 K，扩散加速。

### (c) KOH → water at 298 K：Nernst

KOH 是强电解质 → 完全解离 K⁺ + OH⁻，**一价**。

$\lambda^\circ_{K^+} = 73.5$，$\lambda^\circ_{OH^-} = 197.6$（PPT slide 22）

$$\frac{1}{\lambda^\circ_+} + \frac{1}{\lambda^\circ_-} = \frac{1}{73.5} + \frac{1}{197.6} = 0.01867$$

$$D = \frac{2RT}{[1/\lambda^\circ_+ + 1/\lambda^\circ_-] F^2} = \frac{2 \times 8.314 \times 298}{0.01867 \times (96500)^2}$$

$$= \frac{4955}{0.01867 \times 9.31\times 10^9} = \frac{4955}{1.738\times 10^8}$$

$$\boxed{D \approx 2.85\times 10^{-5} \text{ cm}^2/\text{s}}$$

> KOH 的 D 比 NaCl 大很多（因为 OH⁻ 走质子跳跃机制）。

### 易错

> [!warning]
> - 三小题用三个不同公式 — 看清"题目暗示"：单一稀液 → Wilke-Chang；温度外推 → Tyn-Calus；离子 → Nernst
> - Tyn-Calus 的 $n$ **看 $\Delta H_v$ 范围查表**，不是猜
> - Nernst 单位地狱：$\lambda^\circ$ 单位 A/cm² (= cm²·S/mol)，$F$ = 96500，单位匹配后 $D$ 是 cm²/s

---

## Problem 3 — Scheibel：苯在乙醇中

> (原题) 苯加到乙醇里使其变性。估 288 K 下 $D_{benzene-ethanol}$，用 Scheibel。$\mu_{ethanol} = 1.3079$ cP, $\mu_{benzene} = 0.7128$ cP。

**注意**：苯是**溶质**，乙醇是溶剂 → $\mu_B = \mu_{ethanol} = 1.3079$ cP

### 解答

**摩尔体积**（用 [[L04_liquid_solid_pore_diffusivity]] 知识块 4 加和）：
- 苯（C₆H₆）：$V_A = 6 \times 14.8 + 6 \times 3.7 - 15 = 96$ cm³/mol（减苯环）
- 乙醇（C₂H₆O）：$V_B = 2 \times 14.8 + 6 \times 3.7 + 7.4 = 59$ cm³/mol（O 用 7.4）

**Scheibel 例外检查**（[[L04_liquid_solid_pore_diffusivity]] 知识块 5）：

苯不是溶剂（题目里苯是 solute），所以适用"其他有机溶剂"分支：

$2.5 V_B = 2.5 \times 59 = 147.5$；$V_A = 96 < 147.5$ → **使用 $K = 17.5\times 10^{-8}$**

**代入**：

$$D_{AB} = \frac{17.5\times 10^{-8} \times 288}{1.3079 \times 96^{1/3}} = \frac{17.5\times 10^{-8} \times 288}{1.3079 \times 4.579}$$

$$= \frac{5.04\times 10^{-5}}{5.99}$$

$$\boxed{D \approx 8.42\times 10^{-6} \text{ cm}^2/\text{s}}$$

### 易错

> [!warning]
> - **苯做溶剂 vs 苯做溶质**例外不同。这里苯是溶质所以走"其他有机溶剂"
> - $V_A < 2 V_B$ 走苯做溶剂分支（$K = 18.9\times 10^{-8}$）；$V_A < 2.5 V_B$ 走其他（$K = 17.5\times 10^{-8}$）
> - 不满足例外条件就用通用 $K = 8.2\times 10^{-8}[1 + (3V_B/V_A)^{2/3}]$

---

## Problem 4 — Leffler-Cullinan 浓溶液

> (原题) 25°C，methanol(A)-water(B)，$x_A = 0.35$。$\mu_A = 0.5459$ cP，$\mu_B = 0.8911$ cP，$\mu_{mix} = 1.536$ cP。求 $D_{AB}$。

**关键**：$x_A = 0.35$ 不是稀溶液（无限稀释只 < 0.05）→ **必须用 Leffler-Cullinan**。

### 解答

**Step 1：先用 Wilke-Chang 算两端的 $D^\circ$**

$D^\circ_{AB}$（methanol 在 water 中无限稀释）：
- $V_A$(methanol) = 42, $\Phi_B = 2.26$, $M_B = 18$, $\mu_B = 0.8911$ cP, $T = 298$

$$D^\circ_{AB} = \frac{7.4\times 10^{-8} \times 298 \times (2.26 \times 18)^{1/2}}{42^{0.6} \times 0.8911} = \frac{7.4\times 10^{-8} \times 298 \times 6.382}{9.587 \times 0.8911}$$

$$\approx 1.65\times 10^{-5} \text{ cm}^2/\text{s}$$

$D^\circ_{BA}$（water 在 methanol 中无限稀释）：
- $V_B$(water) = 18.9, $\Phi_A = 1.9$（methanol 做溶剂！）, $M_A = 32$, $\mu_A = 0.5459$ cP

$$D^\circ_{BA} = \frac{7.4\times 10^{-8} \times 298 \times (1.9 \times 32)^{1/2}}{18.9^{0.6} \times 0.5459} = \frac{7.4\times 10^{-8} \times 298 \times 7.797}{5.893 \times 0.5459}$$

$$\approx 5.34\times 10^{-5} \text{ cm}^2/\text{s}$$

**Step 2：Leffler-Cullinan**

$$D \cdot \mu_{mix} = (D^\circ_{AB}\mu_B)^{x_B} (D^\circ_{BA}\mu_A)^{x_A}$$

- $x_A = 0.35, x_B = 0.65$
- $D^\circ_{AB}\mu_B = 1.65\times 10^{-5} \times 0.8911 = 1.470\times 10^{-5}$
- $D^\circ_{BA}\mu_A = 5.34\times 10^{-5} \times 0.5459 = 2.915\times 10^{-5}$

$(1.470\times 10^{-5})^{0.65} = 7.23\times 10^{-4}$
$(2.915\times 10^{-5})^{0.35} = 2.59\times 10^{-2}$

$$D \cdot \mu_{mix} = 7.23\times 10^{-4} \times 2.59\times 10^{-2} = 1.873\times 10^{-5}$$

$$D = \frac{1.873\times 10^{-5}}{1.536}$$

$$\boxed{D_{AB} \approx 1.22\times 10^{-5} \text{ cm}^2/\text{s}}$$

### 易错

> [!warning]
> - **$D^\circ_{AB} \neq D^\circ_{BA}$** — 两个都要算（[[L04_liquid_solid_pore_diffusivity]] 知识块 5 的 callout）
> - 算 $D^\circ_{BA}$ 时，**methanol 是溶剂** → 用 $\Phi_{methanol} = 1.9$（不是 2.26）
> - $\mu_A$ 和 $\mu_B$ 不要搞反 — A 是 methanol（小），B 是 water（大）

---

## Problem 5 — 半导体掺杂 Arrhenius

> (原题) (a) 从 Figure 1（$\ln D$ vs $1/T$ 图）算 $D_o$ 和 $Q$。
>
> (b) 矩形 silicon 300 mm × 150 mm，800°C 稳态。两侧 dopant A 浓度 $c_1 = 2$ mol/m³，$c_2 = 0.03$ mol/m³。扩散速率 $\dot{m} = 3\times 10^{-21}$ kg/s。$M_A = 31$ g/mol。求 silicon 厚度。

**Figure 1 端点**：(0.00125, -52.66) 和 (0.0025, -110.63)，$\ln D$ vs $1/T$ 直线。

### 思路与估算

(a) $\ln D = \ln D_o - (Q/R)\cdot(1/T)$
- 斜率 = $-Q/R$ → $Q = -R \times \text{slope}$
- 截距 = $\ln D_o$ → $D_o = e^{\text{intercept}}$

(b) Fick + 物料衡算：$\dot{m}/M_A = D \cdot A \cdot \Delta c / L$ → 解 $L$。先算 1073 K 下的 $D$。

### 解答

#### (a) 算 $D_o$ 和 $Q$

**斜率**：

$$\text{slope} = \frac{-110.63 - (-52.66)}{0.0025 - 0.00125} = \frac{-57.97}{0.00125} = -46376 \text{ K}$$

**$Q$**：

$$Q = -R \times \text{slope} = -8.314 \times (-46376) = 385600 \text{ J/mol} \approx \boxed{386 \text{ kJ/mol}}$$

**截距**（用点 (0.00125, -52.66) 反推）：

$$\ln D_o = -52.66 - (-46376) \times 0.00125 = -52.66 + 57.97 = 5.31$$

$$D_o = e^{5.31} = 202 \text{ cm}^2/\text{s} = \boxed{2.02\times 10^{-2} \text{ m}^2/\text{s}}$$

#### (b) Silicon 厚度

**算 800°C = 1073 K 下的 $D$**：

$$1/T = 1/1073 = 9.319\times 10^{-4} \text{ K}^{-1}$$

$$\ln D = 5.31 - 46376 \times 9.319\times 10^{-4} = 5.31 - 43.22 = -37.91$$

$$D = e^{-37.91} = 3.45\times 10^{-17} \text{ cm}^2/\text{s} = 3.45\times 10^{-21} \text{ m}^2/\text{s}$$

> 这个数和题目给的扩散速率 $3\times 10^{-21}$ kg/s **数字上一样**纯属巧合 — 单位完全不同。

**Fick 第一定律**：

$\dot{n} = \dot{m}/M_A = 3\times 10^{-21}/0.031 = 9.68\times 10^{-20}$ mol/s

$A = 0.3 \times 0.15 = 0.045$ m²

$\Delta c = 2 - 0.03 = 1.97$ mol/m³

$$L = \frac{D \cdot A \cdot \Delta c}{\dot{n}} = \frac{3.45\times 10^{-21} \times 0.045 \times 1.97}{9.68\times 10^{-20}}$$

$$= \frac{3.06\times 10^{-22}}{9.68\times 10^{-20}}$$

$$\boxed{L \approx 3.16\times 10^{-3} \text{ m} = 3.16 \text{ mm}}$$

### 易错

> [!warning]
> - 横轴 $1/T$（K⁻¹）单位本身很小 ~10⁻³ — 算斜率前要看清是 $1/T$ 还是 $1000/T$（参考 [[L04_liquid_solid_pore_diffusivity]] 知识块 8 知识盲区段）
> - $D_o$ 单位**和图表 $\ln D_{ab}$ 里 $D_{ab}$ 的单位一致**：图说 cm²/s → $D_o$ = $e^{5.31}$ cm²/s
> - 1 cm²/s = $10^{-4}$ m²/s — 注意换算
> - $\dot{m}$（kg/s）转 $\dot{n}$（mol/s）除以 $M_A$（kg/mol，要用 SI）

---

## Problem 6 — 多孔陶瓷的混合扩散

> (原题) O₂(A) + N₂(B) 透过 2 mm 厚陶瓷孔。0.1 atm, 293 K。平均孔径 0.1 μm，孔隙率 30.5%。$y_{O_2,1} = 0.8$，$y_{O_2,2} = 0.2$。$N_A = -N_B$。求 O₂ 摩尔通量。

### 思路与估算

**关键判断**：
- 孔径 100 nm，0.1 atm（稀压），算 $\lambda$ 看 $Kn$
- $\lambda \propto 1/P$，0.1 atm 时 $\lambda \approx 700$ nm，**$Kn \approx 7$ → Knudsen 主导**
- 等摩尔反向 → 用简化混合公式 $1/D_{Ae} = 1/D_{AB} + 1/D_{KA}$
- 多孔修正 $D'_{Ae} = \varepsilon^2 D_{Ae}$
- 通量 $N_A = c \cdot D'_{Ae} \cdot \Delta y_A / L$

### 解答

**Step 1：估 $D_{O_2-N_2}$ at 0.1 atm, 293 K**

用 Hirschfelder 或 J.1 数据外推。1 atm 下 $D_{O_2-N_2}(293) \approx 0.20$ cm²/s。0.1 atm 下：

$$D_{AB}(293, 0.1\text{ atm}) = \frac{0.20}{0.1} = 2.0 \text{ cm}^2/\text{s} = 2.0\times 10^{-4} \text{ m}^2/\text{s}$$

**Step 2：Knudsen $D_{KA}$**

$d_{pore}$ = 0.1 μm = $10^{-5}$ cm, $T = 293$ K, $M_{O_2} = 32$

$$D_{KA} = 4850 \times 10^{-5} \times \sqrt{293/32} = 4850 \times 10^{-5} \times 3.026$$

$$= 0.1468 \text{ cm}^2/\text{s} = 1.47\times 10^{-5} \text{ m}^2/\text{s}$$

**Step 3：混合扩散（等摩尔反向 → 简化版）**

$$\frac{1}{D_{Ae}} = \frac{1}{D_{AB}} + \frac{1}{D_{KA}} = \frac{1}{2.0} + \frac{1}{0.1468} = 0.50 + 6.81 = 7.31 \text{ s/cm}^2$$

$$D_{Ae} = 0.137 \text{ cm}^2/\text{s} = 1.37\times 10^{-5} \text{ m}^2/\text{s}$$

> 注意 Knudsen 阻力主导（6.81 vs 0.50）— 0.1 μm 孔在 0.1 atm 下 Knudsen 主导。

**Step 4：曲折修正（随机多孔）**

$$D'_{Ae} = \varepsilon^2 D_{Ae} = (0.305)^2 \times 1.37\times 10^{-5} = 0.0930 \times 1.37\times 10^{-5}$$

$$= 1.27\times 10^{-6} \text{ m}^2/\text{s}$$

**Step 5：通量**

总浓度 $c = P/RT = 0.1 \times 101325 / (8.314 \times 293) = 4.16$ mol/m³

$$N_A = c \cdot D'_{Ae} \cdot \frac{y_{A,1} - y_{A,2}}{L} = 4.16 \times 1.27\times 10^{-6} \times \frac{0.6}{0.002}$$

$$= 4.16 \times 1.27\times 10^{-6} \times 300$$

$$\boxed{N_A \approx 1.59\times 10^{-3} \text{ mol/(m}^2\cdot\text{s)}}$$

### 易错

> [!warning]
> - **不查 $Kn$ 直接用 $D_{AB}$**：本题压力低（0.1 atm）+ 孔小（100 nm）→ Knudsen 必须考虑
> - **忘记乘 $\varepsilon^2$**（多孔修正）
> - 等摩尔反向 → $\alpha = 0$ → 用简化版混合公式（不要套带 $\alpha y_A$ 的全式）

---

## Problem 7 — Nano-channel 不等摩尔混合

> (原题) Nano-channel 蒸汽重整：$T = 300°C = 573$ K，$P = 0.5$ atm，$d = 200$ nm。$y_{CH_4} = 0.10$，$N_A/N_B = 0.25$。$D_{CH_4-H_2O} = 1.683$ cm²/s。求 $D_{Ae}$。Knudsen 重要吗？

### 思路与估算

1. 算 $\lambda$ at 573 K, 0.5 atm，比较 $d_{pore}$
2. 算 $D_{KA}$
3. 因为 $N_A \neq -N_B$（比例 0.25）→ $\alpha = 1 + N_B/N_A = 1 + 4 = 5 \neq 0$ → **必须用全式**

### 解答

**Step 1：Knudsen 数判断**

$\lambda$ at 573 K, 0.5 atm（用 $\lambda = kT/(\sqrt{2}\pi\sigma^2 P)$，$\sigma_{air} \approx 3.7$ Å = $3.7\times 10^{-10}$ m）：

$$\lambda = \frac{1.38\times 10^{-23} \times 573}{\sqrt{2}\pi (3.7\times 10^{-10})^2 \times 50662.5} \approx 257 \text{ nm}$$

$$Kn = \frac{257}{200} = 1.28 \to \text{过渡区，Knudsen 重要}$$

> **答："Knudsen is important"** — 因为 $Kn$ 接近 1。

**Step 2：Knudsen $D_{KA}$**

$d_{pore} = 200$ nm = $2\times 10^{-5}$ cm, $M_{CH_4} = 16$

$$D_{KA} = 4850 \times 2\times 10^{-5} \times \sqrt{573/16} = 4850 \times 2\times 10^{-5} \times 5.984$$

$$= 0.581 \text{ cm}^2/\text{s}$$

**Step 3：$\alpha$ 与混合公式**

$$\alpha = 1 + \frac{N_B}{N_A} = 1 + \frac{1}{0.25} = 1 + 4 = 5$$

$$\alpha y_A = 5 \times 0.10 = 0.5$$

**Step 4：全混合公式**

$$\frac{1}{D_{Ae}} = \frac{1 - \alpha y_A}{D_{AB}} + \frac{1}{D_{KA}} = \frac{1 - 0.5}{1.683} + \frac{1}{0.581}$$

$$= 0.297 + 1.721 = 2.02 \text{ s/cm}^2$$

$$\boxed{D_{Ae} \approx 0.495 \text{ cm}^2/\text{s}}$$

### 易错

> [!warning]
> - $\alpha = 1 + N_B/N_A$ — 注意 B 在分子上面（不是 A/B 反过来）
> - 等摩尔反向时 $N_A = -N_B$ → $\alpha = 0$；本题 $\alpha = 5 \neq 0$ → 必须用全式
> - $\sigma_{air} \approx 3.7$ Å 是估算 $\lambda$ 用的（题目没给水蒸气 LJ 参数）— 严格的话用 H₂O LJ 参数

---

## Problem 8 — Glucose 受阻扩散

> (原题) Glucose 水溶液穿过 2 mm 厚多孔膜，孔径 3 nm。30°C。glucose 直径 0.86 nm。$\mu_{soln} = 0.001$ Pa·s。求 $D_{eff}$。

### 思路与估算

1. 用 Stokes-Einstein 算 $D^\circ_{AB}$（glucose-water 无限稀释）
2. $\phi = d_s/d_{pore}$
3. 计算 $F_1, F_2$，得 $D_{eff}$

### 解答

**Step 1：Stokes-Einstein**

$r = 0.86/2 = 0.43$ nm = $4.3\times 10^{-10}$ m，$T = 303$ K，$\mu = 10^{-3}$ Pa·s

$$D^\circ_{AB} = \frac{kT}{6\pi r \mu} = \frac{1.38\times 10^{-23} \times 303}{6\pi \times 4.3\times 10^{-10} \times 10^{-3}}$$

$$= \frac{4.181\times 10^{-21}}{8.105\times 10^{-12}} = 5.16\times 10^{-10} \text{ m}^2/\text{s} = 5.16\times 10^{-6} \text{ cm}^2/\text{s}$$

**Step 2：$\phi$ 与因子**

$$\phi = \frac{d_s}{d_{pore}} = \frac{0.86}{3} = 0.287$$

$$F_1 = (1 - 0.287)^2 = (0.713)^2 = 0.508$$

$$F_2 = 1 - 2.104(0.287) + 2.09(0.287)^3 - 0.95(0.287)^5$$

$$= 1 - 0.604 + 0.0494 - 0.00186 = 0.444$$

**Step 3：$D_{eff}$**

$$D_{eff} = D^\circ_{AB} \times F_1 \times F_2 = 5.16\times 10^{-10} \times 0.508 \times 0.444$$

$$\boxed{D_{eff} \approx 1.16\times 10^{-10} \text{ m}^2/\text{s} = 1.16\times 10^{-6} \text{ cm}^2/\text{s}}$$

> 受阻让 $D$ 降到 $D^\circ$ 的 22%（$F_1 \cdot F_2 = 0.226$）。

### 易错

> [!warning]
> - $r = d_s/2$（半径不是直径）
> - $T = 303$ K，不是 30
> - $\phi$ 用直径之比（$d_s/d_{pore}$），不要用半径之比

---

## Problem 9 — 反推孔径（Hindered diffusion 反问题）

> (原题) Ribonuclease 在 chromatography support 中 $D_{eff} = 5\times 10^{-7}$ cm²/s, $D^\circ_{AB} = 1.19\times 10^{-6}$ cm²/s, $d_s = 3.6$ nm, 298 K。求平均孔径。

### 思路

$F_1 \cdot F_2 = D_{eff}/D^\circ_{AB} = 5/11.9 = 0.420$

数值反解 $\phi$（$F_1, F_2$ 是 $\phi$ 的多项式）→ $d_{pore} = d_s/\phi$。

### 解答

**目标**：找 $\phi$ 使 $F_1(\phi) \cdot F_2(\phi) = 0.420$

| $\phi$ | $F_1$ | $F_2$ | $F_1 F_2$ |
|---|---|---|---|
| 0.20 | 0.640 | 0.595 | 0.381 |
| 0.18 | 0.672 | 0.633 | 0.426 |
| 0.181 | 0.671 | 0.631 | 0.423 |
| **0.182** | 0.669 | 0.629 | **0.421** |
| 0.185 | 0.664 | 0.624 | 0.414 |

→ $\phi \approx 0.182$

$$d_{pore} = \frac{d_s}{\phi} = \frac{3.6}{0.182}$$

$$\boxed{d_{pore} \approx 19.8 \text{ nm}}$$

### 易错

> [!warning]
> - Hindered 公式只适用 $0 \leq \phi \leq 0.6$，本题 $\phi = 0.18$ 在范围内 ✓
> - 反解必须**数值迭代**（试错或牛顿法）— 没有解析解
> - 也可估算：$\phi \approx 0.18$（中间值）→ $d_{pore} \approx 5.5 d_s \approx 20$ nm

---

## 答案速查

| 题号 | 答案 | 公式 |
|---|---|---|
| 1 | $d \approx 7.2$ nm | Stokes-Einstein |
| 2(a) | $D \approx 1.06\times 10^{-5}$ cm²/s | Wilke-Chang |
| 2(b) | $D(400 K) \approx 1.70\times 10^{-4}$ cm²/s | Tyn-Calus（n=4） |
| 2(c) | $D \approx 2.85\times 10^{-5}$ cm²/s | Nernst |
| 3 | $D \approx 8.42\times 10^{-6}$ cm²/s | Scheibel（K=17.5×10⁻⁸） |
| 4 | $D \approx 1.22\times 10^{-5}$ cm²/s | Leffler-Cullinan |
| 5(a) | $D_o = 202$ cm²/s, $Q = 386$ kJ/mol | Arrhenius 图解 |
| 5(b) | $L \approx 3.16$ mm | Fick + Arrhenius |
| 6 | $N_A \approx 1.59\times 10^{-3}$ mol/(m²·s) | 混合 + 多孔修正 |
| 7 | $D_{Ae} \approx 0.495$ cm²/s（Knudsen 重要） | 混合（α=5） |
| 8 | $D_{eff} \approx 1.16\times 10^{-10}$ m²/s | Hindered |
| 9 | $d_{pore} \approx 19.8$ nm | Hindered 反解 |

---

## 知识盲区 / Gaps identified

> [!question]
>
> 1. **物性数据查询**：本 tutorial 反复需要 $V_b$（摩尔体积）、$\Phi_B$（缔合参数）、$\mu$（黏度）、$\lambda^\circ$（极限离子电导率）— Welty 7th 附录 J 全有，**做题前先把附录翻熟**。
>
> 2. **每题"为什么用这个公式"的判断**：
>    - 大球形蛋白 → Stokes-Einstein
>    - 普通有机小分子稀液 → Wilke-Chang
>    - 没 $\Phi_B$ 数据 → Scheibel
>    - 浓溶液（$x_A > 0.1$） → Leffler-Cullinan
>    - 温度外推 → Tyn-Calus
>    - 电解质 → Nernst
>    - 固体 → Arrhenius
>    - 多孔（$Kn > 0.1$） → 混合公式
>    - 大分子穿小孔 → Hindered
>
> 3. **Q5 Arrhenius 图读数精度**：图上端点是 PPT 给的"标记点"，相对精确。但中间数据点的散布有 ±5%；用首尾两点取斜率比"全部数据点拟合"略粗，但量级对。
>
> 4. **Q6 / Q7 的 $D_{AB}$ 没 J.1 直接数据时**：可以用 Hirschfelder + LJ 参数估，或用其他类似分子对的数据外推（Q6 我用了 air-O₂ ≈ N₂-O₂ 的近似，因为 air 主要就是 N₂）。
>
> 5. **Q8/Q9 假设 Stokes-Einstein 给的 $D^\circ$ 是分子量级正确**：实际蛋白质形状不一定是完美球形，Stokes-Einstein 给的 $r$ 是"hydrodynamic radius"（含水合层）— 比"几何半径"略大。但作为工程估算够用。

---

## Verification steps for you

- [ ] Q5(a) 把斜率改用其他两端点（图上有 5 个数据点），看 $Q$ 一致性 — 如果差 > 5%，可能图读数有问题
- [ ] Q6 / Q7 检查 $Kn$ 计算 — 用 $\lambda \propto 1/P$ 直觉验证
- [ ] Q4 算 $D^\circ_{BA}$ 时记得换 $\Phi$（甲醇做溶剂，$\Phi = 1.9$ 不是水的 2.26）
- [ ] Q9 数值迭代 $\phi$ 时**用至少 3 个 $\phi$ 值确认结果**，不要只算一次
- [ ] **9 题做完后整理一份"我做的 D 和 Welty 附录数据的对照表"**，建立物性直觉 — 这比记公式更有用
