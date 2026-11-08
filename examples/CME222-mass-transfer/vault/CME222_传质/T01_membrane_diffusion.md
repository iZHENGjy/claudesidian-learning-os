---
type: tutorial
course: "CME222"
week: 4
tutorial: 1
topics: ["膜扩散", "Solution-diffusion model", "稳态 Fick 定律应用"]
related_lectures: ["[[L02_diffusive_mass_transfer]]", "[[L04_liquid_solid_pore_diffusivity]]"]
---

# Tutorial 1 — 膜扩散应用题

> [!info]
> - **所属课程**: [[CME222]]
> - **关联笔记**: [[L02_diffusive_mass_transfer]]（Fick 第一定律）、[[L04_liquid_solid_pore_diffusivity]]（多孔扩散 + 固相扩散）
> - **核心主题**: 5 题全是**膜扩散**（一边高浓度/分压、另一边低浓度/分压、稳态 Fick）
> - **关键模型**: **Solution-diffusion model**（致密膜）+ Pore diffusion（多孔膜）

---

## 本次公式速查

| 公式 | 含义 | 来源 |
|---|---|---|
| $J_{A,z} = -D_{AB} \dfrac{dc_A}{dz}$ | Fick 第一定律 | [[L02_diffusive_mass_transfer]] |
| $J_A \approx D_{AB}\dfrac{c_{A,1} - c_{A,2}}{L}$ | 稳态、平面、线性浓度 | 由 Fick 积分 |
| $c_A = S \cdot p_A$ | **溶解平衡（亨利定律式）** | 膜分离专题 |
| $J_A = \dfrac{D_{AB} \cdot S \cdot \Delta p}{L}$ | **Solution-diffusion 通量公式** | 上两式合并 |
| $J_A = \dfrac{D_{AB} \cdot P}{R T L} \ln\dfrac{P - p_{A,2}}{P - p_{A,1}}$ | Stefan flow（A 扩散，B 滞留） | 单向扩散 |
| $c_A = \dfrac{p_A}{R T}$ | 理想气体浓度 | 物理化学 |

> [!warning] 知识盲区警告
> **Solution-diffusion model（$c_A = S p_A$）** 课程 L04 里没明确讲！课件只讲了 vacancy/interstitial（金属固相 Arrhenius 型）和 Knudsen（多孔）。但本份 tutorial 5 道题里有 4 道用了 solubility 系数 $S$ — 这是**致密聚合物膜 / 玻璃膜的标准模型**。详见末尾"知识盲区"段。

## 本次数据与常数

| 符号 | 名称 | 值 |
|---|---|---|
| $R$ | 气体常数 | 8.314 J/(mol·K) = 8314 J/(kmol·K) |
| $M_{H_2}$ | 氢气分子量 | 2 g/mol = 2 × 10⁻³ kg/mol |
| $M_{H_2O}$ | 水分子量 | 18 g/mol |
| $\lambda$ (空气, 常温常压) | 平均自由程 | ~70 nm（用于 $Kn$ 判断） |

---

## Problem 1 — 氢气穿过 4 bar / 1 bar 的膜

> (原题) Hydrogen gas is maintained at 4 bar and 1 bar on the opposite sides of a membrane of 0.5 mm thickness. At this temperature, $D = 8.7 \times 10^{-8}$ m²/s. The solubility of hydrogen in the materials is $S = 1.5 \times 10^{-3}$ kmol/(m³·bar). Determine the mass diffusion flux of hydrogen through the membrane.

**涉及知识点**: [[Solution-diffusion model]], [[Fick 第一定律]]

### 思路与估算

**思路**：
1. 膜两侧分压差 → 用溶解度 $S$ 转成膜内浓度差（$c_A = S \cdot p_A$）
2. 稳态 + 一维 plane wall → Fick 第一定律积分给出线性分布
3. 套 $J_A = D S \Delta p / L$

**量级估算**：$D S \Delta p / L \sim 10^{-7} \times 10^{-3} \times 1 / 10^{-3} \sim 10^{-7}$ kmol/(m²·s)。

### 解答

膜两侧浓度（用溶解度）：

$$c_{A,1} = S \cdot p_{A,1} = 1.5 \times 10^{-3} \times 4 = 6 \times 10^{-3} \text{ kmol/m}^3$$

$$c_{A,2} = S \cdot p_{A,2} = 1.5 \times 10^{-3} \times 1 = 1.5 \times 10^{-3} \text{ kmol/m}^3$$

