import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_table import DataTable
import pandas as pd

from app import app
from service.account_positions import Account_Positions

positions = Account_Positions()

df_puts = pd.DataFrame()
df_calls = pd.DataFrame()
df_stocks = pd.DataFrame()


# df_puts = positions.get_put_positions()
# df_calls = positions.get_call_positions()
# df_stocks = positions.get_stock_positions()


layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Get Positions",
                    color="primary",
                    className="float-right",
                    id="portfolio-btn",
                ),
            ),
        ),
        dbc.Row(html.H4("PUTS"),),
        dbc.Row([dbc.Col(dbc.Spinner(html.Div(id="puts_table")),)]),
        dbc.Row(html.H4("CALLS"),),
        dbc.Row([dbc.Col(dbc.Spinner(html.Div(id="calls_table")),)]),
        dbc.Row(html.H4("STOCKS"),),
        dbc.Row([dbc.Col(dbc.Spinner(html.Div(id="stocks_table")),)]),
    ]
)


@app.callback(
    [
        Output("puts_table", "children"),
        Output("calls_table", "children"),
        Output("stocks_table", "children"),
    ],
    [
        Input("portfolio-btn", "n_clicks"),
    ]
)
def on_button_click(n):
    if n is None:
        return None, None, None
    else:
        df_puts = positions.get_put_positions()
        df_calls = positions.get_call_positions()
        df_stocks = positions.get_stock_positions()

        return (
            dbc.Table.from_dataframe(df_puts, striped=True, bordered=True),
            dbc.Table.from_dataframe(df_calls, striped=True, bordered=True),
            dbc.Table.from_dataframe(df_stocks, striped=True, bordered=True),
        )

