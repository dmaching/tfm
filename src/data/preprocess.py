from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "sp500_prices_adj_close.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

RETURNS_FILE = PROCESSED_DIR / "returns.csv"
TRAIN_FILE = PROCESSED_DIR / "returns_train.csv"
TEST_FILE = PROCESSED_DIR / "returns_test.csv"
TRAIN_SCALED_FILE = PROCESSED_DIR / "returns_train_scaled.csv"
TEST_SCALED_FILE = PROCESSED_DIR / "returns_test_scaled.csv"
SCALER_FILE = PROCESSED_DIR / "minmax_scaler.pkl"

TRAIN_RATIO = 0.8
MAX_MISSING_RATIO = 0.05


def load_prices() -> pd.DataFrame:
    """
    Carga el fichero de precios ajustados descargado previamente.
    """
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"No se encuentra el archivo {RAW_FILE}. "
            "Ejecuta primero src\\data\\download_data.py"
        )

    prices = pd.read_csv(RAW_FILE, index_col=0, parse_dates=True)
    prices = prices.sort_index()

    return prices


def filter_assets_by_missing_values(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina activos con un porcentaje de valores ausentes superior al umbral definido.
    """
    missing_ratio = prices.isna().mean()
    selected_columns = missing_ratio[missing_ratio <= MAX_MISSING_RATIO].index.tolist()

    filtered_prices = prices[selected_columns].copy()

    print("Filtrado de activos por valores ausentes:")
    print(f"Activos iniciales: {prices.shape[1]}")
    print(f"Activos conservados: {filtered_prices.shape[1]}")
    print(f"Activos eliminados: {prices.shape[1] - filtered_prices.shape[1]}")

    return filtered_prices


def compute_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula retornos logarítmicos diarios a partir de precios ajustados.
    """
    prices = prices.ffill().dropna(axis=1)
    returns = np.log(prices / prices.shift(1))
    returns = returns.dropna()

    return returns


def temporal_train_test_split(returns: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Divide los retornos en train y test respetando el orden temporal.
    """
    split_index = int(len(returns) * TRAIN_RATIO)

    train = returns.iloc[:split_index].copy()
    test = returns.iloc[split_index:].copy()

    return train, test


def scale_returns(
    train: pd.DataFrame,
    test: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, MinMaxScaler]:
    """
    Ajusta un escalador Min-Max con train y transforma train y test.
    """
    scaler = MinMaxScaler(feature_range=(-1, 1))

    train_scaled_array = scaler.fit_transform(train)
    test_scaled_array = scaler.transform(test)

    train_scaled = pd.DataFrame(
        train_scaled_array,
        index=train.index,
        columns=train.columns,
    )

    test_scaled = pd.DataFrame(
        test_scaled_array,
        index=test.index,
        columns=test.columns,
    )

    return train_scaled, test_scaled, scaler


def preprocess_data() -> None:
    """
    Ejecuta el pipeline completo de preprocesamiento.
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    prices = load_prices()
    prices = filter_assets_by_missing_values(prices)

    returns = compute_log_returns(prices)
    train, test = temporal_train_test_split(returns)
    train_scaled, test_scaled, scaler = scale_returns(train, test)

    returns.to_csv(RETURNS_FILE)
    train.to_csv(TRAIN_FILE)
    test.to_csv(TEST_FILE)
    train_scaled.to_csv(TRAIN_SCALED_FILE)
    test_scaled.to_csv(TEST_SCALED_FILE)
    joblib.dump(scaler, SCALER_FILE)

    print("Preprocesamiento completado.")
    print(f"Retornos completos: {returns.shape}")
    print(f"Train: {train.shape}")
    print(f"Test: {test.shape}")
    print(f"Archivos guardados en: {PROCESSED_DIR}")


if __name__ == "__main__":
    preprocess_data()