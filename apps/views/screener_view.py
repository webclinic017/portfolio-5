import dash_html_components as html
import dash_bootstrap_components as dbc

form = dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label("Min", html_for="example-email-grid"),
                    dbc.Input(
                        type="text",
                        id="start-date",
                        placeholder="Min",
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
                        placeholder="Max",
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