#!/usr/bin/env python3
"""讲解型 lecture 笔记检查 — ingest-lecture Step 5 自动化

结构检查:
 1. frontmatter `verified:` 已填（不是模板占位）
 2. 每个知识点小节（`### x.y`）都有"用自己的话说"折叠块
 3. 每个部分（`## 第 N 部分`，串起来看 / 复习除外）都有"误区与陷阱"和"暂停"
 4. 每个 `> [!example] 实例` 块以"计算结果"收尾
 5. 正文里引用的 [作者, 年份] 都出现在"参考文献"段
 6. `[[链接]]` 指向已存在的笔记 / 附件 / 本笔记标题（需 --vault）
 7. 没有"我的疑问"段

内容检查:
 8. 先讲问题：每个知识点有"为什么需要它"，且第一句不以公式、列表或"X 是指 / 定义为"开头
 9. 每部分至少 1 条误区，每条误区都有"反例 / 为什么不对 / 正确说法"，反例里有数据
    （页码、实例编号不算）；"暂停"里有预测题
10. 练习 ≥ 8 题
11. slide 覆盖：frontmatter `pages` 里每一页，要么被正文 `p.N` 引用，要么列在 `pages_skipped`

数字检查（对 verify.py）:
12. 真跑一遍 `verified:` 指向的 verify.py，退出码必须是 0（不信 frontmatter 自报）
13. 笔记里每个"实例 x.y"在 verify.py 里都有 `# 实例 x.y` 段，且该段要么用 assert_slide()
    和课件印的答案比对，要么写明"课件未给答案"；verify.py 里也不能有笔记中不存在的实例
14. 每个"计算结果"里至少有一个数和 verify.py 的 assert / assert_slide 里的数一致
    （相对误差 ≤ 1%，单位必须和笔记写的一致）

课件原文检查（对 MinerU full.md，治"笔记和 verify.py 一起抄错公式"）:
15. 带 `\\tag{}` 的公式里每个小数常数都能在课件原文里找到（"补充"块里的外部公式除外）；
    OCR 漏抽的，对照原页 PNG 后写进 frontmatter `constants_manual`

用法:
    python check_note.py <note.md> [--vault <vault 根目录>] [--source <full.md>] [--no-run]

例:
    python check_note.py 01_Projects/CME222_传质/L03_diffusion_coefficient_estimation.md --vault .

`--source` 可省略：默认读 frontmatter `source_md:`（相对笔记所在目录）。

退出码: 0 = 全通过, 1 = 有问题
"""
import argparse
import ast
import re
import subprocess
import sys
from pathlib import Path

LESSON_RE = re.compile(r"^###\s+\d+\.\d+\s")
PART_RE = re.compile(r"^##\s+第\s*\d+\s*部分")
CITE_RE = re.compile(r"\[([^\[\]\d][^\[\]]*?),\s*(\d{4}[a-z]?)\]")
LINK_RE = re.compile(r"(!?)\[\[([^\]|#]*)(#[^\]|]*)?(\|[^\]]*)?\]\]")
EXAMPLE_RE = re.compile(r">\s*\[!example\][-+]?\s*实例")
PAGE_RE = re.compile(r"p\.\s*(\d+)(?:\s*[–\-~]\s*(\d+))?")
# "X 是指 / 定义为"式开头：主语后紧跟定义动词（"这是一个问题"这类不算）
DEF_OPENING_RE = re.compile(r"^(?!这|那|它)[^，,。；;：:]{1,12}?(是指|指的是|定义为|被定义为|称为|叫做)")
# 反例里不算"数据"的数字：页码、实例 / 小节 / 表号
REF_NUM_RE = re.compile(r"p\.\s*\d+(?:\s*[–\-~]\s*\d+)?|实例\s*\d+\.\d+|§\s*\d+(?:\.\d+)?|\b[A-Z]\.\d+|式\s*\d+\.\d+")
SUPERSCRIPT = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")

MIN_EXERCISES = 8
RESULT_RTOL = 0.01


# ---------- 通用 ----------

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def split_frontmatter(text: str) -> tuple[str, str]:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[3:end], text[end + 4:]
    return "", text


def fm_value(fm: str, key: str) -> str | None:
    """取 frontmatter 值；带引号的取引号内，不带引号的去掉行尾 # 注释。"""
    m = re.search(rf"^{key}:\s*(.*)$", fm, re.MULTILINE)
    if not m:
        return None
    v = m.group(1).strip()
    q = re.match(r"""^(["'])(.*?)\1""", v)
    return q.group(2) if q else re.sub(r"\s+#.*$", "", v).strip()


