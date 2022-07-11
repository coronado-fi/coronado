# vim: set fileencoding=utf-8:


from coronado import CoronadoDuplicatesDisallowedError
from coronado import CoronadoMalformedObjectError
from coronado import CoronadoUnprocessableObjectError
from coronado import TripleObject
from coronado.auth import Auth
from coronado.auth import Scopes
from coronado.baseobjects import BASE_MERCHANT_CATEGORY_CODE_DICT
from coronado.merchant import Merchant
from coronado.merchant import SERVICE_PATH

import json
import uuid

import pytest

import coronado.auth as auth


# *** globals ***


# *** globals ***

_config = auth.loadConfig()
# TODO:  file this bug:
# _auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.VIEW_OFFERS)
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.PORTFOLIOS)


Merchant.initialize(_config['serviceURL'], SERVICE_PATH, _auth)


# +++ tests +++

