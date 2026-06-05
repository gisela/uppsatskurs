# Delad kursdata mellan boken och handledarhandboken

`kursdata.yml` i detta repo är **den enda källan** för fakta som måste vara
identiska i både uppsatskursboken (bookdown) och handledarhandboken
(`supervisor-handbook`, MkDocs): ordgränser, delade nyckeldatum, termin/läsår.

## Hur bok-sidan fungerar (klart och i drift)

- `index.Rmd` läser `kursdata.yml` i en setup-chunk → objektet `kd`.
- Hjälpare: `kd_ord("master")` ger "11 000", `kd_datum("pm_inlamning")` ger
  "20 januari 2026 kl 13:00".
- Kapitlen använder dessa i stället för hårdkodade värden.
- Byt kursomgång genom att lägga ett nytt block under `terminer:` och ändra
  `aktuell_nyckel`.

## Plan för handboks-sidan (EJ tillämpad — körs separat när du vill)

Mål: handboken ska läsa samma `kursdata.yml` i stället för att ha egna kopior
av ordgränser/datum i `mkdocs.yml`. Eftersom handboken är **privat** och boken
**publik** hämtar handboken filen via den publika råa URL:en:

```
https://raw.githubusercontent.com/gisela/uppsatskurs/main/kursdata.yml
```

### Steg 1 — Hämta filen i handbokens CI (rekommenderat, robust)

I `supervisor-handbook/.github/workflows/deploy.yml`, lägg ett steg **före**
`mkdocs build` som laddar ner källfilen till repo-roten:

```yaml
- name: Hämta delad kursdata
  run: curl -fsSL -o kursdata.yml \
       https://raw.githubusercontent.com/gisela/uppsatskurs/main/kursdata.yml
```

(För lokala bygg: kör samma curl, eller behåll en kopia som fallback.)

### Steg 2 — Låt macros läsa filen och fylla de befintliga variablerna

Skapa `supervisor-handbook/main.py` (mkdocs-macros plockar upp den automatiskt):

```python
import yaml
from pathlib import Path

def define_env(env):
    f = Path("kursdata.yml")
    if not f.exists():
        return  # fallback: värden i mkdocs.yml extra: används
    kd = yaml.safe_load(f.read_text(encoding="utf-8"))

    # Skriv över de DELADE värdena så de alltid speglar källan.
    # Behåll handbokens befintliga nyckelnamn så inga {{ }} behöver ändras.
    wc = env.variables.setdefault("course_settings", {}).setdefault("word_count", {})
    wc["master"] = kd["ordgranser"]["master"]
    wc["magister"] = kd["ordgranser"]["magister"]
    wc["include_references"] = kd["ordgranser"]["inkludera_referenser"]

    env.variables["academic_year"] = kd["lasar"]
    env.variables["term"] = kd["aktuell_termin"]
    # Datum: mappa kd$terminer[aktuell_nyckel] → handbokens master.<nyckel>.date
```

### Steg 3 — Ta bort dubbletterna ur `mkdocs.yml`

När macros-mappningen är på plats: ta bort `course_settings.word_count`,
`academic_year`, `term` och de delade datumen ur `extra:` i `mkdocs.yml`.
**Behåll** allt känsligt/privat (kontakter, zoom, statistik, handledarlistor).

### Resultat

Ordgränser och delade datum redigeras därefter på **exakt ett ställe**
(`kursdata.yml`). Felkällan "samma siffra på två ställen som driver isär"
försvinner. Den årliga uppdateringen blir: ändra `kursdata.yml` + handbokens
egna privata datum/kontakter.

### Att bestämma när vi tar handboks-sidan

- **Datum-mappningen** (Steg 2, sista raden): handboken har en rikare
  datumstruktur (`.date`, `.day`, `.zoom_url`). Vi avgör då vilka datum som är
  "delade" (kommer från `kursdata.yml`) och vilka som förblir privata.
- **Fetch vs incheckad kopia:** CI-hämtning (ovan) eller en `git`-baserad
  metod (submodul/subtree) om du hellre vill ha filen incheckad i båda repon.
