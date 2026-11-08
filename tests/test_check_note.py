"""Mutation tests for plugins/claudesidian-notes/shared/scripts/check_note.py.

Each test starts from the known-good L03 example note (copied by the ``ws``
fixture), applies ONE mutation and asserts that check_note.py reacts the way
its docstring promises (exit code + a key substring of the error message).
"""
from __future__ import annotations

import re

import pytest

from conftest import Workspace

# Exact strings from the L03 note / verify.py that the mutations target.
NOTE_RESULT_41 = r"$D_{NH_3\text{-}air} = 0.344$ cm²/s $= 3.44\times10^{-5}$ m²/s"
NOTE_WHY_11 = "**为什么需要它**\n上一讲例 4 里"
NOTE_TRAP_11_COUNTER = ("> **反例：** 表 J.1 中 CO₂–空气 273 K 一栏是 0.136 cm²·atm/s。"
                        "如果压力是 2 atm，$D_{AB}$ 是 0.068 cm²/s，不是 0.136（p.5）。")
VERIFY_ASSERT_D3 = "assert round(D3, 3) == 0.344"
VERIFY_MARK_32 = "# 实例 3.2（p.24）：苯–空气，303 K，1 atm，Fuller。课件未给答案（扩散体积取自课件 p.23）"
VERIFIED_LINE = 'verified: "_attachments/verify.py 全部通过"'


# ---------------------------------------------------------------------------
# baseline
# ---------------------------------------------------------------------------

def test_baseline_passes(ws: Workspace):
    r = ws.run()
    assert r.passed, r.summary()
    assert "=== 总结: 全部通过" in r.stdout
    assert "verify.py: 实际运行通过" in r.stdout
    assert "实例: 4 个" in r.stdout
    assert "练习: 10 题" in r.stdout
    assert "Slide 覆盖: 32/32" in r.stdout
    # source_md starts with "无" -> constants check skipped with a hint, not an error
    assert "[提示] source_md: 无" in r.stdout
    assert r.errors == []


def test_baseline_with_source_excerpt_finds_all_constants(ws: Workspace, source_excerpt):
    r = ws.run("--source", str(source_excerpt))
    assert r.passed, r.summary()
    assert "公式常数: 7 个，课件原文中找到 7 个" in r.stdout


def test_no_run_skips_executing_verify(ws: Workspace):
    r = ws.run("--no-run")
    assert r.passed, r.summary()
    assert "verify.py: 实际运行通过" not in r.stdout


@pytest.mark.parametrize("variant", ["bom", "crlf"])
def test_encoding_variants_still_pass(ws: Workspace, variant):
    if variant == "bom":
        ws.edit_note(lambda t: "﻿" + t)
    else:
        ws.edit_note(lambda t: t.replace("\n", "\r\n"))
    r = ws.run()
    assert r.passed, r.summary()


# ---------------------------------------------------------------------------
# 15. constants vs. slide source (--source)
# ---------------------------------------------------------------------------

def test_wrong_constant_in_both_note_and_verify_is_caught_by_source(ws: Workspace, source_excerpt):
    """0.196 -> 0.19 in the tagged equation AND in verify.py: verify.py still
    passes (delta_AB = 0 so the term vanishes), only the source check can see it."""
    ws.mutate_note(r"\frac{0.196\,\delta_{AB}^2}{T^*}", r"\frac{0.19\,\delta_{AB}^2}{T^*}")
    ws.mutate_verify("0.196 * delta_AB**2", "0.19 * delta_AB**2")
    r = ws.run("--source", str(source_excerpt))
    assert not r.passed
    assert "verify.py: 实际运行通过" in r.stdout        # verify.py itself is green
    assert r.has_error("公式常数 0.19 在课件原文里找不到"), r.summary()


def test_wrong_constant_in_note_only_is_caught_by_source(ws: Workspace, source_excerpt):
    ws.mutate_note(r"\frac{1.585\,V_b}", r"\frac{1.858\,V_b}")
    r = ws.run("--source", str(source_excerpt))
    assert not r.passed
    assert r.has_error("公式常数 1.858 在课件原文里找不到"), r.summary()


