"""Every Markdown file in examples/ must render its math the same on GitHub as in Obsidian.

Uses check_note.py's own GitHub-compatibility check, applied to all example files
(lecture note, index, review vault), not just the lecture note.
"""
import importlib.util
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
CHECK_NOTE = REPO / "plugins" / "claudesidian-notes" / "shared" / "scripts" / "check_note.py"
EXAMPLE_FILES = sorted((REPO / "examples").rglob("*.md"))

spec = importlib.util.spec_from_file_location("check_note", CHECK_NOTE)
check_note = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_note)


def test_examples_exist():
    assert EXAMPLE_FILES, "no Markdown files found under examples/"


@pytest.mark.parametrize("path", EXAMPLE_FILES, ids=lambda p: str(p.relative_to(REPO / "examples")))
def test_example_math_renders_on_github(path: Path):
    warns: list[str] = []
    check_note.check_github_math(path.read_text(encoding="utf-8-sig").splitlines(), warns)
    assert not warns, f"{path.name}: {warns}"
