"""mkdocs-macros: gör delade kursfakta från kursdata.yml tillgängliga i sidorna.

kursdata.yml är ENDA KÄLLAN för ordgränser, delade datum och termin — samma fil
som handledarhandboken (supervisor-handbook) är tänkt att läsa. Redigera värdena
där, aldrig hårdkodat i markdown. Se DELAD-KURSDATA.md.
"""
from pathlib import Path
import yaml

_MANADER = [
    "januari", "februari", "mars", "april", "maj", "juni",
    "juli", "augusti", "september", "oktober", "november", "december",
]


def _load():
    f = Path("kursdata.yml")
    return yaml.safe_load(f.read_text(encoding="utf-8")) if f.exists() else {}


def define_env(env):
    kd = _load()
    # Hela datan tillgänglig som {{ kd.ordgranser.master }} osv.
    env.variables["kd"] = kd
    env.variables["aktuell_termin"] = kd.get("aktuell_termin", "")
    env.variables["lasar"] = kd.get("lasar", "")

    _termin = kd.get("terminer", {}).get(kd.get("aktuell_nyckel"), {})

    @env.macro
    def ordgrans(niva):
        """Ordgräns med tusentalsavgränsare, t.ex. '11 000'."""
        return f"{kd['ordgranser'][niva]:,}".replace(",", " ")

    @env.macro
    def datum(nyckel, med_tid=True):
        """Formatera ett delat datum på svenska, t.ex. '20 januari 2026 kl 13:00'."""
        d = _termin[nyckel]
        y, m, day = d["datum"].split("-")
        txt = f"{int(day)} {_MANADER[int(m) - 1]} {y}"
        if med_tid:
            tid = d.get("tid", kd.get("inlamningstid"))
            if tid:
                txt += f" kl {tid}"
        return txt
