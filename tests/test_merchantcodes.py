# vim: set fileencoding=utf-8:


from coronado.merchantcodes import MerchantCategoryCode

import uuid

import pytest


# --- constants ---

KNOWN_MCC = '1740'


# +++ tests +++

def test_MerchantCategoryCode():
    merchantCode = MerchantCategoryCode(KNOWN_MCC)
    assert isinstance(merchantCode, MerchantCategoryCode)
    assert 'Masonry' in merchantCode.description

    # Create object from existing MCC or TripleObject
    merchantCode = MerchantCategoryCode(merchantCode)
    assert isinstance(merchantCode, MerchantCategoryCode)
    assert 'Masonry' in merchantCode.description


def test_MerchantCategoryCode_list():
    merchantCodes = MerchantCategoryCode.list()
    assert merchantCodes
    assert len(merchantCodes) > 500 # full list

    merchantCodes = MerchantCategoryCode.list(begin = '1500', end = '3000')
    x = len(merchantCodes)
    assert len(merchantCodes) > 10

