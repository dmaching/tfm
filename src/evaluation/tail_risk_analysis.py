"""Análisis adicional de colas y episodios de estrés del experimento base."""
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import torch

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.data.preprocess import scale_returns
from src.evaluation.metrics import historical_cvar, historical_var
from src.models.generate_vae_scenarios import generate_synthetic_scaled_returns, load_vae_model
from src.models.vae import HIDDEN_DIM, LATENT_DIM, VariationalAutoencoder, create_dataloader, set_seed, train_vae

RETURNS_FILE = PROJECT_ROOT / "data" / "processed" / "returns.csv"
TEST_FILE = PROJECT_ROOT / "data" / "processed" / "returns_test.csv"
SYNTHETIC_FILE = PROJECT_ROOT / "data" / "generated" / "vae_synthetic_returns.csv"
VAE_WEIGHTS_FILE = PROJECT_ROOT / "data" / "generated" / "vae_synthetic_markowitz_weights.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "generated" / "tail_risk"
FIGURES_DIR = PROJECT_ROOT / "figures"
N_SCENARIOS = 5000
REPRESENTATIVE_TICKERS = ["AAPL", "JPM", "XOM"]
STRESS_EPISODES = {
    "Corrección de 2018": ("2018-10-01", "2018-12-24"),
    "COVID-19": ("2020-02-20", "2020-03-23"),
}


def load_base_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    """Carga test, escenarios base y pesos VAE para la cartera agregada."""
    test_returns = pd.read_csv(TEST_FILE, index_col=0, parse_dates=True)
    synthetic_returns = pd.read_csv(SYNTHETIC_FILE)[test_returns.columns]
    weights = pd.read_csv(VAE_WEIGHTS_FILE).set_index("ticker").loc[test_returns.columns, "weight"]
    return test_returns, synthetic_returns, weights


def describe_tail(series: pd.Series, label: str, sample: str) -> dict:
    """Resume forma y cuantiles de cola; VaR y CVaR se expresan como retornos."""
    return {
        "sample": sample, "series": label, "n_observations": len(series),
        "skewness": series.skew(), "excess_kurtosis": series.kurt(),
        "var_95": historical_var(series, 0.95), "cvar_95": historical_cvar(series, 0.95),
        "var_99": historical_var(series, 0.99), "cvar_99": historical_cvar(series, 0.99),
        "p01": series.quantile(0.01), "p05": series.quantile(0.05),
        "p95": series.quantile(0.95), "p99": series.quantile(0.99),
    }


def build_tail_table(test_returns: pd.DataFrame, synthetic_returns: pd.DataFrame, weights: pd.Series) -> pd.DataFrame:
    rows = []
    for ticker in test_returns.columns:
        rows += [describe_tail(test_returns[ticker], ticker, "Real test"), describe_tail(synthetic_returns[ticker], ticker, "Sintético VAE")]
    rows += [
        describe_tail(test_returns.dot(weights), "Cartera VAE", "Real test"),
        describe_tail(synthetic_returns.dot(weights), "Cartera VAE", "Sintético VAE"),
    ]
    return pd.DataFrame(rows)


def save_distribution_plots(test_returns: pd.DataFrame, synthetic_returns: pd.DataFrame, weights: pd.Series) -> None:
    import matplotlib.pyplot as plt
    selected = [ticker for ticker in REPRESENTATIVE_TICKERS if ticker in test_returns.columns]
    series_pairs = [(ticker, test_returns[ticker], synthetic_returns[ticker]) for ticker in selected]
    series_pairs.append(("Cartera VAE", test_returns.dot(weights), synthetic_returns.dot(weights)))
    fig, axes = plt.subplots(len(series_pairs), 2, figsize=(10, 3.2 * len(series_pairs)))
    for row, (label, real, synthetic) in enumerate(series_pairs):
        axes[row, 0].hist(real, bins=35, density=True, alpha=0.55, label="Real test")
        axes[row, 0].hist(synthetic, bins=35, density=True, alpha=0.55, label="Sintético VAE")
        axes[row, 0].set_title(f"Distribución de retornos: {label}")
        axes[row, 0].legend()
        probabilities = np.linspace(0.01, 0.99, 99)
        real_q = real.quantile(probabilities).to_numpy()
        synthetic_q = synthetic.quantile(probabilities).to_numpy()
        axes[row, 1].scatter(real_q, synthetic_q, s=12)
        lower, upper = min(real_q.min(), synthetic_q.min()), max(real_q.max(), synthetic_q.max())
        axes[row, 1].plot([lower, upper], [lower, upper], color="black", linewidth=1)
        axes[row, 1].set_xlabel("Cuantiles reales de test")
        axes[row, 1].set_ylabel("Cuantiles sintéticos")
        axes[row, 1].set_title(f"QQ-plot: {label}")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "tail_risk_real_vs_synthetic.png", dpi=300)
    plt.close(fig)


