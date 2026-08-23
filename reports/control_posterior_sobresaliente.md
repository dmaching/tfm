# Control posterior para versión de alta calidad

## Estado final
- PDF generado: `latex/main_sobresaliente.pdf`.
- Páginas: 82 (inicial: 80).
- Figuras: 16.
- Tablas: 7 (inicial: 5).
- Referencias: 22.
- Compilación: correcta con `pdflatex`, `bibtex` y dos pasadas finales.

## Cambios principales realizados
Se alinearon título, metadatos, resumen, abstract y alcance con el VAE implementado; se reforzaron introducción y hueco de investigación; se normalizaron fórmulas; se añadió una síntesis metodológica; se ejecutó una comparación multisemilla; y se reforzaron reproducibilidad, resultados, conclusiones y prospectiva sin alterar las métricas financieras.

## Cambio de título
- Estado: completado en portada, metadatos PDF y referencia propia.
- Apariciones antiguas revisadas: no queda el título «mediante Arquitecturas VAE-GAN» ni su justificación defensiva.

## Mejoras metodológicas
- Correspondencia explícita entre objetivos, evidencias y artefactos.
- Delimitación entre VAE ejecutado y GAN/WGAN teóricas.
- Conexión entre Markowitz, error de estimación, hechos estilizados y escenarios.
- Mayor claridad sobre fuga de información, test reservado y CRISP-DM.

## Mejoras experimentales
- Multisemilla ejecutado: sí; semillas 42, 123 y 2026 para AE-8, VAE-8 y VAE-4.
- Archivos generados: `autoencoder_model_comparison_multiseed.csv` y `autoencoder_model_comparison_multiseed_summary.csv`.
- Resultados resumidos: AE-8 conserva mejor reconstrucción, volatilidad y correlación; VAE-8 presenta el menor error medio de medias sintéticas. La ejecución base se conserva.

## Mejoras de fórmulas
Se normalizaron transposición, producto elemento a elemento, distribución normal, subíndices y espaciado. La notación compila con fuentes AMS estándar.

## Mejoras de estilo
Se suavizaron afirmaciones predictivas, se corrigió la presentación de VAE y se reforzó la interpretación prudente del resultado financiero.

## Bibliografía
Se conservan 22 referencias, sin claves o títulos duplicados. Merton, Engle, Wirth/Hipp y Sharpe están citados. Las dos entradas de López de Prado quedan señaladas para decisión humana.

## Warnings pendientes
Persisten avisos inocuos de plantilla: nombre interno del paquete, colores, destinos PDF duplicados, sustitución tipográfica y cajas `Underfull`. No hay errores, citas/referencias indefinidas ni `Overfull`.

## Riesgos pendientes para revisión humana
- Un solo corte financiero, sin `walk-forward`, costes, rebalanceo o rotación.
- Tres semillas no miden estabilidad temporal.
- Universo de 30 acciones y posible sesgo de supervivencia.
- Revisar visualmente tabla multisemilla y fórmulas.

## Recomendaciones antes de enviar al tutor
Leer de forma continua resumen, introducción, resultados, conclusiones y limitaciones; revisar saltos de página; confirmar URL y permisos del repositorio; y realizar una inspección visual final.
