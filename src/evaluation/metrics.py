import numpy as np
import pandas as pd


TRADING_DAYS = 252


def cumulative_return(returns: pd.Series) -> float:
    """
    Calcula el retorno acumulado de una serie de retornos diarios.
    """
    return float((1 + returns).prod() - 1)


def annualized_return(returns: pd.Series) -> float:
    """
    Calcula el retorno anualizado.
    """
    total_return = (1 + returns).prod()
    n_days = len(returns)

    if n_days == 0:
        return np.nan

    return float(total_return ** (TRADING_DAYS / n_days) - 1)


def annualized_volatility(returns: pd.Series) -> float:
    """
    Calcula la volatilidad anualizada.
    """
    return float(returns.std() * np.sqrt(TRADING_DAYS))


def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    """
    Calcula el ratio de Sharpe anualizado.

    Por simplicidad inicial, la tasa libre de riesgo se fija en 0.
    """
    excess_returns = returns - risk_free_rate / TRADING_DAYS
    volatility = annualized_volatility(excess_returns)

    if volatility == 0:
        return np.nan

    return float(annualized_return(excess_returns) / volatility)


def max_drawdown(returns: pd.Series) -> float:
    """
    Calcula el máximo drawdown de una serie de retornos.
    """
    wealth_index = (1 + returns).cumprod()
    previous_peaks = wealth_index.cummax()
    drawdowns = wealth_index / previous_peaks - 1

    return float(drawdowns.min())


def historical_var(returns: pd.Series, confidence_level: float = 0.95) -> float:
    """Calcula el VaR histórico como el cuantil inferior de los retornos."""
    return float(returns.quantile(1 - confidence_level))


def historical_cvar(returns: pd.Series, confidence_level: float = 0.95) -> float:
    """Calcula el CVaR histórico como la media de los retornos bajo el VaR."""
    var = historical_var(returns, confidence_level)
    tail_returns = returns[returns <= var]
    return float(tail_returns.mean()) if not tail_returns.empty else np.nan


def compute_metrics(returns: pd.Series) -> pd.DataFrame:
    """
    Calcula las métricas principales de una estrategia de cartera.
    """
    metrics = {
        "cumulative_return": cumulative_return(returns),
        "annualized_return": annualized_return(returns),
        "annualized_volatility": annualized_volatility(returns),
        "sharpe_ratio": sharpe_ratio(returns),
        "max_drawdown": max_drawdown(returns),
        "cvar_95": historical_cvar(returns, 0.95),
    }

    return pd.DataFrame([metrics])
