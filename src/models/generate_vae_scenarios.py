from pathlib import Path
import sys

import joblib
import numpy as np
import pandas as pd
import torch
from torch import nn


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.models.vae import VariationalAutoencoder


TRAIN_RETURNS_FILE = PROJECT_ROOT / "data" / "processed" / "returns_train.csv"
TRAIN_SCALED_FILE = PROJECT_ROOT / "data" / "processed" / "returns_train_scaled.csv"
SCALER_FILE = PROJECT_ROOT / "data" / "processed" / "minmax_scaler.pkl"

MODEL_FILE = PROJECT_ROOT / "models" / "vae.pt"

GENERATED_DIR = PROJECT_ROOT / "data" / "generated"
SYNTHETIC_SCALED_FILE = GENERATED_DIR / "vae_synthetic_returns_scaled.csv"
SYNTHETIC_RETURNS_FILE = GENERATED_DIR / "vae_synthetic_returns.csv"
SYNTHETIC_SUMMARY_FILE = GENERATED_DIR / "vae_synthetic_summary.csv"

N_SCENARIOS = 5000
RANDOM_SEED = 42


def set_seed(seed: int = RANDOM_SEED) -> None:
    """
    Fija semillas para reproducibilidad.
    """
    np.random.seed(seed)
    torch.manual_seed(seed)


def load_training_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Carga retornos reales y escalados de entrenamiento.
    """
    if not TRAIN_RETURNS_FILE.exists():
        raise FileNotFoundError(f"No se encuentra el archivo: {TRAIN_RETURNS_FILE}")

    if not TRAIN_SCALED_FILE.exists():
        raise FileNotFoundError(f"No se encuentra el archivo: {TRAIN_SCALED_FILE}")

    train_returns = pd.read_csv(TRAIN_RETURNS_FILE, index_col=0, parse_dates=True)
    train_scaled = pd.read_csv(TRAIN_SCALED_FILE, index_col=0, parse_dates=True)

    return train_returns, train_scaled


def load_vae_model(device: torch.device) -> tuple[VariationalAutoencoder, dict]:
    """
    Carga el modelo VAE entrenado.
    """
    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            f"No se encuentra el modelo {MODEL_FILE}. "
            "Ejecuta primero src\\models\\vae.py"
        )

    checkpoint = torch.load(MODEL_FILE, map_location=device)

    model = VariationalAutoencoder(
        input_dim=checkpoint["input_dim"],
        hidden_dim=checkpoint["hidden_dim"],
        latent_dim=checkpoint["latent_dim"],
    ).to(device)

    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    return model, checkpoint


def generate_synthetic_scaled_returns(
    model: VariationalAutoencoder,
    latent_dim: int,
    n_scenarios: int,
    columns: list[str],
    device: torch.device,
) -> pd.DataFrame:
    """
    Genera escenarios sintéticos escalados muestreando desde una normal estándar
    en el espacio latente del VAE.
    """
    with torch.no_grad():
        z = torch.randn(n_scenarios, latent_dim).to(device)
        synthetic_scaled = model.decode(z).cpu().numpy()

    synthetic_scaled_df = pd.DataFrame(
        synthetic_scaled,
        columns=columns,
    )

    return synthetic_scaled_df


def inverse_transform_returns(
    synthetic_scaled: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Deshace la normalización Min-Max para volver a la escala original de retornos.
    """
    if not SCALER_FILE.exists():
        raise FileNotFoundError(f"No se encuentra el escalador: {SCALER_FILE}")

    scaler = joblib.load(SCALER_FILE)

    synthetic_returns_array = scaler.inverse_transform(synthetic_scaled.values)

    synthetic_returns = pd.DataFrame(
        synthetic_returns_array,
        columns=columns,
    )

    return synthetic_returns


def compute_summary(
    train_returns: pd.DataFrame,
    synthetic_returns: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compara estadísticos básicos entre retornos reales de train y retornos sintéticos.
    """
    rows = []

    for ticker in train_returns.columns:
        rows.append(
            {
                "ticker": ticker,
                "real_mean": train_returns[ticker].mean(),
                "synthetic_mean": synthetic_returns[ticker].mean(),
                "real_std": train_returns[ticker].std(),
                "synthetic_std": synthetic_returns[ticker].std(),
                "real_min": train_returns[ticker].min(),
                "synthetic_min": synthetic_returns[ticker].min(),
                "real_max": train_returns[ticker].max(),
                "synthetic_max": synthetic_returns[ticker].max(),
            }
        )

    summary = pd.DataFrame(rows)

    summary["mean_abs_diff"] = (summary["real_mean"] - summary["synthetic_mean"]).abs()
    summary["std_abs_diff"] = (summary["real_std"] - summary["synthetic_std"]).abs()

    return summary


def run_vae_scenario_generation() -> None:
    """
    Genera escenarios sintéticos de retornos a partir del decoder del VAE.
    """
    set_seed()

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_returns, train_scaled = load_training_data()
    model, checkpoint = load_vae_model(device)

    synthetic_scaled = generate_synthetic_scaled_returns(
        model=model,
        latent_dim=checkpoint["latent_dim"],
        n_scenarios=N_SCENARIOS,
        columns=train_scaled.columns.tolist(),
        device=device,
    )

    synthetic_returns = inverse_transform_returns(
        synthetic_scaled=synthetic_scaled,
        columns=train_returns.columns.tolist(),
    )

    summary = compute_summary(
        train_returns=train_returns,
        synthetic_returns=synthetic_returns,
    )

    synthetic_scaled.to_csv(SYNTHETIC_SCALED_FILE, index=False)
    synthetic_returns.to_csv(SYNTHETIC_RETURNS_FILE, index=False)
    summary.to_csv(SYNTHETIC_SUMMARY_FILE, index=False)

    print("Generación de escenarios sintéticos con VAE completada.")
    print(f"Número de escenarios generados: {N_SCENARIOS}")
    print(f"Escenarios escalados guardados en: {SYNTHETIC_SCALED_FILE}")
    print(f"Escenarios en escala original guardados en: {SYNTHETIC_RETURNS_FILE}")
    print(f"Resumen estadístico guardado en: {SYNTHETIC_SUMMARY_FILE}")
    print()
    print("Resumen de diferencias medias:")
    print(f"Diferencia media absoluta de medias: {summary['mean_abs_diff'].mean():.8f}")
    print(f"Diferencia media absoluta de volatilidades: {summary['std_abs_diff'].mean():.8f}")
    print()
    print("Activos con mayor diferencia de volatilidad:")
    print(summary.sort_values("std_abs_diff", ascending=False).head(10))


if __name__ == "__main__":
    run_vae_scenario_generation()