def test_constant_missing_from_source_is_reported(ws: Workspace, source_without_0196):
    r = ws.run("--source", str(source_without_0196))
    assert not r.passed
    assert r.has_error("公式常数 0.196 在课件原文里找不到"), r.summary()
    assert "公式常数: 7 个，课件原文中找到 6 个" in r.stdout


def test_constants_manual_template_comment_does_not_whitelist(ws: Workspace, source_without_0196):
    """The template's own inline comment mentions "0.196 (p.26)" as an example;
    it must not count as a manually confirmed constant."""
    ws.mutate_note('related: ["[[L02_diffusive_mass_transfer]]"]',
                   'constants_manual: ""  # 只填 OCR 漏抽、已对照原页 PNG 确认的公式常数，如 "0.196 (p.26)"\n'
                   'related: ["[[L02_diffusive_mass_transfer]]"]')
    r = ws.run("--source", str(source_without_0196))
    assert not r.passed
    assert r.has_error("公式常数 0.196 在课件原文里找不到"), r.summary()


def test_constants_manual_real_value_does_whitelist(ws: Workspace, source_without_0196):
    ws.mutate_note('related: ["[[L02_diffusive_mass_transfer]]"]',
                   'constants_manual: "0.196 (p.26)"\nrelated: ["[[L02_diffusive_mass_transfer]]"]')
    r = ws.run("--source", str(source_without_0196))
    assert r.passed, r.summary()


def test_multiline_tag_equation_still_checked(ws: Workspace, source_excerpt):
    ws.mutate_note(r"$$D_{AA^*} = \frac{1}{3}\lambda u \tag{2.1}$$",
                   "$$\nD_{AA^*} = \\frac{1}{3}\\lambda u\n\\tag{2.1}\n$$")
    r = ws.run("--source", str(source_excerpt))
    assert r.passed, r.summary()
    assert "公式常数: 7 个，课件原文中找到 7 个" in r.stdout


def test_missing_source_file_is_an_error(ws: Workspace):
    r = ws.run("--source", str(ws.root / "does_not_exist.md"))
    assert not r.passed
    assert r.has_error("不存在"), r.summary()


# ---------------------------------------------------------------------------
# 12-14. verify.py
# ---------------------------------------------------------------------------

def test_result_number_changed_without_touching_verify(ws: Workspace):
    ws.mutate_note(NOTE_RESULT_41, NOTE_RESULT_41.replace("0.344", "0.433").replace("3.44", "4.33"))
    r = ws.run()
    assert not r.passed
    assert r.has_error("实例 4.1 的计算结果"), r.summary()
    assert r.has_error("在 verify.py 的 assert 里找不到"), r.summary()


def test_verify_assert_broken_is_caught_by_running_it(ws: Workspace):
    ws.mutate_verify(VERIFY_ASSERT_D3, "assert round(D3, 3) == 0.345")
    r = ws.run()
    assert not r.passed
    assert r.has_error("verify.py 跑不通（退出码 1）"), r.summary()
    assert "verify.py: 实际运行通过" not in r.stdout


def test_verify_marker_removed_from_block(ws: Workspace):
    ws.mutate_verify(VERIFY_MARK_32, VERIFY_MARK_32.replace("课件未给答案", ""))
    r = ws.run()
    assert not r.passed
    assert r.has_error("verify.py 实例 3.2 段既没用 assert_slide() 对课件答案，也没写\"课件未给答案\""), r.summary()


def test_example_deleted_from_note_leaves_orphan_verify_block(ws: Workspace):
    ws.edit_note(lambda t: re.sub(r"> \[!example\] 实例 4\.2：.*?\n\n", "", t, count=1, flags=re.S))
    r = ws.run()
    assert "实例: 3 个" in r.stdout
    assert not r.passed
    assert r.has_error("verify.py 有\"实例 4.2\"段，笔记里却没有这道实例"), r.summary()


