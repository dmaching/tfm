from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

GENERATED_DIR = PROJECT_ROOT / "data" / "generated"
FIGURES_DIR = PROJECT_ROOT / "figures"

RETURNS_FILES = {
    "Equal Weight": GENERATED_DIR / "equal_weight_returns.csv",
    "Markowitz": GENERATED_DIR / "markowitz_returns.csv",
    "Markowitz Constrained": GENERATED_DIR / "markowitz_constrained_returns.csv",
    "VAE Synthetic Markowitz": GENERATED_DIR / "vae_synthetic_markowitz_returns.csv",
}

OUTPUT_FILE = FIGURES_DIR / "strategy_cumulative_returns.png"


def load_strategy_returns() -> pd.DataFrame:
    """
    Carga los retornos diarios de las estrategias evaluadas.
    """
    returns = []

    for strategy_name, file_path in RETURNS_FILES.items():
        if not file_path.exists():
            raise FileNotFoundError(f"No se encuentra el archivo: {file_path}")

        strategy_returns = pd.read_csv(file_path, index_col=0, parse_dates=True)

        first_column = strategy_returns.columns[0]
        strategy_returns = strategy_returns.rename(columns={first_column: strategy_name})

        returns.append(strategy_returns[[strategy_name]])

    combined_returns = pd.concat(returns, axis=1)

    return combined_returns


def compute_cumulative_returns(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula la evolución acumulada de cada estrategia.
    """
    cumulative_returns = (1 + returns).cumprod() - 1

    return cumulative_returns


def plot_cumulative_returns(cumulative_returns: pd.DataFrame) -> None:
    """
    Genera la figura de retornos acumulados.
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))

    for column in cumulative_returns.columns:
        plt.plot(cumulative_returns.index, cumulative_returns[column], label=column)

    plt.xlabel("Date")
    plt.ylabel("Cumulative return")
    plt.title("Cumulative returns by strategy")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300)
    plt.close()


def run_plot_strategy_comparison() -> None:
    """
    Ejecuta la comparación gráfica de estrategias.
    """
    strategy_returns = load_strategy_returns()
    cumulative_returns = compute_cumulative_returns(strategy_returns)

    plot_cumulative_returns(cumulative_returns)

    print("Figura de comparación de estrategias generada correctamente.")
    print(f"Archivo guardado en: {OUTPUT_FILE}")
    print()
    print("Retornos acumulados finales:")
    print(cumulative_returns.tail(1).T)


if __name__ == "__main__":
    run_plot_strategy_comparison()