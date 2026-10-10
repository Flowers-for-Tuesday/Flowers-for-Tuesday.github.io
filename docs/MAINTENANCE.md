# Flowers for Tuesday 维护说明

这是一个适合 GitHub Pages 的静态博客。生成页面需要 Python 3.10+ 和 Node.js 18+；Markdown 解析依赖见 `requirements.txt`，公式排版组件已放入仓库，不需要运行 npm install。所有正文与公式在生成时完成排版，关闭 JavaScript 仍可阅读和导航。

## 文件结构

```text
README.md               入场动画的两行原文
content/site.json       个人介绍、账号链接、歌曲、论文数据
content/note-categories.json 笔记分类的显示名称与简介
templates/base.html    共用页头、导航、页脚
scripts/build.py        静态页面生成入口
scripts/notes.py        扫描 Markdown、分类、生成目录与正文
scripts/render-math.cjs 构建时排版公式（KaTeX）
assets/css/site.css     样式与响应式布局
assets/js/site.js       手机导航、可跳过的入场动画
assets/css/notes.css    笔记目录与正文样式
assets/js/notes.js      笔记搜索、分类筛选
assets/vendor/katex/   公式排版组件、样式、字体与授权文件
assets/fonts/          东京街角的小浪漫网页字体
assets/images/         avator.jpg、about.jpeg 原图
files/notes/           笔记附件
files/music/           歌曲音频、歌词、乐谱
files/publications/    公开论文附件
index.html             生成的主页
about/index.html       生成的个人介绍
note/分类/笔记/main.md  笔记源文件（同目录放封面与插图）
note/index.html        自动生成的分类目录
note/分类/笔记/index.html 自动生成的阅读页面
music/index.html       生成的原创音乐列表
publication/index.html 生成的论文列表
404.html               找不到页面时的提示
favicon.ico            原有网站 logo
```

## 编辑与预览

About 页的个人账号导航在 `about.navigation` 中维护，每项包含 `label`（显示名称）与 `url`（账号链接）。
可选的 `icon` 字段支持 `github`、`zhihu`、`bilibili`，对应 `assets/icons/` 下的 SVG 图标；生成时内嵌到 HTML，使用 `currentColor` 随链接文字变色，无需额外加载图标文件。不设置 `icon` 时只显示文字链接。

首次安装 Python 依赖，然后生成并预览（也可在 Python 虚拟环境中运行）：

```powershell
python -m pip install -r requirements.txt
python scripts/build.py
python -m http.server 8000 --bind 127.0.0.1
```

浏览器访问 `http://127.0.0.1:8000`。停止预览按 Ctrl+C。
需要调整结构时编辑生成脚本或模板，需要调整外观时编辑 CSS。生成后的 HTML 也需一起提交，避免下一次生成覆盖手工修改。

## 添加 Markdown 笔记

沿用示例文件夹即可，不需要手工登记笔记列表：

```text
note/
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

每个 Markdown 文件会生成阅读页。`main.md` 或 `index.md` 生成同目录的 `index.html`，其他名称如 `example.md` 生成 `example.html`。同一目录不要同时放 `main.md` 和 `index.md`，以免输出重名。第一层目录默认作为分类，深层目录用于组织主题。

文件开头支持 YAML 元数据（均可选）：

```yaml
---
title: "笔记标题"
date: 2026-10-10 18:30
cover: cover.jpeg
summary: "显示在目录页的摘要；省略时从正文提取。"
category: "Computational Physics" # 省略时使用第一层文件夹名称
draft: false # true 时不生成页面、不进入目录
---
```

无元数据时从一级标题或文件名推断标题。文章按日期从新到旧排列，没有日期时显示“未标注日期”。直接放在 `note/` 根目录的笔记属于“未分类”。分类会随笔记自动出现，也可在 `content/note-categories.json` 配置中文名称和简介。现有“Computational Physics”显示为“计算物理”。

支持标题、段落、粗体、斜体、引用、列表、任务列表、表格、代码高亮、脚注、图片与链接。原始 HTML 作为文本展示。正文图片使用相对路径，例如 `![图示说明](1.png)`；含空格的路径用 `![说明](<figure 1.png>)`。建议填写图片说明供辅助阅读。跨笔记链接可写 `[另一篇笔记](../另一篇/main.md)`，生成器自动转换为网页链接，并对空格与中文路径编码。

公式支持 `$...$` 与 `$$...$$`（包括矩阵、多行 aligned 等 KaTeX 支持的语法）。公式在生成时转换为 HTML 与 MathML，字体由本站提供；长公式可独立横向滚动，不会撑宽手机页面。错误的公式或缺失的本地图片会给出构建错误，避免静默发布损坏页面。

正文页提供章节目录、分类返回、阅读时间估算、Markdown 下载及同类笔记推荐；目录页支持分类与全文关键词搜索。关闭 JavaScript 时所有已发布笔记和分类仍可直接浏览。

修改 Markdown 或资源后运行 `python scripts/build.py`。自动生成的页面不应手动编辑；移除源文件后重新生成，会根据 `note/.generated-pages.json` 清理对应的旧阅读页，原始文件不受影响。

## 添加歌曲与论文

在 `content/site.json` 的对应数组添加对象，将附件放入对应的 `files` 子目录，然后重新生成页面。

笔记附件也可以放在 `files/notes/`，并在 Markdown 中使用相对路径链接。

检查生成器：

```powershell
python -m unittest discover -s tests -v
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

网站地址为 <https://flowers-for-tuesday.github.io/>。发布包通过 `scripts/package_site.py` 生成，只包含网站目录，不包含本地预览工具、构建依赖或 Git 数据。

布局参考 <https://davidtong.org/> 的顶部导航和左图右文结构，所有网站代码为本项目实现。
