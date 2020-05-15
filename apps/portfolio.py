import dash
import dash_html_components as html

from dash.dependencies import Input, Output, State
from dash_table import DataTable
import pandas as pd

from app import app

from service.account_positions import get_account_positions

layout = html.Div([
    html.Button(
        ['Update'],
        id='portfolio-btn'
    ),
    html.Div(id="portfolio-content", className='w3-row app-datatable',),
])

@app.callback(
    Output('portfolio-content', 'children'),
    [Input("portfolio-btn", "n_clicks")]
)
def updateTable(n_clicks):
    df = get_account_positions()

    return DataTable(
        id='datatable-chain',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
        filter_action='native',
        sort_action='native',
        style_cell = {
                'font-family': 'Tahoma',
                'font-size': '1 em',
                'text-align': 'center'
            },
    )