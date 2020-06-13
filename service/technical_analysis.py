import pandas as pd
import logging

import numpy as np
import talib as ta

from itertools import compress

from utils.functions import formatter_number, formatter_number_2_digits
from utils.candle_rankings import candle_rankings

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


def get_analysis(df):

    df["signal"] = 0.0

    df["rsi"] = ta.RSI(df.close, RSI_PERIOD).apply(formatter_number)
    df["macd"], df["macdsignal"], df["macdhist"] = ta.MACD(
        df.close, fastperiod=MACD_FAST, slowperiod=MACD_SLOW, signalperiod=MACD_SIGNAL
    )
    df["short_mavg"] = ta.SMA(df.close, SHORT_SAVG_PERIOD).apply(
        formatter_number_2_digits
    )
    df["long_mavg_1"] = ta.EMA(df.close, LONG_MAVG1_PERIOD).apply(
        formatter_number_2_digits
    )
    df["long_mavg_2"] = ta.EMA(df.close, LONG_MAVG2_PERIOD).apply(
        formatter_number_2_digits
    )

    return df


def get_crossovers(df):

    df["signal"] = 0.0

    df["signal"][LONG_MAVG2_PERIOD:] = np.where(
        df["short_mavg"][LONG_MAVG2_PERIOD:] > df["long_mavg_2"][LONG_MAVG2_PERIOD:],
        1.0,
        0.0,
    )
    df["crossover"] = df["signal"].diff()

    is_signal = df["crossover"] != 0
    signals = df[is_signal]
    signals = signals.dropna()

    return signals


def recognize_candlestick(df):
    """
    Recognizes candlestick patterns and appends 2 additional columns to df;
    1st - Best Performance candlestick pattern matched by www.thepatternsite.com
    2nd - # of matched patterns
    """

    op = df["open"].astype(float)
    hi = df["high"].astype(float)
    lo = df["low"].astype(float)
    cl = df["close"].astype(float)

    candle_names = ta.get_function_groups()["Pattern Recognition"]

    # patterns not found in the patternsite.com
    exclude_items = (
        "CDLCOUNTERATTACK",
        "CDLLONGLINE",
        "CDLSHORTLINE",
        "CDLSTALLEDPATTERN",
        "CDLKICKINGBYLENGTH",
    )

    candle_names = [candle for candle in candle_names if candle not in exclude_items]

    # create columns for each candle
    for candle in candle_names:
        # below is same as;
        # df["CDL3LINESTRIKE"] = talib.CDL3LINESTRIKE(op, hi, lo, cl)
        df[candle] = getattr(ta, candle)(op, hi, lo, cl)
    df["candlestick_pattern"] = np.nan
    df["candlestick_match_count"] = np.nan
    for index, row in df.iterrows():

        # no pattern found
        if len(row[candle_names]) - sum(row[candle_names] == 0) == 0:
            df.loc[index, "candlestick_pattern"] = ""
            df.loc[index, "candlestick_match_count"] = 0
        # single pattern found
        elif len(row[candle_names]) - sum(row[candle_names] == 0) == 1:
            # bull pattern 100 or 200
            if any(row[candle_names].values > 0):
                pattern = (
                    list(
                        compress(
                            row[candle_names].keys(), row[candle_names].values != 0
                        )
                    )[0]
                    + "_Bull"
                )
                df.loc[index, "candlestick_pattern"] = pattern
                df.loc[index, "candlestick_match_count"] = 1
            # bear pattern -100 or -200
            else:
                pattern = (
                    list(
                        compress(
                            row[candle_names].keys(), row[candle_names].values != 0
                        )
                    )[0]
                    + "_Bear"
                )
                df.loc[index, "candlestick_pattern"] = pattern
                df.loc[index, "candlestick_match_count"] = 1
        # multiple patterns matched -- select best performance
        else:
            # filter out pattern names from bool list of values
            patterns = list(
                compress(row[candle_names].keys(), row[candle_names].values != 0)
            )
            container = []
            for pattern in patterns:
                if row[pattern] > 0:
                    container.append(pattern + "_Bull")
                else:
                    container.append(pattern + "_Bear")
            rank_list = [candle_rankings[p] for p in container]
            if len(rank_list) == len(container):
                rank_index_best = rank_list.index(min(rank_list))
                df.loc[index, "candlestick_pattern"] = container[rank_index_best]
                df.loc[index, "candlestick_match_count"] = len(container)

    # clean up candle columns
    cols_to_drop = candle_names
    df.drop(cols_to_drop, axis=1, inplace=True)

    return df

