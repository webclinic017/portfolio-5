import requests
import datetime
import pandas as pd
import broker.utils
from .base import Base
from .urls import GET_PRICE_HISTORY
from utils.functions import date_from_milliseconds

class History(Base):

    """ A class for searching for History. """
    def __init__(self, **query):
        Base.__init__(self)

    
    def get_price_history(self, symbol=None, periodType=None, period=None, startDate=None, endDate=None,
                          frequencyType=None, frequency=None,  needExtendedHoursData=None):
        '''
            STILL BUILDING

            NAME: symbol
            DESC: The ticker symbol to request data for. 
            TYPE: String

            NAME: periodType
            DESC: The type of period to show. Valid values are day, month, year, or ytd (year to date). Default is day.
            TYPE: String

            NAME: period
            DESC: The number of periods to show.
            TYPE: Integer

            NAME: startDate
            DESC: Start date as milliseconds since epoch.
            TYPE: Integer

            NAME: endDate
            DESC: End date as milliseconds since epoch.
            TYPE: Integer

            NAME: frequencyType
            DESC: The type of frequency with which a new candle is formed.
            TYPE: String

            NAME: frequency
            DESC: The number of the frequencyType to be included in each candle.
            TYPE: Integer

            NAME: needExtendedHoursData
            DESC: True to return extended hours data, false for regular market hours only. Default is true
            TYPE: Boolean

            Documentation Link: https://developer.tdameritrade.com/price-history/apis/get/marketdata/%7Bsymbol%7D/pricehistory
            

        '''

        # Validator function for get_price_history
        def validate(data):

            # Valid periods by periodType
            valid_periods = {
                'day': [1, 2, 3, 4, 5, 10],
                'month': [1, 2, 3, 6],
                'year': [1, 2, 3, 5, 10, 15, 20],
                'ytd': [1],
            }

            # Valid frequencyType by period
            valid_frequency_types = {
                'day': ['minute'],
                'month': ['daily', 'weekly'],
                'year': ['daily', 'weekly', 'monthly'],
                'ytd': ['daily', 'weekly'],
            }

            # Valid frequency by frequencyType
            valid_frequencies = {
                'minute': [1, 5, 10, 15, 30],
                'daily': [1],
                'weekly': [1],
                'monthly': [1]
            }

            # check the startDate and endDate types
            if isinstance(data['startDate'], datetime.datetime):
                data['startDate'] = broker.utils.milliseconds_since_epoch(data['startDate'])
            elif not (isinstance(data['startDate'], int) and (data['startDate'] is not None)):
                raise TypeError('startDate must be a datetime.datetime or an int')

            if isinstance(data['endDate'], datetime.datetime):
                data['endDate'] = broker.utils.milliseconds_since_epoch(data['endDate'])
            elif not (isinstance(data['endDate'], int) and (data['endDate'] is not None)):
                raise TypeError('endDate must be a datetime.datetime or an int')

            # check data to confirm that either period or date range is provided
            if (data['startDate'] and data['endDate'] and not data['period']) or (not data['startDate'] and not data['endDate'] and data['period']):

                # Validate periodType
                if data['periodType'] not in valid_periods.keys():
                    print('Period Type: {} is not valid. Valid values are {}'.format(
                        data['periodType'], valid_periods.keys()))
                    raise ValueError('Invalid Value')

                # Validate period
                if data['period'] and data['period'] not in valid_periods[data['periodType']]:
                    print('Period: {} is not valid. Valid values are {}'.format(
                        data['period'], valid_periods[data['periodType']]))
                    raise ValueError('Invalid Value')

                # Validate frequencyType by frenquency
                if data['frequencyType'] not in valid_frequencies.keys():
                    print('frequencyType: {} is not valid. Valid values are {}'.format(
                        data['frequencyType'],  valid_frequencies.keys()))
                    raise ValueError('Invalid Value')

                # Validate frequencyType by periodType
                if data['frequencyType'] not in valid_frequency_types[data['periodType']]:
                    print('frequencyType: {} is not valid. Valid values for period: {} are {}'.format(
                        data['frequencyType'], data['periodType'], valid_frequency_types[data['periodType']]))
                    raise ValueError('Invalid Value')

                # Validate periodType
                if data['frequency'] not in valid_frequencies[data['frequencyType']]:
                    print('frequency: {} is not valid. Valid values are {}'.format(
                        data['frequency'], valid_frequencies[data['frequencyType']]))
                    raise ValueError('Invalid Value')

                # TODO Validate startDate and endDate

                # Recompute payload dictionary and remove any None values
                return({k: v for k, v in data.items() if v is not None})

            else:
                print('Either startDate/endDate or period must be provided exclusively.')
                raise ValueError('Invalid Value')

        # build the params dictionary
        data = {'apikey': self.config['consumer_id'],
                'period': period,
                'periodType': periodType,
                'startDate': startDate,
                'endDate': endDate,
                'frequency': frequency,
                'frequencyType': frequencyType,
                'needExtendedHoursData': needExtendedHoursData}

        # define the endpoint
        endpoint = GET_PRICE_HISTORY.format(symbol=symbol)

        # validate the data
        data = validate(data)

        # build the url
        url = self.api_endpoint(endpoint)

        self._data = self._api_response(url=url, params=data, verify=True)

        # return the response of the get request.
        return self._data['candles']


    def get_price_historyDF(self, symbol=None, periodType=None, period=None, startDate=None, endDate=None,
                          frequencyType=None, frequency=None,  needExtendedHoursData=None):
        res = self.get_price_history(symbol=symbol, periodType=periodType, period=period, startDate=startDate, endDate=endDate,
                          frequencyType=frequencyType, frequency=frequency,  needExtendedHoursData=needExtendedHoursData)
        
        df = pd.json_normalize(res)
        df ['datetime'] =  df ['datetime'].apply(date_from_milliseconds) 
        return df



