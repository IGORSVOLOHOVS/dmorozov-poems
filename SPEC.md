# dmorozov-poems — Software Requirements Specification

Reverse-engineered from the code at commit `222bd72` (branch `release`), 2026-11-20.
It describes what the files do, not what they were meant to do. The documentation
hub is [`docs/README.md`](docs/README.md).

## 1. Purpose and scope

The repository produces a static, single-page website in Russian that presents 50
poems first published by their author on stihi.ru, with a short "about the author"
section and a portrait (`README.md`, `scripts/build_site.py`).

In scope:

- `scripts/fetch_poems.py` — downloads a fixed list of poems from stihi.ru into `data/poems.json`.
- `scripts/build_site.py` — renders `index.html` from `data/poems.json`.
- `index.html`, `css/style.css`, `js/main.js`, `images/denis-portrait.jpg` — the page as served.
- `run_fetch_poems.bat` — a Windows launcher for the fetch script.

Out of scope:

- Hosting. The README says GitHub Pages serves the `main` branch of the GitHub copy;
  no file in the repository configures it (`README.md`). The GitHub API reports Pages
  built from `main`, path `/`, last build from `fcfb8f4` on 2026-08-07 (checked 2026-11-20).
- The poems' wording and the rights to them: they belong to their author, and the
  repository has no licence on purpose (`README.md`, section "License").
- The lab tooling (`recipe.ps1`, `.claude/`, `.gitea/`), apart from FR-23.

## 2. Context

| Actor / system | Role | Evidence |
|---|---|---|
| Maintainer | Runs the two scripts on their own machine and commits the results | `scripts/fetch_poems.py:12-13`, `README.md` |
| Reader | Opens `index.html` in a web browser | `scripts/build_site.py:106-161` |
| stihi.ru | Source of the poem pages, fetched over HTTPS | `scripts/fetch_poems.py:23,82-88` |
| Google Fonts | Serves the Lora and Playfair Display fonts to the reader's browser | `scripts/build_site.py:113-115` |
| GitHub Pages | Hosting, from branch `main` | `README.md`; GitHub API `repos/…/pages` (checked 2026-11-20) |

Runtime: Python 3 for the scripts (`#!/usr/bin/env python3`, `scripts/*.py:1`); any
browser with `localStorage` and `matchMedia` for the page (`js/main.js:8,17`). The
`.bat` launcher and `recipe.ps1` indicate a Windows maintainer machine (inference).

## 3. Functional requirements

All verifications are manual: the repository has no tests for its own code
(`.claude/pytest.ini`; `pytest --collect-only` finds none). "A-n" refers to section 8.

### 3.1 Fetching poems (`scripts/fetch_poems.py`)

- **FR-1.** The system shall request each of the 50 entries of `POEMS`, in list order, as an HTTP GET of `BASE + path` with the `User-Agent` from `HEADERS` and a 15 s timeout.
  Source: `scripts/fetch_poems.py:23-24,28-79,82-86,114-119`. Verification: no test (A-4).
- **FR-2.** The system shall decode every response as windows-1251, replacing undecodable bytes.
  Source: `scripts/fetch_poems.py:87-88`. Verification: no test (A-4).
- **FR-3.** The system shall take the poem text from the first `<div class="text">` up to the first `</div>`, turning `<br>` into newlines, removing other tags, unescaping HTML entities, trimming each line and removing leading and trailing newlines.
  Source: `scripts/fetch_poems.py:98-107`. Verification: no test (A-1).
- **FR-4.** The system shall take the title from the first `<h1>` with tags removed, entities unescaped and whitespace trimmed, and use the title from `POEMS` when the `<h1>` is missing or empty or the request failed.
  Source: `scripts/fetch_poems.py:91-95,117,121`. Verification: no test.
- **FR-5.** The system shall wait `DELAY_SECONDS` (1.5 s) after each request except the last.
  Source: `scripts/fetch_poems.py:25,137-138`. Verification: no test.
