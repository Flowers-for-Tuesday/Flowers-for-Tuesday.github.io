# Music / 音楽

`/music/` 分为“笔记”和“原创作品”。首页卡片与全站导航使用 Music，日文标签为「音楽」。

## 音乐笔记

笔记沿用 Note 的 Markdown、类别筛选、搜索、目录和阅读页面。源文件放在 `files/music/notes/`，例如：

```text
files/music/notes/Classical/harmony/main.md
files/music/notes/R&B/rhythm.md
```

在 YAML 中填写 `title`、`category`、`date` 和可选 `summary`、`cover`；未指定 `category` 时使用第一级文件夹名。`content/music-categories.json` 控制预设类别与顺序，默认 Classical、R&B，新增类别也会自动显示。草稿设置 `draft: true`，发布时改成 `false`。

## 原创专辑

每张专辑使用一个目录，例如 `files/music/albums/my-album/`，其中放置 `main.md`、正方形封面和音频文件。列表以专辑封面卡片排版，点击进入介绍和曲目页面；没有封面时显示音符占位。

```markdown
---
title: 专辑名称
category: 原创作品
date: 2026-11-06
summary: 专辑简介
cover: cover.jpg
draft: false
---

## 关于专辑

创作背景。

## 曲目

1. [第一首](01.mp3)
2. [第二首](02.mp3)
```

曲目链接可指向同目录音频或 HTTPS 播放地址。示例草稿位于 `files/music/albums/first-album/main.md`。

运行 `python scripts/manage.py build` 重新生成。页面生成器在 `scripts/music.py`，样式在 `assets/css/music.css`，首页配图为 `assets/images/music.jpg`。
