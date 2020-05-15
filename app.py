import dash
import dash_auth
from flask_caching import Cache

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = [
    ['hello', 'nishant']
]

external_stylesheets = ['https://www.w3schools.com/w3css/4/w3.css', 'https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)

app = dash.Dash(
    __name__,
    external_stylesheets= external_stylesheets
)

app.title = 'Options Tracker'
app.server.secret_key = "option_tracker_01"
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
server = app.server
app.config.suppress_callback_exceptions = True


cache = Cache(app.server, config={
    'CACHE_TYPE': 'redis',
    # Note that filesystem cache doesn't work on systems with ephemeral
    # filesystems like Heroku.
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory',

    # should be equal to maximum number of users on the app at a single time
    # higher numbers will store more data in the filesystem / redis cache
    'CACHE_THRESHOLD': 200
})
