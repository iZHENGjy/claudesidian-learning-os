# Failure modes

| 模式 | 触发 | 处理 |
|---|---|---|
| `main.md` 不存在 | 没跑 ingest-paper | STOP，提示用户先跑 `ingest-paper`，**不擅自启动** |
| `images/` 还是 hash 命名 | ingest-paper vision 没完成 | STOP，提示回去补完 vision 流程 |
| 主 Excel 找不到 | 用户改了路径 | STOP，让用户提供新路径 |
| 论文类型 = review/perspective | 模型读 abstract 判定 | STOP："综述论文走另外流程，本 skill 不处理" |
| 主 Excel 被打开（PermissionError）| 用户开着 Excel | 报错，**不删** handoff json / notes / checklist；提示用户关 Excel 重试。可先 `--dry-run` 看落点 |
| 性能值没有对应主 Excel 列 | 论文测了表里没有的指标（如 tan δ）| 不硬塞主列；写进 notes，checklist 标 ✗ + 说明缺列 |
| 某指标论文没直接报 | 如只报 G′ 没报 Young's | 主列**留空**，别用推算值硬填；推算说明进 notes |
| 数字没法溯源到图/表 | 模型读不准来源 | checklist 该图标"部分/✗"，不强标精确出处 |
| contributes_to slug 不在大纲词表 | 模型编了新 topic | notes frontmatter 留 `_unknown_topic` 标记 + 警告，**不丢弃** |
| 样本卡片代号历史错位 | 主 Excel 既有混乱 | `find_card` 自动选第一张全空白卡，不覆盖任何现有数据（已内建） |
| 样本卡片用完（无空白卡）| 论文数 > 预留卡数 | 脚本 `write_card` 返回警告"找不到空白卡"，提示用户在主 Excel 加卡片模板 |
| 想手写大矩阵 | 误以为要填 | **绝不**——大矩阵全公式联动，手写破坏 SUMIFS/IF；填好样本卡片即可 |
| Group 填了长句不是 var_code | 违反铁律 | 重新对到 var_dict 的 A1-G7 编码；长句描述放 Group_Notes 列 |
| 同一篇重跑 | 主 Excel 已有该 SS-X 行 | 先用 openpyxl 清掉旧 SS-X 行（样本数据 + 空白卡代号）再重写，避免重复 append |
| 写入位置跳到空白行之后 | 用了 `max_row` 而非真数据行 | 脚本 `last_data_row` 从下往上找真数据行（已内建，别改回 max_row） |
| **si.md 是 main.md 的副本** | si.pdf 与 main.pdf md5 相同（SI 下载阶段拿错文件）| SI 表数据（Table S1/S3 等）全缺 → 缺值标 `[缺-SI未抽到]`，提示用户重新下载真 SI 重抽。**检测**：`md5sum main.pdf si.pdf` 相同即是 |
| meta.yaml DOI 错（mineru 抽错）| ingest-paper 残留 | 警告但不阻塞；用户后期手动补 |

## 重跑清理示例（同篇重抽前）

```python
from openpyxl import load_workbook
wb = load_workbook(MASTER)
ws = wb["样本数据"]
for r in range(ws.max_row, 2, -1):
    if ws.cell(r, 2).value == "SS-7":
        for c in range(1, ws.max_column + 1):
            ws.cell(r, c).value = None
wb.save(MASTER)
```
论文清单 / 样本卡片同理（卡片清代号 + 变量表 E/F/G）。
