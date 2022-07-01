# vim: set fileencoding=utf-8:


from coronado.auth import CoronadoAuthTokenAPIError
from coronado.auth import EXPIRATION_OFFSET
from coronado.auth import Auth
from coronado.auth import Scopes
from coronado.auth import emptyConfig
from coronado.auth import loadConfig

import time

import pytest


# +++ tests +++

# NB:  These tests don't use fixtures because they need to run against the
# actual service.  This may change in the future.

def test_loadConfig():
    config = loadConfig()

    assert isinstance(config, dict)
    assert 'clientID' in config
    assert 'clientName' in config
    assert 'token' in config


def test_emptyConfig():
    config = emptyConfig()

    assert isinstance(config, dict)
    assert 'clientID' in config
    assert 'clientName' in config
    assert 'token' in config


_config = loadConfig()


def test_Auth():
    Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.CONTENT_PROVIDERS)
    Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.PORTFOLIOS)
    # TODO:  fix this grant
    # Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.PUBLISHERS)
    Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.VIEW_OFFERS)

    with pytest.raises(CoronadoAuthTokenAPIError):
        Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.NA)


def test_Auth_expired_token():
    a = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.CONTENT_PROVIDERS)
    oldToken = a.token
    time.sleep(2)
    newToken = a.token
    assert oldToken == newToken

    b = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.CONTENT_PROVIDERS, expirationOffset = EXPIRATION_OFFSET)
    oldTokenStr = b._tokenString
    time.sleep(2)
    newTokenStr = b.token

    assert oldTokenStr != newTokenStr

