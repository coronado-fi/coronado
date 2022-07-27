# vim: set fileencoding=utf-8:


from i18naddress import InvalidAddress as InvalidAddressError
from i18naddress import format_address as formatAddress
from i18naddress import normalize_address as normalizeAddress

from coronado import TripleObject
from coronado.baseobjects import BASE_ADDRESS_CLOO_DICT
from coronado.exceptions import InvalidPayloadError


# Ref: https://github.com/mirumee/google-i18n-address
# Ref: https://pypi.org/project/google-i18n-address


# +++ classes and objects +++

class AddressCLOO(TripleObject):
    """
    AddressCLOO object that provides a high-level definition for address components
    that meets ontological and physical address standards.  An address is a kind
    of index that describes a physical location to which communications may be
    delivered.

    This AddressCLOO class doesn't meet the full ontological criteria for a complete
    address because it doesn't separate building number, subdivisions, and other
    attributes.

    Future implementations may parse the `streetAddress` attribute to separate 
    distinct items like the buildingNumber from streetName or equivalent to fit
    a standard address schema.
    """

    requiredAttributes = [
        'countryCode',
        'postalCode',
        'streetAddress',
    ]


    def __init__(self, obj = BASE_ADDRESS_CLOO_DICT):
        """
        Create a new instance of an address.  `obj` must correspond to a
        valid, existing object ID if it's not a collection or JSON.

        spec:

        ```python
        Address({
            'country_code': 'US',
            'country_subdivision_code': 'PA',
            'latitude': 40.440624,
            'city': 'PITTSBURGH',
            'longitude': -79.995888,
            'postal_code': '15206',
            'street_address': '7370 BAKER ST'
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
        if 'completeAddress' in self.__dict__:
            raise InvalidPayloadError('completeAddress (complete_address) is a deprecated invalid attribute')


    @property
    def complete(self) -> str:
        """
        Return the receiver as a human-readable, multi-line complete address.
        The output will be formatted according to the value of the the 
        `countryCode` attribute.

        Return
        ------
            str
        A text representation of the address.
        """
        addressElements = {
            'city': self.city,
            'country_code': self.countryCode,
            'country_area': self.countrySubdivisionCode,
            'postal_code': self.postalCode,
            'street_address': self.streetAddress,
        }

        try:
            addressElements = normalizeAddress(addressElements)
            return formatAddress(addressElements)
        except InvalidAddressError as e:
            raise InvalidPayloadError(str(e.errors))


    def asSnakeCaseDictionary(self) -> dict:
        """
        Return a dict representation of the receiver with the attributes
        written in snake_case format.

        Return
        ------
            dict
        A dict representation of the receiver.
        """
        result = {
            'complete_address': self.complete,
            'country_code': self.countryCode,
            'country_subdivision_code': self.countrySubdivisionCode,
            'latitude': self.latitude,
            'city': self.city,
            'longitude': self.longitude,
            'postal_code': self.postalCode,
            'street_address': self.streetAddress,
        }

        return result


    def __str__(self) -> str:
        return self.complete

