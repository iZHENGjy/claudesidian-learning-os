# 性能数据落点规范

抽到的性能数据往主 Excel 填时，4 种情况怎么处理（On-Skin SS-8 压测总结出来的）。

## 1. 单位对齐到列名

主 Excel 列名自带单位，handoff 的值**必须换算到该单位**：
- 论文 `57.8 kPa` → 列 `Adhesion Strength (MPa)` 填 `0.0578`
- 论文 `886%` → 列 `Elongation at Break (%)` 填 `886`
- 论文 `2479 kJ/m³` → 列 `Toughness (MJ/m³)` 填 `2.479`

原始值 + 换算关系写进 notes（万一换算错能追溯）。模型在生成 handoff 时换算，**脚本不做语义换算**。

## 2. 主 Excel 没有对应列 → 不硬塞

有些指标主 Excel 48 列里压根没有：lift-off force (N/m)、specific capacitance (μF/cm²)、tan δ、剪切模量 G′、gauge factor 有列但 response time 单位是 μs……

- ❌ **不要**塞进物理量不同的列（lift-off force N/m ≠ Adhesion Strength MPa，是线密度不是压强）
- ✅ 进 `notes.md` 的"额外指标"段：`物理量_单位: 值 [ai]`
- ✅ checklist 该图标 `✗` + 说明"主 Excel 无对应列"
- ✅ 追一行到 `papers/_missing_columns.log`：`SS-X | 指标名 | 单位 | 出处` —— 跨论文统计高频缺列，攒够了再决定要不要给主 Excel 加列（不为单篇改 schema）

## 3. 定性演示（无数值）→ 只入卡片，不展开样本数据

应用类测试常是定性信号：运动监测 ΔR/R 波形、不同基底的定性对比图——**没有单一数值**。

- 样本卡片记该变量取值序列（如 `G1: finger/wrist/ankle/neck`，样本数=部位数）
- 样本数据**不展开成行**（没数值可填，展开了全是空行，反而虚增）
- notes 描述定性结论（"能区分 45°/90° 手指弯曲"）

判断：**有数值才进样本数据行；纯定性演示只进卡片 + notes**。

## 4. 依赖 SI 但 SI 没抽到 → 标注，不编造

若某数据在 SI 表（如 Table S3 力学汇总）但 `si.md` 没抽到（见 `failure-modes.md` 的 si.pdf==main.pdf 检测）：

- 缺的值填 `[缺-SI未抽到]`，**不**从正文趋势编造精确数字
- 能从正文拿到的（如"HV31 模量 15.6 MPa"正文有）照填
- 报告里提示用户："SI 没抽到，中间样本 X/Y 的力学值缺，需补 SI 重抽"

## _missing_columns.log 格式

```
# SS-X | 指标 | 单位 | 出处
SS-8 | lift-off force | N/m | fig4a
SS-8 | specific capacitance | μF/cm² | fig3a
SS-8 | tan delta | - | figS8
```
攒到某指标多篇都出现 → 提议给主 Excel"样本数据"加列（一次性，惠及所有论文）。
