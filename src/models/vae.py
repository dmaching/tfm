from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

TRAIN_SCALED_FILE = PROJECT_ROOT / "data" / "processed" / "returns_train_scaled.csv"
TEST_SCALED_FILE = PROJECT_ROOT / "data" / "processed" / "returns_test_scaled.csv"

MODELS_DIR = PROJECT_ROOT / "models"
FIGURES_DIR = PROJECT_ROOT / "figures"
GENERATED_DIR = PROJECT_ROOT / "data" / "generated"

MODEL_OUTPUT_FILE = MODELS_DIR / "vae.pt"
LOSS_FIGURE_FILE = FIGURES_DIR / "vae_loss.png"
RECONSTRUCTED_TRAIN_FILE = GENERATED_DIR / "vae_reconstructed_train_scaled.csv"
RECONSTRUCTED_TEST_FILE = GENERATED_DIR / "vae_reconstructed_test_scaled.csv"
RECONSTRUCTION_METRICS_FILE = GENERATED_DIR / "vae_reconstruction_metrics.csv"

RANDOM_SEED = 42
BATCH_SIZE = 64
EPOCHS = 150
LEARNING_RATE = 1e-3

HIDDEN_DIM = 64
LATENT_DIM = 8
BETA = 0.001


def set_seed(seed: int = RANDOM_SEED) -> None:
    """
    Fija semillas para facilitar la reproducibilidad del entrenamiento.
    """
    np.random.seed(seed)
    torch.manual_seed(seed)


