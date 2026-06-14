from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

GENERATED_DIR = PROJECT_ROOT / "data" / "generated"

EQUAL_WEIGHT_METRICS_FILE = GENERATED_DIR / "equal_weight_metrics.csv"
MARKOWITZ_METRICS_FILE = GENERATED_DIR / "markowitz_metrics.csv"
MARKOWITZ_CONSTRAINED_METRICS_FILE = GENERATED_DIR / "markowitz_constrained_metrics.csv"

OUTPUT_FILE = GENERATED_DIR / "benchmark_comparison.csv"


def load_metrics(file_path: Path, strategy_name: str) -> pd.DataFrame:
    """
    Carga un archivo de métricas y añade el nombre de la estrategia.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"No se encuentra el archivo: {file_path}")

    metrics = pd.read_csv(file_path)
    metrics.insert(0, "strategy", strategy_name)

    return metrics


def compare_benchmarks() -> None:
    """
    Consolida las métricas de los benchmarks implementados.
    """
    benchmark_metrics = [
        load_metrics(EQUAL_WEIGHT_METRICS_FILE, "Equal Weight"),
        load_metrics(MARKOWITZ_METRICS_FILE, "Markowitz"),
        load_metrics(MARKOWITZ_CONSTRAINED_METRICS_FILE, "Markowitz Constrained"),
    ]

    comparison = pd.concat(benchmark_metrics, ignore_index=True)

    comparison.to_csv(OUTPUT_FILE, index=False)

    print("Comparación de benchmarks generada correctamente.")
    print(f"Archivo guardado en: {OUTPUT_FILE}")
    print()
    print(comparison)


if __name__ == "__main__":
    compare_benchmarks()