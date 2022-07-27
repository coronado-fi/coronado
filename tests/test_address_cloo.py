# vim: set fileencoding=utf-8:


from copy import deepcopy

from coronado.address_cloo import AddressCLOO
from coronado.baseobjects import BASE_ADDRESS_CLOO_DICT
from coronado.exceptions import CallError

import json
import pytest


# --- constants ---

CONTROL_ADDRESS = '7370 BAKER ST\nSUITE 42\nPITTSBURGH, PA 15206\nUNITED STATES'


# === globals ===

_validAddress = None


# +++ tests +++


def test_AddressCLOO():
    global _validAddress

    inputAddress = {
        # We made it a requirement but we'll toss it in the instances:
        'complete_address': '',
        'countryCode': 'US',
        'latitude': 37.802821,
        'line1': '1233 Francisco Street',
        'line2': 'Suite 202',
        'locality': 'San Francisco',
        'longitude': -122.425486,
        'postalCode': '94123',
        'province': 'CA',
    }

    with pytest.raises(CallError):
        AddressCLOO(inputAddress)

    _validAddress = AddressCLOO(BASE_ADDRESS_CLOO_DICT)

    assert isinstance(_validAddress, AddressCLOO)
    assert _validAddress.streetAddress == '7370 BAKER ST\nSUITE 42'
    assert _validAddress.postalCode == '15206'

    inputAddress = deepcopy(BASE_ADDRESS_CLOO_DICT)
    inputAddress['completeAddress'] = _validAddress.complete

    with pytest.raises(CallError):
        AddressCLOO(inputAddress)


def test_AddressCLOO_complete():
    result = _validAddress.complete

    assert result == CONTROL_ADDRESS


def test_AddressCLOO_asSnakeCaseDictionary():
    result = _validAddress.asSnakeCaseDictionary()

    assert result['complete_address'] == CONTROL_ADDRESS


def test_AddressCLOO_inSnakeCaseJSON():
    result = json.loads(_validAddress.inSnakeCaseJSON())

    assert result['complete_address'] == CONTROL_ADDRESS


def test___str__():
    assert _validAddress.complete == str(_validAddress)

