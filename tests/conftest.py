"""Shared fixtures for the check_note.py test-suite.

Every test gets a fresh copy of the known-good L03 example note (plus its
``_attachments/verify.py``) inside ``tmp_path``, applies exactly one mutation,
and runs ``check_note.py`` as a subprocess, the same way a user or CI would.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
CHECK_NOTE = REPO / "plugins" / "claudesidian-notes" / "shared" / "scripts" / "check_note.py"
EXAMPLE_DIR = REPO / "examples" / "CME222-mass-transfer" / "vault" / "CME222_传质"
EXAMPLE_NOTE = EXAMPLE_DIR / "L03_diffusion_coefficient_estimation.md"
EXAMPLE_VERIFY = EXAMPLE_DIR / "_attachments" / "verify.py"
SOURCE_EXCERPT = Path(__file__).resolve().parent / "fixtures" / "source_excerpt.md"


@dataclass
class CheckResult:
    returncode: int
    stdout: str
    stderr: str

    @property
    def output(self) -> str:
        return self.stdout + self.stderr

    @property
    def errors(self) -> list[str]:
        """The ``  - <msg>`` problem lines check_note.py prints before exiting 1."""
        return [l.strip()[2:] for l in self.stdout.splitlines() if l.startswith("  - ")]

    @property
    def passed(self) -> bool:
        return self.returncode == 0

    def has_error(self, needle: str) -> bool:
        return any(needle in e for e in self.errors)

    def summary(self) -> str:  # used in assertion messages
        return f"exit={self.returncode}\n" + "\n".join(f"  - {e}" for e in self.errors)


@dataclass
class Workspace:
    """A throw-away copy of the L03 note + verify.py with mutation helpers."""

    root: Path
    note: Path
    verify: Path
    extra_args: list[str] = field(default_factory=list)

    # -- mutation helpers -------------------------------------------------
    # newline="" everywhere: keep bytes exactly as written (Windows text mode
    # would otherwise turn an injected "\r\n" into "\r\r\n").
    @staticmethod
    def _read(path: Path) -> str:
        with path.open(encoding="utf-8", newline="") as f:
            return f.read()

    @staticmethod
    def _write(path: Path, text: str) -> None:
        with path.open("w", encoding="utf-8", newline="") as f:
            f.write(text)

    def _replace(self, path: Path, old: str, new: str, count: int = 1) -> None:
        text = self._read(path)
        if old not in text:
            raise AssertionError(f"mutation target not found in {path.name}: {old[:80]!r}")
        self._write(path, text.replace(old, new, count))

    def mutate_note(self, old: str, new: str, count: int = 1) -> None:
        self._replace(self.note, old, new, count)

    def mutate_verify(self, old: str, new: str, count: int = 1) -> None:
        self._replace(self.verify, old, new, count)

    def edit_note(self, fn) -> None:
        """Apply an arbitrary ``str -> str`` transform to the note."""
        self._write(self.note, fn(self._read(self.note)))

    def move_verify(self, rel: str) -> None:
        """Move verify.py to ``<note dir>/<rel>`` and point ``verified:`` at it."""
        dst = self.note.parent / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(self.verify), str(dst))
        self.verify = dst
        self.mutate_note('verified: "_attachments/verify.py 全部通过"', f'verified: "{rel} 全部通过"')

    # -- running ----------------------------------------------------------
    def run(self, *args: str, timeout: int = 180) -> CheckResult:
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
        proc = subprocess.run(
            [sys.executable, "-I", str(CHECK_NOTE), str(self.note), *self.extra_args, *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            env=env, timeout=timeout, cwd=str(self.root),
        )
        return CheckResult(proc.returncode, proc.stdout, proc.stderr)


@pytest.fixture
def ws(tmp_path: Path) -> Workspace:
    """Fresh copy of the L03 example (note + _attachments/verify.py) in tmp_path."""
    note = tmp_path / EXAMPLE_NOTE.name
    verify = tmp_path / "_attachments" / "verify.py"
    verify.parent.mkdir()
    # Copy with LF endings regardless of how git checked the files out
    # (core.autocrlf on Windows gives CRLF), so mutation targets written with
    # "\n" match and the CRLF test can inject real CRLFs.
    for src, dst in ((EXAMPLE_NOTE, note), (EXAMPLE_VERIFY, verify)):
        Workspace._write(dst, src.read_text(encoding="utf-8"))
    return Workspace(root=tmp_path, note=note, verify=verify)


@pytest.fixture
def source_excerpt() -> Path:
    assert SOURCE_EXCERPT.exists(), SOURCE_EXCERPT
    return SOURCE_EXCERPT


@pytest.fixture
def source_without_0196(tmp_path: Path, source_excerpt: Path) -> Path:
    """The synthetic excerpt with the Brokaw constant 0.196 knocked out."""
    text = source_excerpt.read_text(encoding="utf-8")
    assert "0 . 1 9 6" in text
    dst = tmp_path / "source_no_0196.md"
    dst.write_text(text.replace("0 . 1 9 6", "0 . X"), encoding="utf-8")
    return dst
