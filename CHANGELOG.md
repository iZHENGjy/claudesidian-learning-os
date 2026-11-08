# Changelog

All notable changes to this project. The repository version is the marketplace version in `.claude-plugin/marketplace.json`; each plugin also carries its own version in its `plugin.json`.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/).

## [0.4.0] — 2026-11-08

`claudesidian-notes` 0.3.0

### Added
- `check_note.py` now checks **content and numbers**, not just layout:
  - teaching: each section opens with a concrete problem (not a definition, formula or list); every misconception has a counterexample with data, the reason, and the correct statement; each part has a prediction question; at least 8 exercises
  - coverage: every page in frontmatter `pages` is cited by the body or listed in `pages_skipped`
  - numbers: actually **runs** `verify.py`; reconciles note examples with `# 实例 x.y` blocks in both directions; each block either checks the slide's printed answer with `assert_slide()` or states `课件未给答案`; every 计算结果 value must appear in an assert (same unit, 1% tolerance)
  - source: every decimal constant in a `\tag`-numbered formula must appear in the MinerU slide text (`source_md`), catching coefficients copied wrong in both the note and its verify script
- `skills/ingest-lecture/assets/verify-template.py` with the `assert_slide()` helper and block conventions.
- Note frontmatter fields `source_md` and `constants_manual`.
- pytest suite for `check_note.py` and a GitHub Actions workflow (JSON/plugin-manifest validation, example verify scripts, checker run, tests).
- `CHANGELOG.md`, `CONTRIBUTING.md`, issue and pull-request templates, `README.zh-CN.md`, and a README for `chemeng-coursework`.
- English hero and before/after images (`docs/assets/hero-en.svg`, `compare-en.svg`) for the English README.

### Changed
- `ingest-lecture` rules separate **teaching explanations** (allowed without a source) from **factual claims** (must be cited or marked 待核实).
- The run report lists every skipped page and every manually confirmed constant, so attempts to get around a check stay visible.
- README rewritten around the four verification gates; Chinese moved to `README.zh-CN.md`.
- Example L03: verify blocks numbered like the note; summary slides p.30–32 cited.
- `paper-review-toolkit` README matches the files actually shipped.

### Fixed
- Example L02: carbon mass flux was 1000× too large (2.4×10⁻⁶ → 2.4×10⁻⁹ kg/(m²·s); molar mass must be 0.012 kg/mol).
- Before/after count of unanswered "I wonder…" questions corrected to 6 (README, example README, demo site).
- `plugin.json` files use the object form of `author` and `./` paths required by current Claude Code validation.

## [0.3.0] — 2026-11-04

`claudesidian-notes` 0.2.0

### Added
- `ingest-lecture` produces **teaching notes**: problem first, worked examples verified by a per-lecture `verify.py`, own-words self-checks, misconceptions and prediction questions, cited supplements.
- `check_note.py` structure checker.
- `build-review-vault` (cheat sheet, traps, question bank with folded answers) and `quiz` (zero-hint rounds with per-concept mastery tracking).
- Real-course example `examples/CME222-mass-transfer` with before/after comparison.
- GitHub Pages showcase site.

## [0.2.0] — 2026-07-09

`claudesidian-notes` 0.1.0 · `paper-review-toolkit` 0.1.0 · `chemeng-coursework` 0.1.0

### Added
- Initial public release: course and paper ingest pipeline (`ingest-lecture`, `ingest-tutorial`, `distill-principles`, `ingest-paper`), formula audits, MinerU extraction scripts, the literature-review toolkit, and the chemical-engineering domain plugin as a reference implementation.

[0.4.0]: https://github.com/iZHENGjy/claudesidian-learning-os/compare/0e2698e...HEAD
[0.3.0]: https://github.com/iZHENGjy/claudesidian-learning-os/compare/b6d73f0...0e2698e
[0.2.0]: https://github.com/iZHENGjy/claudesidian-learning-os/commit/b6d73f0
