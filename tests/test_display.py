# vim: set fileencoding=utf-8:


from coronado.auth import Auth
from coronado.display import CardLinkedOffer as CLOffer
from coronado.display import CardLinkedOfferDetails as CLOfferDetails
from coronado.display import FETCH_RPC_SERVICE_PATH
from coronado.display import OfferSearchResult
from coronado.display import SEARCH_RPC_SERVICE_PATH
from coronado.exceptions import CallError
from coronado.exceptions import UnexpectedError
from coronado.exceptions import UnprocessablePayload
from coronado.offer import OfferType

import pytest

import coronado.auth as auth


# *** constants ***

KNOWN_CARD_ID = '1270'
KNOWN_CARD_PROG_EXT_ID = 'prog-66'
KNOWN_OFFER_ID = '4862'
# KNOWN_OFFER_ID = '10953'


# *** globals ***

_config = auth.loadConfig()
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])


OfferSearchResult.initialize(_config['serviceURL'], SEARCH_RPC_SERVICE_PATH, _auth)
CLOfferDetails.initialize(_config['serviceURL'], FETCH_RPC_SERVICE_PATH, _auth)


# +++ tests +++

def test_OfferSearchResult_withQuery():
    # Known offers working query:
    spec = {
        "proximity_target": {
            "latitude": "40.4604548",
            "longitude": "-79.9215594",
            "radius": 35000
        },
        "card_account_identifier": {
            "card_account_id": KNOWN_CARD_ID
        },
        "text_query": "italian food",
        "page_size": 25,
        "page_offset": 0,
        "apply_filter": {
            "type": "CARD_LINKED"
        }
    }
    offers = OfferSearchResult.queryWith(spec = spec)

    assert isinstance(offers, list)
    assert len(offers)
    assert offers[0].objID

    spec['card_account_identifier']['card_account_id'] = 'BOGUS'
    with pytest.raises(UnprocessablePayload):
        OfferSearchResult.queryWith(spec = spec)

    del spec['proximity_target']
    with pytest.raises(CallError):
        OfferSearchResult.queryWith(spec = spec)


def test_OfferSearchResult_withQuery_args():
    offers = OfferSearchResult.queryWith(
                latitude = '40.46',
                longitude = '-79.92',
                radius = 35000,
                cardAccountID = KNOWN_CARD_ID,
                textQuery = 'Italian food',
                pageSize = 25,
                pageOffset = 0,
                filterType = OfferType.CARD_LINKED)

    assert isinstance(offers, list)
    assert len(offers)
    assert offers[0].objID

    with pytest.raises(CallError):
        OfferSearchResult.queryWith(
                latitude = '40.46',
                longitude = '-79.92',
                radius = 35000,
                textQuery = 'Italian food',
                pageSize = 25,
                pageOffset = 0,
                filterType = OfferType.CARD_LINKED)

    with pytest.raises(CallError):
        OfferSearchResult.queryWith(
                radius = 35000,
                cardAccountID = KNOWN_CARD_ID,
                textQuery = 'Italian food',
                pageSize = 25,
                pageOffset = 0,
                filterType = OfferType.CARD_LINKED)


def test_CLOfferDetails_forID():
    spec = {
        "proximity_target": {
            "latitude": "40.4604548",
            "longitude": "-79.9215594",
            "radius": 35000
        },
        "card_account_identifier": {
            "card_account_id": KNOWN_CARD_ID
        },
    }
    # offerDetails = CLOfferDetails.forID(KNOWN_OFFER_ID, spec)
    offerDetails = CLOfferDetails.forID('4930', spec = spec)

    assert isinstance(offerDetails, CLOfferDetails)
    assert isinstance(offerDetails.offer, CLOffer)

    # TODO:  All of these need to test against specific exceptions,
    #        this is good enough for this release.
    with pytest.raises(UnexpectedError):
        CLOfferDetails.forID('BOGUs', spec = spec)

    with pytest.raises(UnexpectedError):
        CLOfferDetails.forID('0', spec = spec)
        
    spec['card_account_identifier']['card_account_id'] = 'bOGuz'
    with pytest.raises(UnprocessablePayload):
        CLOfferDetails.forID(KNOWN_OFFER_ID, spec = spec)

    spec['card_account_identifier']['card_account_id'] = '0'
    with pytest.raises(UnprocessablePayload):
        offerDetails = CLOfferDetails.forID(KNOWN_OFFER_ID, spec = spec)

    del spec['card_account_identifier']
    with pytest.raises(CallError):
        CLOfferDetails.forID(KNOWN_OFFER_ID, spec = spec)

    with pytest.raises(CallError):
        CLOfferDetails.forID(KNOWN_OFFER_ID, postalCode = '94123')

