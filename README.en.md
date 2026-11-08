<div align="center">

<a href="https://izhengjy.github.io/claudesidian-learning-os/"><img src="docs/assets/hero-en.svg" alt="Turn a course into notes that explain clearly, compute correctly, and get you through the exam" width="820"></a>

# claudesidian-learning-os

**Carry a course from the first lecture to the final exam inside Obsidian: slides → teaching notes → tutorial solutions → formula map → review vault → quizzes.**

Claude Code plugins · any subject · slides in any language

[![CI](https://github.com/iZHENGjy/claudesidian-learning-os/actions/workflows/ci.yml/badge.svg)](https://github.com/iZHENGjy/claudesidian-learning-os/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-0.4.0-2f7a4c)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-b8412c)](LICENSE)

[简体中文](README.md) · **English**

[Live demo](https://izhengjy.github.io/claudesidian-learning-os/) · [Example course](examples/CME222-mass-transfer) · [Quickstart](#quickstart)

</div>

---

**Contents**

- [A semester, step by step](#a-semester-step-by-step)
- [A course folder when it's done](#a-course-folder-when-its-done)
- [How each note is built](#how-each-note-is-built)
  - [Lecture note L##](#lecture-note-l)
  - [Tutorial solutions T##](#tutorial-solutions-t)
  - [Formula map _principles](#formula-map-_principles)
  - [Review vault and quizzes](#review-vault-and-quizzes)
- [Quality checks](#quality-checks)
- [Repository layout](#repository-layout)
- [Quickstart](#quickstart)
- [Commands](#commands)
- [Adding a plugin for your field](#adding-a-plugin-for-your-field)

---

## A semester, step by step

```mermaid
flowchart LR
    A[Slides PDF / PPT] -->|ingest-lecture| L[Lecture note<br/>L##.md]
    T[Tutorial PDF] -->|ingest-tutorial| S[Solutions<br/>T##.md]
    L -->|distill-principles| P[Formula map<br/>_principles.md]
    P -. equation numbers / audit .-> S
    L & S & P -->|build-review-vault| R[Review vault<br/>formulas · traps · questions]
    R -->|quiz| Q[Quizzes<br/>mastery record]
```

| When | You say | You get |
|---|---|---|
| After each lecture | "ingest this lecture" + the slides | A lecture note `L##.md` with its own check script |
| Doing problem sets | "solve this tutorial" | Solutions `T##.md`, citing the formula map's equation numbers |
| After a block of lectures | "distill MATH101" | A formula map `_principles.md`: the course's formulas arranged as a derivation tree |
| Before the exam | "build the review vault for MATH101" | `复习库/` (review vault): formula sheet, common mistakes, question bank by topic |
| Again and again | "quiz me on MATH101" | Rounds of 4 multiple-choice questions + an optional explain-it-back, mastery tracked per concept |

## A course folder when it's done

Everything for one course lives in one folder. The examples below use a calculus course (MATH101) for illustration; for real output, see the [example](examples/CME222-mass-transfer): lecture 3 of a chemical-engineering course, taken all the way from slides to a quiz.

```text
01_Projects/MATH101_Calculus/
├── index.md                       course map: one section per week, linking that week's notes and pitfalls
├── manifest.md                    slide inventory: processing status and note link for each PDF
├── L01_limits.md                  lecture notes, one per lecture
├── L02_derivatives.md
├── L03_differentiation_rules.md
├── L04_applications_of_derivatives.md
├── T01_limit_problems.md          tutorial solutions, one per problem set
├── T02_derivative_problems.md
├── _principles.md                 formula map
├── 复习库/                         review vault
│   ├── 00-总览.md                  overview: topic map + mastery dashboard
│   ├── 01-公式速查.md               one-page formula sheet
│   ├── 02-易错点.md                 every common mistake in the course
│   ├── 题库/<topic>.md              at least 10 questions per topic, answers folded
│   ├── 掌握度/<topic>.md            right/wrong counts and reasons per concept
│   └── verify.py                   checks every numeric answer in the question bank
└── _attachments/
    ├── source/                     original slides (not committed)
    └── <slide deck>/
        ├── full.md                 text and formulas extracted from the PDF
        ├── images/                 slide images, named course_lecture_page_topic
        └── verify.py               check script for every example in this lecture
```

## How each note is built

### Lecture note L##

One per lecture, written so you can understand the lecture without the slides. Taking lecture 2, "Derivatives":

```text
L02_derivatives.md
├── frontmatter            course, week, slide range, skipped slides and why, check result
├── At a glance            ≤ 3 sentences: what problem this lecture solves
├── Reading path           slide pages per part + one question you can answer after it
├── Prerequisites          knowledge used but not taught here (e.g. limits): assumed, or covered in which section
│
├── Part 1 · From average to instantaneous speed
│   ├── 1.1 Average rate of change (p.3–5)     ← every concept has the same 7 parts, see below
│   ├── 1.2 Definition of the derivative (p.6–9)
│   ├── Misconceptions     wrong ideas students hold confidently: counterexample → why it's wrong → correct statement
│   └── Pause              one "why" question + a prediction question in a new situation
├── Part 2 · Differentiation rules        2.1 power rule · 2.2 product and quotient rules
├── Part 3 · The chain rule               3.1 composite functions · 3.2 chain rule
│
├── Review and practice
│   ├── Summary            one line per concept: a sentence + the key formula
│   ├── Exercises (≥ 8)    mostly "why" questions, at least 2 linking two concepts, answers folded
│   ├── Glossary           Chinese–English terms
│   └── References         only sources actually cited and checked
├── Your notes             left for you; the AI doesn't write here
└── Slide transcript (folded)   key points of every slide, so coverage can be traced
```

Every concept (`###` section) follows the same order:

| Part | What goes in it |
|---|---|
| Why you need it | Where you'd get stuck without it: a concrete situation, never opening with a term or formula |
| How it works | A connected explanation from input to output, using the slide's own example |
| On the slides | The slide's definitions and points; formulas numbered |
| Example | The slide's worked example step by step, to the quantity and unit asked for |
| In practice | How practitioners say it, in Chinese and English |
| Pros and cons | Its last sentence leaves the problem the next section's "why you need it" picks up |
| In your own words | A folded self-check: 3 points you must mention + one model answer |

<details>
<summary><b>See a complete concept: §1.2 Definition of the derivative</b></summary>

<br>

> **Why you need it**
> A car's position is $s(t) = 5t^2$ (metres). Between 2 s and 3 s its average speed is 25 m/s, but the speed keeps changing, and a speed camera wants how fast it is going exactly at $t = 2$ s. With a single instant and no time interval, the average-speed formula doesn't apply.
>
> **How it works**
> Make the time interval shorter and shorter: from 2 s to 2.1 s the average speed is 20.5 m/s; from 2 s to 2.01 s it is 20.05 m/s. As the interval shrinks, the average speed settles on one number — the instantaneous speed at $t = 2$ s. The derivative is the value the average rate of change approaches as the interval shrinks to zero.
>
> **On the slides** (p.6–7)
>
> $$f'(x) = \lim_{h\to 0}\frac{f(x+h) - f(x)}{h} \tag{1.2}$$
>
> Geometrically, $f'(a)$ is the slope of the tangent to $y = f(x)$ at $x = a$.
>
> **Example 1.2** (p.8) Given position $s(t) = 5t^2$, find the instantaneous speed at $t = 2$ s.
>
> $$\frac{s(2+h) - s(2)}{h} = \frac{5(2+h)^2 - 20}{h} = \frac{20h + 5h^2}{h} = 20 + 5h$$
>
> $$s'(2) = \lim_{h\to 0} (20 + 5h) = 20\ \text{m/s}$$
>
> **Result**: the instantaneous speed at $t = 2$ s is 20 m/s.
>
> **In practice**: the derivative is a function's instantaneous rate of change at a point — the slope of its tangent line.
>
> **Pros and cons**
> The definition works for any differentiable function and says exactly what a derivative is. But every derivative means computing a limit from scratch, which gets tedious for $x^7$ or $x^2\sin x$ — we need a way that doesn't take a limit every time.
>
> **In your own words**　your answer should include:
> - [ ] the derivative is the limit of the average rate of change as the interval goes to zero
> - [ ] physically it is instantaneous speed; geometrically, the tangent slope
> - [ ] the steps: write the difference quotient → simplify → let $h \to 0$

That last "a way that doesn't take a limit every time" is exactly the "why you need it" of the next section, 2.1 power rule.

</details>

### Tutorial solutions T##

One per problem set, written so you can solve it and write it up in an exam:

```text
T02_derivative_problems.md
├── Formulas for this set      formulas used, cited by formula-map number (X.Y)
├── Data and constants         values + sources; anything not found is marked "please verify", never made up
├── Problem 1 … N
│   ├── original question + translation + formulas used
│   ├── Solution               one chain of reasoning: estimate the magnitude first, explain each step, final answer with units
│   ├── English Concise Answer   100–200 words of full sentences, ready for an English exam paper
│   ├── Pitfalls
│   └── Variants (optional)    how the answer changes if a condition changes
├── Answer table               problem → final answer → concepts involved
├── Gaps identified            weak concepts the problems exposed, linked back to the lectures
└── Feedback for the formula map   formulas used here that the map is missing or gets wrong
```

### Formula map _principles

One per course: every lecture's formulas arranged by how they derive from each other, so you can see where each one comes from:

```text
_principles.md
├── Nomenclature            Roman / Greek / sub- and superscripts, each in Chinese and English, look-alike symbols flagged
├── §1 Starting points      the most basic definitions or axioms, e.g. the limit definition of the derivative (1.1)
├── §2 … §N Derived results each says which equation it comes from and under what assumptions — e.g. the differentiation rules from (1.1) — with numbered steps
└── Equation index          number → section
```

Equation numbers run continuously through the course; tutorial solutions and the review vault cite them.

### Review vault and quizzes

The whole course condensed into a review vault. It only reorganises existing notes; nothing new is added:

```text
复习库/  (review vault)
├── 00-总览.md          overview: topic map (topic → which lectures) + mastery dashboard
├── 01-公式速查.md       one-page formula sheet: formula · meaning · when it applies, ending with "5 to memorise"
├── 02-易错点.md         every misconception in the course: what's wrong + what to do instead + source link
├── 题库/<topic>.md      ≥ 10 questions per topic, tagged recall / application / analysis, answers folded, linked to source sections
├── 掌握度/<topic>.md    updated automatically by quizzes
└── verify.py           checks every numeric answer in the question bank
```

A question-bank entry:

> **Q2 [recall] Geometric meaning of the derivative**
> What does $f'(a)$ represent on the graph of a function?
>
> <details><summary>Answer</summary>The slope of the tangent to y = f(x) at x = a. Tests: L02 §1.2</details>

Say "quiz me on MATH101", choose what this round covers (untested topics, the weakest topic, or your pick), and answer 4 multiple-choice questions. Missed concepts are recorded with the reason and asked again in a new situation next round:

| Concept | Tried | Right | Status |
|---|:---:|:---:|---|
| Limit definition of the derivative | 2 | 2 | 🟢 |
| Chain rule | 2 | 1 | 🔴 differentiating $\sin 3x$, forgot to multiply by the inner derivative 3 |
| Product rule | 1 | 0 | 🔴 wrote $(uv)'$ as $u'v'$ |

## Quality checks

A lecture note isn't done until it passes [`check_note.py`](plugins/claudesidian-notes/shared/scripts/check_note.py):

| Check | What it looks at |
|---|---|
| Numbers | Runs the lecture's `verify.py`; every example has a matching block; every result in the note appears in an assert, in the same unit |
| Slide text | Every constant in a numbered formula must be found in the slide text; where the slide prints an answer, the check must match it |
| Coverage | Every slide is cited by a section or skipped with a stated reason |
| Structure | Each concept opens with a concrete problem; misconceptions have numeric counterexamples; each part has a prediction question; ≥ 8 exercises; no links to notes that don't exist |
| Sources | Anything beyond the slides is cited or marked "to verify" |

The checker itself has [48 tests](tests) that run on every push in CI.

## Repository layout

```text
claudesidian-learning-os/
├── .claude-plugin/marketplace.json      plugin marketplace entry
├── plugins/
│   ├── claudesidian-notes/              the core plugin
│   │   ├── skills/
│   │   │   ├── ingest-lecture/          slides → lecture note
│   │   │   ├── ingest-tutorial/         problem set → solutions
│   │   │   ├── distill-principles/      all lecture notes → formula map
│   │   │   ├── build-review-vault/      notes → review vault
│   │   │   ├── quiz/                    review vault → quizzes
│   │   │   └── ingest-paper/            research paper PDF → searchable markdown
│   │   │       each skill: SKILL.md workflow · assets/ note templates · references/ writing rules and lessons learned
│   │   ├── commands/                    /distill-all  /audit-tutorials
│   │   └── shared/
│   │       ├── assets/manifest-example.md   slide inventory template
│   │       └── scripts/
│   │           ├── mineru_extract.py        PDF slides → text + formulas + images
│   │           ├── extract_images.py        one image per slide, for page-by-page checking
│   │           ├── check_note.py            lecture-note checker
│   │           ├── extract_formulas.py      lists every formula in a course
│   │           ├── validate_principles.py   formula-map self-check
│   │           ├── reverse_audit.py         audits tutorial solutions against the formula map
│   │           └── mineru_convert.py · process_si.py   paper and supplementary-file conversion
│   ├── chemeng-coursework/              chemical-engineering homework coach (example domain plugin)
│   └── paper-review-toolkit/            literature reviews: pull paper data into one spreadsheet
├── examples/CME222-mass-transfer/       real example: one lecture from slides to quiz
├── tests/                               tests for check_note.py
└── docs/                                demo site · plugin spec PLUGIN_SPEC.md
```

## Quickstart

**You need**: [Claude Code](https://claude.com/claude-code), an Obsidian vault, Python 3.10+, and a free [MinerU](https://mineru.net) token (it turns PDF slides into text).

**1. Install the Python dependencies**

```bash
pip install requests PyMuPDF Pillow python-pptx python-dotenv rich pyyaml
```

**2. Add your token**: create a `.env` file at the vault root containing

```text
MINERU_API_TOKEN=<your token>
```

**3. Install the plugin**: open Claude Code inside the vault and enter

```text
/plugin marketplace add iZHENGjy/claudesidian-learning-os
/plugin install claudesidian-notes@claudesidian-learning-os
```

**4. Start**: give Claude a slide deck and say "ingest this lecture". The first time for a course, it asks for the course code and name, then creates `01_Projects/<CODE>_<course name>/`. The name can be in any language.

## Commands

| Say | Skill / command | Output |
|---|---|---|
| "ingest this lecture" / "process these slides" | `ingest-lecture` | `L##_<topic>.md` + `verify.py`; updates `index.md` and `manifest.md` |
| "solve this tutorial" | `ingest-tutorial` | `T##_<topic>.md` |
| "distill MATH101" | `distill-principles` | `_principles.md` |
| "build the review vault for MATH101" | `build-review-vault` | `复习库/` |
| "quiz me on MATH101" | `quiz` | a quiz round; updates `掌握度/` |
| "ingest this paper" | `ingest-paper` | `main.md`, `si.md` and figures named by figure number, in the paper's folder |
| "generate the full index" | `ingest-lecture` | at the end of term, rewrites `index.md` as a complete course map |
| `/distill-all` | command | builds a formula map for every course that doesn't have one |
| `/audit-tutorials MATH101` | command | audits all of a course's tutorial solutions against its formula map |

## Adding a plugin for your field

The core plugin has no subject knowledge built in; the author has used it unchanged for engineering, economics, computer-science and physics courses. When a field has its own plots, handbooks or report formats, put them in a separate domain plugin — [`chemeng-coursework`](plugins/chemeng-coursework) is the chemical-engineering example. See [`docs/PLUGIN_SPEC.md`](docs/PLUGIN_SPEC.md).

## Notes

- Skill prompts are written in Chinese. They handle slides in any language and write notes in the language you work in.
- The checks make sure numbers are computed right, formulas copied right and every slide covered. Citations can only be checked for being present, not for being true, so the notes are still worth a read-through.
- The example doesn't include the original slides or their extracted text.

## Credits

Grew out of a vault built on [claudesidian](https://github.com/heyitsnoah/claudesidian); PDF extraction by [MinerU](https://github.com/opendatalab/MinerU); the teaching-note structure borrows from [Love Learning Anything](https://github.com/RAIZ-Zzz/love-learning-anything), the review vault and quiz from [tutor-skills](https://github.com/RoundTable02/tutor-skills).

[Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) · [MIT License](LICENSE)
