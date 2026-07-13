#!/usr/bin/env python3
"""
Generates index.html from data/poems.json.

Usage:
    python scripts/build_site.py

Run this after data/poems.json changes (e.g. after re-running fetch_poems.py)
to regenerate the static index.html. No third-party dependencies.
"""
import json
import os
import re
from html import escape

SITE_TITLE = "Дмитрий Морозов"
SITE_SUBTITLE = "Стихотворения"
AUTHOR_PROFILE_URL = "https://stihi.ru/avtor/dmorozov"

MONTHS_RU = [
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря",
]


def normalize_poem_text(text):
    """Collapses the doubled-newline artifacts left by fetch_poems.py's
    <br> + source-newline extraction into clean line/stanza breaks:
    a run of exactly 2 newlines is a line break, a run of 3+ is a stanza break."""
    def repl(m):
        return "\x00" if len(m.group(0)) >= 3 else "\n"

    text = re.sub(r"\n{2,}", repl, text)
    text = text.replace("\x00", "\n\n")
    return text.strip("\n")


def format_date(iso_date):
    y, m, d = iso_date.split("-")
    return f"{int(d)} {MONTHS_RU[int(m) - 1]} {y}"


def poem_to_html(poem):
    stanzas = normalize_poem_text(poem["text"]).split("\n\n")
    paragraphs = []
    for stanza in stanzas:
        lines = [escape(line) for line in stanza.split("\n")]
        paragraphs.append("      <p>" + "<br>\n        ".join(lines) + "</p>")
    body = "\n".join(paragraphs)

    return f"""
    <article class="poem" id="{poem['id']}">
      <header class="poem__header">
        <h2 class="poem__title">{escape(poem['title'])}</h2>
        <time class="poem__date" datetime="{poem['date']}">{format_date(poem['date'])}</time>
      </header>
      <div class="poem__text">
{body}
      </div>
      <p class="poem__source">Впервые опубликовано на <a href="{poem['url']}" target="_blank" rel="noopener">Стихи.ру</a></p>
    </article>"""


def toc_entry(poem):
    first_line = normalize_poem_text(poem["text"]).split("\n", 1)[0]
    return f"""        <li>
          <a href="#{poem['id']}">{escape(poem['title'])}</a>
          <time datetime="{poem['date']}">{format_date(poem['date'])}</time>
        </li>"""


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    data_path = os.path.join(repo_root, "data", "poems.json")

    with open(data_path, encoding="utf-8") as f:
        poems = json.load(f)

    toc_html = "\n".join(toc_entry(p) for p in poems)
    poems_html = "\n".join(poem_to_html(p) for p in poems)

    page = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{SITE_TITLE} — {SITE_SUBTITLE}</title>
<meta name="description" content="Стихотворения {SITE_TITLE}: полное собрание, опубликованное на Стихи.ру.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;1,400&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body>

<div class="topbar">
  <button class="icon-btn" data-nav-open aria-label="Открыть оглавление">☰</button>
  <span class="topbar__title">{SITE_TITLE}</span>
  <span style="width:2.35rem"></span>
</div>

<button class="icon-btn theme-toggle" data-theme-toggle aria-label="Переключить тему"></button>
<div class="nav-scrim" data-nav-scrim></div>

<div class="shell">
  <nav class="site-nav" data-nav>
    <button class="icon-btn" data-nav-close aria-label="Закрыть оглавление" style="display:none"></button>
    <p class="site-nav__title">{SITE_TITLE}</p>
    <p class="site-nav__subtitle">{SITE_SUBTITLE}</p>
    <ul class="toc">
{toc_html}
    </ul>
  </nav>

  <main>
    <div class="content">
      <div class="hero">
        <h1>{SITE_SUBTITLE}</h1>
        <p>Собрание стихотворений {SITE_TITLE}, впервые опубликованных на Стихи.ру. {len(poems)} стихотворений, от ранних до последних.</p>
      </div>
{poems_html}

      <footer class="site-footer">
        <p>Все стихотворения принадлежат автору и впервые опубликованы на <a href="{AUTHOR_PROFILE_URL}" target="_blank" rel="noopener">Стихи.ру</a>.</p>
      </footer>
    </div>
  </main>
</div>

<button class="icon-btn to-top" data-to-top aria-label="Наверх">↑</button>

<script src="js/main.js"></script>
</body>
</html>
"""

    out_path = os.path.join(repo_root, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)

    print(f"Wrote {out_path} ({len(poems)} poems)")


if __name__ == "__main__":
    main()
