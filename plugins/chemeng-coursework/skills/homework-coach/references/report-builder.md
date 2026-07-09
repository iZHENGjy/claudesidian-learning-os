# Mode B 整报告模式 — 完整流水线

这是 homework-coach「整报告模式」的主文档。**只在用户显式说"从0做整份报告 / 整份 assignment / 整份 lab report"时走这套**（普通做题走 SKILL.md 的 Mode A）。

定位：**小组报告草稿生成器**。AI 出一份完整草稿（算 + 图 + 文 + 引用 + 排版），用户和组员**个性化 + 把学术诚信关**。不是"交了就行"的代写。

---

## 🚧 护栏（动手前先认，硬性）

1. **引用必须真**：作者名一律 Crossref/WebFetch 查证，**绝不编造作者**。查不到作者的网页用 APA 无作者规则 `("Title," n.d.)`。
2. **Turnitin 归用户**：交前用户必跑查重；教科书定义句（平均自由程定义、机制描述这种）**让用户/组员用自己话改写**——AI 不替写这步。
3. **关键假设问用户**：建模岔路（气体体系、固定分压 vs 浓度驱动力、限制剂、操作小时…）**不默拍**，AskUserQuestion 让用户定。
4. **每张图 Read PNG vision 核对**（见记忆 `feedback_vision_check_figures`）——不能只看代码或 agent 报告就交。
5. **本科生 lab report 口吻**（见记忆 `feedback_student_tone`）——禁研究生套话 / AI 腔。
6. **用户拥有最终版**：skill 只出草稿；填名、查重、个性化、核对数据源都是用户的事，交接时列清。

---

## 八阶段流水线

输出都放 `01_Projects/<CODE>_*/_drafts/<作业slug>/`。

### Phase 0 — Intake（主线程）
- Read 作业 PDF → 抽：**要求清单 + rubric 各项权重 + 格式约束**（页数上限、字体、行距、截止日）。
- 找适用的课程笔记：`01_Projects/<CODE>_*/_principles.md`（公式编号库）、相关 L##/T##。
- 写 `task.md`：题目本质 + 物理模型 + 假设清单 + 设计变量 + 已知常数 + 待查数据。

### Phase 1 — Plan + 澄清（主线程）
- **AskUserQuestion** 把关键建模岔路抛给用户（别默拍）。
- 确认**语言**：中 / 英 / 双（双语 = 中文做 master，再翻译；提交版按课程语言）。
- 确认 **scope**：整稿（Mode B）还是只算+骨架。
- EnterPlanMode 出执行计划给用户批。

### Phase 2 — 算 + 出图（主线程，计算是评分大头，自己把控）
- 写 `calc.py`：顶部强制 utf-8（`sys.stdout = io.TextIOWrapper(...)`）；import `plot_setup`（灰阶）或 `plot_pro`（彩色）。
- 算全量 + **打印逐步中间值**（给正文 worked example 用：每个代表点的 Step 1-N 中间数字）。
- 出图：每张画完 **Read PNG vision 核对**（outlier 压扁？标签溢出？中文方框？）；跑 `check_axis_range`。
- 自检：单位、量级、关键比值符号（如选择性 <1 是否合理）。
- 留 `output.txt`。

### Phase 3 — 文献数据（1 个研究 agent）
- prompt 见 `report-agents.md` §研究 agent。产 `data.md`（每个数字带可引用来源）。
- **引用查证**：研究 agent 给 URL/DOI，关键文献的真实作者**自己用 Crossref API 复核**（`https://api.crossref.org/works/<DOI>`），别信凑的。

### Phase 4 — 正文（并行 prose agent，每节一个）
- prompt 见 `report-agents.md` §分节写作。每节给：rubric 要求 + 已算数字 + data.md 引用 + **本科生口吻要求**。
- 正文里引用写**描述性 tag**（`[Meulenberg 2019]`），组装时统一转 APA。
- 双语：先中文，再 §翻译 agent 翻成英文（保 LaTeX、保 tag、保 fixed 英文标题）。

### Phase 5 — 组装（主线程）
- 复制 `scripts/assemble_template.py` 改：SECTIONS / CITE_MAP（tag→APA，作者查证过）/ TABLES（数字抄 output.txt）/ REFS（APA 字母序）。
- 表/图注入：`[[占位符]]`（精确）或标题锚点。**图按出现顺序编号**（机制/流程图在第1节就是 Fig.1）。
- 跑组装脚本，看自检：无残留 tag、英文版无残留中文。

### Phase 6 — 排版 + 验证（主线程）
```bash
pandoc draft.md -o final.docx --from markdown+tex_math_dollars
python .../scripts/docx_polish.py final.docx        # 默认三线表 DXA
python -c "from docx2pdf import convert; convert('final.docx','final.pdf')"
```
- 用 PyMuPDF 渲染逐页 → **Read 关键页 vision 核对**（表格满宽不挤？公式渲染？图编号顺序？中文不乱码？页数 ≤ 上限？）。
- docx 才是交付物；PDF 只是预览，**会被阅读器锁**（删不掉/不刷新就换名转 `_verify.pdf`）。

### Phase 7 — 多 agent 评审（并行 4 个）
- prompt 见 `report-agents.md` §四审。四维：**rubric 合规 / 计算独立复算 / APA 引用 / 写作AI味**。
- 汇总后**把可改的落实到两版**（图编号、孤儿引用、AI 味词、°C 空格、表述歧义…）。
- 计算审计若报错→停下核对，别带病交。

### Phase 8 — 交接（主线程）
列 user action items：填组号+成员名、**跑 Turnitin**、**个性化改写教科书定义句**、核对引用源（尤其量级类数字）、确认数据假设老师认可。

---

## 教训（治本次踩的坑）

- **子 agent 常只报空闲不发内容** → 完成后用 SendMessage 显式要结果；关键数据（如真实作者）别等它，自己 Crossref 查更稳。
- **Windows console GBK** → 每个 python 脚本顶部 `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')`。
- **heredoc 塞 LaTeX 会被转义乱**（`\alpha`→`\a`bell、`\times`→tab）→ 改 .md 用 **Edit 工具**直接改，别用 `python << EOF` 塞反斜杠。
- **PDF 被锁** → docx 是交付物；锁了换名 `_verify.pdf` 转。
- **图编号按出现顺序** → 机制图在第1节就该 Fig.1，别让它叫 Fig.5 排在 Fig.1 前。
- **calc 参数改了回头对齐正文手写数字** → 组成/物性一改，prose agent 早写的数字就过期，组装前统一对一遍 output.txt。
- **APA 文内别和文末重复** → "数据来源：Meulenberg et al. (2019) [Meulenberg 2019]" 转换后会双标，tag 那处只留描述。
- **教科书定义句查重高危** → 标出来让组员改，AI 不替写。

---

## 复用资产速查

| 要做的事 | 用什么 |
|---|---|
| 灰阶工程图 | `scripts/plot_setup.py` `apply_chemeng_style()` |
| 彩色专业图 | `scripts/plot_pro.py` `apply_pro_style()` + `PALETTE` |
| 三线表排版 | `scripts/docx_polish.py`（默认三线表 DXA）|
| 组装+APA | `scripts/assemble_template.py`（复制改）|
| agent prompts | `references/report-agents.md` |
| docx 细节 | `references/docx-format.md` |
