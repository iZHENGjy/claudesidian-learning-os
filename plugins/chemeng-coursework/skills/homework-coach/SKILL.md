---
name: homework-coach
description: 化工作业助手，双模式。**Mode A 做题伙伴（默认，决策前置）**：AI 先出"决策简报"（待求参数/课内候选方法/适用条件），方法级+假设级决策由用户拍板后才算数/验算/排版，不代写正文；用户明说"直接算"可跳过引导。**Mode B 整报告模式（显式 opt-in）**：用户说"从0做整份报告/小组报告"才触发，出完整草稿（算+图+文+APA引用+排版+多agent评审）+ 内置护栏。Triggers - 做题:"帮我算这道题"/"做这份 tutorial"/"帮我做这道作业题"；整报告:"从0做这份小组报告"/"整份 assignment 帮我做"/"帮我写整份 lab report"。Not-triggers - "解释概念"→explain-concept；"整理这节课笔记"→ingest-lecture；"和我讨论思路"→直接对话。
---

# Skill: homework-coach

## 两种模式（先分流）

| 用户说 | 模式 | 干嘛 |
|---|---|---|
| "帮我算这道题"、"做这份 tutorial" | **A 做题伙伴（默认，决策前置）** | AI 先出决策简报，你拍板方法+假设，AI 才算/验/排版，**不代写正文**。走下面 Phase 0-4。 |
| "从0做这份小组报告"、"整份 assignment / lab report 帮我做" | **B 整报告模式（opt-in）** | AI 出完整草稿（算+图+文+引用+排版+评审）。**Read `references/report-builder.md` 照着 8 阶段跑**。 |

⚠️ **Mode B 是显式 opt-in**：用户没明说"整份/从0做整个报告"就默认走 Mode A，守住"不代写正文"。下面的 Phase 0-4 是 Mode A 的细节。

## 这个 skill 干嘛的

我是化工本科生。做作业不能 AI 代写正文 —— 学术诚信 + 老师一眼能看出 AI 味。另一个病：AI 一上来就替我把所有决策做完，我看着它跑但什么都没学到。

**定位**：做题伙伴 + 决策导航。AI 铺决策地图，你思考 + 拍板 + 写正文，AI 落地算数 / 验算 / 排版。

**做**：Python 算数、单位/量级/守恒闭合 check、对你写的段落给反馈、md→docx 排版。
**不做**：长段中英正文、文献综述、reference 编造、AI 全自动出 docx。

## 触发

- "帮我做 CME### tutorial N"
- "帮我算这道题"
- "做这份作业"

不该触发：
- "解释概念" → `/explain-concept`
- "整理这节课笔记" → `/ingest-lecture`
- "把这份 tutorial 的题目和答案归档到笔记" → `/ingest-tutorial`
- "和我讨论思路" → 直接对话，别套 skill

## 输出位置

```
01_Projects/CME###_*/_drafts/{作业slug}/
├── task.md       # 题目原文 + 你的思路 + 题目给的参数清单
├── decisions.md  # 决策日志（每个决策点你选了什么、自主还是提示后）
├── calc.py       # 可重跑的 Python 计算脚本
├── output.txt    # 计算结果（含每个数字的单位 + 闭合 check）
├── figures/      # 如果题目要求出图才有
├── draft.md      # 你写的正文（AI 只 review 不代写）
└── final.docx    # pandoc 转出的最终版
```

## skill 自带工具

```
${CLAUDE_PLUGIN_ROOT}/skills/homework-coach/
├── SKILL.md
├── references/
│   ├── decision-briefing.md  # ◆Phase 0/0.5/4 决策导航完整规则（简报模板/降级链/交互协议）
│   ├── plot-style.md         # 画图前 Claude 读一遍这个
│   ├── chemeng-plots.md      # 分离过程图解法（三元图/阶梯/干燥曲线）专用函数用法
│   ├── docx-format.md        # 排版前 Claude 读一遍这个
│   ├── report-builder.md     # ★Mode B 整报告 8 阶段流水线（主文档）
│   └── report-agents.md      # ★Mode B 可复用 agent prompt 模板
└── scripts/
    ├── plot_setup.py         # apply_chemeng_style() 灰阶工程图风
    ├── plot_pro.py           # ★apply_pro_style() Okabe-Ito 彩色专业风
    ├── chemeng_plots.py      # 分离过程图解法专用画图库（8 个函数）
    ├── examples_cme214.py    # 拿 tutorial 数据验证 + 出参考图
    ├── assemble_template.py  # ★Mode B 组装模板（拼节+APA引用+插表图，复制改）
    ├── docx_polish.py        # pandoc 转完 docx 后跑, 字体兜底 + 三线表DXA + 图居中
    └── format_compliance.py  # 课程说明有硬性格式要求时, 在 docx_polish 之后跑（可选）
```