稳态扩散通量：

$$J_A = D \cdot \frac{c_{A,1} - c_{A,2}}{L} = D \cdot S \cdot \frac{\Delta p}{L}$$

$$J_A = 8.7 \times 10^{-8} \times 1.5 \times 10^{-3} \times \frac{4 - 1}{0.5 \times 10^{-3}}$$

$$= \frac{8.7 \times 1.5 \times 3}{0.5} \times 10^{-8-3+3}$$

$$= 78.3 \times 10^{-8} \text{ kmol/(m}^2\text{·s)}$$

**最终答案**：$\boxed{J_A = 7.83 \times 10^{-7} \text{ kmol/(m}^2\text{·s)}}$

如果题目真要"mass flux"（kg 单位）：$j_A = J_A \cdot M_{H_2} = 7.83 \times 10^{-7} \times 2 = 1.57 \times 10^{-6}$ kg/(m²·s)。

### 易错

> [!warning]
> - **混淆 $S$ 单位**：本题 $S$ 用 bar 当压力单位（kmol/(m³·**bar**)），所以 $\Delta p$ 也要用 bar（不要换成 Pa）
> - 题目的 "mass diffusion flux" 字面可能是 kg 单位，但通常 chem-eng 里指 molar flux，看老师约定

### 变式

- 如果两侧分压改成 4 bar / 0.5 bar，通量会增加多少？（线性，增加 16.7%）
- 如果膜厚减半到 0.25 mm，通量翻倍

---

## Problem 2 — 反推膜厚

> (原题) Hydrogen diffuse through a nonporous polyvinyltrimethylsilane membrane at 25°C. The pressure on the sides of the membrane are 3.5 MPa and 200 kPa. $D = 160 \times 10^{-11}$ m²/s, $S = 0.54 \times 10^{-4}$ mol/(m³·Pa). If the hydrogen flux is 0.64 kmol/(m²·h), how thick in micrometer should the membrane be?

**涉及知识点**: [[Solution-diffusion model]] 反问题

### 思路与估算

**思路**：把 Q1 的公式反过来 — 已知 $J_A$ 求 $L$。

$$L = \frac{D \cdot S \cdot \Delta p}{J_A}$$

**量级估算**：$D S \Delta p \sim 10^{-9} \times 10^{-7} \times 10^6 \sim 10^{-10}$；$J_A \sim 10^{-4}$ kmol/(m²·s) → $L \sim 10^{-6}$ m = 几 μm。

### 解答

**单位统一**（**关键**）：
- $D = 1.6 \times 10^{-9}$ m²/s
- $S = 0.54 \times 10^{-4}$ mol/(m³·Pa) **= $0.54 \times 10^{-7}$ kmol/(m³·Pa)**
- $\Delta p = 3.5 \times 10^6 - 200 \times 10^3 = 3.3 \times 10^6$ Pa
- $J_A = 0.64$ kmol/(m²·h) = $0.64 / 3600$ = $1.778 \times 10^{-4}$ kmol/(m²·s)

代入：

$$L = \frac{1.6 \times 10^{-9} \times 0.54 \times 10^{-7} \times 3.3 \times 10^6}{1.778 \times 10^{-4}}$$

$$= \frac{1.6 \times 0.54 \times 3.3}{1.778} \times 10^{-9 - 7 + 6 + 4}$$

$$= \frac{2.851}{1.778} \times 10^{-6}$$

$$= 1.60 \times 10^{-6} \text{ m}$$

**最终答案**：$\boxed{L \approx 1.60 \text{ μm}}$

### 易错

> [!warning]
> - **单位地狱**：本题 $S$ 是 mol/(m³·Pa)，$\Delta p$ 单位 Pa，$J_A$ 是 kmol/(m²·h)。**至少 3 处单位换算**，任一错就差 3 个量级
> - 把 $S$ 从 mol/(m³·Pa) 转 kmol/(m³·Pa) 要除 1000
> - $J_A$ 从 /h 转 /s 除 3600
> - **不要忘记 $\Delta p$ 是 3500 - 200 = 3300 kPa，不是 3500**

### 变式

- 如果通量要求降到 0.32 kmol/(m²·h)（一半），膜要多厚？答：3.2 μm（线性翻倍）

---

## Problem 3 — 药品 blister 包装的水蒸气透过

