# Inventario de evidencia real

## Datos disponibles

- archivo: `data/raw/sp500_prices_adj_close.csv`; descripción: cierres ajustados diarios de 30 símbolos; uso: origen de datos.
- archivo: `data/processed/returns.csv`; descripción: 2.766 log-retornos por 30 activos, 2014-01-03--2024-12-30; uso: EDA.
- archivos: `returns_train.csv` y `returns_test.csv`; descripción: 2.212 y 554 filas; uso: entrenamiento y evaluación temporal.
- archivos escalados y `minmax_scaler.pkl`; uso: entrada VAE y transformación inversa.
- archivo: `vae_synthetic_returns.csv`; descripción: 5.000 escenarios por 30 activos; uso: estimación sintética.

## Figuras disponibles

- siete figuras en `latex/figuras/eda/`: ausencias, distribución, boxplot, acumulados, volatilidad móvil, volatilidad por activo y correlación; sección: EDA; interpretación: calidad, colas, dinámica y dependencia.
- siete figuras VAE/escenarios en `figures/`; sección: entrenamiento/calidad generativa; interpretación: pérdida, reconstrucción, distribuciones, volatilidad y correlación.
- `strategy_cumulative_returns.png`; sección: resultados; interpretación: evolución comparada.

## Tablas disponibles

- cinco CSV EDA en `data/generated/eda/`; sección: EDA.
- `benchmark_comparison.csv`; sección: resultados; contiene las cinco métricas de cuatro estrategias.
- `vae_reconstruction_metrics.csv` y `vae_reconstruction_error_by_asset.csv`; sección: entrenamiento.
- `vae_synthetic_summary.csv` y `vae_synthetic_evaluation.csv`; sección: calidad de escenarios.
- CSV de pesos, retornos y métricas por estrategia; sección: optimización/evaluación.

## Modelos realmente implementados

- script: `src/models/vae.py`; modelo: VAE 30--64--64--(mu/logvar 8)--64--64--30; métricas: MSE/MAE, pérdida total/reconstrucción/KL; resultados: checkpoint, historial y reconstrucciones.
- script: `generate_vae_scenarios.py`; modelo: muestreo normal y decoder VAE; resultados: 5.000 escenarios.
- scripts en `src/optimization/`; modelos: equiponderada, Markowitz, Markowitz restringido y Markowitz con escenarios VAE; métricas: retorno, volatilidad, Sharpe y drawdown.

## Modelos mencionados solo a nivel teórico

- GAN, WGAN y VAE-GAN; aparecen en introducción, marco teórico y metodología antigua; recomendación: teoría, planteamiento inicial o trabajo futuro.
- modelos de difusión; aparecen en estado del arte; recomendación: prospectiva.

## Resultados disponibles

- VAE: MSE train 0,0077697; test 0,0104900; MAE train 0,0602216; test 0,0685689.
- carteras: equiponderada 64,93 %, Sharpe 1,88; Markowitz 95,60 %, 1,89; restringida 101,38 %, 2,20; VAE sintético 242,32 %, 2,99. Volatilidades: 13,58 %, 18,86 %, 17,01 % y 25,08 %.

## Bibliografía disponible

- número de entradas: 18.
- referencias citadas inicialmente: 12 claves aproximadamente.
- referencias no citadas inicialmente: trabajos locales sobre aprendizaje profundo, finanzas generativas y evaluación; se incorporaron citas contextuales sin añadir referencias no verificadas.
