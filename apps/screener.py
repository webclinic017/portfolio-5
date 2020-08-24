import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

from app import app

from utils.constants import screener_list
from service.chart_helper import update_graph

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
                            dbc.Input(
                                type="text", id="screener_ticker", placeholder="",
                            ),
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
            dbc.Alert(id="screener-message", is_open=False,),
            dbc.Spinner(html.Div(id="screener-output")),
        ]
    ),
]

layout = dbc.Container([dbc.Row(TOP_COLUMN), dbc.Row(SEARCH_RESULT),], fluid=True)


@app.callback(
    [
        Output("screener-output", "children"),
        Output("screener-message", "is_open"),
        Output("screener-message", "children"),
    ],
    [Input("screener-btn", "n_clicks")],
    [State("screener_ticker", "value"),],
)
def on_button_click(n, ticker):
    if n is None:
        return None, False, ""
    else:
        if ticker:
            fig, info_text = update_graph(ticker)
            chart = html.Div(
                [dbc.Alert(info_text, color="primary"), dcc.Graph(figure=fig),]
            )
            return chart, False, ""
        else:
            return None, True, "No Results Found"
