# Resumen de ampliación integral del TFM

## Objetivo de la intervención

Ampliar la memoria larga sin compactarla, resolver scaffolding y responder a estructura, teoría, figuras, CRISP-DM, EDA, modelos, resultados y APA.

## Estado inicial

PDF de 59 páginas; resumen/abstract vacíos; CRISP-DM y EDA con TODOs; contradicciones VAE-GAN/KL; capítulos 7 y 8 vacíos; 18 referencias, solo 10 usadas.

## Estado final

PDF de 80 páginas, ocho capítulos completos, 9 figuras, 5 tablas, comparación multmodelo ejecutada y 18 referencias citadas.

## Páginas iniciales y finales

59 iniciales y 80 finales: incremento de 21 páginas sin cambios artificiales de formato.

## Archivos modificados

`latex/main.tex`, bibliografía y capítulos 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11 y 12.

## Archivos creados

`src/models/compare_autoencoders.py`, CSV y snippet de comparación, y siete informes integrales en `reports/`.

## Contenido añadido por capítulo

- Introducción: alcance real, evaluación fuera de muestra y cautela.
- Contexto: figuras de Markowitz/VAE y referencias.
- Metodología: CRISP-DM completo y tabla.
- Normativa: seis secciones revisadas.
- Desarrollo: EDA real, tabla descriptiva, modelos AE/VAE y discusión extensa.
- Código/datos: flujo, dependencias, artefactos y limitaciones.
- Conclusiones: objetivos, resultados, aportaciones y cierre.
- Prospectiva: limitaciones detalladas y líneas futuras.

## Contenido conservado

Desarrollo matemático, estado del arte, metodología inicial como contexto histórico, benchmarks, arquitectura VAE, generación, optimización y resultados reales.

## Contenido eliminado y justificación

Solo placeholders, TODOs resueltos, notas bibliográficas internas y afirmaciones empíricas contradictorias. No se eliminó teoría útil.

## Coherencia VAE/GAN/KL

VAE es el núcleo ejecutado; GAN/WGAN son teoría, diseño inicial o futuro; KL regulariza el latente; máximo Sharpe optimiza la cartera.

## EDA incorporado

Cinco figuras comentadas, tabla de cinco activos, ausencias, distribución, extremos, curtosis, dinámica, volatilidad y correlaciones.

## Comparación de modelos

AE-8, VAE-8 y VAE-4 entrenados durante 120 épocas, semilla 42 y mismo split. El AE reconstruye mejor; VAE-8 logra menor error de medias sintéticas y conserva un prior explícito.

## Resultados experimentales

Cuatro estrategias, cinco métricas completas y análisis de riesgo, rentabilidad, causas plausibles, calidad generativa y validez.

## Bibliografía

18 entradas locales, todas citadas; notas internas retiradas. El mínimo de 20 queda parcial de forma explícita.

## Figuras y tablas

9 figuras y 5 tablas con fuente, label y referencia textual.

## Validaciones realizadas

Entrenamiento multmodelo, generación de CSV, compilación LaTeX completa, recuento de páginas, auditoría de citas e índices.

## Warnings pendientes

Warnings no fatales del estilo UNIR, sustitución tipográfica, destinos PDF duplicados y cajas underfull. No hay citas, referencias indefinidas ni cajas overfull.

## Riesgos pendientes para revisión humana

Título VAE-GAN, fuentes 2025/2026, URL del repositorio, inspección visual y robustez temporal.

## Próximos pasos recomendados

Validación walk-forward, varias semillas, cartera AE, costes/rebalanceo, dos referencias adicionales verificadas y revisión APA humana.
