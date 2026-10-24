# arxiv-style 模板使用指南

一个简洁美观的 LaTeX 预印本（arXiv / TechRxiv / bioRxiv 等）模板，基于 [nips_2018.sty](https://media.nips.cc/Conferences/NIPS2018/Styles/nips_2018.sty) 改造而来，并在此基础上做了个性化定制（XeLaTeX 排版、网站配色、带个人网站图标的作者信息块）。

## 项目文件

| 文件 | 说明 |
| --- | --- |
| `arxiv.sty` | 核心样式文件，控制页面版式、字体、标题栏、摘要、关键词等外观 |
| `template.tex` | 示例正文，演示标题、作者、摘要、引用、图表等用法 |
| `references.bib` | BibTeX 参考文献库 |
| `icon.pdf` | 网站蓝色花朵图标，透明背景；显示于作者名左侧，点击跳转到个人网站 |
| `template.pdf` | 编译好的示例输出 |

## 环境要求

`template.tex` 使用了 `\usepackage{fontspec}`，因此：

- **必须使用 XeLaTeX 或 LuaLaTeX 编译**，不要用传统 `pdflatex`，否则 `fontspec` 会报错并终止编译。
- 页眉文字已清空，不再需要安装手写字体。
- 需要 `natbib`、`doi`、`booktabs`、`cleveref`、`hyperref`、`xcolor`、`colortbl`、`caption` 等常见 LaTeX 包。

## 与个人网站一致的配色

默认配色取自网站 `assets/css/site.css` 和 `assets/css/theme.css` 的日间主题。浅纸色背景搭配深蓝灰正文，标题和链接使用低饱和青绿；标题分隔线、摘要细线、图注与示例表格也使用同一套颜色。

| LaTeX 颜色名 | 色值 | 用途 |
| --- | --- | --- |
| `paperBackground` | `#F8F9F6` | 页面背景 |
| `paperInk` | `#263D43` | 正文、公式与较小层级标题 |
| `paperAccent` | `#416F74` | 标题、页眉、链接、图表编号 |
| `paperMuted` | `#637278` | 日期、页码、关键词与图注 |
| `paperSage` | `#87A79A` | 标题下划线与表格横线 |
| `paperLine` | `#D9E0DC` | 页眉、摘要与脚注细线 |
| `paperSurface` | `#EDF2ED` | 示例表头与图片占位背景 |

需要白底黑白打印时，将 `\usepackage{arxiv}` 改成 `\usepackage[print]{arxiv}`。正文和链接变为黑色，辅助元素使用灰阶。

颜色统一定义在 `arxiv.sty`，也可以在加载样式后覆盖。例如，保留彩色标题但使用纯白纸面：

```latex
\usepackage{arxiv}
\definecolor{paperBackground}{HTML}{FFFFFF}
```

自己的图表可以复用 `\textcolor{paperAccent}{...}`、`\rowcolor{paperSurface}` 等命令。表头底色在示例表格中显式设置，不会自动填充所有表格。

## 编译方法

推荐使用 `latexmk`：

```bash
latexmk -xelatex template.tex
```

或手动分步执行：

```bash
xelatex template
bibtex template
xelatex template
xelatex template
```

（多跑两次 `xelatex` 是为了让交叉引用、目录、参考文献编号正确刷新。）

## 快速上手：改成你自己的论文

1. **标题**：修改 `\title{...}`。
2. **日期**：默认使用编译当天日期；取消注释 `\date{...}` 可指定日期，或设为 `\date{}` 隐藏日期。
3. **作者信息**：修改 `\author{...}` 块中的姓名、单位、邮箱。作者名左侧通过 `\includegraphics` 显示 `icon.pdf`，外层 `\href{https://flowersfortuesday.com}{...}` 控制图标的点击跳转。图标直接由网站根目录 `favicon.ico` 中的蓝色花朵导出为 PDF，保留透明背景。复制模板到其他目录时需要一起复制 `icon.pdf`。
4. **页眉短标题**：
   - `\renewcommand{\shorttitle}{}` 已清空页眉正中的文字。若以后需要页眉，可改成 `\renewcommand{\shorttitle}{你的短标题}`。
   - `\renewcommand{\headeright}{...}` 和 `\renewcommand{\undertitle}{...}` 分别控制页眉右上角与标题下方的 "A Preprint" 字样，当前已清空；如需恢复，改回 `A Preprint` 或自定义文字即可。
5. **关键词**：`\keywords{关键词1 \and 关键词2 \and ...}`，不需要可直接删除该行。
6. **PDF 元数据**：`\hypersetup{...}` 中的 `pdftitle`、`pdfauthor`、`pdfsubject`、`pdfkeywords` 会写入生成的 PDF 属性，编译后可用 `pdfinfo template.pdf` 查看核对。
7. **摘要**：`\begin{abstract}...\end{abstract}`，示例中的 `\lipsum[1]` 是占位文本，替换为真实摘要后可删除 `\usepackage{lipsum}`。

## 引用文献

正文引用使用 `natbib` 语法：

```latex
\citet{key}   % 作者年份形式：Kour (2014)
\citep{key}   % 括号形式：(Kour, 2014)
```

参考文献条目写在 `references.bib` 中，正文末尾通过

```latex
\bibliographystyle{unsrtnat}
\bibliography{references}
```

引入。

### 投稿 arXiv 时的注意事项

arXiv 官方编译环境不会自动运行 `bibtex` 生成 `.bbl` 文件，所以投稿前需要把参考文献"内联"进 `.tex` 文件：

1. 本地正常编译一次（`xelatex` + `bibtex` + `xelatex` ×2），确认生成了 `template.bbl`。
2. 打开 `template.bbl`，把其中的 `\bibitem` 列表整段复制到 `template.tex` 里被注释掉的 `\begin{thebibliography}...\end{thebibliography}` 区块中，取消该区块注释。
3. 注释掉 `\bibliography{references}` 这一行（同时可以保留或删除 `\bibliographystyle`）。
4. 打包 `template.tex`（连同图片等资源，不需要再带 `references.bib`）提交 arXiv。

## 常见问题

- **页眉字体显示不对 / 退回默认字体**：检查是否用的是 `xelatex`/`lualatex`，以及所需字体是否已安装在系统中。
- **想要双栏排版**：本模板是单栏设计；如果需要双栏效果，可以参考 [preprint-template.tex](https://github.com/brenhinkeller/preprint-template.tex)。
- **需要多作者/多单位版式**：参考本项目上游 [kourgeorge/arxiv-style](https://github.com/kourgeorge/arxiv-style) 中基于 `authblk` 的写法。

## 许可

本项目基于 MIT License 开源，详见 `License.txt`。
