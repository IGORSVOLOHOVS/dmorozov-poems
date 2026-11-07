# dmorozov-poems

A static site that collects 50 Russian poems first published by their author on
[stihi.ru](https://stihi.ru/avtor/dmorozov). The poems are the author's own, not
Igors Volohovs's: this repository only presents them.

The page text and the poems are in Russian and stay that way. That is this
repository's R-37 exception: nobody translates someone else's poems here.

The site's title names the author Dmitry Morozov, as does the stihi.ru account.
Its "about the author" section calls him Denis.

## What is here

- `index.html` is the whole page. It is generated, so change it through
  `scripts/build_site.py`, not by hand.
- `css/style.css` and `js/main.js` are the style and the small script: the theme
  switch, the mobile menu and scrolling.
- `data/poems.json` holds the poems: id, title, date, source URL and text.
- `images/denis-portrait.jpg` is the portrait in the "about the author" section.
- `scripts/fetch_poems.py` downloads the poems it lists from stihi.ru into
  `data/poems.json`, one polite request at a time, and `run_fetch_poems.bat`
  starts it with a double click.
- `scripts/build_site.py` writes `index.html` from `data/poems.json`.

Both scripts need only Python's standard library, and there is no build step
beyond them:

```
python scripts/fetch_poems.py
python scripts/build_site.py
```

GitHub Pages serves the site from the `main` branch of the GitHub copy of this
repository. Nothing pushes from this Gitea copy to GitHub, so a change made here
does not reach that address by itself.

## Working on it

This repository ships no program. `.\recipe.ps1` is still its whole interface:
`.\recipe.ps1 test` runs pytest and ruff over `.claude`, and `.\recipe.ps1 info`
prints the metadata. The other verbs print `nothing to <verb>`. `CLAUDE.md`
holds the rules.

## License

None, on purpose. The poems and the portrait are another person's work, so all
rights stay with their owner, and a licence here is the author's decision. See
the R-18 exception below.

## Lab requirements

This repository complies with [revision 4.0.0](http://127.0.0.1:3000/igors-lab/software-requirements/src/tag/v4.0.0/BEST_REQUIREMENTS.md) of the lab requirements, except R-02 (#7), R-09 (#8), R-18 (#9), R-37 (#10), R-41 (#11), R-42 (#12).
