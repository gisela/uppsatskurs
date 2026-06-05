# Uppsatskurs

Kursbok/hemsida för uppsatskursen, byggd med [bookdown](https://bookdown.org/).

📖 **Publicerad sida:** https://gisela.github.io/uppsatskurs/

## Bygga boken lokalt

```r
# i R, från projektmappen
bookdown::render_book("index.Rmd")
```

eller från terminalen:

```sh
Rscript build.R
```

Resultatet hamnar i `docs/` och publiceras via GitHub Pages (gren `main`, mapp `/docs`).

## Struktur

- `index.Rmd` – bokens titel/metadata + välkomstsida
- `0X-*.Rmd` – ett kapitel per fil (ordning styrs i `_bookdown.yml`)
- `_bookdown.yml` – bokkonfiguration (kapitelordning, output_dir)
- `_output.yml` – utseende (gitbook-temat)
- `style.css` – egna stilar
- `build.R` – byggskript