（★ = Mode B 整报告模式专用）

按需 import / 调用，**不强制每次都跑**（纯文字题不画图就别 import；不交 docx 就不跑 polish）。

## 5 个 phase（Mode A）

### Phase 0 — 决策简报（AI 铺地图，不算数、不推荐）

**动手算之前必走**。先 Read `references/decision-briefing.md`，开头问一次档位——**学习**（0基础，边做边教）/ **练习**（默认，判别条件后置）/ **冲刺**（熟练/赶due，完整简报）——然后每道题出一份简报：

- **已知 / 待求 / 参数缺口**（要到 X 得先求 a、b 的倒推链）
- **课内工具箱**：候选方法表，**不标推荐**。练习/学习模式只列方法名+出处（判别条件你试答后才揭示）；冲刺模式才带"适用条件"列。依据从课程笔记按降级链查（`_principles` → 知识块/index → manifest → 联网），绝不凭印象编
- **课外资源**：需要外部物性/数据时去哪查
- 结尾把问题抛回给你："你觉得哪个能用？依据是什么？"

逃生门：冲刺模式下说"直接算"→ 提醒一句后 AI 代选，decisions.md 全标 `[AI代选]`（不强迫学习）。

### Phase 0.5 — 决策收集（两段式：你先试答，AI 才揭示判别条件）

方法级（题型判断 / 用哪套公式）+ 假设级（限制剂 / 驱动力 / 边界条件 / 参数来源）决策逐个过：

1. **你先试答**：选哪个 + 依据是什么
2. **AI 才揭示判别条件对答案**：对 → 记 `[自主]`；错 → 指出漏洞让你重选（不直接给正确答案），记 `[提示后]`
3. 你说"不知道 / 展开" → AskUserQuestion 放选项（每项附适用条件 + 笔记出处，**不标推荐**）→ 记 `[提示后]`

学习模式额外：每个决策点前 AI 先讲 3-5 句概念（带出处，**讲概念不讲答案**）。全部拍板前**不写 calc.py**。细节协议见 `references/decision-briefing.md`。

### Phase 1 — 解题（AI 按你的决策执行）

1. **输入 = Phase 0.5 拍板的方法 + 假设**，不再自己另选路线
2. **AI 写 calc.py**：把你的决策翻译成 Python，每步带中文注释；用户拍板的方法/参数在注释里标出（如 `# 方法选择：变夹带图解（用户定，见 decisions.md #2）`）
3. **AI 跑出 output.txt**：每个数字带单位 + 中间步骤
4. **题目要图就画**：
   - **分离过程课（如 CME214 单元操作 II）的三元相图 / 阶梯法 / 干燥曲线 / 过滤线性图 / SLE 直角三角图 / LLE [D] 差点图解 / 湿度图 → 先看 `references/chemeng-plots.md`，用 `chemeng_plots.py` 里 8 个测好的函数，别从零写**（坐标变换 / stepping / 积分临时写必踩坑；湿度图要 `pip install psychrolib`）
   - 其他图：Claude 先 Read `references/plot-style.md` 一遍（中文字体 / 黑白工程图 / 防 outlier 压扁 / 单位规范）
   - calc.py 顶部必 import `plot_setup`：
     ```python
     import sys
     sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/skills/homework-coach/scripts')
     from plot_setup import apply_chemeng_style, check_axis_range
     apply_chemeng_style()
     ```
   - 画完每张图必跑 `check_axis_range(ax, y_data)`，warn 了就修 ylim
   - **画完 Read 一遍 PNG 自查**（vision check）：不能只看代码或 agent 报告就交付，要亲眼确认没有 outlier 把主趋势压扁

**红线**：AI 不替你做关键假设（限制剂 / 操作小时 / 物性来源）。题目少参数 → STOP 问你。

### Phase 2 — 验算（AI 主导）

AI 自动 check 计算：
- 每个数字带单位（不带的标出来）
- 量级合理性（密度 ≠ 10000 kg/m³，温度 ≠ 5000 K 之类）
- 守恒闭合（mass / element / energy balance，tolerance < 1%）
- 公式推导一步一步，不跳步

对你写的初稿段落，AI 只给反馈：
- 哪里漏 step / 公式错 / 单位漏 / 量级错
- **不替你重写**，只列问题，你自己改

如果发现你的思路有逻辑漏洞（如忽略相变、忘了 driving force），AI 提一下让你判断。

### Phase 3 — 排版（自动）

Claude 先 Read `references/docx-format.md` 一遍。然后两步走，**不能跳第二步**：

```powershell
# 1. pandoc 转 docx, tex_math_dollars 必加（公式渲染靠它）
pandoc draft.md -o final.docx --from markdown+tex_math_dollars

# 2. 后处理: 中文字体兜底 + 三线表DXA列宽 + 表头加粗 + 图片居中
python ${CLAUDE_PLUGIN_ROOT}/skills/homework-coach/scripts/docx_polish.py final.docx
# (默认三线表; 想要旧的全网格表加 --grid)
```

