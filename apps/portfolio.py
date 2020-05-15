import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_table import DataTable
import pandas as pd

from app import app
from .views import portfolio_view
from service.account_positions import get_account_positions, get_call_positions, get_put_positions

df_puts = get_put_positions()
df_calls = get_call_positions()

layout = html.Div([
    dbc.Row(
        dbc.Table.from_dataframe(df_puts, striped=True, bordered=True, hover=True)
    ),
    dbc.Row(
        dbc.Table.from_dataframe(df_calls, striped=True, bordered=True, hover=True)
    ),
    dbc.Row(
        dbc.Spinner(html.Div(id="portfolio-output")),className="mt-3",
    )
])

@app.callback(
    Output('portfolio-output', 'children'),
    [Input("portfolio-btn", "n_clicks")]
)
def on_button_click(n):
    if n is None:
        pass
    else:
        df = get_account_positions()
        return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)