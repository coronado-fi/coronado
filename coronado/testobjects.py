# vim: set fileencoding=utf-8:


import json


TEST_CARD_ACCOUNT_JSON = """{
    "id": "triple-abc-123",
    "card_program_id": "triple-abc-123",
    "external_id": "string",
    "status": "ENROLLED",
    "created_at": "2021-12-01T01:59:59.000Z",
    "updated_at": "2021-12-01T01:59:59.000Z"

}"""
TEST_CARD_ACCOUNT_DICT = json.loads(TEST_CARD_ACCOUNT_JSON)


TEST_CARD_ACCOUNT_IDENTIFIER_JSON = """{
  "publisher_external_id": "string",
  "card_program_external_id": "string",
  "external_id": "string",
  "status": "ENROLLED"
}"""
TEST_CARD_ACCOUNT_IDENTIFIER_DICT = json.loads(TEST_CARD_ACCOUNT_IDENTIFIER_JSON)

TEST_CARD_PROGRAM_JSON = """{
  "id": "triple-abc-123",
  "publisher_id": "triple-abc-123",
  "external_id": "string",
  "name": "string",
  "program_currency": "USD",
  "card_bins": [
    "444789"
  ],
  "created_at": "2021-12-01T01:59:59.000Z",
  "updated_at": "2021-12-01T01:59:59.000Z"
}"""
TEST_CARD_PROGRAM_DICT = json.loads(TEST_CARD_PROGRAM_JSON)

TEST_OFFER_ACTIVATIONS_JSON="""{
  "offer_activations": [
    {
      "id": "triple-abc-123",
      "card_account_id": "triple-abc-123",
      "activated_at": "2019-08-24",
      "activation_expires_on": "2019-08-24",
      "offer": {
        "id": "triple-abc-123",
        "type": "CARD_LINKED",
        "headline": "string",
        "reward_rate": 0,
        "reward_type": "FIXED",
        "reward_value": 0,
        "currency_code": "USD"
      },
      "merchant": {
        "name": "string",
        "logo_url": "string"
      }
    }
  ]
}"""
TEST_OFFER_ACTIVATIONS_DICT=json.loads(TEST_OFFER_ACTIVATIONS_JSON)

