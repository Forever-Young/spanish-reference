#!/usr/bin/env python3
"""Build the multi-page site: start page, one page per section, and all.html."""
import html
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1]).resolve()
VERSION = sys.argv[2]
BUILT_DATE = sys.argv[3]
ES_DIR = Path(sys.argv[4]).resolve() if len(sys.argv) > 4 else None
SITE_TITLE = "Справочник по испанскому языку: грамматика и живая речь"
SHORT_TITLE = "Справочник по испанскому языку"


def pandoc(md: str, lua: bool = False) -> str:
    cmd = ["pandoc", "--from=markdown", "--to=html5", "--wrap=none"]
    if lua:
        cmd.append(f"--lua-filter={ROOT / 'build-timestamp.lua'}")
    return subprocess.run(cmd, input=md, capture_output=True, text=True, check=True).stdout


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


OPENER = re.compile(r"\n(::: \{[^\n]*\})[ \t]*\n*$")


def split_sections(text: str):
    """Return (title block, [(part, number, heading, markdown)]).

    Parts are level-1 headings with the class ``part``; sections are level-2
    headings. A ``::: {.class}`` line that opens a wrapper just before a
    heading is moved into the chunk of that heading.
    """
    chunks = re.split(r"(?m)^(?=#{1,2} )", text)
    for i in range(len(chunks) - 1):
        m = OPENER.search(chunks[i])
        if m:
            chunks[i + 1] = m.group(1) + "\n\n" + chunks[i + 1]
            chunks[i] = chunks[i][: m.start()] + "\n"
    title_block, sections, part = chunks[0], [], ""
    pending = ""
    for chunk in chunks[1:]:
        body = chunk.lstrip("\n")
        pm = re.match(r"# (.*?)\s*\{\.part\}\s*$", body.splitlines()[0]) if body.startswith("# ") else None
        if pm:
            part = pm.group(1)
            continue
        if body.startswith("# "):  # the document title
            continue
        m = re.match(r"## (\d+)\.\s+(.*?)(?:\s+\{#[^}]*\})?\s*$", body.splitlines()[0])
        if not m:
            # wrapper opener carried in front of the heading
            m2 = re.search(r"(?m)^## (\d+)\.\s+(.*?)(?:\s+\{#[^}]*\})?\s*$", body)
            if not m2:
                raise SystemExit(f"Unnumbered section heading: {body.splitlines()[0]}")
            m = m2
        sections.append((part, int(m.group(1)), m.group(2), body))
    return title_block, sections


def page_name(n: int) -> str:
    return f"{n:02d}.html"


HEAD = read("site-head.html")
THEME = read("site-theme.html")


