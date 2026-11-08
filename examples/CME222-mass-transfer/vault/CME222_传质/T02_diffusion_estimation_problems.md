---
type: tutorial
course: "CME222"
week: 5
tutorial: 2
topics: ["等摩尔反向扩散", "D 估算 (Hirschfelder/Fuller/Brokaw/Wilke)", "通量速度关系"]
related_lectures: ["[[L02_diffusive_mass_transfer]]", "[[L03_diffusion_coefficient_estimation]]"]
---

# Tutorial 2 — 扩散系数估算与等摩尔反向扩散

> [!info]
> - **所属课程**: [[CME222]]
> - **关联笔记**: [[L02_diffusive_mass_transfer]]、[[L03_diffusion_coefficient_estimation]]
> - **核心主题**: 等摩尔反向扩散（Q1, Q2）+ Hirschfelder/Fuller/Brokaw/Wilke 估算 D（Q3-Q7）

---

## 本次公式速查

| 公式 | 含义 | 来源 |
|---|---|---|
| $J_{A,z} = -cD_{AB}\dfrac{dy_A}{dz}$ | Fick 第一定律（mole fraction 形式） | [[L02_diffusive_mass_transfer]] |
| $\mathbf{N}_A = -cD_{AB}\nabla y_A + y_A(\mathbf{N}_A + \mathbf{N}_B)$ | 总通量 | [[L02_diffusive_mass_transfer]] |
| $N_A = -N_B$ | 等摩尔反向扩散条件 | 简化假设 |
| $N_A = \dfrac{cD_{AB}(y_{A,1} - y_{A,2})}{L}$ | 等摩尔反向扩散通量 | 由 Fick 积分 |
| $\mathbf{N}_A + \mathbf{N}_B = c\mathbf{V}$ | 通量与摩尔平均速度 | Q2 待证 |
| $D_{AB} = \dfrac{0.001858 T^{3/2}(1/M_A + 1/M_B)^{1/2}}{P\sigma_{AB}^2 \Omega_D}$ | Hirschfelder | [[L03_diffusion_coefficient_estimation]] |
| $D_{AB} = \dfrac{10^{-3}T^{1.75}(1/M_A+1/M_B)^{1/2}}{P[(\Sigma v)_A^{1/3}+(\Sigma v)_B^{1/3}]^2}$ | Fuller | [[L03_diffusion_coefficient_estimation]] |
| $\Omega_D = \Omega_{D_0} + \dfrac{0.196\,\delta_{AB}^2}{T^*}$ | Brokaw 极性修正 | [[L03_diffusion_coefficient_estimation]] |
| $\dfrac{1}{D_{1-\text{mix}}} = \sum \dfrac{y_i'}{D_{1-i}}$ | Wilke 多组分 | [[L03_diffusion_coefficient_estimation]] |
| $D_{T_2,P_2} = D_{T_1,P_1}(P_1/P_2)(T_2/T_1)^{3/2}(\Omega_{D,T_1}/\Omega_{D,T_2})$ | Hirschfelder 外推 | [[L03_diffusion_coefficient_estimation]] |

## 本次数据与常数

| 符号 | 值 |
|---|---|
| $R$ | 8.314 J/(mol·K) |
| $c$ at 25°C, 1 atm | $\approx 40.87$ mol/m³ |
| $\lambda$（空气, 常温常压） | ~70 nm |

> [!warning] 物性数据声明
> 本 tutorial 多题需查 Welty 7th 附录 K（LJ 参数 $\sigma$, $\varepsilon/\kappa$）和附录 J（实验 D 数据）。**下面解答里的 LJ 参数是常见参考值**，如果你查的附录数字略不同，按附录走 — 答案会差几个百分点但量级和方法都对。

---

## Problem 1 — 两 bulb + 细管的等摩尔反向扩散

> (原题) 两个 bulb 由直径 0.001 m、长 0.15 m 的细管连接。端 1 含 N₂，端 2 含 H₂。25°C, 1 atm。某时刻 N₂ 在端 1 是 80 mol%，端 2 是 25 mol%。$D_{AB} = 0.784$ cm²/s。求：
>
> (a) H₂ 和 N₂ 的传输速率（mol/s）和方向
> (b) N₂ 在两端相对静止坐标的速度（cm/s）

**涉及知识点**：[[等摩尔反向扩散]]、[[摩尔平均速度 V]]、[[扩散通量 vs 总通量]]

### 思路与估算

**思路**：
1. 两 bulb 体积大 → 端边界浓度恒定 → **稳态**
2. **等摩尔反向**：N₂ 跑去端 2 同时 H₂ 反向跑回，每"扩散一个 N₂"就"对流一个 H₂"过来 → $N_{N_2} = -N_{H_2}$
3. $N_A + N_B = 0 \Rightarrow$ molar-average velocity $\mathbf{V} = 0$（这是等摩尔反向的关键性质！）
4. 所以总通量 = 扩散通量：$N_A = J_A = -cD\,dy_A/dz = cD(y_{A,1}-y_{A,2})/L$
5. 静止参考系下 N₂ 的速度：$v_{N_2} = N_{N_2}/c_{N_2}$（因为 $\mathbf{V}=0$，A 的"扩散速度" = "绝对速度"）

**量级估算**：
- $c \sim 40$ mol/m³，$D \sim 10^{-4}$ m²/s，$\Delta y \sim 0.5$，$L \sim 0.1$ m
- $N \sim 40 \times 10^{-4} \times 0.5 / 0.1 \sim 0.02$ mol/(m²·s)
- 管截面积 $\sim 10^{-6}$ m² → $\dot{n} \sim 10^{-8}$ mol/s

### 解答

**总浓度**：

$$c = \frac{P}{RT} = \frac{101325}{8.314 \times 298.15} = 40.87 \text{ mol/m}^3$$

**管截面积**：

$$A = \pi(d/2)^2 = \pi(5 \times 10^{-4})^2 = 7.854 \times 10^{-7} \text{ m}^2$$

**扩散系数转 SI**：$D = 0.784$ cm²/s $= 0.784 \times 10^{-4}$ m²/s

#### (a) 通量与速率

$$N_{N_2} = \frac{cD(y_{N_2,1} - y_{N_2,2})}{L} = \frac{40.87 \times 0.784 \times 10^{-4} \times (0.80 - 0.25)}{0.15}$$

$$= \frac{40.87 \times 0.784 \times 0.55}{0.15} \times 10^{-4} = 117.5 \times 10^{-4} = 0.01175 \text{ mol/(m}^2\cdot\text{s)}$$

$$\dot{n}_{N_2} = N_{N_2} \cdot A = 0.01175 \times 7.854 \times 10^{-7} = \boxed{9.23 \times 10^{-9} \text{ mol/s}}$$

**方向**：N₂ 从端 1 → 端 2（沿浓度递减方向）

$$\dot{n}_{H_2} = -\dot{n}_{N_2} = \boxed{-9.23 \times 10^{-9} \text{ mol/s}}$$

**方向**：H₂ 从端 2 → 端 1（反向）

#### (b) N₂ 在两端的绝对速度

等摩尔反向 → $\mathbf{V} = 0$ → $v_{N_2} = N_{N_2}/c_{N_2}$

**端 1**：

$$c_{N_2,1} = y_{N_2,1} \cdot c = 0.80 \times 40.87 = 32.70 \text{ mol/m}^3$$

$$v_{N_2,1} = \frac{N_{N_2}}{c_{N_2,1}} = \frac{0.01175}{32.70} = 3.59 \times 10^{-4} \text{ m/s} = \boxed{0.0359 \text{ cm/s}}$$

**端 2**：

$$c_{N_2,2} = 0.25 \times 40.87 = 10.22 \text{ mol/m}^3$$

$$v_{N_2,2} = \frac{0.01175}{10.22} = 1.15 \times 10^{-3} \text{ m/s} = \boxed{0.115 \text{ cm/s}}$$

> 注意 $v_{N_2,2} > v_{N_2,1}$ — 因为同一通量穿过更稀的浓度，需要更快的速度。这是 $N = c \cdot v$ 的几何必然。

### 易错

> [!warning]
> - **没意识到这是等摩尔反向**：题目说"两 bulb 各有自己的气，互相扩散" → 默认 $N_A = -N_B$，立刻用简化的 $N = cD\Delta y/L$，省去解隐式总通量公式
> - **混淆 $J_A$ 和 $N_A$**：等摩尔反向时这两个相等（因为对流贡献 = 0），但**不等摩尔时**要用全总通量公式
> - 计算 $v_A$ 用 $c_A$（A 自己的浓度）**不是**总浓度 $c$
> - 单位：$D$ cm²/s 转 m²/s 除 $10^4$；$L$ 是 0.15 m 不是 cm

### 变式

- 如果改成 $y_{A,1} = 0.99$、$y_{A,2} = 0.01$（接近"纯 A vs 纯 B"），结果如何？
- 如果改成 stagnant air（B 不动）— 这就是单向扩散（Stefan flow），公式形式不同（对数）

---

## Problem 2 — 证明 $\mathbf{N}_A + \mathbf{N}_B = c\mathbf{V}$

> (原题) Starting with Fick's equation for the diffusion of A through a binary mixture of A and B. Prove that $\mathbf{N}_A + \mathbf{N}_B = c\mathbf{V}$. State the assumption made in derivation.

**涉及知识点**：[[摩尔平均速度 V]] 定义、[[总通量 NA]] 定义

### 解答

#### 直接证明（最干净）

**Step 1**：通量定义

$$\mathbf{N}_i = c_i \mathbf{v}_i \quad (i = A, B)$$

每个组分的总通量 = 它自己的浓度 × 它自己的绝对速度（相对静止参考系）。

**Step 2**：摩尔平均速度定义（[[L02_diffusive_mass_transfer]] 知识块 2）

$$\mathbf{V} = \frac{\sum c_i \mathbf{v}_i}{c} = \frac{c_A \mathbf{v}_A + c_B \mathbf{v}_B}{c}$$

**Step 3**：两边乘 $c$

$$c\mathbf{V} = c_A \mathbf{v}_A + c_B \mathbf{v}_B = \mathbf{N}_A + \mathbf{N}_B \quad \blacksquare$$

#### 从 Fick 定律出发（题目要求路径）

**Step 1**：写 A 和 B 的总通量公式（[[L02_diffusive_mass_transfer]]）

$$\mathbf{N}_A = -c D_{AB} \nabla y_A + y_A(\mathbf{N}_A + \mathbf{N}_B)$$

$$\mathbf{N}_B = -c D_{BA} \nabla y_B + y_B(\mathbf{N}_A + \mathbf{N}_B)$$

**Step 2**：相加

$$\mathbf{N}_A + \mathbf{N}_B = -c D_{AB} \nabla y_A - c D_{BA} \nabla y_B + (y_A + y_B)(\mathbf{N}_A + \mathbf{N}_B)$$

**Step 3**：用二元假设
- $y_A + y_B = 1 \Rightarrow \nabla y_A + \nabla y_B = 0$，即 $\nabla y_B = -\nabla y_A$
- $D_{AB} = D_{BA}$（恒定 $c$ 二元体系，[[L03_diffusion_coefficient_estimation]] 知识块 1）

代入：

$$\mathbf{N}_A + \mathbf{N}_B = -c D_{AB}\nabla y_A + c D_{AB}\nabla y_A + (\mathbf{N}_A + \mathbf{N}_B) = (\mathbf{N}_A + \mathbf{N}_B)$$

得到恒等式 — 说明 Fick 定律自身满足这个关系（不矛盾），但**真正的"$\mathbf{N}_A + \mathbf{N}_B = c\mathbf{V}$" 直接来自 $\mathbf{N}$ 和 $\mathbf{V}$ 的定义，不依赖 Fick 定律**。

#### 假设清单

1. **二元体系**（只有 A、B 两组分，$y_A + y_B = 1$）
2. **$\mathbf{N}_i$ 和 $\mathbf{V}$ 都相对同一静止参考系定义**
3. （从 Fick 路径还需）**恒定总摩尔浓度 $c$**，使 $D_{AB} = D_{BA}$ 成立

### 易错

> [!warning]
> - 把通量 $\mathbf{N}$ 和质量通量 $\mathbf{n}$ 搞混 — 注意 mass 基有平行公式 $\mathbf{n}_A + \mathbf{n}_B = \rho\mathbf{v}$（用质量平均速度）
> - 忘记说"二元"假设 — 多组分时改成 $\sum \mathbf{N}_i = c\mathbf{V}$
> - 用静止 vs 流动参考系混乱 — $\mathbf{N}$ 一定是相对静止参考系的"绝对通量"

---

## Problem 3 — Hirschfelder 估 n-丁烷在异丁烷中的 D

> (原题) n-butane → isobutane 异构化，催化剂表面，2 atm, 400°C。用 Hirschfelder 公式估 $D_{n-C_4H_{10}, i-C_4H_{10}}$。

**涉及知识点**：[[Hirschfelder 公式]]，同分异构体扩散

### 思路与估算

**特点**：n-butane 和 isobutane 是**同分异构体** → $M_A = M_B = 58.12$ g/mol。但 LJ 参数（$\sigma, \varepsilon/\kappa$）不同（分子形状不同）。

**量级估算**：气相 D 在 1 atm 下 $\sim 10^{-1}$ cm²/s，2 atm 减半到 $\sim 0.05$ cm²/s。

### 解答

**Step 1：基本量**
- $T = 400 + 273 = 673$ K
- $P = 2$ atm
- $M_A = M_B = 58.12$ g/mol → $\sqrt{1/M_A + 1/M_B} = \sqrt{2/58.12} = 0.1855$

**Step 2：LJ 参数（查 Welty 附录 K）**

| 物质 | $\sigma$ (Å) | $\varepsilon/\kappa$ (K) |
|---|---|---|
| n-butane | 4.687 | 531.4 |
| isobutane | 5.278 | 330.1 |

> [!warning] 请核实附录 K 数据
> 上面是常见参考值。你查 Welty 7th 附录 K 后用真值替换。

**组合规则**：

$$\sigma_{AB} = \frac{\sigma_A + \sigma_B}{2} = \frac{4.687 + 5.278}{2} = 4.983 \text{ Å}$$

$$\frac{\varepsilon_{AB}}{\kappa} = \sqrt{\frac{\varepsilon_A}{\kappa} \cdot \frac{\varepsilon_B}{\kappa}} = \sqrt{531.4 \times 330.1} = 418.8 \text{ K}$$

**Step 3：碰撞积分 $\Omega_D$**

$$T^* = \frac{T}{\varepsilon_{AB}/\kappa} = \frac{673}{418.8} = 1.607$$

查 LJ 碰撞积分表 at $T^* = 1.6$：$\Omega_D \approx 1.176$

**Step 4：代 Hirschfelder**

$$D_{AB} = \frac{0.001858 \times 673^{1.5} \times 0.1855}{2 \times (4.983)^2 \times 1.176}$$

$$= \frac{0.001858 \times 17458 \times 0.1855}{2 \times 24.83 \times 1.176}$$

$$= \frac{6.018}{58.39}$$

$$= \boxed{0.103 \text{ cm}^2/\text{s}}$$

### 易错

> [!warning]
> - **温度用 K 不用 °C**：400°C → 673 K
> - **Hirschfelder 单位是 cgs**：$D$ cm²/s, $P$ atm, $\sigma$ Å, $M$ g/mol。**别擅自换 SI**
> - 同分异构体 $M_A = M_B$ 但 $\sigma_A \neq \sigma_B$、$\varepsilon_A \neq \varepsilon_B$
> - $\Omega_D$ 查表前要确认是用 $T^* = \kappa T/\varepsilon_{AB}$ 还是 $T/\varepsilon$（很多教材有不同标记）

---

## Problem 4 — 用实验数据外推 $D_{CS_2-air}$

> (原题) 用 Welty 附录 J.1 数据估 CS₂ 在空气中、400 K, 2 bar 的扩散系数。

**涉及知识点**：[[Hirschfelder 外推公式]]

### 思路与估算

**思路**：J.1 给的是 273 K, 1 atm（用 $D_{AB} P$ 表示）。要用外推：

$$D_{T_2, P_2} = D_{T_1, P_1} \cdot \frac{P_1}{P_2} \cdot \left(\frac{T_2}{T_1}\right)^{3/2}$$

（简化版 — 忽略 $\Omega_D$ 的温度依赖；想更精确可乘 $\Omega_{D,T_1}/\Omega_{D,T_2}$）

**量级估算**：温度从 273 → 400 增加 1.5×，$T^{3/2}$ 因子 $\approx 1.77$；压力从 1 atm → 2 bar = 1.97 atm 几乎翻倍 → 两者大致抵消，$D$ 略升。

### 解答

**Step 1：从 J.1 取参考值**

CS₂-Air at 273 K：$D_{AB} P = 0.0883$ cm²·atm/s → $D_{273, 1\text{atm}} = 0.0883$ cm²/s

**Step 2：单位转换**

2 bar = $2/1.01325$ atm $\approx 1.974$ atm

**Step 3：外推**

$$D_{400, 2\text{bar}} = 0.0883 \times \frac{1}{1.974} \times \left(\frac{400}{273}\right)^{1.5}$$

$$= 0.0883 \times 0.5066 \times (1.465)^{1.5}$$

$$= 0.0883 \times 0.5066 \times 1.774$$

$$= \boxed{0.0794 \text{ cm}^2/\text{s}}$$

> [!tip] 精度估计
> 简化外推（忽略 $\Omega_D$）误差通常 < 5%。要更精确就再乘 $\Omega_{D,273}/\Omega_{D,400}$ — 一般这个比值 0.95-0.97 之间，会让 $D$ 略小。

### 易错

> [!warning]
> - J.1 表里给的是 $D_{AB} \cdot P$（不是单纯 $D_{AB}$） — 这样设计是因为 $D \cdot P$ 对压强不敏感（$D \propto 1/P$），存表方便
> - 单位 bar / atm 要换算（1 bar ≈ 0.987 atm）
> - 273 K 不是 0°C 的 K — 0°C = 273.15 K，但题用 273 简化
> - $D$ 单位 cm²·atm/s 和 m²·Pa/s 互换：1 cm²·atm/s ≈ 10.13 m²·Pa/s

---

## Problem 5 — Fuller 估 diethyl ether 在空气中的 D

> (原题) Diethyl ether (A, 弱极性) 在空气 (B) 中扩散，2 atm，30°C。用 Fuller correlation 估 $D_{AB}$。

**涉及知识点**：[[Fuller 经验公式]]、[[原子扩散体积加和]]

### 思路与估算

**思路**：题目说"用 Fuller" → **不查 LJ 参数**，用扩散体积。

Diethyl ether: $(CH_3CH_2)_2 O = C_4H_{10}O$，$M_A = 74$ g/mol
Air: $M_B = 29$ g/mol

**$\Sigma v$ 算法**：
- A：用原子加和 + 适当修正
- B (Air)：直接查 PPT 表 = 19.7

**量级估算**：气相 D ~ 0.1-1 cm²/s 量级，2 atm 减半。

### 解答

**Step 1：分子量与扩散体积**

$$\frac{1}{M_A} + \frac{1}{M_B} = \frac{1}{74} + \frac{1}{29} = 0.01351 + 0.03448 = 0.04800$$

$$\sqrt{0.04800} = 0.2191$$

A（diethyl ether $C_4H_{10}O$）的 $\Sigma v$（用 [[L03_diffusion_coefficient_estimation]] 知识块 5 原子表）：

$$\Sigma v_A = 4 \times 16.5 + 10 \times 1.98 + 1 \times 5.48 = 66 + 19.8 + 5.48 = 91.28$$

B（空气，整体查表）：$\Sigma v_B = 19.7$

**Step 2：扩散体积立方根**

$$(\Sigma v_A)^{1/3} = (91.28)^{1/3} = 4.499$$

$$(\Sigma v_B)^{1/3} = (19.7)^{1/3} = 2.701$$

$$\left[(\Sigma v_A)^{1/3} + (\Sigma v_B)^{1/3}\right]^2 = (4.499 + 2.701)^2 = (7.200)^2 = 51.84$$

**Step 3：温度项**

$T = 303$ K → $T^{1.75} = 303^{1.75}$

用对数：$\log T^{1.75} = 1.75 \log 303 = 1.75 \times 2.481 = 4.342$

$$T^{1.75} = 10^{4.342} \approx 21998$$

**Step 4：代 Fuller**

$$D_{AB} = \frac{10^{-3} \times 21998 \times 0.2191}{2 \times 51.84}$$

$$= \frac{10^{-3} \times 4820}{103.68}$$

$$= \frac{4.820}{103.68}$$

$$= \boxed{0.0465 \text{ cm}^2/\text{s}}$$

### 易错

> [!warning]
> - **diethyl ether 是 C₄H₁₀O 不是 C₄H₁₀**（分子结构 CH₃-CH₂-O-CH₂-CH₃，**含一个 O**）
> - $\Sigma v$ 中 oxygen 用 5.48（"except as noted"）—— 不是 9.1（甲酯）也不是 9.9（甲醚）。Diethyl ether 是更"高级"的醚，可以争议是 9.9 — 题目"假设可以用 Fuller correlation 正确估计"暗示用 simple oxygen value
> - **Fuller 是 cgs 单位**（cm²/s, atm, g/mol）— 同 Hirschfelder
> - $T^{1.75}$ 不是 $T^{3/2}$：Fuller 的温度指数比 Hirschfelder 大

### 变式

- 同样问题用 Hirschfelder（如果有 LJ 参数）— 答案应在 0.04-0.05 范围
- 改成 1 atm — $D$ 翻倍到 ~0.093 cm²/s

---

## Problem 6 — Wilke 多组分混合：CO₂ 在 (O₂ + N₂) 中

> (原题) 吸收塔处理废气：3% CO₂ + 5% O₂ + 92% N₂。估 350 K, 1 atm 下 CO₂ 在混合气里的扩散系数。

**涉及知识点**：[[Wilke 多组分混合公式]]、[[Hirschfelder 公式]]

### 思路与估算

**思路**：CO₂（组分 1）在 O₂（2）和 N₂（3）混合气中扩散。

1. 重新归一化（除掉 CO₂ 自己）：
   - $y_{O_2}' = 5/(5+92) = 0.0515$
   - $y_{N_2}' = 92/97 = 0.9485$
2. 分别估 $D_{CO_2-O_2}$ 和 $D_{CO_2-N_2}$（在 350 K, 1 atm）
3. Wilke 调和平均合并

**量级估算**：CO₂ 在空气中 350 K ~ 0.2 cm²/s；O₂、N₂ 都比空气稍小一些 → 混合后接近 0.2。

### 解答

**Step 1：重新归一化**

$$y_{O_2}' = \frac{0.05}{1 - 0.03} = 0.0515, \quad y_{N_2}' = \frac{0.92}{0.97} = 0.9485$$

**Step 2：估 $D_{CO_2-N_2}$（用 J.1 实验数据外推）**

J.1 表 CO₂-N₂ at 298 K：$D_{AB}P = 0.165$ cm²·atm/s

$$D_{CO_2-N_2}|_{350K, 1\text{atm}} = 0.165 \times (350/298)^{1.5} = 0.165 \times 1.275 = 0.210 \text{ cm}^2/\text{s}$$

**Step 3：估 $D_{CO_2-O_2}$（用 Hirschfelder）**

J.1 没直接给 CO₂-O₂，所以用 Hirschfelder。LJ 参数：
- CO₂：$\sigma = 3.941$ Å，$\varepsilon/\kappa = 195.2$ K
- O₂：$\sigma = 3.467$ Å，$\varepsilon/\kappa = 106.7$ K

$$\sigma_{AB} = (3.941 + 3.467)/2 = 3.704 \text{ Å}$$

$$\varepsilon_{AB}/\kappa = \sqrt{195.2 \times 106.7} = 144.3 \text{ K}$$

$$T^* = 350/144.3 = 2.425 \to \Omega_D \approx 0.96$$

$M_{CO_2} = 44, M_{O_2} = 32$：$\sqrt{1/44 + 1/32} = \sqrt{0.0540} = 0.2323$

$T^{1.5} = 350^{1.5} = 6549$

$$D_{CO_2-O_2} = \frac{0.001858 \times 6549 \times 0.2323}{1 \times (3.704)^2 \times 0.96} = \frac{2.827}{13.18} = 0.214 \text{ cm}^2/\text{s}$$

**Step 4：Wilke**

$$\frac{1}{D_{CO_2-\text{mix}}} = \frac{0.0515}{0.214} + \frac{0.9485}{0.210} = 0.241 + 4.516 = 4.757$$

$$\boxed{D_{CO_2-\text{mix}} = 0.210 \text{ cm}^2/\text{s}}$$

> 结果几乎等于 $D_{CO_2-N_2}$，因为 N₂ 占 95% 主导。

### 易错

> [!warning]
> - **重新归一化分母是 $1 - y_1$**（不是 $1 - y_{N_2}$），即除掉**扩散组分自己**的摩尔分数
> - $y_2' + y_3' = 1$（验证用）
> - **每个 $D_{1-i}$ 都要在题目温度压强下估**，不能直接代 25°C 的数据
> - Wilke 给的是**调和平均**（$1/D$ 的加权），不是直接平均

---

## Problem 7 — Brokaw + Wilke：NH₃ 在 N₂/H₂ 混合气中

> (原题) NH₃ 在静止气混合（1/3 N₂ + 2/3 H₂）中扩散。$P = 206.8$ kN/m² (= 2.04 atm), $T = 54°C$ (= 327 K)。NH₃ 沸点 239.81 K，N₂ 77.2 K，H₂ 20.1 K。NH₃ 偶极矩 1.46 D。

**涉及知识点**：[[Brokaw 极性修正]]、[[Wilke 多组分混合公式]]

### 思路与估算

**关键观察**：
- NH₃ 是**极性气体**（$\mu_p = 1.46$ D），应该用 **Brokaw 修正**
- N₂、H₂ 都是非极性 → 各自的 $\delta = 0$
- 所以 $\delta_{AB} = \sqrt{\delta_A \cdot \delta_B} = \sqrt{\delta_{NH_3} \times 0} = 0$
- → **Brokaw 修正项 $\frac{0.196 \delta_{AB}^2}{T^*} = 0$**
- → **退化成 Hirschfelder**

但题目仍要求按极性算 — 是因为 **NH₃ 自己的 LJ 参数 $\sigma_{NH_3}$、$\varepsilon_{NH_3}/\kappa$ 要用极性公式从 $V_b, T_b, \mu_p$ 估**（[[L03_diffusion_coefficient_estimation]] 知识块 6）。

**量级估算**：气相 D 在 1 atm 下 $\sim 0.2$ cm²/s，2 atm 减半 $\sim 0.1$ 量级。NH₃ 在 H₂ 中扩散更快（H₂ 轻），所以混合 D 大概 0.2-0.3。

### 解答

**Step 1：算 NH₃ 的 LJ 参数（极性公式）**

PPT Table 24.4 给：$V_{b,NH_3} = 25.8$ cm³/mol

$$\delta_{NH_3} = \frac{1.94 \times 10^3 \mu_p^2}{V_b T_b} = \frac{1.94 \times 10^3 \times 1.46^2}{25.8 \times 239.81} = \frac{4136}{6187} = 0.668$$

$$\sigma_{NH_3} = \left[\frac{1.585 V_b}{1 + 1.3\delta^2}\right]^{1/3} = \left[\frac{1.585 \times 25.8}{1 + 1.3 \times 0.668^2}\right]^{1/3} = \left[\frac{40.89}{1.580}\right]^{1/3} = (25.88)^{1/3} = 2.96 \text{ Å}$$

$$\frac{\varepsilon_{NH_3}}{\kappa} = 1.18(1 + 1.3\delta^2) T_b = 1.18 \times 1.580 \times 239.81 = 447.0 \text{ K}$$

**Step 2：算 N₂ 和 H₂ 的 LJ 参数（非极性公式）**

$$V_{b,N_2} = 31.2, \quad V_{b,H_2} = 14.3 \text{ cm}^3/\text{mol（PPT 表）}$$

非极性 → $\delta = 0$，$1 + 1.3\delta^2 = 1$：

| 物质 | $\sigma$ = $(1.585 V_b)^{1/3}$ (Å) | $\varepsilon/\kappa$ = $1.18 T_b$ (K) |
|---|---|---|
| N₂ | $(1.585 \times 31.2)^{1/3} = 3.671$ | $1.18 \times 77.2 = 91.10$ |
| H₂ | $(1.585 \times 14.3)^{1/3} = 2.829$ | $1.18 \times 20.1 = 23.72$ |

**Step 3：估 $D_{NH_3-N_2}$**

混合规则（**Brokaw 用几何平均，不是 Hirschfelder 的算术平均**）：

$$\sigma_{AB} = \sqrt{\sigma_A \sigma_B} = \sqrt{2.96 \times 3.671} = 3.30 \text{ Å}$$

$$\varepsilon_{AB}/\kappa = \sqrt{447.0 \times 91.10} = 201.7 \text{ K}$$

$\delta_{AB} = \sqrt{\delta_A \delta_B} = 0$（N₂ 非极性）→ **$\Omega_D = \Omega_{D_0}$**

$$T^* = 327/201.7 = 1.621$$

查 LJ 表：$\Omega_D \approx 1.17$

$M_{NH_3} = 17, M_{N_2} = 28$：$\sqrt{1/17 + 1/28} = \sqrt{0.0945} = 0.3074$

$T^{1.5} = 327^{1.5} = 5913$

$$D_{NH_3-N_2} = \frac{0.001858 \times 5913 \times 0.3074}{2.04 \times 3.30^2 \times 1.17} = \frac{3.376}{25.97} = 0.130 \text{ cm}^2/\text{s}$$

**Step 4：估 $D_{NH_3-H_2}$**

$$\sigma_{AB} = \sqrt{2.96 \times 2.829} = 2.893 \text{ Å}$$

$$\varepsilon_{AB}/\kappa = \sqrt{447.0 \times 23.72} = 102.9 \text{ K}$$

$$T^* = 327/102.9 = 3.18 \to \Omega_D \approx 0.92$$

$\sqrt{1/17 + 1/2} = \sqrt{0.5588} = 0.7475$

$$D_{NH_3-H_2} = \frac{0.001858 \times 5913 \times 0.7475}{2.04 \times 8.37 \times 0.92} = \frac{8.213}{15.71} = 0.523 \text{ cm}^2/\text{s}$$

> 注意 $D_{NH_3-H_2}$ 是 $D_{NH_3-N_2}$ 的 4 倍 — 因为 H₂ 轻又小，扩散快得多。

**Step 5：Wilke 多组分**

混合气里 N₂ 占 1/3，H₂ 占 2/3（已经是除掉 NH₃ 的比例，因为题目说 NH₃ 在 stagnant 混合气中扩散）：

$$\frac{1}{D_{NH_3-\text{mix}}} = \frac{1/3}{0.130} + \frac{2/3}{0.523} = 2.564 + 1.275 = 3.839$$

$$\boxed{D_{NH_3-\text{mix}} = 0.260 \text{ cm}^2/\text{s}}$$

### 易错

> [!warning]
> - **Brokaw 用几何平均 $\sigma_{AB} = \sqrt{\sigma_A \sigma_B}$**（不是 Hirschfelder 的 $\sigma_{AB} = (\sigma_A + \sigma_B)/2$）！这是 Brokaw 公式的特殊约定
> - 当 B 非极性时 $\delta_B = 0 \Rightarrow \delta_{AB} = 0 \Rightarrow$ Brokaw 退化为 Hirschfelder
> - **但 $\sigma_{AB}, \varepsilon_{AB}/\kappa$ 仍要用极性公式从 $V_b, T_b, \mu_p$ 算**（因为 $\delta_{NH_3} \neq 0$ 影响 NH₃ 自身的 LJ 参数）
> - 压强用 atm（题目给 kN/m² = kPa，要除 101.325 转 atm）：206.8 kPa = 2.04 atm
> - $T = 327$ K 不是 327°C

### 变式

- 如果换成 NH₃ 在 H₂O 蒸气中（**两个都极性**）— $\delta_{AB} \neq 0$，Brokaw 修正项才真正起作用
- Hirschfelder 直接用（不做极性修正） — 算出来的 D 大约小 5-10%

---

## 答案速查

| 题号 | 最终答案 | 涉及概念 |
|---|---|---|
| 1(a) | $\dot{n}_{N_2} = 9.23 \times 10^{-9}$ mol/s（端 1→2）；$\dot{n}_{H_2} = -9.23 \times 10^{-9}$ mol/s | [[等摩尔反向扩散]] |
| 1(b) | $v_{N_2,1} = 0.0359$ cm/s；$v_{N_2,2} = 0.115$ cm/s | $v = N/c_A$（$\mathbf{V}=0$） |
| 2 | $\mathbf{N}_A + \mathbf{N}_B = c\mathbf{V}$（直接由定义证） | [[摩尔平均速度 V]] 定义 |
| 3 | $D_{n-C_4-i-C_4} \approx 0.103$ cm²/s | [[Hirschfelder 公式]] |
| 4 | $D_{CS_2-air} \approx 0.0794$ cm²/s | Hirschfelder 外推 |
| 5 | $D_{ether-air} \approx 0.0465$ cm²/s | [[Fuller 经验公式]] |
| 6 | $D_{CO_2-mix} \approx 0.210$ cm²/s | [[Wilke 多组分混合公式]] |
| 7 | $D_{NH_3-mix} \approx 0.260$ cm²/s | Brokaw + Wilke |

---

## 知识盲区 / Gaps identified

> [!question]
>
> 1. **LJ 参数表查不到怎么办**？Q3 / Q6 / Q7 都需要 σ, ε/κ。Welty 7th 附录 K 覆盖大多常见气体，但化合物多了肯定不全。建议：(a) 用 Bird-Stewart-Lightfoot 教材附录补；(b) 用极性公式从 $V_b, T_b$ 估（适用于不知 LJ 参数的物质）。
>
> 2. **$\Omega_D$ 查图精度**：手查 LJ 碰撞积分表通常精度 1-2%，对工程估算够。要更精确可用 8 常数拟合公式（[[L03_diffusion_coefficient_estimation]] 知识块 6）。
>
> 3. **Brokaw 混合规则用几何平均** vs **Hirschfelder 用算术平均**——课程笔记没明确强调这个差异。Brokaw 之所以用几何平均，是为了和极性 $\sigma$ 公式 $\sigma = [1.585 V_b/(1+1.3\delta^2)]^{1/3}$ 在数学上一致。
>
> 4. **等摩尔反向扩散是"特殊条件"，不是"扩散公式默认情形"**：日常套 Fick 之前要先确认。和它对偶的是"单向扩散"（一组分滞留，需要 Stefan flow 公式）。
>
> 5. **Wilke 公式里 $y_i'$ 的意思**：是除掉扩散组分（即组分 1）后**其他组分相互之间的归一化**。Q7 里 N₂ 和 H₂ 比例已经是 1:2 不含 NH₃，所以直接用 1/3 和 2/3。

---

## Verification steps for you

- [ ] Q1 的方向：用直觉验证（高浓度 → 低浓度）
- [ ] Q2 写"假设"那段时点出"二元、相同参考系、恒定 c"三个
- [ ] Q3-Q7 的 LJ 参数用真附录 K 数据重做，看答案是否在 ±10% 范围
- [ ] Q4 Hirschfelder 外推用更准确的版本（含 $\Omega_D$ 比值）核对一下
- [ ] Q7 检查 NH₃ 的 LJ 参数：σ ≈ 2.96 Å, ε/κ ≈ 447 K — 这数和直接查 Welty 表的 σ_NH3 = 2.900 Å, ε/κ = 558.3 K 接近但不完全相同（极性公式估算 vs 实测拟合）
