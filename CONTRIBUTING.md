# Contributing

Thanks for helping. This project is small and opinionated: every change should keep notes **verifiable**. Chinese or English are both fine in issues and PRs.

## Ways to help

- **Report a bad note.** Open an issue with the lecture topic, the part of the note that is wrong, and what `check_note.py` printed. Wrong-but-passing notes are the most valuable reports: they show a gap in the checks.
- **Add a domain plugin** (law, medicine, music, …). Follow [`docs/PLUGIN_SPEC.md`](docs/PLUGIN_SPEC.md) and copy the layout of `plugins/chemeng-coursework/`.
- **Translate prompts.** Skill prompts are written in Chinese; bilingual `description` fields and English reference files are welcome.

## Development setup

```bash
git clone https://github.com/iZHENGjy/claudesidian-learning-os
cd claudesidian-learning-os
pip install pytest
pytest -q
```

To try a plugin from your working copy, add the local folder as a marketplace in Claude Code:

```text
/plugin marketplace add /path/to/claudesidian-learning-os
/plugin install claudesidian-notes@claudesidian-learning-os
```

## Rules for changes

**Skills**
- Keep `SKILL.md` an entry point under ~250 lines; put detail in `references/` and templates in `assets/`.
- The `description` must say when to trigger **and** when not to.
- Framework plugins contain no domain knowledge; domain words appear only as examples.
- When a real run goes wrong, record it in that skill's `references/lessons.md` (failure mode → trigger → fix).

**Checks**
- A new rule in a skill should come with a check in `check_note.py` when it can be checked mechanically, plus a test in `tests/` that shows a broken note being caught.
- Prefer checks that compare against something the model did not write (slide text, the slide's printed answer) over checks of the note against itself.
- Write Python files with an editor or file-writing tool, not shell heredocs: heredocs can drop backslashes and corrupt non-ASCII text.

**Versions**
- Bump the plugin's `plugin.json` version for user-visible changes, bump the marketplace version in `.claude-plugin/marketplace.json` for each release, and add an entry to [`CHANGELOG.md`](CHANGELOG.md).

## Pull requests

1. Branch from `main`.
2. Make sure CI passes locally: `pytest -q`, plus the example `verify.py` scripts if you touched them.
3. Fill in the PR template: what changed, why, and how you verified it on a real note.

Do not commit slides, lecture PDFs, `.env` files or personal vault content. Example courses must have the lecturer's materials replaced with placeholders.
