---
type: lecture
course: "CME222"
week: 3
lecture: 3
title: "Molecular Diffusivity & Estimation of Gas Diffusion Coefficients"
title_zh: "分子扩散系数与气体扩散系数的估算"
date: 2026-Spring
source_ppt: "[[_attachments/CME 222 Lecture 3/L03.pdf]]"
pages: "1-32"
pages_skipped: "1 (封面), 2 (目录), 3 (章节页), 10 (章节页)"
verified: "_attachments/verify.py 全部通过"
related: ["[[L02_diffusive_mass_transfer]]"]
---

# 分子扩散系数与气体扩散系数的估算 / Molecular Diffusivity & Gas Diffusivity Estimation

> [!abstract] 一眼看懂
> 上一讲的 Fick 定律里有个 $D_{AB}$，算通量必须先知道它。这一讲回答：查不到实验值时，怎么从分子大小、分子量、温度和压力把它**估出来**。比如 20 °C 下 CO₂ 在空气里的 $D$，用分子参数算出 0.147 cm²/s，跟实验外推值 0.155 只差约 5%。

| 阅读路线（由易到难） | 课件 | 读完你能回答 |
| --- | --- | --- |
| [[#第 1 部分 · 扩散系数是什么]] | p.4–9 | 气体、液体、固体的 $D$ 各差几个数量级？ |
| [[#第 2 部分 · 从分子运动推出 D]] | p.11–17 | 为什么气体的 $D$ 随温度升高、随压力降低？ |
| [[#第 3 部分 · 两个实用估算式]] | p.18–24 | 有 / 没有分子参数时，各用哪个公式？ |
| [[#第 4 部分 · 极性气体与多组分混合物]] | p.25–29 | 氨这种极性气体、或三种以上气体的混合物怎么估？ |

**前置知识**：

| 前置知识 | 本讲是否用到 | 处理 |
| --- | --- | --- |
| Fick 第一定律、$D_{AB}$ 的含义 | 用到（全讲） | 见 [[L02_diffusive_mass_transfer]] |
| 理想气体、$c = P/RT$ | 用到（p.9、11） | 默认已掌握 |
| 摩尔分数 | 用到（p.28） | 默认已掌握 |

---

## 第 1 部分 · 扩散系数是什么

这一部分先弄清 $D$ 的单位、大小，以及一个常被默认的性质：$D_{AB} = D_{BA}$。

### 1.1 扩散系数的量纲与量级（Dimension & magnitude）（p.4–8）

**为什么需要它**
上一讲例 4 里，碳在铁里的 $D$ 是 $3\times10^{-11}$ m²/s；例 3 里氦在氮里是 $0.687\times10^{-4}$ m²/s，两者差了六个数量级。拿到一个 $D$ 的数值，如果心里没有"气体大概多少、固体大概多少"的尺子，就看不出它是不是单位抄错了。

**它怎么工作**
由 Fick 定律，通量（mol/(m²·s)）除以浓度梯度（mol/m⁴）得到 $D$，单位是 m²/s，也常用 cm²/s。$D$ 不是物质自身的常数，它取决于压力、温度、组成，以及在什么介质里扩散。分子之间越松散，越容易挤过去，所以气体最大、液体次之、固体最小。课件 p.5–8 给出了教材附录的实验值表：气体（表 J.1）、液体（表 J.2）、固体（表 J.3）。查得到就直接用表值。

**课件里的概念**
- 单位：cm²/s 或 m²/s（p.4）
- 影响因素：压力、温度、组成、扩散介质（p.4）
- 典型量级（p.4）：气体 $10^{-6}$–$10^{-5}$ m²/s；液体 $10^{-10}$–$10^{-9}$ m²/s；固体 $10^{-14}$–$10^{-10}$ m²/s
- 表 J.1 给出的是 $D_{AB}P$（cm²·atm/s），除以压力（atm）才是 $D_{AB}$（p.5–6）

**注意：** 表 J.1 第三列是 $D_{AB}P$ 不是 $D_{AB}$。1 atm 下两者数值相同，其他压力要除以 $P$。

**专业说法：** 先按相态估量级，查得到实验值就用实验值。*EN: Know the order of magnitude by phase; use tabulated experimental values when available.*

**优缺点**
表值最可靠，但表里只有少数物系和少数温度。表里没有的物系，就需要从分子性质去估，这是第 2、3 部分的任务。在那之前，还要先确认一个性质：$D_{AB}$ 和 $D_{BA}$ 是否相等。

> [!question]- 用自己的话说：扩散系数的量级
> 合上笔记，用 3–5 句大白话讲清楚。然后打开检查。
>
> > [!success]- 关键环节：你的回答应包含
> > - [ ] $D$ 的单位是面积 / 时间（m²/s）
> > - [ ] 它取决于压力、温度、组成和介质，不是物质常数
> > - [ ] 气体 > 液体 > 固体，大约各差几个数量级
>
> > [!example]- 一种说法
> > 扩散系数说的是"一种分子在另一种东西里挤过去有多容易"。在气体里分子之间空隙大，最容易；液体挤一些；固体最难，慢上百万倍都很正常。同一对物质，温度和压力变了，这个数也会变。

### 1.2 二元扩散系数相等（Equality of diffusion coefficients）（p.9）

**为什么需要它**
查表 J.1 时，"空气中的 CO₂"有数据，"CO₂ 中的空气"却没有。能不能拿前者当后者用？

**它怎么工作**
设想一根管子里只有 A 和 B，温度、压力不变，所以总摩尔浓度 $c = P/RT$ 处处相同。A 的浓度往右减少多少，B 就必须往右增加多少，两者的梯度大小相等、方向相反。如果 A 每秒往右扩散 1 mol，为了保持总浓度不变，B 就得往左扩散 1 mol，所以 $J_A = -J_B$。把 Fick 定律分别写给 A 和 B，代入后两个梯度抵消，剩下的只能是 $D_{AB} = D_{BA}$。

> [!note] 此处在 vault 中嵌入课件 p.9 截图（示例仓库不附课件原图）
*图 1.1 · p.9 · 推导只用了两个条件：总浓度不变（$c_A + c_B = c = P/RT$）和等量反向扩散（$J_A = -J_B$）。*

**课件里的概念**（p.9）

$$c_A + c_B = c = \frac{P}{RT},\qquad J_A = -J_B \tag{1.1}$$

$$-D_{AB}\frac{dc_A}{dz} = -\left(-D_{BA}\frac{dc_B}{dz}\right)\ \Rightarrow\ D_{AB} = D_{BA} \tag{1.2}$$

成立条件：二元体系、摩尔密度（浓度）恒定；对气体即恒温恒压。

**专业说法：** 二元体系中扩散系数是对称的。*EN: For a binary mixture at constant molar density, the diffusivity is symmetric: D_AB = D_BA.*

**优缺点**
表里只要存一个方向的数据。但多数物系连一个方向都查不到，必须能从分子性质算出 $D$。

> [!question]- 用自己的话说：$D_{AB} = D_{BA}$
> > [!success]- 关键环节：你的回答应包含
> > - [ ] 前提是二元、总浓度不变（气体即恒温恒压）
> > - [ ] 总浓度不变迫使 A 和 B 等量反向扩散
> > - [ ] 代入 Fick 定律后两个系数只能相等
>
> > [!example]- 一种说法
> > 两种气体关在同一个管子里，总的分子密度不变。一种往右挤过去多少，另一种就得往左让出多少。两边的推动力一样大、流量又一样大，那么"A 在 B 里有多好挤"和"B 在 A 里有多好挤"就只能是同一个数。

### 误区与陷阱

> [!failure] 陷阱 1.1：直接把表 J.1 的第三列当成 $D_{AB}$
> **反例：** 表 J.1 中 CO₂–空气 273 K 一栏是 0.136 cm²·atm/s。如果压力是 2 atm，$D_{AB}$ 是 0.068 cm²/s，不是 0.136（p.5）。
> **为什么不对：** 那一列是 $D_{AB}P$，气体的 $D$ 与压力成反比，见 [[#1.1 扩散系数的量纲与量级（Dimension & magnitude）（p.4–8）|§1.1]]。
> **正确说法：** 查表值要除以实际压力（atm）。*EN: Divide the tabulated D_AB·P by the actual pressure.*

> [!question]- 暂停：为什么"空气中的 CO₂"的扩散系数可以直接当"CO₂ 中的空气"用？
> **不要往回翻**，先用自己的话回答，再打开检查。
>
> > [!success]- 关键环节：你的回答应包含
> > - [ ] 二元体系、恒温恒压，总浓度不变
> > - [ ] 两种组分等量反向扩散
> > - [ ] 所以 $D_{AB} = D_{BA}$
>
> > [!question]- 预测：一个三种气体的混合物里，用这个推导还能保证 A 对 B 的扩散系数等于 B 对 A 的吗？
> > > [!success]- 展开答案
> > > 不能用这个推导保证。推导要求只有两种组分、A 往一边多少 B 就往另一边多少；有第三种组分时，这个等量反向的关系不再成立。检验的是"二元"这个前提。

---

## 第 2 部分 · 从分子运动推出 D

### 2.1 自扩散系数：平均自由程乘平均速度（Self-diffusion coefficient）（p.11–14）

**为什么需要它**
表里查不到的物系，只能从分子本身的性质算 $D$。最简单的起点是：一种气体在它自己的同位素里扩散，分子大小、质量都一样，只剩下"分子跑多快、跑多远撞一次"这两件事。

**它怎么工作**
把分子想成互不吸引的硬球（p.11 的假设：理想气体、低密度、刚性球、弹性碰撞）。一个分子沿直线飞，飞一段撞一次，再换方向。两次碰撞之间的平均距离叫平均自由程 $\lambda$；分子的平均速率叫 $u$。扩散快慢正比于"每次跑多远 × 跑多快"，系数 1/3 来自三个方向平均。分子越稀（压力低），越少碰撞，$\lambda$ 越长（p.14）；温度越高，$u$ 越大。把 $\lambda$ 和 $u$ 的表达式代进去，就得到只含 $T$、$P$、分子直径和分子量的公式。

**课件里的概念**（p.12–13）

$$D_{AA^*} = \frac{1}{3}\lambda u \tag{2.1}$$

$$\lambda = \frac{\kappa T}{\sqrt{2}\,\pi\sigma_A^2 P},\qquad u = \sqrt{\frac{8\kappa N T}{\pi M_A}} \tag{2.2}$$

$$D_{AA^*} = \frac{2T^{3/2}}{3\pi^{3/2}\sigma_A^2 P}\left(\frac{\kappa^3 N}{M_A}\right)^{1/2} \tag{2.3}$$

其中 $M_A$ 单位 kg/mol，$N = 6.022\times10^{23}$ /mol，$P$ 单位 Pa，$T$ 单位 K，$\kappa = 1.38\times10^{-23}$ J/K，$\sigma$ 为分子（Lennard-Jones）直径，单位 m。

**专业说法：** 硬球动力学理论给出 $D \propto T^{3/2}/(P\sigma^2\sqrt{M})$。*EN: Hard-sphere kinetic theory gives D ∝ T^{3/2} / (P σ² √M).*

**优缺点**
公式清楚地告诉我们 $D$ 怎样随 $T$、$P$ 变化。但它只适用于同一种分子，而真实问题里 A、B 大小和质量都不同。

> [!question]- 用自己的话说：自扩散系数
> > [!success]- 关键环节：你的回答应包含
> > - [ ] 分子当作互不吸引的硬球，飞一段撞一次
> > - [ ] $D$ 正比于平均自由程 × 平均速度
> > - [ ] 压力高 → 自由程短 → $D$ 小；温度高 → 速度大 → $D$ 大
>
> > [!example]- 一种说法
> > 把气体分子想成满屋乱飞的小球。一个小球能扩散多远，看它每次能飞多远才撞上别人，以及它飞得多快。屋里球越挤，每次飞的距离越短；温度越高，球飞得越快。扩散系数就是这两者的乘积再乘个 1/3。

### 2.2 碰撞直径与二元混合物（Collision diameter & binary mixtures）（p.15–17）

**为什么需要它**
CO₂ 在空气里扩散，两种分子直径和质量都不一样，式 2.3 用不了。

**它怎么工作**
两个分子能靠多近，由它们之间的作用力决定：离得很近时强烈排斥，所以存在一个最近距离，这就是碰撞直径（p.15）。直径越小，越不容易撞上，平均自由程越长。A、B 直径不同时，碰撞距离取两者的平均；质量不同时，用两者质量倒数的组合。结果仍然是 $T^{3/2}$、$1/P$ 的形式，这就让我们可以把一个已知条件下的 $D$ 换算到别的温度和压力（p.17）。

**课件里的概念**（p.15–17）
- 碰撞直径（Lennard-Jones diameter）：两分子中心能靠近的最小距离，即分子间势能为零的距离；直径越小，平均自由程越大（p.15）

$$D_{AB} = \frac{2}{3}\left(\frac{\kappa}{\pi}\right)^{3/2} N^{1/2} T^{3/2}\,\frac{\left(\dfrac{1}{2M_A} + \dfrac{1}{2M_B}\right)^{1/2}}{P\left(\dfrac{\sigma_A + \sigma_B}{2}\right)^2},\qquad D_{AB} = D_{BA} \tag{2.4}$$

- 气相扩散依赖压力和温度，可用来预测不同 $P$、$T$ 下的 $D$（p.17）

**专业说法：** 二元气体的硬球扩散系数用平均碰撞直径和两者的质量组合。*EN: Binary hard-sphere diffusivity uses the mean collision diameter and the pair's combined molar masses.*

**优缺点**
硬球模型完全忽略了分子间的吸引力，实际气体的 $D$ 随温度的变化比 $T^{3/2}$ 更快。下一部分的 Hirschfelder 方程就是为了把分子间作用力加回来。

> [!question]- 用自己的话说：二元混合物的 $D$
> > [!success]- 关键环节：你的回答应包含
> > - [ ] 碰撞直径是两分子能靠近的最小距离
> > - [ ] 不同分子用平均直径和两者质量的组合
> > - [ ] 仍是 $D \propto T^{3/2}/P$，可换算到其他温度压力
>
> > [!example]- 一种说法
> > 两种不同大小的球混在一起乱飞，撞不撞得上要看两个球半径加起来有多大，所以取平均直径。轻的球跑得快，所以质量也要一起算进去。算出来的规律和单一气体一样：温度高扩散快，压力高扩散慢。

### 误区与陷阱

> [!failure] 误区 2.1：气体扩散系数只和温度有关，压力变了不影响
> **反例：** 实例 4.2 的 SiH₄–N₂ 在 900 K、100 Pa 下 $D \approx 1091$ cm²/s，大约是常压同温度下的一千倍（$D \propto 1/P$，100 Pa 约为 1 atm 的千分之一）。
> **为什么不对：** 压力低 → 分子稀 → 平均自由程长 → $D$ 大，见 [[#2.1 自扩散系数：平均自由程乘平均速度（Self-diffusion coefficient）（p.11–14）|§2.1]]。
> **正确说法：** 气体 $D$ 与压力成反比。*EN: Gas diffusivity is inversely proportional to pressure.*

> [!question]- 暂停：为什么气体的扩散系数随温度升高、随压力降低？
> > [!success]- 关键环节：你的回答应包含
> > - [ ] $D \propto$ 平均自由程 × 平均速度
> > - [ ] 温度高 → 分子速度大
> > - [ ] 压力高 → 分子密 → 自由程短
>
> > [!question]- 预测：按硬球模型，压力不变、温度从 300 K 升到 600 K，$D$ 变为原来的多少倍？
> > > [!success]- 展开答案
> > > $2^{3/2} \approx 2.83$ 倍（$D \propto T^{3/2}$）。检验的是"$T^{3/2}$ 依赖"一环。

---

## 第 3 部分 · 两个实用估算式

### 3.1 Hirschfelder 方程与碰撞积分（Hirschfelder equation & collision integral）（p.18–21）

**为什么需要它**
硬球模型不考虑分子间的吸引和排斥。工程上要估一个非极性气体对的 $D$，需要一个把这部分作用力也算进去的公式。

**它怎么工作**
Hirschfelder 方程的结构和式 2.4 一样（$T^{3/2}$、$1/P$、分子量、碰撞直径），只是分母多了一个碰撞积分 $\Omega_D$，用来修正分子间作用力。$\Omega_D$ 只取决于无量纲温度 $T^* = \kappa T/\varepsilon_{AB}$，其中 $\varepsilon_{AB}$ 是两分子之间的作用能。温度越高，分子动能越大，越接近硬球碰撞，$\Omega_D$ 越小，$D$ 越大（p.20）。用法：查 A、B 的 Lennard-Jones 参数 $\sigma$ 和 $\varepsilon/\kappa$ → 混合规则得 $\sigma_{AB}$、$\varepsilon_{AB}$ → 算 $T^*$ → 查 $\Omega_D$ → 代入方程。注意这个式子的单位是"混合单位"：$D$ 为 cm²/s，$P$ 为 atm，$\sigma$ 为 Å，$M$ 为 g/mol。

> [!note] 此处在 vault 中嵌入课件 p.19 截图（示例仓库不附课件原图）
*图 3.1 · p.19 · 碰撞积分 $\Omega_D$ 随无量纲温度 $\kappa T/\varepsilon_{AB}$ 下降：$T^*$ 在 2 附近 $\Omega_D \approx 1.07$，到 10 附近降到约 0.74。*

**课件里的概念**（p.18–20）

$$D_{AB} = \frac{0.001858\,T^{3/2}\left(\dfrac{1}{M_A} + \dfrac{1}{M_B}\right)^{1/2}}{P\,\sigma_{AB}^2\,\Omega_D} \tag{3.1}$$

$D_{AB}$：cm²/s；$T$：K；$M_A, M_B$：g/mol；$P$：atm；$\sigma_{AB}$：碰撞直径，Å；$\Omega_D$：碰撞积分，无量纲。适用于非极性、不反应的气体对（p.18）。

$$D_{AB}\big|_{T_2,P_2} = D_{AB}\big|_{T_1,P_1}\,\frac{P_1}{P_2}\left(\frac{T_2}{T_1}\right)^{3/2}\frac{\Omega_D\big|_{T_1}}{\Omega_D\big|_{T_2}} \tag{3.2}$$

$\Omega_D$ 可由图 3.1 查，也可用课件 p.26 给出的关联式算（式 4.4）。

> [!info]- 补充：Lennard-Jones 参数与混合规则
> 计算需要各分子的 $\sigma$ 和 $\varepsilon/\kappa$。本讲用到：CO₂ 3.996 Å / 190 K；N₂ 3.681 Å / 91.5 K；H₂ 2.968 Å / 33.3 K（出自 Welty 教材附录，经 [Pearce et al., 2020] 的表格核对）。空气 3.617 Å / 97.0 K（待核实：未找到可访问的原始表格核对）。非极性气体对的混合规则：$\sigma_{AB} = (\sigma_A + \sigma_B)/2$，$\varepsilon_{AB} = \sqrt{\varepsilon_A\varepsilon_B}$。
> 来源：[Pearce et al., 2020]

> [!example] 实例 3.1：20 °C、1 atm 下 CO₂ 在空气中的扩散系数（p.21）
> ① 混合参数：
> $$\begin{aligned}\sigma_{AB} &= \frac{\sigma_{CO_2} + \sigma_{air}}{2} = \frac{3.996 + 3.617}{2} = 3.806\ \text{Å}\\ \frac{\varepsilon_{AB}}{\kappa} &= \sqrt{190\times97.0} = 135.8\ \text{K}\\ T^* &= \frac{293}{135.8} = 2.158\ \Rightarrow\ \Omega_D = 1.048\end{aligned}$$
> ② 代入式 3.1：
> $$\begin{aligned}D_{AB} &= \frac{0.001858\times293^{3/2}\left(\dfrac{1}{44} + \dfrac{1}{29}\right)^{1/2}}{1\times3.806^2\times1.048}\\ &= 0.147\ \text{cm}^2/\text{s}\end{aligned}$$
> ③ 与表 J.1 比较：表中 273 K 下 $D_{AB}P = 0.136$ cm²·atm/s，用式 3.2 外推到 293 K：
> $$D_{AB}\big|_{293} = 0.136\times\left(\frac{293}{273}\right)^{3/2}\times\frac{\Omega_D\big|_{273}}{\Omega_D\big|_{293}} = 0.155\ \text{cm}^2/\text{s}$$
>
> **计算结果：** 估算值 $D_{CO_2\text{-}air} = 0.147$ cm²/s $= 1.47\times10^{-5}$ m²/s，比实验外推值 0.155 cm²/s 低约 5%。

**专业说法：** 非极性气体对用 Hirschfelder 方程，需要 Lennard-Jones 参数。*EN: For non-polar gas pairs use the Hirschfelder equation with Lennard-Jones parameters.*

**优缺点**
考虑了分子间作用力，本例误差约 5%。但它需要每种分子的 $\sigma$ 和 $\varepsilon$，很多化合物查不到这两个参数。

> [!question]- 用自己的话说：Hirschfelder 方程
> > [!success]- 关键环节：你的回答应包含
> > - [ ] 在硬球公式上加了碰撞积分 $\Omega_D$，修正分子间作用力
> > - [ ] $\Omega_D$ 只看无量纲温度 $\kappa T/\varepsilon_{AB}$，温度越高越小
> > - [ ] 需要两种分子的 Lennard-Jones 参数，单位是混合单位（cm²/s、atm、Å、g/mol）
>
> > [!example]- 一种说法
> > 真实分子不是硬球，靠近时会互相吸引或排斥。Hirschfelder 方程在硬球公式下面多除了一个修正因子，这个因子只看"温度相对于分子间作用力有多强"。温度高时分子冲劲大，作用力的影响小，修正因子就变小。

### 3.2 Fuller 关联式（Fuller correlation）（p.22–24）

**为什么需要它**
苯在空气里扩散，苯的 Lennard-Jones 参数不一定查得到，Hirschfelder 方程用不了。

**它怎么工作**
Fuller 关联式不用 $\sigma$ 和 $\varepsilon$，改用"扩散体积" $\Sigma v$ 代表分子的大小。简单分子的扩散体积直接查表；表里没有的分子，按它含有的原子把原子扩散体积加起来，有芳香环再加一个结构修正（p.23）。温度指数是 1.75，比硬球的 1.5 大。

> [!note] 此处在 vault 中嵌入课件 p.23 截图（示例仓库不附课件原图）
*图 3.2 · p.23 · 上半表是原子和结构增量（C 16.5、H 1.98、芳香环 −20.2），下半表是简单分子的扩散体积（空气 20.1）。*

**课件里的概念**（p.22–23）

$$D_{AB} = \frac{10^{-3}\,T^{1.75}\left(\dfrac{1}{M_A} + \dfrac{1}{M_B}\right)^{1/2}}{P\left[(\Sigma v)_A^{1/3} + (\Sigma v)_B^{1/3}\right]^2} \tag{3.3}$$

$D_{AB}$：cm²/s；$T$：K；$P$：atm；$v$：扩散体积。

> [!example] 实例 3.2：30 °C、1 atm 下苯在空气中的扩散系数（p.24）
> ① 苯 C₆H₆ 的扩散体积（含一个芳香环）：
> $$(\Sigma v)_{C_6H_6} = 6\times16.5 + 6\times1.98 - 20.2 = 90.68$$
> ② 代入式 3.3（$M_{C_6H_6} = 78$，$M_{air} = 29$，$(\Sigma v)_{air} = 20.1$）：
> $$\begin{aligned}D_{AB} &= \frac{10^{-3}\times303^{1.75}\left(\dfrac{1}{78} + \dfrac{1}{29}\right)^{1/2}}{1\times\left(90.68^{1/3} + 20.1^{1/3}\right)^2}\\ &= 0.0920\ \text{cm}^2/\text{s}\end{aligned}$$
> ③ 对照：表 J.1 中苯–空气 298 K 为 0.0962 cm²/s，按 $T^{1.75}$ 换算到 303 K 约 0.0990 cm²/s。
>
> **计算结果：** $D_{C_6H_6\text{-}air} = 0.0920$ cm²/s $= 9.20\times10^{-6}$ m²/s，比表值换算结果低约 7%。

**专业说法：** 缺 Lennard-Jones 参数时用 Fuller 关联式，按原子扩散体积加和。*EN: When Lennard-Jones parameters are unavailable, use the Fuller correlation with additive atomic diffusion volumes.*

**优缺点**
只需要分子式就能算，最方便。但 Fuller 和 Hirschfelder 都针对非极性分子；遇到氨、SO₂ 这样的极性分子，分子间还有偶极作用，需要再修正。

> [!question]- 用自己的话说：Fuller 关联式
> > [!success]- 关键环节：你的回答应包含
> > - [ ] 用扩散体积代替 Lennard-Jones 参数
> > - [ ] 扩散体积可以按原子加和，芳香环有结构修正
> > - [ ] 温度指数 1.75，不需要碰撞积分
>
> > [!example]- 一种说法
> > 如果查不到分子的"碰撞参数"，就换一种办法估它有多大：把分子里每个原子的"体积分"加起来，环状结构再扣一点。有了大小、质量、温度、压力，就能直接算出扩散系数。

### 误区与陷阱

> [!failure] 陷阱 3.1：把 SI 单位直接代进 Hirschfelder 或 Fuller 方程
> **反例：** 实例 3.1 若把 $P$ 写成 101325 Pa、$\sigma$ 写成 $3.806\times10^{-10}$ m，结果会错十几个数量级。
> **为什么不对：** 两个式子的系数 0.001858 和 $10^{-3}$ 是按混合单位给出的：$D$ 为 cm²/s、$P$ 为 atm、$\sigma$ 为 Å、$M$ 为 g/mol，见 [[#3.1 Hirschfelder 方程与碰撞积分（Hirschfelder equation & collision integral）（p.18–21）|§3.1]]。
> **正确说法：** 按方程规定的单位代入，算完再把 cm²/s 换成 m²/s（×10⁻⁴）。*EN: Substitute in the units the correlation uses, then convert cm²/s to m²/s.*

> [!question]- 暂停：什么时候用 Hirschfelder，什么时候用 Fuller？
> > [!success]- 关键环节：你的回答应包含
> > - [ ] 两者都适用于非极性气体对
> > - [ ] 有 Lennard-Jones 参数 → Hirschfelder
> > - [ ] 没有参数、只知道分子式 → Fuller
>
> > [!question]- 预测：用 Fuller 关联式，压力不变、温度从 300 K 升到 600 K，$D$ 变为原来的多少倍？
> > > [!success]- 展开答案
> > > $2^{1.75} \approx 3.36$ 倍，比硬球模型的 2.83 倍大。检验的是"Fuller 温度指数 1.75"一环。

---

## 第 4 部分 · 极性气体与多组分混合物

### 4.1 极性气体：Brokaw 方程（Polar gases: Brokaw equation）（p.25–27）

**为什么需要它**
吸收塔要用水吸收废气里的氨（p.27）。氨分子有偶极矩，分子之间除了普通的吸引排斥，还有偶极作用，非极性的 $\Omega_D$ 不够准。

**它怎么工作**
Brokaw 方法仍然用 Hirschfelder 方程（式 3.1），只是换一种办法算参数。第一步，用偶极矩、沸点下液体摩尔体积和沸点算出极性参数 $\delta$。第二步，用 $\delta$ 和沸点数据算每个分子的 $\sigma$ 和 $\varepsilon/\kappa$（这样就不需要查 Lennard-Jones 表），再用**几何平均**得到 $\sigma_{AB}$ 和 $\varepsilon_{AB}$。第三步，算 $T^*$ 和非极性部分 $\Omega_{D0}$，再加上一项极性修正 $0.196\,\delta_{AB}^2/T^*$。

**课件里的概念**（p.25–26）

$$\Omega_D = \Omega_{D0} + \frac{0.196\,\delta_{AB}^2}{T^*},\qquad \delta_{AB} = (\delta_A\delta_B)^{1/2},\qquad \delta = \frac{1.94\times10^3\,\mu_p^2}{V_bT_b} \tag{4.1}$$

$\mu_p$：偶极矩（Debye）；$V_b$：沸点下液体摩尔体积（cm³/mol）；$T_b$：正常沸点（K）。

$$T^* = \frac{\kappa T}{\varepsilon_{AB}},\quad \frac{\varepsilon_{AB}}{\kappa} = \left(\frac{\varepsilon_A}{\kappa}\frac{\varepsilon_B}{\kappa}\right)^{1/2},\quad \frac{\varepsilon}{\kappa} = 1.18\,(1 + 1.3\,\delta^2)\,T_b \tag{4.2}$$

$$\sigma_{AB} = (\sigma_A\sigma_B)^{1/2},\qquad \sigma = \left(\frac{1.585\,V_b}{1 + 1.3\,\delta^2}\right)^{1/3} \tag{4.3}$$

$$\Omega_{D0} = \frac{A}{(T^*)^B} + \frac{C}{\exp(DT^*)} + \frac{E}{\exp(FT^*)} + \frac{G}{\exp(HT^*)} \tag{4.4}$$

$A = 1.06036$，$B = 0.15610$，$C = 0.19300$，$D = 0.47635$，$E = 1.03587$，$F = 1.52996$，$G = 1.76474$，$H = 3.89411$。

**注意：** Brokaw 方法里 $\sigma_{AB}$ 用几何平均（式 4.3），而非极性的 Hirschfelder 用法用算术平均。两者不要混用。

> [!example] 实例 4.1：373 K、101325 Pa 下氨在空气中的扩散系数（Brokaw）（p.27）
> 已知：$T_{b,NH_3} = 239.81$ K，$T_{b,air} = 78.8$ K，$\mu_{p,NH_3} = 1.46$ D，空气偶极矩为 0。沸点下液体摩尔体积取 NH₃ 25.8、空气 29.9 cm³/mol（待核实：题目未给，未找到可访问的原始表格核对）。
>
> ① 极性参数：
> $$\delta_{NH_3} = \frac{1.94\times10^3\times1.46^2}{25.8\times239.81} = 0.668,\qquad \delta_{air} = 0\ \Rightarrow\ \delta_{AB} = 0$$
> ② 分子参数（式 4.2、4.3）：
> $$\begin{aligned}\sigma_{NH_3} &= \left(\frac{1.585\times25.8}{1 + 1.3\times0.668^2}\right)^{1/3} = 2.958\ \text{Å},\quad \sigma_{air} = (1.585\times29.9)^{1/3} = 3.619\ \text{Å}\\ \sigma_{AB} &= \sqrt{2.958\times3.619} = 3.272\ \text{Å}\\ \frac{\varepsilon_{NH_3}}{\kappa} &= 1.18\times(1 + 1.3\times0.668^2)\times239.81 = 447.3\ \text{K},\quad \frac{\varepsilon_{air}}{\kappa} = 1.18\times78.8 = 93.0\ \text{K}\\ T^* &= \frac{373}{\sqrt{447.3\times93.0}} = 1.829\end{aligned}$$
> ③ 碰撞积分（式 4.1、4.4）：$\Omega_D = \Omega_{D0} + 0.196\times0^2/T^* = 1.110$
> ④ 代入式 3.1：
> $$D_{AB} = \frac{0.001858\times373^{3/2}\left(\dfrac{1}{17} + \dfrac{1}{29}\right)^{1/2}}{1\times3.272^2\times1.110} = 0.344\ \text{cm}^2/\text{s}$$
>
> **计算结果：** $D_{NH_3\text{-}air} = 0.344$ cm²/s $= 3.44\times10^{-5}$ m²/s。

**专业说法：** 极性气体用 Brokaw 修正的碰撞积分，参数由沸点数据和偶极矩估算。*EN: For polar gases, use Brokaw's corrected collision integral, with parameters estimated from boiling-point data and dipole moments.*

**优缺点**
不需要查 Lennard-Jones 表，只要沸点、沸点下液体摩尔体积和偶极矩。本例中空气无极性，$\delta_{AB} = 0$，极性修正项正好消失；但氨的 $\sigma$、$\varepsilon$ 仍是按极性公式算的。剩下的问题是：混合物里不止两种气体时怎么办。

> [!question]- 用自己的话说：Brokaw 方程
> > [!success]- 关键环节：你的回答应包含
> > - [ ] 极性分子有偶极作用，要修正碰撞积分
> > - [ ] 用偶极矩、沸点、沸点体积算极性参数 $\delta$ 和分子参数
> > - [ ] 参数用几何平均组合，最后仍代入 Hirschfelder 方程
>
> > [!example]- 一种说法
> > 像氨这样的分子一头带正电一头带负电，彼此之间多了一种拉扯。Brokaw 方法先根据它有多"极性"算一个修正值，再用沸点数据估出它的大小和作用力，最后还是代进同一个扩散公式里。

### 4.2 多组分混合物：Wilke 方程（Multicomponent mixtures: Wilke equation）（p.28–29）

**为什么需要它**
化学气相沉积里，SiH₄ 要穿过 H₂ 和 N₂ 组成的混合气扩散到硅片上（p.29）。前面所有公式都是两种气体之间的 $D$，现在有三种。

**它怎么工作**
把组分 1 的扩散阻力看成来自其他每一种气体，按它们在"不含组分 1"的气体中所占比例加权：先分别算组分 1 对每种气体的二元 $D$，再用摩尔分数（扣除组分 1 后重新归一）对 $1/D$ 加权求和、取倒数。哪种气体占得多，它对应的二元 $D$ 对结果影响就大。

**课件里的概念**（p.28）

$$D_{1\text{-mixture}} = \frac{1}{\dfrac{y_2'}{D_{1\text{-}2}} + \dfrac{y_3'}{D_{1\text{-}3}} + \cdots + \dfrac{y_n'}{D_{1\text{-}n}}} \tag{4.5}$$

$$y_2' = \frac{y_2}{y_2 + y_3 + \cdots + y_n} = \frac{y_2}{1 - y_1} \tag{4.6}$$

$D_{1\text{-}n}$：组分 1 对组分 n 的二元扩散系数；$y_n'$：按不含组分 1 计的摩尔分数。

> [!example] 实例 4.2：900 K、100 Pa 下 SiH₄ 在 H₂/N₂ 混合气中的扩散系数（p.29）
> 已知 $y_{SiH_4} = 0.0075$，$y_{H_2} = 0.015$，$y_{N_2} = 0.9775$；SiH₄ 的 $\varepsilon/\kappa = 207.6$ K、$\sigma = 4.08$ Å。H₂、N₂ 参数见 §3.1 的补充。$P = 100/101325 = 9.87\times10^{-4}$ atm。
>
> ① 二元 $D$（式 3.1，非极性，算术平均 σ）：
> $$\begin{aligned}D_{SiH_4\text{-}H_2}:&\ \sigma_{AB} = \frac{4.08 + 2.968}{2},\ T^* = \frac{900}{\sqrt{207.6\times33.3}}\ \Rightarrow\ D = 4059\ \text{cm}^2/\text{s}\\ D_{SiH_4\text{-}N_2}:&\ \sigma_{AB} = \frac{4.08 + 3.681}{2},\ T^* = \frac{900}{\sqrt{207.6\times91.5}}\ \Rightarrow\ D = 1091\ \text{cm}^2/\text{s}\end{aligned}$$
> ② 无 SiH₄ 基准的摩尔分数（式 4.6）：
> $$y_{H_2}' = \frac{0.015}{1 - 0.0075} = 0.0151,\qquad y_{N_2}' = \frac{0.9775}{1 - 0.0075} = 0.9849$$
> ③ Wilke 方程（式 4.5）：
> $$D_{SiH_4\text{-mix}} = \frac{1}{\dfrac{0.0151}{4059} + \dfrac{0.9849}{1091}} = 1104\ \text{cm}^2/\text{s}$$
>
> **计算结果：** $D_{SiH_4\text{-mix}} = 1104$ cm²/s $= 0.110$ m²/s。压力只有 100 Pa，所以比常压下大约三个数量级。

**专业说法：** 稀组分在多组分气体中的扩散系数用 Wilke 方程，由各二元扩散系数按无该组分基准的摩尔分数调和平均。*EN: For a dilute species in a multicomponent gas, the Wilke equation harmonically averages the binary diffusivities, weighted by solute-free mole fractions.*

**优缺点**
只需要二元数据就能处理任意多组分。代价是每一对都要先算一次二元 $D$。本讲只讲了气体，液体和固体中的扩散留给下一讲。

> [!question]- 用自己的话说：Wilke 方程
> > [!success]- 关键环节：你的回答应包含
> > - [ ] 先算组分 1 对其他每种气体的二元 $D$
> > - [ ] 摩尔分数要扣除组分 1 后重新归一
> > - [ ] 按这些分数对 $1/D$ 加权求和再取倒数
>
> > [!example]- 一种说法
> > 一种气体要穿过好几种气体组成的人群，它受到的阻力是各种气体分别造成的阻力按人数比例加起来。人多的那种气体说了算。先算出跟每种气体一对一时的扩散系数，再按比例合成一个总的。

### 误区与陷阱

> [!failure] 陷阱 4.1：Brokaw 方法里 σ_AB 也用算术平均
> **反例：** 实例 4.1 若用算术平均 $(2.958 + 3.619)/2 = 3.288$ Å，$D$ 会算成 0.341 cm²/s；按课件用几何平均 3.272 Å 得 0.344 cm²/s。
> **为什么不对：** 课件 p.26 规定 Brokaw 方法中 $\sigma_{AB} = (\sigma_A\sigma_B)^{1/2}$，见 [[#4.1 极性气体：Brokaw 方程（Polar gases: Brokaw equation）（p.25–27）|§4.1]]。
> **正确说法：** 非极性 Hirschfelder 用算术平均，Brokaw 用几何平均。*EN: Arithmetic-mean σ for the non-polar Hirschfelder route; geometric-mean σ for Brokaw.*

> [!failure] 陷阱 4.2：Wilke 方程直接用原始摩尔分数
> **反例：** 实例 4.2 中若直接用 $y_{N_2} = 0.9775$ 而不是 $y_{N_2}' = 0.9849$，权重之和不等于 1。
> **为什么不对：** 权重应只在"其他气体"之间分配，必须扣除组分 1 后重新归一，见 [[#4.2 多组分混合物：Wilke 方程（Multicomponent mixtures: Wilke equation）（p.28–29）|§4.2]]。
> **正确说法：** 用 $y_n' = y_n/(1 - y_1)$。*EN: Use solute-free mole fractions y'_n = y_n / (1 − y_1).*

> [!question]- 暂停：拿到一个气体扩散问题，怎么决定用哪个公式？
> > [!success]- 关键环节：你的回答应包含
> > - [ ] 先查表 J.1，查得到就用（注意除以压力）
> > - [ ] 非极性：有 LJ 参数用 Hirschfelder，没有用 Fuller
> > - [ ] 极性用 Brokaw；三种以上组分用 Wilke 组合二元值
>
> > [!question]- 预测：实例 4.2 中如果 H₂ 和 N₂ 的比例对调（$y_{H_2} = 0.9775$，$y_{N_2} = 0.015$），$D_{SiH_4\text{-mix}}$ 会更接近哪个二元值？
> > > [!success]- 展开答案
> > > 更接近 $D_{SiH_4\text{-}H_2} \approx 4059$ cm²/s，因为权重由占多数的气体决定。检验的是"按无溶质摩尔分数加权"一环。

---

## 复习与练习

### 本讲小结

| 概念 | 一句话 | 关键公式 |
| --- | --- | --- |
| 扩散系数量级 | 气体 > 液体 > 固体，各差几个数量级 | 气体 $10^{-6}$–$10^{-5}$ m²/s |
| $D_{AB} = D_{BA}$ | 二元、总浓度不变时对称 | $J_A = -J_B$ |
| 自扩散 | 平均自由程 × 平均速度 | $D_{AA^*} = \lambda u/3$ |
| 硬球二元 | $D \propto T^{3/2}/P$ | 式 2.4 |
| Hirschfelder | 加碰撞积分修正分子间作用力 | 式 3.1 |
| Fuller | 无 LJ 参数时用扩散体积 | 式 3.3 |
| Brokaw | 极性气体修正 $\Omega_D$ | 式 4.1–4.4 |
| Wilke | 多组分：二元值按无溶质摩尔分数调和平均 | 式 4.5 |

### 练习

#### 练习 1 · 量级判断
有人算出某气体对的 $D = 2\times10^{-9}$ m²/s。这个数可信吗？
> [!success]- 展开答案
> 不可信。气体的 $D$ 在 $10^{-6}$–$10^{-5}$ m²/s，$10^{-9}$ 是液体的量级，很可能单位或公式用错了。

#### 练习 2 · 对称性的前提
$D_{AB} = D_{BA}$ 需要什么前提？
> [!success]- 展开答案
> 二元体系、总摩尔浓度不变（气体即恒温恒压）。

#### 练习 3 · 压力的作用
为什么低压 CVD 反应器里的扩散系数比常压大得多？
> [!success]- 展开答案
> 压力低 → 分子稀 → 平均自由程长 → $D$ 大，$D \propto 1/P$。

#### 练习 4 · 碰撞积分的方向
温度升高时 $\Omega_D$ 怎么变？对 $D$ 有什么影响？
> [!success]- 展开答案
> $\Omega_D$ 减小，所以 $D$ 随温度增加得比 $T^{3/2}$ 更快。

#### 练习 5 · 选公式
要估某有机蒸气在氮气中的 $D$，查不到它的 Lennard-Jones 参数，也不是极性分子，该用哪个公式？
> [!success]- 展开答案
> Fuller 关联式，按原子扩散体积加和得到 $\Sigma v$。

#### 练习 6 · 单位
Hirschfelder 方程中 $P$ 和 $\sigma$ 分别用什么单位？
> [!success]- 展开答案
> $P$ 用 atm，$\sigma$ 用 Å；结果 $D$ 为 cm²/s。

#### 练习 7 · 连接 §1 和 §3
用表 J.1 的 273 K 数据外推到 293 K 时，为什么要乘 $\Omega_D$ 的比值？
> [!success]- 展开答案
> 因为 $D \propto T^{3/2}/\Omega_D$，温度变化时 $\Omega_D$ 也变了，只乘 $(T_2/T_1)^{3/2}$ 会低估温度效应。

#### 练习 8 · 极性修正何时消失
氨在空气中扩散时，为什么 Brokaw 的极性修正项为零？
> [!success]- 展开答案
> 空气偶极矩为 0，所以 $\delta_{air} = 0$，$\delta_{AB} = \sqrt{\delta_{NH_3}\delta_{air}} = 0$，修正项 $0.196\delta_{AB}^2/T^*$ 为零。

#### 练习 9 · Wilke 的权重
Wilke 方程里为什么要用扣除组分 1 后的摩尔分数？
> [!success]- 展开答案
> 组分 1 的阻力来自其他气体，权重只应在其他气体之间分配，扣除后各权重之和才等于 1。

#### 练习 10 · 连接 §2 和 §3
硬球模型给出 $D \propto T^{3/2}$。为什么 Hirschfelder 方程里 $D$ 随温度增加得更快？
> [!success]- 展开答案
> Hirschfelder 方程的分母多了 $\Omega_D$，它随温度升高而减小，所以整体增长快于 $T^{3/2}$。

### 术语中英对照

| 术语 | English | 一句话含义 |
| --- | --- | --- |
| 扩散系数 | diffusion coefficient / mass diffusivity | Fick 定律中的比例系数 |
| 自扩散系数 | self-diffusion coefficient | 分子在其同位素中的扩散系数 |
| 平均自由程 | mean free path | 两次碰撞之间的平均距离 |
| 碰撞直径 | collision (Lennard-Jones) diameter | 两分子中心能靠近的最小距离 |
| 碰撞积分 | collision integral | 修正分子间作用力的无量纲因子 |
| 扩散体积 | diffusion volume | Fuller 关联式中代表分子大小的量 |
| 偶极矩 | dipole moment | 衡量分子极性的量 |
| 无溶质摩尔分数 | solute-free mole fraction | 扣除扩散组分后重新归一的摩尔分数 |

### 参考文献

- [Pearce et al., 2020] Pearce, B. K. D., Ayers, P. W., & Pudritz, R. E. (2020). CRAHCN-O: A consistent reduced atmospheric hybrid chemical network oxygen extension for hydrogen cyanide and formaldehyde chemistry in CO₂-, N₂-, H₂O-, CH₄-, and H₂-dominated atmospheres. arXiv:2009.12375（附表 Lennard-Jones 参数引自 Welty et al.）. https://arxiv.org/pdf/2009.12375

---

## 个人补充

> [!note] 我的理解
> （留给你自己写）

> [!info]- PPT 原文（Slides 1–32）
> **Slides 1–3**: 封面 / 目录 / 章节页
> **Slide 4**: $D$ 的量纲与单位；依赖压力、温度、组成、介质；气体、液体、固体的量级
> **Slides 5–6**: 表 J.1 气体二元扩散系数（$D_{AB}P$）
> **Slide 7**: 表 J.2 液体二元扩散系数
> **Slide 8**: 表 J.3 固体二元扩散系数
> **Slide 9**: $D_{AB} = D_{BA}$ 的条件与推导
> **Slide 10**: 章节页 Estimation of Diffusion Coefficient (Gas Diffusivity)
> **Slide 11**: 动力学理论的四条假设
> **Slides 12–13**: 自扩散系数 $D_{AA^*} = \lambda u/3$，平均自由程与平均速度，代入后的式子及符号单位
> **Slide 14**: 平均自由程的定义与随分子数密度的变化
> **Slide 15**: Lennard-Jones / 碰撞直径的定义
> **Slide 16**: 二元混合物硬球公式，$D_{AB} = D_{BA}$
> **Slide 17**: 气相扩散依赖 $P$、$T$，可用于换算
> **Slide 18**: Hirschfelder 方程及符号单位
> **Slide 19**: 碰撞积分与无量纲温度，$\Omega_D$ 曲线
> **Slide 20**: $\Omega_D$ 随温度下降；$P$、$T$、$\Omega_D$ 外推式
> **Slide 21**: Example 1（CO₂–空气，20 °C，与表 J.1 比较）
> **Slides 22–23**: Fuller 关联式；原子和分子扩散体积表
> **Slide 24**: Example 2（苯–空气，30 °C，1 atm）
> **Slides 25–26**: Brokaw 方程：极性修正、$\delta$、$\varepsilon/\kappa$、$\sigma$ 的估算式与 $\Omega_{D0}$ 关联式常数
> **Slide 27**: Example 3（NH₃–空气，373 K）
> **Slide 28**: Wilke 方程与无溶质摩尔分数
> **Slide 29**: Example 4（SiH₄ CVD，900 K，100 Pa）
> **Slides 30–32**: Take Home Message
