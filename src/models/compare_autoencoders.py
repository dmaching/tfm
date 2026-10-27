from pathlib import Path
import sys

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.models.vae import VariationalAutoencoder


TRAIN_FILE = PROJECT_ROOT / "data" / "processed" / "returns_train_scaled.csv"
TEST_FILE = PROJECT_ROOT / "data" / "processed" / "returns_test_scaled.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "generated" / "autoencoder_model_comparison.csv"
MULTISEED_OUTPUT_FILE = PROJECT_ROOT / "data" / "generated" / "autoencoder_model_comparison_multiseed.csv"
SUMMARY_OUTPUT_FILE = PROJECT_ROOT / "data" / "generated" / "autoencoder_model_comparison_multiseed_summary.csv"
LATEX_FILE = PROJECT_ROOT / "latex" / "snippets" / "autoencoder_model_comparison.tex"

SEEDS = (42, 123, 2026)
EPOCHS = 120
BATCH_SIZE = 64
LEARNING_RATE = 1e-3
HIDDEN_DIM = 64
N_SCENARIOS = 5000


class Autoencoder(nn.Module):
    def __init__(self, input_dim: int, latent_dim: int):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, HIDDEN_DIM), nn.ReLU(),
            nn.Linear(HIDDEN_DIM, HIDDEN_DIM), nn.ReLU(),
            nn.Linear(HIDDEN_DIM, latent_dim),
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, HIDDEN_DIM), nn.ReLU(),
            nn.Linear(HIDDEN_DIM, HIDDEN_DIM), nn.ReLU(),
            nn.Linear(HIDDEN_DIM, input_dim), nn.Tanh(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.decoder(self.encoder(x))


def reset_seed(seed: int) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)


def errors(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    delta = x - y
    return float(np.mean(delta**2)), float(np.mean(np.abs(delta)))


def distribution_errors(real: np.ndarray, synthetic: np.ndarray) -> tuple[float, float, float]:
    mean_error = float(np.mean(np.abs(real.mean(axis=0) - synthetic.mean(axis=0))))
    volatility_error = float(np.mean(np.abs(real.std(axis=0, ddof=1) - synthetic.std(axis=0, ddof=1))))
    correlation_error = float(np.mean(np.abs(np.corrcoef(real, rowvar=False) - np.corrcoef(synthetic, rowvar=False))))
    return mean_error, volatility_error, correlation_error


def train_ae(train: torch.Tensor, test: torch.Tensor, seed: int, latent_dim: int = 8) -> dict:
    reset_seed(seed)
    model = Autoencoder(train.shape[1], latent_dim)
    loader = DataLoader(TensorDataset(train), batch_size=BATCH_SIZE, shuffle=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    model.train()
    for _ in range(EPOCHS):
        for (batch,) in loader:
            optimizer.zero_grad()
            loss = nn.functional.mse_loss(model(batch), batch)
            loss.backward()
            optimizer.step()
    model.eval()
    with torch.no_grad():
        train_hat = model(train).numpy()
        test_hat = model(test).numpy()
        latent = model.encoder(train).numpy()
        rng = np.random.default_rng(seed)
        sampled = rng.multivariate_normal(latent.mean(axis=0), np.cov(latent, rowvar=False), N_SCENARIOS)
        synthetic = model.decoder(torch.tensor(sampled, dtype=torch.float32)).numpy()
    return build_row("Autoencoder determinista", "AE-8", seed, train.numpy(), test.numpy(), train_hat, test_hat, synthetic)


def train_vae(train: torch.Tensor, test: torch.Tensor, seed: int, latent_dim: int, beta: float, label: str) -> dict:
    reset_seed(seed)
    model = VariationalAutoencoder(train.shape[1], HIDDEN_DIM, latent_dim)
    loader = DataLoader(TensorDataset(train), batch_size=BATCH_SIZE, shuffle=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    model.train()
    for _ in range(EPOCHS):
        for (batch,) in loader:
            optimizer.zero_grad()
            reconstruction, mu, logvar = model(batch)
            rec = nn.functional.mse_loss(reconstruction, batch)
            kl = -0.5 * torch.mean(torch.sum(1 + logvar - mu.pow(2) - logvar.exp(), dim=1))
            loss = rec + beta * kl
            loss.backward()
            optimizer.step()
    model.eval()
    with torch.no_grad():
        train_hat, _, _ = model(train)
        test_hat, _, _ = model(test)
        z = torch.randn(N_SCENARIOS, latent_dim)
        synthetic = model.decode(z).numpy()
    return build_row(label, f"VAE-{latent_dim}", seed, train.numpy(), test.numpy(), train_hat.numpy(), test_hat.numpy(), synthetic, beta)


def build_row(model: str, configuration: str, seed: int, train: np.ndarray, test: np.ndarray,
              train_hat: np.ndarray, test_hat: np.ndarray, synthetic: np.ndarray,
              beta: float | None = None) -> dict:
    train_mse, train_mae = errors(train, train_hat)
    test_mse, test_mae = errors(test, test_hat)
    mean_error, volatility_error, correlation_error = distribution_errors(train, synthetic)
    return {
        "model": model, "configuration": configuration, "latent_dim": int(configuration.split("-")[-1]),
        "beta": beta, "epochs": EPOCHS, "seed": seed,
        "train_mse": train_mse, "test_mse": test_mse,
        "train_mae": train_mae, "test_mae": test_mae,
        "synthetic_mean_mae": mean_error,
        "synthetic_volatility_mae": volatility_error,
        "synthetic_correlation_mae": correlation_error,
    }


def main() -> None:
    train_df = pd.read_csv(TRAIN_FILE, index_col=0)
    test_df = pd.read_csv(TEST_FILE, index_col=0)
    train = torch.tensor(train_df.values, dtype=torch.float32)
    test = torch.tensor(test_df.values, dtype=torch.float32)
    rows = []
    for seed in SEEDS:
        rows.extend([
            train_ae(train, test, seed=seed),
            train_vae(train, test, seed=seed, latent_dim=8, beta=0.001, label="VAE base"),
            train_vae(train, test, seed=seed, latent_dim=4, beta=0.001, label="VAE latente reducido"),
        ])
    result = pd.DataFrame(rows)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    LATEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(MULTISEED_OUTPUT_FILE, index=False)
    base_result = result[result["seed"] == 42].copy()
    base_result.to_csv(OUTPUT_FILE, index=False)
    metric_columns = [
        "train_mse", "test_mse", "train_mae", "test_mae",
        "synthetic_mean_mae", "synthetic_volatility_mae", "synthetic_correlation_mae",
    ]
    summary = result.groupby(["model", "configuration"], as_index=False)[metric_columns].agg(
        ["mean", "std", "min", "max", "count"]
    )
    summary.columns = ["_".join(filter(None, map(str, column))).rstrip("_") for column in summary.columns]
    summary.to_csv(SUMMARY_OUTPUT_FILE, index=False)
    formatted = base_result.copy()
    for column in ["train_mse", "test_mse", "train_mae", "test_mae", "synthetic_mean_mae", "synthetic_volatility_mae", "synthetic_correlation_mae"]:
        formatted[column] = formatted[column].map(lambda value: f"{value:.6f}")
    LATEX_FILE.write_text(formatted.to_latex(index=False, escape=True), encoding="utf-8")
    print(result.to_string(index=False))
    print(f"Saved: {MULTISEED_OUTPUT_FILE}")
    print(f"Saved: {SUMMARY_OUTPUT_FILE}")


if __name__ == "__main__":
    main()
