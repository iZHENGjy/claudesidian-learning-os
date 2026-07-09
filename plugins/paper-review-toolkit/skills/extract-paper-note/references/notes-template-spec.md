# notes.md 规范

**给人扫读用** —— 30 秒抓住核心，2 分钟读完全篇。

设计原则：
- **不重复 alt** — 单图描述看 main.md 里的 alt text，notes 只写跨图整合 / 主观判断 / 引用
- **结构化扫读** — bullet / 表格 / inline 图 替代长段落
- **inline 嵌关键图** — 不用跳到 main.md 翻图，notes 自己有"配图"

## 完整模板

```markdown
---
paper_code: SS-X
title: "..."
authors: [...]
year: YYYY
journal: ...
doi: ...
type: research / research-communication / review
contributes_to:
  - {topic: <slug>, relevance: high}
  - {topic: <slug>, relevance: medium}
cross_paper_relations: []
---

# 一句话

(30 字内。读完这句就知道这篇的核心声明。bold 关键词。)

---

# 实验目的（为什么做）

- **动机**: 想解决什么问题 / 填什么空白（一句话）
- **创新点 A**: 一句话
- **创新点 B**: 一句话

(动机 1 条 + 创新点 ≤ 3 条)

---

# 实验结构（设计了哪几组对照）

逐组列出，**和主 Excel "样本数据" 的 Group(var_code) 一一对应**：

| Group | 变量 | 对照内容 | 样本 | 测了什么 |
|---|---|---|---|---|
| A1 | 单体种类 | 叠氮 vs 无叠氮端块 | S1 vs S3 | Fig1 流变, Fig4 电导 |
| A8 | 化学交联 | 交联 vs 物理 | S1 vs S2 | Fig2 流变, Fig3 拉伸 |
| ... | ... | ... | ... | ... |

(这是"逆向出的实验设计"，让人一眼看懂论文怎么布的局)

---

# 实验过程（配方 + 制备 + 测试）

- **配方**: 单体 / IL / 引发剂 / 交联 / 固含量（一句话浓缩）
- **制备**: 关键合成 / 成型步骤（≤ 3 步）
- **测试方法**: 用了哪些表征（流变 / 拉伸 / 阻抗 / ...）+ 关键条件

---

# 核心图

## Fig N — 一句话标题

![Fig N — alt 简版 (从 main.md alt 拿核心信息)](images/figN_topic.jpg)

> 一两句注解：为什么这图核心？读图的关键点？

## Fig M — 一句话标题

![...](images/figM_topic.jpg)

> ...

(嵌 2-4 张最关键 figure。每张配一行 quote-style 注解。)

---

# 机理（跨图整合）

| 主张 | 证据图 |
|---|---|
| 主张 1 | Fig A + Fig B (一句话怎么证) |
| 主张 2 | Fig C + Fig D |
| 主张 3 | 推断（无直接证据），借 ref XX |

(表格代替长段落。每行一个跨图整合的因果链。)

---

# 关键 quote

> "verbatim quote 1..." (sec X.Y, fig N, p M)

> "verbatim quote 2..." (sec X.Y, p M)

(2-4 条。每条 bold 关键数字 / 术语)

---

# Limitations

**作者自承**
- bullet

**我看到的**
- bullet

(各 2-4 条 bullet)

---

# 跨论文关系

(placeholder — 待 cross-paper-review skill 填)
```

## 关键规则

1. **不要 emoji** — 用纯标题
2. **inline 嵌图** — 用 `![alt](images/figN.jpg)` 嵌在 notes，不是只引用图号
3. **每嵌一图，配 1-2 行 > quote-style 注解** — 解释为什么这图核心
4. **机理用表格** — 每行 = 一个跨图整合主张 + 证据图列表
5. **创新点 ≤ 3 bullet** — 多了读不动
6. **一句话总结放最前面** — 30 字内，给极速扫读用
7. **bold 关键数字 + 术语** — 让眼睛能跳读

## "不重复 alt" 检查方法

写完后 grep main.md 看相同描述是否在 alt 已出现：
- 如果 alt 已说 "Fig 3 shows σ rising with IL_wt"
- notes 不该再写 "σ rises with IL_wt"
- notes 应写 "Fig 3 + Fig 5 联合证明：σ 上升源于 IL-rich domain 连通而非密度提升"（跨图整合）

## contributes_to slug 规则

- 用 Paper 1 综述大纲 (`00_Inbox/Ionogel_Paper_Outlines_Final.docx`) Heading 2/3 转 slug
- 转换：去章节号 + 中划线 + 小写
  - `2.3 Phase Separation Mechanisms` → `phase-separation-mechanisms`
  - `3.1 Ionic Conductivity` → `ionic-conductivity`
- **slug 必须在大纲词表里**（不在则警告 + 标 `_unknown_topic`，不丢弃）
- **relevance**: high / medium / low

## quote 出处格式

- `(sec X.Y, fig N, p M)` 三个 anchor 至少给 2 个
- 顺序: sec → fig → page（写综述时优先按 sec 引）
- 多 panel: `fig 4a` / `fig S2c`

## 跨论文关系 placeholder

- 第一遍不写（单篇视野看不出）
- 等独立 `cross-paper-review` skill 跑（后期写）
