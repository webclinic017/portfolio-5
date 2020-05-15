import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_table import DataTable
import pandas as pd

from app import app

from service.account_positions import get_account_positions

layout = html.Div([
     dbc.Row(
        dbc.Col(dbc.Button("Get Portfolio", color="primary", outline=True, className="mr-1", id='portfolio-btn'),)
    ),
    dbc.Spinner(html.Div(id="portfolio-output")),
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