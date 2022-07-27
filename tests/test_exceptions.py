# vim: set fileencoding=utf-8:


from coronado.exceptions import ForbiddenError
from coronado.exceptions import UnexpectedError
from coronado.exceptions import errorFor


# +++ tests +++

def test_errorFor():
    details = "No permissions, fam!" 
    e = errorFor(403, details)

    assert isinstance(e, ForbiddenError)
    assert details == str(e)

    e = errorFor(-1)
    assert isinstance(e, UnexpectedError)

