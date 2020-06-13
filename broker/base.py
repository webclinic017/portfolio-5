import os
import time
import json
import datetime
import requests
import urllib.parse
import logging

import broker.utils
from .config import CONSUMER_ID, REDIRECT_URI, ACCOUNT_NUMBER
from .exceptions import APIException


class Base:

    """
        TD Ameritrade API Client Class.

        Implements OAuth 2.0 Authorization Code Grant workflow, handles configuration
        and state management, adds token for authenticated calls, and performs request 
        to the TD Ameritrade API.
    """

    def __init__(self, **kwargs):
        """
            Initializes the session with default values and any user-provided overrides.

            The following arguments MUST be specified at runtime or else initalization
            will fail.

            NAME: consumer_id
            DESC: The Consumer ID assigned to you during the App registration. This can
                  be found at the app registration portal.

            NAME: account_number
            DESC: This is the account number for your main TD Ameritrade Account.

            NAME: account_password
            DESC: This is the account password for your main TD Ameritrade Account.

            NAME: redirect_uri
            DESC: This is the redirect URL that you specified when you created your
                  TD Ameritrade Application.

        """

        # define the configuration settings.
        self.config = {
            "consumer_id": CONSUMER_ID,
            "account_number": ACCOUNT_NUMBER,
            "account_password": None,
            "redirect_uri": REDIRECT_URI,
            "resource": "https://api.tdameritrade.com",
            "api_version": "/v1",
            "cache_state": True,
            "json_path": None,
            "authenticaiton_url": "https://auth.tdameritrade.com",
            "auth_endpoint": "https://auth.tdameritrade.com" + "/auth?",
            "token_endpoint": "https://api.tdameritrade.com" + "/v1" + "/oauth2/token",
            "refresh_enabled": True,
        }

        # This serves as a mechanism to validate input parameters for the different endpoint arguments.
        self.endpoint_arguments = {
            "search_instruments": {
                "projection": [
                    "symbol-search",
                    "symbol-regex",
                    "desc-search",
                    "desc-regex",
                    "fundamental",
                ]
            },
            "get_market_hours": {
                "markets": ["EQUITY", "OPTION", "FUTURE", "BOND", "FOREX"]
            },
            "get_movers": {
                "market": ["$DJI", "$COMPX", "$SPX.X"],
                "direction": ["up", "down"],
                "change": ["value", "percent"],
            },
            "get_user_principals": {
                "fields": [
                    "streamerSubscriptionKeys",
                    "streamerConnectionInfo",
                    "preferences",
                    "surrogateIds",
                ]
            },
        }

        # loop through the key word arguments.
        for key in kwargs:

            # there may be a chance an unknown argument was pass through. Print a warning if this is the case.
            if key not in self.config:
                print("WARNING: The argument, {} is an unkown argument.".format(key))
                raise KeyError("Invalid Argument Name.")

        # update the configuration settings so they now contain the passed through value.
        self.config.update(kwargs.items())

        # call the state_manager method and update the state to init (initalized)
        self.state_manager("init")

        # define a new attribute called 'authstate' and initalize it to '' (Blank). This will be used by our login function.
        self.authstate = False

        # Initalize the client with no streaming session.
        self.streaming_session = None

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        self.merged_headers = self.headers()

        # API response
        self._data = {}

    def __repr__(self):
        """
            Defines the string representation of our TD Ameritrade Class instance.

            RTYPE: String
        """

        # grab the logged in state.
        if self.state["loggedin"]:
            logged_in_state = "True"
        else:
            logged_in_state = "False"

        # define the string representation
        str_representation = "<TDAmeritrade Client (logged_in = {}, authorized = {})>".format(
            logged_in_state, self.authstate
        )

        return str_representation

    def headers(self, mode=None):
        """ 
            Returns a dictionary of default HTTP headers for calls to TD Ameritrade API,
            in the headers we defined the Authorization and access token.

            NAME: mode            
            DESC: Defines the content-type for the headers dictionary.
            TYPE: String
        """

        # grab the access token
        token = self.state["access_token"]

        # create the headers dictionary
        headers = {"Authorization": f"Bearer {token}"}

        if mode == "application/json":
            headers["Content-type"] = "application/json"

        return headers

    def api_endpoint(self, url):
        """
            Convert relative endpoint (e.g., 'quotes') to full API endpoint.

            NAME: url
            DESC: The URL that needs conversion to a full endpoint URL.
            TYPE: String

            RTYPE: String
        """

        # if they pass through a valid url then, just use that.
        if urllib.parse.urlparse(url).scheme in ["http", "https"]:
            return url

        # otherwise build the URL
        return urllib.parse.urljoin(
            self.config["resource"] + self.config["api_version"] + "/", url.lstrip("/")
        )

    def state_manager(self, action):
        """
            Manages the self.state dictionary. Initalize State will set
            the properties to their default value. Save will save the 
            current state if 'cache_state' is set to TRUE.

            NAME: action
            DESC: action argument must of one of the following:
                    'init' -- Initalize State.
                    'save' -- Save the current state.
            TYPE: String            
        """

        # define the initalized state, these are the default values.
        initialized_state = {
            "access_token": None,
            "refresh_token": None,
            "access_token_expires_at": 0,
            "refresh_token_expires_at": 0,
            "authorization_url": None,
            "redirect_code": None,
            "token_scope": "",
            "loggedin": False,
        }

        # Grab the current directory of the client file, that way we can store the JSON file in the same folder.
        if self.config["json_path"] is not None:
            file_path = self.config["json_path"]
        else:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            filename = "TDAmeritradeState.json"
            file_path = os.path.join(dir_path, filename)

        # if the state is initalized
        if action == "init":
            self.state = initialized_state

            # if they allowed for caching and the file exist, load the file.
            if self.config["cache_state"] and os.path.isfile(file_path):
                with open(file_path, "r") as fileHandle:
                    self.state.update(json.load(fileHandle))

            # if they didnt allow for caching delete the file.
            elif not self.config["cache_state"] and os.path.isfile(
                os.path.join(dir_path, filename)
            ):
                os.remove(file_path)

        # if they want to save it and have allowed for caching then load the file.
        elif action == "save" and self.config["cache_state"]:
            with open(file_path, "w") as fileHandle:

                # build JSON string using dictionary comprehension.
                json_string = {key: self.state[key] for key in initialized_state}
                json.dump(json_string, fileHandle)

    def login(self):
        """
            Ask the user to authenticate  themselves via the TD Ameritrade Authentication Portal. This will
            create a URL, display it for the User to go to and request that they paste the final URL into
            command window.

            Once the user is authenticated the API key is valide for 90 days, so refresh tokens may be used
            from this point, up to the 90 days.
        """

        # if caching is enabled then attempt silent authentication.
        if self.config["cache_state"]:

            # if it was successful, the user is authenticated.
            if self.silent_sso():

                # update the authentication state
                self.authstate = "Authenticated"

                return True

        # update the authentication state
        self.authstate = "Authenticated"

        # prepare the payload to login
        data = {
            "response_type": "code",
            "redirect_uri": self.config["redirect_uri"],
            "client_id": self.config["consumer_id"] + "@AMER.OAUTHAP",
        }

        # url encode the data.
        params = urllib.parse.urlencode(data)

        # build the full URL for the authentication endpoint.
        url = self.config["auth_endpoint"] + params

        # set the newly created 'authorization_url' key to the newly created url
        self.state["authorization_url"] = url

        # aks the user to go to the URL provided, they will be prompted to authenticate themsevles.
        print(
            "Please go to URL provided authorize your account: {}".format(
                self.state["authorization_url"]
            )
        )

        # ask the user to take the final URL after authentication and paste here so we can parse.
        my_response = input("Paste the full URL redirect here: ")

        # store the redirect URL
        self.state["redirect_code"] = my_response

        # this will complete the final part of the authentication process.
        self.grab_access_token()

    def logout(self):
        """
            Clears the current TD Ameritrade Connection state.
        """

        # change state to initalized so they will have to either get a
        # new access token or refresh token next time they use the API
        self.state_manager("init")

    def grab_access_token(self):
        """
            Access token handler for AuthCode Workflow. This takes the
            authorization code parsed from the auth endpoint to call the
            token endpoint and obtain an access token.
        """

        # Parse the URL
        url_dict = urllib.parse.parse_qs(self.state["redirect_code"])

        # Convert the values to a list.
        url_values = list(url_dict.values())

        # Grab the Code, which is stored in a list.
        url_code = url_values[0][0]

        # define the parameters of our access token post.
        data = {
            "grant_type": "authorization_code",
            "client_id": self.config["consumer_id"],
            "access_type": "offline",
            "code": url_code,
            "redirect_uri": self.config["redirect_uri"],
        }

        # post the data to the token endpoint and store the response.
        token_response = requests.post(
            url=self.config["token_endpoint"], data=data, verify=True
        )

        # call the save_token method to save the access token.
        self.token_save(token_response)

        # update the state if the request was successful.
        if token_response and token_response.ok:
            self.state_manager("save")

    def silent_sso(self):
        """
            Attempt a silent authentication, by checking whether current access token
            is valid and/or attempting to refresh it. Returns True if we have successfully 
            stored a valid access token.

            RTYPE: Boolean
        """

        # if the current access token is not expired then we are still authenticated.
        if self.token_seconds(token_type="access_token") > 0:
            return True

        # if the refresh token is expired then you have to do a full login.
        elif self.token_seconds(token_type="refresh_token") <= 0:
            return False

        # if the current access token is expired then try and refresh access token.
        elif self.state["refresh_token"] and self.token_refresh():
            return True

        # More than likely a first time login, so can't do silent authenticaiton.
        return False

    def token_refresh(self):
        """
            Refreshes the current access token.

            RTYPE: Boolean
        """

        # build the parameters of our request
        data = {
            "client_id": self.config["consumer_id"] + "@AMER.OAUTHAP",
            "grant_type": "refresh_token",
            "access_type": "offline",
            "refresh_token": self.state["refresh_token"],
        }

        # make a post request to the token endpoint
        response = requests.post(self.config["token_endpoint"], data=data, verify=True)

        # if there was an error go through the full authentication
        if response.status_code == 401:
            print("The Credentials you passed through are invalid.")
            return False
        elif response.status_code == 400:
            print("Validation was unsuccessful.")
            return False
        elif response.status_code == 500:
            print("The TD Server is experiencing an error, please try again later.")
            return False
        elif response.status_code == 403:
            print("You don't have access to this resource, cannot authenticate.")
            return False
        elif response.status_code == 503:
            print("The TD Server can't respond, please try again later.")
            return False
        else:
            # save the token and the state, since we now have a new access token that has a new expiration date.
            self.token_save(response)
            self.state_manager("save")
            return True

    def token_save(self, response):
        """
            Parses an access token from the response of a POST request and saves it
            in the state dictionary for future use. Additionally, it will store the
            expiration time and the refresh token.

            NAME: response
            DESC: A response object recieved from the `token_refresh` or `grab_access_token`
                  methods.
            TYPE: requests.Response

            RTYPE: Boolean
        """

        # parse the data.
        json_data = response.json()

        # make sure there is an access token before proceeding.
        if "access_token" not in json_data:
            self.logout()
            return False

        # save the access token and refresh token
        self.state["access_token"] = json_data["access_token"]
        self.state["refresh_token"] = json_data["refresh_token"]

        # and the logged in status
        self.state["loggedin"] = True

        # store token expiration time
        self.state["access_token_expires_at"] = time.time() + int(
            json_data["expires_in"]
        )
        self.state["refresh_token_expires_at"] = time.time() + int(
            json_data["refresh_token_expires_in"]
        )

        return True

    def token_seconds(self, token_type="access_token"):
        """
            Return the number of seconds until the current access token or refresh token
            will expire. The default value is access token because this is the most commonly used
            token during requests.

            NAME: token_type
            DESC: The type of token you would like to determine lifespan for. Possible values are:
                  'access_token'
                  'refresh_token'
            TYPE: String

            RTYPE: Boolean
        """

        # if needed check the access token.
        if token_type == "access_token":

            # if the time to expiration is less than or equal to 0, return 0.
            if (
                not self.state["access_token"]
                or time.time() >= self.state["access_token_expires_at"]
            ):
                return 0

            # else return the number of seconds until expiration.
            token_exp = int(self.state["access_token_expires_at"] - time.time())

        # if needed check the refresh token.
        elif token_type == "refresh_token":

            # if the time to expiration is less than or equal to 0, return 0.
            if (
                not self.state["refresh_token"]
                or time.time() >= self.state["refresh_token_expires_at"]
            ):
                return 0

            # else return the number of seconds until expiration.
            token_exp = int(self.state["refresh_token_expires_at"] - time.time())

        return token_exp

    def token_validation(self, nseconds=5):
        """
            Verify the current access token is valid for at least N seconds, and
            if not then attempt to refresh it. Can be used to assure a valid token
            before making a call to the TD Ameritrade API.

            PARA: nseconds
            TYPE: integer
            DESC: The minimum number of seconds the token has to be valid for before
                  attempting to get a refresh token.
        """
        if (
            self.token_seconds(token_type="access_token") < nseconds
            and self.config["refresh_enabled"]
        ):
            self.token_refresh()

    def validate_arguments(
        self, endpoint=None, parameter_name=None, parameter_argument=None
    ):
        """
            This will validate an argument for the specified endpoint and raise an error if the argument
            is not valid. Can take both a list of arguments or a single argument.

            NAME: endpoint
            DESC: This is the endpoint name, and should line up exactly with the TD Ameritrade Client library.
            TYPE: String

            NAME: parameter_name
            DESC: An endpoint can have a parameter that needs to be passed through, this represents the name of
                  that parameter.
            TYPE: String

            NAME: parameter_argument
            DESC: The arguments being validated for the particular parameter name. This can either be a single value
                  or a list of values.
            TYPE: List<Strings> OR String


            EXAMPLES:

            WITH NO LIST:
            ------------------------------------------------------------
            api_endpoint = 'search_instruments'
            para_name = 'projection'
            para_args = 'fundamental'

            self.validate_arguments(endpoint = api_endpoint, 
                                    parameter_name = para_name, 
                                    parameter_argument = para_args)


            WITH LIST:
            ------------------------------------------------------------
            api_endpoint = 'get_market_hours'
            para_name = 'markets'
            para_args = ['FOREX', 'EQUITY']

            self.validate_arguments(endpoint = api_endpoint, 
                                    parameter_name = para_name, 
                                    parameter_argument = para_args)

        """

        # grab the possible parameters for the endpoint.
        parameters_dictionary = self.endpoint_arguments[endpoint]

        # grab the parameter arguments, for the specified parameter name.
        parameter_possible_arguments = parameters_dictionary[parameter_name]

        # if it's a list then see if it matches any of the possible values.
        if type(parameter_argument) is list:

            # build the validation result list.
            validation_result = [
                argument not in parameter_possible_arguments
                for argument in parameter_argument
            ]

            # if any of the results are FALSE then raise an error.
            if any(validation_result):
                print(
                    "\nThe value you passed through is not valid, please choose one of the following valid values: {} \n".format(
                        " ,".join(parameter_possible_arguments)
                    )
                )
                raise ValueError("Invalid Value.")
            elif not any(validation_result):
                return True

        # if the argument isn't in the list of possible values, raise an error.
        elif parameter_argument not in parameter_possible_arguments:
            print(
                "\nThe value you passed through is not valid, please choose one of the following valid values: {} \n".upper().format(
                    " ,".join(parameter_possible_arguments)
                )
            )
            raise ValueError("Invalid Value.")

        elif parameter_argument in parameter_possible_arguments:
            return True

    def prepare_arguments_list(self, parameter_list=None):
        """
            Some endpoints can take multiple values for a parameter, this
            method takes that list and creates a valid string that can be 
            used in an API request. The list can have either one index or
            multiple indexes.

            NAME: parameter_list
            DESC: A list of paramater values assigned to an argument.
            TYPE: List

            EXAMPLE:

            SessionObject.prepare_arguments_list(parameter_list = ['MSFT', 'SQ'])

        """

        # validate it's a list.
        if type(parameter_list) is list:

            # specify the delimeter and join the list.
            delimeter = ","
            parameter_list = delimeter.join(parameter_list)

        return parameter_list

    def _api_response(self, url, params, verify=True):
        response = requests.get(
            url=url, headers=self.merged_headers, params=params, verify=verify
        )
        # print(" Request URL: ", response.request.url)
        # print(" Request Body:", response.request.body)
        logging.debug(response.text)

        response_dict = response.json()

        try:
            response_dict[
                "error"
            ]  # see if there is a fault message in the API response

        except (KeyError, TypeError) as e:
            return response_dict  # if no fault code or list is returned, then return the API response

        # if there is a fault code, raise an API exception
        raise APIException(error_message=response["error"])

