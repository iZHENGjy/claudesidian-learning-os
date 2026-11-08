<div align="center">

<a href="https://izhengjy.github.io/claudesidian-learning-os/"><img src="docs/assets/showcase.png" alt="把一门课，变成讲得清、算得对、考得到的笔记" width="820"></a>

# claudesidian-learning-os

**丢一份课件，得到一份讲得清楚、例题全部算完的笔记；考前一句话，整门课变成复习库和测验。**

Claude Code + Obsidian 插件

[![CI](https://github.com/iZHENGjy/claudesidian-learning-os/actions/workflows/ci.yml/badge.svg)](https://github.com/iZHENGjy/claudesidian-learning-os/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-0.4.0-2f7a4c)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-b8412c)](LICENSE)

**简体中文** · [English](README.en.md)

[在线展示](https://izhengjy.github.io/claudesidian-learning-os/) · [真实课程示例](examples/CME222-mass-transfer) · [快速上手](#快速上手)

</div>

## 它做什么

| 什么时候 | 你说 | 得到 |
|---|---|---|
| 每节课后 | "整理这节课" + 课件 PDF | 一份讲解型笔记：每个知识点先讲为什么需要它，再讲怎么用；课件例题全部算到结果 |
| 做习题时 | "解这份 tutorial" | 带推导的解答，并和整门课的公式表对账 |
| 学完一门课 | "蒸馏 CME222" | 整门课的公式推导树，每个公式有编号 |
| 考前 | "做 CME222 的复习库"，再说"考我 CME222" | 一页公式速查、全部易错点、按主题的题库；测验记录你哪些概念还没掌握 |

## 一份笔记长什么样

下面是示例课程（化工传质）第 3 讲里的一节，原样摘录，只删了课件截图：

> ### 3.2 Fuller 关联式（课件 p.22–24）
>
> **为什么需要它**
> 苯在空气里扩散，苯的 Lennard-Jones 参数不一定查得到，Hirschfelder 方程用不了。
>
> **它怎么工作**
> Fuller 关联式不用 $\sigma$ 和 $\varepsilon$，改用"扩散体积" $\Sigma v$ 代表分子的大小。简单分子的扩散体积直接查表；表里没有的分子，按它含有的原子把原子扩散体积加起来，有芳香环再加一个结构修正（p.23）。温度指数是 1.75，比硬球的 1.5 大。
>
> **实例 3.2**：30 °C、1 atm 下苯在空气中的扩散系数（p.24）
>
> $$(\Sigma v)_{C_6H_6} = 6\times16.5 + 6\times1.98 - 20.2 = 90.68$$
>
> $$D_{AB} = \frac{10^{-3}\times303^{1.75}\left(\frac{1}{78} + \frac{1}{29}\right)^{1/2}}{1\times\left(90.68^{1/3} + 20.1^{1/3}\right)^2} = 0.0920\ \text{cm}^2/\text{s}$$
>
> **计算结果**：0.0920 cm²/s，比表值换算结果低约 7%。
>
> **优缺点**
> 只需要分子式就能算，最方便。但 Fuller 和 Hirschfelder 都针对非极性分子；遇到氨、SO₂ 这样的极性分子，分子间还有偶极作用，需要再修正。
>
> <details><summary><b>用自己的话说</b>（先合上笔记自己讲，再点开对照）</summary>
>
> 你的回答应包含：
> - [ ] 用扩散体积代替 Lennard-Jones 参数
> - [ ] 扩散体积可以按原子加和，芳香环有结构修正
> - [ ] 温度指数 1.75，不需要碰撞积分
>
> 一种说法：如果查不到分子的"碰撞参数"，就换一种办法估它有多大：把分子里每个原子的"体积分"加起来，环状结构再扣一点。有了大小、质量、温度、压力，就能直接算出扩散系数。
> </details>

每一讲都这样写：上一节"优缺点"留下的问题，就是下一节"为什么需要它"的开头。每部分结尾还有常见误区（带数字反例）和一道预测题。[完整笔记 →](examples/CME222-mass-transfer/vault/CME222_传质/L03_diffusion_coefficient_estimation.md)

## 考前：复习库和测验

整门课压成一个复习库。题库每题标了类型、答案折叠、链接回出处小节：

> **第 2 题 [记忆] 对称性的前提**
> $D_{AB} = D_{BA}$ 成立的条件是什么？
>
> <details><summary>看答案</summary>二元体系、总摩尔浓度不变（气体即恒温恒压）。考点：L03 §1.2</details>

说"考我 CME222"，每轮出 4 道选择题，答错的概念连同错因记进掌握度：

| 概念 | 作答 | 答对 | 状态 |
|---|:---:|:---:|---|
| Fuller 的温度依赖 | 1 | 1 | 🟢 |
| Brokaw 中 σ_AB 的组合方式 | 1 | 0 | 🔴 沿用了非极性方程的算术平均，应为几何平均 |
| 表 J.1 的压力换算 | 1 | 0 | 🔴 把表中 $D_{AB}P$ 一列直接当成了 $D_{AB}$ |

## 和直接让 AI 写笔记有什么不同

<p align="center"><img src="docs/assets/compare.png" alt="同一道例题：旧版笔记停在思路，系数写成 0.19；新版算到 D = 0.344 cm²/s，验算通过" width="820"></p>

直接让 AI 整理课件，常见的结果是例题停在"思路是……"、系数抄错一位，读着顺所以没人发现。这里每份笔记都要过一遍检查脚本才算完成：

- **例题必须算完**，每个数字写进验算脚本 `verify.py`，算不对就改笔记，不许改断言凑数
- **公式系数对照课件原文**：上图旧笔记把 0.196 抄成了 0.19；如果笔记和验算脚本一起抄错，只有对照原文才查得出来
- **课件每一页都要被讲到**，跳过的页要写明理由
- **课件以外的内容要有出处**，查不到就标"待核实"，不凭记忆写

同一讲的新旧对比：例题算到结果 0/4 → 4/4，公式错误 1 → 0，空链接 10 → 0。[看完整示例和复现命令 →](examples/CME222-mass-transfer)

## 快速上手

需要：[Claude Code](https://claude.com/claude-code)、一个 Obsidian vault、Python 3.10+、免费的 [MinerU](https://mineru.net) token（用来把 PDF 课件转成文字）。

```bash
pip install requests PyMuPDF Pillow python-pptx python-dotenv rich pyyaml
```

在 vault 根目录建 `.env`，写一行 `MINERU_API_TOKEN=你的token`。然后在 vault 里打开 Claude Code：

```text
/plugin marketplace add iZHENGjy/claudesidian-learning-os
/plugin install claudesidian-notes@claudesidian-learning-os
```

之后丢一份课件说"整理这节课"就行。笔记会放在 `01_Projects/<课程代码>_<课名>/` 下，课名用什么语言都可以。

## 包含什么

| 插件 | 用途 |
|---|---|
| [`claudesidian-notes`](plugins/claudesidian-notes) | 主体：讲义笔记、习题、公式图谱、复习库、测验，以及论文整理 |
| [`chemeng-coursework`](plugins/chemeng-coursework) | 化工作业助手，也是"怎么给自己的专业加插件"的示范 |
| [`paper-review-toolkit`](plugins/paper-review-toolkit) | 写文献综述时，把论文数据抽进一张总表 |

主体插件不含任何专业知识，作者在工科、经济学、计算机、物理课上都直接用过。想给自己的专业加规则，照着 [`docs/PLUGIN_SPEC.md`](docs/PLUGIN_SPEC.md) 做。

## 说明

- 检查脚本能保证数字算对、公式抄对、课件讲全；但引用只能查"写了出处"，查不了出处是不是真的，所以笔记仍然值得你自己过一遍。
- 同一份课件多跑几次质量是否稳定，还没做系统测试。

## 致谢

源自基于 [claudesidian](https://github.com/heyitsnoah/claudesidian) 搭的 vault；PDF 抽取用 [MinerU](https://github.com/opendatalab/MinerU)；讲解型笔记结构借鉴 [Love Learning Anything](https://github.com/RAIZ-Zzz/love-learning-anything)，复习库和测验借鉴 [tutor-skills](https://github.com/RoundTable02/tutor-skills)。示例课程不附课件原图。

[更新日志](CHANGELOG.md) · [参与贡献](CONTRIBUTING.md) · [MIT 许可证](LICENSE)
