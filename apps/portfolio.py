import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_table import DataTable
import pandas as pd

from app import app
from service.account_positions import Account_Positions

positions = Account_Positions()

df_puts = positions.get_put_positions()
df_calls = positions.get_call_positions()
df_stocks = positions.get_stock_positions()


layout = html.Div([
    dbc.Row(
        html.H4("PUTS"),
    ),
    dbc.Row(
        dbc.Table.from_dataframe(df_puts, striped=True, bordered=True, hover=True, className="mt-3")
    ),
    dbc.Row(
        html.H4("CALLS"),
    ),
    dbc.Row(
        dbc.Table.from_dataframe(df_calls, striped=True, bordered=True, hover=True, className="mt-3")
    ),
    dbc.Row(
        html.H4("STOCKS"),
    ),
    dbc.Row(
        dbc.Table.from_dataframe(df_stocks, striped=True, bordered=True, hover=True, className="mt-3")
    ),
])