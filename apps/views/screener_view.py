import dash_html_components as html
import dash_bootstrap_components as dbc
from utils.constants import screener_list

LEFT_COLUMN = dbc.Jumbotron(
    [
        html.H4(children="Option Income Finder"),
        html.Hr(className="my-2"),
        html.P(children="Screen the current option markets for income-focused option"),
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Choose one"),
                            dbc.RadioItems(
                                options=[
                                    {"label": "SECURED PUT", "value": "PUT"},
                                    {"label": "COVERED CALL", "value": "CALL"},
                                ],
                                value="PUT",
                                id="contract_type",
                                inline=True,
                            ),
                        ]
                    ),
                    width=12,
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("WatchList"),
                            dbc.Select(
                                options=[{"label": i, "value": i} for i in screener_list],
                                value="",
                                id="ticker_list",
                            ),
                        ]
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Ticker", html_for="example-email-grid"),
                            dbc.Input(type="text", id="ticker", placeholder="",),
                        ]
                    ),
                    width=6,
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Min Exp Days", html_for="example-email-grid"),
                            dbc.Input(
                                type="text", id="min_expiration_days", placeholder="15",
                            ),
                        ]
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Max Exp Days", html_for="example-password-grid"),
                            dbc.Input(
                                type="text", id="max_expiration_days", placeholder="45",
                            ),
                        ]
                    ),
                    width=6,
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Min Delta", html_for="example-email-grid"),
                            dbc.Input(type="text", id="min_delta", placeholder="0.25",),
                        ]
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Max Delta", html_for="example-email-grid"),
                            dbc.Input(type="text", id="max_delta", placeholder="0.35",),
                        ]
                    ),
                    width=6,
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Premium %", html_for="premium"),
                            dbc.Input(type="text", id="premium", placeholder="2",),
                        ]
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Discount/Gain %", html_for="moneyness"),
                            dbc.Input(type="text", id="moneyness", placeholder="5",),
                        ]
                    ),
                    width=6,
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Search",
                    color="primary",
                    className="float-right",
                    id="screener-btn",
                ),
            ),
        ),
    ],
)

SEARCH_RESULT = [
    dbc.Row(
        dbc.Alert(
            "No Records returned the matching criteria",
            id="alert-message",
            is_open=False,
            duration=2000,
            color="danger",
        ),
    ),
    dbc.Row(dbc.Spinner(html.Div(id="screener-output")),),
]

layout = html.Div(
    [dbc.Row([dbc.Col(LEFT_COLUMN, width=3,), dbc.Col(SEARCH_RESULT, width=9),],),],
)
