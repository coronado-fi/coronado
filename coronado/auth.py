# vim: set fileencoding=utf-8:


from coronado import CoronadoAuthAPIError

import enum
import json
import os
import urllib.parse as encoder

import appdirs
import requests



# --- constants ----

API_NAME = 'coronado' # lower case by design; used also as a namespace
API_URL = 'https://api.partners.dev.tripleupdev.com/'
SECRETS_PATH = appdirs.user_config_dir(API_NAME)
SECRETS_FILE_NAME = 'config.json'
SECRETS_FILE_PATH = os.path.join(SECRETS_PATH, SECRETS_FILE_NAME)
TOKEN_URL = 'https://auth.partners.dev.tripleupdev.com/oauth2/token'


# --- functions ---

def loadConfig() -> dict:
    """
    Load the configuration from the system-dependent config path for the current
    user.  The configuration is stored in A JSON file at SECRETS_FILE_PATH.

    Return
    ------
    A dictionary of configuration parameters.

    """
    os.makedirs(SECRETS_PATH, exist_ok = True)
    with open(SECRETS_FILE_PATH, 'r') as inputStream:
        config = json.load(inputStream)

    return config


def emptyConfig():
    """
    Configuration generator builds an empty configuration to fill in the details.


    Return
    ------
    A dictionary of configuration parameters, all the values are empty.
    """
    return { "clientID": "",
             "clientName": "",
             "secret": "",
             "token": "", }


# +++ classes +++

class Scopes(enum.Enum):
    """
    Client credentials OAuth2 flow scopes.

    Enum items
    ----------
    CONTENT_PROVIDERS : str
        API partner content provider scope
    PORTFOLIOS : str
        API partner portfolios scope
    PUBLISHERS : str
        API partner publishers scope
    VIEW_OFFERS : str
        API partner view offers scope
    """
    CONTENT_PROVIDERS = 'api.tripleup.com/partner.content_providers'
    NA = 'no.scope.for.testint'
    PORTFOLIOS = 'api.tripleup.com/partner.portfolios'
    PUBLISHERS = 'api.tripleup.com/partner.publishers'
    VIEW_OFFERS = 'api.tripleup.com/partner.view_offers'


class Auth(object):
    def _getToken(self):
        scopeStr = encoder.quote(self.scope.value)
        payload = { 'grant_type': 'client_credentials', 'scope': scopeStr, }
        credentials = (self.clientID, self.clientSecret)

        response = requests.request('POST', self.tokenURL, data = payload, auth = credentials)

        if response.status_code != 200:
            raise CoronadoAuthAPIError(': '.join([response.reason, json.loads(response.text)["error"]]))

        return json.loads(response.content)

    # --------------------

    def __init__(self, tokenURL = TOKEN_URL, clientID = None, clientSecret = None, scope = None):
        self.tokenURL = tokenURL
        self.clientID = clientID
        self.clientSecret = clientSecret
        self.scope = scope

        self.token = self._getToken()

