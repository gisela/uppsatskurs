# Tidsplan

En översikt över kursens viktigaste datum för **{{ aktuell_termin }}**.
Alla datum hämtas automatiskt från kursens gemensamma datafil (`kursdata.yml`)
— samma källa som handledarhandboken är tänkt att använda.

| Datum | Moment |
|-------|--------|
| **{{ datum("pm_inlamning") }}** | PM-inlämning |
| **{{ datum("ideventilering_inlamning") }}** | Inlämning för halvtidsseminarium |
| **{{ datum("handledare_godkannande", med_tid=False) }}** | Handledargodkännande |
| **{{ datum("opponering_inlamning") }}** | Inlämning för opponering |
| **{{ datum("forsta_seminarium", med_tid=False) }}** | Första slutseminarium |
