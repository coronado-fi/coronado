# vim: set fileencoding=utf-8:


from coronado.offers import MerchantCategoryCode as MCC
from coronado.baseobjects import BASE_MERCHANT_CATEGORY_CODE_DICT

import json


# *** globals ***


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


test_MCC()
test_MCC_inSnakeCaseJSON()

