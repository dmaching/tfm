from pathlib import Path
import sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.evaluation.metrics import compute_metrics


SYNTHETIC_RETURNS_FILE = PROJECT_ROOT / "data" / "generated" / "vae_synthetic_returns.csv"
TEST_RETURNS_FILE = PROJECT_ROOT / "data" / "processed" / "returns_test.csv"

GENERATED_DIR = PROJECT_ROOT / "data" / "generated"

WEIGHTS_OUTPUT_FILE = GENERATED_DIR / "vae_synthetic_markowitz_weights.csv"
RETURNS_OUTPUT_FILE = GENERATED_DIR / "vae_synthetic_markowitz_returns.csv"
METRICS_OUTPUT_FILE = GENERATED_DIR / "vae_synthetic_markowitz_metrics.csv"

TRADING_DAYS = 252
RISK_FREE_RATE = 0.0
MAX_WEIGHT = 0.20


def load_returns() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Carga los escenarios sintéticos generados por el VAE y los retornos reales de test.
    """
    if not SYNTHETIC_RETURNS_FILE.exists():
        raise FileNotFoundError(
            f"No se encuentra el archivo {SYNTHETIC_RETURNS_FILE}. "
            "Ejecuta primero src\\models\\generate_vae_scenarios.py"
        )

    if not TEST_RETURNS_FILE.exists():
        raise FileNotFoundError(
            f"No se encuentra el archivo {TEST_RETURNS_FILE}. "
            "Ejecuta primero src\\data\\preprocess.py"
        )

    synthetic_returns = pd.read_csv(SYNTHETIC_RETURNS_FILE)
    test_returns = pd.read_csv(TEST_RETURNS_FILE, index_col=0, parse_dates=True)

    synthetic_returns = synthetic_returns[test_returns.columns]

    return synthetic_returns, test_returns


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


def optimize_portfolio_from_synthetic_returns(synthetic_returns: pd.DataFrame) -> pd.DataFrame:
    """
    Optimiza una cartera usando los escenarios sintéticos generados por el VAE.

    Restricciones:
    - Suma de pesos igual a 1.
    - Long-only.
    - Peso máximo por activo del 20 %.
    """
    mean_returns = synthetic_returns.mean()
    covariance_matrix = synthetic_returns.cov()

    n_assets = synthetic_returns.shape[1]
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
            f"La optimización con escenarios VAE no ha convergido: {result.message}"
        )

    weights_df = pd.DataFrame(
        {
            "ticker": synthetic_returns.columns,
            "weight": result.x,
        }
    )

    weights_df["weight"] = weights_df["weight"].round(10)

    return weights_df


def compute_test_portfolio_returns(
    test_returns: pd.DataFrame,
    weights_df: pd.DataFrame,
) -> pd.Series:
    """
    Evalúa, con datos reales de test, una cartera optimizada con escenarios sintéticos.
    """
    weights = weights_df.set_index("ticker").loc[test_returns.columns, "weight"].values

    portfolio_returns = test_returns.dot(weights)
    portfolio_returns.name = "vae_synthetic_markowitz_return"

    return portfolio_returns


def run_vae_synthetic_markowitz() -> None:
    """
    Ejecuta la optimización de cartera usando escenarios sintéticos VAE
    y evalúa el resultado sobre retornos reales de test.
    """
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    synthetic_returns, test_returns = load_returns()

    weights_df = optimize_portfolio_from_synthetic_returns(synthetic_returns)
    portfolio_returns = compute_test_portfolio_returns(test_returns, weights_df)
    metrics = compute_metrics(portfolio_returns)

    weights_df.to_csv(WEIGHTS_OUTPUT_FILE, index=False)
    portfolio_returns.to_csv(RETURNS_OUTPUT_FILE)
    metrics.to_csv(METRICS_OUTPUT_FILE, index=False)

    print("Optimización con escenarios sintéticos VAE completada.")
    print(f"Número de escenarios sintéticos: {synthetic_returns.shape[0]}")
    print(f"Número de activos: {synthetic_returns.shape[1]}")
    print(f"Peso máximo por activo: {MAX_WEIGHT:.0%}")
    print()
    print(f"Pesos guardados en: {WEIGHTS_OUTPUT_FILE}")
    print(f"Retornos guardados en: {RETURNS_OUTPUT_FILE}")
    print(f"Métricas guardadas en: {METRICS_OUTPUT_FILE}")
    print()
    print("Métricas VAE Synthetic Markowitz:")
    print(metrics.T)
    print()
    print("Pesos principales:")
    print(weights_df.sort_values("weight", ascending=False).head(10))


if __name__ == "__main__":
    run_vae_synthetic_markowitz()