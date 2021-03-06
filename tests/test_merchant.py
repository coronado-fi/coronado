# vim: set fileencoding=utf-8:


# from coronado.merchant import MerchantStatus
from coronado import TripleObject
from coronado.auth import Auth
from coronado.auth import Scope
from coronado.baseobjects import BASE_MERCHANT_CATEGORY_CODE_DICT
from coronado.exceptions import CallError
from coronado.merchant import Merchant
from coronado.merchant import MerchantCategoryCode as MCC
from coronado.merchant import SERVICE_PATH

import json
import uuid

import pytest

import coronado.auth as auth


# *** globals ***


# *** globals ***

_config = auth.loadConfig()
# TODO:  file this bug:
# _auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scope.VIEW_OFFERS)
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scope.PORTFOLIOS)


Merchant.initialize(_config['serviceURL'], SERVICE_PATH, _auth)


# +++ tests +++

def test_MCC():
    _code = MCC(BASE_MERCHANT_CATEGORY_CODE_DICT)

    assert 'code' in _code.listAttributes()
    assert 'description' in _code.listAttributes()


def test_MCC_inSnakeCaseJSON():
    _code = MCC(BASE_MERCHANT_CATEGORY_CODE_DICT)
    payload = _code.inSnakeCaseJSON()
    control = json.loads(payload)

    assert _code.code == control['code']
    assert _code.description == control['description']



@pytest.mark.skip('501 - not implemented in underlying API')
def test_Merchant_create():
    spec = {
        "external_id": uuid.uuid4().hex,
        "assumed_name": "Malwart Stores %s" % uuid.uuid4().hex,
        "address": {
            "complete_address": "7370 BAKER ST STE 100\nPITTSBURGH, PA 15206",
            "line_1": "7370 BAKER ST STE 100",
            "line_2": "",
            "locality": "PITTSBURGH",
            "province": "PA",
            "postal_code": "15206",
            "country_code": "US",
            "latitude": 40.440624,
            "longitude": -79.995888
        },
        "merchant_category_code": {
            "code": "7998"
        },
        "logo_url": "https://assets.website-files.com/6287e9b993a42a7dcb001b99/6287eb0b156c574ac578dab3_Triple-Logo-Full-Color.svg"
    }

    account = Merchant.create(spec)
    assert account

    with pytest.raises(CallError):
        Merchant.create(None)

#     spec['external_id'] = KNOWN_ACCT_EXT_ID
#     with pytest.raises(CoronadoDuplicatesDisallowedError):
#         Merchant.create(spec)

    spec['external_id'] = '****'
    with pytest.raises(CoronadoUnprocessableObjectError):
        Merchant.create(spec)

