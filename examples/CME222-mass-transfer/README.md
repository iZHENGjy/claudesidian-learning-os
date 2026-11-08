# Example · CME222 Mass Transfer（传质）

A real chemical-engineering course run through the pipeline: 4 lectures, 3 tutorials, one lecture rewritten with the new teaching-note rules, and a review vault built for the whole course.

一门真实化工课程跑完整条流水线的产出：4 讲、3 份习题；其中 L03 按新规则重写，整门课生成了复习库。

> Slide screenshots are replaced by placeholders — the lecturer's slides are not redistributed here.
> 课件截图已替换为占位文字，示例仓库不附课件原图。

## What's inside / 目录

```
vault/CME222_传质/
├── L03_diffusion_coefficient_estimation.md   ← 新格式讲解型笔记（重点看这份）
├── L01, L02, L04, T01–T03                    ← 旧格式笔记，作为复习库的来源
├── _attachments/verify.py                    ← L03 全部例题的验算脚本
└── 复习库/
    ├── 00-总览.md        掌握度看板（含一轮测验后的状态）
    ├── 01-公式速查.md     全课公式一页纸
    ├── 02-易错点.md       全课误区合集
    ├── 题库/             5 个主题 × 10 题，答案折叠
    ├── 掌握度/           按概念记录对错和错因
    └── verify.py         题库所有应用题的验算
before/L03_diffusion_coefficient_estimation.md  ← 同一讲的旧版笔记，用来对照
```

## Before → after (L03, same 32-slide lecture) / 同一讲新旧对比

| | Before / 旧版 | After / 新版 |
|---|---|---|
| Lecture examples worked to a number / 课件例题算到结果 | 0 / 4（只写思路） | **4 / 4**，`verify.py` 断言全部通过 |
| Formula errors / 公式错误 | Brokaw 系数 0.196 写成 0.19 | 已改正；Brokaw 的 σ 按课件用几何平均 |
| Data not on the slides / 课件外数据 | 无出处 | 核对后标出处，查不到的标"待核实" |
| Self-checks / 自测 | AI 以"我"的口吻写的 5 个疑问，无答案 | 8 个"用自己的话说" + 4 个"暂停"预测题 + 10 道练习 |
| Common mistakes / 误区 | 无 | 每部分 1–2 条，带数字反例 |
| Dead links / 空链接 | 10 个 | 0 个 |
| `check_note.py` | 13 处问题 | 通过 |

## Review vault / 复习库

- 5 topics, 50 questions (recall / application / analysis = 6 / 2 / 2 per topic), every question linked to the lecture section it tests. / 5 个主题 50 题，每题链接到出处小节
- All 10 application answers verified by `复习库/verify.py`. / 应用题答案全部脚本验算
- One quiz round recorded in `掌握度/气体扩散系数.md` (simulated answers, 2 / 4 correct); the dashboard and weak-spot list update accordingly. / 一轮测验（模拟作答）后的看板和薄弱点

## Reproduce / 自己验证

```bash
python vault/CME222_传质/_attachments/verify.py
python vault/CME222_传质/复习库/verify.py
python ../../plugins/claudesidian-notes/shared/scripts/check_note.py vault/CME222_传质/L03_diffusion_coefficient_estimation.md --vault vault
```