class VariationalAutoencoder(nn.Module):
    """
    Autoencoder Variacional básico para vectores diarios de retornos escalados.
    """

    def __init__(self, input_dim: int, hidden_dim: int, latent_dim: int):
        super().__init__()

        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
        )

        self.fc_mu = nn.Linear(hidden_dim, latent_dim)
        self.fc_logvar = nn.Linear(hidden_dim, latent_dim)

        self.decoder_input = nn.Linear(latent_dim, hidden_dim)

        self.decoder = nn.Sequential(
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim),
            nn.Tanh(),
        )

    def encode(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        hidden = self.encoder(x)
        mu = self.fc_mu(hidden)
        logvar = self.fc_logvar(hidden)

        return mu, logvar

    def reparameterize(self, mu: torch.Tensor, logvar: torch.Tensor) -> torch.Tensor:
        std = torch.exp(0.5 * logvar)
        epsilon = torch.randn_like(std)

        return mu + epsilon * std

    def decode(self, z: torch.Tensor) -> torch.Tensor:
        hidden = self.decoder_input(z)
        reconstruction = self.decoder(hidden)

        return reconstruction

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        reconstruction = self.decode(z)

        return reconstruction, mu, logvar


def load_scaled_returns() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Carga los retornos escalados de train y test.
    """
    if not TRAIN_SCALED_FILE.exists():
        raise FileNotFoundError(
            f"No se encuentra el archivo {TRAIN_SCALED_FILE}. "
            "Ejecuta primero src\\data\\preprocess.py"
        )

    if not TEST_SCALED_FILE.exists():
        raise FileNotFoundError(
            f"No se encuentra el archivo {TEST_SCALED_FILE}. "
            "Ejecuta primero src\\data\\preprocess.py"
        )

    train_scaled = pd.read_csv(TRAIN_SCALED_FILE, index_col=0, parse_dates=True)
    test_scaled = pd.read_csv(TEST_SCALED_FILE, index_col=0, parse_dates=True)

    return train_scaled, test_scaled


def create_dataloader(train_scaled: pd.DataFrame) -> DataLoader:
    """
    Crea un DataLoader de PyTorch a partir del conjunto de entrenamiento.
    """
    train_tensor = torch.tensor(train_scaled.values, dtype=torch.float32)
    dataset = TensorDataset(train_tensor)

    dataloader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
    )

    return dataloader


def vae_loss_function(
    reconstruction: torch.Tensor,
    original: torch.Tensor,
    mu: torch.Tensor,
    logvar: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Calcula la pérdida del VAE.

    La pérdida combina:
    - error de reconstrucción mediante MSE;
    - regularización KL del espacio latente.
    """
    reconstruction_loss = nn.functional.mse_loss(
        reconstruction,
        original,
        reduction="mean",
    )

    kl_loss = -0.5 * torch.mean(
        torch.sum(1 + logvar - mu.pow(2) - logvar.exp(), dim=1)
    )

    total_loss = reconstruction_loss + BETA * kl_loss

    return total_loss, reconstruction_loss, kl_loss


def train_vae(
    model: VariationalAutoencoder,
    dataloader: DataLoader,
    device: torch.device,
) -> pd.DataFrame:
    """
    Entrena el VAE y devuelve el historial de pérdidas.
    """
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    history = []

    model.train()

    for epoch in range(1, EPOCHS + 1):
        epoch_total_loss = 0.0
        epoch_reconstruction_loss = 0.0
        epoch_kl_loss = 0.0

        for batch in dataloader:
            x = batch[0].to(device)

            optimizer.zero_grad()

            reconstruction, mu, logvar = model(x)
            total_loss, reconstruction_loss, kl_loss = vae_loss_function(
                reconstruction,
                x,
                mu,
                logvar,
            )

            total_loss.backward()
            optimizer.step()

            epoch_total_loss += total_loss.item()
            epoch_reconstruction_loss += reconstruction_loss.item()
            epoch_kl_loss += kl_loss.item()

        n_batches = len(dataloader)

        avg_total_loss = epoch_total_loss / n_batches
        avg_reconstruction_loss = epoch_reconstruction_loss / n_batches
        avg_kl_loss = epoch_kl_loss / n_batches

        history.append(
            {
                "epoch": epoch,
                "total_loss": avg_total_loss,
                "reconstruction_loss": avg_reconstruction_loss,
                "kl_loss": avg_kl_loss,
            }
        )

        if epoch == 1 or epoch % 10 == 0:
            print(
                f"Epoch {epoch:03d}/{EPOCHS} | "
                f"loss={avg_total_loss:.6f} | "
                f"reconstruction={avg_reconstruction_loss:.6f} | "
                f"kl={avg_kl_loss:.6f}"
            )

    return pd.DataFrame(history)


def reconstruct_returns(
    model: VariationalAutoencoder,
    data: pd.DataFrame,
    device: torch.device,
) -> pd.DataFrame:
    """
    Reconstruye un conjunto de retornos escalados usando el VAE entrenado.
    """
    model.eval()

    data_tensor = torch.tensor(data.values, dtype=torch.float32).to(device)

    with torch.no_grad():
        reconstruction, _, _ = model(data_tensor)

    reconstructed = pd.DataFrame(
        reconstruction.cpu().numpy(),
        index=data.index,
        columns=data.columns,
    )

    return reconstructed


def compute_reconstruction_metrics(
    original_train: pd.DataFrame,
    reconstructed_train: pd.DataFrame,
    original_test: pd.DataFrame,
    reconstructed_test: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula métricas simples de error de reconstrucción.
    """
    train_error = original_train.values - reconstructed_train.values
    test_error = original_test.values - reconstructed_test.values

    metrics = {
        "train_mse": np.mean(train_error**2),
        "train_mae": np.mean(np.abs(train_error)),
        "test_mse": np.mean(test_error**2),
        "test_mae": np.mean(np.abs(test_error)),
    }

    return pd.DataFrame([metrics])


def save_loss_plot(history: pd.DataFrame) -> None:
    """
    Guarda la curva de pérdida del entrenamiento.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(history["epoch"], history["total_loss"], label="Total loss")
    plt.plot(history["epoch"], history["reconstruction_loss"], label="Reconstruction loss")
    plt.plot(history["epoch"], history["kl_loss"], label="KL loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("VAE training loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(LOSS_FIGURE_FILE, dpi=300)
    plt.close()


def run_vae_training() -> None:
    """
    Ejecuta el entrenamiento completo del VAE.
    """
    set_seed()

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    train_scaled, test_scaled = load_scaled_returns()

    input_dim = train_scaled.shape[1]

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print("Entrenamiento de VAE iniciado.")
    print(f"Dispositivo: {device}")
    print(f"Input dim: {input_dim}")
    print(f"Hidden dim: {HIDDEN_DIM}")
    print(f"Latent dim: {LATENT_DIM}")
    print(f"Epochs: {EPOCHS}")
    print(f"Beta KL: {BETA}")
    print()

    dataloader = create_dataloader(train_scaled)

    model = VariationalAutoencoder(
        input_dim=input_dim,
        hidden_dim=HIDDEN_DIM,
        latent_dim=LATENT_DIM,
    ).to(device)

    history = train_vae(model, dataloader, device)

    reconstructed_train = reconstruct_returns(model, train_scaled, device)
    reconstructed_test = reconstruct_returns(model, test_scaled, device)

    reconstruction_metrics = compute_reconstruction_metrics(
        original_train=train_scaled,
        reconstructed_train=reconstructed_train,
        original_test=test_scaled,
        reconstructed_test=reconstructed_test,
    )

    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "input_dim": input_dim,
            "hidden_dim": HIDDEN_DIM,
            "latent_dim": LATENT_DIM,
            "beta": BETA,
        },
        MODEL_OUTPUT_FILE,
    )

    history.to_csv(GENERATED_DIR / "vae_loss_history.csv", index=False)
    reconstructed_train.to_csv(RECONSTRUCTED_TRAIN_FILE)
    reconstructed_test.to_csv(RECONSTRUCTED_TEST_FILE)
    reconstruction_metrics.to_csv(RECONSTRUCTION_METRICS_FILE, index=False)

    save_loss_plot(history)

    print()
    print("Entrenamiento de VAE completado.")
    print(f"Modelo guardado en: {MODEL_OUTPUT_FILE}")
    print(f"Curva de pérdida guardada en: {LOSS_FIGURE_FILE}")
    print(f"Reconstrucción train guardada en: {RECONSTRUCTED_TRAIN_FILE}")
    print(f"Reconstrucción test guardada en: {RECONSTRUCTED_TEST_FILE}")
    print(f"Métricas de reconstrucción guardadas en: {RECONSTRUCTION_METRICS_FILE}")
    print()
    print("Métricas de reconstrucción:")
    print(reconstruction_metrics.T)


if __name__ == "__main__":
    run_vae_training()