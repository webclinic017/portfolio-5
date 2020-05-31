from broker.history import History
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd

import numpy as np
from talib import RSI, BBANDS


def get_RSI(ticker):
    
    endDate = dt.now()
    startDate = endDate - timedelta(days=45)

    history = History()
    res = history.get_price_history(symbol=ticker, periodType="month",
                                    frequencyType="daily", frequency=1, startDate=startDate, endDate=endDate)
    price = pd.json_normalize(res)
    close = price['close'].values

    rsi = RSI(close, timeperiod=14)
    return rsi[-1]