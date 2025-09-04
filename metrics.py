from __future__ import annotations
import numpy as np
import pandas as pd

TRADING_DAYS = 252

def daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna(how='all')

def normalize_weights(w, cols: list[str]) -> pd.Series:
    s = pd.Series(w, index=cols, dtype=float)
    total = s.clip(lower=0).sum()
    if total == 0:
        s[:] = 1.0 / max(1, len(cols))
    else:
        s = s / total
    return s

def portfolio_returns(ret: pd.DataFrame, weights: pd.Series) -> pd.Series:
    aligned = ret[weights.index]
    return (aligned * weights).sum(axis=1)

def annualized_volatility(ret_port: pd.Series) -> float:
    return float(ret_port.std() * np.sqrt(TRADING_DAYS))

def annualized_return(ret_port: pd.Series) -> float:
    return float(ret_port.mean() * TRADING_DAYS)

def sharpe_ratio(ret_port: pd.Series, rf_annual: float = 0.0) -> float:
    vol = annualized_volatility(ret_port)
    if vol == 0:
        return float('nan')
    ex_ret = annualized_return(ret_port) - rf_annual
    return float(ex_ret / vol)

def max_drawdown(cumulative: pd.Series) -> float:
    roll_max = cumulative.cummax()
    drawdown = cumulative / roll_max - 1.0
    return float(drawdown.min())

def cumulative_curve(ret: pd.Series, start_value: float = 1.0) -> pd.Series:
    return (1.0 + ret).cumprod() * start_value
