from datetime import datetime as dt
from datetime import timedelta

from broker.transactions import Transaction
from broker.config import ACCOUNT_NUMBER


def get_transactions(start_date=None, end_date=None, symbol=None):

    if not end_date:
        to_date = dt.now()
        end_date = to_date.strftime("%Y-%m-%d")
    
    if not start_date:
        from_date = to_date - timedelta(days=90)
        start_date = from_date.strftime("%Y-%m-%d")

    transaction = Transaction()
    df = transaction.get_transactionsDF(
        ACCOUNT_NUMBER,
        transaction_type="TRADE",
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
    )
    new_df = df.filter(
        [
            "settlementDate",
            "netAmount",
            "transactionSubType",
            "transactionItem.amount",
            "transactionItem.price",
            "transactionItem.instrument.underlyingSymbol",
            "transactionItem.instrument.description",
            "transactionItem.instrument.assetType"
        ],
        axis=1,
    )
    return new_df
