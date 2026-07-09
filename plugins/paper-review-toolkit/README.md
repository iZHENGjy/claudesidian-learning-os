# paper-review-toolkit

科研综述项目"markdown → 结构化数据 → 主 Excel"自动化的下游 plugin。从 ionogel 综述项目（150+ 论文）打磨出来。

## 跟 claudesidian-notes 的关系

```
[ claudesidian-notes ]                    ← 已装 vault
   ├── ingest-paper (PDF → markdown vision pipeline)
   └── ...
        │
        ▼  main.md / si.md / images figN_xxx + alt text
[ paper-review-toolkit ]                  ← 本 plugin
   └── extract-paper-note (markdown → samples.yaml + notes + 主 Excel)
```

**前置依赖**: `claudesidian-notes` plugin 必须先装（提供 ingest-paper）。

## 包含什么

```
paper-review-toolkit/
├── .claude-plugin/plugin.json
├── skills/
│   └── extract-paper-note/
│       ├── SKILL.md
│       ├── references/   字段规范 / notes 模板 / failure modes
│       ├── scripts/      batch_append_to_excel.py
│       ├── assets/       空白 notes 模板
│       └── examples/     calibration 跑出的 SS-7 样例
└── README.md (本文件)
```

## 工作流

```
原 PDF
  │
  │  claudesidian-notes / ingest-paper
  ▼
main.md + si.md + images/figN_xxx.jpg + meta.yaml
  │   (vision 核对，alt text 含数字+趋势+反直觉)
  │
  │  paper-review-toolkit / extract-paper-note
  ▼
samples.yaml + notes.md + checklist.md
  │
  │  scripts/batch_append_to_excel.py
  ▼
主 Excel auto-append (带 [ai] 标记 + verified flag + source_ref)
  │
  │  用户在主 Excel 一处审 (筛 [ai] → 打 ✓)
  ▼
verified data → 写综述时 AI 直接拿来用
```

## 依赖的外部资源（vault 提供）

- 主 Excel `IONOGEL_dynamic.xlsx`（schema 来源 + 数据落地）
- 综述大纲 docx 在 `00_Inbox/`（contributes_to slug 词表）

## 触发

| Skill | Trigger 关键词 |
|---|---|
| extract-paper-note | "抽这篇论文的数据" / "整理 SS-X 的数据" / "做 SS-X 的笔记" |

## 后续要加的 skill

- `outline-migrate` — 综述大纲改了后 batch update 所有 notes 的 contributes_to slug
- `cross-paper-review` — 跨论文对比，填 notes.md 的"跨论文关系"placeholder
- `extra-fields-promote` — 扫所有 samples.yaml 的 extra 字段，建议高频字段提升到主 Excel
