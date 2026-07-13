#!/usr/bin/env python3
"""
Fetches all poems by the author "dmorozov" from stihi.ru and writes them to
data/poems.json for use by the static site.

Usage:
    python scripts/fetch_poems.py

No third-party dependencies required (stdlib only). Run from the repo root
so that data/poems.json ends up in the right place.

Run this yourself, locally — it makes 50 individual, polite (rate-limited)
GET requests to stihi.ru with a short delay between each.
"""
import json
import os
import re
import sys
import time
import urllib.request
from html import unescape

BASE = "https://stihi.ru/"
HEADERS = {"User-Agent": "Mozilla/5.0 (personal-archive-script; contact: owner of the poems)"}
DELAY_SECONDS = 1.5

# (id, title as listed on the author page, date, url path)
POEMS = [
    ("2025-05-22-7092", "Для всех другой путник", "2025-05-22", "2025/05/22/7092"),
    ("2024-09-22-2510", "Сердцем слышу", "2024-09-22", "2024/09/22/2510"),
    ("2024-06-22-6188", "Понимаю, прощаю", "2024-06-22", "2024/06/22/6188"),
    ("2024-06-18-5374", "Прошепчу", "2024-06-18", "2024/06/18/5374"),
    ("2024-06-15-5093", "На согласие", "2024-06-15", "2024/06/15/5093"),
    ("2024-06-15-5069", "Ни ни люди люди", "2024-06-15", "2024/06/15/5069"),
    ("2024-06-15-5047", "Новый мир сознанья", "2024-06-15", "2024/06/15/5047"),
    ("2024-05-29-6613", "Вознесенья путь", "2024-05-29", "2024/05/29/6613"),
    ("2024-05-25-5034", "В новом свете", "2024-05-25", "2024/05/25/5034"),
    ("2024-05-14-5584", "Конец", "2024-05-14", "2024/05/14/5584"),
    ("2024-05-14-5567", "Отражение", "2024-05-14", "2024/05/14/5567"),
    ("2024-04-22-7375", "В реальном мире", "2024-04-22", "2024/04/22/7375"),
    ("2024-04-22-7305", "В движении", "2024-04-22", "2024/04/22/7305"),
    ("2024-04-22-7236", "Адорас", "2024-04-22", "2024/04/22/7236"),
    ("2024-01-25-8356", "Новая земля", "2024-01-25", "2024/01/25/8356"),
    ("2024-01-22-8120", "Контроль", "2024-01-22", "2024/01/22/8120"),
    ("2024-01-20-0221", "Нежданный день будущем на", "2024-01-20", "2024/01/20/221"),
    ("2024-01-03-5863", "В толще холодных льдов", "2024-01-03", "2024/01/03/5863"),
    ("2024-01-02-6173", "Судьба", "2024-01-02", "2024/01/02/6173"),
    ("2024-01-02-4569", "Новый день", "2024-01-02", "2024/01/02/4569"),
    ("2024-01-02-4504", "Помощь", "2024-01-02", "2024/01/02/4504"),
    ("2023-12-25-7834", "Воскрешение", "2023-12-25", "2023/12/25/7834"),
    ("2023-12-25-7764", "Самоспасение", "2023-12-25", "2023/12/25/7764"),
    ("2023-12-18-7974", "Самоуничтожения", "2023-12-18", "2023/12/18/7974"),
    ("2023-12-16-7678", "Древние боги времени", "2023-12-16", "2023/12/16/7678"),
    ("2023-12-05-6439", "Вечная ночь, вечная луна", "2023-12-05", "2023/12/05/6439"),
    ("2023-12-03-8231", "Луна новая на иверском", "2023-12-03", "2023/12/03/8231"),
    ("2023-12-03-8120", "Новое воплощение", "2023-12-03", "2023/12/03/8120"),
    ("2023-12-03-8071", "Новое для себя", "2023-12-03", "2023/12/03/8071"),
    ("2023-11-21-8293", "Сияние", "2023-11-21", "2023/11/21/8293"),
    ("2023-11-14-7076", "Отделение от иллюзии", "2023-11-14", "2023/11/14/7076"),
    ("2023-11-06-8003", "Огонь, страдание", "2023-11-06", "2023/11/06/8003"),
    ("2023-11-03-5889", "Небольшая ночь", "2023-11-03", "2023/11/03/5889"),
    ("2023-10-28-6833", "Мечтать немного", "2023-10-28", "2023/10/28/6833"),
    ("2023-10-20-7643", "Дела", "2023-10-20", "2023/10/20/7643"),
    ("2023-10-10-5406", "Три дня", "2023-10-10", "2023/10/10/5406"),
    ("2023-10-10-5289", "Мв идеальное воплощение на", "2023-10-10", "2023/10/10/5289"),
    ("2023-09-24-6611", "Новый день", "2023-09-24", "2023/09/24/6611"),
    ("2023-09-24-6492", "Для всех другой путник", "2023-09-24", "2023/09/24/6492"),
    ("2023-09-24-6446", "В знак ко встречам", "2023-09-24", "2023/09/24/6446"),
    ("2023-09-04-7277", "Печальное письмо", "2023-09-04", "2023/09/04/7277"),
    ("2023-07-30-7050", "Для жизни пожеланием", "2023-07-30", "2023/07/30/7050"),
    ("2023-07-30-6922", "Начинают жизнь", "2023-07-30", "2023/07/30/6922"),
    ("2023-07-30-6896", "Понимая, обучаясь, развиваясь судьба", "2023-07-30", "2023/07/30/6896"),
    ("2023-07-30-6870", "От реалии об состояния снов", "2023-07-30", "2023/07/30/6870"),
    ("2023-07-30-6840", "Отговори, луна", "2023-07-30", "2023/07/30/6840"),
    ("2023-04-28-7756", "Но - это противящее явление", "2023-04-28", "2023/04/28/7756"),
    ("2023-04-28-7728", "Люди об лице скрывает для меня", "2023-04-28", "2023/04/28/7728"),
    ("2023-04-28-7686", "В жилище слова суетно", "2023-04-28", "2023/04/28/7686"),
    ("2023-04-05-5766", "Новое об лице скрывав", "2023-04-05", "2023/04/05/5766"),
]


