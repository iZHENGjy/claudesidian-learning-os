# -*- coding: utf-8 -*-
"""【模板 · 复制改了用】把分节 markdown 拼成一份完整报告 draft.md。

这是 Mode B (整报告模式) 第 5 阶段"组装"的起点。每份作业复制一份, 改 4 个地方:
  1. SECTIONS    —— 你的分节文件名 (各 agent 写的 sec_*.md)
  2. CITE_MAP    —— 描述性引用 tag → APA 文内引用 (Crossref 查证过的真作者!)
  3. TABLES/FIGS —— 计算表格和图 (从 calc 的 output.txt 抄数字, 图用相对路径)
  4. REFS        —— APA 第7版参考文献 (按第一作者姓氏字母排序)

设计要点:
- 正文里写**描述性 tag** (如 [Meulenberg 2019]), 组装时统一换成 APA 文内 (Meulenberg et al., 2019)。
  好处: 正文不用动, 改 CITE_MAP 一处就全换; 中英两版共用同一套 APA 文内。
- 表格/图用两种注入: ① [[占位符]] (精确位置) ② 在某标题前插入 (锚点)。
- 跑完自检: 有没有没换掉的 tag、英文版有没有混进中文。

跑法: python assemble_template.py   (在作业 _drafts 目录下)
"""
import io, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def rd(f):
    return open(f, encoding="utf-8").read()


# ========== 1. 分节文件 (各 agent 写的) ==========
SECTIONS = ["sec_intro.md", "sec_calc_discuss.md", "sec_material.md", "sec_enhance.md"]

# ========== 2. 引用映射: 描述性 tag → APA 文内引用 ==========
# ⚠️ 作者名必须 Crossref/WebFetch 查证过, 绝不编! 无作者网页用 ("Title," n.d.)。
CITE_MAP = {
    "[Smith 2020]": "(Smith et al., 2020)",
    "[SomeWebPage]": '("Some Web Page," n.d.)',
    # ... 把你正文里用到的 tag 全列上
}

# ========== 3. 计算表格 / 图 (数字从 output.txt 抄; 图用相对路径) ==========
# 用 [[TABLE_X]] 占位符在正文里精确定位, 或下面用标题锚点插入。
TABLE_X = """
**Table 1. 标题 (条件)**

| 列A | 列B | 列C |
|---|---|---|
| 1 | 2 | 3 |

![Fig. 1. 图说明 (按出现顺序编号!)](figures/fig1.png)
"""

# ========== 4. 参考文献 (APA 7, 字母序) ==========
REFS = """
## References

Author, A. A., & Author, B. B. (Year). Title of the article. *Journal Name, Vol*(Issue), pages. https://doi.org/xxx

Title of web page. (n.d.). In *Site Name*. Retrieved Month Day, Year, from https://...
"""

COVER = """# 报告标题

**课程**: ___　|　**组别**: ___　|　**成员**: ___

---

"""


# ========== 组装逻辑 (一般不用改) ==========
def apply_map(text, m):
    for k, v in m.items():
        text = text.replace(k, v)
    return text


def clean_dangling_eqrefs(text):
    """清掉裸的公式交叉引用 (2.7)/(see §2.1) 之类 (从 _principles 抄来的悬空引用)。"""
    text = re.sub(r"\s*\(\d\.\d\)", "", text)
    text = re.sub(r"\s*\(see §\d\.\d\)|\s*§\d\.\d", "", text)
    return text


def build():
    parts = [COVER]
    for f in SECTIONS:
        s = rd(f)
        s = apply_map(s, CITE_MAP)          # tag → APA 文内
        s = clean_dangling_eqrefs(s)        # 清悬空公式号
        s = s.replace("[[TABLE_X]]", TABLE_X)   # 占位符注入表/图
        # 锚点注入示例 (在某标题前插表):
        # s = s.replace("### 2.4 标题", TABLE_X + "\n### 2.4 标题")
        parts.append(s)
    parts.append(REFS)
    draft = "\n\n".join(parts)
    open("draft.md", "w", encoding="utf-8").write(draft)

    # ---- 自检 ----
    print(f"[OK] draft.md 生成, {len(draft)} 字符")
    leftover = re.findall(r"\[[A-Z][^\]]*\d{4}[^\]]*\]|\[_principles[^\]]*\]", draft)
    print("未替换的引用 tag:", set(leftover) if leftover else "无")
    # 英文版额外查: 有没有混进中文 (中文版跳过这条)
    zh = re.findall(r"[一-鿿]", draft)
    print("残留中文字符数:", len(zh), "(英文版应为 0; 中文版忽略)")


if __name__ == "__main__":
    build()
