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