def test_verify_block_missing_for_example(ws: Workspace):
    ws.mutate_verify("# 实例 3.2（p.24）", "# 例题 3.2（p.24）")
    r = ws.run()
    assert not r.passed
    assert r.has_error("verify.py 里没有\"实例 3.2\"段"), r.summary()


def test_collapsed_example_callout_is_counted(ws: Workspace):
    ws.mutate_note("> [!example] 实例 4.1：", "> [!example]- 实例 4.1：")
    r = ws.run()
    assert r.passed, r.summary()
    assert "实例: 4 个" in r.stdout


def test_collapsed_example_callout_is_still_checked(ws: Workspace):
    ws.mutate_note("> [!example] 实例 4.1：", "> [!example]- 实例 4.1：")
    ws.mutate_note(NOTE_RESULT_41, NOTE_RESULT_41.replace("0.344", "0.433").replace("3.44", "4.33"))
    r = ws.run()
    assert not r.passed
    assert r.has_error("实例 4.1 的计算结果"), r.summary()


def test_example_without_result_line(ws: Workspace):
    ws.mutate_note("> **计算结果：** $D_{NH_3", "> **结论：** $D_{NH_3")
    r = ws.run()
    assert not r.passed
    assert r.has_error("实例没有\"计算结果\": [!example] 实例 4.1"), r.summary()


def test_verify_path_with_spaces(ws: Workspace):
    ws.move_verify("_attachments/CME 222 Lecture 3/verify.py")
    r = ws.run()
    assert r.passed, r.summary()
    assert "verify.py: 实际运行通过" in r.stdout


def test_verify_printing_non_gbk_characters(ws: Workspace):
    """Child stdout is a pipe; on Windows that defaults to the ANSI code page."""
    ws.mutate_verify('print("verify.py: 全部通过")', 'print("verify.py: 全部通过 (Ω_D = 1.110, σ = 3.272 Å)")')
    r = ws.run()
    assert r.passed, r.summary()


def test_verified_without_py_path_is_flagged(ws: Workspace):
    ws.mutate_note(VERIFIED_LINE, 'verified: "全部通过"')
    r = ws.run()
    assert not r.passed
    assert r.has_error("有 4 个实例，但 verified 里没有 verify.py 路径"), r.summary()


def test_verified_pointing_at_missing_file(ws: Workspace):
    ws.mutate_note(VERIFIED_LINE, 'verified: "_attachments/nope.py 全部通过"')
    r = ws.run()
    assert not r.passed
    assert r.has_error("verified 指向的 _attachments/nope.py 不存在"), r.summary()


def test_verified_template_placeholder(ws: Workspace):
    ws.mutate_note(VERIFIED_LINE, 'verified: "{{VERIFY_RESULT}}"')
    r = ws.run()
    assert not r.passed
    assert r.has_error("frontmatter `verified:` 未填"), r.summary()


# ---------------------------------------------------------------------------
# 8. "为什么需要它" must open with a concrete problem
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("opening, expected", [
    pytest.param("扩散系数是指单位浓度梯度下的摩尔通量。", "以定义开头", id="definition"),
    pytest.param("$$J_A = -D_{AB}\\frac{dc_A}{dz}$$\n", "以公式 / 列表开头", id="display-formula"),
    pytest.param("- 气体 $D$ 大约 $10^{-5}$ m²/s\n", "以公式 / 列表开头", id="bullet-list"),
])
def test_why_first_bad_openings(ws: Workspace, opening, expected):
    ws.mutate_note(NOTE_WHY_11, "**为什么需要它**\n" + opening + "上一讲例 4 里")
    r = ws.run()
    assert not r.passed
    assert r.has_error(expected), r.summary()
    assert r.has_error("### 1.1"), r.summary()


