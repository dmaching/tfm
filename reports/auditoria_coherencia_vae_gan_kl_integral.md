# Auditoría integral de coherencia VAE, GAN y KL

| Archivo | Sección | Tipo de mención | Problema | Acción aplicada |
|---|---|---|---|---|
| `main.tex` | Resumen/Abstract | Alcance | El título puede inducir a pensar en una GAN ejecutada | Se declara que el núcleo validado es VAE y GAN/WGAN no se implementaron |
| `01_introduccion.tex` | Planteamiento | Planteamiento inicial/implementación | GAN y optimización KL figuraban como fases ejecutadas | Se sustituyen por muestreo/decoder VAE y máximo Sharpe; se añade aclaración temprana |
| `02_objetivos.tex` | Objetivos | Objetivo | Se proponía diseñar GAN/WGAN | Se convierte en revisión teórica y prospectiva |
| `03_marco_teorico.tex` | GAN/WGAN | Teoría | Mención válida pero potencialmente ambigua | Se conserva como fundamento y se delimita el VAE experimental |
| `04_estado_arte.tex` | Propuesta | Estado del arte/planteamiento | Atribuía la generación ejecutada a VAE-GAN | Se reformula como inspiración inicial y extensión futura |
| `05_metodologia.tex` | Diseño híbrido | Planteamiento inicial | Describía en presente una GAN entrenada | Se conserva como historia metodológica, con avisos explícitos de no implementación |
| `05_metodologia.tex` | Funciones de pérdida | Teoría | Podía confundirse KL del VAE con optimización financiera | Se separan pérdida variacional y máximo Sharpe |
| `06_desarrollo.tex` | VAE/escenarios | Implementación real | Necesitaba parámetros verificables | Se documentan 30--64--64--8, beta 0,001, 150 épocas, Adam y 5.000 escenarios |
| `08_resultados.tex` | Resultados | Resultado experimental | Riesgo de atribuir causalidad a IA | Se explica que cambia la fuente de parámetros y se evita afirmar superioridad general |
| `11_conclusiones.tex` | Conclusiones | Conclusión | Riesgo de extrapolación | Se limita la evidencia al periodo y protocolo analizados |
| `12_limitaciones.tex` | Prospectiva | Limitación/futuro | GAN/WGAN no ejecutadas | Se declaran expresamente como trabajo futuro |

La clasificación final es coherente: generador, discriminador y criterio adversario aparecen únicamente en teoría, diseño inicial o futuro; no se les atribuyen métricas. La divergencia KL aparece como comparación de distribuciones en teoría y como regularización del posterior VAE en la implementación, nunca como objetivo de pesos.
