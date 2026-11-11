# ASSET-001 — 增量资产索引工具

状态：实现完成；首次正式资产扫描待开发者确认。
日期：2026-11-11（Europe/Berlin）

## 目标

使用本地 Python 标准库生成增量资产清单。默认预览；只有传入 `--apply` 才写入 `assets.csv`、`change_log.csv` 和 `ASSET_INDEX.md` 的 ASSET-001 生成区。

## 数据与行为

- `assets.csv` 保存 asset_id、相对路径、文件名、SHA-256、大小、修改时间、确认状态和备注。
- `change_log.csv` 记录新候选资产的添加事件。
- 新资产状态为 `CANDIDATE`。已存在记录的 asset_id、status 和 notes 保留；同路径文件变化时只刷新观测到的哈希、大小与时间。
- 不因重命名或重复哈希自动合并。相同哈希只输出提示；未匹配的路径不推断删除或重命名。
- 索引手工内容位于生成区之外，工具只替换已标记区；首次写入时在文件末尾增加生成区。
- 默认扫描当前目录，默认输出到当前目录；隐藏路径和 `__pycache__` 默认跳过。

## 使用

```powershell
python tools/update_asset_index.py --root . --output-dir .
python tools/update_asset_index.py --root . --output-dir . --apply
```

首次扫描只查看预览；未获开发者确认前不得添加 `--apply`。

## 边界

此工具仅用于项目资料库，不修改 App、网站或 Scrivener。ASSET-001 详细先前方案文本在本轮资料中未找到；实现以本轮明确要求为准。
