# TODO TFM

## Estado actual

El trabajo ya cuenta con una estructura general alineada con la memoria final:

- Introducción.
- Objetivos.
- Marco teórico.
- Estado del arte.
- Metodología.
- Desarrollo específico de la contribución.
- Código fuente y datos analizados.
- Resultados y evaluación.
- Herramientas y tecnologías.
- Marco normativo, ética y protección de datos.
- Conclusiones.
- Limitaciones y prospectiva.

El siguiente gran objetivo es desarrollar la contribución técnica del trabajo: construir un pipeline reproducible que permita descargar datos financieros, calcular retornos, generar escenarios sintéticos y comparar carteras.

---

## Prioridad inmediata: Capítulo 6

### 6. Desarrollo específico de la contribución

Objetivo: documentar qué se ha construido realmente y cómo funciona el pipeline experimental.

Secciones previstas:

- Diseño del pipeline experimental.
- Selección del universo de activos.
- Descarga de datos financieros con `yfinance`.
- Construcción del conjunto de retornos.
- Implementación de benchmarks: cartera equiponderada y Markowitz.
- Implementación inicial del VAE.
- Implementación inicial de GAN/WGAN.
- Generación de escenarios sintéticos.
- Optimización de carteras a partir de escenarios generados.

---

## Implementación técnica pendiente

### 1. Preparar entorno Python

- Crear entorno virtual.
- Instalar dependencias.
- Crear `requirements.txt`.
- Comprobar que el proyecto ejecuta correctamente desde el repositorio.

Dependencias iniciales:

- `numpy`
- `pandas`
- `matplotlib`
- `scipy`
- `scikit-learn`
- `yfinance`
- `torch` o `tensorflow`
- `cvxpy` o `scipy.optimize`

---

### 2. Descargar datos

- Seleccionar subconjunto inicial de activos del S&P 500.
- Descargar precios ajustados con `yfinance`.
- Guardar datos brutos en `data/raw/`.
- Guardar datos procesados en `data/processed/`.
- Documentar fuente, periodo temporal y frecuencia.

Decisiones pendientes:

- Número inicial de activos.
- Periodo exacto.
- Frecuencia diaria.
- Criterio de selección de activos.

---

### 3. Preprocesar datos

- Usar precios ajustados.
- Calcular log-retornos.
- Alinear fechas comunes.
- Eliminar activos con demasiados valores nulos.
- Normalizar los retornos.
- Separar entrenamiento y test mediante split temporal.
- Guardar parámetros de normalización.

---

### 4. Implementar benchmarks

Benchmark 1: cartera equiponderada.

- Todos los activos reciben el mismo peso.
- Calcular retorno acumulado, volatilidad, Sharpe y drawdown.

Benchmark 2: Markowitz clásico.

- Estimar media y covarianza con datos históricos.
- Resolver optimización long-only.
- Comparar con cartera equiponderada.

---

### 5. Implementar VAE

- Definir entrada del modelo.
- Definir encoder.
- Definir espacio latente.
- Definir decoder.
- Implementar función de pérdida: reconstrucción + KL.
- Entrenar con retornos normalizados.
- Guardar curvas de pérdida.

---

### 6. Implementar GAN/WGAN

- Definir generador.
- Definir discriminador o critic.
- Entrenar con representaciones latentes o retornos.
- Generar escenarios sintéticos.
- Evaluar estabilidad del entrenamiento.

---

### 7. Evaluar escenarios sintéticos

Comparar datos reales y generados mediante:

- Media.
- Volatilidad.
- Histogramas.
- Matriz de correlación.
- Divergencia KL.
- Distancia Wasserstein, si procede.
- Gráficos comparativos.

---

### 8. Optimizar cartera con escenarios generados

- Estimar media generada.
- Estimar covarianza generada.
- Resolver optimización long-only.
- Comparar pesos obtenidos.
- Evaluar fuera de muestra si es posible.

---

## Capítulo 7: Código fuente y datos analizados

Pendiente de redactar tras implementar el pipeline.

Secciones previstas:

- Estructura del repositorio.
- Fuente de datos.
- Descripción del conjunto de datos.
- Scripts y notebooks desarrollados.
- Reproducibilidad del experimento.

---

## Capítulo 8: Resultados y evaluación

Pendiente de redactar tras obtener resultados.

Secciones previstas:

- Evaluación de escenarios sintéticos.
- Comparación de estrategias de cartera.
- Análisis de métricas.
- Discusión de resultados.

---

## Capítulos finales pendientes

### Capítulo 9: Herramientas y tecnologías

- Revisar una vez esté definida la implementación final.
- Añadir librerías exactas empleadas.

### Capítulo 10: Marco normativo, ética y protección de datos

- Revisar redacción.
- Asegurar que se explica que no se usan datos personales.
- Revisar propiedad intelectual, uso de datos financieros y código.

### Capítulo 11: Conclusiones

- Redactar al final, cuando existan resultados.
- Conectar objetivos, metodología y resultados.

### Capítulo 12: Limitaciones y prospectiva

Incluir:

- Limitación del universo de activos.
- Limitaciones computacionales.
- Sensibilidad del entrenamiento de modelos generativos.
- Ausencia de costes de transacción.
- Posible extensión a modelos de difusión.
- Posible extensión a rebalanceo dinámico.

---

## Revisión formal pendiente

- Redactar resumen.
- Redactar abstract.
- Añadir palabras clave.
- Revisar citas APA.
- Revisar referencias bibliográficas.
- Añadir figuras al marco teórico.
- Revisar índice de figuras y tablas.
- Revisar que todos los capítulos principales empiezan en página nueva.
- Revisión ortográfica completa.
- Comprobar extensión mínima exigida.
- Compilar versión final sin warnings graves.