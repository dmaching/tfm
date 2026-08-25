# Correcciones de revisión manual de Daniel — bloque 01

Fecha: 25 de agosto de 2026
Alcance: correcciones quirúrgicas sobre `latex/`, sin reescritura global, sin cambios de métricas, estructura ni título.

## Cambios aplicados

### Resumen

- Reformulada la frase de planteamiento: «estudia si escenarios sintéticos pueden proporcionar una base alternativa» → «estudia si **el uso de** escenarios sintéticos **puede** proporcionar una base alternativa».
- Explicada la cautela sobre los resultados para evitar la lectura contradictoria «son más rentables pero no son superiores». La frase antigua («Estos resultados son favorables en rentabilidad y Sharpe, pero también implican mayor volatilidad y no acreditan superioridad general.») se sustituyó por dos frases:
  - «Estos resultados son favorables en rentabilidad y Sharpe, aunque también implican mayor volatilidad.»
  - «La estrategia VAE fue, por tanto, superior en este experimento concreto, pero eso no basta para afirmar superioridad general: las cifras proceden de un único universo de activos, un único corte temporal y una evaluación sin costes de transacción, rebalanceo ni validación *walk-forward*.»
- Eliminada la palabra «validada» en «la implementación validada se centra en VAE» → «la implementación se centra en el VAE».
- Ajustada la frase final para no repetir la lista de exclusiones ya incorporada arriba: «El estudio es académico, sin costes, rebalanceo ni validación *walk-forward*.» → «El estudio tiene carácter académico y no constituye una recomendación de inversión.»
- No se modificó ninguna cifra (242,32 %, 25,08 %, 2,99, -13,96 %, 2.766, 5.000, 554, 30 activos, 8 dimensiones latentes).

### Abstract

- Traslado equivalente de todos los cambios del resumen:
  - «whether synthetic scenarios can provide» → «whether **the use of** synthetic scenarios can provide».
  - Nueva formulación de la cautela: «The VAE strategy was therefore superior in this particular experiment, but that is not enough to claim general superiority: the figures are obtained from a single asset universe, a single temporal split, and an evaluation without transaction costs, rebalancing, or walk-forward validation.»
  - «the validated implementation focuses on the VAE» → «the implementation focuses on the VAE».
  - «The study is academic and excludes transaction costs, rebalancing, and walk-forward validation.» → «The study is academic and does not constitute investment advice.»
- Extensión verificada: **263 palabras** (dentro del rango 150–300). El resumen en español queda en 290 palabras.

### Introducción

- Corregida la frase indicada en el capítulo 1: «esto es, un subconjunto de los activos financieros disponibles, de forma eficiente» → «esto es, **elegir** un subconjunto de los activos financieros disponibles **de manera eficiente**». Se comprobó que la frase anterior (sistema de segundo orden) y la posterior (cita de Markowitz 1952) siguen conectando.
- No se reescribió el resto de la introducción.

### Planteamiento del trabajo

- Reordenada la sección 1.2 según el criterio indicado: idea general → cuatro fases → delimitación de alcance.
- «propone una metodología híbrida que integra el modelado generativo y la teoría de la información» → «propone una **aproximación experimental** que integra modelado generativo, teoría de la información y **optimización clásica de carteras**». Se evita así la lectura de que existe una arquitectura híbrida implementada.
- Conservada literalmente la frase «El núcleo de la investigación se divide en cuatro fases:», ahora seguida inmediatamente por el `enumerate` de las cuatro fases (sin cambios en su contenido).
- Eliminada la frase redundante «Conviene delimitar desde el inicio el alcance alcanzado.»
- Eliminada la palabra «validado» de «El desarrollo experimental validado se centra en el Autoencoder Variacional» → «El desarrollo experimental se centra en el Autoencoder Variacional».
- El párrafo de alcance se movió detrás de las cuatro fases conservando íntegramente sus aclaraciones esenciales: VAE-GAN como diseño inicial descartado, GAN/WGAN no entrenadas, KL como regularización del espacio latente del VAE, no predicción de precios puntuales, generación de vectores plausibles de retornos y evaluación de pesos sobre observaciones posteriores no usadas en entrenamiento.
- El párrafo final sobre carácter académico permanece al cierre de la sección, donde ya estaba.

