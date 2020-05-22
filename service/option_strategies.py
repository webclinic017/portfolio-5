import pandas as pd
from utils.enums import PUT_CALL, ORDER_TYPE
from .checks import (
    singles_checks,
)
from datetime import datetime
from .search_income import income_finder

 # Mapping column for UI display
table_mapping = {
    "strike_price": "STRIKE",
    "stock_price": "STOCK PRICE",
    "volatility": "VOLATILITY",
    "delta": "DELTA",
    "mark": "PRICE",
    "underlying": "TICKER",
    "expiration": "EXPIRATION",
    "days_to_expiration": "DAYS",
    "returns": "RETURNS",
    "breakeven": "BREAK EVEN",
    "symbol" : "SYMBOL",										
}

def _process_legs(ticker, legs, params, check_func):
    if _filter_checks(params, check_func):
        for leg in legs:
            kwargs =  _create_legs(leg, params)
            return income_finder(ticker, **kwargs)
    else:
        raise ValueError(
            "Invalid filter values provided, please check the filters and try again."
        )

def _create_legs(leg, params):
    return _merge(params, leg[0])


def _filter_checks(filter, func=None):
    return True
    # return True if func is None else func(filter)

def _merge(params, contractType):
    return {**params, **{"contractType": contractType}}

def long_call (ticker, params):
    legs = [(PUT_CALL.CALL.value, ORDER_TYPE.DEBIT.value)]
    return _process_legs( ticker, legs, params, singles_checks)


def short_call(ticker, params):
    legs = [(PUT_CALL.CALL.value, ORDER_TYPE.CREDIT.value)]
    return _process_legs(ticker, legs, params, singles_checks)


def long_put(ticker, params):
    legs = [(PUT_CALL.PUT.value, ORDER_TYPE.DEBIT.value)]
    return _process_legs(ticker, legs, params, singles_checks)


def short_put(ticker, params):
    legs = [(PUT_CALL.PUT.value, ORDER_TYPE.CREDIT.value)]
    return _process_legs(ticker, legs, params, singles_checks)

def watchlist_income(watch_list, params, func):
    df = pd.DataFrame()
    # Get Option chain for watch list
    for ticker in watch_list:
        # print("getting stock option for ", stock)
        df2 = func(ticker, params)
        # Append to main DF list
        df = df.append(df2, ignore_index=True)

    if not df.empty:
        df = df.sort_values(by=['days_to_expiration','symbol'])
        df = df.rename(columns=table_mapping)
    return df