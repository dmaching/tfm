# Auditoría de coherencia VAE, GAN y KL

| Frase original | Archivo | Problema | Frase corregida |
|---|---|---|---|
| «Desarrollo de una GAN» | `01_introduccion.tex` | No existe código adversario | «Generación mediante muestreo y decodificación del espacio latente del VAE» |
| «Optimización mediante divergencia KL» | `01_introduccion.tex` | El optimizador maximiza Sharpe | «KL actúa únicamente como regularizador latente» |
| «arquitectura híbrida VAE-GAN» | `02_objetivos.tex` | Objetivo no ejecutado | Objetivo delimitado a VAE; GAN/WGAN como antecedentes |
| «Diseñar una GAN o WGAN» | `02_objetivos.tex` | No ejecutado | Revisar estas familias y distinguir teoría de experimento |
| «arquitectura principal VAE-GAN» | `03_marco_teorico.tex` | Exceso sobre evidencia | «implementación experimental exclusivamente VAE» |
| Descripción de generador/discriminador | capítulos teóricos | Válida solo como teoría | Se conserva en el marco conceptual, sin atribuir resultados |
| KL como parte de ELBO | marco teórico/desarrollo | Coherente con código | Se explicita `MSE + beta*KL`, beta 0,001 |
| GAN/WGAN en metodología antigua | `05_metodologia.tex` | Archivo ya no incluido | Se sustituyó su inclusión por metodología CRISP-DM verificada |