- **FR-6.** The system shall, when a request raises an exception or the page yields no text, record the poem id as failed, keep the poem in the output with `"text": ""`, and continue with the next poem.
  Source: `scripts/fetch_poems.py:116-135`. Verification: no test.
- **FR-7.** The system shall write all entries, failed ones included, as a UTF-8 JSON array (`ensure_ascii=False`, indent 2) to `data/poems.json` under the repository root found from the script's own path, creating `data/` if needed and replacing the previous file.
  Source: `scripts/fetch_poems.py:140-146`. Verification: no test (A-1).
- **FR-8.** The system shall print `[i/N] <id> ...` per poem, a warning or error line per failure, `Done: <ok>/<N> poems fetched with text -> <path>`, and the failed ids, all to stderr.
  Source: `scripts/fetch_poems.py:115,123,126,148-151`. Verification: no test (A-4).
- **FR-9.** `run_fetch_poems.bat` shall change to its own directory, run `python scripts\fetch_poems.py` and wait for a key press.
  Source: `run_fetch_poems.bat:2-4`. Verification: no test.

### 3.2 Building the page (`scripts/build_site.py`)

- **FR-10.** The system shall read `data/poems.json` and write `index.html` (UTF-8), both under the repository root found from the script's own path, and print `Wrote <path> (<n> poems)`.
  Source: `scripts/build_site.py:95-100,163-167`. Verification: no test (A-2).
- **FR-11.** The system shall treat a run of exactly two newlines in a poem's text as a line break and a run of three or more as a stanza break.
  Source: `scripts/build_site.py:37-46`. Verification: no test (A-2).
- **FR-12.** The system shall show each `YYYY-MM-DD` date as `<day> <Russian month in the genitive> <year>`, with the day without a leading zero.
  Source: `scripts/build_site.py:31-34,49-51`. Verification: no test (A-2).
- **FR-13.** The system shall render each poem, in file order, as `<article class="poem" id="<id>">` holding the escaped title in `<h2>`, a `<time datetime="<date>">`, one `<p>` per stanza with lines joined by `<br>`, and a link to the poem's `url` opening in a new tab.
  Source: `scripts/build_site.py:54-72,103`. Verification: no test (A-2).
- **FR-14.** The system shall render a table of contents with one entry per poem, in file order, linking to `#<id>` and showing the title and the formatted date, preceded by a link to `#about`.
  Source: `scripts/build_site.py:86-91,102,134-137`. Verification: no test (A-2).
- **FR-15.** The system shall render an "Об авторе" section with `id="about"` holding the image `AUTHOR_PHOTO` (alt text built from `AUTHOR_NAME`, 986 × 1280, `loading="lazy"`) and the escaped `AUTHOR_BIO`.
  Source: `scripts/build_site.py:20-29,75-83`. Verification: no test (A-2).
- **FR-16.** The system shall wrap the content in a page with `lang="ru"`, the title `SITE_TITLE — SITE_SUBTITLE`, a meta description, the Google Fonts and `css/style.css` links, a hero stating the number of poems, a footer linking to `AUTHOR_PROFILE_URL`, the theme, menu and back-to-top buttons, and `js/main.js` at the end of the body.
  Source: `scripts/build_site.py:106-161`. Verification: no test (A-2).

### 3.3 Page behaviour (`js/main.js`, `css/style.css`)

- **FR-17.** The page shall, when its script loads, apply a theme stored under the `localStorage` key `dmorozov-poems-theme` if the value is `light` or `dark`, by setting `data-theme` on `<html>`.
  Source: `js/main.js:5-12,26`. Verification: no test (A-3).
- **FR-18.** The theme button shall switch between light and dark, store the choice under the same key, and show ☀ with the label "Включить светлую тему" in the dark theme or ☽ with "Включить тёмную тему" in the light one.
  Source: `js/main.js:14-37`. Verification: no test (A-3).
- **FR-19.** The page shall use the dark palette when no theme is chosen and the system prefers a dark scheme.
  Source: `css/style.css:19-39`, `js/main.js:17`. Verification: no test (A-3).
