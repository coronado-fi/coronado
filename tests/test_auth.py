# vim: set fileencoding=utf-8:


from coronado.auth import Auth
from coronado.auth import CoronadoAuthInvalidScopes
from coronado.auth import CoronadoAuthTokenAPIError
from coronado.auth import EXPIRATION_OFFSET
from coronado.auth import Scopes
from coronado.auth import emptyConfig
from coronado.auth import loadConfig

import json
import time

import pytest


# +++ tests +++

# NB:  These tests don't use fixtures because they need to run against the
# actual service.  This may change in the future.


def test_loadConfig():
    config = loadConfig()

    assert isinstance(config, dict)
    assert "clientID" in config
    assert "clientName" in config


def test_emptyConfig():
    config = emptyConfig()

    assert isinstance(config, dict)
    assert "clientID" in config
    assert "clientName" in config


_config = loadConfig()


def test_Auth():
    Auth(
        _config["tokenURL"],
        clientID=_config["clientID"],
        clientSecret=_config["secret"],
        scope=Scopes.CONTENT_PROVIDERS,
    )
    Auth(
        _config["tokenURL"],
        clientID=_config["clientID"],
        clientSecret=_config["secret"],
        scope=[
            Scopes.PORTFOLIOS,
            Scopes.CONTENT_PROVIDERS,
        ],
    )
    Auth(
        _config["tokenURL"],
        clientID=_config["clientID"],
        clientSecret=_config["secret"],
    )

    with pytest.raises(CoronadoAuthTokenAPIError):
        Auth(
            _config["tokenURL"],
            clientID=_config["clientID"],
            clientSecret=_config["secret"],
            scope=Scopes.NA,
        )

    with pytest.raises(CoronadoAuthInvalidScopes):
        Auth(
            _config["tokenURL"],
            clientID=_config["clientID"],
            clientSecret=_config["secret"],
            scope=69,
        )

    with pytest.raises(CoronadoAuthInvalidScopes):
        Auth(
            _config["tokenURL"],
            clientID=_config["clientID"],
            clientSecret=_config["secret"],
            scope=[
                Scopes.PORTFOLIOS,
                42,
            ],
        )


def test_Auth_expired_token():
    a = Auth(
        _config["tokenURL"],
        clientID=_config["clientID"],
        clientSecret=_config["secret"],
        scope=Scopes.CONTENT_PROVIDERS,
    )
    oldToken = a.token
    time.sleep(2)
    newToken = a.token
    assert oldToken == newToken

    b = Auth(
        _config["tokenURL"],
        clientID=_config["clientID"],
        clientSecret=_config["secret"],
        scope=Scopes.CONTENT_PROVIDERS,
        expirationOffset=EXPIRATION_OFFSET,
    )
    oldToken = b._token
    assert oldToken != b.token


def test_Auth_accessToken():
    a = Auth(
        _config["tokenURL"],
        clientID=_config["clientID"],
        clientSecret=_config["secret"],
        scope=Scopes.CONTENT_PROVIDERS,
    )
    control = json.loads(a.tokenPayload)["access_token"]

    assert a.token == control


def test_Auth_tokenType():
    a = Auth(
        _config["tokenURL"],
        clientID=_config["clientID"],
        clientSecret=_config["secret"],
        scope=Scopes.CONTENT_PROVIDERS,
    )
    control = json.loads(a.tokenPayload)["token_type"]

    assert a.tokenType == control


def test_Auth_info():
    info = Auth(
        _config["tokenURL"],
        clientID=_config["clientID"],
        clientSecret=_config["secret"],
        scope=Scopes.CONTENT_PROVIDERS,
    ).info
    assert info["scope"] == Scopes.CONTENT_PROVIDERS.value
    assert info["tokenIssuerID"]
    assert "issuingServer" in info
