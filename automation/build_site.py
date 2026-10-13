#!/usr/bin/env python3
"""Markdown 원고 → docs/ 정적 페이지.

  automation/pages/*.md  → docs/<slug>.html        (무료 샘플 등 단독 페이지)
  automation/posts/*.md  → docs/blog/<slug>.html   (SEO 블로그 글)

글 머리에 YAML 형식의 메타데이터를 둔다:
  ---
  title: 제목
  description: 검색 결과에 보일 한두 문장
  date: 2026-10-13
  slug: url-에-쓸-영문-슬러그
  ---

블로그 목록(docs/blog/index.html)과 sitemap.xml도 함께 다시 만든다.
변환에는 pandoc을 쓴다.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE_URL = "https://seungyun-shin.github.io/Agent_work_reposi/"

PAGE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="root" content="{root}">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="article">
<link rel="canonical" href="{url}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap">
<link rel="stylesheet" href="{root}assets/style.css">
<script src="{root}assets/config.js"></script>
</head>
<body>
<header class="top"><div class="wrap"><a href="{root}">AI 업무자동화 키트</a><nav><a href="{root}free-prompts.html">무료 샘플</a><a href="{root}blog/">블로그</a></nav></div></header>
<main class="wrap"><article>
<h1>{title}</h1>
{meta_line}
{body}
</article>
<div class="cta">
<h3>이런 프롬프트가 40개 더 있습니다</h3>
<p>메일·보고서·회의·엑셀·마케팅·CS까지, 복붙해서 바로 쓰는 실무 프롬프트 40개 + 자동화 워크플로우 5개.</p>
<p class="price"><s data-list-price></s> 런칭 특가 <b data-price></b></p>
<a class="btn" data-buy href="{root}">키트 자세히 보기</a>
</div>
</main>
<footer><div class="wrap">© 2026 AI 업무자동화 키트</div></footer>
</body>
</html>
"""

INDEX = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="root" content="../">
<title>AI 업무자동화 블로그 | 복붙 프롬프트 모음</title>
<meta name="description" content="직장인을 위한 ChatGPT·Claude 실무 프롬프트와 업무 자동화 방법.">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap">
<link rel="stylesheet" href="../assets/style.css">
<script src="../assets/config.js"></script>
</head>
<body>
<header class="top"><div class="wrap"><a href="../">AI 업무자동화 키트</a><nav><a href="../free-prompts.html">무료 샘플</a><a href="./">블로그</a></nav></div></header>
<main class="wrap">
<h1>AI 업무자동화 블로그</h1>
<div class="post-list">
{items}
</div>
</main>
<footer><div class="wrap">© 2026 AI 업무자동화 키트</div></footer>
</body>
</html>
"""


def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        sys.exit(f"{path}: 머리 메타데이터(---)가 없습니다")
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip().strip('"')
    for key in ("title", "description", "slug"):
        if not meta.get(key):
            sys.exit(f"{path}: '{key}' 메타데이터가 비어 있습니다")
    if not re.fullmatch(r"[a-z0-9-]+", meta["slug"]):
        sys.exit(f"{path}: slug는 영문 소문자·숫자·하이픈만 씁니다")
    body = subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "html5"],
        input=text[m.end():], capture_output=True, text=True, check=True,
    ).stdout
    # 한글 바로 옆의 따옴표·괄호에 붙은 **굵게**는 CommonMark에서 풀리지 않는다.
    # 그대로 배포되지 않도록 막고, 원고에서 <strong>…</strong>으로 바꾸게 한다.
    leftover = re.sub(r"<(pre|code)>.*?</\1>", "", body, flags=re.S)
    if "**" in leftover:
        line = next(l for l in leftover.splitlines() if "**" in l)
        sys.exit(f"{path}: 굵게(**)가 변환되지 않았습니다 → <strong>으로 바꾸세요: {line.strip()[:80]}")
    return meta, body


def render(meta, body, root, url):
    date = meta.get("date", "")
    return PAGE.format(
        root=root,
        title=html.escape(meta["title"]),
        description=html.escape(meta["description"]),
        url=url,
        meta_line=f'<p class="price">{html.escape(date)}</p>' if date else "",
        body=body,
    )


def main():
    urls = [SITE_URL, SITE_URL + "blog/"]

    for path in sorted((ROOT / "automation/pages").glob("*.md")):
        meta, body = parse(path)
        url = SITE_URL + meta["slug"] + ".html"
        (DOCS / f"{meta['slug']}.html").write_text(render(meta, body, "", url), encoding="utf-8")
        urls.append(url)

    posts = []
    for path in (ROOT / "automation/posts").glob("*.md"):
        meta, body = parse(path)
        url = SITE_URL + "blog/" + meta["slug"] + ".html"
        (DOCS / "blog" / f"{meta['slug']}.html").write_text(render(meta, body, "../", url), encoding="utf-8")
        posts.append(meta)
        urls.append(url)

    posts.sort(key=lambda p: p.get("date", ""), reverse=True)
    items = "\n".join(
        f'<a href="{p["slug"]}.html">{html.escape(p["title"])}'
        f'<small>{html.escape(p.get("date", ""))} · {html.escape(p["description"])}</small></a>'
        for p in posts
    )
    (DOCS / "blog" / "index.html").write_text(INDEX.format(items=items), encoding="utf-8")

    sitemap = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    (DOCS / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{sitemap}\n</urlset>\n",
        encoding="utf-8",
    )
    print(f"pages built, {len(posts)} posts, {len(urls)} urls in sitemap")


if __name__ == "__main__":
    main()
