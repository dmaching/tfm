from pathlib import Path
import sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.evaluation.metrics import compute_metrics


RETURNS_TRAIN_FILE = PROJECT_ROOT / "data" / "processed" / "returns_train.csv"
RETURNS_TEST_FILE = PROJECT_ROOT / "data" / "processed" / "returns_test.csv"

GENERATED_DIR = PROJECT_ROOT / "data" / "generated"

WEIGHTS_OUTPUT_FILE = GENERATED_DIR / "markowitz_constrained_weights.csv"
RETURNS_OUTPUT_FILE = GENERATED_DIR / "markowitz_constrained_returns.csv"
METRICS_OUTPUT_FILE = GENERATED_DIR / "markowitz_constrained_metrics.csv"

TRADING_DAYS = 252
RISK_FREE_RATE = 0.0
MAX_WEIGHT = 0.20


def load_returns() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Carga los retornos de entrenamiento y test generados en el preprocesamiento.
    """
    if not RETURNS_TRAIN_FILE.exists():
        raise FileNotFoundError(
            f"No se encuentra el archivo {RETURNS_TRAIN_FILE}. "
            "Ejecuta primero src\\data\\preprocess.py"
        )

    if not RETURNS_TEST_FILE.exists():
        raise FileNotFoundError(
            f"No se encuentra el archivo {RETURNS_TEST_FILE}. "
            "Ejecuta primero src\\data\\preprocess.py"
        )

    train_returns = pd.read_csv(RETURNS_TRAIN_FILE, index_col=0, parse_dates=True)
    test_returns = pd.read_csv(RETURNS_TEST_FILE, index_col=0, parse_dates=True)

    return train_returns, test_returns


def portfolio_return(weights: np.ndarray, mean_returns: pd.Series) -> float:
    """
    Calcula el retorno esperado anualizado de una cartera.
    """
    return float(np.dot(weights, mean_returns) * TRADING_DAYS)


def portfolio_volatility(weights: np.ndarray, covariance_matrix: pd.DataFrame) -> float:
    """
    Calcula la volatilidad anualizada de una cartera.
    """
    variance = np.dot(weights.T, np.dot(covariance_matrix * TRADING_DAYS, weights))
    return float(np.sqrt(variance))


def negative_sharpe_ratio(
    weights: np.ndarray,
    mean_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
    risk_free_rate: float = RISK_FREE_RATE,
) -> float:
    """
    Función objetivo: negativo del ratio de Sharpe.
    """
    expected_return = portfolio_return(weights, mean_returns)
    expected_volatility = portfolio_volatility(weights, covariance_matrix)

    if expected_volatility == 0:
        return np.inf

    sharpe = (expected_return - risk_free_rate) / expected_volatility

    return -sharpe


def optimize_constrained_markowitz_portfolio(train_returns: pd.DataFrame) -> pd.DataFrame:
    """
    Optimiza una cartera media-varianza con restricciones adicionales de diversificación.

    Restricciones:
    - La suma de pesos debe ser igual a 1.
    - No se permiten posiciones cortas.
    - Ningún activo puede superar MAX_WEIGHT.
    """
    mean_returns = train_returns.mean()
    covariance_matrix = train_returns.cov()

    n_assets = train_returns.shape[1]
    initial_weights = np.repeat(1 / n_assets, n_assets)

    bounds = tuple((0.0, MAX_WEIGHT) for _ in range(n_assets))

    constraints = (
        {
            "type": "eq",
            "fun": lambda weights: np.sum(weights) - 1,
        },
    )

    result = minimize(
        fun=negative_sharpe_ratio,
        x0=initial_weights,
        args=(mean_returns, covariance_matrix),
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={
            "maxiter": 1000,
            "ftol": 1e-9,
            "disp": False,
        },
    )

    if not result.success:
        raise RuntimeError(
            f"La optimización de Markowitz restringido no ha convergido: {result.message}"
        )

    weights_df = pd.DataFrame(
        {
            "ticker": train_returns.columns,
            "weight": result.x,
        }
    )

    weights_df["weight"] = weights_df["weight"].round(10)

    return weights_df


def compute_portfolio_test_returns(
    test_returns: pd.DataFrame,
    weights_df: pd.DataFrame,
) -> pd.Series:
    """
    Evalúa la cartera optimizada sobre el conjunto de test.
    """
    weights = weights_df.set_index("ticker").loc[test_returns.columns, "weight"].values

    portfolio_returns = test_returns.dot(weights)
    portfolio_returns.name = "markowitz_constrained_return"

    return portfolio_returns


def run_constrained_markowitz_benchmark() -> None:
    """
    Ejecuta el benchmark de Markowitz con límite máximo de peso por activo.
    """
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    train_returns, test_returns = load_returns()

    weights_df = optimize_constrained_markowitz_portfolio(train_returns)
    portfolio_returns = compute_portfolio_test_returns(test_returns, weights_df)
    metrics = compute_metrics(portfolio_returns)

    weights_df.to_csv(WEIGHTS_OUTPUT_FILE, index=False)
    portfolio_returns.to_csv(RETURNS_OUTPUT_FILE)
    metrics.to_csv(METRICS_OUTPUT_FILE, index=False)

    print("Benchmark de Markowitz restringido completado.")
    print(f"Número de activos: {train_returns.shape[1]}")
    print(f"Peso máximo por activo: {MAX_WEIGHT:.0%}")
    print(f"Periodo train: {train_returns.index.min().date()} a {train_returns.index.max().date()}")
    print(f"Periodo test: {test_returns.index.min().date()} a {test_returns.index.max().date()}")
    print()
    print(f"Pesos guardados en: {WEIGHTS_OUTPUT_FILE}")
    print(f"Retornos guardados en: {RETURNS_OUTPUT_FILE}")
    print(f"Métricas guardadas en: {METRICS_OUTPUT_FILE}")
    print()
    print("Métricas Markowitz restringido:")
    print(metrics.T)
    print()
    print("Pesos principales:")
    print(weights_df.sort_values("weight", ascending=False).head(10))


if __name__ == "__main__":
    run_constrained_markowitz_benchmark()