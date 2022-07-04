# vim: set fileencoding=utf-8:


from coronado import TripleObject
from coronado.baseobjects import BASE_ADDRESS_DICT

import json


# +++ classes and objects +++

class Address(TripleObject):
    def __init__(self, obj = BASE_ADDRESS_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = [ 'completeAddress', ]

        self.assertAll(requiredAttributes)

        self.completeAddress = 'WARNING:  USE the .complete attribute instead of .completeAddress'


    @property
    def complete(self):
        completeAddress = '\n'.join([
            self.line1,
            self.line2,
            '%s, %s %s' % (self.locality, self.province, self.postalCode), ])

        return completeAddress
        

    def inSnakeCaseJSON(self):
        return json.dumps(self.asSnakeCaseDictionary())


    def asSnakeCaseDictionary(self):
        result = {
            'complete_address': self.complete,
            'country_code': self.countryCode,
            'latitude': self.latitude,
            'line_1': self.line1,
            'line_2': self.line2,
            'locality': self.locality,
            'longitude': self.longitude,
            'postal_code': self.postalCode,
            'province': self.province,
        }

        return result

