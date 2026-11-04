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
| sub-agent 报告主导写笔记 | 主线程拿到 sub-agent 输出 + MinerU md 后**没 Read 旧笔记 / 模板**就动笔 | **STOP**，回到 Step 4 开头先 Read 旧笔记列章节清单，再决定 Edit 还是 Write |

| 例题只写"思路"没算完 | 赶进度、觉得"读者自己会算" | 课件例题一律算到**计算结果**，并进 verify.py；2026-11 对比发现旧版 L02 的 Example 2、3 都停在思路 |
| 质量通量差 1000 倍 | 分子量 12 g/mol 直接乘，结果标成 kg | 算 kg 单位时分子量写成 0.012 kg/mol；verify.py 里用 kg/mol 写断言（旧版 L02 Example 4 写成 2.4×10⁻⁶ kg/(m²·s)，正确是 2.4×10⁻⁹） |
| 大量空链接 | 给"以后可能建"的概念页预留 `[[术语]]` | 只链接已存在的笔记；check_note.py 会报出 |
| AI 补充里有错 | 凭记忆写"APF 高 → 熔点高"这类说法，没有出处 | 课件以外的内容先上网核对，写进带来源的"补充"折叠块；核对不了就删 |
| 公式系数 / 组合规则抄错 | 凭印象写公式（旧版 L03 把 Brokaw 的 0.196 写成 0.19；新版初稿 Brokaw 用了算术平均 σ） | 写每个公式前对照课件原页；同一讲不同方法的混合规则分开写清 |
| 例题依赖课件外数据 | L03 例题要 Lennard-Jones 参数、沸点下摩尔体积，课件没给 | 上网核对后标出处；核对不了标"待核实"，verify.py 里同样注明 |

---

## Example — Good

一个知识点小节（节选，完整范例见 `examples/` 或对比文件夹里的 L02）：

```markdown
### 3.1 通量与 Fick 第一定律（Flux & Fick's first law）（p.15）

**为什么需要它**
Example 3 里管子一端 He 分压 0.6 atm，另一端 0.2 atm，相距 0.2 m。我们想知道每秒每平方米有多少 He 扩散过去，但手上只有两端浓度，没有分子速度，需要一条把"浓度差"和"流量"直接连起来的规律。

**它怎么工作**
浓度沿某方向降得越陡，往那个方向扩散得越快，比例系数叫扩散系数。负号表示从浓处流向稀处。这条定律给的是相对运动流体的扩散通量，被整体带走的部分第 4 部分再加回来。

**课件里的概念**
$$J_{A,z} = -D_{AB}\frac{dc_A}{dz} \tag{3.2}$$

> [!example] 实例 3.1：He–N₂ 管中扩散（p.18）
> $$\begin{aligned}J_{A,z} &= -D_{AB}\frac{c_{A,2}-c_{A,1}}{\Delta z} = -0.687\times10^{-4}\times\frac{8.18-24.54}{0.2}\ &= 5.62\times10^{-3}\ \text{mol/(m}^2\text{·s)}\end{aligned}$$
> **计算结果：** $J_{He} = 5.62\times10^{-3}$ mol/(m²·s)，$j_{He} = 2.25\times10^{-5}$ kg/(m²·s)。

**专业说法：** 扩散通量与浓度梯度成正比、方向相反。*EN: Fick's first law: diffusive flux is proportional and opposite to the concentration gradient.*

**优缺点**
只要两端浓度就能算。但它默认总浓度不变，数据也常给摩尔分数，所以需要下一节的其他写法。

> [!question]- 用自己的话说：Fick 第一定律
> > [!success]- 关键环节：你的回答应包含
> > - [ ] 通量是每秒每平方米穿过的量
> > - [ ] 浓度降得越陡扩散越快，比例系数是扩散系数
> > - [ ] 从浓到稀，所以有负号
```

## Example — Bad

- 以定义或公式开头，没有先讲"为什么需要它"
- 要点列表堆术语代替讲解
- 例题只写思路不算到结果
- 课件以外的说法没有出处
- 给不存在的概念页加 `[[链接]]`
- 以用户口吻写"我的疑问"
