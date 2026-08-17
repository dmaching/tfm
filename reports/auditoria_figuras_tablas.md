# Auditoría de figuras y tablas

## Elementos insertados en la memoria

| Tipo | Ubicación | Caption | Label | Fuente | Referencia textual | Tamaño/maquetación |
|---|---|---:|---:|---:|---:|---|
| Figura TikZ: arquitectura VAE-GAN | `latex/capitulos/05_metodologia.tex` | OK | OK (`fig:arquitectura_vae_gan`) | OK | FALTA | Ajustada a `0.85\textwidth`; era el elemento ancho situado aproximadamente en la página 24. |
| Tabla: comparación de estrategias | `latex/capitulos/08_resultados.tex` | OK | OK (`tab:resultados`) | OK | OK | La tabla excede el ancho disponible; se recomienda reformatear columnas o aplicar `\resizebox{\textwidth}{!}{...}` tras revisar legibilidad. |

No se detectaron otros entornos `figure` o `table` insertados en los capítulos. La ecuación etiquetada `eq:retorno_logaritmico` no forma parte de esta auditoría.

## Imágenes existentes pero no insertadas

En `figures/` existen nueve PNG generados por el pipeline: curva de pérdida VAE, evaluaciones de reconstrucción, distribuciones y correlaciones sintéticas, comparación de volatilidad y rendimiento acumulado de estrategias. No aparecen mediante `\includegraphics` en la memoria actual. Antes de insertarlos deben verificarse sus datos, añadir caption, label, fuente y referencia textual.

## Hallazgos pendientes

- FALTA referencia en el texto a `fig:arquitectura_vae_gan`.
- La tabla `tab:resultados` produce un `overfull hbox` importante por sus seis columnas.
- Los snippets EDA usan `width=0.85\textwidth`, pero no se insertan automáticamente.
- La compilación mantiene avisos de destinos PDF duplicados para la figura y la tabla; no alteran su numeración visible, pero conviene revisar la interacción entre `hyperref` y la plantilla UNIR.
