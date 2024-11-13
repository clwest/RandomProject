import ccxt, yfinance
import pandas_ta as ta
import pandas as pd
# import config
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

exchange = ccxt.binance()

bars = exchange.fetch_ohlcv('ETH/USDT', timeframe='5m', limit=500)
df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

adx = df.ta.adx()
macd = df.ta.macd(fast=14, slow=28)
rsi = df.ta.rsi()

df = pd.concat([df, adx, macd, rsi], axis=1)

print(df)


last_row = df.iloc[-1]
print(last_row)

WEBHOOK_URL = "http://127.0.0.1:5000/webhook"

if last_row['ADX_14'] >= 25:
    if last_row['DMP_14'] > last_row['DMN_14']:
        message = f"**STRONG UPTREND**: The ADX is {last_row['ADX_14']:.2f} + DI {last_row['DMP_14']:.2f} - DI {last_row['DMN_14']:.2f}."
    if last_row['DMN_14'] > last_row['DMP_14']:
        message = f"**STRONG DOWNTREND**: The ADX is {last_row['ADX_14']:.2f} + DI {last_row['DMP_14']:.2f} - DI {last_row['DMN_14']:.2f}."

    data = {
        "content": message
    }

    requests.post(WEBHOOK_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'})

if last_row['ADX_14'] < 25:
    message = f"**NO TREND**: The ADX is {last_row['ADX_14']:.2f} + DI {last_row['DMP_14']:.2f} - DI {last_row['DMN_14']:.2f}."

    data = {
        "content": message
    }

    requests.post(WEBHOOK_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    
from flask import Flask, request, abort
app = Flask(__name__)
@app.route('/webhook', methods=['POST'])
def get_webhook():
    if request.method == 'POST':
        
        print("received data: ", request.json)
        
        return 'success', 200
    else:
        
        abort(400)
    if __name__ == '__main__':
        app.run()