@pytest.mark.parametrize("opening", [
    pytest.param("这是一个很实际的问题：", id="zhe-shi-yi-ge"),
    pytest.param("$D_{AB}$ 查不到实验值时就卡住了。", id="inline-symbol"),
    pytest.param("1.5 atm 的反应器里，查表值直接代进去就错了一半。", id="leading-decimal"),
])
def test_why_first_legit_openings_pass(ws: Workspace, opening):
    ws.mutate_note(NOTE_WHY_11, "**为什么需要它**\n" + opening + "上一讲例 4 里")
    r = ws.run()
    assert r.passed, r.summary()


def test_why_first_missing(ws: Workspace):
    ws.mutate_note("**为什么需要它**\n查表 J.1 时", "**背景**\n查表 J.1 时")
    r = ws.run()
    assert not r.passed
    assert r.has_error("缺\"为什么需要它\""), r.summary()
    assert r.has_error("### 1.2"), r.summary()


# ---------------------------------------------------------------------------
# 9. misconceptions and pauses
# ---------------------------------------------------------------------------

def test_misconception_counterexample_with_only_page_refs(ws: Workspace):
    ws.mutate_note(NOTE_TRAP_11_COUNTER, "> **反例：** 表 J.1 中 CO₂–空气那一栏其实是 $D_{AB}P$，不是 $D_{AB}$（p.5）。")
    r = ws.run()
    assert not r.passed
    assert r.has_error("误区的反例没有数据（页码 / 实例编号不算）: [!failure] 陷阱 1.1"), r.summary()


def test_misconception_missing_correct_statement(ws: Workspace):
    ws.mutate_note("> **正确说法：** 查表值要除以实际压力（atm）。*EN: Divide the tabulated D_AB·P by the actual pressure.*\n", "")
    r = ws.run()
    assert not r.passed
    assert r.has_error("误区缺正确说法: [!failure] 陷阱 1.1"), r.summary()


def test_pause_without_prediction(ws: Workspace):
    ws.mutate_note("> > [!question]- 预测：一个三种气体的混合物里", "> > [!question]- 思考：一个三种气体的混合物里")
    r = ws.run()
    assert not r.passed
    assert r.has_error("\"暂停\"里没有预测题: ## 第 1 部分"), r.summary()


def test_pause_removed(ws: Workspace):
    ws.edit_note(lambda t: re.sub(r"> \[!question\]- 暂停：为什么气体的扩散系数随温度升高、随压力降低？.*?(?=\n---)",
                                  "", t, count=1, flags=re.S))
    r = ws.run()
    assert not r.passed
    assert r.has_error("缺\"暂停\"自测: ## 第 2 部分"), r.summary()


def test_part_without_misconceptions_section(ws: Workspace):
    ws.edit_note(lambda t: re.sub(r"### 误区与陷阱\n\n> \[!failure\] 陷阱 3\.1.*?(?=> \[!question\]- 暂停：什么时候用)",
                                  "", t, count=1, flags=re.S))
    r = ws.run()
    assert not r.passed
    assert r.has_error("缺\"误区与陷阱\": ## 第 3 部分"), r.summary()


# ---------------------------------------------------------------------------
# 10-11. exercises and slide coverage
# ---------------------------------------------------------------------------

def test_exercises_reduced_to_six(ws: Workspace):
    def cut(t: str) -> str:
        a, b = t.index("#### 练习 7 ·"), t.index("### 术语中英对照")
        return t[:a] + t[b:]
    ws.edit_note(cut)
    r = ws.run()
    assert "练习: 6 题" in r.stdout
    assert not r.passed
    assert r.has_error("练习只有 6 题（至少 8 题）"), r.summary()


def test_uncovered_slide_when_citation_removed(ws: Workspace):
    ws.mutate_note("，p.30–32。）", "。）")
    r = ws.run()
    assert "Slide 覆盖: 29/32" in r.stdout
    assert not r.passed
    assert r.has_error("这些页既没被正文 p.N 引用，也不在 pages_skipped: [30, 31, 32]"), r.summary()


