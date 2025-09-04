from __future__ import annotations
import datetime as dt
from typing import List
import pandas as pd
import yfinance as yf

DEFAULT_YEARS = 5

def parse_tickers(raw: str, max_n: int = 5) -> List[str]:
    tickers = [t.strip().upper() for t in raw.replace(";", ",").split(",") if t.strip()]
    return tickers[:max_n]

def download_prices(tickers: List[str], start: dt.date, end: dt.date) -> pd.DataFrame:
    if not tickers:
        return pd.DataFrame()
    df = yf.download(tickers, start=start, end=end, progress=False, auto_adjust=False)['Adj Close']
    if isinstance(df, pd.Series):
        df = df.to_frame(name=tickers[0])
    df = df.ffill().dropna(how='all')
    return df
