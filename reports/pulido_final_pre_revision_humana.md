# Pulido final previo a revisión humana

Fecha de comprobación: 23 de agosto de 2026.

## Cambios realizados

- Se resolvió el duplicado del índice sin eliminar contenido. La antigua sección 3.3.4 se denomina ahora «Visión general y secuencia experimental» y la sección 3.3.5 conserva «Diseño general del experimento».
- Se eliminó la carga de `mathabx` en `latex/estilo_unir-1.sty`. Este paquete sustituía glifos matemáticos estándar y era la causa de los signos anómalos. La notación queda cubierta por `amsmath`, `amssymb` y `amsfonts`.
- Se revisaron las expresiones con `=`, `\leq`, `\geq`, `\sim`, signo menos, `\cdot`, `\odot`, `\sqrt{252}`, `D_{KL}`, `\mu`, `\Sigma`, `w` y `r_t`. No se alteró su significado matemático.
- Se normalizaron porcentajes en resumen, abstract, metodología, desarrollo, resultados, conclusiones y limitaciones. El criterio visible es `64,93 %`, `-13,96 %` y `20 %`, usando un espacio no separable antes de `\%`.
- Se limpiaron la tabla comparativa de carteras y el texto circundante: comas duplicadas, porcentajes dentro de modo matemático, signos negativos y drawdowns.
- Se corrigió el escape de `equal_weight.py`, detectado durante la compilación.
- Se retiraron los campos `note` de la bibliografía para evitar comentarios o anotaciones internas.

## Referencias académicas añadidas

1. Wirth, R. y Hipp, J. (2000), *CRISP-DM: Towards a Standard Process Model for Data Mining*, Proceedings of the 4th International Conference on the Practical Applications of Knowledge Discovery and Data Mining, 1, 29–39. Citada en la justificación metodológica de CRISP-DM. Verificación: copia académica del trabajo y metadatos bibliográficos coincidentes.
2. Sharpe, W. F. (1966), *Mutual Fund Performance*, The Journal of Business, 39(1), 119–138, DOI `10.1086/294846`. Citada al definir el ratio de Sharpe en resultados. Verificación: registro del volumen de JSTOR/University of Chicago Press, página del autor en Stanford y DOI coincidentes.

## Referencias de 2025 y 2026

- `rasekhschaffe2026`: respaldada por `papers/Rasekhschaffe2026.pdf` y arXiv `2602.00196`; título, autor y fecha de envío (30-01-2026) coinciden. Es una prepublicación arXiv v1, no un artículo revisado por pares.
- `aghapour2025solving`: respaldada por `papers/Aghapour2025.pdf` y arXiv `2507.09916`. El registro vivo de arXiv figura en versión v4, revisada el 01-08-2026; se actualizó el título bibliográfico al título vigente. Sigue siendo una prepublicación, aunque su año de primera entrega es 2025.
- `voronina2025genai`: respaldada por `papers/Voronina2025.pdf` y arXiv `2512.24526`; título, autores y fecha de envío (31-12-2025) coinciden. Es una prepublicación arXiv v1.
- `machin2026repositorio`: el repositorio del propio TFM es una fuente primaria local del proyecto, pero no una referencia académica externa ni revisada por pares.

No se detectó ninguna referencia 2025/2026 sin respaldo identificable. El riesgo pendiente de las tres referencias académicas recientes es su condición de prepublicaciones y la posibilidad de nuevas versiones posteriores.

## Verificación de compilación

- Compilación completa realizada con `pdflatex`, `bibtex` y dos pasadas finales de `pdflatex`.
- Salida verificada: `latex/main_pulido.pdf`, 80 páginas.
- Log final sin errores LaTeX, citas indefinidas, referencias indefinidas, `Overfull \hbox`, `Overfull \vbox` ni placeholders.
- Extracción de texto comprobada: porcentajes y drawdowns aparecen limpios; el índice contiene una sola entrada con cada uno de los dos títulos diferenciados.
- Persisten avisos no bloqueantes heredados de la plantilla: definiciones de color incompatibles, destinos PDF duplicados y algunas cajas `Underfull`. No son errores, referencias indefinidas ni desbordamientos `Overfull`.

## Riesgos pendientes para revisión humana

- `latex/main.pdf` estaba abierto y bloqueado por otra aplicación durante la compilación; por ello la versión validada se guardó como `latex/main_pulido.pdf`. Al cerrar el visor puede recompilarse o sustituirse el nombre de salida.
- Conviene inspeccionar visualmente una última vez las páginas con fórmulas y la tabla principal en el visor final elegido, aunque la causa de los glifos anómalos fue retirada y el PDF compila con fuentes matemáticas AMS estándar.
- Las advertencias de destinos PDF duplicados proceden de la numeración/estructura de la plantilla y afectan a algunos enlaces internos, no al contenido visible. Corregirlas exigiría intervenir en la plantilla más allá del pulido formal solicitado.
