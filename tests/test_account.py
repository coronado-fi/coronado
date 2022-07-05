# vim: set fileencoding=utf-8:


from coronado import CoronadoMalformedObjectError
from coronado import TripleObject
from coronado.account import CardAccount
from coronado.account import CardAccountStatus
from coronado.auth import Auth
from coronado.auth import Scopes

import pytest

import coronado.auth as auth


# *** globals ***

_config = auth.loadConfig()
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], scope = Scopes.PUBLISHERS)


CardAccount.serviceURL = _config['serviceURL']
CardAccount.auth = _auth


# *** tests ***

def test_CardAccount_list():
    accounts = CardAccount.list()

    assert isinstance(accounts, list)

    if len(accounts):
        account = accounts[0]
        assert isinstance(account, TripleObject)
        assert account.objID


@pytest.mark.skip('failed - underlying service has issues that need to be solved first')
def test_CardAccount_create():
    accountSpec = {
        'card_program_external_id': 'rebates-nation-24',
        # TODO:  file bug
        # 'external_id': 'PNC-card-69',
        'external_id': 'pnc-card-69',
        'status': CardAccountStatus.ENROLLED.value,
        # TODO:  file bug for Matt
        # 'publisher_external_id': 'PNCBANK',
        'publisher_external_id': 'pncbank',
    }

    with pytest.raises(CoronadoMalformedObjectError):
        CardAccount.create(None)
    
    account = CardAccount.create(accountSpec)

    assert account
    # TODO:  finish the implementation; handle 422, other errors
    


def test_CardAccount_byID():
    accountID = 'bogusID'

    account = CardAccount.byID(accountID)

    assert not account

# test_CardAccount_create()
# test_CardAccount_byID()

