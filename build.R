#!/usr/bin/env Rscript
# Bygger boken till ./docs (för GitHub Pages).
# Kör med:  Rscript build.R   eller  source("build.R")
bookdown::render_book("index.Rmd", output_format = "bookdown::gitbook")
