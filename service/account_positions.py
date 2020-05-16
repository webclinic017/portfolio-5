import numpy as np
import pandas as pd
import logging


from broker.account import Account
from broker.quotes import Quotes
from broker.orders import Order
from broker.config import ACCOUNT_NUMBER
from utils.enums import PUT_CALL



def get_put_positions():
    """ 
    Get all open Puts first from Accounts API and later pricing information
    for the symbol via Quotes
    """
    def addmoneyness(row):
        intrinsic = round(max(row['strikePrice'] - row['underlyingPrice'], 0),2)
        extrinsic = round(row['lastPrice'] - intrinsic, 2)
        ITM = np.where(row["strikePrice"] > row["underlyingPrice"] , 'Y', 'N')
        return intrinsic, extrinsic, ITM
   
    # Get All Open Positions
    res = get_account_positions()

    # Filter for puts
    isPut= res['option_type'] == PUT_CALL.PUT.value
    res_puts = res[isPut]

    # Get Quotes for open puts
    df = __get_option_position_details(res_puts)

    resDF = pd.DataFrame()
    resDF[['intrinsic','extrinsic','ITM']] = df.apply(addmoneyness, axis=1 ,result_type="expand")
    df = df.join(resDF)

    if not df.empty:
        df = df.drop(['option_type','type'], axis=1)

    return df


def get_call_positions():
    """ 
    Get all open Calls first from Accounts API and later pricing information
    for the symbol via Qouotes
    """

    def addmoneyness(row):
        intrinsic = round(max(row['underlyingPrice'] - row['strikePrice'], 0), 2)
        extrinsic = round(row['lastPrice'] - intrinsic, 2)
        ITM = np.where(row["strikePrice"] < row["underlyingPrice"] , 'Y', 'N')
        return intrinsic, extrinsic, ITM

    # Get All Open Positions
    res = get_account_positions()

    # Filter for calls
    isCall = res['option_type'] == PUT_CALL.CALL.value  
    res_calls = res[isCall]

    # Get Quotes for open calls
    df = __get_option_position_details(res_calls)

    resDF = pd.DataFrame()
    resDF[['intrinsic','extrinsic','ITM']] = df.apply(addmoneyness, axis=1 ,result_type="expand")
    df = df.join(resDF)

    if not df.empty:
        df = df.drop(['option_type','type'], axis=1)

    return df

def get_stock_positions():
    """ 
    Get all open Calls first from Accounts API and later pricing information
    for the symbol via Qouotes
    """

    # Get All Open Positions
    res = get_account_positions()

    # Filter for calls
    isEquity = res['type'] == "EQUITY"  
    res_equity = res[isEquity]

    # Get Quotes for open calls
    df = __get_stock_position_details(res_equity)
    if not df.empty:
        df = df.drop(['option_type','type'], axis=1)
    return df


def get_account_positions():
    """ 
    Get open positions for a given account
    """
    account = Account()
    logging.debug(" Getting positions")
    return account.get_positionsDF(account=ACCOUNT_NUMBER)
    

def __get_option_position_details(df):
    """ 
    Get pricing info or the symbol via Quotes
    """

    def get_quotes(row):
        """ 
        Invoke quotes for passed symbol
        """ 

        quotes = Quotes()
        res = quotes.get_quotes(row['symbol'])
        return res['underlyingPrice'], res['strikePrice'], res['lastPrice']

    # Invoke getQuotesForSymbol for each symbol
    res = pd.DataFrame()
    res[['underlyingPrice','strikePrice','lastPrice']] = df.apply(get_quotes, axis=1 ,result_type="expand")
    df = df.join(res)
    return df


def __get_stock_position_details(df):
    """ 
    Get pricing info or the symbol via Quotes
    """

    def get_quotes(row):
        """ 
        Invoke quotes for passed symbol
        """ 

        quotes = Quotes()
        res = quotes.get_quotes(row['symbol'])
        return res['mark']

    # Invoke getQuotesForSymbol for each symbol
    res = pd.DataFrame()
    res['mark'] = df.apply(get_quotes, axis=1)
    df = df.join(res)
    return df
