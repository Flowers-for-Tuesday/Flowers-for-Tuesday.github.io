"""Generate the GitHub Pages site; see requirements.txt and docs/MAINTENANCE.md."""
import json
from html import escape
from pathlib import Path
from string import Template
from urllib.parse import urlsplit
from notes import build_notes

BASE = Path(__file__).resolve().parents[1]
DATA = json.loads((BASE / "content/site.json").read_text(encoding="utf-8"))
TEMPLATE = Template((BASE / "templates/base.html").read_text(encoding="utf-8"))
QUOTE = [line.strip() for line in (BASE / "README.md").read_text(encoding="utf-8-sig").splitlines() if line.strip()][:2]
NAV = [("about", "About"), ("note", "Note"), ("music", "Music"), ("gallery", "Gallery"), ("publication", "Publication")]


def e(value):
    return escape(str(value), quote=True)


def safe_url(value):
    """Allow repository paths and HTTPS links, reject executable URL schemes."""
    if not value or "\\" in value or any(ord(c) < 32 for c in value):
        raise ValueError(f"Invalid content URL: {value!r}")
    parts = urlsplit(value)
    if (parts.scheme and parts.scheme != "https") or (parts.netloc and not parts.scheme):
        raise ValueError(f"Use a relative path or HTTPS URL: {value!r}")
    return e(value)


def render(page, main, description, title=None, *, output=None, extra_head=""):
    target = BASE / (output or ("index.html" if page == "home" else "404.html" if page == "404" else f"{page}/index.html"))
    depth = len(target.relative_to(BASE).parts) - 1
    root = "/".join([".."] * depth) or "."
    navigation = "\n".join(
        f'<a href="{root}/{slug}/"' + (' aria-current="page"' if page == slug else '') + f'>{label}</a>'
        for slug, label in NAV
    )
    intro = ""
    if page == "home":
        lines = "".join(f'<p class="intro-line">{e(line)}</p>' for line in QUOTE)
        intro = f'''<dialog class="intro" aria-label="入场文字" aria-describedby="intro-words">
          <div class="intro-inner">
          <div id="intro-words">{lines}</div></div>
          <button class="intro-skip" type="button" autofocus>进入主页 <span aria-hidden="true">↗</span></button>
        </dialog>'''
    html = TEMPLATE.substitute(
        root=root, page=page, title=e(title or DATA["name"]), description=e(description),
        navigation=navigation, main=main, intro=intro,
        extra_head=extra_head.replace("{root}", root),
        footer_text=e(DATA["home"]["footer_text"]),
        email=e(DATA["email"]),
        footer_links="".join(
            f'<a href="{safe_url(link["url"])}">{e(link["label"])} <span aria-hidden="true">↗</span></a>'
            for link in DATA["social_links"]
        ),
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(line.rstrip() for line in html.splitlines()) + "\n", encoding="utf-8")


def home():
    profile_links = "".join(
        f'<a class="text-link" href="{safe_url(link["url"])}">{profile_icon(link)}{e(link["label"])} <span aria-hidden="true">↗</span></a>'
        for link in DATA["social_links"]
    )
    profile_links += f'<a class="text-link" href="mailto:{e(DATA["email"])}" title="{e(DATA["email"])}">{profile_icon({"icon": "email"})}Email <span aria-hidden="true">↗</span></a>'
    cards = ""
    for number, slug, label, chinese in [
        ("01", "note", "Note", "学习笔记"),
        ("02", "music", "Music", "原创音乐"),
        ("03", "gallery", "Gallery", "摄影作品"),
        ("04", "publication", "Publication", "学术发表"),
    ]:
        cards += f'''<a class="directory-card{' is-expanded' if slug == 'note' else ''}" href="./{slug}/" aria-labelledby="card-{slug}">
          <div class="directory-card-surface">
            <img src="./assets/images/{slug}.jpg" width="{2896 if slug == 'publication' else 2892}" height="4096" alt="" loading="lazy" decoding="async">
            <span class="card-number" aria-hidden="true">{number}</span>
            <div class="card-caption"><h3 id="card-{slug}">{label}<span>{chinese}</span></h3><span class="card-arrow" aria-hidden="true">↗</span></div>
          </div>
        </a>'''
    render("home", f'''
      <div class="home-layout">
      <section class="hero" aria-labelledby="home-name">
        <figure class="hero-image"><img src="./assets/images/avator.jpg" width="1600" height="1600" fetchpriority="high" alt="窗边伏在桌上的女孩，阳光洒在书页上"></figure>
        <div class="hero-copy">
          <h1 id="home-name">{e(DATA['name'])}<span class="title-period">.</span></h1>
          <aside class="home-quote"><span class="quote-mark" aria-hidden="true">“</span><p>{'<br>'.join(e(line) for line in DATA['home']['quote'])}</p></aside>
          <div class="home-profiles">
            <nav class="profile-links" aria-label="个人账号与邮箱">{profile_links}</nav>
          </div>
        </div>
      </section>
      <section class="directory" aria-label="栏目导航">
        <div class="directory-track" id="directory-track" aria-label="栏目卡片，悬停或聚焦展开">{cards}</div>
      </section>
      </div>
    ''', " ".join(DATA["home"]["quote"]))


def profile_icon(link):
    icon = link.get("icon")
    if icon not in ("github", "zhihu", "bilibili", "email"):
        return ""
    svg = (BASE / f"assets/icons/{icon}.svg").read_text(encoding="utf-8").strip()
    return svg.replace("<svg ", f'<svg class="profile-icon icon-{icon}" aria-hidden="true" focusable="false" fill="currentColor" ', 1)


