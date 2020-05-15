import unittest

from datetime import datetime as dt
from datetime import timedelta
import pandas as pd

from broker.quotes import Quotes
from broker.account import Account
from broker.config import CONSUMER_ID, REDIRECT_URI, ACCOUNT_NUMBER
from broker.option_chain import OptionChain
from broker.options import Options
import logging



class APIResponses(unittest.TestCase):

    def test_quotes(self):
        ticker = "LYFT"
        quotes = Quotes()
        res = quotes.get_quotes(ticker)
        assert res is not None

    def test_position(self):
        account = Account()
        res = account.get_positions(account=ACCOUNT_NUMBER)
        assert res[0] is not None

    def test_history(self):
        from broker.history import History

        endDate = dt.now()
        startDate = endDate - timedelta(days=45)

        history = History()
        res = history.get_price_history(symbol="MSFT", periodType="month",
                                        frequencyType="daily", frequency=1, startDate=startDate, endDate=endDate)
        assert res['candles'] is not None

    def test_options(self):
        startDate = dt.now()
        endDate = startDate + timedelta(days=45)

        options = Options()
        option_chain_req = OptionChain(
            symbol="AMD",
            strategy="SINGLE",
            range="ALL",
            includeQuotes="TRUE",
            fromDate=startDate,
            toDate=endDate,
        )
        res = options.get_options_chain(option_chain=option_chain_req)
        assert res['symbol'] is not None

    def test_strategies(self):
        from service.option_strategies import (
            watchlist_income,
            short_put,
            short_call,
            long_put,
            long_call
        )

        tickers = ['AAPL', 'MSFT', 'LYFT','CAT', 'DIS']

        params = {
            'moneyness': 2,
            'premium': 2,
            'min_expiration_days': 15,
            'max_expiration_days': 40,
        }

        res = watchlist_income(tickers, params, short_put)
        assert res is not None


if __name__ == "__main__":
    logging.basicConfig (filename="tests.log", level=logging.DEBUG, format='%(asctime)s %(message)s')
    unittest.main()
