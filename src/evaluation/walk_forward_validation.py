"""Extensión walk-forward expanding del experimento original."""
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import torch

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.data.preprocess import scale_returns
from src.evaluation.metrics import compute_metrics
from src.models.generate_vae_scenarios import generate_synthetic_scaled_returns
from src.models.vae import HIDDEN_DIM, LATENT_DIM, VariationalAutoencoder, create_dataloader, set_seed, train_vae
from src.optimization.equal_weight import compute_equal_weight_portfolio
from src.optimization.markowitz import compute_portfolio_test_returns as evaluate_markowitz, optimize_markowitz_portfolio
from src.optimization.markowitz_constrained import optimize_constrained_markowitz_portfolio
from src.optimization.vae_synthetic_markowitz import compute_test_portfolio_returns as evaluate_vae, optimize_portfolio_from_synthetic_returns

RETURNS_FILE = PROJECT_ROOT / "data" / "processed" / "returns.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "generated" / "walk_forward"
FIGURES_DIR = PROJECT_ROOT / "figures"
INITIAL_TRAIN_RATIO = 0.70
TEST_WINDOW = 84
WINDOW_TYPE = "expanding"
N_SCENARIOS = 5000
BASE_SEED = 42


def build_folds(n_observations: int) -> list[tuple[int, int, int]]:
    """Construye folds expanding con periodos de test no solapados."""
    test_start = int(n_observations * INITIAL_TRAIN_RATIO)
    folds = []
    fold = 1
    while test_start + TEST_WINDOW <= n_observations:
        folds.append((fold, test_start, test_start + TEST_WINDOW))
        fold += 1
        test_start += TEST_WINDOW
    return folds


def evaluate_fold(returns: pd.DataFrame, fold: int, test_start: int, test_end: int, device: torch.device) -> tuple[list[dict], pd.DataFrame]:
    """Reentrena el VAE y evalúa las cuatro estrategias en un fold."""
    train_returns = returns.iloc[:test_start].copy()
    test_returns = returns.iloc[test_start:test_end].copy()
    train_scaled, _, scaler = scale_returns(train_returns, test_returns)
    seed = BASE_SEED + fold
    set_seed(seed)
    model = VariationalAutoencoder(train_scaled.shape[1], HIDDEN_DIM, LATENT_DIM).to(device)
    train_vae(model, create_dataloader(train_scaled), device)
    synthetic_scaled = generate_synthetic_scaled_returns(model, LATENT_DIM, N_SCENARIOS, train_returns.columns.tolist(), device)
    synthetic_returns = pd.DataFrame(scaler.inverse_transform(synthetic_scaled), columns=train_returns.columns)

    strategies = {
        "Equal Weight": compute_equal_weight_portfolio(test_returns)[0],
        "Markowitz": evaluate_markowitz(test_returns, optimize_markowitz_portfolio(train_returns)),
        "Markowitz Constrained": evaluate_markowitz(test_returns, optimize_constrained_markowitz_portfolio(train_returns)),
        "VAE Synthetic Markowitz": evaluate_vae(test_returns, optimize_portfolio_from_synthetic_returns(synthetic_returns)),
    }
    rows, returns_rows = [], []
    for strategy, portfolio_returns in strategies.items():
        rows.append({
            "fold": fold, "seed": seed,
            "train_start": train_returns.index.min().date(), "train_end": train_returns.index.max().date(),
            "test_start": test_returns.index.min().date(), "test_end": test_returns.index.max().date(),
            "n_train": len(train_returns), "n_test": len(test_returns), "strategy": strategy,
            **compute_metrics(portfolio_returns).iloc[0].to_dict(),
        })
        returns_rows.append(pd.DataFrame({"date": portfolio_returns.index, "fold": fold, "strategy": strategy, "daily_return": portfolio_returns.values}))
    return rows, pd.concat(returns_rows, ignore_index=True)


def save_sharpe_plot(results: pd.DataFrame) -> None:
    import matplotlib.pyplot as plt
    plt.figure(figsize=(9, 5))
    for strategy, group in results.groupby("strategy", sort=False):
        plt.plot(group["fold"], group["sharpe_ratio"], marker="o", label=strategy)
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xlabel("Fold")
    plt.ylabel("Ratio de Sharpe anualizado")
    plt.title("Walk-forward: Sharpe por fold y estrategia")
    plt.xticks(sorted(results["fold"].unique()))
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "walk_forward_sharpe_by_fold.png", dpi=300)
    plt.close()


def write_summary(results: pd.DataFrame) -> None:
    vae = results[results["strategy"] == "VAE Synthetic Markowitz"]
    winners = results.loc[results.groupby("fold")["sharpe_ratio"].idxmax()]
    vae_wins = int((winners["strategy"] == "VAE Synthetic Markowitz").sum())
    text = (
        "## Extensión walk-forward\n\n"
        f"Se aplicó una validación expanding con {results['fold'].nunique()} folds de {TEST_WINDOW} sesiones. "
        "En cada fold se reajustó el escalador con el train, se reentrenó el VAE desde cero y se generaron 5.000 escenarios. "
        f"La estrategia VAE obtuvo el mayor Sharpe en {vae_wins} de {results['fold'].nunique()} folds; "
        f"su Sharpe medio fue {vae['sharpe_ratio'].mean():.2f} (desviación típica {vae['sharpe_ratio'].std():.2f}). "
        "Este resultado describe la consistencia observada en estas ventanas y no implica superioridad general.\n"
    )
    (OUTPUT_DIR / "walk_forward_paragraph.md").write_text(text, encoding="utf-8")


def run_walk_forward_validation() -> None:
    if not RETURNS_FILE.exists():
        raise FileNotFoundError(f"No se encuentra {RETURNS_FILE}. Ejecuta preprocess.py primero.")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    returns = pd.read_csv(RETURNS_FILE, index_col=0, parse_dates=True)
    folds = build_folds(len(returns))
    if not folds:
        raise ValueError("No hay observaciones suficientes para construir folds walk-forward.")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    all_rows, all_returns = [], []
    print(f"Walk-forward {WINDOW_TYPE}: {len(folds)} folds, test de {TEST_WINDOW} sesiones.")
    for fold, test_start, test_end in folds:
        print(f"\nFold {fold}/{len(folds)} (semilla {BASE_SEED + fold})")
        rows, fold_returns = evaluate_fold(returns, fold, test_start, test_end, device)
        all_rows.extend(rows)
        all_returns.append(fold_returns)
    results = pd.DataFrame(all_rows)
    metrics = ["cumulative_return", "annualized_return", "annualized_volatility", "sharpe_ratio", "max_drawdown", "cvar_95"]
    summary = results.groupby("strategy", sort=False)[metrics].agg(["mean", "std"])
    summary.columns = [f"{metric}_{stat}" for metric, stat in summary.columns]
    summary = summary.reset_index()
    results.to_csv(OUTPUT_DIR / "walk_forward_results_by_fold.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "walk_forward_summary.csv", index=False)
    pd.concat(all_returns, ignore_index=True).to_csv(OUTPUT_DIR / "walk_forward_daily_returns.csv", index=False)
    save_sharpe_plot(results)
    write_summary(results)
    print("\nResultados guardados en:", OUTPUT_DIR)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run_walk_forward_validation()
