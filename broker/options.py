import requests
import datetime
import pandas as pd

import broker.utils
from .base import Base
from .urls import GET_OPTION_CHAIN

class Options(Base):

    """ A class for searching for a options. """
    def __init__(self, **query):
        Base.__init__(self)

    
    def     get_options_chain(self, option_chain=None, args_dictionary=None):
        '''
            Get option chain for an optionable Symbol using one of two methods. Either,
            use the OptionChain object which is a built-in object that allows for easy creation of the
            POST request. Otherwise, can pass through a dictionary of all the arguments needed.

            Documentation Link: https://developer.tdameritrade.com/option-chains/apis/get/marketdata/chains

            NAME: option_chain
            DESC: Represents a single OptionChainObject.
            TYPE: TDAmeritrade.OptionChainObject

            EXAMPLE:

            from td.option_chain import OptionChain

            option_chain_1 = OptionChain(args)

            SessionObject.get_options_chain( option_chain = option_chain_1)

        '''

        # define the endpoint
        endpoint = GET_OPTION_CHAIN

        # build the url
        url = self.api_endpoint(endpoint)

        # Grab the items needed for the request.
        if option_chain is not None:

            # this request requires an API key, so let's add that.
            option_chain.add_chain_key(
                key_name='apikey', key_value=self.config['consumer_id'])

            # take the JSON representation of the string
            data = option_chain._get_query_parameters()

        else:

            # otherwise take the args dictionary.
            data = args_dictionary

        self._data = self._api_response(url=url, params=data, verify=True)

        # return the response of the get request.
        return self._data


    def get_options_chainDF(self, option_chain=None, args_dictionary=None):
        '''get transaction information as Dataframe'''
        return pd.json_normalize(self.get_options_chain(option_chain, args_dictionary))

    def get_put_options_chainDF(self, option_chain=None, args_dictionary=None):
        res = self.get_options_chain(option_chain, args_dictionary)
        '''get transaction information as Dataframe'''
        return pd.json_normalize(res['putExpDateMap'])

    def get_call_options_chainDF(self, option_chain=None, args_dictionary=None):
        '''get transaction information as Dataframe'''
        df = self.get_options_chain(option_chain, args_dictionary)
        return df['callExpDateMap']




