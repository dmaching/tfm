from pathlib import Path

import pandas as pd
import yfinance as yf


TICKERS = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "META",
    "NVDA", "JPM", "V", "PG", "UNH",
    "HD", "MA", "DIS", "BAC", "XOM",
    "KO", "PEP", "CSCO", "PFE", "MRK",
    "WMT", "ADBE", "NFLX", "CRM", "INTC",
    "T", "VZ", "CMCSA", "NKE", "ORCL",
]

START_DATE = "2014-01-01"
END_DATE = "2024-12-31"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_FILE = RAW_DATA_DIR / "sp500_prices_adj_close.csv"


def download_prices() -> pd.DataFrame:
    """
    Descarga precios históricos ajustados de un subconjunto inicial de activos
    pertenecientes al S&P 500.

    Returns
    -------
    pd.DataFrame
        DataFrame con fechas como índice y tickers como columnas.
    """
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Descargando datos financieros desde Yahoo Finance...")
    print(f"Periodo: {START_DATE} a {END_DATE}")
    print(f"Número de activos: {len(TICKERS)}")

    data = yf.download(
        tickers=TICKERS,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=False,
        progress=True,
        group_by="column",
    )

    if data.empty:
        raise ValueError("No se han descargado datos. Revisa la conexión o los tickers.")

    if "Adj Close" not in data.columns:
        raise ValueError("No se encuentra la columna 'Adj Close' en los datos descargados.")

    prices = data["Adj Close"].copy()
    prices = prices.sort_index()

    prices.to_csv(OUTPUT_FILE)

    print(f"Datos guardados en: {OUTPUT_FILE}")
    print(f"Dimensiones del dataset: {prices.shape[0]} filas x {prices.shape[1]} activos")

    return prices


if __name__ == "__main__":
    download_prices()