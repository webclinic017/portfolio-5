# Import the client

from broker.history import History
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd
import logging

logging.basicConfig(filename="screener.log",
                    level=logging.DEBUG, format='%(asctime)s %(message)s')

# ============================================================================
# Search instrumenticker# from td.search import Search
# search = Search()

# res = search.search_instruments("AAPL")


# ============================================================================
# Get Price History
#

# endDate = dt.now()
# startDate = endDate - timedelta(days=45)

# history = History()
# res = history.get_price_history(symbol="MSFT", periodType="month",
#                                 frequencyType="daily", frequency=1, startDate=startDate, endDate=endDate)
# print(res)
# ============================================================================
# Get Options Chain

# from td.options import Options
# from td.option_chain import OptionChain

# startDate = dt.now()
# endDate = startDate + timedelta(days=45)

# options = Options()
# option_chain_req = OptionChain(
#     symbol="AAPL",
#     strategy="SINGLE",
#     range="ALL",
#     includeQuotes="TRUE",
#     fromDate=startDate,
#     toDate=endDate,
# )
# res = options.get_options_chain(option_chain=option_chain_req)

# ============================================================================
# Get Position Details

# from td.account import Account

# from td.config import CONSUMER_ID, REDIRECT_URI, ACCOUNT_NUMBER

# account = Account()

# account.login()
# res = account.get_accounts(account = ACCOUNT_NUMBER)
# print (res)
#
# res = search_income('MSFT', min_expiration_days=14, max_expiration_days=20, contractType="PUT", )
# from service.option_strategies import (
#     watchlist_income,
#     short_put,
#     short_call,
#     long_put,
#     long_call
# )

# tickers = ['AAPL', 'MSFT', 'LYFT','CAT', 'DIS']

# params = {
#     'moneyness': 2,
#     'premium': 2,
#     'min_expiration_days': 15,
#     'max_expiration_days': 40,
# }

# res = watchlist_income(tickers, params, short_put)
# print(res)


# from td.quotes import Quotes
# quotes = Quotes()

# res = quotes.get_quotes("AAPL_050120C280")exit

from service.account_positions import get_account_positions

res = get_account_positions()
print(res)