学校有 Word 模板：第 1 步加 `--reference-doc=学校模板.docx`，第 2 步照跑。

**课程说明写死了格式要求**（正文 Times New Roman 10pt / 公式右侧编号 / 三栏页眉 / 页脚页码之类）→ 再跑一步
`python ${CLAUDE_PLUGIN_ROOT}/skills/homework-coach/scripts/format_compliance.py final.docx <课程代码>`。
可选，没有硬性格式要求就不用跑；踩到新的格式坑往这个脚本里加规则，别只改单份作业。

**跳过 docx_polish.py → 必然踩中文字体 / 表格 / 图片居中三个坑**（详见 references/docx-format.md）。

### Phase 4 — 复盘（留学习痕迹）

1. 写 `decisions.md` 到 `_drafts/{作业slug}/`：每个决策点 / 你的选择 / `[自主]` 还是 `[提示后]` / 依据出处（模板见 `references/decision-briefing.md`）
2. 卡住的知识点单独列一段（指向 L## / _principles 编号），复习优先
3. 对话末尾口头小结一遍："你自主拿下了什么、卡在哪"

## 规则

1. **AI 不写描述性正文**。可以写：calculation steps（公式 + 数字代入 + 单位）、Python 代码注释。不能写：problem statement、approach 段、conclusion 段、对结果的解释 —— 这些你自己写。
2. **缺参数 STOP 问你**，不自创假设。
3. **每个数字标 source**：题目给的 / 你假设的 / 课堂笔记的（注明 `L##` 出处）/ 外部数据的（贴 URL）。
4. **不强制 reference**。绝大多数 tutorial 数据全在题面，不需要外部 paper。如果题目明确要外部 reference 才走 `/ingest-paper`。
5. **不强制 BFD / 焓表模板**。题目要求才画 / 才列。
6. **守恒闭合 FAIL → STOP**，告诉你差值在哪个 unit，等你决定怎么改假设。
7. **数值量级离谱（偏 100x 以上）→ STOP**，不擅自往下走。
8. **画图 / 排版必走 skill 自带工具**：画图必 `apply_chemeng_style()`，排版必跑 `docx_polish.py`。AI 默认 matplotlib + pandoc 配置会踩 8 个坑（见 `references/plot-style.md` + `references/docx-format.md`）。
9. **简报阶段不给推荐、不先算数值**——把答案剧透了决策就白问了。练习/学习模式连判别条件都后置（试答后才揭示）；冲刺模式才给完整表。
10. **方法级 + 假设级决策没拍板前不写 calc.py**。冲刺模式说"直接算"才由 AI 代选，且提醒一句 + decisions.md 全标 `[AI代选]`。
11. **每个决策记进 decisions.md**，区分 `[自主]` / `[提示后]`——这是防 AI 依赖退化的档案，不是形式主义。

## Failure modes

| 模式 | 怎么处理 |
|---|---|
| 作业 PDF 路径找不到 | 问你路径 |
| 题目缺参数 | STOP 列出缺什么，等你给假设或题目原文 |
| 计算闭合 FAIL | 报告差值 + 哪个 unit 出问题，等你决定 |
| pandoc 报错 / Word 占用 docx | 提示你关 Word 再 retry |
| 你写的段落 AI review 出问题 | 列出问题，**不直接改你的文字** |

## Mode B — 整报告模式（细节看 references/report-builder.md）

**只在用户显式说"从0做整份报告 / 整份 assignment / 整份 lab report"时走。** 定位 = 小组报告**草稿生成器** + 护栏，用户和组员负责个性化 + 把学术诚信关。

8 阶段：① Intake 读 PDF 抽 rubric → ② Plan + 关键假设问用户 → ③ 算+图（vision 核对）→ ④ 文献数据(研究 agent) → ⑤ 分节正文(并行 agent，本科口吻) → ⑥ 组装(cite_map→APA + 三线表) → ⑦ 排版+PDF 验证 → ⑧ 多 agent 四审(rubric/算/引/写) → 交接 user action items。

**护栏（硬性）**：引用必须 Crossref 查证**绝不编**；Turnitin + 教科书句改写归用户；关键假设问用户；每图 vision 核对；**只出草稿**。

→ 照 `references/report-builder.md` 跑；agent prompt 抄 `references/report-agents.md`；组装用 `scripts/assemble_template.py`。

## 跟其他 skill 的关系

- `/ingest-paper` — 罕见，题目明确要外部 paper 时才调
- `/explain-concept` — 卡在某个概念时单独跑
- `/ingest-tutorial` — 不一样的任务（归档 tutorial 到笔记），不是当下做题
