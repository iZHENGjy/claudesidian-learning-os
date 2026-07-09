---
name: extract-paper-note
description: 从 ingest-paper 处理过的论文文件夹抽数据，逆向实验设计，直接填进主 Excel 4 个 sheet + 写 notes/checklist。Triggers - "抽这篇论文的数据" / "extract paper note" / "整理 SS-X 的数据" / "做 SS-X 的笔记"。Not-triggers - 还没跑 ingest-paper（缺 main.md / 图还是 hash 命名）、综述 / perspective 类论文、只想快速了解论文讲什么而不入库、lecture / tutorial（走对应 skill）。
---

# Skill: extract-paper-note

## Role

从 `ingest-paper` 处理过的论文文件夹（含 vision 修过的 `main.md` + `si.md` + 带分级 alt text 的图 + `meta.yaml`），**逆向出论文的实验设计**，直接把数据填进主 Excel 4 个 sheet，并写 2 份人看的产物。

| 产物 | 给谁 | 规范 |
|---|---|---|
| 主 Excel 4 sheet | 你审 | 论文清单(配方) / 样本数据(性能) / 样本卡片(实验设计) / 大矩阵(自动联动) |
| `notes.md` | 你快速看论文 | 实验目的/结构/过程/缺陷 → `references/notes-template-spec.md` |
| `checklist.md` | 你复查 | 逐图表讲解+分类+入表位置 → `references/checklist-spec.md` |

## 核心设计原则（这次重写的根本）

**模型直接读论文 + 直接懂主 Excel 列 → 直接生成行。脚本只做机械写入，零语义判断。**

- ❌ 不再有 `samples.yaml` 中间层 schema（旧版的过度设计，压制模型、引入 bug）
- ✅ 模型读 main.md/si.md，逆向实验设计，自己决定拆几行、每列填什么
- ✅ 模型产出一个 `extract_handoff.json`（列名已对齐主 Excel），脚本照着写
- ✅ 脚本 `write_to_excel.py` 只负责：找对位置、备份、写入、避开公式/合并格

## 两条铁律（旧版违反的，务必遵守）

1. **样本数据的 `Group` 列填 var_code**（`A1`/`A8`/`D1`...），**不是长句描述**
2. **每个对照实验组 = 一个 var_code，组内每个取值展开一行**（学现有 SS-1..SS-6 范式）。同一物理样本在多个对照组出现 → 多行

### ⚠️ "对照组" ≠ "表征条件扫描"（SS-7 踩过的坑）

判断某个变量该不该单列成一组（=展开行）：**问"论文是不是设计来研究这个变量的影响"**。

- ✅ **是对照组**：论文专门做 A/B 对比来回答"X 变了性能怎么变"
  - SS-6 测 -20/0/20/40°C 的力学 → 研究"抗冻性"，温度是研究对象 → D1 成组
- ❌ **只是表征条件**：某条件只是测量的 x 轴 / 常规扫描，不是研究对象
  - SS-7 的电导-温度曲线(25-100°C) → 温度只是 Arrhenius 表征的 x 轴，研究对象是"4 个样本电导一不一样" → **不成组**，主列放代表温度(25°C)值，温度依赖进 notes
- ❌ **凑手头样品的差异**：对照里附带变了的次要参数，不是主变量
  - SS-7 拉伸对照(交联3.8 vs 未交联3.4)主变量是**交联**，分子量3.4/3.8只是手头样品 → 归 A8(交联)，**不单列** A12(分子量)

宁可少分组、忠实于论文设计，也不要把表征扫描虚增成对照组（会灌水行数、误导读者）。

## When to trigger

- "抽这篇论文的数据" / "extract paper note" / "整理 SS-X 的数据"
- 用户指定 `01_Projects/Review_<主题>/papers/(YYYY) Title/` 路径

**不触发**：还没跑 `ingest-paper`（缺 main.md / 图还是 hash / 缺 alt）→ STOP；review/perspective → STOP；lecture/tutorial 走对应 skill。

## Inputs

- 论文文件夹（必须有 main.md + si.md 含 alt text + images/ figN 命名 + meta.yaml）
- 主 Excel `01_Projects/Review_离子凝胶/IONOGEL_dynamic (8).xlsx`

## 主 Excel 4 个 sheet（先读懂结构再填）

| Sheet | 内容 | 颗粒度 | 怎么填 |
|---|---|---|---|
| **论文清单** | 配方基础(Monomer/IL liquid/Initiator/Crosslinker/UV) + 元数据 + Monomer_Polar/Nonpolar/IL_short | 每篇 1 行 | handoff `论文清单` dict，脚本 append |
| **样本数据** | Group(var_code) + Sample + 48 列性能 | 每样本/条件 1 行 | handoff `样本数据` 行数组，脚本 append |
| **样本卡片** | 实验设计图谱：每变量取值序列+样本数 | 每篇 1 张卡 | handoff `样本卡片` dict，脚本写**空白卡** B 代号 + 变量表 E/F/G |
| **大矩阵** | 57 变量横向指纹 | 每篇 1 行 | **不写**！全公式联动，填好样本卡片后对应行自动汇总 |

