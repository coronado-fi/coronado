# vim: set fileencoding=utf-8:


from coronado import CoronadoAPIError
from coronado import CoronadoMalformedObjectError
from coronado import CoronadoUnprocessableObjectError
from coronado.address import Address
from coronado.auth import Auth
from coronado.auth import Scopes
from coronado.publisher import Publisher

import uuid

import pytest

import coronado.auth as auth


# *** constants ***

KNOWN_PUB_ID = 4


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
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.PUBLISHERS)

Publisher.initialize(_config['serviceURL'], _auth)


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


@pytest.mark.skip('failed - underlying service has issues that need to be solved first')
def test_publisher_createDuplicateFail():
    pass


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


@pytest.mark.skip('failed - underlying service has issues that need to be solved first')
def test_Publisher_updateWith():
    address = _address.asSnakeCaseDictionary()
    address['postal_code'] = '99999'

    result = Publisher.updateWith(4, address)

    assert result