- **FR-20.** On screens up to 860 px wide the ☰ button shall open the table of contents as a drawer over a dimmed background, and a click on the background or on any link in the drawer shall close it.
  Source: `js/main.js:40-63`, `css/style.css:345-377`. Verification: no test (A-3).
- **FR-21.** The ↑ button shall become visible when the page is scrolled more than 600 px and shall scroll smoothly to the top when clicked.
  Source: `js/main.js:65-78`, `css/style.css:327-342`. Verification: no test (A-3).
- **FR-22.** The layout shall show the table of contents as a sticky left column above 860 px, show the top bar only up to 860 px, and stack the portrait above the biography up to 560 px.
  Source: `css/style.css:75-84,259-269,345-397`. Verification: no test (A-3).

### 3.4 Repository interface

- **FR-23.** `recipe.ps1` shall follow the lab standard (repo-quality-template, revision 4.0.0 of the lab requirements per `README.md`): `info` prints name, code, version and summary; `test` runs pytest and ruff over `.claude` only; `clean` deletes cache folders; `build`, `install`, `uninstall`, `run` and `publish` print `nothing to <verb>`.
  Source: `recipe.ps1:9-12,40-74`. Verification: no test; `.\recipe.ps1 info` and `run` were run (A-5).

### 3.5 Declared but not implemented

| Statement | Where | What the code does |
|---|---|---|
| "Fetches all poems by the author" | `scripts/fetch_poems.py:3` | Fetches only the 50 listed entries; nothing reads the author page (`:28-79`) |
| "Run from the repo root so that data/poems.json ends up in the right place" | `scripts/fetch_poems.py:9-10` | The output path comes from the script's own location (`:140-144`) |
| `POEMS` holds the "title as listed on the author page" | `scripts/fetch_poems.py:27` | None of the 50 titles in `POEMS` equals the title stored for the same id in `data/poems.json` |
| "полное собрание" (the complete collection) | `scripts/build_site.py:112` | No check of completeness exists |
| "от ранних до последних" (from the earliest to the latest) | `scripts/build_site.py:144` | Poems appear in `POEMS` order, newest first |
| A close button for the drawer | `scripts/build_site.py:131`, `js/main.js:43,56` | Rendered with `display:none` and no text, so it is never visible |
| First line of each poem in the table of contents | `scripts/build_site.py:87` | Inference: `first_line` is computed and never used |

## 4. Interfaces

### 4.1 Command line

| Command | Arguments | Output | Exit status | Source |
|---|---|---|---|---|
| `python scripts/fetch_poems.py` | none | stderr: progress and summary; file `data/poems.json` | 0, also when poems failed; non-zero only on an uncaught error such as a failed write (inference: no `sys.exit` call) | `README.md`, `scripts/fetch_poems.py:110-155` |
| `run_fetch_poems.bat` | none | as above, then `pause` | 0 even when Python fails, because `pause` comes last (checked 2026-11-20 with a copy of the launcher whose Python step exits 3, input from `nul`) | `run_fetch_poems.bat` |
| `python scripts/build_site.py` | none | stdout: `Wrote <path> (<n> poems)`; file `index.html` | non-zero on a missing or malformed `data/poems.json`, a missing key or a malformed date (inference: no error handling) | `README.md`, `scripts/build_site.py:94-171` |
| `.\recipe.ps1 <verb>` | `build`, `install`, `uninstall`, `clean`, `run`, `publish`, `info`, `test` | see FR-23 | 0 or 1 | `recipe.ps1:1-7,40-74` |

### 4.2 Outgoing HTTP

| Method | URL | Headers | Timeout | Expected content |
|---|---|---|---|---|
| GET | `https://stihi.ru/<YYYY>/<MM>/<DD>/<n>` | `User-Agent` from `HEADERS` | 15 s | windows-1251 HTML with `<h1>` and `<div class="text">` |

Source: `scripts/fetch_poems.py:23-24,82-107`. Redirects are followed by `urllib` defaults (inference).

### 4.3 Page structure shared by `build_site.py`, `main.js` and `style.css`