### Figura 5.1 / valores perdidos

- Eliminado el entorno `figure` de `figuras/eda/missing_values_by_asset.png` en la subsección «Valores perdidos y calidad de los datos» de `latex/capitulos/06_desarrollo.tex`, junto con su `\caption` y su `\label{fig:eda_missing_values}`.
- Eliminada la referencia cruzada «La Figura~\ref{fig:eda_missing_values} muestra este resultado para cada columna.» No existían otras menciones a esa figura en el cuerpo de la memoria.
- Sustituida por un párrafo explicativo, ajustado a los datos reales de la sección (umbral del 5 %, 30 activos conservados, 0 ausencias en 2.766 observaciones): describe la revisión activo por activo, el tratamiento previo de observaciones no válidas procedentes de descarga, ajustes corporativos y cálculo de log-retornos, y el motivo por el que esto importa en modelos generativos (evitar patrones espurios por ausencias artificiales).
- Se conservaron intactos los datos cuantitativos previos y el párrafo posterior sobre sesgo de selección y `eda_dataset_shape.csv`.
- El archivo de imagen `figuras/eda/missing_values_by_asset.png` **no** se ha borrado del repositorio; simplemente ya no se incluye en la memoria.
- Renumeración verificada en el índice de figuras regenerado: la antigua Figura 5.2 (distribución agregada de log-retornos) es ahora la Figura 5.1, y el resto desplaza en uno. Todas las referencias `\ref` siguen resolviendo.
- Figuras conservadas por el feedback del tutor: Figura 2.1 (frontera eficiente de Markowitz), Figura 2.2 (esquema conceptual del VAE) y Figura 3.1 (arquitectura híbrida VAE-GAN considerada inicialmente y no implementada). El documento mantiene 8 figuras (2.1, 2.2, 3.1 y 5.1–5.5) y 7 tablas (3.1, 3.2, 5.1–5.4 y 6.1).

## Cambios no aplicados

- No se tocó el título del trabajo ni los metadatos PDF.
- No se modificó ninguna métrica, tabla experimental, cifra de resultados ni conclusión numérica.
- No se modificó la estructura de capítulos ni el orden de la memoria.
- No se reintrodujo en ningún punto la idea de que GAN/WGAN estén implementadas o entrenadas.
- No se borró `figuras/eda/missing_values_by_asset.png` ni el snippet correspondiente en `latex/snippets/eda_figures_snippets.tex` (ese archivo no se incluye en la compilación, por lo que no genera etiquetas duplicadas ni figuras huérfanas).
- No se reescribió el marco teórico, el estado del arte ni el capítulo 5.
- No se sobrescribió `main_sobresaliente.pdf`; el PDF regenerado es `main.pdf`.

## Archivos modificados

- `latex/main.tex` (resumen y abstract)
- `latex/capitulos/01_introduccion.tex` (frase de introducción y reordenación de la sección 1.2)
- `latex/capitulos/02_objetivos.tex` («experimento validado» → «experimento implementado»)
- `latex/capitulos/05_metodologia.tex` («ejecución finalmente validada» → «realizada»; «pipeline validado» → «pipeline implementado»)
- `latex/capitulos/06_desarrollo.tex` (eliminación de la figura de valores perdidos, párrafo sustitutorio y tres erratas menores)
- `latex/capitulos/07_codigo.tex` (errata «multmodelo»)
- `latex/capitulos/08_resultados.tex` (refuerzo de la interpretación de superioridad y errata «multmodelo»)
- `latex/capitulos/11_conclusiones.tex` (errata «multmodelo»)
- `reports/correcciones_revision_daniel_01.md` (este informe)

## Compilación

- Comando (desde `latex/`):

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

  Un primer intento falló con `! I can't write on file 'main.pdf'` porque el visor de PDF estaba abierto; se compiló provisionalmente con `-jobname=main_revision_daniel` y, una vez cerrado el visor, se regeneró `main.pdf` con el ciclo completo. Los artefactos temporales `main_revision_daniel.*` se han eliminado.

