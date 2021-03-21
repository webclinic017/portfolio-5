from datetime import datetime as dt
from datetime import timedelta

import pandas as pd
import logging

from broker.transactions import Transaction
from broker.config import ACCOUNT_NUMBER

from utils.functions import parse_option_symbol, formatter_number_2_digits


current_year_date = '2021-01-01'
default_start_duration = 180

# Mapping column for UI display
params_options = {
    "transactionDate": "DATE",
    "netAmount": "TOTAL_PRICE",
    "transactionSubType": "TRAN_TYPE",
    "transactionItem.amount": "QTY",
    "transactionItem.price": "PRICE",
    "transactionItem.instrument.underlyingSymbol": "TICKER",
    "transactionItem.instrument.assetType": "TYPE",
    "transactionItem.instrument.optionExpirationDate": "EXPIRY_DATE",
    "transactionItem.instrument.putCall": "OPTION_TYPE",
    "transactionItem.positionEffect": "POSITION",
    "transactionItem.instrument.symbol": "SYMBOL",
    "transactionItem.instruction": "INSTRUCTION",
}

# Mapping column for UI display
params_equity = {
    "transactionDate": "DATE",
    "netAmount": "TOTAL_PRICE",
    "transactionSubType": "TRAN_TYPE",
    "transactionItem.amount": "QTY",
    "transactionItem.price": "PRICE",
    "transactionItem.instrument.assetType": "TYPE",
    "transactionItem.positionEffect": "POSITION",
    "transactionItem.instrument.symbol": "SYMBOL",
    "transactionItem.instruction": "INSTRUCTION",
}


def retrive_transactions(
    start_date=None, end_date=None, symbol=None, instrument_type=None, tran_type=None
):
    """
    This method is called from Transactions screen.
    It will internally call get_transactions method.

    Args:
        start_date ([str], optional): [Include Transcations after the start date]. Defaults to None.
        end_date ([str], optional): [Include Transcations before the end date]. Defaults to None.
        symbol ([str], optional): [description]. Defaults to None.
        instrument_type ([str], optional): [description]. Defaults to None.
        tran_type ([str], optional): [description]. Defaults to None.

    Returns:
        [df]: [Transactions for given search criteria]
    """    

    
    df = get_transactions(start_date, end_date, symbol, instrument_type, tran_type)
    if instrument_type:
        if instrument_type == "PUT" or instrument_type == "CALL":
            # Filter for either PUT or CALL option types
            df = df.rename(columns=params_options)
            df = df[df["OPTION_TYPE"] == instrument_type]
            

        elif instrument_type == "EQUITY":
            # Filter for either EQUITY or OPTION asset types
            df = df.rename(columns=params_equity)
            df = df[df["TYPE"] == instrument_type]
           

    if tran_type:
        # Filter for Transaction sub type
        df = df[df["transactionSubType"] == tran_type]
    return df

def get_transactions(
    start_date=None, end_date=None, symbol=None, instrument_type=None, tran_type=None
):
    """[Calls the TD transactions API class ]

    Args:
        start_date ([str], optional): [Include Transcations after the start date]. Defaults to None.
        end_date ([str], optional): [Include Transcations before the end date]. Defaults to None.
        symbol ([str], optional): [description]. Defaults to None.
        instrument_type ([str], optional): [description]. Defaults to None.
        tran_type ([str], optional): [description]. Defaults to None.

    Returns:
        df: Transactions for given search criteria
    """    

    
    # In case start date or end date is not passed, use to initiliaze default
    to_date = dt.now()

    if not end_date:
        end_date = to_date.strftime("%Y-%m-%d")

    if not start_date:
        from_date = to_date - timedelta(days=default_start_duration)
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

        # Change df['transactionDate'] string to remove timestamp
        df["transactionDate"] = pd.to_datetime(
            df["transactionDate"], format="%Y-%m-%dT%H:%M:%S%z"
        ).dt.strftime("%Y-%m-%d")

        # Change df['optionExpirationDate'] string to remove timestamp
        df["transactionItem.instrument.optionExpirationDate"] = pd.to_datetime(
            df["transactionItem.instrument.optionExpirationDate"], format="%Y-%m-%dT%H:%M:%S%z"
        ).dt.strftime("%Y-%m-%d")
    return df


def get_report(start_date=None, end_date=None, symbol=None, instrument_type=None):
    
    """
    This method is called from Transactions screen.
    It will internally call get_transactions method.

    Args:
        start_date ([str], optional): [Include Transcations after the start date]. Defaults to None.
        end_date ([str], optional): [Include Transcations before the end date]. Defaults to None.
        symbol ([str], optional): [description]. Defaults to None.
        instrument_type ([str], optional): [description]. Defaults to None.

    Returns:
        [df]: [Transactions for given search criteria]
    """    

    df = get_transactions(start_date, end_date, symbol, instrument_type)
 
    # Processing for Options
    if not df.empty:
        if (instrument_type == "PUT" or instrument_type == "CALL"):
            df = df.rename(columns=params_options)
            # Filter for either PUT or CALL option types
            df = df[df["OPTION_TYPE"] == instrument_type]
            df = parse_option_response(df)
            
        
        elif instrument_type == "EQUITY":
            df = df.rename(columns=params_equity)
            # Filter for either EQUITY or OPTION asset types
            df = df[df["TYPE"] == instrument_type]
            df = parse_equity_response(df)
            
    
    return df

