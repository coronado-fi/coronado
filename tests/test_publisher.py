# vim: set fileencoding=utf-8:


from coronado import CoronadoAPIError
from coronado import CoronadoDuplicatesDisallowedError
from coronado import CoronadoMalformedObjectError
from coronado import CoronadoUnprocessableObjectError
from coronado.address import Address
from coronado.auth import Auth
from coronado.auth import Scope
from coronado.publisher import Publisher
from coronado.publisher import SERVICE_PATH

import uuid

import pytest

import coronado.auth as auth


# *** constants ***

KNOWN_PUB_ID = '10'
KNOWN_ASSUMED_NAME = 'Kukla Enterprises, Inc.'


# *** globals ***

_address = Address({
    # We made it a requirement but we'll toss it in the instances:
    'complete_address': '',
    'countryCode': 'US',
    'latitude': 0,
    'line1': '2801 Turk Boulevard',
    'line2': 'Suite 202',
    'locality': 'San Francisco',
    'longitude': 0,
    'postalCode': '94118',
    'province': 'CA',
})

_config = auth.loadConfig()
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scope.PUBLISHERS)

Publisher.initialize(_config['serviceURL'], SERVICE_PATH, _auth)


# --- utility functions ---

def _generateTestPayload():
    return {  # sn ::= snake case
        'address': _address.asSnakeCaseDictionary(),
        'assumed_name': 'R2D2 Enterprises %s' % uuid.uuid4().hex,
        'external_id': uuid.uuid4().hex[-12:],
        'revenue_share': 1.5,
    }


# +++ tests +++

def test_Publisher_create():
    with pytest.raises(CoronadoMalformedObjectError):
        Publisher.create(None)

    pubSpec = _generateTestPayload()
    publisher = Publisher.create(pubSpec)
    assert isinstance(publisher, Publisher)

    del(pubSpec['address'])
    with pytest.raises(CoronadoUnprocessableObjectError):
        Publisher.create(pubSpec)

    pubSpec = _generateTestPayload()
    pubSpec['revenue_share'] = 'bogus'
    with pytest.raises(CoronadoUnprocessableObjectError):
        Publisher.create(pubSpec)


def test_Publisher_list():
    result = Publisher.list()

    assert len(result)

    publisherInfo = result[0]
    assert publisherInfo.objID


def test_Publisher_byID():
    result = Publisher.byID(KNOWN_PUB_ID)
    assert isinstance(result, Publisher)

    assert not Publisher.byID({ 'bogus': 'test'})
    assert not Publisher.byID(None)
    assert not Publisher.byID('bogus')


def test_Publisher_createDuplicateFail():
    p = Publisher.byID(KNOWN_PUB_ID)
    address = Address(p.address)
    pubSpec = {
        'address': address.asSnakeCaseDictionary(),
        'assumed_name': p.assumedName,
        'external_id': p.externalID,
        'revenue_share': p.revenueShare,
    }

    with pytest.raises(CoronadoDuplicatesDisallowedError):
        Publisher.create(pubSpec)


def test_Publisher_updateWith():
    address = _address.asSnakeCaseDictionary()

    control = 'OOO Kukla'
    orgName = Publisher.byID(KNOWN_PUB_ID).assumedName
    payload = { 'assumed_name' : control, 'address': address, }
    result = Publisher.updateWith(KNOWN_PUB_ID, payload)
    assert result.assumedName == control

    # Reset:
    payload['assumed_name'] = orgName
    Publisher.updateWith(KNOWN_PUB_ID, payload)

# TODO:  implement these tests after the underlying bug is fixed:
#     orgAddress = result.address
#     x = orgAddress.line2
#     control = 'Suite 303'
#     address['line2'] = control
#     payload = { 'address': address, }
#     result = Publisher.updateWith(KNOWN_PUB_ID, address)
#     assert result.address.postalCode == control
#
#     # Reset
#     payload['address'] = orgAddress
#     Publisher.updateWith(4, payload)


def test_Publisher_instanceByID():
    assert Publisher(KNOWN_PUB_ID).assumedName == KNOWN_ASSUMED_NAME


test_Publisher_create()

