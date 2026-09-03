# Integración walk-forward y colas

## Cambios aplicados

- Se añadió una subsección breve en resultados con el diseño expanding de 9 folds, los Sharpe medios y el resultado de 5 de 9 folds favorables al VAE.
- Se incorporó el análisis de colas y estrés: CVaR 95 %, comparación de distribución y ausencia de escenarios tan severos como los peores días equiponderados de 2018 y COVID-19.
- Se añadieron menciones mínimas en conclusiones, limitaciones y capítulo 6 para documentar scripts y artefactos.

## Cambios preservados

- El split 80/20, sus métricas, la arquitectura, el título, la estructura general y la bibliografía permanecen sin cambios.
- Se mantiene una interpretación prudente: la extensión no demuestra superioridad general del VAE.

## Compilación

- Comandos ejecutados desde `latex/`: `pdflatex -interaction=nonstopmode -halt-on-error main.tex`, `bibtex main` y dos pasadas finales de `pdflatex`.
- Resultado: correcto; PDF generado sin errores fatales, citas indefinidas ni referencias indefinidas. Se mantienen únicamente advertencias tipográficas no fatales del estilo y del documento.
- PDF: `latex/main.pdf`.
