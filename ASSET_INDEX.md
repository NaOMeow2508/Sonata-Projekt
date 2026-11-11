# 项目资产索引

记录日期：2026-11-11。路径仅用于定位，不代表授权移动、修改或上传。
本资料库未复制源码、图片、PDF 或完整剧本。

## 源码与基线
| 资产 | 绝对路径 | 来源与确认状态 |
| --- | --- | --- |
| App 源码 | C:\Users\MaNin\Documents\Codex\2026-10-13\web-app-mvp-react-typescript-vite\outputs\learning-app | 历史聊天提供线索，后经直接源码检查及基线验证确认存在 |
| 网站源码 | C:\Users\MaNin\OneDrive\OneDrive - Personal\学术文件夹\游戏设计\surprise from Sonata 网站 | 当前工作区直接检查及基线验证确认存在 |
| 项目资料库 | C:\Users\MaNin\Documents\Sonata-Project-Hub | 开发者本轮指定，独立知识库 |

App 关键入口为 index.html、src/main.tsx、src/App.tsx；内容为 src/data/content.ts；进度服务为 src/services/learningProgress.ts。
网站入口为 index.html；项目介绍为 projekt-sonata.html；共享样式和脚本位于 assets。
基线 Commit 与测试结果见 PROJECT_STATUS.md。

## 备份与报告
备份根目录：
C:\Users\MaNin\Sonata-Backups\2026-11-11-115831-baseline-4341acbf

- learning-app-source：App 基线前源码副本，24 个文件。
- portfolio-source：网站基线前副本，15 个文件。
- reference-artifacts/Kleine-Welten.html：历史分享产物，1 个文件。
- manifests/sha256-manifest.json：逐文件 SHA-256、源路径与备份路径。
- manifests/file-list.csv：文件清单。
- manifests/git-baselines.json：两仓库基线提交与最终 Git 状态。
- manifests/app-validation.json、app-test-output.txt、app-build-output.txt、app-startup.json：实际执行记录。
- verification-report.md：按执行顺序追加的报告；早期阻塞已由后续完成记录更新。

以上 40 个备份文件已经核验。备份位于同一磁盘，不等同于异地灾备。不要覆盖现有备份。
原分享文件位于：
C:\Users\MaNin\Documents\Codex\2026-10-13\web-app-mvp-react-typescript-vite\outputs\Kleine-Welten.html

## 尚未导入的外部资料
基础目录：
C:\Users\MaNin\OneDrive\OneDrive - Personal\学术文件夹\游戏设计\融合项目游戏设计

| 文件或项目 | 已检查内容 | 确认状态 |
| --- | --- | --- |
| A1单词表.pdf | 文件名及存在性 | 正文未审阅；待导入、版本确认 |
| 融合课程框架.pdf | 文件名及存在性 | 正文未审阅；待导入、来源确认 |
| Datengrundlage_Integrationskurse_Kinder_DE.pdf | 文件名及存在性 | 正文与证据质量未审核 |
| Sonata_Logo_Blue_Eyes.png | 文件名及存在性 | 未导入；与网站 Logo 的一致性未校验 |
| 小小世界（暂定）.scriv | 项目入口与目录标题 | 不是已验证的 App 代码；正文未导入 |

Scrivener 项目包含：
- 小小世界（暂定）.scrivx：目录中有“设定手册”“AI动画生成分镜和提示词”“EP01 垃圾分类｜Sonata und die sprechenden Dinge”。
- 小小世界（暂定）-NyxNote_Kairos.scrivx：目录中有“项目设计”“故事大纲及设定（第一版）”“EP01.”。

两入口位于同一个 .scriv 包，版本关系尚未确认，不能视作独立备份。
网站 assets/sonata-logo.png 已存在；assets/brand-placeholder.svg 为保留的旧占位图。App 当前图形为 src/components/Lumo.tsx 中的 SVG，不是 Sonata 角色。

## 来源规则
开发者本轮指令确认长期方向；直接源码读取确认实现；实际执行日志确认验证结果。
历史聊天、文件名、目录标题只用于定位，不足以确认正文、教学质量或功能完成。
后续导入资料需记录提供者、原始路径、版本、确认状态及使用许可，不覆盖来源文件。

## E01-002 — 已完成的文字导入
导入时间：2026-11-11T12:50:29+01:00
本节为最新追加状态，更新前文“正文未导入”“版本关系尚未确认”等建库时快照；旧记录保留，不覆盖。
当前工作入口已由开发者确认为无后缀 .scrivx；本次原目录中未发现后缀入口。
| 资料 | Hub 路径 | 状态 |
| --- | --- | --- |
| 第一季核心设定 | [03_Visual_Assets/Sonata/Season01_Story_Bible_DRAFT.md](03_Visual_Assets/Sonata/Season01_Story_Bible_DRAFT.md) | DRAFT |
| 第一集六场剧本 | [02_Episodes/E01_Waste_Sorting/Script/E01_Dialogue_DE_ZH_DRAFT.md](02_Episodes/E01_Waste_Sorting/Script/E01_Dialogue_DE_ZH_DRAFT.md) | DRAFT |
| 15段开场动画提示词 | [02_Episodes/E01_Waste_Sorting/Prompts/E01_Opening_Animation_Prompts_DRAFT.md](02_Episodes/E01_Waste_Sorting/Prompts/E01_Opening_Animation_Prompts_DRAFT.md) | DRAFT |
| 教育 App 设计摘要 | [06_Collaboration/Tasks/Education_App_Concept_DRAFT.md](06_Collaboration/Tasks/Education_App_Concept_DRAFT.md) | DRAFT |
| 第一版历史设定 | [06_Collaboration/Decisions/Legacy_Season01_Outline_REFERENCE.md](06_Collaboration/Decisions/Legacy_Season01_Outline_REFERENCE.md) | REFERENCE |

来源关系：[Scrivener_Source_Relationship.md](06_Collaboration/Decisions/Scrivener_Source_Relationship.md)。
完整性报告：[E01-002_Import_Report.md](06_Collaboration/Handoffs/E01-002_Import_Report.md)。
源路径、UUID、SHA-256 与时间：[E01-002_Import_Manifest.json](06_Collaboration/Handoffs/E01-002_Import_Manifest.json)。
仅导入文字；核心设定的 1 张嵌入图片未提取，PDF、图片及其他媒体未导入。
