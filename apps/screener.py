from datetime import datetime as dt
import pandas as pd
import re
import logging

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from utils.constants import screener_list
from dash.dependencies import Input, Output, State

from app import app

from service.account_transactions import get_transactions

TOP_COLUMN = dbc.Jumbotron(
    [
        html.H5(children="Screener"),
        html.Hr(className="my-2"),
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("WatchList"),
                            dbc.Select(
                                options=[
                                    {"label": i, "value": i} for i in screener_list
                                ],
                                value="",
                                id="screener_ticker_list",
                            ),
                        ]
                    ),
                    width=3,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Ticker", html_for="example-email-grid"),
                            dbc.Input(type="text", id="screener_ticker", placeholder="",),
                        ]
                    ),
                    width=3,
                ),
            ],
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
    [
        Output("screener-output", "children"),
        Output("screener-message", "is_open"),
        Output("screener-message", "children"),
    ],
    [Input("screener-btn", "n_clicks")],
    [
        State("screener_ticker", "value"),
        State("screener_ticker_list", "value"),
    ],
)
def on_button_click(n, ticker, ticker_list):

    return None, None, False