def train_before_episode(train_returns: pd.DataFrame, seed: int, device: torch.device) -> pd.DataFrame:
    """Entrena el mismo VAE con datos anteriores al episodio, sin fuga temporal."""
    train_scaled, _, scaler = scale_returns(train_returns, train_returns)
    set_seed(seed)
    model = VariationalAutoencoder(train_returns.shape[1], HIDDEN_DIM, LATENT_DIM).to(device)
    train_vae(model, create_dataloader(train_scaled), device)
    synthetic_scaled = generate_synthetic_scaled_returns(model, LATENT_DIM, N_SCENARIOS, train_returns.columns.tolist(), device)
    return pd.DataFrame(scaler.inverse_transform(synthetic_scaled), columns=train_returns.columns)


def analyse_stress_episodes(returns: pd.DataFrame, device: torch.device) -> pd.DataFrame:
    """Contrasta el peor retorno diario equiponderado con escenarios previos a cada crisis."""
    rows = []
    for index, (episode, (start, end)) in enumerate(STRESS_EPISODES.items(), start=1):
        train_returns = returns.loc[returns.index < pd.Timestamp(start)]
        episode_returns = returns.loc[start:end].mean(axis=1)
        worst_return = episode_returns.min()
        worst_date = episode_returns.idxmin()
        synthetic_returns = train_before_episode(train_returns, seed=100 + index, device=device)
        synthetic_portfolio = synthetic_returns.mean(axis=1)
        percentile = float((synthetic_portfolio <= worst_return).mean() * 100)
        rows.append({
            "episode": episode, "episode_start": start, "episode_end": end,
            "training_end": train_returns.index.max().date(), "seed": 100 + index,
            "worst_daily_return_date": worst_date.date(), "observed_worst_daily_return": worst_return,
            "synthetic_p01": synthetic_portfolio.quantile(0.01), "synthetic_p05": synthetic_portfolio.quantile(0.05),
            "synthetic_minimum": synthetic_portfolio.min(), "observed_return_percentile_in_synthetic": percentile,
            "synthetic_scenarios_as_or_more_severe": int((synthetic_portfolio <= worst_return).sum()),
        })
    return pd.DataFrame(rows)


def write_paragraph(tail_table: pd.DataFrame, stress_table: pd.DataFrame) -> None:
    portfolio = tail_table[tail_table["series"] == "Cartera VAE"].set_index("sample")
    stress_text = "; ".join(
        f"{row.episode}: {row.synthetic_scenarios_as_or_more_severe} escenarios tan severos o más"
        for row in stress_table.itertuples()
    )
    text = (
        "## Extensión de colas y estrés\n\n"
        "Se compararon los retornos reales de test con los 5.000 escenarios VAE mediante asimetría, curtosis, "
        "VaR y CVaR históricos, expresados como retornos del extremo inferior. Para la cartera VAE, el CVaR al 95 % "
        f"fue {portfolio.loc['Real test', 'cvar_95']:.4f} en test y {portfolio.loc['Sintético VAE', 'cvar_95']:.4f} "
        "en los escenarios. La cobertura temporal sin fuga se evaluó reentrenando con datos anteriores a cada episodio: "
        f"{stress_text}. El resultado debe interpretarse como evidencia sobre la cobertura de cola de esta configuración, "
        "no como una garantía de riesgo futuro.\n"
    )
    (OUTPUT_DIR / "tail_risk_paragraph.md").write_text(text, encoding="utf-8")


def run_tail_risk_analysis() -> None:
    for file_path in [RETURNS_FILE, TEST_FILE, SYNTHETIC_FILE, VAE_WEIGHTS_FILE]:
        if not file_path.exists():
            raise FileNotFoundError(f"No se encuentra {file_path}.")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    test_returns, synthetic_returns, weights = load_base_data()
    tail_table = build_tail_table(test_returns, synthetic_returns, weights)
    tail_table.to_csv(OUTPUT_DIR / "tail_metrics_real_vs_synthetic.csv", index=False)
    save_distribution_plots(test_returns, synthetic_returns, weights)
    returns = pd.read_csv(RETURNS_FILE, index_col=0, parse_dates=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    stress_table = analyse_stress_episodes(returns, device)
    stress_table.to_csv(OUTPUT_DIR / "stress_episode_coverage.csv", index=False)
    write_paragraph(tail_table, stress_table)
    print("Análisis de colas completado.")
    print(tail_table[tail_table["series"] == "Cartera VAE"].to_string(index=False))
    print(stress_table.to_string(index=False))


if __name__ == "__main__":
    run_tail_risk_analysis()