| Hook | Element | Rendered at | Used at |
|---|---|---|---|
| `data-theme-toggle` | theme button | `scripts/build_site.py:126` | `js/main.js:29` |
| `data-nav-open` | ☰ button in the top bar | `scripts/build_site.py:121` | `js/main.js:42` |
| `data-nav` | table-of-contents `<nav>` | `scripts/build_site.py:130` | `js/main.js:40`, class `is-open` at `css/style.css:358` |
| `data-nav-scrim` | dimmed background | `scripts/build_site.py:127` | `js/main.js:41`, class `is-visible` at `css/style.css:371` |
| `data-nav-close` | hidden close button | `scripts/build_site.py:131` | `js/main.js:43` |
| `data-to-top` | ↑ button | `scripts/build_site.py:156` | `js/main.js:65`, class `is-visible` at `css/style.css:338` |
| `data-theme` on `<html>` | `light` or `dark` | `js/main.js:10,34` | `css/style.css:19,30` |
| `#about`, `#<poem id>` | anchors | `scripts/build_site.py:63,77` | table of contents (`:89,134`) |

Browser storage: `localStorage["dmorozov-poems-theme"]`, values `light` or `dark` (`js/main.js:5,35`).

## 5. Data

`data/poems.json` — UTF-8 JSON array, one object per poem (`scripts/fetch_poems.py:129-135`):

| Field | Type | Meaning |
|---|---|---|
| `id` | string | `YYYY-MM-DD-NNNN`, the date plus the stihi.ru number padded to four digits (path `2024/01/20/221` gives `2024-01-20-0221`, `scripts/fetch_poems.py:45`); used as the HTML anchor |
| `title` | string | From the page's `<h1>`, or the `POEMS` title as a fallback |
| `date` | string | `YYYY-MM-DD`, taken from `POEMS`, not from the page |
| `url` | string | `https://stihi.ru/<path>` |
| `text` | string | Lines separated by `\n`; see FR-11 for how runs of newlines are read; `""` after a failure |

Committed content, checked 2026-11-20: 50 objects, unique ids, same order, dates and URLs
as `POEMS`, no empty text, no duplicate titles, dates from 2023-04-05 to 2025-05-22 in
descending order, longest run of newlines 6.

Other artefacts: `index.html` (generated, 1785 lines, stored with LF); `images/denis-portrait.jpg`
(JPEG, 986 × 1280, 167054 bytes; a Git LFS pointer in history since `b90b857`, `.gitattributes:10`).

## 6. Non-functional requirements

- **NFR-1.** Both scripts shall use only the Python standard library. Source: `scripts/fetch_poems.py:9,15-21`, `scripts/build_site.py:9,11-14`.
- **NFR-2.** The fetch shall send one request at a time with a 1.5 s pause, 50 requests per run, each limited to 15 s. Source: `scripts/fetch_poems.py:12-13,25,85,137-138`.
- **NFR-3.** Output files shall be UTF-8, with non-ASCII characters kept as is in the JSON. Source: `scripts/fetch_poems.py:145-146`, `scripts/build_site.py:164`.
- **NFR-4.** Titles, poem lines and the biography shall be HTML-escaped; `id`, `date` and `url` are inserted unescaped. Source: `scripts/build_site.py:58,63-71,81,89-90`.
- **NFR-5.** Icon buttons shall carry `aria-label`s, the portrait an `alt` text and fixed dimensions, and the document `lang="ru"`. Source: `scripts/build_site.py:78,107,121,126,131,156`, `js/main.js:23`.
- **NFR-6.** The page shall load its own assets by relative paths. Source: `scripts/build_site.py:21,116,158`.
- **NFR-7.** The build output shall depend only on `data/poems.json` and the script's constants (inference: no clock, randomness or environment is read in `scripts/build_site.py`; a rebuild on 2026-11-20 matched the committed `index.html` apart from line endings).
- **NFR-8.** Text files shall be stored with LF and checked out with LF, except `.ps1`, `.bat` and `.cmd`, which are stored with LF and checked out with CRLF; `*.jpg`, `*.png`, `*.pdf`, `*.zip`, `*.7z` go through Git LFS. Source: `.gitattributes:1-4,8-12`; `git ls-files --eol` shows `i/lf w/crlf` for `recipe.ps1` and `run_fetch_poems.bat`.
- **NFR-9.** The page text and the poems shall stay in Russian, untranslated. Source: `README.md` (R-37 exception), `scripts/build_site.py:107`.

