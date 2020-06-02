from datetime import datetime as dt
from datetime import timedelta
import pandas as pd

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


def get_analysis(df):
    analysis = df
 
    analysis['rsi'] = ta.RSI(df.close, RSI_PERIOD).apply(formatter_number)
    analysis['macd'], analysis['macdsignal'], analysis['macdhist'] = ta.MACD(df.close, fastperiod=MACD_FAST, slowperiod=MACD_SLOW, signalperiod=MACD_SIGNAL)
    analysis['sma10'] = ta.SMA(df.close, 10).apply(formatter_number_2_digits)
    analysis['ema20'] = ta.EMA(df.close, 20).apply(formatter_number_2_digits)
    analysis['ema30'] = ta.EMA(df.close, 30).apply(formatter_number_2_digits)

    return analysis
   