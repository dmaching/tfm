"""Generate reproducible EDA tables and figures from existing return data."""

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
GENERATED_DIR = PROJECT_ROOT / "data" / "generated"
EDA_TABLE_DIR = GENERATED_DIR / "eda"
EDA_FIGURE_DIR = PROJECT_ROOT / "latex" / "figuras" / "eda"

PREFERRED_INPUTS = (
    PROCESSED_DIR / "returns.csv",
    PROCESSED_DIR / "returns_train.csv",
    GENERATED_DIR / "vae_synthetic_returns.csv",
)


def find_input_csv() -> Path:
    """Select an existing returns CSV without modifying any source data."""
    for path in PREFERRED_INPUTS:
        if path.exists():
            return path

    searched = "\n".join(f"  - {path.relative_to(PROJECT_ROOT)}" for path in PREFERRED_INPUTS)
    raise FileNotFoundError(
        "No se encontró un CSV de retornos para el EDA. Rutas comprobadas:\n"
        f"{searched}\n"
        "Ejecuta primero src/data/preprocess.py o proporciona uno de esos archivos."
    )


def load_returns(path: Path) -> pd.DataFrame:
    """Load a date-indexed numeric returns table."""
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    data = data.apply(pd.to_numeric, errors="coerce").sort_index()
    if data.empty or data.shape[1] == 0:
        raise ValueError(f"El archivo {path} no contiene columnas de retornos utilizables.")
    if not isinstance(data.index, pd.DatetimeIndex):
        raise ValueError(f"El índice de {path} no se pudo interpretar como fechas.")
    return data


def save_tables(returns: pd.DataFrame) -> list[Path]:
    """Create the requested CSV summaries."""
    EDA_TABLE_DIR.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    shape = pd.DataFrame(
        [{"rows": returns.shape[0], "columns": returns.shape[1],
          "start_date": returns.index.min(), "end_date": returns.index.max()}]
    )
    missing = pd.DataFrame({
        "missing_count": returns.isna().sum(),
        "missing_percentage": returns.isna().mean().mul(100),
    })
    descriptive = returns.describe().T
    skew_kurtosis = pd.DataFrame({
        "skewness": returns.skew(),
        "kurtosis": returns.kurtosis(),
    })

    correlation = returns.corr()
    upper_mask = np.triu(np.ones(correlation.shape, dtype=bool), k=1)
    top_correlations = (
        correlation.where(upper_mask)
        .stack()
        .rename("correlation")
        .reset_index()
        .rename(columns={"level_0": "asset_1", "level_1": "asset_2"})
    )
    top_correlations["absolute_correlation"] = top_correlations["correlation"].abs()
    top_correlations = top_correlations.sort_values("absolute_correlation", ascending=False).head(50)

    tables = {
        "eda_dataset_shape.csv": (shape, False),
        "eda_missing_values.csv": (missing, True),
        "eda_descriptive_statistics.csv": (descriptive, True),
        "eda_skewness_kurtosis.csv": (skew_kurtosis, True),
        "eda_top_correlations.csv": (top_correlations, False),
    }
    for filename, (table, include_index) in tables.items():
        output = EDA_TABLE_DIR / filename
        table.to_csv(output, index=include_index, index_label="asset" if include_index else None)
        outputs.append(output)
    return outputs


def finish_figure(plt, path: Path) -> Path:
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    return path


def save_figures(returns: pd.DataFrame) -> list[Path]:
    """Create the requested PNG figures using matplotlib only."""
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "Falta matplotlib. Instala las dependencias de requirements.txt antes de generar las figuras EDA."
        ) from exc
    EDA_FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    clean = returns.dropna(how="all")
    sample_columns = clean.columns[: min(5, clean.shape[1])]

    missing = returns.isna().sum().sort_values(ascending=False)
    missing.plot(kind="bar", figsize=(12, 5), color="#005B96")
    plt.title("Valores perdidos por activo")
    plt.xlabel("Activo")
    plt.ylabel("Número de valores perdidos")
    outputs.append(finish_figure(plt, EDA_FIGURE_DIR / "missing_values_by_asset.png"))

    values = clean.to_numpy().ravel()
    values = values[np.isfinite(values)]
    plt.figure(figsize=(9, 5))
    plt.hist(values, bins=80, color="#005B96", alpha=0.8)
    plt.title("Distribución agregada de retornos")
    plt.xlabel("Retorno")
    plt.ylabel("Frecuencia")
    outputs.append(finish_figure(plt, EDA_FIGURE_DIR / "returns_distribution.png"))

    clean[sample_columns].plot(kind="box", figsize=(10, 5), rot=45)
    plt.title("Distribución de retornos por activo (muestra)")
    plt.ylabel("Retorno")
    outputs.append(finish_figure(plt, EDA_FIGURE_DIR / "returns_boxplot.png"))

    (1 + clean[sample_columns].fillna(0)).cumprod().plot(figsize=(11, 6))
    plt.title("Rendimiento acumulado (muestra)")
    plt.xlabel("Fecha")
    plt.ylabel("Crecimiento de una unidad monetaria")
    outputs.append(finish_figure(plt, EDA_FIGURE_DIR / "cumulative_returns_sample.png"))

    clean[sample_columns].rolling(window=21, min_periods=10).std().mul(np.sqrt(252)).plot(figsize=(11, 6))
    plt.title("Volatilidad móvil anualizada de 21 sesiones (muestra)")
    plt.xlabel("Fecha")
    plt.ylabel("Volatilidad anualizada")
    outputs.append(finish_figure(plt, EDA_FIGURE_DIR / "rolling_volatility_sample.png"))

    correlation = clean.corr()
    plt.figure(figsize=(10, 8))
    image = plt.imshow(correlation, vmin=-1, vmax=1, cmap="coolwarm", aspect="auto")
    plt.colorbar(image, label="Correlación")
    plt.xticks(range(len(correlation.columns)), correlation.columns, rotation=90, fontsize=6)
    plt.yticks(range(len(correlation.index)), correlation.index, fontsize=6)
    plt.title("Matriz de correlaciones")
    outputs.append(finish_figure(plt, EDA_FIGURE_DIR / "correlation_heatmap.png"))

    summary = pd.DataFrame({"Media": clean.mean(), "Volatilidad": clean.std()})
    summary.sort_values("Volatilidad", ascending=False).plot(kind="bar", figsize=(12, 6))
    plt.title("Media y volatilidad diaria por activo")
    plt.xlabel("Activo")
    plt.ylabel("Valor diario")
    outputs.append(finish_figure(plt, EDA_FIGURE_DIR / "mean_volatility_by_asset.png"))
    return outputs


def main() -> None:
    input_path = find_input_csv()
    returns = load_returns(input_path)
    outputs = save_tables(returns) + save_figures(returns)
    print(f"EDA generado desde: {input_path.relative_to(PROJECT_ROOT)}")
    print(f"Dimensiones analizadas: {returns.shape[0]} filas x {returns.shape[1]} columnas")
    print("Archivos generados:")
    for output in outputs:
        print(f"  - {output.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
