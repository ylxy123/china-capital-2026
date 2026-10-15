# 编译、复核与复现范围

## 阅读与排版

根目录 PDF 为 2026-10-15 交付的扩充修订版，共 143 页。它与 `.tex` 的原始对应关系记录在 `research/deliverable_sha256.json` 和 `research/native_pdf_export.json`，开源整理保留了这两个文件的原始字节。

安装 README 中列出的 TeX 依赖后运行 `make pdf`。Makefile 使用 XeLaTeX 和 latexmk 自动进行目录与交叉引用所需的多轮编译，输出到 `build/`。不同 TeX/字体版本可能使分页或 PDF 字节变化，因此本项目不承诺跨环境逐字节一致；请比较内容与渲染结果。

## 结构与交付完整性

`make check` 执行扩充版结构检查和原始交付文件 SHA-256 检查。结构检查包含 12 个主章、12 幅图表、291 个段落对应、引文键、交叉引用、环境闭合和重复段落。它会更新 `research/structural_validation.json`。哈希检查针对本次发布快照；修改书稿后不应仍声称与旧 PDF 对应。

## 重建扩写过程

以下步骤会覆盖根目录 `.tex` 及对应台账，建议在临时克隆中运行：

```sh
python3 research/scripts/assemble_expansion.py
python3 research/scripts/verify_expansion.py
python3 research/scripts/finalize_expansion_research.py
```

组装使用 `research/expansion/` 的原稿、扩写笔记及修订表。复算和来源台账不是新调查数据，结构可复现不表示其中全部经验判断都已独立复核。

## 脚本边界

| 脚本 | 用途与限制 |
| --- | --- |
| `verify_expansion.py` | 当前扩充版检查；Python 3.10+ 标准库 |
| `assemble_expansion.py` | 从底稿重新组装，会覆盖书稿 |
| `finalize_expansion_research.py` | 更新扩充版研究台账 |
| `build_registry.py`、`build_data_and_figures.py`、`build_bibliography.py`、`build_review_tables.py`、`verify_manuscript.py` | 初版历史流程；不应连续运行来重建扩充版 |
| `compile_native.py` | 历史应用内编译工具，需要显式设置应用桥接环境；公共构建使用 `make pdf` |
| `capture_editor_pdf.py` | Linux 历史应用输出捕获，需要运行中的应用与可选 PyMuPDF；公共构建不需要 |

无须原作者的本地目录、应用会话或第三方下载缓存即可从当前 `.tex` 编译书稿。历史应用工具不属于普通构建入口。

## 数据核查

`research/data/key_data.csv` 区分观察值、研究估计、审计记录与假设算例；`calculation_checks.json`、`debt_scenarios.csv` 保存已列明假设下的算术结果。来源访问或引用状态是历史记录，不代表今天链接仍可访问。原始资料不随仓库重新分发，需依来源索引独立取得。

## 本次开源验证

本次验证详情见 `docs/RELEASE.md`。本仓库未通过自动检查宣称同行评审、全国因果识别或全部事实无误。
