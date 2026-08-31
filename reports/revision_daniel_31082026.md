# Revisión Daniel 31/08/2026

## Cambios aplicados
- Se suavizó el párrafo de la sección 4.6 sobre reproducibilidad y transparencia, manteniendo expresamente que la reproducibilidad no equivale a validez externa.
- Se reformuló en la sección 5.1.3 la explicación sobre los valores ausentes para aclarar que un tratamiento incorrecto puede inducir regularidades artificiales ajenas al comportamiento real de los retornos.
- Se añadió a la explicación de la Figura 2.1 una frase breve que aclara que la frontera eficiente reúne carteras para distintos niveles de volatilidad esperada.

## Cambios no aplicados
- No se añadió otra explicación de $w^\top \Sigma w$: el texto existente ya indica que $\Sigma$ es la matriz de varianzas-covarianzas y que el producto cuadrático devuelve la varianza de la cartera incorporando volatilidades y covarianzas. Añadir la frase propuesta habría duplicado esa explicación.
- No se modificaron métricas, resultados, fórmulas, estructura ni título, ni se reescribieron capítulos.

## Decisión cuantiles/cuartiles
- Se conserva «cuantiles». La aparición revisada enumera de forma general las variables derivadas del análisis exploratorio —entre ellas cuantiles y extremos— y no se refiere específicamente a Q1, mediana y Q3. Por tanto, «cuartiles» sería una restricción innecesaria del significado.

## Compilación
- La compilación inicial no pudo sobrescribir `main.pdf` porque estaba bloqueado.
- Se ejecutó la cadena completa con el nombre de trabajo alternativo: `pdflatex`, `bibtex` y dos pasadas finales de `pdflatex`.
- Resultado: `latex/main_revision_31082026.pdf`, 82 páginas, compilado correctamente.
- El log final no contiene citas indefinidas ni referencias indefinidas.

## Riesgos pendientes
- El log conserva avisos no bloqueantes previos o ajenos a esta revisión: definiciones de color incompatibles, sustitución de algunas formas tipográficas, cajas `underfull` y destinos PDF duplicados.
- `main.pdf` continúa sujeto al bloqueo externo observado durante la compilación; se generó el PDF alternativo solicitado sin intentar forzar su cierre o sobrescritura.
