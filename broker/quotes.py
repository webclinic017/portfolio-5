import requests
import pandas as pd
from .base import Base
from .urls import GET_QUOTES

class Quotes(Base):

    """ A class for searching for an account. """
    def __init__(self, **query):
        Base.__init__(self)

    
    def get_quotes(self, instruments=None):
        '''

            Serves as the mechanism to make a request to the Get Quote and Get Quotes Endpoint.
            If one item is provided a Get Quote request will be made and if more than one item
            is provided then a Get Quotes request will be made.

            Documentation Link: https://developer.tdameritrade.com/quotes/apis

            NAME: instruments
            DESC: A list of different financial instruments.
            TYPE: List

            EXAMPLES:

            SessionObject.get_quotes(instruments = ['MSFT'])
            SessionObject.get_quotes(instruments = ['MSFT','SQ'])

        '''

        # because we have a list argument, prep it for the request.
        instruments = self.prepare_arguments_list(parameter_list=instruments)

        # build the params dictionary
        data = {'apikey': self.config['consumer_id'],
                'symbol': instruments}

        # define the endpoint
        endpoint = GET_QUOTES

        # build the url
        url = self.api_endpoint(endpoint)

        self._data = self._api_response(url=url, params=data, verify=True)

        # return the response of the get request.
        return self._data[instruments]
        
    def get_quotesDF(self, instruments=None):
        '''get transaction information as Dataframe'''
        return pd.json_normalize(self.get_quotes(instruments=instruments))