def about():
    paragraphs = "".join(f'<p>{e(p)}</p>' for p in DATA["about"]["paragraphs"])
    education = []
    for item in DATA["about"]["background"]:
        logo = (
            f'<div class="education-logo"><img src="{safe_url("../" + item["logo"])}" alt="" loading="lazy"></div>'
            if item.get("logo") else ""
        )
        education.append(f'''<li class="education-item">
          <p class="education-years">{e(item['years'])}</p>
          <span class="education-track" aria-hidden="true"></span>
          <div class="education-content">{logo}<div class="education-details"><h3>{e(item['school'])}</h3><p>{e(item['program'])}</p></div></div>
        </li>''')
    render("about", f'''
      <section class="about-hero">
        <figure class="about-image"><img src="../assets/images/about.jpeg" width="2474" height="3500" alt="戴着蓝色花冠的精灵坐在铺满花瓣的门前"></figure>
        <div class="about-copy"><h1>About<span class="title-period">.</span></h1>
          <p class="page-subtitle"> 2026/10/10，夜，于北京</p>{paragraphs}
          <p>你可以在 <a href="../note/">Note</a> 阅读我的笔记，在 <a href="../music/">Music</a> 听听我写的歌，在 <a href="../gallery/">Gallery</a> 看看我的旅途，或在 <a href="../publication/">Publication</a> 了解我的学术发表。</p>
        </div>
      </section>
      <section class="about-background" aria-labelledby="background-heading">
        <div class="about-background-copy"><h2 id="background-heading">Background</h2><ol class="education-timeline" role="list">{''.join(education)}</ol></div>
        <figure class="about-image background-image"><img src="../assets/images/background.jpeg" width="2474" height="3500" alt="书架之间探出头的蓝发女孩" loading="lazy"></figure>
      </section>
    ''', "关于 Flowers for Tuesday：个人介绍、笔记、原创音乐、摄影与学术发表。", "About | " + DATA["name"])


def entries(kind, items):
    output = []
    for item in items:
        links = "".join(f'<a class="text-link" href="{safe_url(link["url"])}">{e(link["label"])} <span aria-hidden="true">↗</span></a>' for link in item.get("links", []))
        audio = f'<audio controls preload="none" src="{safe_url(item["audio"])}">你的浏览器不支持音频播放，<a href="{safe_url(item["audio"])}">下载音频</a>。</audio>' if kind == "music" and item.get("audio") else ""
        photo = f'<a class="gallery-photo" href="{safe_url(item["image"])}"><img src="{safe_url(item["image"])}" alt="{e(item.get("alt", item["title"]))}" loading="lazy" decoding="async"></a>' if kind == "gallery" and item.get("image") else ""
        output.append(f'''<article class="entry"><p class="entry-meta">{e(item.get('date', ''))}</p><h2>{e(item['title'])}</h2><p class="muted">{e(item.get('description', ''))}</p>{audio}{photo}<div class="entry-links">{links}</div></article>''')
    return "".join(output)


def collection(page, key, label, chinese, description, empty_title, empty_text):
    items = DATA[key]
    unit = {"music": "首作品", "gallery": "幅作品"}.get(page, "篇记录")
    content = entries(page, items) if items else f'''<div class="empty-state"><span class="empty-ornament" aria-hidden="true">✳</span><h2>{empty_title}</h2><p>{empty_text}</p></div>'''
    render(page, f'''
      <header class="page-heading"><p class="eyebrow">{chinese}</p><h1>{label}<span class="title-period">.</span></h1></header>
      <section class="collection" aria-label="{chinese}列表"><div class="collection-heading"><h2>{chinese}</h2><span>{len(items):02d} {unit}</span></div>{content}</section>
      <div class="page-end"><span>慢慢积累，慢慢更新。</span><a class="text-link" href="../">返回主页 <span aria-hidden="true">↗</span></a></div>
    ''', description, label + " | " + DATA["name"])


if __name__ == "__main__":
    if len(QUOTE) != 2:
        raise ValueError("README.md must contain at least two non-empty lines for the entrance text.")
    home()
    about()
    build_notes(BASE, render)
    collection("music", "music", "Music", "原创音乐", "一些旋律，一些未说出口的话。这里收藏我自己写的歌曲。", "让旋律，慢慢响起。", "原创歌曲正在整理中，之后可以在这里聆听与阅读。")
    collection("gallery", "gallery", "Gallery", "摄影作品", "一些星光，一些夜色。这里收藏我的摄影作品，记录镜头中的宇宙与日常。", "把星光，留在这里。", "摄影作品正在整理中，之后会在这里分享我的天文摄影与拍摄记录。")
    collection("publication", "publications", "Publication", "学术发表", "在问题与答案之间，记录每一步探索。这里汇集我的公开学术论文。", "每一份探索，都值得记录。", "论文目录待更新，之后会在这里整理公开发表的论文与阅读链接。")
    render("404", '<section class="not-found"><h1>这一页，还未写下。</h1><p class="muted">你寻找的页面不存在，或已搬到别处。</p><a class="text-link" href="/">返回主页 ↗</a></section>', "页面未找到", "404 | " + DATA["name"])
    # GitHub Pages serves 404.html at arbitrary paths, so its assets need absolute URLs.
    path = BASE / "404.html"
    path.write_text(path.read_text(encoding="utf-8").replace('href="./', 'href="/').replace('src="./', 'src="/'), encoding="utf-8")
    print("Built home, About, Note, Music, Gallery, Publication and 404 pages.")
