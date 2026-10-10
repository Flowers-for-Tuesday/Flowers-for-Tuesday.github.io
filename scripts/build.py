"""Generate the GitHub Pages site. Requires Python 3.10+, no third-party packages."""
import json
from html import escape
from pathlib import Path
from string import Template
from urllib.parse import urlsplit

BASE = Path(__file__).resolve().parents[1]
DATA = json.loads((BASE / "content/site.json").read_text(encoding="utf-8"))
TEMPLATE = Template((BASE / "templates/base.html").read_text(encoding="utf-8"))
QUOTE = [line.strip() for line in (BASE / "README.md").read_text(encoding="utf-8-sig").splitlines() if line.strip()][:2]
NAV = [("about", "About"), ("note", "Note"), ("music", "Music"), ("publication", "Publication")]


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


def render(page, main, description, title=None):
    root = "." if page in ("home", "404") else ".."
    navigation = "\n".join(
        f'<a href="{root}/{slug}/"' + (' aria-current="page"' if page == slug else '') + f'>{label}</a>'
        for slug, label in NAV
    )
    intro = ""
    if page == "home":
        lines = "".join(f'<p class="intro-line">{e(line)}</p>' for line in QUOTE)
        intro = f'''<dialog class="intro" aria-label="入场文字" aria-describedby="intro-words">
          <div class="intro-inner"><span class="intro-eyebrow">Flowers for Tuesday</span>
          <div id="intro-words">{lines}</div><span class="intro-rule" aria-hidden="true"></span></div>
          <button class="intro-skip" type="button" autofocus>进入主页 <span aria-hidden="true">↗</span></button>
        </dialog>'''
    html = TEMPLATE.substitute(
        root=root, page=page, title=e(title or DATA["name"]), description=e(description),
        github=safe_url(DATA["github"]), navigation=navigation, main=main, intro=intro,
        replay='<button class="replay-intro" type="button" hidden>重看开场</button>' if page == "home" else "",
    )
    target = BASE / ("index.html" if page == "home" else "404.html" if page == "404" else f"{page}/index.html")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(line.rstrip() for line in html.splitlines()) + "\n", encoding="utf-8")


def home():
    rows = ""
    for number, slug, label, chinese, text in [
        ("01", "note", "Note", "笔记", "记下问题，也记下寻找答案的过程。"),
        ("02", "music", "Music", "音乐", "把难以言说的心情，写进旋律里。"),
        ("03", "publication", "Publication", "学术发表", "记录研究中的思考与公开发表的成果。"),
    ]:
        rows += f'''<a class="directory-row" href="./{slug}/"><span class="row-number">{number}</span>
          <h3>{label}<span>{chinese}</span></h3><p>{text}</p><span class="row-arrow" aria-hidden="true">↗</span></a>'''
    render("home", f'''
      <section class="hero">
        <figure class="hero-image"><img src="./assets/images/avator.jpg" width="1600" height="1600" fetchpriority="high" alt="窗边伏在桌上的女孩，阳光洒在书页上"></figure>
        <div class="hero-copy"><p class="eyebrow">WELCOME TO MY LITTLE CORNER</p>
          <h1>Flowers<br>for Tuesday<span class="title-period">.</span></h1>
          <p class="hero-description">{e(DATA['description'])}</p>
          <p class="muted hero-note">欢迎来到我的个人博客。<br>在平凡的日子里，留下一点值得珍藏的东西。</p>
          <a class="text-link" href="./about/">关于我 <span aria-hidden="true">↗</span></a>
        </div>
      </section>
      <section class="directory" aria-labelledby="directory-heading"><div class="section-heading"><h2 id="directory-heading">在这里，慢慢生长</h2><span class="eyebrow">A PERSONAL COLLECTION</span></div>{rows}</section>
      <aside class="home-quote"><span class="quote-mark" aria-hidden="true">“</span><p>{e(QUOTE[0])}<br>{e(QUOTE[1])}</p><span class="quote-credit">— Flowers for Tuesday</span></aside>
    ''', DATA["description"])


