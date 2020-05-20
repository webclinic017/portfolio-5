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
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Option Type", html_for="example-email-grid"),
                        dbc.Select(
                            id="option-type",
                            options=[
                                {"label": "ALL", "value": ''},
                                {"label": "CALL", "value": 'CALL'},
                                {"label": "PUT", "value": 'PUT'},
                            ],
                            value="ALL",
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
                                {"label": "SELECT", "value": ""},
                                {"label": "SL", "value": 'SL'},
                                {"label": "BY", "value": 'BY'},
                                {"label": "OA", "value": 'OA'},
                            ],
                            value="SELECT",
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
                                {"label": "Symbol", "value": 'S'},
                                {"label": "Date", "value": 'D'},
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
        html.Div(id='sum')
    ),
    dbc.Row(
        dbc.Spinner(html.Div(id="transaction-output")),className="mt-3",
    )
])

@app.callback(
    [Output('transaction-output', 'children'),
    Output('transaction-message', 'is_open'),
    Output('sum', 'children'),],
    [
        Input("transaction-btn", "n_clicks"),
        Input("start-date-picker", "date"),
        Input("end-date-picker", "date"),
    ],
    [
        State('transaction-ticker', 'value'),
        State("option-type", "value"),
        State("tran-type", "value"),
    ]
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
                id='table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                # table interactivity
                editable=True,
                # filtering=True,
                sort_action="native",
                sort_mode="multi",
                row_selectable="multi",
                style_table={
                    'overflowY': 'scroll',
                    'width': '100%',
                    'minWidth': '100%',
                },
                style_cell={
                    'fontFamily': 'sans-serif',
                    'textAlign': 'center',
                    'height': '40px',
                    'fontWeight': '400',
                    'padding': '10px 10px',
                    'whiteSpace': 'inherit',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                },
                # style header
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