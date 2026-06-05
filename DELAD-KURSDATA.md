# Delad kursdata mellan boken och handledarhandboken

`kursdata.yml` i detta repo är **den enda källan** för fakta som måste vara
identiska i både uppsatskursboken och handledarhandboken (`supervisor-handbook`):
ordgränser, delade nyckeldatum, termin/läsår. Båda sajterna är nu **MkDocs** med
`mkdocs-macros`, så delningen är enkel och ser likadan ut på båda håll.

## Hur bok-sidan fungerar (klart och i drift)

- `main.py` läser `kursdata.yml` och exponerar den för macros.
- Använd i Markdown: `{{ ordgrans("master") }}` → "11 000",
  `{{ datum("pm_inlamning") }}` → "20 januari 2026 kl 13:00",
  `{{ aktuell_termin }}`, eller direkt `{{ kd.ordgranser.master }}`.
- Byt kursomgång: lägg ett nytt block under `terminer:` i `kursdata.yml` och
  ändra `aktuell_nyckel`.

## Plan för handboks-sidan (EJ tillämpad — körs separat när du vill)

Mål: handboken läser samma `kursdata.yml` i stället för att ha egna kopior av
ordgränser/datum i `mkdocs.yml`. Handboken är **privat**, boken **publik**, så
handboken hämtar filen via den publika råa URL:en:

```
https://raw.githubusercontent.com/gisela/uppsatskurs/main/kursdata.yml
```

### Steg 1 — Hämta filen i handbokens CI

I `supervisor-handbook/.github/workflows/deploy.yml`, lägg ett steg **före**
`mkdocs build`:

```yaml
- name: Hämta delad kursdata
  run: curl -fsSL -o kursdata.yml \
       https://raw.githubusercontent.com/gisela/uppsatskurs/main/kursdata.yml
```

### Steg 2 — Läs filen i handbokens macros

Handboken har ingen `main.py` ännu (den använder bara `extra:`). Lägg till en
`main.py` i handboks-roten som skriver över de **delade** nycklarna med värden
från `kursdata.yml` — behåll handbokens befintliga nyckelnamn så inga `{{ }}`
behöver ändras:

```python
from pathlib import Path
import yaml

def define_env(env):
    f = Path("kursdata.yml")
    if not f.exists():
        return  # fallback: värden i mkdocs.yml extra: används
    kd = yaml.safe_load(f.read_text(encoding="utf-8"))
    wc = env.variables.setdefault("course_settings", {}).setdefault("word_count", {})
    wc["master"] = kd["ordgranser"]["master"]
    wc["magister"] = kd["ordgranser"]["magister"]
    wc["include_references"] = kd["ordgranser"]["inkludera_referenser"]
    env.variables["academic_year"] = kd["lasar"]
    env.variables["term"] = kd["aktuell_termin"]
    # Datum: mappa kd["terminer"][aktuell_nyckel] → handbokens master.<nyckel>.date
```

### Steg 3 — Ta bort dubbletterna ur handbokens `mkdocs.yml`

När mappningen är på plats: ta bort `course_settings.word_count`,
`academic_year`, `term` och de delade datumen ur `extra:`. **Behåll** allt
känsligt/privat (kontakter, zoom-länkar, statistik, handledarlistor) — det ska
aldrig ligga i den publika `kursdata.yml`.

### Att bestämma när vi tar handboks-sidan

- **Datum-mappningen** (Steg 2, sista raden): handboken har en rikare
  datumstruktur (`.date`, `.day`, `.zoom_url`). Vi avgör då vilka datum som är
  delade vs förblir privata.
- **Fetch vs incheckad kopia:** CI-hämtning (ovan) är enklast. Alternativ:
  git submodul/subtree om du hellre vill ha filen incheckad i båda repon.
