from datetime import datetime as dt
import pandas as pd
import re

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash_table import DataTable

from app import app

from service.account_transactions import get_transactions

LEFT_COLUMN = dbc.Jumbotron(
    [
        html.H4(children="Transactions"),
        html.Hr(className="my-2"),
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                "From Date",
                                html_for="example-email-grid",
                                className="mr-3",
                            ),
                            dbc.Col(
                                dcc.DatePickerSingle(
                                    id="start-date-picker", display_format="YYYY-MM-DD",
                                ),
                            ),
                        ]
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                "To Date",
                                html_for="example-email-grid",
                                className="mr-3",
                            ),
                            dbc.Col(
                                dcc.DatePickerSingle(
                                    id="end-date-picker", display_format="YYYY-MM-DD",
                                ),
                            ),
                        ]
                    ),
                    width=6,
                ),
            ],
        ),
        dbc.Row(
            [
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
                    width=6,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Option Type", html_for="example-email-grid"),
                            dbc.Select(
                                id="option-type",
                                options=[
                                    {"label": "ALL", "value": ""},
                                    {"label": "CALL", "value": "CALL"},
                                    {"label": "PUT", "value": "PUT"},
                                ],
                            ),
                        ],
                    ),
                    width=6,
                ),
            ],
        ),
        dbc.Row(
            [
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
                    width=6,
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
                    width=6,
                ),
            ],
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Search",
                    color="primary",
                    outline=True,
                    className="float-right",
                    id="transaction-btn",
                ),
            ),
        ),
    ],
)

SEARCH_RESULT = [
    dbc.Row(
        dbc.Alert(
            "No Records returned the matching criteria",
            id="transaction-message",
            is_open=False,
            duration=2000,
            color="danger",
        ),
        className="mt-3",
    ),
    dbc.Row(html.Div(id="sum")),
    dbc.Row(dbc.Spinner(html.Div(id="transaction-output")), className="mt-3",),
]

layout = html.Div(
    [dbc.Row([dbc.Col(LEFT_COLUMN, width=3, className="px-3"), dbc.Col(SEARCH_RESULT, width=9, className="px-3"), ],),],
)


@app.callback(
    [
        Output("transaction-output", "children"),
        Output("transaction-message", "is_open"),
        Output("sum", "children"),
    ],
    [
        Input("transaction-btn", "n_clicks"),
        Input("start-date-picker", "date"),
        Input("end-date-picker", "date"),
    ],
    [
        State("transaction-ticker", "value"),
        State("option-type", "value"),
        State("tran-type", "value"),
    ],
)
def on_button_click(n, start_date, end_date, ticker, option_type, tran_type):
    if n is None:
        return None, False, ""
    else:
        df = get_transactions(start_date, end_date, ticker, option_type, tran_type)
        if not df.empty:
            sum = round(df["TOTAL PRICE"].sum(), 2)
            sumText = 'Grand Total = "{}"'.format(sum)
            dt = DataTable(
                id="table",
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict("records"),
                # table interactivity
                # filtering=True,
                sort_action="native",
                style_cell={
                    'padding': '15px',
                    'width': 'auto',
                    'textAlign': 'center',
                    'fontFamily': 'sans-serif',
                },
                 style_header={
                    'fontWeight': 'bold',
                    'backgroundColor': 'white',
                },
                style_data_conditional=[
                    {
                        # stripped rows
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    },
                ],

                
            )
            return dt, False, sumText
        else:
            return None, False, ""
