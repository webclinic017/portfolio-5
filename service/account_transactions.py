import logging
import re

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
        "netAmount": "TOTAL_PRICE",
        "transactionSubType": "TRAN_TYPE",
        "transactionItem.amount": "QTY",
        "transactionItem.price": "PRICE",
        "transactionItem.instrument.underlyingSymbol": "TICKER",
        "transactionItem.instrument.assetType": "TYPE",
        "transactionItem.instrument.putCall": "OPTION_TYPE",
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


def get_report(start_date=None, end_date=None, symbol=None, instrument_type=None):
    df = get_transactions(start_date, end_date, symbol, instrument_type)
 
    # Processing for Options
    if not df.empty and (instrument_type == "PUT" or instrument_type == "CALL"):
        # All opening positions
        df_open = df [df["POSITION"] == 'OPENING']

        # All Closing positions
        df_close = df [df["POSITION"] == 'CLOSING']

        result_df = pd.merge(df_open[["SYMBOL","DATE","TOTAL_PRICE", "PRICE", "QTY","TICKER", "POSITION"]], df_close[["SYMBOL", "DATE", "TOTAL_PRICE", "QTY", "TICKER", "PRICE", "POSITION"]], how="outer", on=["SYMBOL", "QTY", "TICKER"], suffixes=("_O", "_C"))
        result_df = result_df.fillna(0)
        result_df["PRICE"] = result_df["PRICE_O"]
        result_df["DATE"] = result_df.apply(lambda x: get_date (x.DATE_O, x.DATE_C), axis=1)
        result_df["CLOSE_PRICE"] = result_df["PRICE_C"]
        result_df["TOTAL_PRICE"] = result_df.apply(lambda x:  x.TOTAL_PRICE_O + x.TOTAL_PRICE_C, axis=1)
        result_df["POSITION"] = result_df["POSITION_O"]
        result_df["TRAN_TYPE"] = result_df["POSITION_C"]

        # Add Expiration Date and Strike price bt parsing option symbol string
        result_df[["EXPIRATION_DATE","STRIKE_PRICE"]] = result_df.apply(parse_option_string, axis=1,result_type="expand")
        return result_df
        
    else:
        return df

def parse_option_string(row):

    option_symbol = row ["SYMBOL"]
    
    logging.debug(" Option Symbol is %s", option_symbol)
    
    # Regex to parse option string
    matcher = re.compile(r'^(.+)([0-9]{6})([PC])(\d*\.?\d*)')

    groups = matcher.search(option_symbol)

    # Date is in group 2
    date_string = groups[2]
    logging.debug(" date_string is %s", date_string)

    # Strike is in group 4
    strike_price = groups[4]
    logging.debug(" strike_price is %s", strike_price)

    # Convert to datetime
    expiration_date = dt.strptime(date_string,'%m%d%y').strftime('%m/%d/%y')

    return expiration_date, strike_price


def get_date(opening_date, closing_date):

    # No dates are coming as nan if blank or else as string
    if isinstance(opening_date, str):
        return opening_date
    else:
        # Only for closing transaction not matching
        return closing_date


