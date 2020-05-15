import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
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

form = dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label("Start Date", html_for="example-email-grid"),
                    dbc.Input(
                        type="text",
                        id="start-date",
                        placeholder="Start Date",
                    ),
                ]
            ),
            width=3,
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label("End Date", html_for="example-password-grid"),
                    dbc.Input(
                        type="text",
                        id="end-date",
                        placeholder="End Date",
                    ),
                ]
            ),
            width=3,
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label("Premium", html_for="premium"),
                    dbc.Input(
                        type="text",
                        id="premium",
                        placeholder="Premium",
                    ),
                ]
            ),
            width=3,
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label("Moneyness", html_for="moneyness"),
                    dbc.Input(
                        type="text",
                        id="moneyness",
                        placeholder="Moneyness",
                    ),
                ]
            ),
            width=3,
        ),
    ],
    form=True,
)
layout = html.Div([
    form,
    dbc.Row(
        dbc.Col(dbc.Button("Update", color="primary", outline=True, className="mr-1", id='screener-btn'),)
    ),
    dbc.Row(
        dbc.Spinner(html.Div(id="screener-output")),
    )
])

@app.callback(
    Output('screener-output', 'children'),
    [Input("screener-btn", "n_clicks")],
    [
        State('start-date', 'value'),
        State('end-date', 'value'),
        State('premium', 'value'),
        State('moneyness', 'value'),
    ]
)
def on_button_click(n, start_date, end_date,premium,moneyness):
    if n is None:
        pass
    else:
        params = {
            'moneyness': 2,
            'premium': 2,
            'min_expiration_days': 15,
            'max_expiration_days': 40,
        }

   
        if start_date:
            params['min_expiration_days'] = int(start_date)
        if end_date:
            params['max_expiration_days'] = int(end_date)
        if premium:
            params['premium'] = premium
        if moneyness:
            params['moneyness'] = moneyness

        tickers = ['AAPL', 'MSFT', 'LYFT','CAT', 'DIS']
        

        df = watchlist_income(tickers, params, short_put)
        df = df.drop(['desired_premium', 'moneyness','type','open_interest','volume','expiration_type','days_to_expiration','spread'], axis = 1) 

        return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)