from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REAL_RETURNS_FILE = PROJECT_ROOT / "data" / "processed" / "returns_train.csv"
SYNTHETIC_RETURNS_FILE = PROJECT_ROOT / "data" / "generated" / "vae_synthetic_returns.csv"

GENERATED_DIR = PROJECT_ROOT / "data" / "generated"
FIGURES_DIR = PROJECT_ROOT / "figures"

EVALUATION_FILE = GENERATED_DIR / "vae_synthetic_evaluation.csv"

DISTRIBUTION_FIGURE_FILE = FIGURES_DIR / "vae_synthetic_distribution.png"
VOLATILITY_FIGURE_FILE = FIGURES_DIR / "vae_synthetic_volatility_comparison.png"
REAL_CORRELATION_FIGURE_FILE = FIGURES_DIR / "vae_synthetic_correlation_real.png"
SYNTHETIC_CORRELATION_FIGURE_FILE = FIGURES_DIR / "vae_synthetic_correlation_synthetic.png"


def load_returns() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Carga retornos reales de entrenamiento y escenarios sintéticos generados por el VAE.
    """
    if not REAL_RETURNS_FILE.exists():
        raise FileNotFoundError(f"No se encuentra el archivo: {REAL_RETURNS_FILE}")

    if not SYNTHETIC_RETURNS_FILE.exists():
        raise FileNotFoundError(f"No se encuentra el archivo: {SYNTHETIC_RETURNS_FILE}")

    real_returns = pd.read_csv(REAL_RETURNS_FILE, index_col=0, parse_dates=True)
    synthetic_returns = pd.read_csv(SYNTHETIC_RETURNS_FILE)

    synthetic_returns = synthetic_returns[real_returns.columns]

    return real_returns, synthetic_returns


def compute_evaluation(real_returns: pd.DataFrame, synthetic_returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula métricas comparativas por activo entre retornos reales y sintéticos.
    """
    rows = []

    for ticker in real_returns.columns:
        real = real_returns[ticker]
        synthetic = synthetic_returns[ticker]

        rows.append(
            {
                "ticker": ticker,
                "real_mean": real.mean(),
                "synthetic_mean": synthetic.mean(),
                "mean_abs_diff": abs(real.mean() - synthetic.mean()),
                "real_std": real.std(),
                "synthetic_std": synthetic.std(),
                "std_abs_diff": abs(real.std() - synthetic.std()),
                "real_skew": real.skew(),
                "synthetic_skew": synthetic.skew(),
                "real_kurtosis": real.kurtosis(),
                "synthetic_kurtosis": synthetic.kurtosis(),
                "real_min": real.min(),
                "synthetic_min": synthetic.min(),
                "real_max": real.max(),
                "synthetic_max": synthetic.max(),
            }
        )

    return pd.DataFrame(rows)


def plot_distribution(real_returns: pd.DataFrame, synthetic_returns: pd.DataFrame) -> None:
    """
    Compara la distribución agregada de retornos reales y sintéticos.
    """
    real_values = real_returns.values.flatten()
    synthetic_values = synthetic_returns.values.flatten()

    plt.figure(figsize=(8, 5))
    plt.hist(real_values, bins=100, density=True, alpha=0.5, label="Real train")
    plt.hist(synthetic_values, bins=100, density=True, alpha=0.5, label="VAE synthetic")
    plt.xlabel("Daily log return")
    plt.ylabel("Density")
    plt.title("Real vs VAE synthetic returns")
    plt.legend()
    plt.tight_layout()
    plt.savefig(DISTRIBUTION_FIGURE_FILE, dpi=300)
    plt.close()


def plot_volatility_comparison(evaluation: pd.DataFrame) -> None:
    """
    Compara volatilidad real y sintética por activo.
    """
    evaluation_sorted = evaluation.sort_values("real_std", ascending=False)

    x = np.arange(len(evaluation_sorted))
    width = 0.4

    plt.figure(figsize=(11, 5))
    plt.bar(x - width / 2, evaluation_sorted["real_std"], width, label="Real")
    plt.bar(x + width / 2, evaluation_sorted["synthetic_std"], width, label="Synthetic")
    plt.xticks(x, evaluation_sorted["ticker"], rotation=90)
    plt.xlabel("Ticker")
    plt.ylabel("Standard deviation")
    plt.title("Real vs VAE synthetic volatility by asset")
    plt.legend()
    plt.tight_layout()
    plt.savefig(VOLATILITY_FIGURE_FILE, dpi=300)
    plt.close()


def plot_correlation_matrix(correlation_matrix: pd.DataFrame, output_file: Path, title: str) -> None:
    """
    Guarda una matriz de correlación como figura.
    """
    plt.figure(figsize=(8, 7))
    plt.imshow(correlation_matrix, aspect="auto")
    plt.colorbar(label="Correlation")
    plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=90)
    plt.yticks(range(len(correlation_matrix.index)), correlation_matrix.index)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()


def evaluate_synthetic_scenarios() -> None:
    """
    Evalúa los escenarios sintéticos generados por el VAE frente a los retornos reales.
    """
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    real_returns, synthetic_returns = load_returns()

    evaluation = compute_evaluation(real_returns, synthetic_returns)
    evaluation.to_csv(EVALUATION_FILE, index=False)

    plot_distribution(real_returns, synthetic_returns)
    plot_volatility_comparison(evaluation)

    real_corr = real_returns.corr()
    synthetic_corr = synthetic_returns.corr()

    plot_correlation_matrix(
        real_corr,
        REAL_CORRELATION_FIGURE_FILE,
        "Real train correlation matrix",
    )

    plot_correlation_matrix(
        synthetic_corr,
        SYNTHETIC_CORRELATION_FIGURE_FILE,
        "VAE synthetic correlation matrix",
    )

    print("Evaluación de escenarios sintéticos completada.")
    print(f"Evaluación guardada en: {EVALUATION_FILE}")
    print(f"Distribución guardada en: {DISTRIBUTION_FIGURE_FILE}")
    print(f"Volatilidad guardada en: {VOLATILITY_FIGURE_FILE}")
    print(f"Correlación real guardada en: {REAL_CORRELATION_FIGURE_FILE}")
    print(f"Correlación sintética guardada en: {SYNTHETIC_CORRELATION_FIGURE_FILE}")
    print()
    print("Resumen agregado:")
    print(f"Diferencia media absoluta de medias: {evaluation['mean_abs_diff'].mean():.8f}")
    print(f"Diferencia media absoluta de volatilidades: {evaluation['std_abs_diff'].mean():.8f}")
    print(f"Curtosis media real: {evaluation['real_kurtosis'].mean():.4f}")
    print(f"Curtosis media sintética: {evaluation['synthetic_kurtosis'].mean():.4f}")
    print()
    print("Activos con mayor diferencia de volatilidad:")
    print(evaluation.sort_values("std_abs_diff", ascending=False).head(10))


if __name__ == "__main__":
    evaluate_synthetic_scenarios()