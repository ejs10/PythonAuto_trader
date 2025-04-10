# strategy/strategy_rsi.py

import pandas as pd

from data.data_loader import get_price_data
#from strategy.strategy_rsi import rsi_strategy
from trade.trader import PaperTrader


def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def rsi_strategy(df: pd.DataFrame, period: int = 14, overbought: int = 70, oversold: int = 30) -> str:
    rsi_series = calculate_rsi(df['Close'], period)
    current_rsi = rsi_series.iloc[-1]

    if current_rsi < oversold:
        return "BUY"
    elif current_rsi > overbought:
        return "SELL"
    else:
        return "HOLD"


def backtest_rsi(ticker="AAPL", period="6mo"):
    df = get_price_data(ticker, period)
    trader = PaperTrader()
    for i in range(30, len(df)):
        sample = df.iloc[:i+1]
        signal = rsi_strategy(sample)
        price = df['Close'].iloc[i]
        if signal == "BUY":
            trader.buy(ticker, price, 1)
        elif signal == "SELL":
            trader.sell(ticker, price, 1)
    trader.status()