def parse_option_response(df_trade):
    """[Parse Option Response coming from transactions API]

    Args:
        df_trade ([df]): [Filtered Options transaction]

    Returns:
        [df]: [Options transactions to be displayed on screen]
    """    
    # df_recieve_deliver = df[df["transactionSubType"] == "OA"]
    
    # All opening positions
    df_open = df_trade [df_trade["POSITION"] == 'OPENING']

    # Combine orders which were split by broker into multiple orders while execution
    df_open = df_open.groupby(['SYMBOL','DATE','EXPIRY_DATE','TICKER','POSITION']).agg({'TOTAL_PRICE':'sum','PRICE':'mean', 'QTY':'sum'})
    df_open = df_open.reset_index()
   
    
    # All Closing positions
    df_close = df_trade [df_trade["POSITION"] == 'CLOSING']

    # Combine orders which were split by broker into multiple orders while execution
    df_close = df_close.groupby(['SYMBOL','DATE','EXPIRY_DATE','TICKER','POSITION']).agg({'TOTAL_PRICE':'sum','PRICE':'mean', 'QTY':'sum'})
    df_close = df_close.reset_index()
 

    result_df = pd.merge(df_open[["SYMBOL","DATE","EXPIRY_DATE","TOTAL_PRICE", "PRICE", "QTY","TICKER", "POSITION"]], df_close[["SYMBOL", "DATE", "TOTAL_PRICE", "QTY", "TICKER", "PRICE", "POSITION"]], how="outer", on=["SYMBOL", "QTY", "TICKER"], suffixes=("_O", "_C"))
    result_df[["DATE","CLOSE_DATE"]] = result_df.apply(get_date, axis=1, result_type="expand")
    result_df["PRICE"] = result_df["PRICE_O"]
    result_df["CLOSE_PRICE"] = result_df["PRICE_C"].fillna(0)
    result_df["TOTAL_PRICE"] = result_df.apply(get_net_total_price, axis=1)
    # result_df["POSITION"] = result_df["POSITION_O"]
    # result_df["TRAN_TYPE"] = result_df["POSITION_C"]

    # Add Close Date and Strike price by parsing option symbol string
    result_df[["CLOSE_DATE","STRIKE_PRICE"]] = result_df.apply(parse_option_string, axis=1,result_type="expand")


    # merge TRADE and RECIEVE AND DELIVER
    # final_df = pd.merge(result_df[["SYMBOL","DATE","CLOSE_DATE", "STRIKE_PRICE", "EXPIRY_DATE","TOTAL_PRICE", "PRICE", "QTY","TICKER"]], df_recieve_deliver[["SYMBOL", "DATE", "TOTAL_PRICE", "QTY", "TICKER", "PRICE", "POSITION"]], how="outer", on=["SYMBOL", "QTY", "TICKER"], suffixes=("_O", "_C"))
    result_df = result_df[(result_df['CLOSE_DATE'] > current_year_date)]
    return result_df

def parse_equity_response(df_trade):
    """[Parse Equity Response coming from transactions API]

    Args:
        df_trade ([df]): [Filtered Options transaction]

    Returns:
        [df]: [Equity transactions to be displayed on screen]
    """  
    return df_trade


def get_net_total_price(row):
    """[summary]

    Args:
        row ([df row]): [Single row of DF to whch the function is applied]

    Returns:
        [Net Total price]: [Sum of opening transcation and Closing transaction]
    """    
    open_total = row ["TOTAL_PRICE_O"]
    close_total = row ["TOTAL_PRICE_C"]
    if pd.isna(open_total):
        open_total = 0
    if pd.isna(close_total):
        close_total = 0

    return open_total + close_total

def parse_option_string(row):
    """Parse Option String to get expiration date and Strike price.
    If closing transaction is not applicable, use Expiry date as the Close date for those Option trades

    Args:
        row ([df row]): [Single row of DF to whch the function is applied]

    Returns:
        [type]: [description]
    """    
    
    option_symbol = row ["SYMBOL"]
    close_date = row ["CLOSE_DATE"]
    expiration_date, strike_price =  parse_option_symbol(option_symbol)

    # If transaction was not explicitly closed, close date is same as option expiry date
    if pd.isna(close_date):
        close_date = expiration_date
    return close_date, strike_price
    

def get_date(row):
    """ Return dates for opening trade and Closing Trade for the Option Trade
    If Open Trade date is not pulled in the search criteria, the corresponding close trade is displayed
    on its own as independent Open Trade so swap with Open date for such trades 

    Args:
        row ([df row]): [Single row of DF to whch the function is applied]

    Returns:
        [type]: [description]
    """    

    open_date = row["DATE_O"]
    close_date = row["DATE_C"]

    if pd.isna(open_date):
        # Open date is before Search and transaction not pulled or other mismatch
        # Only for closing transaction not matching
        open_date = close_date
        close_date = None
    return open_date, close_date


