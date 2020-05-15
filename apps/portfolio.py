import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_table import DataTable
import pandas as pd

from app import app
from .views import portfolio_view
from service.account_positions import get_account_positions

layout = portfolio_view.layout

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