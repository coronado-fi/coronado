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
    def complete(self) -> str:
        """
        Return the receiver as a human-readable, multi-line complete address.
        Output format:

            line1\n
            locality, province, postalCode

        Return
        ------
            A string representation of the address.
        """
        completeAddress = '\n'.join([
            ('%s %s' % (self.line1, self.line2)).strip(),
            '%s, %s %s' % (self.locality, self.province, self.postalCode), ])

        return completeAddress
        

    def inSnakeCaseJSON(self) -> str:
        """
        Return a JSON representation of the receiver with the attributes
        written in snake_case format.

        Return
        ------
            A string with a JSON representation of the receiver.

        """
        return json.dumps(self.asSnakeCaseDictionary())


    def asSnakeCaseDictionary(self):
        """
        Return a dict representation of the receiver with the attributes 
        written in snake_case format.

        Return
        ------
            A dict representation of the receiver.
        """
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


    def __str__(self) -> str:
        return '%s\n%s\n%s, %s %s %s' % (
            self.line1,
            self.line2,
            self.locality,
            self.province,
            self.postalCode,
            self.countryCode,
        )

