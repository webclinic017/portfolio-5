import pandas as pd

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_table import DataTable

from app import app
from .views import screener_view
from utils.constants import screener_list
from utils.constants import style_cell, style_header, style_data_conditional

from service.option_strategies import (
    watchlist_income,
    short_put,
    short_call,
    long_put,
    long_call
)

layout = screener_view.layout

@app.callback(
    [Output('screener-output', 'children'),
    Output("screener-message", "is_open"),
    Output("screener-message", "children"),],
    [Input("screener-btn", "n_clicks")],
    [
        State('contract_type', 'value'),
        State('min_expiration_days', 'value'),
        State('max_expiration_days', 'value'),
        State('min_delta', 'value'),
        State('max_delta', 'value'),
        State('premium', 'value'),
        State('moneyness', 'value'),
        State('ticker', 'value'),
        State('ticker_list', 'value'),
    ]
)
def on_button_click(n, contract_type, min_expiration_days, max_expiration_days, min_delta, max_delta, premium,moneyness, ticker, ticker_list):
    if n is None:
        return None, False, ""
    else:
        params = {}
        func = None
   
        if contract_type == "PUT":
            func = short_put
        else:
            func = short_call
            
        if min_expiration_days:
            params['min_expiration_days'] = int(min_expiration_days)
        if max_expiration_days:
            params['max_expiration_days'] = int(max_expiration_days)
        if min_delta:
            params['min_delta'] = float(min_delta)
        if max_delta:
            params['max_delta'] = float(max_delta)
        if premium:
            params['premium'] = premium
        if moneyness:
            params['moneyness'] = moneyness
        
        if ticker:
            tickers=[ticker]
        elif ticker_list:
            tickers = screener_list.get(ticker_list)
        else:
            return None, True, "Enter Ticker or Select Watchlist"

        df = watchlist_income(tickers, params, func)
        if not df.empty:
            df = df.drop(['desired_premium', 'desired_moneyness','desired_min_delta','desired_max_delta','type','open_interest','volume','expiration_type','spread'], axis = 1) 
        
            dt = DataTable(
                    id="table",
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict("records"),
                    page_size=10,
                    sort_action="native",
                    filter_action="native",
                    style_cell=style_cell,
                    style_header=style_header,
                    style_data_conditional=style_data_conditional,
                )
            return dt, False, ""
            
        else:
            return None, True, "No Results Found"