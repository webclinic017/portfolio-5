import dash
import dash_html_components as html

from dash.dependencies import Input, Output, State
from dash_table import DataTable
import pandas as pd

from app import app

from service.option_strategies import (
    watchlist_income,
    short_put,
    short_call,
    long_put,
    long_call
)

layout = html.Div([
    html.Button(
        ['Update'],
        id='screener-btn'
    ),
    html.Div(id="screener-content", className='w3-row app-datatable',),
])

@app.callback(
    Output('screener-content', 'children'),
    [Input("screener-btn", "n_clicks")]
)
def updateTable(n_clicks):
    tickers = ['AAPL', 'MSFT', 'LYFT','CAT', 'DIS']

    params = {
        'moneyness': 2,
        'premium': 2,
        'min_expiration_days': 15,
        'max_expiration_days': 40,
    }

    df = watchlist_income(tickers, params, short_put)
    df = df.drop(['desired_premium', 'moneyness','type','open_interest','volume','expiration_type','days_to_expiration','spread'], axis = 1) 

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