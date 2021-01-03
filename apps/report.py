import logging

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_tabulator

from app import app

from service.account_transactions import get_report

# downloadButtonType
# takes
#       css     => class names
#       text    => Text on the button
#       type    => type of download (csv/ xlsx / pdf, remember to include appropriate 3rd party js libraries)
#       filename => filename prefix defaults to data, will download as filename.type

downloadButtonType = {"css": "btn btn-primary", "text":"Export", "type":"csv"}



TOP_COLUMN = dbc.Jumbotron(
    [
        html.H5(children="Reports"),
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
                    width=3,
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
                    width=3,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Ticker", html_for="example-email-grid"),
                            dbc.Input(
                                type="text",
                                id="report-ticker",
                                placeholder="symbol",
                            ),
                        ],
                    ),
                    width=3,
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
                    width=3,
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "Search",
                        color="primary",
                        className="float-right",
                        id="report-btn",
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
            dbc.Alert(id="report-message", is_open=False,),
            dbc.Spinner(html.Div(id="report-output")),
        ]
    ),
]

layout = dbc.Container([dbc.Row(TOP_COLUMN), dbc.Row(SEARCH_RESULT),], fluid=True)

@app.callback(
    [
        Output("report-output", "children"),
        Output("report-message", "is_open"),
        Output("report-message", "children"),
    ],
    [Input("report-btn", "n_clicks"),],
    [
        State("start-date-picker", "date"),
        State("end-date-picker", "date"),
        State("report-ticker", "value"),
        State("instrument-type", "value"),
    ],
)
def on_search(n, start_date, end_date, ticker, instrument_type):
    if n is None:
        return None, False, ""
    else:

        df = get_report(start_date, end_date, ticker, instrument_type)
        if not df.empty:
 
            columns = [
                {"title": "DATE", "field": "DATE"},
                {"title": "EXPIRATION DATE", "field": "EXPIRATION_DATE"},
                {"title": "TOTAL PRICE", "field": "TOTAL_PRICE", "topCalc":"sum", "topCalcParams":{"precision":2,}},
                {"title": "PRICE", "field": "PRICE"},
                {"title": "CLOSE PRICE", "field": "CLOSE_PRICE"},
                {"title": "SYMBOL", "field": "SYMBOL"},
                {"title": "QTY", "field": "QTY"},
                {"title": "TICKER", "field": "TICKER"},
            ]

            dt = (
                dash_tabulator.DashTabulator(
                    id="report-table",
                    columns=columns,
                    data=df.to_dict("records"),
                    downloadButtonType=downloadButtonType,
                ),
            )

            return dt, True,""
        else:
            return None, True, "No Records found"
