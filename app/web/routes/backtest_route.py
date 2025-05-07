# auto_trader/app/routes/backtest_route.py

from flask import Blueprint, request, jsonify, render_template
from data.data_loader import get_price_data
from strategy.strategy_ma import moving_average_strategy
from strategy.strategy_rsi import rsi_strategy
from backtest.backtester import run_backtest

backtest_bp = Blueprint('backtest', __name__)

@backtest_bp.route('/')
def index():
    return render_template("index.html")

@backtest_bp.route('/run_backtest', methods=["POST"])
def run_backtest_api():
    data = request.json
    ticker = data.get("ticker")
    period = data.get("period")
    strategy = data.get("strategy")
    params = data.get("params", {})

    df = get_price_data(ticker, period)

    if strategy == "ma":
        short = int(params.get("short", 5))
        long = int(params.get("long", 20))
        def strategy_fn(df): return moving_average_strategy(df, short, long)
    elif strategy == "rsi":
        low = int(params.get("low", 30))
        high = int(params.get("high", 70))
        def strategy_fn(df): return rsi_strategy(df, low, high)
    else:
        return jsonify({"error": "Unknown strategy"}), 400

    result = run_backtest(df, strategy_fn, ticker)
    return jsonify(result)
