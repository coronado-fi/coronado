# vim: set fileencoding=utf-8:


from coronado import CoronadoDuplicatesDisallowedError
from coronado import CoronadoMalformedObjectError
from coronado import CoronadoUnprocessableObjectError
from coronado import TripleObject
from coronado.auth import Auth
from coronado.auth import Scope
from coronado.cardaccount import CardAccount
from coronado.cardaccount import CardAccountStatus
from coronado.cardaccount import SERVICE_PATH

import uuid

import pytest

import coronado.auth as auth


# +++ constants +++

KNOWN_ACCT_EXT_ID = 'pnc-card-69-3149b4780d6f4c2fa21fb45d2637efbb'
KNOWN_ACCT_ID = '1270'
KNOWN_CARD_PROG_EXT_ID = 'prog-66'
KNOWN_PUB_EXTERNAL_ID = '0d7c608a3df5'


# *** globals ***

_config = auth.loadConfig()
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scope.PUBLISHERS)


CardAccount.initialize(_config['serviceURL'], SERVICE_PATH, _auth)


# *** tests ***

def test_CardAccountStatus():
    x = CardAccountStatus('ENROLLED')

    assert x == CardAccountStatus.ENROLLED
    assert str(x) == 'ENROLLED'


def test_CardAccount_create():
    spec = {
        'card_program_external_id': KNOWN_CARD_PROG_EXT_ID,
        'external_id': 'pnc-card-69-%s' % uuid.uuid4().hex,
        'publisher_external_id': KNOWN_PUB_EXTERNAL_ID,
        'status': str(CardAccountStatus.ENROLLED),
    }

    account = CardAccount.create(spec)
    assert account

    with pytest.raises(CoronadoMalformedObjectError):
        CardAccount.create(None)

    spec['external_id'] = KNOWN_ACCT_EXT_ID
    with pytest.raises(CoronadoDuplicatesDisallowedError):
        CardAccount.create(spec)

    spec['external_id'] = '****'
    with pytest.raises(CoronadoUnprocessableObjectError):
        CardAccount.create(spec)



def test_CardAccount_list():
    accounts = CardAccount.list()

    assert isinstance(accounts, list)

    if len(accounts):
        account = accounts[0]
        assert isinstance(account, TripleObject)
        assert account.objID

    accounts = CardAccount.list(pubExternalID = KNOWN_PUB_EXTERNAL_ID)
    assert accounts[0].status == CardAccountStatus.ENROLLED.value

    accounts = CardAccount.list(pubExternalID = KNOWN_PUB_EXTERNAL_ID, cardAccountExternalID = KNOWN_ACCT_EXT_ID)
    assert accounts[0].status == CardAccountStatus.ENROLLED.value


def test_CardAccount_byID():
    result = CardAccount.byID(KNOWN_ACCT_ID)
    assert isinstance(result, CardAccount)

    assert not CardAccount.byID({ 'bogus': 'test'})
    assert not CardAccount.byID(None)
    assert not CardAccount.byID('bogus')


def test_CardAccount_updateWith():
    control = CardAccountStatus.NOT_ENROLLED
    payload = { 'status' : str(control), }
    obj  = CardAccount.updateWith(KNOWN_ACCT_ID, payload)
    assert obj.status == str(control)

    # Reset:
    payload['status'] = 'ENROLLED'
    CardAccount.updateWith(KNOWN_ACCT_ID, payload)

