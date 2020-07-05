import numpy as np
import pandas as pd
import logging


from broker.account import Account
from broker.quotes import Quotes
from broker.orders import Order
from broker.config import ACCOUNT_NUMBER
from utils.enums import PUT_CALL
from utils.functions import formatter_number_2_digits


class Account_Positions:
    def __init__(self):
        super().__init__()
        self.params_options = {
            "quantity": "QTY",
            "underlying": "TICKER",
            "symbol": "SYMBOL",
            "underlyingPrice": "TICKER PRICE",
            "strikePrice": "STRIKE PRICE",
            "lastPrice": "OPTION PRICE",
            "intrinsic": "INTRINSIC",
            "extrinsic": "EXTRINSIC",
            "ITM": "ITM",
            "theta": "THETA",
            "cost_price": "PURCHASE PRICE"
        }

        self.params_stocks = {
            "quantity": "QTY",
            "underlying": "TICKER",
            "mark": "TICKER PRICE",
        }

        # Get All Open Positions
        self.res = pd.DataFrame()

    def get_put_positions(self):
        """ 
        Get all open Puts first from Accounts API and later pricing information
        for the symbol via Quotes
        """

        def addmoneyness(row):
            intrinsic = round(max(row["strikePrice"] - row["underlyingPrice"], 0), 2)
            extrinsic = round(row["lastPrice"] - intrinsic, 2)
            ITM = np.where(row["strikePrice"] > row["underlyingPrice"], "Y", "N")
            return intrinsic, extrinsic, ITM

        res = self.get_account_positions()
        # Filter for puts
        isPut = res["option_type"] == PUT_CALL.PUT.value
        res_puts = res[isPut]

        # Get Quotes for open puts
        df = self.__get_option_pricing(res_puts)

        resDF = pd.DataFrame()
        resDF[["intrinsic", "extrinsic", "ITM"]] = df.apply(
            addmoneyness, axis=1, result_type="expand"
        )
        df = df.join(resDF)

        if not df.empty:
            df = df.drop(["option_type", "type"], axis=1)
            df = df.rename(columns=self.params_options)

        # Add liquidity for Puts if assigned
        df["COST"] = df["STRIKE PRICE"] * df["QTY"] * 100

        return df

    def get_call_positions(self):
        """ 
        Get all open Calls first from Accounts API and later pricing information
        for the symbol via Qouotes
        """

        def addmoneyness(row):
            intrinsic = round(max(row["underlyingPrice"] - row["strikePrice"], 0), 2)
            extrinsic = round(row["lastPrice"] - intrinsic, 2)
            ITM = np.where(row["strikePrice"] < row["underlyingPrice"], "Y", "N")
            return intrinsic, extrinsic, ITM

        res = self.get_account_positions()

        # Filter for calls
        isCall = res["option_type"] == PUT_CALL.CALL.value
        res_calls = res[isCall]

        # Get Quotes for open calls
        df = self.__get_option_pricing(res_calls)

        resDF = pd.DataFrame()
        resDF[["intrinsic", "extrinsic", "ITM"]] = df.apply(
            addmoneyness, axis=1, result_type="expand"
        )
        df = df.join(resDF)

        if not df.empty:
            df = df.drop(["option_type", "type"], axis=1)
            df = df.rename(columns=self.params_options)

        return df

    def get_stock_positions(self):
        """ 
        Get all open Calls first from Accounts API and later pricing information
        for the symbol via Qouotes
        """

        res = self.get_account_positions()

        # Filter for calls
        isEquity = res["type"] == "EQUITY"
        res_equity = res[isEquity]

        # Get Quotes for open calls
        df = self.__get_stock_pricing(res_equity)
        if not df.empty:
            df = df.drop(["option_type", "type", "symbol"], axis=1)
            df = df.rename(columns=self.params_stocks)

        return df

    def get_account_positions(self):
        """ 
        Get open positions for a given account
        """

        if self.res.empty:
            account = Account()
            logging.debug(" Getting positions")
            self.res = account.get_positionsDF(account=ACCOUNT_NUMBER)

        return self.res

    def __get_option_pricing(self, df):
        """ 
        Get pricing info or the symbol via Quotes
        """

        def get_quotes(row):
            """ 
            Invoke quotes for passed symbol
            """

            quotes = Quotes()
            res = quotes.get_quotes(row["symbol"])
            return (
                res["underlyingPrice"],
                res["strikePrice"],
                res["lastPrice"],
                res["theta"],
            )

        # Invoke getQuotesForSymbol for each symbol
        res = pd.DataFrame()
        res[["underlyingPrice", "strikePrice", "lastPrice", "theta"]] = df.apply(
            get_quotes, axis=1, result_type="expand"
        )
        res["theta"] = res["theta"].apply(formatter_number_2_digits)
        df = df.join(res)
        return df

    def __get_stock_pricing(self, df):
        """ 
        Get pricing info or the symbol via Quotes
        """

        def get_quotes(row):
            """ 
            Invoke quotes for passed symbol
            """

            quotes = Quotes()
            res = quotes.get_quotes(row["symbol"])
            return res["mark"]

        # Invoke getQuotesForSymbol for each symbol
        res = pd.DataFrame()
        res["mark"] = df.apply(get_quotes, axis=1)
        df = df.join(res)
        return df
