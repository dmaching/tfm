from pathlib import Path
import sys

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.evaluation.metrics import compute_metrics


RETURNS_TEST_FILE = PROJECT_ROOT / "data" / "processed" / "returns_test.csv"

GENERATED_DIR = PROJECT_ROOT / "data" / "generated"
RETURNS_OUTPUT_FILE = GENERATED_DIR / "equal_weight_returns.csv"
METRICS_OUTPUT_FILE = GENERATED_DIR / "equal_weight_metrics.csv"
WEIGHTS_OUTPUT_FILE = GENERATED_DIR / "equal_weight_weights.csv"


def load_test_returns() -> pd.DataFrame:
    """
    Carga los retornos diarios del periodo de test.
    """
    if not RETURNS_TEST_FILE.exists():
        raise FileNotFoundError(
            f"No se encuentra el archivo {RETURNS_TEST_FILE}. "
            "Ejecuta primero src\\data\\preprocess.py"
        )

    returns = pd.read_csv(RETURNS_TEST_FILE, index_col=0, parse_dates=True)
    return returns


def compute_equal_weight_portfolio(returns: pd.DataFrame) -> tuple[pd.Series, pd.DataFrame]:
    """
    Calcula los retornos de una cartera equiponderada.
    """
    n_assets = returns.shape[1]

    if n_assets == 0:
        raise ValueError("El conjunto de retornos no contiene activos.")

    weights = np.repeat(1 / n_assets, n_assets)

    portfolio_returns = returns.dot(weights)
    portfolio_returns.name = "equal_weight_return"

    weights_df = pd.DataFrame(
        {
            "ticker": returns.columns,
            "weight": weights,
        }
    )

    return portfolio_returns, weights_df


def run_equal_weight_benchmark() -> None:
    """
    Ejecuta el benchmark de cartera equiponderada sobre el conjunto de test.
    """
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    returns = load_test_returns()
    portfolio_returns, weights_df = compute_equal_weight_portfolio(returns)
    metrics = compute_metrics(portfolio_returns)

    portfolio_returns.to_csv(RETURNS_OUTPUT_FILE)
    metrics.to_csv(METRICS_OUTPUT_FILE, index=False)
    weights_df.to_csv(WEIGHTS_OUTPUT_FILE, index=False)

    print("Benchmark de cartera equiponderada completado.")
    print(f"Número de activos: {returns.shape[1]}")
    print(f"Retornos guardados en: {RETURNS_OUTPUT_FILE}")
    print(f"Métricas guardadas en: {METRICS_OUTPUT_FILE}")
    print(f"Pesos guardados en: {WEIGHTS_OUTPUT_FILE}")
    print()
    print(metrics.T)


if __name__ == "__main__":
    run_equal_weight_benchmark()