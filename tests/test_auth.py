# vim: set fileencoding=utf-8:


from coronado import CoronadoAuthAPIError
from coronado.auth import Auth
from coronado.auth import Scopes
from coronado.auth import emptyConfig
from coronado.auth import loadConfig

import copy

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


def test_Auth():
    config = loadConfig()

    a = Auth(config['tokenURL'], clientID = config['clientID'], clientSecret = config['secret'], scope = Scopes.CONTENT_PROVIDERS)
    a = Auth(config['tokenURL'], clientID = config['clientID'], clientSecret = config['secret'], scope = Scopes.PORTFOLIOS)
    # TODO:  fix this grant
    # a = Auth(config['tokenURL'], clientID = config['clientID'], clientSecret = config['secret'], scope = Scopes.PUBLISHERS)
    a = Auth(config['tokenURL'], clientID = config['clientID'], clientSecret = config['secret'], scope = Scopes.VIEW_OFFERS)

    with pytest.raises(CoronadoAuthAPIError):
        Auth(config['tokenURL'], clientID = config['clientID'], clientSecret = config['secret'], scope = Scopes.NA)


# test_Auth()

