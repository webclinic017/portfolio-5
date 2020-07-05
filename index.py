import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app, server
from apps import portfolio, screener, transaction, income_finder

import logging

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Income Finder", href="/page-1", id="page-1-link")),
        dbc.NavItem(dbc.NavLink("Screener", href="/page-2", id="page-2-link")),
        dbc.NavItem(dbc.NavLink("Portfolio", href="/page-3", id="page-3-link")),
        dbc.NavItem(dbc.NavLink("Transactions", href="/page-4", id="page-4-link")),
    ],
    brand="Aarya",
    brand_href="#",
    color="dark",
    dark=True,
)


content = html.Div(id="page-content", className="content")

app.layout = html.Div([dcc.Location(id="url"), navbar, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return income_finder.layout
    elif pathname == "/page-2":
        return screener.layout
    elif pathname == "/page-3":
        return portfolio.layout
    elif pathname == "/page-4":
        return transaction.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)