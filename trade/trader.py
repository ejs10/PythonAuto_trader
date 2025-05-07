# trade/trader.py

from config.settings import Config

class PaperTrader:
    def __init__(self, initial_cash: float = 10_000_000):
        self.initial_cash = initial_cash # 초기 금액 저장
        self.cash = initial_cash
        self.positions = {}  # 종목: 수량
        self.trade_log = []  # 매매 내역 기록
        self.total_profit = 0.0

    @property
    def position(self):
        """
        호환성을 위해 추가: position 속성 접근 시 첫 번째 종목의 수량 반환
        """
        if not self.positions:
            return 0
        return next(iter(self.positions.values()))

    def buy(self, ticker: str, price: float, quantity: int):
        total_cost = price * quantity

        if self.cash >= total_cost:
            self.cash -= total_cost
            self.positions[ticker] = self.positions.get(ticker, 0) + quantity
            self.trade_log.append((ticker, "BUY", price, quantity))
            print(f"✅ 매수: {ticker} {quantity}주 @ {price:.2f} | 잔고: {self.cash:,.0f}원")

            #총 수익 업데이트 (현재 자산 - 초기 자산)
            self.update_total_profit()

        else:
            print("❌ 매수 실패: 잔고 부족")

    def sell(self, ticker: str, price: float, quantity: int):
        holding_qty = self.positions.get(ticker, 0)

        if holding_qty >= quantity:
            self.positions[ticker] -= quantity
            self.cash += price * quantity
            self.trade_log.append((ticker, "SELL", price, quantity))
            print(f"✅ 매도: {ticker} {quantity}주 @ {price:.2f} | 잔고: {self.cash:,.0f}원")

            # 총 수익 업데이트 (현재 자산 - 초기 자산)
            self.update_total_profit()
        else:
            print("❌ 매도 실패: 보유 수량 부족")

    def update_total_profit(self):
        """총 수익 업데이트 (단순히 현금 기준으로 계산)"""
        self.total_profit = self.cash - self.initial_cash

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
