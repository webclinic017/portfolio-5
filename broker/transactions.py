import pandas as pd
from .base import Base


class Transaction(Base):

    """ A class for searching for an account. """

    def __init__(self, **query):
        Base.__init__(self)

    def get_transactions(self, account=None, transaction_type=None, symbol=None,
                         start_date=None, end_date=None, transaction_id=None):
        '''
            Serves as the mechanism to make a request to the "Get Transactions" and "Get Transaction" Endpoint. 
            If one `transaction_id` is provided a "Get Transaction" request will be made and if it is not provided
            then a "Get Transactions" request will be made.

            Documentation Link: https://developer.tdameritrade.com/transaction-history/apis

            NAME: account
            DESC: The account number you wish to recieve transactions for.
            TYPE: String

            NAME: transaction_type
            DESC: The type of transaction. Only transactions with the specified type will be returned. Valid
                  values are the following: ALL, TRADE, BUY_ONLY, SELL_ONLY, CASH_IN_OR_CASH_OUT, CHECKING,
                                            DIVIDEND, INTEREST, OTHER, ADVISOR_FEES
            TYPE: String

            NAME: symbol
            DESC: The symbol in the specified transaction. Only transactions with the specified 
                  symbol will be returned.
            TYPE: String

            NAME: start_date
            DESC: Only transactions after the Start Date will be returned. Note: The maximum date range is 
                  one year. Valid ISO-8601 formats are: yyyy-MM-dd.
            TYPE: String

            NAME: end_date
            DESC: Only transactions before the End Date will be returned. Note: The maximum date range is 
                  one year. Valid ISO-8601 formats are: yyyy-MM-dd.
            TYPE: String

            NAME: transaction_id
            DESC: The transaction ID you wish to search. If this is specifed a "Get Transaction" request is
                  made. Should only be used if you wish to return one transaction.
            TYPE: String

        '''

        # default to a "Get Transaction" Request if anything else is passed through along with the transaction_id.
        if transaction_id is not None:
            account = None
            transaction_type = None,
            start_date = None,
            end_date = None

        # if the request type they made isn't valid print an error and return nothing.
        else:

            if transaction_type not in ['ALL', 'TRADE', 'BUY_ONLY', 'SELL_ONLY', 'CASH_IN_OR_CASH_OUT', 'CHECKING', 'DIVIDEND', 'INTEREST', 'OTHER', 'ADVISOR_FEES']:
                print('The type of transaction type you specified is not valid.')
                return False

        # if transaction_id is not none, it means we need to make a request to the get_transaction endpoint.
        if transaction_id:

            # define the endpoint
            endpoint = '/accounts/{}/transactions/{}'.format(
                account, transaction_id)

            # build the url
            url = self.api_endpoint(endpoint)

            self._data = self._api_response(url=url, params=None, verify=True)

            # return the response of the get request.
            return self._data

        # if it isn't then we need to make a request to the get_transactions endpoint.
        else:

            # build the params dictionary
            data = {'type': transaction_type,
                    'symbol': symbol,
                    'startDate': start_date,
                    'endDate': end_date}

            # define the endpoint
            endpoint = '/accounts/{}/transactions'.format(account)

            # build the url
            url = self.api_endpoint(endpoint)

            self._data = self._api_response(url=url, params=data, verify=True)

            # return the response of the get request.
            return self._data

    
    def get_transactionsDF(self, account=None, transaction_type=None, symbol=None,
                         start_date=None, end_date=None, transaction_id=None):
        '''get transaction information as Dataframe'''
        return pd.json_normalize(self.get_transactions(account=account, transaction_type=transaction_type, symbol=symbol, start_date=start_date, end_date=end_date))

