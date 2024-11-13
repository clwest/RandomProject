import ccxt, yfinance
import pandas_ta as ta
import pandas as pd
import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')



exchange_id = 'binanceus'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    "apiKey": BINANCE_API_KEY,
    "secret": BINANCE_SECRET_KEY
})

webhook = os.getenv('DISCORD_WEBHOOK')


bars = exchange.fetch_ohlcv('ETH/USDT', timeframe='5m', limit=500)


df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
adx = df.ta.adx()
macd = df.ta.macd()
rsi = df.ta.rsi()

df = pd.concat([df, adx, macd, rsi], axis=1)

st.dataframe(df)
print(df)
