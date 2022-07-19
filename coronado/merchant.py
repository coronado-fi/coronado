# vim: set fileencoding=utf-8:


from coronado import TripleObject
from coronado.baseobjects import BASE_MERCHANT_CATEGORY_CODE_DICT
from coronado.baseobjects import BASE_MERCHANT_DICT

import json


# +++ constants +++

SERVICE_PATH = 'partner/merchants'


# *** classes and objects ***


class MerchantCategoryCode(TripleObject):
    """
    A Merchant Category Code, or MCC, is a 4-digit number that indicates a line
    of business and the types of goods and services that the business provides
    to their customers.

    This class is often imported as:

    ```python
    from coronado.offers import MerchantCategoryCode as MCC
    ```

    <a href='https://www.merchantmaverick.com/merchant-category-code-mcc/' target='_blank'>Merchant Category Codes (MCC):</a>
    All You Need to Know from *Maverick Merchant*.
    """
    requiredAttributes = [ 'code', 'description', ]


    def __init__(self, obj = BASE_MERCHANT_CATEGORY_CODE_DICT):
        """
        Create a new MCC instance.

        spec:

        ```
        {
            'code': '4269',
            'description': 'Aquaria, Dolphinaria, Seaquaria, and Zoos',
        }
        ```
        """
        TripleObject.__init__(self, obj)


    def __str__(self):
        return '%s: %s' % (self.code, self.description)


    def asSnakeCaseDictionary(self) -> dict:
        """
        Return a dict representation of the receiver with the attributes
        written in snake_case format.

        Return
        ------
            A dict representation of the receiver.
        """
        return { 'code': self.code, 'description': self.description, }


class Merchant(TripleObject):
    """
    A Merchant associated with offers in the triple system.
    """
    def __init__(self, obj = BASE_MERCHANT_DICT):
        """
        Only partial implementation in the back-end
        ===========================================

        Create a new Merchant instance.
        """
        TripleObject.__init__(self, obj)


    @classmethod
    def list(klass: object, paramMap = None, **args) -> list:
        """
        Return a list of merchants.  The list is a seqwuential query from the
        beginning of time.

        Arguments
        ---------
            externalID
        Optional merchant external ID value to query for filtering

        Returns
        -------
            list
        A list of Merchant objects.  May return `None`.
        """
        paramMap = { 'externalID': 'merchant_external_id', }
        response = super().list(paramMap, **args)
        result = [ Merchant(obj) for obj in json.loads(response.content)['merchants'] ]
        return result

