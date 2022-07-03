# vim: set fileencoding=utf-8:


from coronado import CoronadoMalformedObjectError
from coronado import TripleObject
from coronado.baseobjects import BASE_PUBLISHER_DICT

import requests


# *** classes and objects ***

class Publisher(TripleObject):
    def __init__(self, obj = BASE_PUBLISHER_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = [ 'objID', 'assumedName', 'address', 'createdAt', 'updatedAt', ]

        self.assertAll(requiredAttributes)

