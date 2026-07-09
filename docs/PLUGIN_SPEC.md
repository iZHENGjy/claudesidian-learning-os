# Plugin Spec: three layers + how to add a new domain
# 插件规范：三层分工 + 怎么加一个新领域

> **What this file says**: how the plugin system is layered, and what a new domain plugin must provide.
> **When to read it**: when you want to add a new domain (law / medicine / music / any subject).
> **What you can do after**: build a new plugin from the checklist in section 3, reusing the framework layer instead of rewriting it.

## 1. Three layers / 三层架构

```
Domain plugins   chemeng-coursework (chemical engineering, reference impl.) │ yours…
领域插件层         ↑ domain knowledge only: specialty plotting, handbooks, conventions

Framework        claudesidian-notes (course + paper pipeline) + paper-review-toolkit
框架层             ↑ domain-agnostic: ingest → distill → reverse-audit;
                   battle-tested on engineering / economics / CS / physics courses

Kernel           vault structure (PARA) · manifest mechanism · MinerU wrapper
内核层            (shared/scripts/) · your vault's CLAUDE.md routing
```

Rules / 原则:
- The framework layer must contain **no domain words** (domain terms may appear only as examples). 框架层不许出现领域词。
- Domain plugins must **not reimplement** framework mechanics (MinerU calls, manifest read/write, templates). 领域插件不许重写框架已有机制。

## 2. What the framework provides / 框架层提供什么

| Mechanism | Where | Purpose |
|---|---|---|
| MinerU wrapper | `claudesidian-notes/shared/scripts/mineru_extract.py`, `mineru_convert.py` | any PDF → markdown + images |
| Page renderer | `shared/scripts/extract_images.py` | per-page PNGs for vision checking |
| SI dispatcher | `shared/scripts/process_si.py` | multi-format supplementary-info handling |
| Manifest mechanism | each course's `manifest.md` | declare materials/indexes; skills grep on demand, never hardcode globs |
| Note templates | each skill's `assets/*.md` | lecture / tutorial / principles skeletons |
| Formula loop | `shared/scripts/extract_formulas.py` / `validate_principles.py` / `reverse_audit.py` | force-scan (no LLM recall) / self-check / solutions-vs-principles audit |
| Data honesty rule | ingest-tutorial SKILL | unfound reference data gets "please verify", never fabricated |

## 3. New domain plugin checklist / 新领域插件清单

Copy the structure of `plugins/chemeng-coursework/`:

```
plugins/<your-domain>/
├── .claude-plugin/plugin.json   # name / version / description / skills array
└── skills/<skill-name>/
    ├── SKILL.md                 # ≤250-line entry: frontmatter (name + description
    │                            #   with Triggers / Not-triggers) + workflow
    ├── references/              # detailed rules, Read on demand
    ├── scripts/                 # domain-specific scripts (e.g. ChemE plotting lib)
    └── assets/                  # domain templates
```

Four steps / 四步接入:
1. Create the directory above and write SKILL.md (spell out Triggers / Not-triggers in the description — any language). 建目录写 SKILL.md。
2. Add an entry to `.claude-plugin/marketplace.json` in the repo root. marketplace.json 加一条。
3. Add a trigger-word line to your vault's CLAUDE.md routing section. 你 vault 的 CLAUDE.md 路由段加一行。
4. Run it once on real material; write the pitfalls into `references/lessons.md`. 用真实材料跑通一次，坑写进 lessons.md。

## 4. Language conventions / 语言约定

- Folder/course names are language-free: `01_Projects/<CODE>_<course name>/` — Chinese, English, Japanese, anything. 目录/课名不限语言。
- SKILL.md bodies are currently Chinese (author's working language); bilingual descriptions in frontmatter are encouraged (list trigger words in both languages). 欢迎双语化。
