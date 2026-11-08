# paper-review-toolkit

**文献综述数据抽取** — turns papers already processed by `ingest-paper` into rows of one master spreadsheet, plus a short reading note and a figure-by-figure checklist for review. Built on a real review project of 150+ papers (ionogels); the mechanics are domain-agnostic, the shipped column mapping is the ionogel example.

**Requires** `claudesidian-notes` (its `ingest-paper` skill produces the input) and `openpyxl`.

## How it fits

```text
paper PDF (main + SI)
   │  claudesidian-notes / ingest-paper
   ▼
main.md + si.md + images/figN_*.jpg (vision-checked alt text) + meta.yaml
   │  paper-review-toolkit / extract-paper-note
   ▼
extract_handoff.json          columns already named as in the master spreadsheet
notes.md · checklist.md       for you: what the paper did, and where each figure went
   │  scripts/write_to_excel.py   (backs up first, writes mechanically, no judgement)
   ▼
master spreadsheet, 4 sheets  papers · sample data · sample cards · overview matrix
   │  you review rows marked [ai] once, in one place
   ▼
verified data, ready to cite when writing the review
```

**Design rule:** the model reads the paper and decides what goes in each column; the script only finds the right place, backs up, and writes. No intermediate schema, no semantic decisions in code.

## Skill: `extract-paper-note`

| Say | Not for |
|---|---|
| "抽这篇论文的数据" / "extract paper note" / "整理 SS-X 的数据" | papers not yet run through `ingest-paper`; reviews and perspectives; lectures or tutorials |

Key rules (details in `SKILL.md`):
- One control-experiment group = one variable code, one row per value. A condition that is only a measurement axis (e.g. temperature in an Arrhenius plot) is **not** a group.
- Prefer fewer groups that match the paper's own design over inflating rows.

## Contents

```text
skills/extract-paper-note/
├── SKILL.md
├── references/
│   ├── data-mapping-spec.md      how paper content maps to spreadsheet columns
│   ├── notes-template-spec.md    notes.md structure
│   ├── checklist-spec.md         checklist.md structure
│   └── failure-modes.md          pitfalls from real runs
├── scripts/write_to_excel.py     handoff.json → master spreadsheet
└── assets/notes-blank-template.md
```

```bash
python scripts/write_to_excel.py extract_handoff.json --master "path/to/master.xlsx"
python scripts/write_to_excel.py extract_handoff.json --master "path/to/master.xlsx" --dry-run   # print what would be written
export REVIEW_MASTER_XLSX="path/to/master.xlsx"     # or set once; then --master can be omitted
```

The script has no built-in spreadsheet path: it exits with an error unless `--master` or `REVIEW_MASTER_XLSX` is given. It backs up the spreadsheet before every real write.

## Adapting to your own review

The four sheet layouts and the shipped column mapping come from the author's ionogel review and are an example. For another topic: point `--master` (or the `REVIEW_MASTER_XLSX` environment variable) at your spreadsheet, and rewrite `references/data-mapping-spec.md` for your columns. `write_to_excel.py` writes by column name, so the sheet structure is the only thing that needs to match.
