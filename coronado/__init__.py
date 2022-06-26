# vim: set fileencoding=utf-8:


from copy import deepcopy

from coronado.tools import tripleKeysToCamelCase

import json


# *** constants ***

__VERSION__ = '1.0.0'


# +++ classes and objects +++

class CoronadoMalformedObject(Exception):
    pass


class TripleObject(object):
    # +++ public +++

    def __init__(self, obj = None):
        if isinstance(obj, str):
            d = json.loads(obj)
        elif isinstance(obj, dict):
            d = deepcopy(obj)
        else:
            raise CoronadoMalformedObject

        d = tripleKeysToCamelCase(d)

        for key, value in d.items():
            if isinstance(value, (list, tuple)):
                setattr(self, key, [TripleObject(x) if isinstance(x, dict) else x for x in value])
            else:
                setattr(self, key, TripleObject(value) if isinstance(value, dict) else value)


    def assertAll(self, requiredAttributes: list) -> bool:
        if not all(attribute in self.__dict__.keys() for attribute in requiredAttributes):
            raise CoronadoMalformedObject("missing attributes during instantiation")


class CardAccountIdentifier(TripleObject):
    def __init__(self, obj = None):
        TripleObject.__init__(self, obj)

        requiredAttributes = ['cardProgramExternalID', ]

        self.assertAll(requiredAttributes)


class CardAccount(TripleObject):
    def __init__(self, obj = None):
        TripleObject.__init__(self, obj)

        requiredAttributes = ['objID', 'cardProgramID', 'externalID', 'status', 'createdAt', 'updatedAt', ]

        self.assertAll(requiredAttributes)


class CardProgram(TripleObject):
    def __init__(self, obj = None):
        TripleObject.__init__(self, obj)

        requiredAttributes = ['externalID', 'name', 'programCurrency', ]

        self.assertAll(requiredAttributes)


class OfferActivations(TripleObject):
    def __init__(self, obj = None):
        TripleObject.__init__(self, obj)

        requiredAttributes = ['offerActivations', ]

        self.assertAll(requiredAttributes)

