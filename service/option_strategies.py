import multiprocessing
import pandas as pd
from joblib import Parallel, delayed

from utils.enums import PUT_CALL, ORDER_TYPE
from utils.functions import formatter_currency_with_cents

from .checks import singles_checks
from .search_income import income_finder


num_cores = multiprocessing.cpu_count()

# Mapping column for UI display
TABLE_MAPPING = {
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
    "symbol": "SYMBOL",
    "open_interest": "OPEN INT",
    "volume" : "VOLUME",
    "percentage_otm" : "OTM",
}


def _process_legs(ticker, legs, params, check_func):
    if _filter_checks(params, check_func):
        for leg in legs:
            kwargs = _create_legs(leg, params)
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


def long_call(ticker, params):
    legs = [(PUT_CALL.CALL.value, ORDER_TYPE.DEBIT.value)]
    return _process_legs(ticker, legs, params, singles_checks)


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
    # Parallel mode for API calls
    results = Parallel(n_jobs=num_cores)(delayed(func)(i, params) for i in watch_list)

    #  Aggregate the results
    for result in results:
        df = df.append(result, ignore_index=True)

    if not df.empty:
        df = df.sort_values(by=["returns"], ascending=False)
        df["strike_price"] = df["strike_price"].apply(formatter_currency_with_cents)
        df["stock_price"] = df["stock_price"].apply(formatter_currency_with_cents)
        df["mark"] = df["mark"].apply(formatter_currency_with_cents)
        df["breakeven"] = df["breakeven"].apply(formatter_currency_with_cents)

        df = df.drop(
            [
                "desired_premium",
                "desired_moneyness",
                "desired_min_delta",
                "desired_max_delta",
                "type",
                "expiration_type",
                "spread",
                "expiration"
            ],
            axis=1,
        )

        df = df.rename(columns=TABLE_MAPPING)
    return df
