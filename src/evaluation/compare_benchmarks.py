from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

GENERATED_DIR = PROJECT_ROOT / "data" / "generated"

EQUAL_WEIGHT_METRICS_FILE = GENERATED_DIR / "equal_weight_metrics.csv"
MARKOWITZ_METRICS_FILE = GENERATED_DIR / "markowitz_metrics.csv"
MARKOWITZ_CONSTRAINED_METRICS_FILE = GENERATED_DIR / "markowitz_constrained_metrics.csv"
VAE_SYNTHETIC_MARKOWITZ_METRICS_FILE = GENERATED_DIR / "vae_synthetic_markowitz_metrics.csv"

OUTPUT_FILE = GENERATED_DIR / "benchmark_comparison.csv"
FORMATTED_OUTPUT_FILE = GENERATED_DIR / "benchmark_comparison_formatted.csv"


def load_metrics(file_path: Path, strategy_name: str) -> pd.DataFrame:
    """
    Carga un archivo de métricas y añade el nombre de la estrategia.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"No se encuentra el archivo: {file_path}")

    metrics = pd.read_csv(file_path)
    metrics.insert(0, "strategy", strategy_name)

    return metrics


def format_percentage(value: float) -> str:
    """
    Convierte un valor decimal en porcentaje con dos decimales.
    """
    return f"{value * 100:.2f} %"


def format_decimal(value: float) -> str:
    """
    Formatea un número decimal con dos decimales.
    """
    return f"{value:.2f}"


def create_formatted_comparison(comparison: pd.DataFrame) -> pd.DataFrame:
    """
    Crea una versión formateada de la tabla comparativa para lectura y memoria.
    """
    formatted = comparison.copy()

    percentage_columns = [
        "cumulative_return",
        "annualized_return",
        "annualized_volatility",
        "max_drawdown",
    ]

    for column in percentage_columns:
        formatted[column] = formatted[column].apply(format_percentage)

    formatted["sharpe_ratio"] = formatted["sharpe_ratio"].apply(format_decimal)

    formatted = formatted.rename(
        columns={
            "strategy": "Estrategia",
            "cumulative_return": "Retorno acumulado",
            "annualized_return": "Retorno anualizado",
            "annualized_volatility": "Volatilidad anualizada",
            "sharpe_ratio": "Ratio de Sharpe",
            "max_drawdown": "Máximo drawdown",
        }
    )

    return formatted


def compare_benchmarks() -> None:
    """
    Consolida las métricas de los benchmarks implementados.
    """
    benchmark_metrics = [
        load_metrics(EQUAL_WEIGHT_METRICS_FILE, "Equal Weight"),
        load_metrics(MARKOWITZ_METRICS_FILE, "Markowitz"),
        load_metrics(MARKOWITZ_CONSTRAINED_METRICS_FILE, "Markowitz Constrained"),
        load_metrics(VAE_SYNTHETIC_MARKOWITZ_METRICS_FILE, "VAE Synthetic Markowitz"),
    ]

    comparison = pd.concat(benchmark_metrics, ignore_index=True)

    formatted_comparison = create_formatted_comparison(comparison)

    comparison.to_csv(OUTPUT_FILE, index=False)
    formatted_comparison.to_csv(FORMATTED_OUTPUT_FILE, index=False)

    print("Comparación de benchmarks generada correctamente.")
    print(f"Archivo guardado en: {OUTPUT_FILE}")
    print(f"Archivo formateado guardado en: {FORMATTED_OUTPUT_FILE}")
    print()
    print(comparison)
    print()
    print("Tabla formateada:")
    print(formatted_comparison)


if __name__ == "__main__":
    compare_benchmarks()