import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output


import dash_tabulator

from app import app
from service.account_positions import Account_Positions
from utils.functions import formatter_currency

layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Show Positions",
                    color="primary",
                    className="float-right",
                    id="portfolio-btn",
                ),
            ),
        ),
        dbc.Row(html.H3(dbc.Badge("PUTS", color="primary", className="ml-1"))),
        html.Hr(className="my-2"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div((dbc.Alert(id="put-total", is_open=False,))),
                        dbc.Spinner(html.Div(id="puts_table")),
                    ]
                )
            ]
        ),
        html.P(),
        dbc.Row(html.H3(dbc.Badge("CALLS", color="primary", className="ml-1"))),
        html.Hr(className="my-2"),
        dbc.Row([dbc.Col(dbc.Spinner(html.Div(id="calls_table")),)]),
        html.P(),
        dbc.Row(html.H3(dbc.Badge("STOCKS", color="primary", className="ml-1"))),
        html.Hr(className="my-2"),
        dbc.Row([dbc.Col(dbc.Spinner(html.Div(id="stocks_table")),)]),
    ],
    fluid=True,
)


@app.callback(
    [
        Output("puts_table", "children"),
        Output("calls_table", "children"),
        Output("stocks_table", "children"),
        Output("put-total", "is_open"),
        Output("put-total", "children"),
    ],
    [Input("portfolio-btn", "n_clicks"),],
)
def on_button_click(n):
    if n is not None:
        positions = Account_Positions()

        df_puts = positions.get_put_positions()
        df_calls = positions.get_call_positions()
        df_stocks = positions.get_stock_positions()
        cash_required = formatter_currency(df_puts["COST"].sum())

        calls_dt = (
            dash_tabulator.DashTabulator(
                id="call-table",
                columns=[{"id": i, "title": i, "field": i} for i in df_calls.columns],
                data=df_calls.to_dict("records"),
            ),
        )

        stocks_dt = (
            dash_tabulator.DashTabulator(
                id="put-table",
                columns=[{"id": i, "title": i, "field": i} for i in df_stocks.columns],
                data=df_stocks.to_dict("records"),
            ),
        )

        puts_dt = (
            dash_tabulator.DashTabulator(
                id="put-table",
                columns=[{"id": i, "title": i, "field": i} for i in df_puts.columns],
                data=df_puts.to_dict("records"),
            ),
        )

        return (
            puts_dt,
            calls_dt,
            stocks_dt,
            True,
            f" Cash Required : {cash_required}",
        )
    else:
        return None, None, None, None, None
