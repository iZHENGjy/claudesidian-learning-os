#!/usr/bin/env python3
"""讲解型 lecture 笔记结构检查 — ingest-lecture Step 5 自动化

检查:
1. frontmatter `verified:` 已填（不是模板占位）
2. 每个知识点小节（`### x.y`）都有"用自己的话说"折叠块
3. 每个部分（`## 第 N 部分`，串起来看 / 复习除外）都有"误区与陷阱"和"暂停"
4. 每个 `> [!example] 实例` 块以"计算结果"收尾
5. 正文里引用的 [作者, 年份] 都出现在"参考文献"段
6. `[[链接]]` 指向已存在的笔记 / 附件 / 本笔记标题（需 --vault）
7. 没有"我的疑问"段

用法:
    python check_note.py <note.md> [--vault <vault 根目录>]

例:
    python check_note.py 01_Projects/CME222_传质/L02_diffusive_mass_transfer.md --vault .

退出码: 0 = 全通过, 1 = 有问题
"""
import argparse
import re
import sys
from pathlib import Path

LESSON_RE = re.compile(r"^###\s+\d+\.\d+\s")
PART_RE = re.compile(r"^##\s+第\s*\d+\s*部分")
CITE_RE = re.compile(r"\[([^\[\]]+?),\s*(\d{4}[a-z]?)\]")
LINK_RE = re.compile(r"(!?)\[\[([^\]|#]*)(#[^\]|]*)?(\|[^\]]*)?\]\]")


def split_frontmatter(text: str) -> tuple[str, str]:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[3:end], text[end + 4:]
    return "", text


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


def headings(lines: list[str]) -> set[str]:
    return {re.sub(r"^#+\s+", "", l).strip() for l in lines if re.match(r"^#{1,6}\s", l)}


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("note")
    ap.add_argument("--vault", help="vault 根目录；给了才检查 [[链接]] 是否存在")
    args = ap.parse_args()

    path = Path(args.note)
    if not path.exists():
        sys.exit(f"ERROR: 文件不存在 {path}")
    fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
    lines = body.splitlines()
    errors: list[str] = []
    print(f"=== {path.name} ===\n")

    # 1. verified
    m = re.search(r"^verified:\s*(.*)$", fm, re.MULTILINE)
    if not m or not m.group(1).strip().strip('"') or "{{" in m.group(1):
        errors.append("frontmatter `verified:` 未填（跑完 verify.py 后写结果，或写\"无计算\"）")

    # 2. 每个知识点有"用自己的话说"
    lessons = sections(lines, LESSON_RE, ("## ", "### "))
    missing = [t for t, b in lessons if not any("用自己的话说" in l for l in b)]
    print(f"知识点小节: {len(lessons)} 个")
    if not lessons:
        errors.append("没有 `### x.y` 知识点小节（不是讲解型结构）")
    for t in missing:
        errors.append(f"缺\"用自己的话说\": {t}")

    # 3. 每个部分有误区与暂停
    parts = [(t, b) for t, b in sections(lines, PART_RE, ("## ",)) if "串起来看" not in t and "复习" not in t]
    print(f"部分: {len(parts)} 个")
    for t, b in parts:
        text = "\n".join(b)
        if "误区与陷阱" not in text:
            errors.append(f"缺\"误区与陷阱\": {t}")
        if "暂停" not in text:
            errors.append(f"缺\"暂停\"自测: {t}")

    # 4. 实例以计算结果收尾
    n_example = 0
    i = 0
    while i < len(lines):
        if re.match(r">\s*\[!example\]\s*实例", lines[i]):
            n_example += 1
            title = lines[i]
            j = i + 1
            block = []
            while j < len(lines) and lines[j].startswith(">"):
                block.append(lines[j])
                j += 1
            if not any("计算结果" in l for l in block):
                errors.append(f"实例没有\"计算结果\": {title.strip('> ').strip()}")
            i = j
        else:
            i += 1
    print(f"实例: {n_example} 个")

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

    print()
    if errors:
        print(f"=== 总结: {len(errors)} 处问题 ===")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("=== 总结: 全部通过 ✓ ===")


if __name__ == "__main__":
    main()
