# vim: set fileencoding=utf-8:


from coronado import CoronadoMalformedObjectError
from coronado import TripleObject
from coronado.auth import Auth
from coronado.auth import Scopes

import pytest

import coronado.auth as auth


# *** globals ***

_config = auth.loadConfig()


# +++ tests +++


