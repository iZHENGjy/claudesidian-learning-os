# 示例：CME222 传质 · 第 3 讲

一门真实化工课（传质）的第 3 讲"分子扩散系数与气体扩散系数的估算"，从一份 32 页课件出发，走完整条流水线：讲义笔记 → 例题验算 → 复习库 → 一轮测验。

文件夹 `CME222_传质/` 就是它在 vault 里的样子（对应 `01_Projects/CME222_传质/`），可以直接复制进 Obsidian 打开。

**[在线阅读这份示例 →](https://izhengjy.github.io/claudesidian-learning-os/example/)** 笔记是按 Obsidian 写的，在线阅读页按 Obsidian 的样子显示：折叠块可以点开，带编号的公式、笔记之间的链接都正常。GitHub 的文件页不支持 Obsidian 的折叠块，只能近似显示。

> 课件原图和课件原文不随仓库分发，笔记里的课件截图位置用占位说明代替。

## 文件

```text
CME222_传质/
├── index.md                                  课程地图：本周概要 + 本周易错
├── L03_diffusion_coefficient_estimation.md   讲义笔记
├── _attachments/
│   └── CME 222 Lecture 3/
│       └── verify.py                         讲义里 4 道例题的验算
└── 复习库/
    ├── 00-总览.md                             主题地图 + 掌握度看板 + 薄弱点
    ├── 01-公式速查.md                          5 个公式 + 考前必背 5 条
    ├── 02-易错点.md                            4 条易错，每条链回讲义出处
    ├── 题库/气体扩散系数.md                     10 题，答案折叠
    ├── 掌握度/气体扩散系数.md                   一轮测验后的对错和错因
    └── verify.py                              题库 2 道计算题的验算
```

## 按顺序看

**1. 讲义笔记** — [`L03_diffusion_coefficient_estimation.md`](CME222_传质/L03_diffusion_coefficient_estimation.md)

由 `ingest-lecture` 生成。32 页课件整理成 4 个部分、8 个知识点：

| 部分 | 知识点 | 课件 |
|---|---|---|
| 1 · 扩散系数是什么 | 1.1 量纲与量级 · 1.2 二元扩散系数相等 | p.4–9 |
| 2 · 从分子运动推出 D | 2.1 自扩散系数 · 2.2 碰撞直径与二元混合物 | p.11–17 |
| 3 · 两个实用估算式 | 3.1 Hirschfelder 方程 · 3.2 Fuller 关联式 | p.18–24 |
| 4 · 极性气体与多组分混合物 | 4.1 Brokaw 方程 · 4.2 Wilke 方程 | p.25–29 |

每个知识点都按"为什么需要它 → 它怎么工作 → 课件里的概念 → 实例 → 专业说法 → 优缺点 → 用自己的话说"写；每部分结尾有误区和预测题；最后是本讲小结、10 道练习、术语中英对照。课件第 1–3、10 页是封面、目录和章节页，在 frontmatter 的 `pages_skipped` 里写明了。

**2. 例题验算** — [`_attachments/CME 222 Lecture 3/verify.py`](CME222_传质/_attachments/CME%20222%20Lecture%203/verify.py)

课件的 4 道例题（CO₂–空气、苯–空气、氨–空气、SiH₄ 在混合气中）每道一段，每个结果一条断言。课件没有印出答案，所以每段都标注了"课件未给答案"。

**3. 复习库** — [`复习库/`](CME222_传质/复习库)

由 `build-review-vault` 从讲义整理而来，只整理、不加新内容：

- [`01-公式速查.md`](CME222_传质/复习库/01-公式速查.md)：Hirschfelder、温度压力换算、Fuller、Brokaw、Wilke 五个公式，各附适用条件
- [`02-易错点.md`](CME222_传质/复习库/02-易错点.md)：4 条易错，每条写错在哪、正确做法、出处链接
- [`题库/气体扩散系数.md`](CME222_传质/复习库/题库/气体扩散系数.md)：10 题（记忆 6 · 应用 2 · 分析 2），答案折叠，每题链接到考的那一节

**4. 测验** — [`掌握度/气体扩散系数.md`](CME222_传质/复习库/掌握度/气体扩散系数.md)

一轮 `quiz`（模拟作答）后的记录：4 个概念答对 2 个，答错的两个记下了错因，并同步到 [`00-总览.md`](CME222_传质/复习库/00-总览.md) 的看板和薄弱点。

## 自己跑一遍检查

在仓库根目录：

```bash
python "examples/CME222-mass-transfer/CME222_传质/_attachments/CME 222 Lecture 3/verify.py"
python "examples/CME222-mass-transfer/CME222_传质/复习库/verify.py"
python plugins/claudesidian-notes/shared/scripts/check_note.py \
  "examples/CME222-mass-transfer/CME222_传质/L03_diffusion_coefficient_estimation.md" \
  --vault examples/CME222-mass-transfer
```

三条都应输出"全部通过"。

---

**English.** Lecture 3 of a real chemical-engineering course (mass transfer), taken from a 32-slide deck through the whole pipeline: the lecture note (4 parts, 8 concepts), a check script for its 4 worked examples, a review vault for the topic (formula sheet, 4 common mistakes, 10 questions) and one simulated quiz round. The `CME222_传质/` folder is laid out exactly as it sits in a vault. Slides are not included. Run the three commands above from the repo root; each should report a pass.
