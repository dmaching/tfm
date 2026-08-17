# Checklist feedback tutor

## Bloque 1. Estructura oficial

- [x] Mantener exactamente los ocho capítulos oficiales y sus epígrafes obligatorios.
  Archivo/sección: `latex/main.tex` y capítulos incluidos.
  Acción: estructura verificada; consultar `reports/auditoria_estructura_unir.md`.

## Bloque 2. Teoría y estado del arte

- [ ] Ampliar la fundamentación teórica y la revisión de literatura sin duplicar contenidos.
  Archivo/sección: capítulo 2, `03_marco_teorico.tex` y `04_estado_arte.tex`.
  Acción: seleccionar y analizar manualmente fuentes académicas relevantes.
- [ ] Reforzar la síntesis crítica y el hueco de investigación.
  Archivo/sección: 2.3 Conclusiones.
  Acción: revisar manualmente después de ampliar la literatura.

## Bloque 3. Figuras

- [ ] Incorporar figuras teóricas correctamente citadas y con fuente.
  Archivo/sección: 2.1 y 2.2.
  Acción: seleccionar figuras o elaborar diagramas basados en fuentes verificadas.
- [x] Ajustar el diagrama ancho señalado alrededor de la página 24.
  Archivo/sección: metodología, figura `fig:arquitectura_vae_gan`.
  Acción: se limitó mecánicamente a `0.85\textwidth` y se añadieron etiqueta y fuente.
- [ ] Revisar la referencia textual de todas las figuras y tablas.
  Archivo/sección: documento completo.
  Acción: incorporar referencias en el texto cuando se redacten las secciones pendientes.

## Bloque 4. Metodología CRISP-DM

- [ ] Justificar el uso de CRISP-DM.
  Archivo/sección: 3.3, `02_objetivos.tex`.
  Acción: completar manualmente la subsección preparada.
- [ ] Distribuir el contenido metodológico existente entre las fases CRISP-DM.
  Archivo/sección: 3.3 y `05_metodologia.tex`.
  Acción: revisar conceptualmente la correspondencia antes de mover texto.

## Bloque 5. EDA

- [ ] Ejecutar y documentar el análisis exploratorio completo con datos reales.
  Archivo/sección: nueva sección 5.1, `06_desarrollo.tex`.
  Acción: generar primero `data/processed/returns.csv` y ejecutar `src/analysis/generate_eda_outputs.py`.
- [ ] Insertar y comentar tablas y figuras EDA seleccionadas.
  Archivo/sección: 5.1 y `latex/snippets/eda_figures_snippets.tex`.
  Acción: copiar manualmente solo las figuras pertinentes tras validar sus resultados.

## Bloque 6. Modelos y entrenamiento

- [ ] Mostrar el entrenamiento de los algoritmos candidatos.
  Archivo/sección: Entrenamiento y comparación de modelos, capítulo 5.
  Acción: incorporar curvas y métricas procedentes de ejecuciones reales.
- [ ] Comparar al menos tres modelos o variantes con protocolo común.
  Archivo/sección: Modelos candidatos y Métricas de comparación.
  Acción: usar implementaciones existentes y justificar cualquier candidato adicional.
- [ ] Seleccionar el modelo final mediante métricas.
  Archivo/sección: Selección del modelo final.
  Acción: redactar la decisión únicamente después de obtener resultados comparables.

## Bloque 7. Resultados

- [ ] Profundizar el análisis y relacionarlo con objetivos y literatura.
  Archivo/sección: 5.12 Resultados experimentales (numeración sujeta a recompilación).
  Acción: revisar manualmente tras completar EDA y comparación.
- [ ] Revisar coherencia entre CSV generados, tabla y afirmaciones.
  Archivo/sección: `08_resultados.tex`.
  Acción: contrastar cada cifra con `data/generated/benchmark_comparison.csv` cuando exista.

## Bloque 8. Referencias APA

- [ ] Alcanzar al menos 20 referencias académicas relevantes.
  Archivo/sección: `latex/bibliografia.bib`.
  Acción: hay 18 entradas; añadir fuentes solo tras selección académica manual.
- [ ] Revisar metadatos, citas en texto y bibliografía en estilo APA.
  Archivo/sección: documento completo y `.bib`.
  Acción: resolver los hallazgos de `reports/auditoria_bibliografia_apa.md` sin inventar campos.