**关键约束**：
- 样本卡片是公式驱动（基础信息 VLOOKUP、总数 COUNTA）→ 脚本只填代号 + 变量表 E(取值序列)/F(样本数)/G(备注)，**绝不碰公式格**
- 主 Excel 现有卡片代号有历史错位 → 脚本自动选**第一张全空白卡**（标题空+代号空），不覆盖任何数据
- **空白卡用完会自动扩容**：`ensure_blank_card` 复制用户预留的「空白卡片模板」块（公式行引用自动偏移、合并格/样式照搬），批量 148 篇不会卡在卡片数量
- 大矩阵每行的 SUMIFS/IF 公式自动联动对应样本卡片，手写会破坏公式。⚠️ **已知限制**：仅预留的 5 张空白卡(641-961)在大矩阵有联动行；**扩容新建的卡大矩阵暂无联动行**——大矩阵本身有历史错位，建议日后整体重建，而非在错位基础上插行

## Workflow（单线程，模型从头读到尾）

### Step 1 — 逆向实验设计

通读 `main.md` + `si.md` + 所有图表 alt，产出"实验设计图谱"：
- 论文设计了哪几组对照实验？每组在变什么变量（对到 var_dict 的 A1-G7）？
- 每组有哪些样本？总共多少不重复样本？
- 每个样本测了什么性能、在什么条件下测？

**先口头报给用户**：`识别到 N 组对照 / M 个样本 / K 个性能指标`，让用户确认抽全了再往下。

### Step 2 — 生成 extract_handoff.json + 写 notes/checklist

直接读主 Excel 4 sheet 列结构 + 现有 SS-1..6 范式，产出 `<paper_dir>/extract_handoff.json`（格式见下）。同时按规范写 notes.md + checklist.md。

### Step 3 — 跑脚本写入主 Excel

```
py ${CLAUDE_PLUGIN_ROOT}/skills/extract-paper-note/scripts/write_to_excel.py <paper_dir>/extract_handoff.json
```
脚本自动备份 → 写 3 个 sheet（大矩阵靠公式联动）。先 `--dry-run` 看落点再真写。

### Step 4 — dump 验证（不发文件）

dump 主 Excel 的 SS-X 行给用户看：Group 是 var_code、行数合理、配方填了、公式没坏、位置接上一篇。**不要 SendUserFile**（用户看行号会迷路，直接 dump 数据）。

## extract_handoff.json 格式

```json
{
  "paper_code": "SS-7",
  "论文清单": { "Title": "...", "Monomer": "... [ai]", "IL liquid": "... [ai]",
                "Monomer_Polar": "PEO ...", "Sample Count": 4, "Var Count": 5, ... },
  "样本数据": [
    {"Group": "A1", "Sample": "...", "Ionic Conductivity (mS·cm⁻¹)": "10"},
    {"Group": "A8", "Sample": "...", "Tensile Strength (MPa)": "0.38", "Toughness (MJ/m³)": "0.4"}
  ],
  "样本卡片": {
    "A1": {"取值序列": "SOS-N3 / SOS", "样本数": 2, "备注": "叠氮 vs 无叠氮"},
    "D1": {"取值序列": "25-100°C", "样本数": 4, "备注": "电导温度扫描"}
  }
}
```
- 性能列名 **原样照抄主 Excel**（含希腊字母/单位，如 `"Ionic Conductivity (mS·cm⁻¹)"`）
- 性能列**只放数字 + `[ai]`**（铁律：散文/多条件/范围进 notes，别塞主列）
- 论文清单值带 `[ai]` 标记（AI 抽的待审）
- 大矩阵不写（公式联动），json 里不需要 `大矩阵` 键

## Rules

1. **不动 ingest-paper 产出**（main.md/si.md/images/meta.yaml 只读）
2. **Group = var_code，不是长句**
3. **按变量取值展开行**（学 SS-1..6 范式）
4. **性能主列只放数字**（散文进 notes，没报的指标留空别硬填）。单位换算 / 主 Excel 缺列 / 定性演示信号的落点 → `references/data-mapping-spec.md`
5. **样本卡片只填空白卡 + 不碰公式格**；**大矩阵完全不写**
6. **每个数字尽量可溯源**（checklist 记它来自哪张图、进 Excel 哪行）
7. **review/perspective → STOP**
8. **notes 不重复 alt 已有描述**（详见 notes-template-spec.md）
9. **dump 验证不发文件**

详细 failure modes → `references/failure-modes.md`

## Examples（活示范）

实跑 SS-7 (2013) High Toughness 的真实产物：
- `papers/(2013) High Toughness.../extract_handoff.json` — 模型产出的交接文件
- `.../notes.md` — 实验目的/结构/过程/缺陷
- `.../checklist.md` — 11 图表逐条 + 入主 Excel 位置
- 主 Excel SS-7：论文清单 r8 / 样本数据 r106-115 / 样本卡片 r641 卡 / 大矩阵 r12 自动联动
