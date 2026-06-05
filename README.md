# Uppsatskurs

Kursbok/hemsida för uppsatskursen, byggd med [MkDocs](https://www.mkdocs.org/)
och [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) — samma
verktyg som handledarhandboken (`supervisor-handbook`).

📖 **Publicerad sida:** https://gisela.github.io/uppsatskurs/

## Jobba lokalt

```sh
pip install -r requirements.txt
mkdocs serve     # förhandsvisa på http://127.0.0.1:8000
mkdocs build     # bygg statisk sajt till ./site
```

Publicering sker automatiskt: vid push till `main` bygger och deployar
GitHub Actions (`.github/workflows/deploy.yml`) till GitHub Pages.

## Struktur

- `docs/` – innehållet (Markdown)
- `mkdocs.yml` – konfiguration, tema, navigering, plugins
- `main.py` – mkdocs-macros: läser in delade kursfakta från `kursdata.yml`
- `kursdata.yml` – **enda källan** för ordgränser och delade datum (se nedan)

## Delad kursdata

`kursdata.yml` är den gemensamma källan för fakta som måste vara identiska i
både denna bok och handledarhandboken (ordgränser, nyckeldatum, termin).
Använd den i sidorna via macros, t.ex. `{{ ordgrans("master") }}` eller
`{{ datum("pm_inlamning") }}`. Redigera värdena där — aldrig hårdkodat.
Se [DELAD-KURSDATA.md](DELAD-KURSDATA.md).