def fetch(path):
    url = BASE + path
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read()
    # stihi.ru serves pages as windows-1251
    return raw.decode("windows-1251", errors="replace")


def extract_title(html_content):
    m = re.search(r"<h1>(.*?)</h1>", html_content, re.S)
    if not m:
        return ""
    return unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()


def extract_text(html_content):
    m = re.search(r'<div class="text">(.*?)</div>', html_content, re.S)
    if not m:
        return ""
    block = m.group(1)
    block = re.sub(r"<br\s*/?>", "\n", block)
    block = re.sub(r"<[^>]+>", "", block)
    block = unescape(block)
    lines = [line.strip() for line in block.split("\n")]
    return "\n".join(lines).strip("\n")


def main():
    results = []
    failed = []

    for i, (poem_id, title, date, path) in enumerate(POEMS, 1):
        print(f"[{i}/{len(POEMS)}] {poem_id} ...", file=sys.stderr)
        text = ""
        page_title = title
        try:
            html_content = fetch(path)
            text = extract_text(html_content)
            page_title = extract_title(html_content) or title
            if not text:
                print("  warning: no text found on page", file=sys.stderr)
                failed.append(poem_id)
        except Exception as e:
            print(f"  ERROR: {e}", file=sys.stderr)
            failed.append(poem_id)

        results.append({
            "id": poem_id,
            "title": page_title,
            "date": date,
            "url": BASE + path,
            "text": text,
        })

        if i < len(POEMS):
            time.sleep(DELAY_SECONDS)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    out_dir = os.path.join(repo_root, "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "poems.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    ok = len(results) - len(failed)
    print(f"\nDone: {ok}/{len(results)} poems fetched with text -> {out_path}", file=sys.stderr)
    if failed:
        print("Failed or empty: " + ", ".join(failed), file=sys.stderr)


if __name__ == "__main__":
    main()
