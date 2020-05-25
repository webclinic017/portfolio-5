import pandas as pd

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_table import DataTable

from app import app
from utils.constants import screener_list
from utils.constants import style_cell, style_header, style_data_conditional

from service.option_strategies import (
    watchlist_income,
    short_put,
    short_call,
    long_put,
    long_call
)

TOP_COLUMN = dbc.Jumbotron(
    [
        html.H5(children="Income Finder"),
        html.Hr(className="my-2"),
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Choose one"),
                            dbc.RadioItems(
                                options=[
                                    {"label": "SECURED PUT", "value": "PUT"},
                                    {"label": "COVERED CALL", "value": "CALL"},
                                ],
                                value="PUT",
                                id="contract_type",
                                inline=True,
                            ),
                        ]
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("WatchList"),
                            dbc.Select(
                                options=[
                                    {"label": i, "value": i} for i in screener_list
                                ],
                                value="",
                                id="ticker_list",
                            ),
                        ]
                    ),
                    width=3,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Ticker", html_for="example-email-grid"),
                            dbc.Input(type="text", id="ticker", placeholder="",),
                        ]
                    ),
                    width=3,
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Min Exp Days", html_for="example-email-grid"),
                            dbc.Input(
                                type="text", id="min_expiration_days", placeholder="15",
                            ),
                        ]
                    ),
                    width=2,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Max Exp Days", html_for="example-password-grid"),
                            dbc.Input(
                                type="text", id="max_expiration_days", placeholder="45",
                            ),
                        ]
                    ),
                    width=2,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Min Delta", html_for="example-email-grid"),
                            dbc.Input(type="text", id="min_delta", placeholder="0.25",),
                        ]
                    ),
                    width=2,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Max Delta", html_for="example-email-grid"),
                            dbc.Input(type="text", id="max_delta", placeholder="0.35",),
                        ]
                    ),
                    width=2,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Premium %", html_for="premium"),
                            dbc.Input(type="text", id="premium", placeholder="2",),
                        ]
                    ),
                    width=2,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Discount/Gain %", html_for="moneyness"),
                            dbc.Input(type="text", id="moneyness", placeholder="5",),
                        ]
                    ),
                    width=2,
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Search",
                    color="primary",
                    className="float-right",
                    id="screener-btn",
                ),
            ),
        ),
    ],
    className="container-fluid",
)

SEARCH_RESULT = [
    dbc.Col(
        [
            html.Div(
                dbc.Alert(
                    id="screener-message",
                    is_open=False,
                    duration=2000,
                    color="danger",
                ),
            ),
            html.Div(dbc.Spinner(html.Div(id="screener-output"))),
        ]       
    ),
]

layout = html.Div(
    [
        dbc.Row(TOP_COLUMN, className="justify-content-center"),
        dbc.Row(SEARCH_RESULT, className="justify-content-center"),
    ],
)

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