def sections(lines: list[str], start_re: re.Pattern, stop_prefixes: tuple[str, ...]) -> list[tuple[str, list[str]]]:
    """按标题切块：从匹配 start_re 的行开始，到下一个同级或更高级标题为止。"""
    out: list[tuple[str, list[str]]] = []
    cur: tuple[str, list[str]] | None = None
    for line in lines:
        if start_re.match(line):
            if cur:
                out.append(cur)
            cur = (line.strip(), [])
        elif cur and line.startswith(stop_prefixes):
            out.append(cur)
            cur = None
        elif cur:
            cur[1].append(line)
    if cur:
        out.append(cur)
    return out


def callouts(lines: list[str], head_re: re.Pattern) -> list[tuple[str, list[str]]]:
    """收集以 head_re 开头的 `>` 引用块（到第一行不以 > 开头为止）。"""
    out = []
    i = 0
    while i < len(lines):
        if head_re.match(lines[i]):
            j = i + 1
            while j < len(lines) and lines[j].startswith(">"):
                j += 1
            out.append((lines[i].strip("> ").strip(), lines[i + 1:j]))
            i = j
        else:
            i += 1
    return out


def headings(lines: list[str]) -> set[str]:
    return {re.sub(r"^#+\s+", "", l).strip() for l in lines if re.match(r"^#{1,6}\s", l)}


def parse_numbers(text: str) -> list[float]:
    """抽出文本里的数：支持 1.47\\times10^{-5}、1.47×10⁻⁵、1.47\\cdot10^{-5}、1.47e-5、1,104。"""
    t = text.translate(SUPERSCRIPT)
    t = re.sub(r"(?<=\d),(?=\d{3}\b)", "", t)          # 千分位逗号
    t = t.replace("\\,", "").replace("{", "").replace("}", "")
    num = r"(\d+(?:\.\d+)?)"
    sci = re.compile(num + r"\s*(?:\\times|\\cdot|×|·|x)\s*10\s*\^?\s*([-+]?\d+)|"
                     + num + r"[eE]([-+]?\d+)|" + num)
    out = []
    for m in sci.finditer(t):
        if m.group(1):
            out.append(float(m.group(1)) * 10 ** int(m.group(2)))
        elif m.group(3):
            out.append(float(m.group(3)) * 10 ** int(m.group(4)))
        else:
            out.append(float(m.group(5)))
    return out


def close(a: float, b: float, rtol: float) -> bool:
    return abs(a - b) <= rtol * max(abs(a), abs(b)) or (a == 0 and b == 0)


def page_set(spec: str) -> set[int]:
    """'1-32' / '1 (封面), 2 (目录), 5–7' → {1,2,5,6,7}"""
    pages: set[int] = set()
    for part in re.split(r"[,，、;；]", spec or ""):
        m = re.match(r"\s*(\d+)(?:\s*[–\-~]\s*(\d+))?", part)
        if m:
            a = int(m.group(1))
            b = int(m.group(2)) if m.group(2) else a
            pages.update(range(min(a, b), max(a, b) + 1))
    return pages


# ---------- 内容检查 ----------

def check_why_first(lessons, errors):
    for title, body in lessons:
        idx = next((k for k, l in enumerate(body) if l.strip().startswith("**为什么需要它**")), None)
        if idx is None:
            errors.append(f"缺\"为什么需要它\"（知识点必须从问题讲起）: {title}")
            continue
        same_line = body[idx].strip().split("**", 2)[-1].strip().lstrip("：:").strip()
        first = same_line or next((l.strip() for l in body[idx + 1:] if l.strip()), "")
        if not first or first.startswith(("**", "#")):
            errors.append(f"\"为什么需要它\"下面是空的: {title}")
        elif first.startswith(("$$", "\\[", ">", "|")) or re.match(r"^([-*+]|\d+[.)、])\s", first):
            errors.append(f"\"为什么需要它\"以公式 / 列表开头，应先写具体失败场景: {title}")
        elif DEF_OPENING_RE.match(first):
            errors.append(f"\"为什么需要它\"以定义开头（\"{first[:24]}…\"），应先写具体失败场景: {title}")


