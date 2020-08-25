import logging

import dash
import dash_auth
import dash_bootstrap_components as dbc

logging.basicConfig(filename="app.log",
                    level=logging.DEBUG, format='%(asctime)s %(message)s')

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = [
    ['hello', 'nishant']
]
external_stylesheets=[dbc.themes.COSMO]
app = dash.Dash(__name__)

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app = dash.Dash(
    __name__,
    external_stylesheets= external_stylesheets,
    suppress_callback_exceptions=True
)

app.title = 'Options Tracker'
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
server = app.server
