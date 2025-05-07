# streamlit_app.py

import streamlit as st
import pandas as pd
from backtest.optimizer import plot_equity_curve
from data.data_loader import get_price_data
from strategy.strategy_ma import moving_average_strategy
from strategy.strategy_rsi import rsi_strategy
from config.settings import Config
from trade.trader import PaperTrader

# --- 페이지 설정 ---
st.set_page_config(page_title="📊 전략 백테스트 대시보드", layout="centered")
st.title("📈 주식 자동매매 전략 대시보드")

# --- 사이드바 설정 ---
st.sidebar.header("⚙️ 설정")
ticker = st.sidebar.selectbox("📌 종목 선택", ["AAPL", "TSLA", "GOOG", "MSFT"])
period = st.sidebar.selectbox("⏳ 데이터 기간", ["3mo", "6mo", "1y"])
strategy_type = st.sidebar.selectbox("🧠 전략 선택", ["이동평균 (MA)", "RSI"])

# MA 전략 설정
if strategy_type == "이동평균 (MA)":
    short_range = st.sidebar.slider("단기 이동평균", 5, 20, 5)
    long_range = st.sidebar.slider("장기 이동평균", 25, 60, 30)
    Config.MA_SHORT = short_range
    Config.MA_LONG = long_range

elif strategy_type == "RSI":
    rsi_period = st.sidebar.slider("RSI 기간", 5, 30, 14)
    rsi_overbought = st.sidebar.slider("과매수 기준", 60, 90, 70)
    rsi_oversold = st.sidebar.slider("과매도 기준", 10, 40, 30)

# 백테스트 실행
if st.sidebar.button("🚀 백테스트 실행"):
    df = get_price_data(ticker, period=period)
    st.success("✅ 데이터 로딩 완료")
    st.success(f"📥 데이터 로딩 완료: {ticker} ({period})")

    trader = PaperTrader()
    equity_curve = []

    for i in range(30, len(df)):
        window_df = df.iloc[:i + 1]

        #전략 시그널 계산
        if strategy_type == "이동평균 (MA)":
            signal = moving_average_strategy(window_df)
            # signal = moving_average_strategy(window_df, short_range, long_range)
        elif strategy_type == "RSI":
            signal = rsi_strategy(window_df, period=rsi_period, overbought=rsi_overbought, oversold=rsi_oversold)
        else:
            signal = "HOLD"

        price = df["Close"].iloc[i]

        if signal == "BUY":
            trader.buy(ticker, price, 1)
        elif signal == "SELL":
            trader.sell(ticker, price, 1)

        # 자산기록 (현금 + 주식)
        total_value = trader.cash + trader.position * price if ticker in trader.positions else trader.cash
        equity_curve.append(total_value)

    #결과시각화
    trader.status()
    st.subheader("📈 누적 수익률 그래프")
    st.line_chart(equity_curve)

    # 💰 수익률 정보
    st.metric("총 수익", f"${trader.total_profit:.2f}")

    #수정
    position_count = trader.positions.get(ticker, 0)
    st.caption(f"📌 최종 잔고: ${trader.cash:.2f} / 보유 수량: {position_count}")

    # Equity Curve Plot
    if strategy_type == "이동평균 (MA)":
        try:
            plot_equity_curve(df, short_range, long_range)
        except Exception as e:
            st.error(f"차트 생성 오류 : {e}")
    else:
        st.warning("⚠️ RSI 전략은 아직 수익률 시각화 미지원 (옵션)")


