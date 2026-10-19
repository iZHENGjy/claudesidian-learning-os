# Lessons — ingest-lecture

踩过的坑和参考样例。遇到怪现象先翻这份。

---

## Failure modes

| 模式 | 触发 | 处理 |
|---|---|---|
| PDF 读 password-protected 误报 | Read 工具说 PDF 加密但实际未加密 | 改用 `PyMuPDF`（`import fitz`）提取 |
| 课程文件夹不存在 | `01_Projects/<CODE>_课名/` 没有 | 问用户课程名 + 学期，创建文件夹 + index.md，**不擅自猜** |
| extract_images.py 失败 | PPT 解析错 / 0 图 | WARN，继续生成笔记（无图嵌入），报告用户 |
| MOC 已存在但 frontmatter 不合规 | index.md 缺 frontmatter | WARN，只追加 Week 段，**不修 frontmatter** |
| 一讲多 PDF/PPT | 用户传多份附件 | 逐份提取后合并到**同一笔记**；不为每份生成独立笔记 |
| MinerU 图片 hash 是 64 位（2026-10 起） | `images/<hash>.jpg` 的 hash 是 sha256 64 位十六进制，不是 32 位 | sub-agent prompt 写"完整 64 位"，重命名脚本用 `[0-9a-f]{64}` 校验 |
| 按页切分漏图 | 用 `*_content_list.json` 的 `page_idx` 切分逐页 md 时只认 `image`/`table`，漏掉 `type: chart` 的图（数据图、响应曲线） | 切分时把 `chart` 一起算；重命名后 grep full.md 确认 `hash refs left = 0` |
| 关键图 MinerU 没导出 | 整页蓝底图、公式截图被抽成零散文字，没有图片文件 | 从 `_pages/*.png` 按坐标裁剪成 `<CODE>_L##_p##_<slug>_<type>.jpg` 放进 images/；课件漏画的图可自绘并在文件名和说明里标 selfdrawn |
| sub-agent 报告主导写笔记 | 主线程拿到 sub-agent 输出 + MinerU md 后**没 Read 旧笔记 / 模板**就动笔 | **STOP**，回到 Step 4 开头先 Read 旧笔记列章节清单，再决定 Edit 还是 Write |

---

## Example — Good

知识块 + 图：

```markdown
## 知识块 1 — Fick 第一定律

扩散通量与浓度梯度成正比:

$$J_A = -D_{AB} \frac{dc_A}{dz}$$

**解读**: A 组分通量 = 扩散系数 × 浓度梯度的负值。负号表示
扩散从高浓度到低浓度方向。

[[扩散系数]] $D_{AB}$ 量级决定传质速率——气体 ~10⁻⁵ m²/s,
液体 ~10⁻⁹ m²/s。

![[CME222_L02_s09.png]]
> Fick 定律示意:通量方向沿浓度降低方向

> [!tip] 延伸(非 PPT 内容)
> Fick 定律与傅里叶导热 $q = -k\nabla T$ 形式完全类比。
```

## Example — Bad

- 全英文
- slide-by-slide 镜像
- 没有知识块组织
- 通用 padding 替代具体解读
