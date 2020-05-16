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

layout = layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("From Date", html_for="example-email-grid", className="mr-3"),
                        dbc.Col(
                            dcc.DatePickerSingle(
                                id='start-date-picker',
                                display_format='YYYY-MM-DD',
                            ), 
                        ) ,
                    ]
                ),
                width=2,
            ),
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("To Date", html_for="example-email-grid", className="mr-3"),
                        dbc.Col(
                            dcc.DatePickerSingle(
                                id='end-date-picker',
                                display_format='YYYY-MM-DD',
                            ), 
                        ) ,
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
        ],
    ),
    dbc.Row(
        dbc.Col(dbc.Button("Search", color="primary", outline=True, className="mr-1", id='transaction-btn'),),
    ),
    dbc.Row(
        dbc.Alert(
                "No Records returned the matching criteria",
                id="transaction-message",
                is_open=False,
                duration=2000,
                color="danger"
            ), className="mt-3"
    ),
    dbc.Row(
        dbc.Spinner(html.Div(id="transaction-output")),className="mt-3",
    )
])

@app.callback(
    [Output('transaction-output', 'children'),
    Output('transaction-message', 'is_open'),],
    [Input("transaction-btn", "n_clicks"),
    Input("start-date-picker", "date"),
    Input("end-date-picker", "date")],
    [
        State('transaction-ticker', 'value'),
    ]
)
def on_button_click(n, start_date, end_date, ticker):
    if n is None:
        return None, False
    else:
        df = get_transactions(start_date, end_date, ticker)
        if not df.empty:
            return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True), False
        else:
            return None, False