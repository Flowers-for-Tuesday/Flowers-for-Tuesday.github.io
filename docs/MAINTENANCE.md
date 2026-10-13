# Flowers for Tuesday 维护说明

这是一个适合 GitHub Pages 的静态博客。生成页面需要 Python 3.10+ 和 Node.js 18+；Markdown 解析依赖见 `requirements.txt`，公式排版组件已放入仓库，不需要运行 npm install。所有正文与公式在生成时完成排版，关闭 JavaScript 仍可阅读和导航。

## 快捷预览与发布

在 Windows 上，日常操作只需要项目根目录中的两个入口：

1. 双击 **`preview.cmd`**：自动准备项目环境、生成页面并打开浏览器。保持命令窗口开启，修改 Markdown、JSON、模板、CSS 或 JavaScript 并保存，页面会自动刷新。生成失败时，浏览器右下角和终端会显示错误；修正并保存后自动重试。关闭窗口或按 Ctrl+C 停止预览。
2. 确认本地效果后，双击 **`publish.cmd`**：检查远程分支、生成页面、运行检查，将项目中所有未被 `.gitignore` 排除的修改和删除一起提交并推送到 `origin/main`，随后等待 GitHub Pages 确认部署。显示“部署成功”后，再打开线上网站检查。

本机需要已安装 Python、Node.js 和 Git，并具有该远程仓库的推送权限。第一次运行会联网安装 Python 依赖到项目内的 `.venv/`，以后自动复用；无需手动激活虚拟环境。发布失败时窗口会保留错误信息，已有文件和本地提交不会被撤销。

也可以在项目目录中运行以下命令（跨平台）：

```powershell
python scripts/manage.py preview --open
python scripts/manage.py build
python scripts/manage.py publish -m "更新笔记与页面样式"
python scripts/manage.py status
```

预览地址默认是 `http://127.0.0.1:8000`，仅本机可访问；端口已被占用时使用 `python scripts/manage.py preview --open --port 8001`。`status` 只查询当前提交的部署状态，不创建提交或推送。发布默认最多等待 5 分钟，超时后 GitHub 会继续运行，可稍后查询；`--timeout 600` 可延长等待，`--no-wait` 可只推送、不等待部署结果。返回码 `0` 表示成功（使用 `--no-wait` 时仅表示推送成功），`1` 表示失败，`2` 表示代码已推送但部署状态尚未确认。

如果远程 `main` 有本地尚未包含的提交，发布工具会停止，请先处理本地修改并同步远程。它不会强制推送。网络中断后可再次运行发布命令，已有提交会继续推送，没有新改动时不会创建空提交。预览和发布可以同时开启，文件生成会依次执行。

### 在 VS Code 中调试

用 VS Code 打开整个项目文件夹后：

- 按 **F5**：启动本地预览，并在 Edge 中打开网站，可在 `assets/js/` 内设置断点；前端样式可在浏览器开发者工具中查看。
- 按 **Ctrl+Shift+B**：重新生成页面。
- 通过 **终端 → 运行任务 → 网站：提交并部署**：输入本次更新说明并发布。

浏览器开发者工具中的临时样式调整不会自动保存到源文件；确认效果后，把改动写回 CSS。结束浏览器调试后，如需关闭预览，在 VS Code 中终止“网站：本地预览”任务。修改 `scripts/dev.py`、`scripts/manage.py` 或依赖配置后，需要重启预览。

## 文件结构

