"""<CODE> L## — 所有实例数字验算（ingest-lecture Step 4.5）

约定（check_note.py 会检查）：
- 每道实例一段，以 `# 实例 x.y（p.N）：…` 注释开头，编号和笔记里的 `> [!example] 实例 x.y` 一致
- 课件印了答案 → 该段用 assert_slide() 和课件答案比对
- 课件没印答案 → 该段注释写明"课件未给答案"（先翻原页确认，不许默认写）
- 笔记"计算结果"里的数，必须出现在某条 assert 里
- 公式常数旁注释课件页码；课件没给的数据注释来源或"待核实"
- 用文件写入工具写本文件，不要用 shell heredoc（会吞反斜杠）
"""
import math
from fractions import Fraction


def assert_slide(calc, printed, page, rtol=0.02):
    """课件印了答案时用：脚本算的值必须和课件答案一致（课件常只给 3 位有效数字，默认容差 2%）"""
    assert abs(calc - printed) <= rtol * abs(printed), f"{page}: 算得 {calc:.4g}，课件印的是 {printed}"


# 公式（系数逐个对照课件原页）
def example_formula(x, y):
    """课件 p.N：<公式名>，单位：…"""
    return 0.0 * x * y


# 实例 1.1（p.N）：<题目一句话>。课件印的答案：<值>
r11 = example_formula(1.0, 2.0)
assert round(r11, 4) == 0.0
assert_slide(r11 + 1.0, 1.0, "p.N")

# 实例 1.2（p.N）：<题目一句话>。课件未给答案
r12 = Fraction(1, 3)
assert r12 == Fraction(1, 3)

print("verify.py: 全部通过")
