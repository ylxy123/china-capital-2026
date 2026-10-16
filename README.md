# 新时代资本论

**2026年中国大陆的生产、分配与风险** · 姚林翔宇 · 扩充修订版

[![Content: CC BY-SA 4.0](https://img.shields.io/badge/content-CC_BY--SA_4.0-blue.svg)](LICENSE-CONTENT)
[![Code: MIT](https://img.shields.io/badge/code-MIT-green.svg)](LICENSE-CODE)

[阅读 PDF](china-capital-2026.pdf) · [下载 PDF](https://github.com/ylxy123/china-capital-2026/raw/refs/heads/main/china-capital-2026.pdf) · [LaTeX 源码](china-capital-2026.tex) · [复现说明](docs/REPRODUCIBILITY.md) · [参与贡献](CONTRIBUTING.md)

本书围绕四个问题展开：财富怎样生产，资源与决策由谁控制，收益怎样分配，风险最终由谁承担。通过生产账、权利与收入账、再生产与风险账，将企业、劳动、土地、金融、家庭与公共服务放在同一分析框架中。

本书是作者姚林翔宇历时数年研究与撰写的原创研究专论，并非马克思《资本论》的译本或改写。仓库开放书稿、排版源码、研究脚本、来源索引、数据复算与段落审计资料，方便阅读、质疑、复核与改进。

## 版本与研究边界

- 版本：扩充修订版；首次开源日期：2026-10-15。
- 研究范围：中国大陆；资料发布截止：2026-10-14。
- 当前 PDF：143 页；严格正文计数：119,168 个汉字。
- 结构：导论、12 章、结语、3 个附录及参考文献；12 幅图表，正文引用 50 项来源。
- 未进行新问卷、访谈或全国因果回归，未取得受限微观数据库。公开统计、研究估计、预测、机制推论和假设算例在书中分别标明。
- WID 相关原值存在未解释的一致性问题，仅保留作来源审计，不用于精确比较；详见[问题台账](research/sources/issues.csv)。

上述信息对应随仓库提供的 PDF。结构检查通过不等于全部事实或理论已经得到独立验证。

## 内容目录

1. 中国经济的制度结构
2. 商品、价值与价格
3. 劳动、技术与剩余
4. 企业、所有权与控制权
5. 货币、信用与资本循环
6. 土地、住房与地方财政
7. 家庭与社会再生产
8. 收入、财富与社会位置
9. 平台、数据与人工智能
10. 制造业与全球联系
11. 积累、失衡与危机
12. 制度改进的条件与代价

## 快速开始

直接阅读 [PDF](china-capital-2026.pdf)，无需安装软件。

复核书稿结构需要 Python 3.10 或更新版本，仅使用标准库：

```sh
git clone https://github.com/ylxy123/china-capital-2026.git
cd china-capital-2026
python3 research/scripts/verify_expansion.py
python3 scripts/check_release.py
```

编译需要 XeLaTeX、latexmk、ctex、Fandol 字体及 PGFPlots。Ubuntu / Debian 可安装：

```sh
sudo apt-get update
sudo apt-get install latexmk texlive-xetex texlive-lang-chinese texlive-latex-extra texlive-pictures
make pdf
```

输出为 `build/china-capital-2026.pdf`，不会覆盖根目录已发布 PDF。图表和参考文献已内嵌于单个 `.tex` 文件，无须外部图片或 BibTeX 数据库。具体复现范围与历史脚本限制见[复现说明](docs/REPRODUCIBILITY.md)。

## 仓库内容

| 路径 | 用途 |
| --- | --- |
| `china-capital-2026.pdf` / `.tex` | 完整书稿与排版源码 |
| `research/scripts/` | 组装、核查、数据与文献整理脚本 |
| `research/data/` | 使用的数据记录与复算结果 |
| `research/sources/` | 来源索引、概念、文献评议与问题台账 |
| `research/expansion/` | 扩写底稿、段落对应、候选命题与修订记录 |
| `research/deliverable_sha256.json` | 原始交付源码与 PDF 的 SHA-256 |
| `docs/` | 复现和版本说明 |

第三方网页、论文全文、下载缓存、本机日志与原始打包文件未纳入公开仓库；原始出处可从来源索引查找。

## 引用

> 姚林翔宇. 新时代资本论：2026年中国大陆的生产、分配与风险. 扩充修订版, 2026. https://github.com/ylxy123/china-capital-2026

机器可读引用见 [CITATION.cff](CITATION.cff)。引用具体论断时，请附章节或段落锚点；复用数据时同时引用原始来源及其统计口径。

## 授权

- **书稿、LaTeX 书稿源码、原创图表与研究文档：**[CC BY-SA 4.0](LICENSE-CONTENT)。允许分享、修改及商业使用，须署名、提供协议链接、标明修改，并按相同协议分享改编内容。
- **Python 等程序代码：**[MIT](LICENSE-CODE)。允许使用、修改及商业使用，须保留版权与许可声明。
- **第三方引文与数据：**遵循原权利人的条款，不因收录或引用而获得本项目的重新授权。

具体边界见 [LICENSE](LICENSE) 和 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## 纠错与贡献

欢迎通过 [Issues](https://github.com/ylxy123/china-capital-2026/issues) 提交文字、数据、来源、论证或编译问题。请提供章节、页码或 `arg:Pxxx` 段落锚点，以及可核对的出处。提交修改前请阅读[贡献指南](CONTRIBUTING.md)。

## English

*Capital in a New Era: Production, Distribution, and Risk in Mainland China (2026)* is a Chinese-language research monograph by Linxiangyu Yao, the result of several years of research and writing. This repository contains the complete PDF, self-contained LaTeX manuscript, Python research scripts, source registers, and calculation/audit tables. Original content is licensed under CC BY-SA 4.0; software is licensed under MIT. Third-party material retains its original rights. See the reproducibility guide for build instructions and research limitations.