```text
README.md               入场动画的两行原文
preview.cmd             Windows 双击预览入口
publish.cmd             Windows 双击提交与部署入口
.vscode/                本地预览、生成、发布任务与 Edge 调试配置
content/site.json       首页引文、个人介绍、账号链接、歌曲、论文数据
content/note-categories.json 笔记分类的显示名称
templates/base.html    共用页头、导航、页脚
scripts/build.py        静态页面生成入口
scripts/notes.py        扫描 Markdown、分类、生成目录与正文
scripts/render-math.cjs 构建时排版公式（KaTeX）
scripts/manage.py       自动准备环境、检查、提交、推送、查询部署
scripts/dev.py          监听源文件修改与浏览器自动刷新
assets/css/site.css     样式与响应式布局
assets/js/site.js       手机导航、可跳过的入场动画
assets/css/notes.css    笔记目录与正文样式
assets/js/notes.js      笔记搜索、分类筛选
assets/vendor/katex/   公式排版组件、样式、字体与授权文件
assets/fonts/          东京街角的小浪漫网页字体
assets/images/         avator.jpg、about.jpeg 原图
files/notes/           笔记源文件、封面、插图与附件
files/music/           歌曲音频、歌词、乐谱
files/gallery/         摄影作品原图
files/publications/    公开论文附件
index.html             生成的主页
about/index.html       生成的个人介绍
files/notes/分类/笔记/main.md 笔记源文件（同目录放封面与插图）
note/index.html        自动生成的分类目录
note/分类/笔记/index.html 自动生成的阅读页面
music/index.html       生成的原创音乐列表
gallery/index.html     生成的摄影作品列表
publication/index.html 生成的论文列表
404.html               找不到页面时的提示
favicon.ico            原有网站 logo
```

## 编辑与预览

About 页支持多篇介绍，在 `content/site.json` 的 `about.entries` 数组中维护，每篇包含 `subtitle`（时间、地点副标题）和 `paragraphs`（正文段落数组）。复制数组中的一项即可新增一篇；按数组顺序显示，默认打开第一篇。保存后重新生成页面即可生效。

```json
"entries": [
  {"subtitle": "2025/12/7，夜，于北京", "paragraphs": ["第一篇的第一段。", "第一篇的第二段。"]},
  {"subtitle": "2026/10/12，于北京", "paragraphs": ["第二篇的正文。"]}
]
```

正文上方的左右箭头可循环切换文章，并显示当前篇数；按钮获得焦点时也可用键盘左右方向键切换。只有一篇时按钮置灰。关闭 JavaScript 时所有文章按顺序展示。下方的 Background 学习经历由所有文章共用。

About 页的学习经历在 `content/site.json` 的 `about.background` 数组中维护，按数组顺序显示为相连的时间线。添加经历时复制一项，填写 `years`（年份）、`school`（学校）、`program`（专业或项目），无需修改 HTML 或手动添加连接线。可选的 `logo` 填写相对项目根目录的图片路径，例如 `assets/images/pku-logo.png`；省略该字段时只显示经历内容。

学校标识保存在本地：北京大学校徽来自 https://www.pku.edu.cn/pku_logo_red.png ，Perimeter Institute 标识来自 https://landing.perimeterinstitute.ca/hubfs/Stacked_Perimeter%20English%20Logo%20Black-908x301.png 。

首页个人区域的账号导航在 `social_links` 中维护，每项包含 `label`（显示名称）与 `url`（账号链接）；页脚复用同一份配置。首页链接竖向排列，末尾的 Email 读取顶层 `email` 字段，并显示 `assets/icons/email.svg` 邮箱图标。
可选的 `icon` 字段支持 `github`、`zhihu`、`bilibili`，对应 `assets/icons/` 下的 SVG 图标；生成时内嵌到 HTML，使用 `currentColor` 随链接文字变色，无需额外加载图标文件。不设置 `icon` 时只显示文字链接。

根据修改目的编辑以下源文件：

| 想修改的内容 | 对应文件 |
| --- | --- |
| 个人介绍、个人账号、歌曲、摄影作品和论文 | `content/site.json` |
| 主页引文、页脚文字 | `content/site.json` 中的 `home`；`quote` 数组每项显示为一行 |
| 主页栏目卡片配图 | `assets/images/note.jpg`、`music.jpg`、`gallery.jpg`、`publication.jpg` |
| 笔记正文、公式与图片 | `files/notes/分类/笔记/main.md` 及同目录图片 |
| 笔记分类的显示名称 | `content/note-categories.json` |
| 导航栏、共用页头和页脚 | `templates/base.html` |
| 字体大小、间距、颜色、页面布局 | `assets/css/site.css`、`assets/css/notes.css` |
| 入场动画、卡片交互、移动端导航、笔记筛选 | `assets/js/site.js`、`assets/js/notes.js` |
| 入场的两行文字 | `README.md` |
| 主页与各栏目的页面结构 | `scripts/build.py`；笔记页面结构在 `scripts/notes.py` |

