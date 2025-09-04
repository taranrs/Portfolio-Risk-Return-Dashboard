import datetime as dt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data_utils import parse_tickers, download_prices, DEFAULT_YEARS
from metrics import (
    daily_returns,
    normalize_weights,
    portfolio_returns,
    annualized_volatility,
    annualized_return,
    sharpe_ratio,
    max_drawdown,
    cumulative_curve,
)

st.set_page_config(page_title="Portfolio Risk & Return", layout="wide")
st.title("Portfolio Risk & Return Dashboard")

# Sidebar inputs
with st.sidebar:
    st.header("Inputs")
    raw = st.text_input("Tickers (comma separated)", "AAPL, MSFT, NVDA")
    tickers = parse_tickers(raw)

    years = st.slider("History (years)", 1, 10, DEFAULT_YEARS)
    end = dt.date.today()
    start = end - dt.timedelta(days=365 * years)

    rf = st.number_input("Risk-free rate (annual)", min_value=0.0, max_value=0.2, value=0.02, step=0.005)

    st.caption("Weights are normalized to sum to 1. Use 0 to exclude an asset.")

    weights = []
    for t in tickers:
        w = st.slider(f"Weight: {t}", 0.0, 1.0, 1.0 / len(tickers) if tickers else 0.0, 0.01)
        weights.append(w)

# Stop if no tickers
if not tickers:
    st.info("Enter 1–5 tickers to begin.")
    st.stop()

# Download data
prices = download_prices(tickers, start, end)
if prices.empty:
    st.warning("No price data returned for the given tickers/range.")
    st.stop()

returns = daily_returns(prices)
weights_s = normalize_weights(weights, prices.columns.tolist())
ret_port = portfolio_returns(returns, weights_s)
curve = cumulative_curve(ret_port)

# Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Annualized Return", f"{annualized_return(ret_port)*100:,.2f}%")
with col2:
    st.metric("Annualized Volatility", f"{annualized_volatility(ret_port)*100:,.2f}%")
with col3:
    sr = sharpe_ratio(ret_port, rf)
    st.metric("Sharpe Ratio", f"{sr:,.2f}")
with col4:
    mdd = max_drawdown(curve)
    st.metric("Max Drawdown", f"{mdd*100:,.2f}%")

st.divider()

# Charts
left, right = st.columns([2, 1])
with left:
    fig_curve = go.Figure()
    fig_curve.add_trace(go.Scatter(x=curve.index, y=curve, mode="lines", name="Portfolio"))
    fig_curve.update_layout(title="Cumulative Return (Start = 1.0)", xaxis_title="Date", yaxis_title="Value")
    st.plotly_chart(fig_curve, use_container_width=True)

with right:
    alloc = pd.Series(weights_s.values, index=weights_s.index)
    fig_pie = px.pie(values=alloc.values, names=alloc.index, title="Allocation")
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

colA, colB = st.columns(2)
with colA:
    corr = returns.corr()
    fig_corr = px.imshow(corr, text_auto=True, title="Return Correlation (daily)")
    st.plotly_chart(fig_corr, use_container_width=True)

with colB:
    fig_prices = px.line(prices, title="Adjusted Close Prices")
    st.plotly_chart(fig_prices, use_container_width=True)

st.caption("Data from Yahoo Finance via yfinance. For educational use only – not investment advice.")
