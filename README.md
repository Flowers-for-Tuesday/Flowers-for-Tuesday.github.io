# 僕の*シークレットベース*~ 

>ねぇ、<br>
このまま夜が来たら、<br>
僕らどうなるんだろうね

 -- <i>ヨルシカ</i>「夜行」

---

## 给文章添加封面

在文章 Front Matter 中加一行 `cover:` 即可，路径指向 `assets/images/...` 下的图片：

```yaml
---
title: "量子蒙特卡洛（QMC）"
date: 2026-05-22T9:30+08:00
categories:
  - Note
cover: /assets/images/Note/QMC/cover.jpg
excerpt: "当前计算凝聚态物理中 QMC 是非常常用的第一性原理计算方法之一……"
---
```

效果：

- **首页/归档列表**：左侧显示小缩略图，右侧是标题、日期与摘要。
- **文章详情页**：封面作为顶部全宽 banner，标题白字叠加其上。

可选字段：

| 字段 | 作用 | 默认值 |
| --- | --- | --- |
| `cover` | 封面图片路径 | 无（不显示封面） |
| `cover_filter` | banner 黑色遮罩透明度（0~1，越大越暗） | `0.4` |
| `cover_caption` | banner 右下角的小字注释（支持 Markdown） | 无 |
| `excerpt` | 列表页显示的摘要（不写会自动取正文开头） | 自动 |

封面图片建议放在 `assets/images/<分类>/<文章 slug>/cover.jpg` 下，方便和文章里其他图片归档在一起。

## 写一条 Thought

Thoughts 是轻量化的短内容（一两段话加张图就行），文件放在 `_thoughts/` 目录下：

```yaml
---
date: 2026-05-23 18:00
tags:
  - 杂记            # 可选
title: "可以省略"   # 可选；省略时只显示日期
---

正文随意，支持 Markdown、图片、引用、代码片段。
```

- 列表页 `/thoughts/` 是按时间倒序的单列 feed，全文直接铺开，不需要点进去。
- 单条永久链接 `/thoughts/<filename>/`，方便分享。
- 标签会跳到 `Posts → Tags` 视图对应的分组。

文件命名约定：`YYYY-MM-DD-<短描述>.md`，比如 `_thoughts/2026-05-23-first.md`。

## 文章列表分组方式

主导航 `Posts` 页面顶部有 `Time / Categories / Tags` 三个 tab，可以分别按时间、分类、标签查看所有文章。文章详情页底部的分类/标签 chip 会直接深链到 `/posts/#cat-<slug>` 或 `/posts/#tag-<slug>` 并自动激活相应 tab。
