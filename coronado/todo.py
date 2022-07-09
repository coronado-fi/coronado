# class CardAccountIdentifier(TripleObject):
#     def __init__(self, obj = BASE_CARD_ACCOUNT_IDENTIFIER_DICT):
#         TripleObject.__init__(self, obj)
#
#         requiredAttributes = ['cardProgramExternalID', ]
#
#         self.assertAll(requiredAttributes)
#
#
# class MerchantCategoryCode(TripleObject):
#     def __init__(self, obj = BASE_MERCHANT_CATEGORY_CODE_DICT):
#         TripleObject.__init__(self, obj)
#
#         requiredAttributes = [ 'code', 'description', ]
#
#         self.assertAll(requiredAttributes)
#
#
# class MerchantLocation(TripleObject):
#     def __init__(self, obj = BASE_MERCHANT_LOCATION_DICT):
#         TripleObject.__init__(self, obj)
#
#         requiredAttributes = [ 'objID', 'isOnline', 'address', ]
#
#         self.assertAll(requiredAttributes)
#
#
# class OfferActivation(TripleObject):
#     def __init__(self, obj = BASE_OFFER_ACTIVATION_DICT):
#         TripleObject.__init__(self, obj)
#
#         requiredAttributes = ['objID', 'cardAccountID', 'activatedAt', 'offer', ]
#
#         self.assertAll(requiredAttributes)
#
#
# class OfferDisplayRules(TripleObject):
#     def __init__(self, obj = BASE_OFFER_DISPLAY_RULES_DICT):
#         TripleObject.__init__(self, obj)
#
#         requiredAttributes = ['action', 'scope', 'type', 'value', ]
#
#         self.assertAll(requiredAttributes)
#
#
# class Publisher(TripleObject):
#     def __init__(self, obj = BASE_PUBLISHER_DICT):
#         TripleObject.__init__(self, obj)
#
#         requiredAttributes = [ 'objID', 'assumedName', 'address', 'createdAt', 'updatedAt', ]
#
#         self.assertAll(requiredAttributes)
#
#
# class Reward(TripleObject):
#     def __init__(self, obj = BASE_REWARD_DICT):
#         TripleObject.__init__(self, obj)
#
#         requiredAttributes = [ 'transactionID', 'offerID', 'transactionDate', 'transactionAmount', 'transactionCurrencyCode', 'merchantName', 'status', ]
#
#         self.assertAll(requiredAttributes)
#
#
# class Transaction(TripleObject):
#     def __init__(self, obj = BASE_TRANSACTION_DICT):
#         TripleObject.__init__(self, obj)
#
#         requiredAttributes = [ 'objID', 'cardAccountID', 'externalID', 'localDate', 'debit', 'amount', 'currencyCode', 'transactionType', 'description', 'matchingStatus', 'createdAt', 'updatedAt', ]
#
#         self.assertAll(requiredAttributes)



