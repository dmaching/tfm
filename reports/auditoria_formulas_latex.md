# Auditoría de fórmulas

## Fórmulas revisadas

Se revisaron las expresiones de media-varianza, restricción presupuestaria, entropía, divergencia KL, información mutua, reparametrización, ELBO, objetivo GAN, log-retornos, retorno y varianza de cartera, restricciones `long-only`, distribución latente, momentos sintéticos y máximo Sharpe.

## Fórmulas corregidas

- Se mantuvo `D_{KL}` con subíndice y `\parallel` entre distribuciones.
- Se normalizó la transposición de la varianza de cartera a `\mathbf{w}^{\top}\boldsymbol{\Sigma}\mathbf{w}`.
- Se normalizó el producto elemento a elemento de la reparametrización a `\odot`.
- Se agrupó la reparametrización con `\qquad` y `\mathcal{N}(0,I)` para evitar espaciados irregulares.
- Se verificaron `r_t`, `P_t`, `P_{t-1}`, sumatorios, fracciones y restricciones con `\leq`/`\geq`.
- La retirada previa de `mathabx` mantiene los glifos matemáticos AMS estándar.

## Archivos modificados

- `latex/capitulos/03_marco_teorico.tex`.
- `latex/capitulos/06_desarrollo.tex`.

## Riesgos pendientes

La extracción de texto de un PDF no siempre conserva visualmente raíces, superíndices o símbolos. Se requiere comprobación visual del PDF final, además del control del log.
