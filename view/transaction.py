import logging

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_tabulator

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
            [
                dbc.Col(
                        dbc.Checklist(
                            options=[
                                {"label": "Group by ticker", "value": 1},
                            ],
                            value=[],
                            id="is_group",
                            switch=True,
                            className="float-right",
                        ),
                        width=10,
                    ),
                dbc.Col(
                    dbc.Button(
                        "Search",
                        color="primary",
                        className="float-right",
                        id="transaction-btn",
                    ),
                ),
            ],
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
        State("is_group", "value"),
    ],
)
def on_button_click(n, start_date, end_date, ticker, instrument_type, tran_type, is_group):
    if n is None:
        return None, False, ""
    else:

        df = get_transactions(start_date, end_date, ticker, instrument_type, tran_type)
        logging.info("instrument_type is %s ", instrument_type)
        if not df.empty:
            sumText = 'Grand Total = "{}"'.format(round(df["TOTAL_PRICE"].sum(), 2))
            options = {"selectable": 1}
            # Padd groupBy option to the Tabulator component to group at Ticker level
            if is_group:
                options["groupBy"] = "TICKER"

            columns = [
                {"title": "DATE", "field": "DATE"},
                {"title": "TOTAL PRICE", "field": "TOTAL_PRICE", "topCalc":"sum", "topCalcParams":{"precision":2,}},
                {"title": "SYMBOL", "field": "SYMBOL"},
                {"title": "TRAN TYPE", "field": "TRAN_TYPE"},
                {"title": "POSITION", "field": "POSITION"},
                {"title": "QTY", "field": "QTY"},
                {"title": "PRICE", "field": "PRICE"},
                {"title": "TICKER", "field": "TICKER"},
                {"title": "TYPE", "field": "TYPE"},
                {"title": "OPTION TYPE", "field": "OPTION_TYPE"},
            ]

            dt = (
                dash_tabulator.DashTabulator(
                    id="screener-table",
                    columns=columns,
                    data=df.to_dict("records"),
                    options=options,
                ),
            )

            return dt, True, sumText
        else:
            return None, True, "No Records found"
