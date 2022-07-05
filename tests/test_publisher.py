# vim: set fileencoding=utf-8:


from copy import deepcopy

from coronado import CoronadoMalformedObjectError
from coronado import CoronadoUnprocessableObjectError
from coronado.address import Address
from coronado.auth import Auth
from coronado.auth import Scopes
from coronado.publisher import Publisher

import pytest

import coronado.auth as auth


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

_publisher_sn = {  # sn ::= snake case
    'address': _address.asSnakeCaseDictionary(),
    'assumed_name': 'R2D2 Enterprises, LLC',
    'external_id': '6942',
    'revenue_share': 1.5,
}

Publisher.serviceURL = _config['serviceURL']
Publisher.auth = _auth


# +++ tests +++

@pytest.mark.skip('failed - underlying service has issues that need to be solved first')
def test_Publisher_create():
    with pytest.raises(CoronadoMalformedObjectError):
        Publisher.create(None)
    
    pubSpec = deepcopy(_publisher_sn)
    publisher = Publisher.create(pubSpec)

    del(pubSpec['address'])
    with pytest.raises(CoronadoUnprocessableObjectError):
        Publisher.create(pubSpec)

    assert publisher
    # TODO:  finish the implementation; handle 422, other errors
    # TODO: 500 on what should be successful creation


def test_Publisher_list():
    result = Publisher.list()

    assert len(result)

    publisherInfo = result[0]
    assert publisherInfo.objID


@pytest.mark.skip('failed - underlying service has issues that need to be solved first')
def test_Publisher_byID():
    result = Publisher.byID(4)

    assert result
    # TODO: 500 on what should be successful request


@pytest.mark.skip('failed - underlying service has issues that need to be solved first')
def test_Publisher_updateWith():
    address = _address.asSnakeCaseDictionary()
    address['postal_code'] = '99999'

    result = Publisher.updateWith(4, address)

    assert result


# test_Publisher_create()
# test_Publisher_list()
# test_Publisher_byID()
# test_Publisher_updateWith()