> (原题) Blister 包装：polymer 形成 trough（5 mm 内径、3 mm 深、L = 50 μm 厚壁）+ aluminum foil lidding（不透）。$D_{AB} = 6 \times 10^{-14}$ m²/s（水蒸气在 polymer 里）。外表面 $c_A = 4.5 \times 10^{-3}$ kmol/m³，内表面 $c_A = 0.5 \times 10^{-3}$ kmol/m³。求传输到药片的速率（mol/s）。把 polymer sheet 当 plane wall。

**涉及知识点**: [[Fick 第一定律]] + 几何（求传质有效面积）

### 思路与估算

**思路**：
1. **lidding 是 Al 不透水** → 只有 polymer trough 的**底面 + 侧壁**透水
2. plane wall 假设 → $J_A = D \Delta c / L$
3. 传输速率 = $J_A \times A_{trough}$

**几何**（trough = 浅圆柱杯）：
- 底面（圆）：$A_{bot} = \pi (D/2)^2$
- 侧壁（圆筒侧面）：$A_{side} = \pi D h$
- 顶面是 Al → 不算

**量级估算**：$D \sim 10^{-14}$，$\Delta c \sim 10^{-3}$，$L \sim 10^{-5}$，$A \sim 10^{-5}$
→ $\dot{n} \sim 10^{-14} \times 10^{-3} / 10^{-5} \times 10^{-5} = 10^{-17}$ kmol/s = $10^{-14}$ mol/s

### 解答

**通量**：

$$J_A = D \cdot \frac{\Delta c}{L} = 6 \times 10^{-14} \times \frac{(4.5 - 0.5) \times 10^{-3}}{50 \times 10^{-6}}$$

$$= 6 \times 10^{-14} \times \frac{4 \times 10^{-3}}{5 \times 10^{-5}} = 4.8 \times 10^{-12} \text{ kmol/(m}^2\text{·s)}$$

**Trough 表面积**（只算 polymer 部分）：

$$A_{bot} = \pi (2.5 \times 10^{-3})^2 = 1.963 \times 10^{-5} \text{ m}^2$$

$$A_{side} = \pi \cdot 5 \times 10^{-3} \cdot 3 \times 10^{-3} = 4.712 \times 10^{-5} \text{ m}^2$$

$$A_{total} = 6.675 \times 10^{-5} \text{ m}^2$$

**传输速率**：

$$\dot{n} = J_A \cdot A_{total} = 4.8 \times 10^{-12} \times 6.675 \times 10^{-5}$$

$$= 3.20 \times 10^{-16} \text{ kmol/s} = 3.20 \times 10^{-13} \text{ mol/s}$$

**最终答案**：$\boxed{\dot{n} \approx 3.2 \times 10^{-13} \text{ mol/s}}$

### 易错

> [!warning]
> - **漏算 trough 侧壁**：很多人只算底面，但侧壁面积约是底面的 2.4 倍 — **侧壁占大头**
> - 顶面 lidding 是 Al，**不能算进 polymer 透水面积**
> - 单位：题目要 mol/s，但浓度用 kmol/m³ → 最后乘 1000

### 变式

- 这袋药能放多久？— 假设药片受不了 0.01 g 水（$5.6 \times 10^{-4}$ mol），$\dot{n} = 3.2 \times 10^{-13}$ mol/s → 时间 $= 5.6 \times 10^{-4} / 3.2 \times 10^{-13} = 1.75 \times 10^9$ s ≈ 55 年（远长于药品保质期 → 包装设计 OK）

---

## Problem 4 — Water-resistant sheet 单孔水蒸气透过

> (原题) Water-resistant sheet 含 10 μm 直径、100 μm 长的孔。298 K, 1 atm。顶部饱和液态水，底部 50% RH。$D = 0.26 \times 10^{-4}$ m²/s。$p_{sat}$(298 K) = 0.03165 bar。求单孔的水蒸气透过率 (kmol/s)。

**涉及知识点**: [[Knudsen 数判断]], [[Fick 第一定律]] (or Stefan flow)

### 思路与估算

**思路**：
1. **先判断扩散机制** — 算 $Kn = \lambda/d_{pore}$。常温常压空气 $\lambda \approx 70$ nm = 0.07 μm；$d_{pore}$ = 10 μm → $Kn \approx 0.007 \ll 1$ → **纯分子扩散**，不用 Knudsen
2. 边界条件：顶 $p_{A,1} = p_{sat}$；底 $p_{A,2} = 0.5 \cdot p_{sat}$
3. 因为空气滞留（air 不能反向逆流），严格用 **Stefan flow** 公式；但 $p_A \ll P$ 时近似等于简单 Fick
4. 单孔速率 = $J_A \times A_{pore}$（$A_{pore}$ = 圆孔截面）