def check_parts(parts, errors):
    for title, body in parts:
        text = "\n".join(body)
        if "误区与陷阱" not in text:
            errors.append(f"缺\"误区与陷阱\": {title}")
        fails = callouts(body, re.compile(r">\s*\[!failure\]"))
        if "误区与陷阱" in text and not fails:
            errors.append(f"\"误区与陷阱\"下没有 [!failure] 误区: {title}")
        for ft, fb in fails:
            ftext = "\n".join(fb)
            lack = [k for k in ("反例", "为什么不对", "正确说法") if k not in ftext]
            if lack:
                errors.append(f"误区缺{'/'.join(lack)}: {ft[:40]}")
            elif not parse_numbers(REF_NUM_RE.sub("", ftext.split("为什么不对")[0])):
                errors.append(f"误区的反例没有数据（页码 / 实例编号不算）: {ft[:40]}")
        pauses = callouts(body, re.compile(r">\s*\[!question\][-+]?\s*暂停"))
        if not pauses:
            errors.append(f"缺\"暂停\"自测: {title}")
        elif not any("预测" in "\n".join(pb) for _, pb in pauses):
            errors.append(f"\"暂停\"里没有预测题: {title}")


def check_exercises(lines, errors):
    start = next((k for k, l in enumerate(lines) if re.match(r"^###\s+练习", l)), None)
    if start is None:
        errors.append("缺\"### 练习\"段")
        return 0
    n = 0
    for l in lines[start + 1:]:
        if re.match(r"^#{1,3}\s", l):
            break
        if re.match(r"^####\s+练习", l):
            n += 1
    if n < MIN_EXERCISES:
        errors.append(f"练习只有 {n} 题（至少 {MIN_EXERCISES} 题）")
    return n


def check_coverage(fm, lines, errors):
    pages = page_set(fm_value(fm, "pages") or "")
    if not pages:
        errors.append("frontmatter `pages:` 未填，无法检查 slide 覆盖")
        return
    skipped = page_set(fm_value(fm, "pages_skipped") or "")
    end = next((k for k, l in enumerate(lines) if re.match(r">\s*\[!\w+\][-+]?\s*PPT 原文", l)), len(lines))
    cited: set[int] = set()
    for l in lines[:end]:
        if l.startswith("| [[#"):          # 阅读路线表的大段页码不算覆盖
            continue
        for m in PAGE_RE.finditer(l):
            a = int(m.group(1))
            b = int(m.group(2)) if m.group(2) else a
            cited.update(range(min(a, b), max(a, b) + 1))
    missing = sorted(pages - cited - skipped)
    print(f"Slide 覆盖: {len(pages & (cited | skipped))}/{len(pages)}（其中 pages_skipped {len(pages & skipped)} 页）")
    if missing:
        errors.append(f"这些页既没被正文 p.N 引用，也不在 pages_skipped: {missing}")


# ---------- verify.py ----------

def verify_blocks(src: str) -> dict[str, str]:
    """把 verify.py 按 `# 实例 x.y` 注释行切段。"""
    marks = list(re.finditer(r"^[ \t]*#\s*实例\s*(\d+\.\d+)", src, re.MULTILINE))
    blocks: dict[str, str] = {}
    for k, m in enumerate(marks):
        end = marks[k + 1].start() if k + 1 < len(marks) else len(src)
        blocks[m.group(1)] = blocks.get(m.group(1), "") + src[m.start():end]
    return blocks


def asserted_numbers(src: str) -> list[float]:
    """assert 语句里的数字常量，加上 assert_slide(算得值, 课件值, …) 的位置参数。"""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []
    nodes = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Assert):
            nodes.append(n.test)
        elif isinstance(n, ast.Call) and getattr(n.func, "id", "") == "assert_slide":
            nodes.extend(n.args[:2])
    out = []
    for root in nodes:
        for c in ast.walk(root):
            if isinstance(c, ast.Constant) and isinstance(c.value, (int, float)) and not isinstance(c.value, bool):
                out.append(float(c.value))
    return out


