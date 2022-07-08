# vim: set fileencoding=utf-8:


from coronado import CoronadoMalformedObjectError
from coronado import TripleObject
from coronado.account import CardAccount
from coronado.account import CardAccountStatus
from coronado.auth import Auth
from coronado.auth import Scopes

import uuid

import pytest

import coronado.auth as auth


# *** globals ***

_config = auth.loadConfig()
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.PUBLISHERS)


<<<<<<< HEAD
CardAccount.initialize(_config['serviceURL'], _auth)
=======
CardAccount._serviceURL = _config['serviceURL']
CardAccount._auth = _auth
>>>>>>> dev


# *** tests ***

def test_CardAccount_list():
    accounts = CardAccount.list()

    assert isinstance(accounts, list)

    if len(accounts):
        account = accounts[0]
        assert isinstance(account, TripleObject)
        assert account.objID

    accounts = CardAccount.list(pubExternalID = '4')


def test_CardAccount_create():
    spec = {
        'card_program_external_id': 'rebates-nation-24',
        'external_id': 'pnc-card-69',
        'publisher_external_id': 'pncbank',
        'status': CardAccountStatus.ENROLLED.value,
    }

    with pytest.raises(CoronadoMalformedObjectError):
        CardAccount.create(None)
    
    account = CardAccount.create(spec)

    assert account
    # TODO:  finish the implementation; handle 422, other errors



def test_CardAccount_byID():
    accountID = 'bogusID'

    account = CardAccount.byID(accountID)

    assert not account

# test_CardAccount_list()
test_CardAccount_create()
# test_CardAccount_byID()

