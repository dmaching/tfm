from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

TRAIN_SCALED_FILE = PROJECT_ROOT / "data" / "processed" / "returns_train_scaled.csv"
TEST_SCALED_FILE = PROJECT_ROOT / "data" / "processed" / "returns_test_scaled.csv"

RECONSTRUCTED_TRAIN_FILE = PROJECT_ROOT / "data" / "generated" / "vae_reconstructed_train_scaled.csv"
RECONSTRUCTED_TEST_FILE = PROJECT_ROOT / "data" / "generated" / "vae_reconstructed_test_scaled.csv"

GENERATED_DIR = PROJECT_ROOT / "data" / "generated"
FIGURES_DIR = PROJECT_ROOT / "figures"

ERROR_BY_ASSET_FILE = GENERATED_DIR / "vae_reconstruction_error_by_asset.csv"

DISTRIBUTION_FIGURE_FILE = FIGURES_DIR / "vae_real_vs_reconstructed_distribution.png"
ERROR_BY_ASSET_FIGURE_FILE = FIGURES_DIR / "vae_reconstruction_error_by_asset.png"
SCATTER_FIGURE_FILE = FIGURES_DIR / "vae_real_vs_reconstructed_scatter.png"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Carga los retornos escalados reales y reconstruidos.
    """
    required_files = [
        TRAIN_SCALED_FILE,
        TEST_SCALED_FILE,
        RECONSTRUCTED_TRAIN_FILE,
        RECONSTRUCTED_TEST_FILE,
    ]

    for file_path in required_files:
        if not file_path.exists():
            raise FileNotFoundError(f"No se encuentra el archivo: {file_path}")

    train_scaled = pd.read_csv(TRAIN_SCALED_FILE, index_col=0, parse_dates=True)
    test_scaled = pd.read_csv(TEST_SCALED_FILE, index_col=0, parse_dates=True)

    reconstructed_train = pd.read_csv(RECONSTRUCTED_TRAIN_FILE, index_col=0, parse_dates=True)
    reconstructed_test = pd.read_csv(RECONSTRUCTED_TEST_FILE, index_col=0, parse_dates=True)

    return train_scaled, test_scaled, reconstructed_train, reconstructed_test


def compute_error_by_asset(
    original: pd.DataFrame,
    reconstructed: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula MSE y MAE de reconstrucción por activo.
    """
    error = original - reconstructed

    error_by_asset = pd.DataFrame(
        {
            "ticker": original.columns,
            "mse": np.mean(error.values**2, axis=0),
            "mae": np.mean(np.abs(error.values), axis=0),
        }
    )

    return error_by_asset.sort_values("mse", ascending=False)


def plot_real_vs_reconstructed_distribution(
    original_test: pd.DataFrame,
    reconstructed_test: pd.DataFrame,
) -> None:
    """
    Compara la distribución global de retornos reales y reconstruidos en test.
    """
    real_values = original_test.values.flatten()
    reconstructed_values = reconstructed_test.values.flatten()

    plt.figure(figsize=(8, 5))
    plt.hist(real_values, bins=80, alpha=0.5, density=True, label="Real test")
    plt.hist(reconstructed_values, bins=80, alpha=0.5, density=True, label="VAE reconstructed test")
    plt.xlabel("Scaled return")
    plt.ylabel("Density")
    plt.title("Real vs reconstructed scaled returns")
    plt.legend()
    plt.tight_layout()
    plt.savefig(DISTRIBUTION_FIGURE_FILE, dpi=300)
    plt.close()


def plot_error_by_asset(error_by_asset: pd.DataFrame) -> None:
    """
    Representa el error MSE de reconstrucción por activo.
    """
    plt.figure(figsize=(10, 5))
    plt.bar(error_by_asset["ticker"], error_by_asset["mse"])
    plt.xlabel("Ticker")
    plt.ylabel("MSE")
    plt.title("VAE reconstruction error by asset")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(ERROR_BY_ASSET_FIGURE_FILE, dpi=300)
    plt.close()


def plot_real_vs_reconstructed_scatter(
    original_test: pd.DataFrame,
    reconstructed_test: pd.DataFrame,
    sample_size: int = 5000,
) -> None:
    """
    Genera un gráfico de dispersión entre valores reales y reconstruidos.
    """
    real_values = original_test.values.flatten()
    reconstructed_values = reconstructed_test.values.flatten()

    if len(real_values) > sample_size:
        rng = np.random.default_rng(42)
        selected_indices = rng.choice(len(real_values), size=sample_size, replace=False)
        real_values = real_values[selected_indices]
        reconstructed_values = reconstructed_values[selected_indices]

    plt.figure(figsize=(6, 6))
    plt.scatter(real_values, reconstructed_values, alpha=0.25, s=8)
    plt.xlabel("Real scaled return")
    plt.ylabel("Reconstructed scaled return")
    plt.title("Real vs reconstructed values")
    plt.tight_layout()
    plt.savefig(SCATTER_FIGURE_FILE, dpi=300)
    plt.close()


def evaluate_vae() -> None:
    """
    Ejecuta la evaluación visual del VAE.
    """
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    train_scaled, test_scaled, reconstructed_train, reconstructed_test = load_data()

    train_error_by_asset = compute_error_by_asset(train_scaled, reconstructed_train)
    test_error_by_asset = compute_error_by_asset(test_scaled, reconstructed_test)

    error_by_asset = test_error_by_asset.copy()
    error_by_asset.to_csv(ERROR_BY_ASSET_FILE, index=False)

    plot_real_vs_reconstructed_distribution(test_scaled, reconstructed_test)
    plot_error_by_asset(error_by_asset)
    plot_real_vs_reconstructed_scatter(test_scaled, reconstructed_test)

    print("Evaluación visual del VAE completada.")
    print(f"Error por activo guardado en: {ERROR_BY_ASSET_FILE}")
    print(f"Figura de distribuciones guardada en: {DISTRIBUTION_FIGURE_FILE}")
    print(f"Figura de error por activo guardada en: {ERROR_BY_ASSET_FIGURE_FILE}")
    print(f"Figura de dispersión guardada en: {SCATTER_FIGURE_FILE}")
    print()
    print("Errores de reconstrucción más altos en test:")
    print(test_error_by_asset.head(10))
    print()
    print("Errores medios:")
    print(f"Train MSE medio por activo: {train_error_by_asset['mse'].mean():.6f}")
    print(f"Test MSE medio por activo: {test_error_by_asset['mse'].mean():.6f}")
    print(f"Train MAE medio por activo: {train_error_by_asset['mae'].mean():.6f}")
    print(f"Test MAE medio por activo: {test_error_by_asset['mae'].mean():.6f}")


if __name__ == "__main__":
    evaluate_vae()