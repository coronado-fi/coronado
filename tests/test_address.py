# vim: set fileencoding=utf-8:


from coronado.address import Address

import json


# --- constants ---

COMPLETE_ADDRESS = '1233 Francisco Street\nSuite 202\nSan Francisco, CA 94123'


# +++ tests +++

_validAddress = Address({ 
    # We made it a requirement but we'll toss it in the instances:
    'complete_address': '',  
    'countryCode': 'US',
    'latitude': 37.802821,
    'line1': '1233 Francisco Street',
    # 'line2': 'Suite 202',
    'locality': 'San Francisco',
    'longitude': -122.425486,
    'postalCode': '94123',
    'province': 'CA',
})


def test_Address_completeAddress():
    result = _validAddress.complete

    assert result == COMPLETE_ADDRESS


def test_Address_asSnakeCaseDictionary():
    result = _validAddress.asSnakeCaseDictionary()

    assert result['complete_address'] == COMPLETE_ADDRESS


def test_Address_inSnakeCaseJSON():
    result = json.loads(_validAddress.inSnakeCaseJSON())

    assert result['complete_address'] == COMPLETE_ADDRESS