def check_verify(note: Path, fm: str, lines: list[str], run: bool, errors):
    examples = callouts(lines, EXAMPLE_RE)
    verified = fm_value(fm, "verified") or ""
    m = re.search(r"(\S.*?\.py)(?=\s|$)", verified)
    if not m:
        if examples:
            errors.append(f"有 {len(examples)} 个实例，但 verified 里没有 verify.py 路径（写的是\"{verified[:30]}\"）")
        return
    vpath = (note.parent / m.group(1)).resolve()
    if not vpath.exists():
        errors.append(f"verified 指向的 {m.group(1)} 不存在")
        return
    src = read(vpath)

    if run:
        try:
            r = subprocess.run([sys.executable, vpath.name], cwd=vpath.parent, capture_output=True,
                               text=True, encoding="utf-8", errors="replace", timeout=120)
            if r.returncode != 0:
                tail = (r.stderr or r.stdout).strip().splitlines()[-3:]
                errors.append(f"verify.py 跑不通（退出码 {r.returncode}）: {' | '.join(tail)}")
            else:
                print("verify.py: 实际运行通过")
        except subprocess.TimeoutExpired:
            errors.append("verify.py 运行超过 120 秒")

    asserted = asserted_numbers(src)
    blocks = verify_blocks(src)
    note_ids: set[str] = set()

    for title, body in examples:
        m_id = re.search(r"实例\s*(\d+\.\d+)", title)
        if m_id is None:
            errors.append(f"实例标题没有 x.y 编号，无法和 verify.py 对账: {title[:40]}")
            continue
        eid = m_id.group(1)
        note_ids.add(eid)
        blk = blocks.get(eid)
        if blk is None:
            errors.append(f"verify.py 里没有\"实例 {eid}\"段（用 `# 实例 {eid}` 注释开头）")
        elif "assert_slide(" not in blk and "课件未给答案" not in blk:
            errors.append(f"verify.py 实例 {eid} 段既没用 assert_slide() 对课件答案，也没写\"课件未给答案\"")
        k = next((i for i, l in enumerate(body) if "计算结果" in l), None)
        if k is None:
            continue
        result = "\n".join(body[k:]).split("计算结果", 1)[-1]
        nums = [x for x in parse_numbers(REF_NUM_RE.sub("", result)) if not (x == int(x) and abs(x) < 10)]
        if not nums:
            errors.append(f"实例 {eid} 的计算结果里没有数字")
        elif not any(close(x, y, RESULT_RTOL) for x in nums for y in asserted):
            errors.append(f"实例 {eid} 的计算结果 {[f'{x:.4g}' for x in nums[:3]]} 在 verify.py 的 assert 里找不到"
                          "（assert 要用笔记写的单位）")

    for eid in sorted(set(blocks) - note_ids):
        errors.append(f"verify.py 有\"实例 {eid}\"段，笔记里却没有这道实例（删了实例？编号不一致？）")


# ---------- 课件原文 ----------

def normalize_source(text: str) -> str:
    """MinerU 公式会把数字拆成 '0 . 0 0 1 8 5 8' / '1. 1 8'：只合并由单个数字或小数点组成的连续记号。"""
    tok = r"(?:\d\.?|\.)"
    return re.sub(rf"(?<![\w.]){tok}(?:[ ]{tok})+\d*(?![\w.])", lambda m: m.group(0).replace(" ", ""), text)


def tagged_equations(lines: list[str], errors) -> list[str]:
    """正文里所有带 \\tag 的 $$…$$ 公式（含引用块里的；"补充"块里的外部公式除外）。"""
    kept = []
    in_supp = False
    for l in lines:
        if re.match(r">\s*\[!info\][-+]?\s*补充", l):
            in_supp = True
            continue
        if in_supp and l.startswith(">"):
            continue
        in_supp = False
        kept.append(re.sub(r"^(?:>\s?)+", "", l))
    text = "\n".join(kept)
    if text.count("$$") % 2:
        errors.append("有没闭合的 $$（公式块数不成对），公式常数核对可能不完整")
    return [b for b in re.findall(r"\$\$(.+?)\$\$", text, re.S) if "\\tag" in b]


def check_constants(note: Path, fm: str, lines: list[str], source_arg: str | None, errors, warns):
    source_md = source_arg or fm_value(fm, "source_md")
    src_ppt = fm_value(fm, "source_ppt") or ""
    if not source_md:
        if re.search(r"\.pdf\b", src_ppt, re.I):
            errors.append("课件是 PDF，但 frontmatter 没有 `source_md:`（MinerU full.md 路径），无法核对公式常数")
        else:
            warns.append("没有课件原文（source_md），跳过公式常数核对")
        return
    if source_md.startswith("无"):
        warns.append(f"source_md: {source_md} —— 跳过公式常数核对")
        return
    spath = Path(source_md) if source_arg else note.parent / source_md
    if not spath.exists():
        errors.append(f"source_md 指向的 {source_md} 不存在")
        return
    raw = read(spath)
    src_nums: set[float] = set()
    for t in (raw, normalize_source(raw)):          # 原文和合并后的都收，避免合并误伤
        src_nums |= {round(x, 12) for x in parse_numbers(t)}
        src_nums |= {round(float(s), 12) for s in re.findall(r"\d+\.\d+", t)}
    manual = {round(x, 12) for x in parse_numbers(REF_NUM_RE.sub("", fm_value(fm, "constants_manual") or ""))}

    consts: dict[float, str] = {}
    for block in tagged_equations(lines, errors):
        block = re.sub(r"\\tag\*?\{[^}]*\}", "", block)
        for m in re.finditer(r"\d+\.\d+", block.replace(" ", "")):
            consts[round(float(m.group(0)), 12)] = m.group(0)
    missing = [s for v, s in consts.items() if v not in src_nums and v not in manual]
    print(f"公式常数: {len(consts)} 个，课件原文中找到 {len(consts) - len(missing)} 个")
    for s in missing:
        errors.append(f"公式常数 {s} 在课件原文里找不到——对照原页确认；OCR 漏抽的写进 frontmatter `constants_manual`")


