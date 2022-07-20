# vim: set fileencoding=utf-8:


from coronado import CoronadoAPIError
from coronado import TripleObject
from coronado.baseobjects import BASE_MERCHANT_CATEGORY_CODE_DICT

import iso18245


# +++ classes +++

class MerchantCategoryCode(TripleObject):
    """
    ISO-18245 merchant category codes implementation.  Leverages the Python
    package <a href='https://pypi.org/project/iso18245/' target='_blank'>iso18245</a> for code resolution and validation.
    """
    def __init__(self, obj):
        if isinstance(obj, TripleObject):
            TripleObject.__init__(self, obj = obj)
            return
        else:
            TripleObject.__init__(self, obj = BASE_MERCHANT_CATEGORY_CODE_DICT)

        try:
            self.description = None
            categoryInfo = iso18245.get_mcc(obj)
        except iso18245.MCCNotFound:
            self.description = str(iso18245.get_mcc_range(obj).description)

        self.code = obj 
        if not self.description:
            self.description = str(
                categoryInfo.iso_description
                or categoryInfo.stripe_description
                or categoryInfo.visa_description
                or categoryInfo.range.description
            )


    @classmethod
    def list(klass, paraMap = None, **args) -> list:
        """
        List all the MCCs known to the triple systems.  Full range is between 0000 and 
        9999, inclusive.  Ranges must be expressed as 4-digit strings.

        Arguments
        ---------
            begin : str
        The starting code for listing a range (inclusive).

            end : str
        The ending code for listing a range (inclusive).

        Returns
        -------
            list
        A list of `MerchantCategoryCode` objects, or `None` if empty.

        Raises
        ------

        """
        begin = '0000'
        end = '9999'

        if len(args):
            requiredArgs = ['begin', 'end', ]
            if not all(arg in args.keys() for arg in requiredArgs):
                missing = set(requiredArgs)-set(args.keys())
                raise CoronadoAPIError("arg%s %s missing during instantiation" % ('' if len(missing) == 1 else 's', missing))
            begin = args['begin']
            end = args['end']
        merchantCodes = [ MerchantCategoryCode(code) for code in sorted([ catInfo.mcc for catInfo in iso18245.get_all_mccs_in_range(begin, end) ]) ]

        return merchantCodes


    @classmethod
    def create(klass, spec: dict) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def byID(klass, objID: str) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def updateWith(klass, objID: str, spec: dict) -> object:
        """
        **Disabled for this class.**
        """
        None

