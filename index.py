import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from view import portfolio, screener, transaction, income_finder, report, pivot


# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Income Finder", href="/income_finder", id="page-1-link")),
        dbc.NavItem(dbc.NavLink("Screener", href="/screener", id="page-2-link")),
        dbc.NavItem(dbc.NavLink("Portfolio", href="/portfolio", id="page-3-link")),
        dbc.NavItem(dbc.NavLink("Transactions", href="/transaction", id="page-4-link")),
        dbc.NavItem(dbc.NavLink("Report", href="/report", id="page-5-link")),
        dbc.NavItem(dbc.NavLink("Pivot", href="/pivot", id="page-6-link")),
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
    if pathname in ["/", "/income_finder"]:
        return income_finder.layout
    elif pathname == "/screener":
        return screener.layout
    elif pathname == "/portfolio":
        return portfolio.layout
    elif pathname == "/transaction":
        return transaction.layout
    elif pathname == "/report":
        return report.layout
    elif pathname == "/pivot":
        return pivot.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

if __name__ == '__main__':
    app.run_server(debug=True)