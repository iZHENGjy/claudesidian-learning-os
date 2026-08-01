# 化工作业 docx 排版规范

Phase 3 排版按这份操作。**两步**: pandoc 转 docx, 再跑 docx_polish.py 兜底。漏第二步就会出中文字体 / 表格 / 图片居中的坑。

## 标准流程

```powershell
# 1. pandoc 转 docx (公式必须加 tex_math_dollars)
pandoc draft.md -o final.docx --from markdown+tex_math_dollars

# 2. 后处理 (字体兜底 + 表格 grid + 图片居中)
python ${CLAUDE_PLUGIN_ROOT}/skills/homework-coach/scripts/docx_polish.py final.docx
```

学校提供 Word 模板时:
```powershell
pandoc draft.md -o final.docx --from markdown+tex_math_dollars `
  --reference-doc=path/to/学校模板.docx
python ${CLAUDE_PLUGIN_ROOT}/skills/homework-coach/scripts/docx_polish.py final.docx
```

`--reference-doc` 决定段距 / margin / 字号 / heading 样式; docx_polish.py 只补 reference docx 漏掉的中文字体 + 表格 / 图片细节, **两者职责不冲突**, 都要跑。

## 公式

markdown 里:
- inline: `$...$`
- block: `$$...$$`

pandoc flag **必须** `--from markdown+tex_math_dollars`, 否则 `$` 不会被识别成公式分隔符。

复杂公式 (多行对齐 / 矩阵):
```markdown
$$
\begin{aligned}
\dot{m}_{in} &= \dot{m}_{out} + \dot{m}_{reacted} \\
&= \rho v A + r V
\end{aligned}
$$
```

pandoc 转 OMML (Office Math), Word 原生渲染, 不依赖 LaTeX 安装。

## 表格

标准 markdown 表格:
```markdown
| 参数 | 值 | 单位 |
|---|---|---|
| Temperature | 298 | K |
| Pressure | 101.3 | kPa |
| Flow rate | 12.5 | mol/s |
```

docx_polish.py 默认 (三线表) 会自动:
- **三线表**: 顶线 + 表头下线 + 底线, 无竖线无内横线 (学术规范 booktabs 风)
- **固定 DXA 内容自适应列宽**: 满页宽, 不挤在左边窄栏。**不用百分比**——百分比列宽在 Google Docs 会崩 (Anthropic 官方 docx skill 的硬规则)
- 表格字 9pt + 表头加粗居中 + 单元格垂直居中
- 全部 cell 字体兜底为微软雅黑 (中文) + Times New Roman (英文/数字)

想要旧的全网格 (Table Grid): `python docx_polish.py final.docx --grid`。

**为什么不是 pandoc 默认**: pandoc 转宽表 (≥6 列) 会挤在左边窄栏、列宽乱; docx_polish 的 DXA 重算列宽治这个坑。

**数字右对齐** docx_polish.py 没做 (默认左对齐够用)。要右对齐手动改。

## 排版后必验证 (Mode B / 重要报告)

docx 才是交付物。转完用 docx2pdf + PyMuPDF 渲染逐页 **Read 关键页 vision 核对**:
```bash
python -c "from docx2pdf import convert; convert('final.docx','final.pdf')"
# 再用 fitz 渲染 → Read PNG 看: 表格满宽不挤? 公式渲染? 图编号顺序? 中文不乱码? 页数 ≤ 上限?
```
⚠️ PDF **会被阅读器锁** (删不掉/不刷新) → 锁了换名转 `_verify.pdf`; docx 是交付物, PDF 只是预览。

## 图片

markdown 里:
```markdown
![图1: 反应器转化率随温度变化](figures/conversion_vs_T.png)
```

- alt text 兼做 caption (pandoc 转 docx 时不会自动生成 caption, alt text 会跟在图下方作为段落)
- 图片路径用相对路径 (`figures/...`), 不要绝对路径
- docx_polish.py 把含图片的段落自动居中

## 中文字体

**这是最大的坑**。Word 里 "字体" 其实有两套: West (西文) + East Asia (中文)。pandoc 默认只设 West, 中文 fallback 到 docx 模板的默认 East Asia 字体 (经常是宋体, 跟正文 Times New Roman 不协调; 或者没设, 显示成方框)。

docx_polish.py 的 set_run_fonts() 给每个 run 强制设:
- East Asia = Microsoft YaHei
- ascii / hAnsi = Times New Roman

这样中文是雅黑, 英文/数字是 TNR, 风格一致。

如果学校模板有特定中文字体要求 (如宋体), 改 docx_polish.py 里 `CHINESE_FONT = 'SimSun'`。

## 常见踩坑

| 坑 | 处理 |
|---|---|
| 中文字体不统一 / 显示方框 | docx_polish.py 字体兜底 (必跑) |
| 公式 `$...$` 没渲染, 显示成 `$Q=mC\Delta T$` 原文 | pandoc 没加 `--from markdown+tex_math_dollars` |
| 表格没边框 / 表头不加粗 | docx_polish.py 自动处理 |
| 图片左对齐 | docx_polish.py 自动居中 |
| pandoc 报 `permission denied` 写不进 docx | Word 打开了这个文件, 关掉再 retry |
| 学校模板 margin 错了 | reference docx 里改, 不要在 docx_polish.py 改 |
| heading 不分级 | markdown 里用 `#` / `##` / `###`, 不要用 `**粗体**` 假装标题 |
| 列表渲染丑 | 用标准 `-` / `1.` markdown 列表, 不要 `•` 这种 unicode |

## 一句话验收

转完 docx 用 Word 打开, 翻一遍:
- 中文都是雅黑, 英文/数字都是 TNR
- 公式渲染正常
- 表格有 grid, 表头加粗居中
- 图片居中, 有 caption
- 标题分级清楚

任一不对 → 回 markdown 改, 重新跑 pandoc + docx_polish.py。
