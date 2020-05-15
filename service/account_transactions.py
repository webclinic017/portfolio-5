from datetime import datetime as dt
from datetime import timedelta

from broker.transactions import Transaction
from broker.config import ACCOUNT_NUMBER


def get_transactions():

    endDate = dt.now()
    startDate = endDate - timedelta(days=5)

    startDate = startDate.strftime('%Y-%m-%d')
    endDate = endDate.strftime('%Y-%m-%d')

    transaction = Transaction()
    res = transaction.get_transactions(
        ACCOUNT_NUMBER, transaction_type='TRADE', symbol=None, start_date=startDate, end_date=endDate)
    return res
