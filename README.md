# Portfolio Risk & Return Dashboard  

An interactive **Streamlit web app** that calculates and visualizes **portfolio risk and return metrics** using live market data. Designed to simulate portfolio allocations, assess risk/return trade-offs, and present results in a clear dashboard format.  

---

## Features  
- **Real-time data** pulled from Yahoo Finance (`yfinance`)  
- **Core portfolio metrics**: daily returns, annualized volatility, Sharpe ratio, maximum drawdown  
- **Portfolio simulation**: adjust weights for up to **5 assets** and compare diversification outcomes  
- **Visualizations** with Plotly:  
  - Cumulative return curve  
  - Allocation pie chart  
  - Correlation heatmap  
  - Historical price trends  

---

## Installation  

Clone the repository:  
```bash
git clone https://github.com/taranrs/portfolio-risk-return-dashboard.git
cd Portfolio-Risk-Return-Dashboard
pip install -r requirements.txt
streamlit run app.py
