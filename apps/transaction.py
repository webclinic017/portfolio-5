from datetime import datetime as dt
import pandas as pd
import re
import logging

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_tabulator
from utils.constants import style_cell, style_header, style_data_conditional

from app import app

from service.account_transactions import get_transactions

TOP_COLUMN = dbc.Jumbotron(
    [
        html.H5(children="Transactions"),
        html.Hr(className="my-2"),
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("From Date", className="mr-3",),
                            dbc.Col(
                                dcc.DatePickerSingle(
                                    id="start-date-picker", display_format="YYYY-MM-DD",
                                ),
                            ),
                        ]
                    ),
                    width=2,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("To Date", className="mr-3",),
                            dbc.Col(
                                dcc.DatePickerSingle(
                                    id="end-date-picker", display_format="YYYY-MM-DD",
                                ),
                            ),
                        ]
                    ),
                    width=2,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Ticker", html_for="example-email-grid"),
                            dbc.Input(
                                type="text",
                                id="transaction-ticker",
                                placeholder="symbol",
                            ),
                        ],
                    ),
                    width=2,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Instrument Type", html_for="example-email-grid"),
                            dbc.Select(
                                id="instrument-type",
                                options=[
                                    {"label": "ALL", "value": ""},
                                    {"label": "CALL", "value": "CALL"},
                                    {"label": "PUT", "value": "PUT"},
                                    {"label": "EQUITY", "value": "EQUITY"},
                                    {"label": "ALL OPTIONS", "value": "OPTION"},
                                ],
                            ),
                        ],
                    ),
                    width=2,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Tran Type", html_for="example-email-grid"),
                            dbc.Select(
                                id="tran-type",
                                options=[
                                    {"label": "ALL", "value": ""},
                                    {"label": "SL", "value": "SL"},
                                    {"label": "BY", "value": "BY"},
                                    {"label": "OA", "value": "OA"},
                                ],
                            ),
                        ],
                    ),
                    width=2,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Group By", html_for="example-email-grid"),
                            dbc.Select(
                                id="tran-group",
                                options=[
                                    {"label": "SELECT", "value": ""},
                                    {"label": "Symbol", "value": "S"},
                                    {"label": "Date", "value": "D"},
                                ],
                                value="SELECT",
                            ),
                        ],
                    ),
                    width=2,
                ),
            ],
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Search",
                    color="primary",
                    className="float-right",
                    id="transaction-btn",
                ),
            ),
        ),
    ],
    className="container-fluid",
)

SEARCH_RESULT = [
    dbc.Col(
        [
            dbc.Alert(id="transaction-message", is_open=False,),
            dbc.Spinner(html.Div(id="transaction-output")),
        ]
    ),
]

layout = dbc.Container([dbc.Row(TOP_COLUMN), dbc.Row(SEARCH_RESULT),], fluid=True)


@app.callback(
    [
        Output("transaction-output", "children"),
        Output("transaction-message", "is_open"),
        Output("transaction-message", "children"),
    ],
    [Input("transaction-btn", "n_clicks"),],
    [
        State("start-date-picker", "date"),
        State("end-date-picker", "date"),
        State("transaction-ticker", "value"),
        State("instrument-type", "value"),
        State("tran-type", "value"),
    ],
)
def on_button_click(n, start_date, end_date, ticker, instrument_type, tran_type):
    if n is None:
        return None, False, ""
    else:
        df = get_transactions(start_date, end_date, ticker, instrument_type, tran_type)
        logging.info("instrument_type is %s ", instrument_type)
        if not df.empty:
            sum = round(df["TOTAL PRICE"].sum(), 2)
            sumText = 'Grand Total = "{}"'.format(sum)
            options = { "groupBy": "TICKER", "selectable":1}

            dt = dash_tabulator.DashTabulator(
                id='screener-table',
                columns=[{"id": i, "title": i, "field": i} for i in df.columns],
                data=df.to_dict("records"),
                options=options,
                ),

            return dt, True, sumText
        else:
            return None, True, "No Records found"