# ---------- main ----------

def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("note")
    ap.add_argument("--vault", help="vault 根目录；给了才检查 [[链接]] 是否存在")
    ap.add_argument("--source", help="课件 MinerU full.md；不给则读 frontmatter source_md")
    ap.add_argument("--no-run", action="store_true", help="不实际运行 verify.py")
    args = ap.parse_args()

    path = Path(args.note)
    if not path.exists():
        sys.exit(f"ERROR: 文件不存在 {path}")
    fm, body = split_frontmatter(read(path))
    lines = body.splitlines()
    errors: list[str] = []
    warns: list[str] = []
    print(f"=== {path.name} ===\n")

    # 1. verified
    v = fm_value(fm, "verified")
    if not v or "{{" in v:
        errors.append("frontmatter `verified:` 未填（跑完 verify.py 后写结果，或写\"无计算\"）")

    # 2. 每个知识点有"用自己的话说"
    lessons = sections(lines, LESSON_RE, ("## ", "### "))
    print(f"知识点小节: {len(lessons)} 个")
    if not lessons:
        errors.append("没有 `### x.y` 知识点小节（不是讲解型结构）")
    for t, b in lessons:
        if not any("用自己的话说" in l for l in b):
            errors.append(f"缺\"用自己的话说\": {t}")

    # 8. 先讲问题
    check_why_first(lessons, errors)

    # 3 + 9. 每个部分的误区与暂停
    parts = [(t, b) for t, b in sections(lines, PART_RE, ("## ",)) if "串起来看" not in t and "复习" not in t]
    print(f"部分: {len(parts)} 个")
    check_parts(parts, errors)

    # 4. 实例以计算结果收尾
    examples = callouts(lines, EXAMPLE_RE)
    print(f"实例: {len(examples)} 个")
    for t, b in examples:
        if not any("计算结果" in l for l in b):
            errors.append(f"实例没有\"计算结果\": {t}")

    # 10. 练习
    if lessons:
        print(f"练习: {check_exercises(lines, errors)} 题")

    # 11. slide 覆盖
    if lessons:
        check_coverage(fm, lines, errors)

    # 5. 引用都在参考文献里
    ref_idx = next((k for k, l in enumerate(lines) if re.match(r"^#{2,3}\s+参考文献", l)), None)
    main_text = "\n".join(lines[:ref_idx] if ref_idx is not None else lines)
    ref_text = "\n".join(lines[ref_idx:]) if ref_idx is not None else ""
    cites = {f"[{a.strip()}, {y}]" for a, y in CITE_RE.findall(main_text)}
    print(f"引用: {len(cites)} 处")
    for c in sorted(cites):
        if c not in ref_text:
            errors.append(f"引用 {c} 不在\"参考文献\"段")

    # 6. 链接存在
    if args.vault:
        vault = Path(args.vault)
        names = {p.stem for p in vault.rglob("*.md")} | {p.name for p in vault.rglob("*") if p.is_file()}
        own = headings(lines)
        dead = set()
        for embed, target, anchor, _ in LINK_RE.findall(body):
            target = target.strip()
            if not target:  # [[#标题]] 本笔记内跳转
                if anchor and anchor[1:].strip() not in own:
                    dead.add(f"[[{anchor}]]（本笔记无此标题）")
                continue
            if Path(target).name not in names and Path(target).stem not in names:
                dead.add(f"[[{target}]]")
        print(f"空链接: {len(dead)} 个")
        for d in sorted(dead):
            errors.append(f"空链接 {d}")

    # 7. 不写"我的疑问"
    if any(re.match(r"^##\s+我的疑问", l) for l in lines):
        errors.append("有\"我的疑问\"段（新模板已取消，改用\"暂停\"预测题）")

    # 12–14. verify.py
    if lessons:
        check_verify(path, fm, lines, not args.no_run, errors)

    # 15. 公式常数对课件原文
    if lessons:
        check_constants(path, fm, lines, args.source, errors, warns)

    print()
    for w in warns:
        print(f"  [提示] {w}")
    if errors:
        print(f"=== 总结: {len(errors)} 处问题 ===")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("=== 总结: 全部通过 ✓ ===")


if __name__ == "__main__":
    main()