## 7. Constraints and dependencies

| Dependency | Version | Where needed | Source |
|---|---|---|---|
| Python 3 | not pinned; the build was run with 3.13.3 | both scripts | `scripts/*.py:1` |
| stihi.ru | — | fetch only | `scripts/fetch_poems.py:23` |
| Google Fonts: Lora (400, 500, italic 400), Playfair Display (600, 700) | — | reader's browser; fallbacks Georgia, Times New Roman, serif | `scripts/build_site.py:115`, `css/style.css:3-4` |
| Windows `cmd` | — | `run_fetch_poems.bat` | `run_fetch_poems.bat` |
| Git LFS | — | checking out the portrait | `.gitattributes:10` |
| PowerShell, pytest, ruff `==0.16.1` | pytest not pinned | `recipe.ps1 test` | `recipe.ps1:46-52`, `.claude/ruff.toml` |

There is no requirements or lock file. No licence applies: rights stay with the author (`README.md`).

## 8. Acceptance

- **A-1 (FR-3, FR-6, FR-7).** `data/poems.json` holds 50 objects with exactly the keys of section 5, unique ids, the same order, dates and URLs as `POEMS`, and no empty `text`.
- **A-2 (FR-10 – FR-16).** `python scripts/build_site.py` (`README.md`) prints `Wrote … (50 poems)`, and the new `index.html` equals the committed one apart from line endings; it holds 50 `<article class="poem"` elements.
- **A-3 (FR-17 – FR-22).** In a browser: the theme button switches the theme and the choice survives a reload; with no stored choice the system scheme applies; at 860 px or narrower ☰ opens the drawer and a click on the background or a link closes it; after 600 px of scrolling ↑ appears and returns to the top; at 560 px or narrower the portrait sits above the biography.
- **A-4 (FR-1, FR-2, FR-5, FR-8).** With network access, `python scripts/fetch_poems.py` (`README.md`) ends with `Done: 50/50 poems fetched with text` and no `Failed or empty` line, and then A-1 holds.
- **A-5 (FR-23).** `.\recipe.ps1 info` prints the name, code `dp`, version `1.0.0` and the summary, and exits 0.

A-1, A-2 and A-5 were checked on 2026-11-20. A-3 and A-4 were not run.

## 9. Open questions

1. Who the intended readers are, and whether the author agreed to the republication. The README states that rights stay with the author; commit `73a3912` says the portrait and biographical facts were provided by the repository owner. No consent is recorded.
2. Which first name is correct: the page title says Dmitry, the "about" section says Denis (`README.md`, `scripts/build_site.py:16,20`).
3. Answered: GitHub Pages is enabled and serves `main`, path `/`; its last build is from `fcfb8f4` (2026-08-07), status `built` (GitHub API, checked 2026-11-20). Still open: how `release` and `test` reached the GitHub copy is not recorded, although the README says nothing pushes there from the Gitea copy.
4. Whether GitHub Pages would serve the portrait if its source were switched to `release`, where the image is a Git LFS pointer. Not checked; today it serves `main`, where the image is the JPEG itself.
5. How the list of 50 poems was compiled, whether it is the author's complete list, and where the `POEMS` titles come from, since none matches the stored titles.
6. Whether a fetch with failures should exit non-zero or keep the previous text instead of writing `""` (FR-6, FR-7 describe the current behaviour only).
7. The minimum Python version and the supported browsers. Neither is stated.
8. Whether a Gitea runner serves `.gitea/workflows/` for this repository (`CLAUDE.md` covers both cases).
9. Whether the hero wording "от ранних до последних" or the newest-first order is the intended one.