def about():
    paragraphs = "".join(f'<p>{e(p)}</p>' for p in DATA["about"]["paragraphs"])
    profile_links = "".join(
        f'<a class="text-link" href="{safe_url(link["url"])}">{e(link["label"])} <span aria-hidden="true">↗</span></a>'
        for link in DATA["about"]["navigation"]
    )
    render("about", f'''
      <section class="about-hero">
        <figure class="about-image"><img src="../assets/images/about.jpeg" width="2474" height="3500" alt="戴着蓝色花冠的精灵坐在铺满花瓣的门前"></figure>
        <div class="about-copy"><p class="eyebrow">A LITTLE ABOUT ME</p><h1>About<span class="title-period">.</span></h1>
          <p class="page-subtitle">关于我</p>{paragraphs}
          <p>你可以在 <a href="../note/">Note</a> 阅读我的笔记，在 <a href="../music/">Music</a> 听听我的原创音乐，或在 <a href="../publication/">Publication</a> 了解我的学术发表。</p>
          <div class="about-profiles"><h2 id="profiles-heading">在其他地方找到我</h2>
            <nav class="profile-links" aria-labelledby="profiles-heading">{profile_links}</nav>
          </div>
        </div>
      </section>
      <section class="about-background"><p class="eyebrow">BACKGROUND</p><h2>更多关于我</h2><p class="muted">{e(DATA['about']['background'])}</p></section>
    ''', "关于 Flowers for Tuesday：个人介绍、笔记、原创音乐与学术发表。", "About | " + DATA["name"])


def entries(kind, items):
    output = []
    for item in items:
        links = "".join(f'<a class="text-link" href="{safe_url(link["url"])}">{e(link["label"])} <span aria-hidden="true">↗</span></a>' for link in item.get("links", []))
        audio = f'<audio controls preload="none" src="{safe_url(item["audio"])}">你的浏览器不支持音频播放，<a href="{safe_url(item["audio"])}">下载音频</a>。</audio>' if kind == "music" and item.get("audio") else ""
        output.append(f'''<article class="entry"><p class="entry-meta">{e(item.get('date', ''))}</p><h2>{e(item['title'])}</h2><p class="muted">{e(item.get('description', ''))}</p>{audio}<div class="entry-links">{links}</div></article>''')
    return "".join(output)


def collection(page, key, label, chinese, description, empty_title, empty_text):
    items = DATA[key]
    content = entries(page, items) if items else f'''<div class="empty-state"><span class="empty-ornament" aria-hidden="true">✳</span><h2>{empty_title}</h2><p>{empty_text}</p><span class="empty-caption">TO BE CONTINUED</span></div>'''
    render(page, f'''
      <header class="page-heading"><p class="eyebrow">{chinese}</p><h1>{label}<span class="title-period">.</span></h1><p>{description}</p></header>
      <section class="collection" aria-label="{chinese}列表"><div class="collection-heading"><h2>{chinese}</h2><span>{len(items):02d} {'首作品' if page == 'music' else '篇记录'}</span></div>{content}</section>
      <div class="page-end"><span>慢慢积累，慢慢更新。</span><a class="text-link" href="../">返回主页 <span aria-hidden="true">↗</span></a></div>
    ''', description, label + " | " + DATA["name"])


if __name__ == "__main__":
    if len(QUOTE) != 2:
        raise ValueError("README.md must contain at least two non-empty lines for the entrance text.")
    home()
    about()
    collection("note", "notes", "Note", "学习笔记", "随手写下的想法，认真整理的知识。让每一次思考都有迹可循。", "下一页，留给新的思考。", "笔记正在整理中，之后会在这里分享文字与笔记文件。")
    collection("music", "music", "Music", "原创音乐", "一些旋律，一些未说出口的话。这里收藏我自己写的歌曲。", "让旋律，慢慢响起。", "原创歌曲正在整理中，之后可以在这里聆听与阅读。")
    collection("publication", "publications", "Publication", "学术发表", "在问题与答案之间，记录每一步探索。这里汇集我的公开学术论文。", "每一份探索，都值得记录。", "论文目录待更新，之后会在这里整理公开发表的论文与阅读链接。")
    render("404", '<section class="not-found"><p class="eyebrow">404 / PAGE NOT FOUND</p><h1>这一页，还未写下。</h1><p class="muted">你寻找的页面不存在，或已搬到别处。</p><a class="text-link" href="/">返回主页 ↗</a></section>', "页面未找到", "404 | " + DATA["name"])
    # GitHub Pages serves 404.html at arbitrary paths, so its assets need absolute URLs.
    path = BASE / "404.html"
    path.write_text(path.read_text(encoding="utf-8").replace('href="./', 'href="/').replace('src="./', 'src="/'), encoding="utf-8")
    print("Built home, About, Note, Music, Publication and 404 pages.")
