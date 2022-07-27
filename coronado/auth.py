# vim: set fileencoding=utf-8:


from datetime import datetime

from jose import jwt
from jose.exceptions import ExpiredSignatureError
from jose.exceptions import JWTClaimsError
from jose.exceptions import JWTError

from coronado.exceptions import AuthInvalidScope
from coronado.exceptions import AuthTokenAPIError

import enum
import json
import os

import appdirs
import requests

from coronado.tools import tripleKeysToCamelCase
from coronado import TripleEnum

# --- constants ----

API_NAME = 'coronado' # lower case by design; used also as a namespace
EXPIRATION_OFFSET = -3900
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
             "serviceURL": "", # API service URL
             "token": "",
             "tokenURL": ""}


# +++ classes +++

class Scope(TripleEnum):
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
    NA = 'no.scope.for.testing'
    PORTFOLIOS = 'api.tripleup.com/partner.portfolios'
    PUBLISHERS = 'api.tripleup.com/partner.publishers'
    VIEW_OFFERS = 'api.tripleup.com/partner.view_offers'


class Auth(object):
    def _buildScopeStrFrom(self, scopes):
        if isinstance(scopes, Scope):
            return scopes.value
        elif isinstance(scopes, list):
            return ' '.join([ s.value for s in scopes ])
        
        return ""


    def _getTokenPayload(self) -> str:
        # scopeStr = encoder.quote(self._buildScopeStrFrom(self._scope))
        scopeStr = self._buildScopeStrFrom(self._scope)
        payload = { 'grant_type': 'client_credentials', 'scope': scopeStr, }
        credentials = (self._clientID, self._clientSecret)

        response = requests.request('POST', self._tokenURL, data = payload, auth = credentials)

        if response.status_code != 200:
            raise AuthTokenAPIError(': '.join([response.reason, json.loads(response.text)["error"]]))

        return str(response.content, encoding = 'utf-8')


    def _setState(self, expirationOffset = None):
        d = json.loads(self._tokenPayload)

        deltaSeconds = expirationOffset if expirationOffset else d['expires_in']

        now = round(datetime.now().timestamp())
        self._expirationTime = round(now+deltaSeconds)
        self._token = d['access_token']
        self._tokenType = d['token_type']


    def _resolveScopeFrom(self, scope):
        if not scope:
            return
        if isinstance(scope, Scope):
            return scope
        elif isinstance(scope, list):
            for item in scope:
                if not isinstance(item, Scope):
                    raise AuthInvalidScope(str(scope))
            return scope
        else:
            raise AuthInvalidScope(str(scope))

    # --------------------

    def __init__(self, tokenURL = TOKEN_URL, clientID = None, clientSecret = None, scope = None, expirationOffset = None):
        """
        Instantiates a new Auth object.  It requires URLs and configuration
        parameters granted by triple for use with this API.

        Arguments
        ---------
            tokenURL : str
        The URL for the access token provider

            clientID : str
        A unique client ID, provider by triple

            clientSecret : str
        The unique client ID associated secret

            scope : coronado.auth.Scope
        The client credentials OAuth2 scope for which access is granted. `scope`
        is one of:

        - A single `Scope` value
        - A list of two or more `Scope` values
        - `None`

        If `None`, the receiver will grant access to all available scopes.

        See:  <a href='https://aws.amazon.com/blogs/mobile/understanding-amazon-cognito-user-pool-oauth-2-0-grants/' target='_blank'>AWS Cognito user pool grants</a>
        for details.

            expirationOffset : int
        Expiration time buffer, seconds to subtract from expiration time to
        that the internal token representation is up-to-date; **used only for
        unit testing, users should ignore this argument**.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the 
        **`coronado.exceptions`** module.
        """
        self._tokenURL = tokenURL
        self._clientID = clientID
        self._clientSecret = clientSecret
        self._scope = self._resolveScopeFrom(scope)

        self._tokenPayload = self._getTokenPayload()

        self._setState(expirationOffset)


    @property
    def tokenPayload(self) -> str:
        """
        Returns the current access token associated with the receiver.  The
        property is guaranteed to never return an expired token.  The underlying
        implementation will request a new access token to the token provider
        API.

        Returns
        -------
        A JWT string
        """
        now = round(datetime.now().timestamp())
        delta = self._expirationTime-now
        if delta < 0:
            self._tokenPayload = self._getTokenPayload()
            self._setState()

        return self._tokenPayload


    @property
    def token(self) -> str:
        """
        Return the current access token by itself.  Auth objects have a JWT
        representation internally, which includes the actual access token in
        one of its attributes.  This property returns that access token
        sans all the rest of the JWT JSON structure.

        Returns
        -------
            A token string
        """
        self.tokenPayload  # This is for the refresh token side effect

        return self._token


    @property
    def tokenType(self) -> str:
        """
        Return the current token type by itself.  Auth objects have a JWT
        representation internally, which includes the actual access token in
        one of its attributes.  This property returns that token type
        attribute sans all the rest of the JWT JSON structure.

        Returns
        -------
            A token type string
        """
        self.tokenPayload  # This is for the refresh token side effect

        return self._tokenType


    @property
    def info(self) -> dict:
        """
        Return the receiver's reserved OAuth2 claims set.
        
        Reference:  https://www.oauth.com/oauth2-servers/openid-connect/id-tokens/

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the 
        **`coronado.exceptions`** module.
        """
        self.tokenPayload

        try:
            claimSet = jwt.decode(self.token, '', options = {'verify_signature': False})
        except JWTError as e:
            raise AuthTokenAPIError(str(e))
        except ExpiredSignatureError as e:
            raise AuthTokenAPIError(str(e))
        except JWTClaimsError as e:
            raise AuthTokenAPIError(str(e))
            
        return tripleKeysToCamelCase(claimSet)

