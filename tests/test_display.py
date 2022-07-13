# vim: set fileencoding=utf-8:


from coronado import CoronadoAPIError
from coronado import CoronadoUnprocessableObjectError
from coronado.auth import Auth
from coronado.display import OfferSearchResult
from coronado.display import CLOfferDetails
from coronado.display import SERVICE_PATH

import pytest

import coronado.auth as auth


# *** constants ***

KNOWN_CARD_ID = '2'
KNOWN_CARD_PROG_EXT_ID = 'prog-5a4d1563410c4ff687d8a6fa8c208fe8'
# KNOWN_OFFER_ID = '4862'
KNOWN_OFFER_ID = '10953'


# *** globals ***

_config = auth.loadConfig()
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])


classes = [ OfferSearchResult, CLOfferDetails, ]
for c in classes:
    c.initialize(_config['serviceURL'], SERVICE_PATH, _auth)


# +++ tests +++

def test_OfferSearchResult_searchFor():
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
    offers = OfferSearchResult.forQuery(spec)

    assert isinstance(offers, list)
    assert len(offers)
    assert offers[0].objID

    spec['card_account_identifier']['card_account_id'] = 'BOGUS'
    with pytest.raises(CoronadoAPIError):
        OfferSearchResult.forQuery(spec)

    del spec['proximity_target']
    with pytest.raises(CoronadoUnprocessableObjectError):
        OfferSearchResult.forQuery(spec)


@pytest.mark.skip('offer details API errors')
def test_CLOfferDetails_forID():
    offerDetails = CLOfferDetails.forID(KNOWN_OFFER_ID)

    assert offerDetails


# test_CLOfferDetails_forID()

