# claudesidian-learning-os

**A personal learning OS for Claude Code + Obsidian — ingest any course or paper into machine-verifiable notes, in any language, for any subject.**

[中文版在下面 ↓](#中文版)

## What is this

Three Claude Code plugins that turn an Obsidian vault into a study pipeline:

| Plugin | Layer | What it does |
|---|---|---|
| `claudesidian-notes` | Framework | Lecture/tutorial/paper PDF → MinerU extraction → vision-checked **step-by-step teaching notes** → first-principles formula maps (`_principles.md`) → solutions reverse-audited against them → **exam review vault** (cheat sheet, traps, question bank) → **quizzes** with concept-level mastery tracking |
| `paper-review-toolkit` | Framework | Literature-review projects: paper folders → structured data extraction → master spreadsheet |
| `chemeng-coursework` | Domain (reference) | Chemical-engineering homework companion: decision-first coaching, ChemE plotting library (ternary / McCabe-Thiele / psychrometric...), docx polishing |

The framework layer has **zero domain knowledge** — it has ingested engineering, economics, CS, physics and polymer courses without a line changed. The chemical-engineering plugin is the worked example of how to build your own domain plugin (law, medicine, music — see `docs/PLUGIN_SPEC.md`).

## See it on a real course

[`examples/CME222-mass-transfer`](examples/CME222-mass-transfer) is a real chemical-engineering course run through the pipeline. Same 32-slide lecture, old notes vs new:

| | Before | After |
|---|---|---|
| Lecture examples worked to a number | 0 / 4 | **4 / 4**, checked by `verify.py` |
| Formula errors | 1 (Brokaw coefficient 0.19 instead of 0.196) | 0 |
| Self-checks | none | 8 own-words checks, 4 prediction questions, 10 exercises |
| Dead links | 10 | 0 |

Plus a review vault for the whole course: 5 topics, 50 questions with folded answers, every application answer script-verified, and a mastery dashboard after one quiz round.

## Why it's different

- **Two outputs for two jobs** — while the course runs, each lecture becomes a teaching note: every idea starts from the problem it solves, every lecture example is worked to a number, and every section ends with a "say it in your own words" self-check and a prediction question. Before the exam, the whole course is condensed into a review vault (one-page formulas, all traps, a question bank with folded answers) that the `quiz` skill drills you on, tracking which concepts you still miss.
- **Verifiable, not vibes** — every number in a note is re-computed by a `verify.py` with asserts, formulas are force-scanned by script, every generated figure is vision-checked, tutorial solutions are reverse-audited against the principles file, and anything beyond the slides must cite a checked source or be marked "to verify".
- **Manifest-driven** — skills never hardcode file globs; each course declares its materials in a `manifest.md` that skills read at run time.
- **Honest data policy** — a reference value that can't be found in indexed sources is flagged "please verify", never fabricated.

## Requirements

- [Claude Code](https://claude.com/claude-code) + an Obsidian vault using PARA-style folders (the [claudesidian](https://github.com/heyitsnoah/claudesidian) starter kit is a great base)
- Python 3.10+ with `requests PyMuPDF Pillow python-pptx python-dotenv rich pyyaml` (paper SI handling adds `python-docx openpyxl pandas`; ChemE psychrometric charts add `psychrolib`)
- A free [MinerU](https://mineru.net) API token for PDF extraction — set `MINERU_API_TOKEN` in your environment or a `.env` file

## Quickstart

```bash
git clone https://github.com/iZHENGjy/claudesidian-learning-os
```

In Claude Code, inside your vault:

```
/plugin marketplace add <path-or-url-of-this-repo>
/plugin install claudesidian-notes@claudesidian-learning-os
```

Then drop a lecture PDF anywhere and say **"ingest this lecture"**. Notes land in `01_Projects/<CODE>_<course name>/L##_<topic>.md` — the course name can be in any language. Before the exam say **"build the review vault for <CODE>"**, then **"quiz me on <CODE>"**.

## Vault conventions the framework expects

```
01_Projects/<CODE>_<course name>/
├── index.md          # MOC, appended per week
├── manifest.md       # declares source PDFs + extraction indexes (skills update it)
├── L01_<topic>.md    # lecture teaching notes
├── T01_<topic>.md    # tutorial solutions
├── _principles.md    # distilled formula map with numbered equations
├── 复习库/            # review vault: overview, cheat sheet, traps, question bank, mastery
└── _attachments/     # sources + MinerU output + per-lecture verify.py
```

## Building your own domain plugin

Four steps, ~copy the `chemeng-coursework` structure. See [`docs/PLUGIN_SPEC.md`](docs/PLUGIN_SPEC.md).

## Language

Content is language-agnostic. Skill prompts are currently written in Chinese (the author's working language); the mechanics work in any language and bilingual contributions are very welcome.

## Credits

Grew out of a vault based on [claudesidian](https://github.com/heyitsnoah/claudesidian) by Noah Brier. PDF extraction by [MinerU](https://github.com/opendatalab/MinerU). The teaching-note structure borrows ideas from [Love Learning Anything](https://github.com/RAIZ-Zzz/love-learning-anything) (MIT); the review vault and quiz borrow from [tutor-skills](https://github.com/RoundTable02/tutor-skills) (MIT). License: [MIT](LICENSE).

---

# 中文版

**Claude Code + Obsidian 的个人学习操作系统——把任何课程、任何论文吃成机器可校验的笔记，语言不限、学科不限。**

## 这是什么

三个 Claude Code plugin，把 Obsidian vault 变成学习流水线：

| Plugin | 层 | 干什么 |
|---|---|---|
| `claudesidian-notes` | 框架层 | lecture/tutorial/论文 PDF → MinerU 抽取 → vision 核对的**讲解型笔记** → 第一原理公式图谱 → 解题反向对账 → **复习库**（速查 / 易错 / 题库）→ **测验**（按概念记录掌握度） |
| `paper-review-toolkit` | 框架层 | 文献综述项目：论文文件夹 → 结构化数据抽取 → 主表格 |
| `chemeng-coursework` | 领域层（参考实现） | 化工作业助手：决策前置辅导、化工画图库、docx 排版 |

框架层**没有任何领域知识**——工科、经济学、CS、物理、高分子课程都跑过，一行没改。化工插件是"怎么做自己领域插件"的现成示范（法学/医学/音乐都行，见 `docs/PLUGIN_SPEC.md`）。

## 真实课程效果

[`examples/CME222-mass-transfer`](examples/CME222-mass-transfer) 是一门真实化工课程（传质）跑完流水线的产出。同一讲 32 页课件，新旧笔记对比：

| | 旧版 | 新版 |
|---|---|---|
| 课件例题算到结果 | 0 / 4 | **4 / 4**，verify.py 验算 |
| 公式错误 | 1 处（Brokaw 系数 0.196 写成 0.19） | 0 |
| 自测 | 无 | 8 个"用自己的话说"、4 道预测题、10 道练习 |
| 空链接 | 10 个 | 0 |

另有整门课的复习库：5 个主题 50 题、答案折叠、应用题全部脚本验算，以及一轮测验后的掌握度看板。

## 差异点

- **两种产出各管一件事**——学期中每讲一份讲解型笔记：先讲问题再给概念、课件例题全部算完、每节有"用自己的话说"自测和预测题；考前把整门课压成复习库（一页公式、全部易错点、答案折叠的题库），用 `quiz` 出题考你、记录哪些概念还没掌握
- **可校验，不靠感觉**——笔记里每个数字都由 verify.py 断言验算、公式脚本强制扫描、每张图 vision 核对、解题和原理文件反向对账；课件以外的内容必须有核对过的出处，否则标"待核实"
- **manifest 驱动**——skill 绝不写死文件名，每门课在 manifest.md 声明自己的材料
- **数据诚实**——查不到的参考数据标"请核实"，绝不编造

## 快速上手

上面英文版三行命令：clone → `/plugin marketplace add` → `/plugin install`。然后丢一份 lecture PDF 说"**整理这节课**"，笔记出现在 `01_Projects/<CODE>_<课名>/L##_<主题>.md`——课名任何语言都行。考前说"**做 <CODE> 的复习库**"，再说"**考我 <CODE>**"。

依赖：Python 3.10+（包清单见英文版）+ 免费 [MinerU](https://mineru.net) token（环境变量 `MINERU_API_TOKEN` 或 `.env`）。

## 加自己的领域

四步，照抄 `chemeng-coursework` 的结构，见 [`docs/PLUGIN_SPEC.md`](docs/PLUGIN_SPEC.md)。

## 致谢

源自基于 Noah Brier 的 [claudesidian](https://github.com/heyitsnoah/claudesidian) 搭的 vault。PDF 抽取用 [MinerU](https://github.com/opendatalab/MinerU)。讲解型笔记结构借鉴 [Love Learning Anything](https://github.com/RAIZ-Zzz/love-learning-anything)（MIT），复习库和测验借鉴 [tutor-skills](https://github.com/RoundTable02/tutor-skills)（MIT）。许可证：[MIT](LICENSE)。
