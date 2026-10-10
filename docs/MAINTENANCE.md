# Flowers for Tuesday 维护说明

这是一个不需要 Node.js 依赖的静态博客，适合 GitHub Pages。所有页面均有完整 HTML，关闭 JavaScript 仍可阅读和导航。

## 文件结构

```text
README.md               入场动画的两行原文
content/site.json       个人介绍、笔记、歌曲、论文数据
templates/base.html    共用页头、导航、页脚
scripts/build.py        静态页面生成脚本（Python 3.10+，仅标准库）
assets/css/site.css     样式与响应式布局
assets/js/site.js       手机导航、可跳过的入场动画
assets/fonts/          东京街角的小浪漫网页字体
assets/images/         avator.jpg、about.jpeg 原图
files/notes/           笔记附件
files/music/           歌曲音频、歌词、乐谱
files/publications/    公开论文附件
index.html             生成的主页
about/index.html       生成的个人介绍
note/index.html        生成的笔记列表
music/index.html       生成的原创音乐列表
publication/index.html 生成的论文列表
404.html               找不到页面时的提示
favicon.ico            原有网站 logo
```

## 编辑与预览

About 页的个人账号导航在 `about.navigation` 中维护，每项包含 `label`（显示名称）与 `url`（账号链接）。

修改 `content/site.json` 后，在仓库根目录运行：

```powershell
python scripts/build.py
python -m http.server 8000 --bind 127.0.0.1
```

浏览器访问 `http://127.0.0.1:8000`。停止预览按 Ctrl+C。
需要调整结构时编辑生成脚本或模板，需要调整外观时编辑 CSS。生成后的 HTML 也需一起提交，避免下一次生成覆盖手工修改。

## 添加内容

三个数组默认为空，网站显示真实的待更新状态。按以下格式添加对象，并将文件放入对应 `files` 子目录，然后重新生成页面。

笔记（添加到 `notes`）：

```json
{
  "title": "笔记标题",
  "date": "2026-10-10",
  "description": "这份笔记的简短介绍。",
  "links": [{"label": "阅读 PDF", "url": "../files/notes/example.pdf"}]
}
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

使用 GitHub 仓库 **Settings → Pages → Build and deployment → Deploy from a branch**，选择 `main` 分支的 `/(root)`。根目录 `.nojekyll` 表示直接托管生成的静态文件，无需 Jekyll。网站地址为 <https://flowers-for-tuesday.github.io/>。

后续更新：重新生成页面，将修改提交并推送至 `main`；GitHub Pages 按仓库的 Pages 设置发布。

布局参考 <https://davidtong.org/> 的顶部导航和左图右文结构，所有网站代码为本项目实现。