def document(title: str, body: str, css_class: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="site.css">
{HEAD}
</head>
<body class="{css_class}">
{body}
</body>
</html>
"""


def grouped_list(sections, current: int | None, cls: str) -> str:
    """Parts as bold lines, their sections indented below."""
    out, last = [], None
    for part, n, heading, _ in sections:
        if part != last:
            if last is not None:
                out.append("</ol></li>")
            out.append(f'<li class="part"><span class="part-name">{html.escape(part)}</span><ol>')
            last = part
        cur = ' aria-current="page"' if n == current else ""
        out.append(f'<li><a href="{page_name(n)}"{cur}>{n}. {html.escape(heading)}</a></li>')
    out.append("</ol></li>")
    return f'<ol class="toc-list {cls}">\n' + "\n".join(out) + "\n</ol>"


def sidebar(sections, current: int | None) -> str:
    return f"""<nav id="sidebar" aria-label="Оглавление">
<div class="side-top">
<a href="./"{' aria-current="page"' if current is None else ''}>Начало</a>
<a href="all.html">Одной страницей</a>
</div>
<div id="search"></div>
<div class="toc-scroll">
{grouped_list(sections, current, "side-list")}
</div>
</nav>"""


SIDE_JS_TEMPLATE = """<script src="pagefind/pagefind-ui.js" onerror="void 0"></script>
<script>
(function () {
  var b = document.body;
  var btn = document.querySelector('.menu-btn');
  if (btn) btn.addEventListener('click', function () { b.classList.toggle('nav-open'); });
  var scrim = document.querySelector('.scrim');
  if (scrim) scrim.addEventListener('click', function () { b.classList.remove('nav-open'); });
  var cur = document.querySelector('#sidebar [aria-current="page"]');
  var side = document.getElementById('sidebar') || document.querySelector('.start');
  var sc = document.querySelector('.toc-scroll');
  if (sc && cur && cur.closest('.toc-list')) sc.scrollTop = Math.max(0, cur.offsetTop - sc.clientHeight / 3);
  if (window.PagefindUI) {
    new PagefindUI({ element: '#search', @PROCESS@ mergeIndex: [{ bundlePath: new URL('pagefind-es/', document.baseURI).pathname, language: 'es' }], showImages: false, showSubResults: true, resetStyles: false,
      translations: { placeholder: 'Поиск', clear_search: 'Очистить', load_more: 'Ещё результаты',
        search_label: 'Поиск по справочнику', filters_label: 'Фильтры', zero_results: 'Ничего не найдено: [SEARCH_TERM]',
        many_results: '[COUNT] результатов: [SEARCH_TERM]', one_result: '[COUNT] результат: [SEARCH_TERM]',
        alt_search: 'Ничего не найдено по [SEARCH_TERM]. Показаны результаты по [DIFFERENT_TERM]',
        search_suggestion: 'Ничего не найдено по [SEARCH_TERM]. Попробуйте:', searching: 'Ищу [SEARCH_TERM]…' } });
    var inp = document.querySelector('#search input');
    if (inp && side) inp.addEventListener('input', function () { side.classList.toggle('searching', inp.value.trim() !== ''); });
  } else {
    var s = document.getElementById('search'); if (s) s.remove();
  }
})();
</script>"""


SIDE_JS = SIDE_JS_TEMPLATE.replace("@PROCESS@ ", "")


def all_page_js(page_ids: dict[str, str]) -> str:
    """Search on all.html: results jump inside this page instead of to section pages."""
    import json
    proc = ("processResult: function (r) { var m = %s; "
            "function fix(u) { var f = u.split('#'), p = f[0].split('/').pop(); "
            "return 'all.html#' + (f[1] || m[p] || ''); } "
            "r.url = fix(r.url); (r.sub_results || []).forEach(function (x) { x.url = fix(x.url); }); return r; }," % json.dumps(page_ids, ensure_ascii=False))
    return SIDE_JS_TEMPLATE.replace("@PROCESS@", proc)


def section_page(sections, idx: int, fragment: str) -> str:
    part, n, heading, _ = sections[idx]
    prev_link = next_link = '<span></span>'
    if idx > 0:
        _, pn, ph, _ = sections[idx - 1]
        prev_link = f'<a class="prev" href="{page_name(pn)}" rel="prev">← {html.escape(ph)}</a>'
    if idx < len(sections) - 1:
        _, nn, nh, _ = sections[idx + 1]
        next_link = f'<a class="next" href="{page_name(nn)}" rel="next">{html.escape(nh)} →</a>'
    body = f"""<button type="button" class="menu-btn" aria-label="Оглавление">☰ Разделы</button>
<div class="scrim"></div>
{THEME}
<div class="layout">
{sidebar(sections, n)}
<main data-pagefind-body>
<p class="crumbs"><a href="./">{SHORT_TITLE}</a> · {html.escape(part)}</p>
{fragment}
<nav class="pager" aria-label="Соседние разделы">{prev_link}{next_link}</nav>
</main>
</div>
{SIDE_JS}"""
    return document(f"{n}. {heading} — {SHORT_TITLE}", body, "paged")


def main() -> None:
    text = read("reference.md")
    _title_block, sections = split_sections(text)
    OUT.mkdir(parents=True, exist_ok=True)

    fragments = [pandoc(md) for _, _, _, md in sections]

    # ids -> page, to retarget cross-section links
    id_page: dict[str, str] = {}
    for (_, n, _, _), frag in zip(sections, fragments):
        for i in re.findall(r'\bid="([^"]+)"', frag):
            id_page.setdefault(i, page_name(n))

    def retarget(frag: str, own: str) -> str:
        def fix(m):
            target = m.group(1)
            page = id_page.get(target)
            if page is None or page == own:
                return m.group(0)
            return f'href="{page}#{target}"'
        return re.sub(r'href="#([^"]+)"', fix, frag)

    for idx, ((_, n, _, _), frag) in enumerate(zip(sections, fragments)):
        frag = retarget(frag, page_name(n))
        frag = frag.replace("<h2 ", '<h2 data-pagefind-meta="title" ', 1)
        (OUT / page_name(n)).write_text(section_page(sections, idx, frag), encoding="utf-8")

    # Spanish-only pages for a second search index (Spanish word forms)
    if ES_DIR:
        ES_DIR.mkdir(parents=True, exist_ok=True)
        for (_, n, heading, _), frag in zip(sections, fragments):
            parts = []
            for m in re.finditer(r"<(em|strong)>(.*?)</\1>", frag, re.S):
                t = html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
                if re.search(r"[A-Za-zÁ-ÿ]", t) and not re.search(r"[А-Яа-яЁё]", t):
                    parts.append(t)
            ps = "\n".join(f"<p>{html.escape(t)}</p>" for t in parts)
            page = (f'<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><title>{html.escape(heading)}</title></head>'
                    f'<body><main data-pagefind-body><meta data-pagefind-meta="title[content]" content="{html.escape(f"{n}. {heading}")}">{ps}</main></body></html>')
            (ES_DIR / page_name(n)).write_text(page, encoding="utf-8")

    # start page
    header = read("site-header.html").replace("@VERSION@", VERSION).replace("@DATE@", BUILT_DATE)
    toc = grouped_list(sections, None, "start-list")
    body = f"""{THEME}
<div class="start">
<h1>{SHORT_TITLE}<span class="subtitle">Грамматика и живая речь</span></h1>
{header}
<div id="search"></div>
<h2 class="start-toc">Разделы</h2>
{toc}
</div>
{SIDE_JS}"""
    (OUT / "index.html").write_text(document(SITE_TITLE, body, "start-page"), encoding="utf-8")

    # everything on one page
    whole = pandoc(text, lua=True)
    page_ids = {}
    for (_, n, _, _), frag in zip(sections, fragments):
        m = re.search(r'<h2[^>]*\bid="([^"]+)"', frag)
        if m:
            page_ids[page_name(n)] = m.group(1)
        else:  # heading without id (wrapped section): add one to the whole page
            whole, k = re.subn(rf"<h2>({n}\. )", rf'<h2 id="sec-{n}">\1', whole, count=1)
            if k:
                page_ids[page_name(n)] = f"sec-{n}"
    body = f"""{THEME}
<p class="crumbs noprint"><a href="./">← На главную</a></p>
<div class="noprint all-search"><div id="search"></div></div>
{whole}
{all_page_js(page_ids)}"""
    (OUT / "all.html").write_text(
        document(f"{SITE_TITLE} (одной страницей)", body, "all-page"), encoding="utf-8")
    print(f"Created {len(sections)} section pages, index.html and all.html in {OUT}")


main()