首页桌面端左侧显示圆形头像、姓名、引文和个人账号链接，右侧为手风琴式图片卡片：默认展开 Note，悬停或键盘聚焦其他分类时展开对应图片，其余三张收窄为带竖排分类文字的缩略图。展开图保持原始比例，宽屏下与左侧个人区域等高，四张卡片始终共同铺满右栏；窄屏会适当降低图片高度。鼠标移出后保留当前展开项。手机端个人信息在上方，卡片在下方，轻触收起的卡片展开，再次轻触进入栏目。键盘可用 Tab、左右方向键、Home / End 切换焦点，Enter 进入栏目；系统开启“减少动态效果”时关闭过渡动画。卡片配图与栏目同名，可直接替换 `assets/images/` 中对应的 JPG。引文读取 `home.quote`，同时用作首页的描述元数据。开场动画的文字仍独立读取 `README.md`。

推荐用快捷预览工具监听修改：

```powershell
python scripts/manage.py preview --open
```

浏览器访问 `http://127.0.0.1:8000`。停止预览按 Ctrl+C。
修改应保存在源文件中，直接修改生成的 `index.html` 等文件会在下次生成时被覆盖。发布工具会自动重新生成并提交 HTML。右下角的本地预览状态与刷新脚本只在预览服务器中临时加入，不会写入生成文件或部署到线上。

## 添加 Markdown 笔记

沿用示例文件夹即可，不需要手工登记笔记列表：

```text
files/notes/
  Computational Physics/
    PIMC/
      main.md
      cover.jpeg
      1.png
      2.png
    HF＆Post HF/
      main.md
      cover.jpeg
      1.png
  新的分类/
    新的笔记/
      main.md
```

每个 Markdown 文件会在 `note/` 下的对应目录生成阅读页，例如 `files/notes/Computational Physics/PIMC/main.md` 生成 `note/Computational Physics/PIMC/index.html`。分类子目录中的 `main.md` 或 `index.md` 生成 `index.html`，其他名称如 `example.md` 生成 `example.html`。同一目录不要同时放 `main.md` 和 `index.md`，以免输出重名。第一层目录默认作为分类，深层目录用于组织主题。`note/` 只存放生成结果，日常编辑统一在 `files/notes/` 中进行；已有笔记网页地址保持不变。

文件开头支持 YAML 元数据（均可选）：

```yaml
---
title: "笔记标题"
date: 2026-10-10 18:30
cover: cover.jpeg
summary: "可选：在笔记列表的标题下显示的简短介绍，不会插入正文。"
category: "Computational Physics" # 省略时使用第一层文件夹名称
draft: false # true 时不生成页面、不进入目录
---
```

无元数据时从一级标题或文件名推断标题。文章按日期从新到旧排列，没有日期时显示“未标注日期”。直接放在 `files/notes/` 根目录的笔记属于“未分类”；其中 `index.md` 生成 `note/index-note.html`，避免覆盖目录页。分类会随笔记自动出现，也可在 `content/note-categories.json` 配置中文名称。现有“Computational Physics”显示为“计算物理”。列表展示封面、日期、标题、可选的 summary 和阅读入口。

`summary` 填写在 Markdown 文件开头的 YAML 元数据中，按纯文本显示在预览卡片的标题下，并参与列表搜索；不会插入文章标题区或正文。省略、留空或仅填写空白时不显示摘要，也不会自动截取正文填充卡片。较长内容可用 YAML 的 `summary: >-` 分行填写。页面描述元数据仍可使用摘要，未填写时沿用自动提取的描述。

支持标题、段落、粗体、斜体、引用、列表、任务列表、表格、代码高亮、脚注、图片与链接。原始 HTML 作为文本展示。正文图片使用相对路径，例如 `![图示说明](1.png)`；含空格的路径用 `![说明](<figure 1.png>)`。建议填写图片说明供辅助阅读。跨笔记链接可写 `[另一篇笔记](../另一篇/main.md)`，生成器自动转换为网页链接，并对空格与中文路径编码。

公式支持 `$...$` 与 `$$...$$`（包括矩阵、多行 aligned 等 KaTeX 支持的语法）。公式在生成时转换为 HTML 与 MathML，字体由本站提供；长公式可独立横向滚动，不会撑宽手机页面。错误的公式或缺失的本地图片会给出构建错误，避免静默发布损坏页面。

