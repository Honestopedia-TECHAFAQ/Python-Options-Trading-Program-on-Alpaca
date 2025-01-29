import alpaca_trade_api as tradeapi
import pandas as pd
import time
import datetime
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

symbols = ["AAPL", "TSLA", "SPY"]
capital = 30000
max_risk_per_trade = 0.02 * capital

def get_historical_data(symbol, timeframe="1D", limit=100):
    barset = api.get_barset(symbol, timeframe, limit=limit)
    df = pd.DataFrame(barset[symbol].df)
    return df

def calculate_signals(df):
    df['rsi'] = RSIIndicator(df['close']).rsi()
    bb = BollingerBands(df['close'])
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()
    df['signal'] = "HOLD"
    
    if df['rsi'].iloc[-1] < 30:
        df['signal'].iloc[-1] = "BUY CALL"
    elif df['rsi'].iloc[-1] > 70:
        df['signal'].iloc[-1] = "BUY PUT"
    elif df['close'].iloc[-1] > df['bb_upper'].iloc[-1]:
        df['signal'].iloc[-1] = "BUY PUT"
    elif df['close'].iloc[-1] < df['bb_lower'].iloc[-1]:
        df['signal'].iloc[-1] = "BUY CALL"
    return df

def execute_trade(symbol, signal):
    if signal == "BUY CALL":
        api.submit_order(
            symbol=symbol,
            qty=1,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
    elif signal == "BUY PUT":
        api.submit_order(
            symbol=symbol,
            qty=1,
            side='sell',
            type='market',
            time_in_force='gtc'
        )

def log_trade(trade_data):
    df = pd.DataFrame([trade_data])
    df.to_csv("trade_log.csv", mode='a', header=False, index=False)

while True:
    for symbol in symbols:
        df = get_historical_data(symbol)
        df = calculate_signals(df)
        signal = df['signal'].iloc[-1]
        execute_trade(symbol, signal)
        log_trade({
            "timestamp": datetime.datetime.now(),
            "symbol": symbol,
            "signal": signal,
            "price": df['close'].iloc[-1]
        })
    time.sleep(3600)
