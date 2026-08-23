# Control previo para elevación académica

Fecha del control: 23 de agosto de 2026.

## Estado inicial

- PDF: `latex/main_pulido.pdf`.
- Páginas: 80.
- Figuras: 16 entornos `figure` en las fuentes LaTeX.
- Tablas: 5 entornos `table` en las fuentes LaTeX.
- Referencias: 22 entradas BibTeX.
- Compilación: la versión `main_pulido.pdf` estaba validada mediante `pdflatex`, `bibtex` y dos pasadas finales de `pdflatex`; el PDF es A4 y no está cifrado. `main.pdf` figura modificado y ha estado bloqueado por el visor en compilaciones recientes.
- Estado Git previo: existe un cambio sin commit en `latex/main.pdf`; debe preservarse. No se realizará `reset`, descarte ni sobrescritura destructiva.

## Estructura detectada

La memoria conserva la plantilla UNIR y se organiza en resumen, abstract y ocho capítulos: introducción; contexto y estado del arte; objetivos y metodología CRISP-DM; marco normativo; desarrollo experimental y resultados; código y datos; conclusiones; limitaciones y prospectiva. El desarrollo contiene EDA, pipeline, benchmarks, VAE, generación de escenarios, optimización, comparación AE-8/VAE-8/VAE-4 y evaluación financiera.

## Fortalezas actuales

- Extensión suficiente y estructura oficial consolidada.
- Separación temporal entrenamiento/test y escalado ajustado solo con entrenamiento.
- EDA real con cobertura, distribuciones, volatilidad y correlaciones.
- Comparación ejecutada de tres autoencoders y resultados almacenados en CSV.
- Evaluación financiera común frente a equiponderación y dos variantes de Markowitz.
- Discusión prudente del retorno elevado del VAE y capítulo específico de limitaciones.
- CRISP-DM vinculado con artefactos reproducibles.
- 22 referencias, incluidas Markowitz, Merton, Engle, Wirth/Hipp y Sharpe.
- GAN/WGAN ya se distinguen en varios lugares como marco conceptual o trabajo futuro.

## Debilidades actuales

- El título todavía promete «Arquitecturas VAE-GAN», aunque el experimento validado implementa un VAE.
- Resumen y abstract conservan una justificación defensiva del título antiguo.
- La metodología mantiene un epígrafe denominado «Arquitectura VAE-GAN considerada en el diseño inicial», que requiere una delimitación más limpia.
- Algunas fórmulas y convenciones vectoriales necesitan homogeneización final.
- La comparación AE/VAE usa una sola semilla; existe infraestructura suficiente para una validación multisemilla ligera.
- La correspondencia entre objetivos, evidencias y artefactos está distribuida y puede sintetizarse mejor.
- Los metadatos PDF aparecen vacíos para título, autor, asunto y palabras clave.

## Riesgos académicos principales

- Desalineación entre título y contribución implementada.
- Riesgo de interpretar el 242,32 % como evidencia generalizable o predictiva.
- Un único corte temporal y ausencia de `walk-forward`, costes, rebalanceo y rotación.
- Comparación de redes basada hasta ahora en una sola semilla.
- Posible sesgo de supervivencia y universo limitado a 30 activos.
- Las referencias 2025/2026 son prepublicaciones y pueden recibir nuevas versiones.

## Riesgos técnicos principales

- `main.pdf` puede permanecer bloqueado; será necesario compilar con un nombre alternativo.
- La plantilla produce avisos heredados de colores, destinos PDF duplicados y cajas `Underfull`.
- El script multisemilla requiere parametrizar la semilla actual, conservar la ejecución base y medir tiempo antes de integrar resultados.
- Cualquier tabla multisemilla debe proceder exclusivamente de una ejecución real y reproducible.

## Mejoras planificadas

- Crear respaldo Git y registrar el estado previo.
- Alinear título, metadatos, resumen, abstract y menciones internas con la implementación VAE.
- Auditar todas las apariciones VAE-GAN/GAN/WGAN y mantener solo las justificadas.
- Realizar mejoras quirúrgicas en introducción, marco teórico, fórmulas, CRISP-DM, resultados, reproducibilidad, conclusiones y prospectiva.
- Ejecutar, si el coste es razonable, AE-8/VAE-8/VAE-4 con semillas 42, 123 y 2026; conservar resultados base.
- Añadir una síntesis de garantías metodológicas sin duplicar tablas existentes.
- Auditar bibliografía, citas, figuras, tablas y estilo técnico.
- Compilar y producir controles e informes posteriores para revisión humana.

## Elementos que no deben modificarse

- Estructura oficial UNIR.
- Resultados, métricas o tablas experimentales sin recálculo desde scripts.
- Contenido útil del autor y extensión global de la memoria.
- Estado del arte de GAN/WGAN como teoría y prospectiva.
- Carácter académico y no prescriptivo del trabajo.
- Separación entrenamiento/test y trazabilidad de artefactos.
- Cambios locales existentes ajenos a esta intervención.
