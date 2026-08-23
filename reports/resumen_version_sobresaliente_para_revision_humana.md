# Resumen de versión mejorada para revisión humana

## Qué se ha mejorado
Título y metadatos coherentes con VAE; resumen y abstract sin defensa del título antiguo; introducción prudente; hueco de investigación nítido; fórmulas normalizadas; garantías metodológicas; validación multisemilla real; discusión, conclusiones y prospectiva reforzadas.

## Qué no se ha tocado
No se cambiaron estructura UNIR, resultados financieros, tabla de estrategias, métricas, periodo, universo, split, VAE principal ni estado del arte GAN/WGAN. No se redujo la memoria.

## Qué debe revisar Daniel manualmente
- Voz personal, especialmente en metodología heredada en futuro verbal.
- Portada, índice, saltos y tabla multisemilla.
- Fórmulas en el visor final.
- URL, visibilidad y limpieza del repositorio.
- Referencia SSRN de López de Prado.

## Riesgos académicos restantes
Un único test; falta de `walk-forward`; costes y operación omitidos; universo reducido; posible sesgo de supervivencia; hiperparámetros limitados; prepublicaciones recientes.

## Riesgos técnicos restantes
Destinos PDF duplicados de plantilla; descarga futura de yfinance no idéntica; posible variación bit a bit entre plataformas.

## Preguntas probables del tutor
1. **¿Por qué se cambió el título?** El anterior prometía VAE-GAN sin implementación; el nuevo describe el núcleo validado.
2. **¿Por qué VAE y no GAN?** El VAE ofrece entrenamiento estable y prior explícito; GAN exige otro protocolo no validado.
3. **¿Qué aporta frente a Markowitz?** Una fuente alternativa de escenarios para estimar parámetros antes del optimizador clásico.
4. **¿Por qué el resultado es tan alto?** Periodo, pesos en activos revalorizados y sensibilidad del óptimo; no es predicción futura.
5. **¿Qué impide generalizar?** Un corte, 30 activos, sin costes, rebalanceo, rotación ni `walk-forward`.
6. **¿Segunda fase?** `Walk-forward`, costes, más activos, selección previa, HRP, Black--Litterman, CVaR y después WGAN/difusión.
7. **¿AE reconstruye mejor pero se mantiene VAE?** Reconstrucción y generación difieren; VAE aporta prior y trazabilidad del experimento principal.
8. **¿Cómo se evita fuga?** Corte cronológico; escalador y modelos solo con entrenamiento; test reservado.
9. **¿Qué aporta CRISP-DM?** Ordena pregunta, datos, modelado, evaluación y artefactos.
10. **¿Es recomendación financiera?** No; es un experimento académico retrospectivo.

## Archivos principales generados
- `latex/main_sobresaliente.pdf`.
- Dos CSV multisemilla en `data/generated/`.
- Informes de control, título, GAN/WGAN, fórmulas, bibliografía y checklist.

## Comandos de compilación usados
`pdflatex -jobname=main_sobresaliente -interaction=nonstopmode -halt-on-error main.tex`, `bibtex main_sobresaliente` y dos pasadas finales.

## Estado final recomendado
Versión sólida y lista para revisión humana detallada; no enviar sin lectura completa e inspección visual final.
