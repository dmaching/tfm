# Referencias adicionales: Merton y Engle

Fecha de comprobación: 23 de agosto de 2026.

## Referencias añadidas

- Merton, Robert C. (1972). «An Analytic Derivation of the Efficient Portfolio Frontier». *Journal of Financial and Quantitative Analysis*, 7(4), 1851–1872. Clave BibTeX: `merton1972analytic`.
- Engle, Robert F. (1982). «Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation». *Econometrica*, 50(4), 987–1007. Clave BibTeX: `engle1982autoregressive`.

## Archivos modificados

- `latex/bibliografia.bib`: incorporación de las dos entradas académicas.
- `latex/capitulos/03_marco_teorico.tex`: incorporación de dos frases breves con sus citas.
- `reports/referencias_extra_merton_engle.md`: presente informe.

No se modificaron resultados experimentales, tablas, métricas, título ni estructura UNIR.

## Ubicación de las citas

- Merton se cita en `Modelo de media-varianza de Markowitz`, inmediatamente después del párrafo que explica la representación de la frontera eficiente.
- Engle se cita en `Riesgo financiero y hechos estilizados`, después de la explicación de la volatilidad cambiante y su agrupamiento.

## Auditoría bibliográfica

- Número final de entradas BibTeX: **22**.
- Citas de Merton y Engle presentes en el cuerpo y resueltas en los archivos auxiliares.
- Claves BibTeX duplicadas: **0**.
- Títulos bibliográficos duplicados: **0**.
- Notas internas, comentarios editoriales o placeholders en la bibliografía: **0**.

## Compilación

- Se intentó primero la salida normal `main.pdf`, pero el archivo estaba bloqueado por el visor.
- Se completó correctamente la cadena `pdflatex` → `bibtex` → `pdflatex` → `pdflatex` con `-jobname=main_pulido`.
- PDF validado: `latex/main_pulido.pdf`, 80 páginas.
- El log final no contiene errores LaTeX, citas indefinidas, referencias indefinidas, `Overfull \hbox` ni `Overfull \vbox`.

## Warnings relevantes

Persisten avisos no bloqueantes ya existentes en la plantilla: nombre interno del paquete UNIR, definiciones de color incompatibles, destinos PDF duplicados, sustitución de alguna variante tipográfica y cajas `Underfull`. No afectan a la resolución de las nuevas citas ni alteran el contenido experimental.
