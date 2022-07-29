# vim: set fileencoding=utf-8:


from coronado.address import Address
from coronado.auth import Auth
from coronado.auth import Scope
from coronado.exceptions import CallError
from coronado.exceptions import InvalidPayloadError
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
    'city': 'San Francisco',
    'countryCode': 'US',
    'countrySubdivisionCode': 'CA',
    'latitude': 0,
    'longitude': 0,
    'postalCode': '94118',
    'province': 'CA',
    'streetAddress': '2801 Turk Boulevard\\nSuite 202',
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
    with pytest.raises(CallError):
        Publisher.create(None)

    pubSpec = _generateTestPayload()
    publisher = Publisher.create(pubSpec)
    assert isinstance(publisher, Publisher)

    del(pubSpec['address'])
    with pytest.raises(CallError):
        Publisher.create(pubSpec)

    pubSpec = _generateTestPayload()
    pubSpec['external_id'] = '10'
    with pytest.raises(InvalidPayloadError):
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


def test_Publisher_instanceByID():
    assert Publisher(KNOWN_PUB_ID).assumedName == KNOWN_ASSUMED_NAME

