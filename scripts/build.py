"""Generate the GitHub Pages site; see requirements.txt and docs/MAINTENANCE.md."""
import json
from datetime import date
from html import escape
from pathlib import Path
from string import Template
from urllib.parse import urlsplit
from notes import build_notes
from projects import build_projects
from gallery import build_gallery
from about import load_about_entries
from music import build_music
from palettes import build_palettes, build_color_page

BASE = Path(__file__).resolve().parents[1]
DATA = json.loads((BASE / "content/site.json").read_text(encoding="utf-8"))
TEMPLATE = Template((BASE / "templates/base.html").read_text(encoding="utf-8"))
INTRO_TEXT = (
    "刻まれた言葉が、心に浮かぶ",
    "「我が愛を、ここに棄てる」",
)
NAV = [("about", "About"), ("note", "Note"), ("music", "Music"), ("gallery", "Gallery"), ("research", "Research")]


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
    active_page = page
    navigation = "\n".join(
        f'<a href="{root}/{slug}/"' + (' aria-current="page"' if active_page == slug else '') + f'>{label}</a>'
        for slug, label in NAV
    )
    intro = ""
    if page == "home":
        lines = "\n            ".join(f'<p class="intro-line">{e(line)}</p>' for line in INTRO_TEXT)
        intro = f'''<dialog class="intro" aria-label="入场文字" aria-describedby="intro-words">
          <div id="intro-words" class="intro-inner" lang="ja">
            {lines}
          </div>
          <button class="intro-skip" type="button" autofocus>进入主页 <span aria-hidden="true">↗</span></button>
        </dialog>'''
    html = TEMPLATE.substitute(
        root=root, page=page, title=e(title or DATA["name"]), description=e(description),
        navigation=navigation, main=main, intro=intro,
        extra_head=extra_head.replace("{root}", root),
        footer_text=e(DATA["home"]["footer_text"]),
        links_current=' aria-current="page"' if page == "links" else "",
        color_current=' aria-current="page"' if page == "color" else "",
        info_current=' aria-current="page"' if page == "info" else "",
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(line.rstrip() for line in html.splitlines()) + "\n", encoding="utf-8")


def info():
    cname = BASE / "CNAME"
    domain = cname.read_text(encoding="utf-8").strip() if cname.is_file() else ""
    domain = domain or "flowers-for-tuesday.github.io"
    releases = sorted(DATA["releases"], key=lambda release: release["date"], reverse=True)
    addresses = DATA.get("ipv4_by_domain", {}).get(domain.lower(), [])
    ip_row = '<div><dt>IPv4 地址</dt><dd>' + '<br>'.join(e(ip) for ip in addresses) + '</dd></div>' if addresses else ''
    render("info", f'''<div class="utility-layout site-info">
        <h1 class="info-heading" lang="en">Info<span class="title-period" aria-hidden="true">.</span></h1>
        <dl aria-label="网站信息">
          <div><dt>网站地址</dt><dd><a href="{safe_url("https://" + domain + "/")}">{e(domain)}</a></dd></div>
          {ip_row}
          <div><dt>网站版本</dt><dd>{e(releases[0]["version"])}</dd></div>
          <div><dt>托管平台</dt><dd lang="en">GitHub Pages</dd></div>
          <div><dt lang="en">Source Code</dt><dd><a href="https://github.com/Flowers-for-Tuesday/Flowers-for-Tuesday.github.io">在 GitHub 查看</a></dd></div>
          <div><dt>网站字体</dt><dd>中文（汉仪明禅刻本），<span lang="en">English（Sondra）</span>，<span lang="ja">日本語（A1 明朝）</span>，<span lang="es">Español（Sondra）</span>，<span lang="fr">Français（Bodoni Moda）</span>，<span lang="de">Deutsch（Bodoni Moda）</span></dd></div>
        </dl>
      </div>
      <section class="utility-layout site-log" aria-labelledby="log">
        <h2 id="log" class="info-heading" lang="en">Log<span class="title-period" aria-hidden="true">.</span></h2>
        {render_log_entries(releases)}
      </section>''', "网站信息、字体说明与更新日志。", "Info | " + DATA["name"],
      extra_head='<link rel="stylesheet" href="{root}/assets/css/utility.css"><link rel="stylesheet" href="{root}/assets/css/log.css">')
    render("log", '<p><a href="../info/#log">查看更新日志</a></p>', "网站更新日志。", "Log | " + DATA["name"],
           extra_head='<meta http-equiv="refresh" content="0; url=../info/#log">')


def links():
    items = json.loads((BASE / "content/links.json").read_text(encoding="utf-8"))
    entries = []
    for item in items:
        url = safe_url(item["url"])
        description = f'<p>{e(item["description"])}</p>' if item.get("description") else ""
        entries.append(f'''<li class="saved-link"><a href="{url}">
          <div><h2>{e(item['label'])}</h2>{description}<span class="saved-link-url">{e(item['url'])}</span></div>
          <span class="saved-link-arrow" aria-hidden="true">↗</span>
        </a></li>''')
    content = '<ul class="saved-links" role="list">' + ''.join(entries) + '</ul>' if entries else '<div class="empty-state"><p>有用的网址，陆续收藏于此。</p></div>'
    render("links", f'''<div class="utility-layout"><header class="page-heading"><h1 lang="en">Links<span class="title-period">.</span></h1></header>
      <section class="links-collection" aria-label="收藏的网址">{content}</section></div>''',
      "收藏一些有用的网址。", "Links | " + DATA["name"],
      extra_head='<link rel="stylesheet" href="{root}/assets/css/utility.css">')


