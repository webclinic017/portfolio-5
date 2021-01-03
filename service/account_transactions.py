import logging

from datetime import datetime as dt
from datetime import timedelta

import pandas as pd

from broker.transactions import Transaction
from broker.config import ACCOUNT_NUMBER



def get_transactions(
    start_date=None, end_date=None, symbol=None, instrument_type=None, tran_type=None
):

    # Mapping column for UI display
    params_transactions = {
        "transactionDate": "DATE",
        "netAmount": "TOTAL PRICE",
        "transactionSubType": "TRAN TYPE",
        "transactionItem.amount": "QTY",
        "transactionItem.price": "PRICE",
        "transactionItem.instrument.underlyingSymbol": "TICKER",
        "transactionItem.instrument.assetType": "TYPE",
        "transactionItem.instrument.putCall": "OPTION TYPE",
        "transactionItem.positionEffect": "POSITION",
        "transactionItem.instrument.symbol": "SYMBOL",
    }

    # In case start date or end date is not passed, use to initiliaze default
    to_date = dt.now()

    if not end_date:
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

    if not df.empty:
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
                "transactionItem.instrument.assetType",
                "transactionItem.instrument.putCall",
            ],
            axis=1,
        )

        # Change df['transactionDate'] string to remove timestamp
        df["transactionDate"] = pd.to_datetime(
            df["transactionDate"], format="%Y-%m-%dT%H:%M:%S%z"
        ).dt.strftime("%m/%d/%y")

        if instrument_type:
            if instrument_type == "PUT" or instrument_type == "CALL":
                # Filter for either PUT or CALL option types
                isOptionType = (
                    df["transactionItem.instrument.putCall"] == instrument_type
                )
                df = df[isOptionType]

                # Add Expiration Date
                df["expirationDate"] = df["transactionItem.instrument.symbol"].apply(get_expiration_date)

            elif instrument_type == "EQUITY" or instrument_type == "OPTION":
                # Filter for either EQUITY or OPTION asset types
                isAssetType = (
                    df["transactionItem.instrument.assetType"] == instrument_type
                )
                df = df[isAssetType]

        if tran_type:
            isTranType = df["transactionSubType"] == tran_type
            # Filter for Transaction sub type
            df = df[isTranType]

        df = df.rename(columns=params_transactions)

        # For Equity Ticker comes as null. Use Symbol
        df['TICKER'].fillna(df['SYMBOL'], inplace = True)

    return df

def get_expiration_date(option_symbol):
 
    #split string by _ and get next 6 characters as symbol is of format FB_031320C225
    date_string = option_symbol.split('_')[1][:6]

    # Convert to datetime
    return  dt.strptime(date_string, '%m%d%y').strftime('%m/%d/%y')


def get_report(start_date=None, end_date=None, symbol=None, instrument_type=None):
    df = get_transactions(start_date, end_date, symbol, instrument_type)
 
    # All opening positions
    df_open = df [df["POSITION"] == 'OPENING']

    # All Closing positions
    df_close = df [df["POSITION"] == 'CLOSING']

    result_df = pd.merge(df_open[["SYMBOL","DATE","TOTAL PRICE", "PRICE", "TICKER", "POSITION"]], df_close[["SYMBOL", "TOTAL PRICE", "PRICE", "POSITION"]], how="left", on=["SYMBOL"], suffixes=("_O", "_C"))
    
    result_df["PRICE"] = result_df["PRICE_O"]
    result_df["TOTAL PRICE"] = result_df["TOTAL PRICE_O"]
    result_df["POSITION"] = result_df["POSITION_O"]
    result_df["TRAN TYPE"] = result_df["POSITION_C"]

    return result_df
