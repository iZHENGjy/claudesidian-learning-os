# claudesidian-learning-os

**A personal learning OS for Claude Code + Obsidian — ingest any course or paper into machine-verifiable notes, in any language, for any subject.**

[中文版在下面 ↓](#中文版)

## What is this

Three Claude Code plugins that turn an Obsidian vault into a study pipeline:

| Plugin | Layer | What it does |
|---|---|---|
| `claudesidian-notes` | Framework | Lecture/tutorial/paper PDF → MinerU extraction → vision-checked structured notes → first-principles formula maps (`_principles.md`) → solutions reverse-audited against them |
| `paper-review-toolkit` | Framework | Literature-review projects: paper folders → structured data extraction → master spreadsheet |
| `chemeng-coursework` | Domain (reference) | Chemical-engineering homework companion: decision-first coaching, ChemE plotting library (ternary / McCabe-Thiele / psychrometric...), docx polishing |

The framework layer has **zero domain knowledge** — it has ingested engineering, economics, CS, physics and polymer courses without a line changed. The chemical-engineering plugin is the worked example of how to build your own domain plugin (law, medicine, music — see `docs/PLUGIN_SPEC.md`).

## Why it's different

- **Verifiable, not vibes** — formulas are force-scanned by script (not "the LLM remembers"), every generated figure is vision-checked, and tutorial solutions are reverse-audited against the principles file with exit-code-driven scripts.
- **Manifest-driven** — skills never hardcode file globs; each course declares its materials in a `manifest.md` that skills read at run time.
- **Honest data policy** — a reference value that can't be found in indexed sources is flagged "please verify", never fabricated.

## Requirements

- [Claude Code](https://claude.com/claude-code) + an Obsidian vault using PARA-style folders (the [claudesidian](https://github.com/heyitsnoah/claudesidian) starter kit is a great base)
- Python 3.10+ with `requests PyMuPDF Pillow python-pptx python-dotenv rich pyyaml` (paper SI handling adds `python-docx openpyxl pandas`; ChemE psychrometric charts add `psychrolib`)
- A free [MinerU](https://mineru.net) API token for PDF extraction — set `MINERU_API_TOKEN` in your environment or a `.env` file

## Quickstart

```bash
git clone https://github.com/<you>/claudesidian-learning-os
```

In Claude Code, inside your vault:

```
/plugin marketplace add <path-or-url-of-this-repo>
/plugin install claudesidian-notes@claudesidian-learning-os
```

Then drop a lecture PDF anywhere and say **"ingest this lecture"**. Notes land in `01_Projects/<CODE>_<course name>/L##.md` — the course name can be in any language.

## Vault conventions the framework expects

```
01_Projects/<CODE>_<course name>/
├── index.md          # MOC, appended per week
├── manifest.md       # declares source PDFs + extraction indexes (skills update it)
├── L01.md, T01.md    # lecture notes / tutorial solutions
├── _principles.md    # distilled formula map with numbered equations
└── _attachments/     # sources + MinerU output
```

## Building your own domain plugin

Four steps, ~copy the `chemeng-coursework` structure. See [`docs/PLUGIN_SPEC.md`](docs/PLUGIN_SPEC.md).

## Language

Content is language-agnostic. Skill prompts are currently written in Chinese (the author's working language); the mechanics work in any language and bilingual contributions are very welcome.

## Credits

Grew out of a vault based on [claudesidian](https://github.com/heyitsnoah/claudesidian) by Noah Brier. PDF extraction by [MinerU](https://github.com/opendatalab/MinerU). License: [MIT](LICENSE).

---

# 中文版

**Claude Code + Obsidian 的个人学习操作系统——把任何课程、任何论文吃成机器可校验的笔记，语言不限、学科不限。**

## 这是什么

三个 Claude Code plugin，把 Obsidian vault 变成学习流水线：

| Plugin | 层 | 干什么 |
|---|---|---|
| `claudesidian-notes` | 框架层 | lecture/tutorial/论文 PDF → MinerU 抽取 → vision 核对的结构化笔记 → 第一原理公式图谱 → 解题反向对账 |
| `paper-review-toolkit` | 框架层 | 文献综述项目：论文文件夹 → 结构化数据抽取 → 主表格 |
| `chemeng-coursework` | 领域层（参考实现） | 化工作业助手：决策前置辅导、化工画图库、docx 排版 |

框架层**没有任何领域知识**——工科、经济学、CS、物理、高分子课程都跑过，一行没改。化工插件是"怎么做自己领域插件"的现成示范（法学/医学/音乐都行，见 `docs/PLUGIN_SPEC.md`）。

## 差异点

- **可校验，不靠感觉**——公式脚本强制扫描、每张图 vision 核对、解题和原理文件反向对账（退出码驱动）
- **manifest 驱动**——skill 绝不写死文件名，每门课在 manifest.md 声明自己的材料
- **数据诚实**——查不到的参考数据标"请核实"，绝不编造

## 快速上手

上面英文版三行命令：clone → `/plugin marketplace add` → `/plugin install`。然后丢一份 lecture PDF 说"**整理这节课**"，笔记出现在 `01_Projects/<CODE>_<课名>/L##.md`——课名任何语言都行。

依赖：Python 3.10+（包清单见英文版）+ 免费 [MinerU](https://mineru.net) token（环境变量 `MINERU_API_TOKEN` 或 `.env`）。

## 加自己的领域

四步，照抄 `chemeng-coursework` 的结构，见 [`docs/PLUGIN_SPEC.md`](docs/PLUGIN_SPEC.md)。

## 致谢

源自基于 Noah Brier 的 [claudesidian](https://github.com/heyitsnoah/claudesidian) 搭的 vault。PDF 抽取用 [MinerU](https://github.com/opendatalab/MinerU)。许可证：[MIT](LICENSE)。
