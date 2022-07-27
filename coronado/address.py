# vim: set fileencoding=utf-8:
"""
DEPRECATED
==========
This implementation of Address is invalid and will stop working by 01.Aug.2022.
The Address class (like most objects in this package), its attributes, and 
semantics conform to the **triple Card Linked Offer Ontology**.

Please review `coronado.address_cloo.AddressCLOO` for details on how the objects
and behaviors in this module changed.

Also review:

- `coronado.baseobjects.BASE_ADDRESS_DICT`
- `coronado.baseobjects.BASE_ADDRESS_JSON`
"""


from coronado import TripleObject
from coronado.baseobjects import BASE_ADDRESS_DICT

import json


# TODO:  Review https://github.com/mirumee/google-i18n-address


# +++ classes and objects +++

class Address(TripleObject):
    """
    Address object that provides a high-level definition for address components
    that meets ontological and physical address standards.  An address is a kind
    of index that describes a physical location to which communications may be
    delivered.

    This Address class doesn't meet the full ontological criteria for a complete
    address because it doesn't separate building number, subdivisions, and other
    attributes.

    Future implementations may parse the `.line` and `.line2` attributes to
    separate distinct items like the buildingNumber from streetName or
    equivalent to fit a standard address schema.

    This Address implementation is equivalent to the <a href='https://spec.edmcouncil.org/fibo/ontology/FND/Places/NorthAmerica/USPostalServiceAddresses/GeneralDeliveryAddress' target='_blank'>FIBO GeneralDeliveryAddress</a>
    class.
    """

    requiredAttributes = [ 'completeAddress', ]


    def __init__(self, obj = BASE_ADDRESS_DICT):
        """
        Create a new instance of an address.  `obj` must correspond to a
        valid, existing object ID if it's not a collection or JSON.

        obj specification:

        ```
        Address({
            # We made it a requirement but we'll toss it in the instances:
            'complete_address': '',
            'countryCode': 'US',
            'latitude': 37.802821,
            'line1': '1233 Francisco Street',
            'line2': 'Suite 202',
            'locality': 'San Francisco',
            'longitude': -122.425486,
            'postalCode': '94123',
            'province': 'CA',
        })
        ```

        Arguments
        ---------
            obj
        An object used for building a valid address.  The object can
        be one of:

        - A dictionary - a dictionary with instantiation values as described
          in the API documentation
        - A JSON string
        - A triple objectID

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the 
        **`coronado.exceptions`** module.
        """
        TripleObject.__init__(self, obj)
        self.completeAddress = 'WARNING:  USE .complete instead of .completeAddress'


    @property
    def complete(self) -> str:
        """
        Return the receiver as a human-readable, multi-line complete address.
        Output format:

            line1\\n
            locality, province, postalCode

        Return
        ------
            A string representation of the address.
        """
        completeAddress = '\n'.join([
            ('%s %s' % (self.line1, self.line2)).strip(),
            '%s, %s %s' % (self.locality, self.province, self.postalCode), ])

        return completeAddress


    def asSnakeCaseDictionary(self) -> dict:
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

