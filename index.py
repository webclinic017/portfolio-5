import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server
from apps import portfolio, screener

app.layout = html.Div([
    # header
    html.Div(
        html.H3("Portfolio Manager", className="w3-container app-header")
        ),
         
    # tabs
    html.Div([
        dcc.Tabs(
            id="tabs",
            className='w3-bar app-tab',
            value="options_tab",
            children=[
                dcc.Tab(
                    label='Portfolio', 
                    value='portfolio_tab',
                    className='w3-bar-item w3-button app-tabs w3-hover-white',
                    selected_className='app-tabs-selected',
                ),
                dcc.Tab(
                    label='Screener', 
                    value='screener_tab',
                    className='w3-bar-item w3-button app-tabs w3-hover-white',
                    selected_className='app-tabs-selected',
                ),
            ],
        ), 
        ], className = 'w3-container'
        ),
    # Tab content
    html.Div(id="tab_content", className='w3-container w3-padding-16'),
])

@app.callback(Output("tab_content", "children"), [Input("tabs", "value")])
def render_content(tab):
    if tab == "portfolio_tab":
        return portfolio.layout
    elif tab == "screener_tab":
        return screener.layout

if __name__ == '__main__':
    app.run_server(debug=True)