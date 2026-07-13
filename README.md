# Дмитрий Морозов — Стихотворения

Статичный сайт со стихотворениями, впервые опубликованными автором на [Стихи.ру](https://stihi.ru/avtor/dmorozov).

## Структура

- `index.html` — готовая статичная страница (сгенерирована из `data/poems.json`)
- `css/style.css`, `js/main.js` — стили и минимальный JS (тема, мобильное меню, скролл)
- `data/poems.json` — тексты стихотворений
- `scripts/fetch_poems.py` — скачивает тексты стихов с stihi.ru в `data/poems.json`
- `scripts/build_site.py` — генерирует `index.html` из `data/poems.json`
- `run_fetch_poems.bat` — запуск `fetch_poems.py` двойным кликом (Windows)

## Обновление контента

Если у автора появились новые стихи:

```
python scripts/fetch_poems.py   # обновит data/poems.json
python scripts/build_site.py    # пересоберёт index.html
```

Никаких сборщиков и внешних зависимостей не требуется (только стандартная библиотека Python).

## Публикация

Сайт полностью статический — подходит для GitHub Pages без какой-либо сборки: просто раздать содержимое репозитория как есть (ветка `main`, корень `/`).