**量级估算**：水蒸气在空气中 $D \sim 10^{-5}$ m²/s（典型气相）；$\Delta c \sim p_A/(RT) \sim 1500/(8.314 \times 298) \sim 0.6$ mol/m³；$J_A \sim D \Delta c / L \sim 10^{-5} \times 0.6 / 10^{-4} \sim 0.06$ mol/(m²·s)；孔截面 $\sim 10^{-10}$ m² → 单孔 $\dot{n} \sim 10^{-11}$ mol/s = $10^{-14}$ kmol/s。

### 解答

**Step 1：判断扩散机制**

$$Kn = \frac{\lambda}{d_{pore}} = \frac{70 \times 10^{-9}}{10 \times 10^{-6}} = 0.007 \ll 1$$

→ **纯分子扩散**（Knudsen 不重要）。

**Step 2：边界分压**

$$p_{A,1} = p_{sat} = 0.03165 \text{ bar} = 3165 \text{ Pa}$$

$$p_{A,2} = 0.5 \times p_{sat} = 1582.5 \text{ Pa}$$

**Step 3：通量（Stefan flow，A 扩散 / B 滞留 air）**

$$J_A = \frac{D \cdot P}{R T L} \ln\frac{P - p_{A,2}}{P - p_{A,1}}$$

$$= \frac{2.6 \times 10^{-5} \times 101325}{8.314 \times 298 \times 100 \times 10^{-6}} \ln\frac{99742.5}{98160}$$

$$= \frac{2.634}{0.2478} \times \ln(1.01613)$$

$$= 10.63 \times 0.01600$$

$$= 0.170 \text{ mol/(m}^2\text{·s)} = 1.70 \times 10^{-4} \text{ kmol/(m}^2\text{·s)}$$

**Step 4：单孔截面积**

$$A_{pore} = \pi (d/2)^2 = \pi (5 \times 10^{-6})^2 = 7.854 \times 10^{-11} \text{ m}^2$$

**Step 5：单孔速率**

$$\dot{n} = J_A \cdot A_{pore} = 1.70 \times 10^{-4} \times 7.854 \times 10^{-11}$$

$$= 1.33 \times 10^{-14} \text{ kmol/s}$$

**最终答案**：$\boxed{\dot{n} \approx 1.33 \times 10^{-14} \text{ kmol/s}}$

> [!tip] 简化检验
> 用纯 Fick（忽略 Stefan）：$J_A \approx D \Delta c / L = D \Delta p_A / (RTL)$
> $= 2.6 \times 10^{-5} \times (3165 - 1582.5) / (8.314 \times 298 \times 100 \times 10^{-6})$
> $= 0.166$ mol/(m²·s)
> 和 Stefan 结果差 < 3% — 因为 $p_A \ll P$ 时两种近似几乎一致。

### 易错

> [!warning]
> - **不查 $Kn$ 就直接套 Fick**：本题 $d_{pore} = 10$ μm 看着小，但比 $\lambda \approx 70$ nm 大 100+ 倍，仍是分子扩散主导。**养成先算 $Kn$ 的习惯**
> - **顶部"饱和液体"** = 气液界面，$p_A = p_{sat}$（不是题目里没说的别的值）
> - 50% RH = $p_A / p_{sat} = 0.5$（题目最后一行明示）
> - $\dot{n}$ vs $J_A$：前者是 kmol/s（一个孔的总速率），后者是 kmol/(m²·s)。**不要忘记乘截面积**

### 变式

- 如果孔径降到 100 nm（$Kn \approx 0.7$）— 进入过渡区，要用混合公式 $1/D_{Ae} = 1/D_{AB} + 1/D_{KA}$
- 如果孔径降到 10 nm（$Kn \approx 7$）— 进入纯 Knudsen，$D_{KA} = 4850 d \sqrt{T/M}$

---

## Problem 5 — He 球容器漏气速率

> (原题) He 储存在 SiO₂ 球容器，20°C。$D_{sphere}$ = 0.2 m，壁厚 L = 2 mm。初始压 4 bar，外界 He 分压可忽略。$D = 0.4 \times 10^{-13}$ m²/s，$S = 0.45 \times 10^{-3}$ kmol/(m³·bar)。求 $dp/dt$（一维 + $D \gg L$）。

