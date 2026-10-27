# Generación de escenarios sintéticos para optimización de carteras

Código y memoria de un Trabajo de Fin de Máster sobre el uso de un autoencoder variacional (VAE) para generar escenarios conjuntos de retornos y aplicarlos a la optimización de carteras del S&P 500.

El estudio compara cuatro estrategias fuera de muestra:

- cartera equiponderada;
- Markowitz clásico;
- Markowitz con restricciones de pesos;
- Markowitz estimado a partir de escenarios sintéticos del VAE.

También incluye una validación *walk-forward* y un análisis de riesgo de cola. Los resultados son de carácter académico y no constituyen asesoramiento financiero.

## Contenido

```text
src/
├── analysis/       # Análisis exploratorio y figuras
├── data/           # Descarga y preprocesamiento
├── evaluation/     # Métricas, comparativas y validaciones
├── models/         # VAE y comparación de autoencoders
└── optimization/   # Estrategias de cartera
figures/            # Figuras finales empleadas en la memoria
latex/              # Fuentes LaTeX y PDF final
data/               # Estructura para datos regenerables (no versionados)
```

La [memoria final](latex/main.pdf) documenta la metodología, los experimentos, los resultados y las limitaciones.

## Requisitos

- Python 3.11 o posterior
- Una distribución LaTeX compatible con `pdflatex` y BibTeX, solo si se desea recompilar la memoria

Instalación recomendada:

```bash
python -m venv .venv
```

En Linux o macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Reproducción del experimento

Ejecuta los comandos desde la raíz del repositorio y en el orden indicado:

```bash
python -m src.data.download_data
python -m src.data.preprocess
python -m src.analysis.generate_eda_outputs
python -m src.models.vae
python -m src.models.generate_vae_scenarios
python -m src.models.compare_autoencoders
python -m src.evaluation.evaluate_vae
python -m src.evaluation.evaluate_synthetic_scenarios
python -m src.optimization.equal_weight
python -m src.optimization.markowitz
python -m src.optimization.markowitz_constrained
python -m src.optimization.vae_synthetic_markowitz
python -m src.evaluation.compare_benchmarks
python -m src.evaluation.plot_strategy_comparison
python -m src.evaluation.walk_forward_validation
python -m src.evaluation.tail_risk_analysis
```

La descarga usa Yahoo Finance a través de `yfinance`. Los datos, modelos entrenados y resultados tabulares se generan localmente en `data/` y `models/`; no se incluyen en el control de versiones. Las figuras finales sí se conservan para que la memoria pueda consultarse sin repetir el entrenamiento.

## Compilar la memoria

Desde el directorio `latex/`:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Autor

Daniel Machín González
