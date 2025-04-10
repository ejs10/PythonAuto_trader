#from .server import *
# auto_trader/app/__init__.py

from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    # 라우트 등록
    from app.routes.backtest_route import backtest_bp
    app.register_blueprint(backtest_bp)

    return app