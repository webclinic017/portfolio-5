import requests
from .base import Base
from .urls import SEARCH_INSTRUMENTS

class Search(Base):

    """ A class for searching for a company. """
    def __init__(self, **query):
        Base.__init__(self)
    

    def search_instruments(self, symbol=None, projection='symbol-search'):
        '''
            Search or retrieve instrument data, including fundamental data.

            Documentation Link: https://developer.tdameritrade.com/instruments/apis/get/instruments

            NAME: symbol
            DESC: The symbol of the financial instrument you would like to search.
            TYPE: string

            NAME: projection
            DESC: The type of request, default is "symbol-search". The type of request include the following:

                  1. symbol-search
                     Retrieve instrument data of a specific symbol or cusip

                  2. symbol-regex
                     Retrieve instrument data for all symbols matching regex. 
                     Example: symbol=XYZ.* will return all symbols beginning with XYZ

                  3. desc-search
                     Retrieve instrument data for instruments whose description contains 
                     the word supplied. Example: symbol=FakeCompany will return all 
                     instruments with FakeCompany in the description

                  4. desc-regex
                     Search description with full regex support. Example: symbol=XYZ.[A-C] 
                     returns all instruments whose descriptions contain a word beginning 
                     with XYZ followed by a character A through C

                  5. fundamental
                     Returns fundamental data for a single instrument specified by exact symbol.

            TYPE: string

            EXAMPLES:

            SessionObject.search_instrument(symbol = 'XYZ', projection = 'symbol-search')
            SessionObject.search_instrument(symbol = 'XYZ.*', projection = 'symbol-regex')
            SessionObject.search_instrument(symbol = 'FakeCompany', projection = 'desc-search')
            SessionObject.search_instrument(symbol = 'XYZ.[A-C]', projection = 'desc-regex')
            SessionObject.search_instrument(symbol = 'XYZ.[A-C]', projection = 'fundamental')

        '''

        # validate argument
        self.validate_arguments(endpoint='search_instruments',
                                parameter_name='projection', parameter_argument=projection)

        # build the params dictionary
        data = {'apikey': self.config['consumer_id'],
                'symbol': symbol,
                'projection': projection}

        # define the endpoint
        endpoint = SEARCH_INSTRUMENTS

        # build the url
        url = self.api_endpoint(endpoint)

        self._data = self._api_response(url=url, params=data, verify=True)

        # return the response of the get request.
        return self._data

    def get_instruments(self, cusip=None):
        '''
            Get an instrument by CUSIP (Committee on Uniform Securities Identification Procedures) code.

            Documentation Link: https://developer.tdameritrade.com/instruments/apis/get/instruments/%7Bcusip%7D

            NAME: cusip
            DESC: The CUSIP code of a given financial instrument.
            TYPE: string

            EXAMPLES:

            SessionObject.get_instruments(cusip = 'SomeCUSIPNumber')
        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # build the params dictionary
        data = {'apikey': self.config['consumer_id']}

        # define the endpoint
        endpoint = '/instruments'

        # build the url
        url = self.api_endpoint(endpoint) + "/" + cusip

        # return the response of the get request.
        return requests.get(url=url, headers=merged_headers, params=data, verify=True).json()