**涉及知识点**: [[Solution-diffusion model]] + 物料平衡 + 理想气体

### 思路与估算

**思路**：
1. **D >> L** → 球壳近似平面墙（plane wall），用 $J_A = D S \Delta p / L$
2. 流出总速率 $\dot{n}_{out} = J_A \cdot A_{sphere}$
3. **物料平衡**：$d n_{He}/dt = -\dot{n}_{out}$
4. 理想气体 $n = pV/(RT)$ → $dp/dt = -\dot{n}_{out} \cdot RT / V$

**量级估算**：
- $J_A \sim D S \Delta p / L \sim 10^{-13} \times 10^{-3} \times 4 / 10^{-3} \sim 4 \times 10^{-13}$ kmol/(m²·s)
- $A \sim 10^{-1}$ m²，$V \sim 10^{-3}$ m³
- $\dot{n} \sim 10^{-14}$ kmol/s
- $RT \sim 10^3 \times 300 \sim 10^6$ J/kmol（$R$ 用 8314）
- $dp/dt \sim 10^{-14} \times 10^6 / 10^{-3} \sim 10^{-5}$ Pa/s

### 解答

**Step 1：膜内浓度差**

$$c_{A,1} = S \cdot p_A = 0.45 \times 10^{-3} \times 4 = 1.8 \times 10^{-3} \text{ kmol/m}^3$$

$$c_{A,2} \approx 0$$

**Step 2：通量**

$$J_A = D \cdot \frac{c_{A,1} - c_{A,2}}{L} = 0.4 \times 10^{-13} \times \frac{1.8 \times 10^{-3}}{2 \times 10^{-3}} = 3.6 \times 10^{-14} \text{ kmol/(m}^2\text{·s)}$$

**Step 3：球面积**

$$A = 4\pi r^2 = 4\pi (0.1)^2 = 0.1257 \text{ m}^2$$

**Step 4：流出总速率**

$$\dot{n}_{out} = J_A \cdot A = 3.6 \times 10^{-14} \times 0.1257 = 4.525 \times 10^{-15} \text{ kmol/s}$$

**Step 5：球内体积**

$$V = \frac{4}{3}\pi r^3 = \frac{4}{3}\pi (0.1)^3 = 4.189 \times 10^{-3} \text{ m}^3$$

**Step 6：理想气体 $dp/dt$**

理想气体 $pV = nRT$，$V$ 和 $T$ 不变：

$$\frac{dp}{dt} = \frac{RT}{V} \cdot \frac{dn}{dt} = -\frac{RT}{V} \cdot \dot{n}_{out}$$

$R = 8314$ J/(kmol·K)，$T = 293$ K：

$$\frac{dp}{dt} = -\frac{8314 \times 293}{4.189 \times 10^{-3}} \times 4.525 \times 10^{-15}$$

$$= -5.815 \times 10^8 \times 4.525 \times 10^{-15}$$

$$= -2.63 \times 10^{-6} \text{ Pa/s}$$

**最终答案**：$\boxed{\dfrac{dp}{dt} \approx -2.63 \times 10^{-6} \text{ Pa/s} = -2.63 \times 10^{-11} \text{ bar/s}}$

> 换成更直观的：$\approx -83$ Pa/year ≈ $-8.3 \times 10^{-4}$ bar/year（一年漏不到 1 mbar，4 bar 的瓶能放上千年）。

### 易错

> [!warning]
> - **R 的单位**：$R = 8.314$ J/(mol·K) **= 8314 J/(kmol·K)** = 0.08314 L·bar/(mol·K)。本题 $\dot{n}$ 用 kmol → 必须用 8314
> - 球的 $A$ 是 $4\pi r^2$，不是 $\pi D^2 / 4$（那是圆面积）
> - $V$ 是球体积 $(4/3)\pi r^3$，**不要用 trough 那种圆柱**
> - **D >> L** 这个条件给的就是让你**不必用球壳的对数公式**，用 plane wall
> - $T$ 必须用 K（293），不要 °C（20）

### 变式

- 容器要漏到 1 bar 多久？— $\Delta p = 3$ bar = $3 \times 10^5$ Pa，速率 $\sim 10^{-6}$ Pa/s → 时间 $3 \times 10^{11}$ s ≈ 万年。但实际上 $J_A \propto p$，会越来越慢（指数衰减），所以更快变化要做微分方程 $dp/dt \propto p$（自动指数衰减形式）
- 改用塑料瓶（$D \sim 10^{-9}$ m²/s）— 漏速率快 $10^4$ 倍

