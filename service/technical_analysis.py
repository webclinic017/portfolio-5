import pandas as pd
import logging
from statistics import mean 

import numpy as np
import talib as ta

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

# Crossover constants
SHORT_SAVG_PERIOD = 10
LONG_MAVG1_PERIOD = 20
LONG_MAVG2_PERIOD = 30
PERIOD = 30


def get_analysis(df):
    
    df['signal'] = 0.0

    df['rsi'] = ta.RSI(df.close, RSI_PERIOD).apply(formatter_number)
    df['macd'], df['macdsignal'], df['macdhist'] = ta.MACD(df.close, fastperiod=MACD_FAST, slowperiod=MACD_SLOW, signalperiod=MACD_SIGNAL)
    df['short_mavg'] = ta.SMA(df.close, SHORT_SAVG_PERIOD).apply(formatter_number_2_digits)
    df['long_mavg_1'] = ta.EMA(df.close, LONG_MAVG1_PERIOD).apply(formatter_number_2_digits)
    df['long_mavg_2'] = ta.EMA(df.close, LONG_MAVG2_PERIOD).apply(formatter_number_2_digits)

    low_period = min(df.low.tail(PERIOD))
    high_period = max(df.high.tail(PERIOD))
    mean_period = formatter_number_2_digits(mean(df.close.tail(PERIOD)))

    logging.info("low_30 %s high_30 %s", low_period, high_period)

    return df, low_period, high_period, mean_period



def get_crossovers(df):
    
    df['signal'] = 0.0

    df['signal'][LONG_MAVG2_PERIOD:] = np.where(df['short_mavg'][LONG_MAVG2_PERIOD:] > df['long_mavg_2'][LONG_MAVG2_PERIOD:], 1.0, 0.0)
    df['crossover'] = df['signal'].diff()

    is_signal = df['crossover'] != 0
    signals = df[is_signal]
    signals = signals.dropna()

    return signals


def get_candlestick_patterns(df):
    # extract OHLC 
    op = df['open']
    hi = df['high']
    lo = df['low']
    cl = df['close']

    candle_names = ta.get_function_groups()['Pattern Recognition']

    for candle in candle_names:
        df[candle] = getattr(ta, candle)(op, hi, lo, cl)

    
    return df

   