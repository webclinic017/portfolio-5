import dash_html_components as html
import dash_bootstrap_components as dbc

layout = html.Div([
     dbc.Row(
        dbc.Col(dbc.Button("Get Portfolio", color="primary", outline=True, className="mr-1", id='portfolio-btn'),)
    ),
    dbc.Spinner(html.Div(id="portfolio-output")),
])