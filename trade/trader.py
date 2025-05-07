# trade/trader.py

from config.settings import Config

class PaperTrader:
    def __init__(self, initial_cash: float = 10_000_000):
        self.cash = initial_cash
        self.positions = {}  # 종목: 수량
        self.trade_log = []  # 매매 내역 기록

    def buy(self, ticker: str, price: float, quantity: int):
        total_cost = price * quantity

        if self.cash >= total_cost:
            self.cash -= total_cost
            self.positions[ticker] = self.positions.get(ticker, 0) + quantity
            self.trade_log.append((ticker, "BUY", price, quantity))
            print(f"✅ 매수: {ticker} {quantity}주 @ {price:.2f} | 잔고: {self.cash:,.0f}원")
        else:
            print("❌ 매수 실패: 잔고 부족")

    def sell(self, ticker: str, price: float, quantity: int):
        holding_qty = self.positions.get(ticker, 0)

        if holding_qty >= quantity:
            self.positions[ticker] -= quantity
            self.cash += price * quantity
            self.trade_log.append((ticker, "SELL", price, quantity))
            print(f"✅ 매도: {ticker} {quantity}주 @ {price:.2f} | 잔고: {self.cash:,.0f}원")
        else:
            print("❌ 매도 실패: 보유 수량 부족")

    def status(self):
        print("\n📊 현재 상태")
        print(f"💰 잔고: {self.cash:,.0f}원")
        print("📦 보유 종목:")
        for ticker, qty in self.positions.items():
            if qty > 0:
                print(f"   - {ticker}: {qty}주")
        print("📝 최근 거래:")
        for log in self.trade_log[-5:]:
            print(f"   {log[1]} {log[0]} {log[3]}주 @ {log[2]:.2f}")
