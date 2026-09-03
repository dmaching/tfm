# Extensiones metodológicas: walk-forward y análisis de colas

## Ejecución

- `python src\evaluation\walk_forward_validation.py`
- `python src\evaluation\tail_risk_analysis.py`

Las dos extensiones reutilizan la arquitectura VAE, la generación de 5.000 escenarios y las optimizaciones ya existentes. El experimento original 80/20 no se modifica; únicamente se amplían sus métricas con CVaR histórico al 95 %.

## Walk-forward

Se aplicó una ventana expanding con entrenamiento inicial del 70 % de las 2.766 observaciones y nueve folds de test consecutivos de 84 sesiones. El escalador se reajusta dentro de cada fold, el VAE se reentrena desde cero y las semillas son `43` a `51` (`42 + número de fold`).

La estrategia VAE obtuvo el Sharpe más alto en 5 de 9 folds. Su Sharpe medio fue 1,34, con desviación típica 2,03. Markowitz clásico obtuvo el Sharpe medio más alto (1,49), seguido de Markowitz restringido (1,42). Por tanto, los resultados muestran una ventaja del VAE en una mayoría limitada de ventanas, pero no una superioridad uniforme.

## Colas y episodios de estrés

El análisis compara asimetría, curtosis en exceso, VaR, CVaR y percentiles entre el test real y los 5.000 escenarios del VAE original. Para la cartera VAE, el CVaR histórico al 95 % fue -3,06 % en test y -3,37 % en los escenarios.

Para evaluar cobertura sin fuga de información se reentrenó el mismo VAE con datos previos a cada episodio. En la corrección de 2018, el peor retorno diario equiponderado fue -3,87 % el 10/10/2018; ningún escenario sintético fue igual o más severo. En COVID-19, el peor retorno fue -12,45 % el 16/03/2020; tampoco hubo escenarios igual o más severos. Esta evidencia es consistente con una suavización de extremos y debe presentarse como una limitación de cobertura de cola, no como una conclusión predictiva.

## Artefactos

- `data/generated/walk_forward/walk_forward_results_by_fold.csv`
- `data/generated/walk_forward/walk_forward_summary.csv`
- `data/generated/walk_forward/walk_forward_daily_returns.csv`
- `data/generated/walk_forward/walk_forward_paragraph.md`
- `figures/walk_forward_sharpe_by_fold.png`
- `data/generated/tail_risk/tail_metrics_real_vs_synthetic.csv`
- `data/generated/tail_risk/stress_episode_coverage.csv`
- `data/generated/tail_risk/tail_risk_paragraph.md`
- `figures/tail_risk_real_vs_synthetic.png`