---

## 答案速查

| 题号 | 最终答案 | 涉及概念 |
|---|---|---|
| 1 | $J_A = 7.83 \times 10^{-7}$ kmol/(m²·s) | [[Solution-diffusion model]] |
| 2 | $L \approx 1.60$ μm | Solution-diffusion 反问题 |
| 3 | $\dot{n} \approx 3.2 \times 10^{-13}$ mol/s | Fick + trough 几何 |
| 4 | $\dot{n} \approx 1.33 \times 10^{-14}$ kmol/s | Stefan flow + Knudsen 数判断 |
| 5 | $dp/dt \approx -2.63 \times 10^{-6}$ Pa/s | Solution-diffusion + 物料平衡 |

---

## 知识盲区 / Gaps identified

> [!question] 课程没明确讲，但本 tutorial 大量使用的概念
>
> 1. **Solution-diffusion model（致密膜）— 5 题里有 4 题（Q1, Q2, Q3, Q5）用到，但 [[L04_liquid_solid_pore_diffusivity]] 完全没讲**
>
>    模型框架（建议加进笔记）：
>    - **致密膜**（dense membrane / nonporous polymer / glass）里没有"孔" — 分子靠 **dissolve into → diffuse through → desorb out** 三步走
>    - 关键物性：**solubility coefficient $S$**（kmol/(m³·bar) 或 mol/(m³·Pa)）— 表示气体在膜内的"溶解能力"
>    - 平衡条件：$c_A = S \cdot p_A$（亨利定律式）
>    - 通量：$\boxed{J_A = \dfrac{D \cdot S \cdot \Delta p}{L} = \dfrac{P_e \cdot \Delta p}{L}}$
>    - 工程上常把 **permeability $P_e = D \cdot S$** 当一个独立物性（避开分别测 $D$ 和 $S$）
>
>    **教材去查**：Welty 7th 主教材在 "Membrane separation processes" 章节有，或 Geankoplis 4th Ch. 13。
>
> 2. **Stefan flow（Q4）— [[L02_diffusive_mass_transfer]] 给了总通量公式 $N_A = -cD\nabla y_A + y_A(N_A + N_B)$，但没具体推到"单向扩散（A 流，B 滞留）"的对数形式**
>
>    单向扩散结果：$N_A = \dfrac{cD}{L} \ln\dfrac{1 - y_{A,2}}{1 - y_{A,1}} = \dfrac{DP}{RTL}\ln\dfrac{P - p_{A,2}}{P - p_{A,1}}$（与 Q4 形式一致）
>
>    **教材去查**：Welty 主教材 "Steady-state ordinary molecular diffusion" 章节，或 Bird-Stewart-Lightfoot Transport Phenomena Ch. 18。
>
> 3. **Knudsen 数判断扩散机制（Q4）— [[L04_liquid_solid_pore_diffusivity]] 知识块 10 讲过，但题目没直接提示，需要你自己想到去算 $Kn$**
>
>    经验：**孔径 ≤ 100 nm** 才需要担心 Knudsen，本题 10 μm 远大于 $\lambda \approx 70$ nm，纯分子扩散。
>
> 4. **球壳几何 + plane wall 简化（Q5）**
>
>    严格来说球壳的扩散是 1D 球坐标问题：$J_A = D \cdot \dfrac{r_o r_i}{r_o - r_i} \cdot \dfrac{c_{A,1} - c_{A,2}}{r^2}$。当 $L = r_o - r_i \ll r$ 时退化到 plane wall。题目说 "$D \gg L$" 就是给你这个简化的许可。**严格球壳公式在 [[Fick 第二定律]] 后续讲会接触**。

---

## Verification steps for you

- [ ] 自己用计算器重算 Q1（量级 $10^{-7}$ kmol/(m²·s) 对就 OK）
- [ ] Q4 同时用 **简化 Fick** 和 **Stefan flow** 算，确认两个结果差 < 5%
- [ ] Q5 检查单位：$dp/dt$ 应该是 Pa/s 量级，不是 bar/s（差 5 个量级，量纲对就行）
- [ ] 把 $S = D \cdot S$ 当成"permeability"重写公式：$J_A = P_e \Delta p / L$ — 看是不是一致
- [ ] **Tutorial 课和老师对答案后**，把题号和你算的数字记到 Q1-Q5 后面（或你的草稿纸）以便后续查