正文页提供章节目录、分类返回、Markdown 下载及同类笔记推荐；目录页支持分类与全文关键词搜索。关闭 JavaScript 时所有已发布笔记和分类仍可直接浏览。

开启快捷预览时，修改 Markdown 或资源会自动生成；也可手动运行 `python scripts/manage.py build`。自动生成的页面不应手动编辑；移除源文件后重新生成，会根据 `note/.generated-pages.json` 清理对应的旧阅读页，原始文件不受影响。

## 添加歌曲、摄影作品与论文

在 `content/site.json` 的对应数组添加对象，将附件放入对应的 `files` 子目录，然后重新生成页面。

笔记附件与 Markdown 源文件一起放在 `files/notes/` 中，可继续使用相对路径引用同目录图片或其他笔记。生成器会自动换算网页中的图片地址、跨笔记链接和 Markdown 下载地址。

检查生成器：

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

歌曲（添加到 `music`，`audio` 可选）：

```json
{
  "title": "歌曲标题",
  "date": "2026-10-10",
  "description": "这首歌的创作说明。",
  "audio": "../files/music/example.mp3",
  "links": [{"label": "歌词与乐谱", "url": "../files/music/example.pdf"}]
}
```

摄影作品（添加到 `gallery`，照片放入 `files/gallery/`，点击照片可查看原图）：

```json
{
  "title": "猎户座星云",
  "date": "2026-10-11",
  "description": "拍摄地点、器材与曝光记录。",
  "image": "../files/gallery/orion-nebula.jpg",
  "alt": "星空中的猎户座星云"
}
```

`alt` 可省略，默认使用作品标题；`date`、`description` 和 `links` 也可省略。当前 `gallery` 为空时显示占位内容，不会添加示例照片。

论文（添加到 `publications`）：

```json
{
  "title": "论文标题",
  "date": "2026",
  "description": "作者列表 · 期刊或会议名称",
  "links": [
    {"label": "DOI", "url": "https://doi.org/实际的论文DOI"},
    {"label": "PDF", "url": "../files/publications/example.pdf"}
  ]
}
```

以上仅为格式示例，不会展示在网站上。列表按 JSON 中的顺序显示，最新内容可放在数组最前面。

## 入场动画与字体

生成脚本读取 README 前两行非空文本。动画在当前浏览器标签页首次访问主页时显示，可点击“进入主页”或按 Escape 跳过；页脚“重看开场”可重播。系统开启“减少动态效果”时不会自动播放。无 JavaScript 时不会遮挡正文。

字体来自本机安装的“东京街角的小浪漫”，已转换为 WOFF2，保留全部字形并优先使用已安装的同名字体，未安装字体的设备会读取仓库中的文件。

## GitHub Pages

远程仓库：<https://github.com/Flowers-for-Tuesday/Flowers-for-Tuesday.github.io>

推荐使用 GitHub 仓库 **Settings → Pages → Build and deployment → Source → GitHub Actions**。`.github/workflows/pages.yml` 会在每次推送至 `main` 后安装依赖、检查生成器、扫描 Markdown 并部署。以后只需上传 Markdown 和同目录图片，不需要手动登记或生成 HTML。切换来源后，可在 Actions 的 **Build and publish website → Run workflow** 立即运行一次。

如果仍使用 **Deploy from a branch → main → /(root)**，本次已提交的生成页面可照常发布；后续更新需要本地生成并提交 HTML。工作流会完成构建并保存 `github-pages` 产物，但在来源不是 GitHub Actions 时跳过部署，以免与已有发布方式冲突。

`publish.cmd` 兼容以上两种发布方式，会自动生成并提交 HTML；部署状态检查会匹配本次提交，只有 Pages 发布任务成功才显示“部署成功”，构建成功但部署被跳过不会被误报。

网站地址为 <https://flowers-for-tuesday.github.io/>。发布包通过 `scripts/package_site.py` 生成，只包含网站目录，不包含本地预览工具、构建依赖或 Git 数据。

布局参考 <https://davidtong.org/> 的顶部导航和左图右文结构，所有网站代码为本项目实现。