def render_log_entries(releases):
    items = json.loads((BASE / "content/log.json").read_text(encoding="utf-8"))
    entries = []
    for item in sorted(items, key=lambda item: date.fromisoformat(item["date"]), reverse=True):
        published = date.fromisoformat(item["date"]).isoformat()
        version = item.get("version") or next((r["version"] for r in releases if r["date"] <= published), None)
        version_line = f'<span class="log-version">{e(version)}</span>' if version else ""
        changes = "".join(f'<li>{e(change)}</li>' for change in item["changes"])
        entries.append(f'''<li class="log-entry"><article>
          <div class="log-meta"><time datetime="{published}">{published}</time>{version_line}</div>
          <div class="log-entry-content"><h3>{e(item['title'])}</h3><ul>{changes}</ul></div>
        </article></li>''')
    return '<ol class="log-list" role="list">' + ''.join(entries) + '</ol>' if entries else '<p class="muted">还没有更新记录。</p>'


def home():
    profile_links = "".join(
        f'<a class="text-link" href="{safe_url(link["url"])}">{profile_icon(link)}{e(link["label"])} <span aria-hidden="true">↗</span></a>'
        for link in DATA["social_links"]
    )
    profile_links += f'<a class="text-link" href="mailto:{e(DATA["email"])}" title="{e(DATA["email"])}">{profile_icon({"icon": "email"})}Email <span aria-hidden="true">↗</span></a>'
    cards = ""
    for number, slug, label, japanese in [
        ("01", "about", "About", "私"),
        ("02", "note", "Note", "物理"),
        ("03", "music", "Music", "音楽"),
        ("04", "gallery", "Gallery", "旅路"),
        ("05", "research", "Research", "研究"),
    ]:
        cards += f'''<a class="directory-card{' is-expanded' if slug == 'about' else ''}" href="./{slug}/" aria-labelledby="card-{slug}">
          <div class="directory-card-surface">
            <img src="./assets/images/{slug}.jpg" width="{2896 if slug == 'note' else 2892}" height="4096" alt="" loading="lazy" decoding="async">
            <span class="card-number" aria-hidden="true">{number}</span>
            <div class="card-caption"><h3 id="card-{slug}">{label}<span lang="ja">{japanese}</span></h3><span class="card-arrow" aria-hidden="true">↗</span></div>
          </div>
        </a>'''
    render("home", f'''
      <div class="home-layout">
      <section class="hero" aria-labelledby="home-name">
        <figure class="hero-image"><img src="./assets/images/avator.png" width="1862" height="1862" fetchpriority="high" alt="个人头像"></figure>
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
    articles = []
    for index, item in enumerate(load_about_entries(BASE)):
        articles.append(f'''<article class="about-entry" data-entry-theme="{item['theme']}" aria-labelledby="about-subtitle-{index}">
          <p class="page-subtitle" id="about-subtitle-{index}">{e(item['subtitle'])}</p>{item['html']}
        </article>''')
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
        <figure class="about-image theme-image" role="img" aria-label="白昼溪流与夜晚星河下的旅人">
          <img class="theme-image-day" src="../assets/images/about_day.jpeg" width="992" height="1654" alt="" decoding="async">
          <img class="theme-image-night" src="../assets/images/about_night.jpeg" width="992" height="1654" alt="" decoding="async">
        </figure>
        <div class="about-copy"><p class="eyebrow" lang="ja">私</p><h1>About<span class="title-period">.</span></h1>
          <div class="about-pagination" role="group" aria-label="切换 About 文章" hidden>
            <button type="button" class="about-previous" aria-label="上一篇" aria-controls="about-entries"><span aria-hidden="true">←</span></button>
            <span class="about-position" role="status" aria-atomic="true"></span>
            <button type="button" class="about-next" aria-label="下一篇" aria-controls="about-entries"><span aria-hidden="true">→</span></button>
          </div>
          <div id="about-entries">{''.join(articles)}</div>
          <p class="about-empty muted" hidden>此时，还没有留下文字。</p>
        </div>
      </section>
      <section class="about-background" aria-labelledby="background-heading">
        <div class="about-background-copy"><h2 id="background-heading">Background</h2><ol class="education-timeline" role="list">{''.join(education)}</ol></div>
        <figure class="about-image background-image theme-image" role="img" aria-label="山林间的旅途与烛光下的壁画">
          <img class="theme-image-day" src="../assets/images/background_day.jpeg" width="992" height="1654" alt="" decoding="async">
          <img class="theme-image-night" src="../assets/images/background_night.jpeg" width="992" height="1654" alt="" decoding="async">
        </figure>
      </section>
    ''', "关于 Flowers for Tuesday：个人介绍、笔记、音乐与原创作品、摄影与学术发表。", "About | " + DATA["name"])


if __name__ == "__main__":
    build_palettes(BASE)
    build_color_page(BASE, render, DATA['name'])
    home()
    about()
    links()
    info()
    build_notes(BASE, render)
    build_music(BASE, render, DATA["name"])
    build_gallery(BASE, render, DATA["name"])
    build_projects(BASE, render)
    render("404", '<section class="not-found"><h1>这一页，还未写下。</h1><p class="muted">你寻找的页面不存在，或已搬到别处。</p><a class="text-link" href="/">返回主页 ↗</a></section>', "页面未找到", "404 | " + DATA["name"])
    # GitHub Pages serves 404.html at arbitrary paths, so its assets need absolute URLs.
    path = BASE / "404.html"
    path.write_text(path.read_text(encoding="utf-8").replace('href="./', 'href="/').replace('src="./', 'src="/'), encoding="utf-8")
    print("Built home, About, Links, Color, Log, Info, Note, Music, Gallery, Research and 404 pages.")