- Resultado: compilación correcta, sin errores. Sin citas indefinidas, sin referencias indefinidas, sin etiquetas duplicadas y sin placeholders. Los únicos avisos son preexistentes y ajenos a estos cambios: nombre del paquete `estilo_unir-1` vs `unir`, definiciones de color de `xcolor`, sustitución de la forma de fuente `OT1/cmr/bx/sc` y los avisos `destination with the same identifier` de `hyperref` (uno menos que antes, precisamente por la figura eliminada).
- PDF generado: `latex/main.pdf` (82 páginas).

## Riesgos pendientes

- `main_sobresaliente.pdf` sigue reflejando la versión anterior. `main.pdf` ya está actualizado; si se quiere mantener sincronizado el PDF de referencia, hay que copiarlo o regenerarlo.
- Los avisos `destination with the same identifier` de `hyperref` son preexistentes (numeración de página del título frente a `\frontmatter`/`\mainmatter`). No afectan al PDF, pero conviene resolverlos si se quiere un log limpio.
- `latex/snippets/eda_figures_snippets.tex` sigue conteniendo el snippet de la figura de valores perdidos con la etiqueta `fig:eda_missing_values`. Si alguna vez se incluyera ese archivo, reaparecería la figura eliminada.
- Los números de figura citados en textos externos al proyecto (correos, informes previos como `reports/auditoria_figuras_tablas*.md`) quedan desactualizados tras la renumeración.
- El resumen en español queda en 290 palabras; si el criterio de 150–300 se aplicara también al resumen, está en el límite superior.

## Recomendaciones para revisión humana

- Leer del tirón la sección 1.2 ya reordenada para confirmar que el salto de «cuatro fases» al párrafo de alcance suena natural con la voz del autor.
- Confirmar que la nueva formulación del resumen y del abstract («fue superior en este experimento concreto, pero eso no basta para afirmar superioridad general») transmite la cautela deseada sin sonar defensiva.
- Verificar en el PDF que la subsección 5.1.3 no queda visualmente pobre tras eliminar la figura y que el párrafo sustitutorio no repite lo que dice el párrafo siguiente sobre sesgo de selección.
- Decidir si se conserva el archivo de imagen `missing_values_by_asset.png` en el repositorio o se retira del control de versiones.
- Decidir si `main_sobresaliente.pdf` debe actualizarse con el contenido de `main.pdf` antes de la entrega.

## Revisión global mínima de erratas evidentes

### Criterio aplicado

Se revisaron únicamente erratas, fallos de escritura, repeticiones o incoherencias formales muy evidentes, preservando el estilo del autor y evitando reescrituras generales. Ante la duda entre cambiar o conservar, se conservó.

### Cambios globales aplicados

- «multmodelo» → «multimodelo» (5 apariciones: `06_desarrollo.tex`, `08_resultados.tex` ×1, `11_conclusiones.tex`, `07_codigo.tex` ×2). Errata clara de escritura.
- «normalización Min-Max en el intervalo ([-1,1])» → «en el intervalo \([-1,1]\)» en `06_desarrollo.tex`. Paréntesis sobrantes procedentes de una conversión de modo matemático; el resto del documento ya usa `\(...\)`.
- «un límite máximo del (20~\%) por activo» → «un límite máximo del 20~\% por activo» en `06_desarrollo.tex`. Paréntesis claramente incorrectos.
- «no al experimento validado» → «no al experimento implementado» en `02_objetivos.tex`.
- «la ejecución finalmente validada» → «la ejecución finalmente realizada» y «El pipeline validado termina en el *decoder*» → «El pipeline implementado termina en el *decoder*» en `05_metodologia.tex`.
- Refuerzo de la interpretación en `08_resultados.tex`, sección «Evaluación comparativa y validez»: «La evidencia no permite afirmar que el VAE supere en general a Markowitz o equiponderación, ni que prediga el mercado.» → «La estrategia VAE fue superior en este experimento concreto, pero un único universo de activos y un único corte temporal no bastan para afirmar superioridad general frente a Markowitz o equiponderación, ni para sostener que el modelo prediga el mercado.» Mismo significado, razonamiento explícito y sin contradicción aparente.
- Verificación automática de palabras duplicadas consecutivas, dobles espacios y espacio antes de signo de puntuación en todos los `.tex` de `capitulos/` y en `main.tex`: sin incidencias (los únicos dobles espacios detectados son alineaciones internas de tablas).

