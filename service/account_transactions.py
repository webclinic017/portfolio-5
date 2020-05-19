from datetime import datetime as dt
from datetime import timedelta

from broker.transactions import Transaction
from broker.config import ACCOUNT_NUMBER
import pandas as pd

def get_transactions(
    start_date=None, end_date=None, symbol=None, option_type=None, tran_type=None
):
    
    # Mapping column for UI display
    params_transactions = {
        "transactionDate": "DATE",
        "netAmount": "TOTAL PRICE",
        "transactionSubType": "TRAN TYPE",
        "transactionItem.amount": "QTY",
        "transactionItem.price": "PRICE",
        "transactionItem.instrument.underlyingSymbol": "TICKER",
        "transactionItem.instrument.description": "DESC",
        "transactionItem.instrument.assetType": "TYPE",
        "transactionItem.instrument.putCall": "OPTION TYPE",
        "transactionItem.positionEffect": "POSITION",
        "transactionItem.instrument.symbol" : "SYMBOL",
    }


    if not end_date:
        to_date = dt.now()
        end_date = to_date.strftime("%Y-%m-%d")

    if not start_date:
        from_date = to_date - timedelta(days=180)
        start_date = from_date.strftime("%Y-%m-%d")

    transaction = Transaction()
    df = transaction.get_transactionsDF(
        ACCOUNT_NUMBER,
        transaction_type="TRADE",
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
    )

    df = df.filter(
        [
            "transactionDate",
            "netAmount",
            "transactionItem.instrument.symbol",
            "transactionSubType",
            "transactionItem.positionEffect",
            "transactionItem.amount",
            "transactionItem.price",
            "transactionItem.instrument.underlyingSymbol",
            "transactionItem.instrument.description",
            "transactionItem.instrument.assetType",
            "transactionItem.instrument.putCall",
        ],
        axis=1,
    )

    # Change df['transactionDate'] string to remove timestamp
    df['transactionDate'] = pd.to_datetime(df['transactionDate'], format="%Y-%m-%dT%H:%M:%S%z").dt.strftime("%m/%d/%y")

    if option_type:
        isOptionType = df["transactionItem.instrument.putCall"] == option_type
        df = df[isOptionType]

    if tran_type:
        isTranType = df["transactionSubType"] == tran_type
        df = df[isTranType]
    
    df = df.rename(columns=params_transactions)
    return df