def test_uncovered_slide_can_be_declared_skipped(ws: Workspace):
    ws.mutate_note("，p.30–32。）", "。）")
    ws.mutate_note('pages_skipped: "1 (封面), 2 (目录), 3 (章节页), 10 (章节页)"',
                   'pages_skipped: "1 (封面), 2 (目录), 3 (章节页), 10 (章节页), 30–32 (总结页)"')
    r = ws.run()
    assert r.passed, r.summary()
    assert "pages_skipped 7 页" in r.stdout


def test_reading_route_table_does_not_count_as_coverage(ws: Workspace):
    """The route table cites p.25–29 in bulk and the PPT 原文 appendix lists
    "Slide 27"; neither may count as coverage once the body stops citing p.27."""
    # heading + the [[#…|§4.1]] wikilink that repeats the heading text
    ws.mutate_note("Brokaw equation）（p.25–27）", "Brokaw equation）（p.25–26）", count=-1)
    ws.mutate_note("吸收塔要用水吸收废气里的氨（p.27）。", "吸收塔要用水吸收废气里的氨。")
    ws.mutate_note("> [!example] 实例 4.1：373 K、101325 Pa 下氨在空气中的扩散系数（Brokaw）（p.27）",
                   "> [!example] 实例 4.1：373 K、101325 Pa 下氨在空气中的扩散系数（Brokaw）")
    r = ws.run()
    assert "Slide 覆盖: 31/32" in r.stdout
    assert not r.passed
    assert r.has_error("也不在 pages_skipped: [27]"), r.summary()


# ---------------------------------------------------------------------------
# 5-7. citations, links, forbidden sections
# ---------------------------------------------------------------------------

def test_citation_missing_from_references(ws: Workspace):
    ws.edit_note(lambda t: re.sub(r"^- \[Pearce et al\., 2020\].*$", "", t, count=1, flags=re.M))
    r = ws.run()
    assert not r.passed
    assert r.has_error("引用 [Pearce et al., 2020] 不在\"参考文献\"段"), r.summary()


def test_dead_wikilink_with_vault(ws: Workspace):
    r = ws.run("--vault", str(ws.root))      # tmp vault has no L02 note
    assert not r.passed
    assert r.has_error("空链接 [[L02_diffusive_mass_transfer]]"), r.summary()


def test_wikilinks_resolve_with_vault(ws: Workspace):
    (ws.root / "L02_diffusive_mass_transfer.md").write_text("# L02\n", encoding="utf-8")
    r = ws.run("--vault", str(ws.root))
    assert r.passed, r.summary()
    assert "空链接: 0 个" in r.stdout


def test_dead_heading_anchor_with_vault(ws: Workspace):
    (ws.root / "L02_diffusive_mass_transfer.md").write_text("# L02\n", encoding="utf-8")
    ws.mutate_note("[[#第 1 部分 · 扩散系数是什么]]", "[[#第 1 部分 · 扩散系数是啥]]")
    r = ws.run("--vault", str(ws.root))
    assert not r.passed
    assert r.has_error("本笔记无此标题"), r.summary()


def test_my_questions_section_is_rejected(ws: Workspace):
    ws.mutate_note("## 个人补充", "## 我的疑问\n\n- 为什么？\n\n## 个人补充")
    r = ws.run()
    assert not r.passed
    assert r.has_error("有\"我的疑问\"段"), r.summary()


def test_missing_self_explanation_block(ws: Workspace):
    ws.mutate_note("> [!question]- 用自己的话说：Fuller 关联式", "> [!question]- 复述：Fuller 关联式")
    r = ws.run()
    assert not r.passed
    assert r.has_error("缺\"用自己的话说\": ### 3.2"), r.summary()


def test_nonexistent_note_path(ws: Workspace):
    ws.note = ws.root / "missing.md"
    r = ws.run()
    assert not r.passed
    # check_note.py reconfigures stdout to UTF-8 but not stderr, so under a
    # non-UTF-8 locale the Chinese part of this message may be mojibake;
    # only assert on the ASCII parts.
    assert r.stderr.startswith("ERROR:")
    assert "missing.md" in r.stderr
    assert r.stdout == ""
