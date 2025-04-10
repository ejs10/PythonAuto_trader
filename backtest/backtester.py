# backtest/backtester.py

import pandas as pd
from strategy.strategy_ma import moving_average_strategy
from trade.trader import PaperTrader

def run_backtest(df: pd.DataFrame, ticker: str, quantity: int = 1):
    trader = PaperTrader()
    buy_price = None
    daily_returns = []

    # 전체 데이터 순회하면서 전략 적용
    for i in range(30, len(df)):  # 30일 이후부터 충분한 이동평균 확보
        sample = df.iloc[:i+1]
        signal = moving_average_strategy(sample)
        current_price = df["Close"].iloc[i]

        if signal == "BUY":
            trader.buy(ticker, current_price, quantity)
            buy_price = current_price
        elif signal == "SELL":
            trader.sell(ticker, current_price, quantity)
            buy_price = None
        # else: HOLD → 아무것도 안함

        #누적 수익률 계산
        daily_returns.append(trader.total_profit)

    result = {
        "total_profit": trader.total_profit,
        "cash": trader.cash,
        "position": trader.position,
        "returns": daily_returns,  # 📈 Streamlit용 그래프 데이터
    }
    return result

    # 최종 결과 출력
    trader.status()
