# Micropulido final para envío al tutor

Fecha de revisión: 25 de agosto de 2026.

## Cambios aplicados

- Se revisó el capítulo 3 y se sustituyeron por presente o pasado las formulaciones de anteproyecto que describían tareas ya ejecutadas: adquisición, preprocesamiento, división temporal, evaluación, benchmarks y métricas.
- Se conservaron los futuros y condicionales que se refieren realmente a extensiones no implementadas, en particular la posible incorporación posterior de GAN/WGAN.
- En el apartado 3.3.9 se sustituyó la formulación que podía presentar la divergencia KL como criterio de optimización de cartera por: «Análisis complementario de la calidad distribucional mediante medidas informacionales, como la divergencia de Kullback-Leibler, sin utilizarla como función objetivo directa de la cartera.»
- Se reforzó en la lista de métricas que la divergencia KL es una medida complementaria de calidad distribucional y no una función objetivo financiera. La introducción de metodología ya indica que la KL forma parte de la pérdida del VAE.
- Se corrigió la errata `medirsá`; tras adaptar el tiempo verbal, la redacción final es `midió`.
- Se eliminó la segunda aparición de «Fuente: elaboración propia» de la Figura 3.1. La atribución se conserva una sola vez dentro del pie de figura.
- Se aplicó una suavización mínima a dos frases generales del marco normativo y a formulaciones de adquisición y preprocesamiento propias de un anteproyecto. No se alteró el contenido técnico.
- Se eliminaron la cita y la entrada `lopezdeprado2018chapter1`, redundantes con el libro completo de López de Prado.

## Cambios no aplicados y motivo

- No se modificaron títulos oficiales, estructura, resultados, métricas ni valores numéricos.
- No se reescribieron completos el marco normativo, la adquisición de datos ni la construcción de retornos. La revisión Winston se limitó a frases puntuales para conservar la voz y la precisión del texto.
- No se cambiaron los nombres `download_data.py`, `returns_train.csv`, `returns_test.csv`, `returns_train_scaled.csv`, `returns_test_scaled.csv`, `minmax_scaler.pkl`, `benchmark_comparison.csv` y `compare_autoencoders.py`: ya aparecían mediante `\texttt{...}` y con los guiones bajos escapados en LaTeX.
- No se sustituyeron formulaciones futuras que describen trabajo futuro real, especialmente ampliaciones GAN/WGAN.

## Referencias de López de Prado

Se conservó `lopez2018advances`, correspondiente al libro completo *Advances in Financial Machine Learning*. Se eliminó `lopezdeprado2018chapter1`, que remitía mediante SSRN al capítulo 1 de la misma obra y se citaba en el mismo grupo, sin aportar un uso diferenciado. La bibliografía resultante mantiene 21 entradas.

## PDF generado

- Archivo: `latex/main.pdf`
- Tamaño tras la compilación final: 1.722.829 bytes.
- Extensión: 82 páginas.
- No fue necesario generar `main_final_tutor.pdf`, porque `main.pdf` no estaba bloqueado.

## Estado de compilación

Se ejecutó desde `latex/` la secuencia solicitada:

```text
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Resultado: compilación correcta, con código de salida 0. BibTeX informó de cero avisos. La comprobación del log final no encontró citas indefinidas, referencias indefinidas ni solicitudes de una nueva pasada. Tampoco se localizaron placeholders en `main.tex` o en los capítulos incluidos.

## Riesgos pendientes para revisión humana

- La plantilla sigue produciendo avisos no bloqueantes sobre definiciones de color incompatibles, sustitución de una variante de fuente y cajas `underfull`.
- `pdfTeX` informa de destinos PDF duplicados para algunas páginas, figuras y tablas. No impide generar ni leer el PDF, pero conviene comprobar manualmente los enlaces internos si se consideran importantes para la entrega.
- Conviene hacer una última inspección visual de portada, índices, saltos de página y pies de figuras en el visor que utilizará el tutor.
- La valoración de naturalidad frente a Winston es probabilística; las correcciones se mantuvieron deliberadamente mínimas para no homogeneizar la voz del autor ni perder precisión.

No se modificaron métricas, estructura ni conclusiones durante este micropulido.
