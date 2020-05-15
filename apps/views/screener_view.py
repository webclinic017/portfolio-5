import dash_html_components as html
import dash_bootstrap_components as dbc

layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Choose one"),
                        dbc.RadioItems(
                            options=[
                                {"label": "SECURED PUT", "value": 'PUT'},
                                {"label": "COVERED CALL", "value": 'CALL'},
                            ],
                            value='PUT',
                            id="contract_type",
                            inline=True,
                        ),
                    ]
                ),
                width=4,
            ),
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Ticker", html_for="example-email-grid"),
                        dbc.Input(
                            type="text",
                            id="ticker",
                            placeholder="symbol",
                        ),
                    ]
                ),
                width=2,
            ),
        ],
    ),
    dbc.Row(
        [
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Min Expiration Days", html_for="example-email-grid"),
                        dbc.Input(
                            type="text",
                            id="min_expiration_days",
                            placeholder="Min",
                        ),
                    ]
                ),
                width=2,
            ),
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Max Expiration Days", html_for="example-password-grid"),
                        dbc.Input(
                            type="text",
                            id="max_expiration_days",
                            placeholder="Max",
                        ),
                    ]
                ),
                width=2,
            ),
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Min Delta", html_for="example-email-grid"),
                        dbc.Input(
                            type="text",
                            id="min_delta",
                            placeholder="min",
                        ),
                    ]
                ),
                width=2,
            ),
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Max Delta", html_for="example-email-grid"),
                        dbc.Input(
                            type="text",
                            id="max_delta",
                            placeholder="max",
                        ),
                    ]
                ),
                width=2,
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
                width=2,
            ),
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Min Stock Discount/Gain", html_for="moneyness"),
                        dbc.Input(
                            type="text",
                            id="moneyness",
                            placeholder="Moneyness",
                        ),
                    ]
                ),
                width=2,
            ),
        ],
    ),
    dbc.Row(
        dbc.Col(dbc.Button("Search", color="primary", outline=True, className="mr-1", id='screener-btn'),),
    ),
    dbc.Row(
        dbc.Alert(
                "No Records returned the matching criteria",
                id="alert-message",
                is_open=False,
                duration=2000,
                color="danger"
            ), className="mt-3"
    ),
    dbc.Row(
        dbc.Spinner(html.Div(id="screener-output")),className="mt-3",
    )
])