### Cambios deliberadamente no aplicados

- «En el contexto actual de Big Data...» al inicio del segundo párrafo de la sección Motivación: es genérica, pero encaja con el hilo argumental del autor (Big Data aparece también en el capítulo 1 y en el título de la titulación) y no está mal escrita. Se conserva.
- Alternancia «VAE» / «VAEs» / «Autoencoder Variacional» / «Autoencoders Variacionales»: el uso actual es coherente (singular para el modelo implementado, plural para la familia de modelos, forma extendida en primera mención de cada capítulo). No se homogeneizó por la fuerza.
- Uso de «drawdown» con y sin `\textit{}`: hay algún caso sin cursiva en capítulos de limitaciones y conclusiones. No es una errata clara y tocarlo excedía el criterio conservador.
- Frases directas y algo coloquiales del autor (por ejemplo «El caos se caracteriza por la complejidad.») se mantienen tal cual.
- No se tocaron nombres de scripts, archivos CSV, citas, entradas bibliográficas, captions, títulos de capítulos ni contenido de tablas.

### Términos revisados

- **VAE / VAEs**: coherente. El modelo implementado se nombra siempre como VAE / Autoencoder Variacional, en singular y como componente ejecutada. Los plurales aparecen solo al hablar de la familia de modelos en introducción, marco teórico y estado del arte.
- **GAN / GANs / WGAN**: coherente tras los cambios. Aparecen exclusivamente como marco teórico (`03_marco_teorico.tex`, `04_estado_arte.tex`), como diseño inicial descartado (`01_introduccion.tex`, `05_metodologia.tex`) o como trabajo futuro (`12_limitaciones.tex`). En `06_desarrollo.tex` se afirma explícitamente que no se incluye una GAN en la comparación de modelos. Ninguna afirmación de entrenamiento.
- **VAE-GAN**: se describe siempre como arquitectura considerada en el diseño inicial y descartada. La Figura 3.1 mantiene el caption «Arquitectura híbrida VAE-GAN considerada inicialmente y no implementada de forma completa», y el texto que la acompaña en `05_metodologia.tex` aclara que es un diagrama conceptual, no del software ejecutado.
- **predicción / predecir**: coherente. Todos los usos son o bien descripciones de otros enfoques de la literatura (estado del arte), o bien negaciones explícitas de que este trabajo prediga precios puntuales, o bien usos legítimos («lo que predeciría una distribución normal»). No hay ninguna afirmación de predicción de precios propia.
- **superioridad**: revisado en resumen, abstract, resultados y conclusiones. En los cuatro sitios se afirma ahora superioridad únicamente relativa al experimento concreto y se niega la superioridad general, con los motivos explícitos.
- **metodología híbrida**: eliminada como descripción del trabajo propio en la sección 1.2. La palabra «híbrida» solo se conserva referida a la arquitectura VAE-GAN considerada y descartada, que es su uso correcto.
- **escenarios sintéticos**: uso uniforme en todo el documento; se habla siempre de generación de escenarios o de vectores plausibles de retornos, no de predicciones.
- **validado**: eliminado en los cuatro puntos donde calificaba al desarrollo, el experimento, la implementación o el pipeline. Se mantiene en usos legítimos como «necesidad de validación adicional», «validación *walk-forward*» y «validación temporal», que describen algo que no se hizo o que se propone como trabajo futuro.

### Riesgos pendientes para revisión humana

- La lectura fluida se comprobó sobre el fuente `.tex` y el índice de figuras generado, no párrafo a párrafo sobre el PDF maquetado. Conviene una lectura humana del PDF en resumen, abstract, capítulo 1 y subsección 5.1.3.
- La eliminación de «validado» en `02_objetivos.tex` y `05_metodologia.tex` va algo más allá del párrafo concreto señalado por Daniel; se hizo por coherencia terminológica y es fácilmente reversible.
- Quedan varios `\textit{drawdown}` inconsistentes y avisos de `hyperref` preexistentes que no se abordaron por criterio conservador.
