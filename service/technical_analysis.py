from datetime import datetime as dt
from datetime import timedelta
import pandas as pd
import logging
from statistics import mean 

import numpy as np
import talib as ta

from broker.history import History
from utils.functions import formatter_number, formatter_number_2_digits

# Technical Analysis
SMA_FAST = 50
SMA_SLOW = 200
RSI_PERIOD = 14
DX_PERIOD = 14
RSI_AVG_PERIOD = 15
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
STOCH_K = 14
STOCH_D = 3
SIGNAL_TOL = 3
Y_AXIS_SIZE = 12


def get_analysis(ticker, startDate=None, endDate=None):

    if not endDate:
        endDate = dt.now()
    
    if not startDate:
        startDate = endDate - timedelta(days=120)

    # Retrieve Prices and volumes for a ticker
    history = History()
    df = history.get_price_historyDF(
        symbol=ticker,
        periodType="month",
        frequencyType="daily",
        frequency=1, 
        startDate=startDate,
        endDate=endDate,
    )
    
    df['rsi'] = ta.RSI(df.close, RSI_PERIOD).apply(formatter_number)
    df['macd'], df['macdsignal'], df['macdhist'] = ta.MACD(df.close, fastperiod=MACD_FAST, slowperiod=MACD_SLOW, signalperiod=MACD_SIGNAL)
    df['sma10'] = ta.SMA(df.close, 10).apply(formatter_number_2_digits)
    df['ema20'] = ta.EMA(df.close, 20).apply(formatter_number_2_digits)
    df['ema30'] = ta.EMA(df.close, 30).apply(formatter_number_2_digits)
    low_30 = min(df.low.tail(30))
    high_30 = max(df.high.tail(30))
    mean_30 = formatter_number_2_digits(mean(df.close.tail(30)))

    logging.info("low_30 %s high_30 %s", low_30, high_30)

    return df, low_30, high_30, mean_30
   