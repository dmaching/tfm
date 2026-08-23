# Plan de redacción completa

## Archivos previstos

- `latex/main.tex`.
- `latex/capitulos/01_introduccion.tex`, `02_objetivos.tex`, `03_marco_teorico.tex`, `06_desarrollo.tex`, `07_codigo.tex`, `11_conclusiones.tex` y `12_limitaciones.tex`.
- Informes nuevos en `reports/`.

## Capítulos incompletos detectados

- Capítulo 3: fases CRISP-DM en scaffolding.
- Capítulo 5: EDA y comparación de modelos con TODOs.
- Capítulo 6: sección de datos vacía y código insuficiente.
- Capítulos 7 y 8: vacíos.
- Resumen y abstract: placeholders.

## TODOs existentes

Se detectaron TODOs sobre CRISP-DM, EDA, comparación de modelos, figuras teóricas, bibliografía y revisión APA.

## Estrategia

Redactar desde scripts, CSV y figuras reales; conservar resultados verificables; emplear GAN/WGAN solo como teoría o prospectiva; usar KL solo como regularización del VAE; y compilar hasta eliminar errores.

## Riesgos conceptuales

- El título conserva «VAE-GAN», pero no hay código adversario.
- Solo se entrenó una configuración VAE; no existe comparación multmodelo.
- Un único corte temporal limita la generalización.
- Rentabilidades elevadas pueden depender del periodo y de concentración.
- Solo existen 18 entradas BibTeX locales verificables.
