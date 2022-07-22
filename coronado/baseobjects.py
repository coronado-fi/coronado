# vim: set fileencoding=utf-8:


import json


# If you copy/paste the JSON spec here, remember to escape the \n to prevent
# JSON parser errros.
BASE_ADDRESS_JSON = """{
    "complete_address": "7370 BAKER ST STE 100\\nPITTSBURGH, PA 15206",
    "line_1": "7370 BAKER ST",
    "line_2": "SUITE 100",
    "locality": "PITTSBURGH",
    "province": "PA",
    "postal_code": "15206",
    "country_code": "US",
    "latitude": 40.440624,
    "longitude": -79.995888
}"""
BASE_ADDRESS_DICT = json.loads(BASE_ADDRESS_JSON)


BASE_CARD_ACCOUNT_JSON = """{
    "id": "triple-abc-123",
    "card_program_id": "triple-abc-123",
    "external_id": "string",
    "status": "ENROLLED",
    "created_at": "2021-12-01T01:59:59.000Z",
    "updated_at": "2021-12-01T01:59:59.000Z"

}"""
BASE_CARD_ACCOUNT_DICT = json.loads(BASE_CARD_ACCOUNT_JSON)


BASE_CARD_ACCOUNT_IDENTIFIER_JSON = """{
  "publisher_external_id": "string",
  "card_program_external_id": "string",
  "external_id": "string",
  "status": "ENROLLED"
}"""
BASE_CARD_ACCOUNT_IDENTIFIER_DICT = json.loads(BASE_CARD_ACCOUNT_IDENTIFIER_JSON)


BASE_CARD_PROGRAM_JSON = """{
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
BASE_CARD_PROGRAM_DICT = json.loads(BASE_CARD_PROGRAM_JSON)


BASE_MERCHANT_CATEGORY_CODE_JSON = """{
    "code": "7998",
    "description": "Aquaria, Dolphinaria, Seaquaria, and Zoos"
}"""
BASE_MERCHANT_CATEGORY_CODE_DICT = json.loads(BASE_MERCHANT_CATEGORY_CODE_JSON)


BASE_MERCHANT_JSON = """{
  "id": "triple-abc-123",
  "external_id": "string",
  "assumed_name": "string",
  "address": {
    "complete_address": "7370 BAKER ST STE 100\\nPITTSBURGH, PA 15206",
    "line_1": "7370 BAKER ST STE 100",
    "line_2": "string",
    "locality": "PITTSBURGH",
    "province": "PA",
    "postal_code": "15206",
    "country_code": "US",
    "latitude": 40.440624,
    "longitude": -79.995888
  },
  "merchant_category_code": {
    "code": "7998",
    "description": "Aquariums, Dolphinariums, Seaquariums, and Zoos"
  },
  "logo_url": "string"
}"""
BASE_MERCHANT_DICT = json.loads(BASE_MERCHANT_JSON)


BASE_MERCHANT_LOCATION_JSON = """{
    "id": "triple-abc-123",
    "location_name": "string",
    "is_online": true,
    "email": "string",
    "phone_number": "string",
    "address": {
        "complete_address": "7370 BAKER ST STE 100\\nPITTSBURGH, PA 15206",
        "line_1": "7370 BAKER ST STE 100",
        "line_2": "string",
        "locality": "PITTSBURGH",
        "province": "PA",
        "postal_code": "15206",
        "country_code": "US",
        "latitude": 40.440624,
        "longitude": -79.995888
    }
}"""
BASE_MERCHANT_LOCATION_DICT = json.loads(BASE_MERCHANT_LOCATION_JSON)


# Ontological mapping foundation

# TODO:  Clarify with the KDR and implementation teams:
#   "description": "string",
BASE_OFFER_JSON = """
{
  "activation_required": true,
  "category": "AUTOMOTIVE",
  "category_tags": "string",
  "currency_code": "USD",
  "effective_date": "2021-12-01",
  "expiration_date": "2021-12-31",
  "headline": "string",
  "id": "triple-abc-123",
  "is_activated": false,
  "max_redemptions": "1/3M",
  "mode": "ONLINE",
  "type": "CARD_LINKED"
}
"""
BASE_OFFER_DICT = json.loads(BASE_OFFER_JSON)


BASE_MERCHANT_OFFER_JSON = """
{
  "activation_required": true,
  "category": "AUTOMOTIVE",
  "category_tags": "string",
  "currency_code": "USD",
  "effective_date": "2021-12-01",
  "expiration_date": "2021-12-31",
  "headline": "string",
  "id": "triple-abc-123",
  "is_activated": false,
  "max_redemptions": "1/3M",
  "mode": "ONLINE",
  "type": "CARD_LINKED",


  "activation_duration_in_days": 0,
  "category_mccs": [
    {
      "code": "7998",
      "description": "Aquariums, Dolphinariums, Seaquariums, and Zoos"
    }
  ],
  "description": "string",
  "excluded_dates": [
    "2021-12-25"
  ],
  "external_id": "string",
  "logo_url": "string",
  "marketing_fee": 0,
  "marketing_fee_currency_code": "USD",
  "marketing_fee_type": "FIXED",
  "maximum_reward_cumulative": 0,
  "maximum_reward_per_transaction": 0,
  "merchant_id": "triple-abc-123",
  "merchant_website": "string",
  "minimum_spend": 0,
  "reward_rate": 0,
  "reward_type": "FIXED",
  "reward_value": 0,
  "terms_and_conditions": "string",
  "valid_day_parts": {
    "sunday": {
      "times": [
        "00:30-13:30"
      ]
    },
    "monday": {
      "times": [
        "00:30-13:30"
      ]
    },
    "tuesday": {
      "times": [
        "00:30-13:30"
      ]
    },
    "wednesday": {
      "times": [
        "00:30-13:30"
      ]
    },
    "thursday": {
      "times": [
        "00:30-13:30"
      ]
    },
    "friday": {
      "times": [
        "00:30-13:30"
      ]
    },
    "saturday": {
      "times": [
        "00:30-13:30"
      ]
    }
  }
}
"""
BASE_MERCHANT_OFFER_DICT = json.loads(BASE_MERCHANT_OFFER_JSON)


BASE_OFFER_ACTIVATION_JSON = """{
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
}"""
BASE_OFFER_ACTIVATION_DICT=json.loads(BASE_OFFER_ACTIVATION_JSON)


BASE_CLOFFER_DETAILS_JSON = """
{
  "offer": {
    "id": "triple-abc-123",
    "activation_required": true,
    "activation_duration_in_days": 0,
    "currency_code": "USD",
    "category": "AUTOMOTIVE",
    "category_tags": "string",
    "category_mccs": [
      {
        "code": "7998",
        "description": "Aquariums, Dolphinariums, Seaquariums, and Zoos"
      }
    ],
    "description": "string",
    "effective_date": "2021-12-01",
    "excluded_dates": [
      "2021-12-25"
    ],
    "expiration_date": "2021-12-31",
    "is_activated": false,
    "headline": "string",
    "max_redemptions": "1/3M",
    "maximum_reward_per_transaction": 0,
    "maximum_reward_cumulative": 0,
    "merchant_category_code": {
      "code": "7998",
      "description": "Aquariums, Dolphinariums, Seaquariums, and Zoos"
    },
    "merchant_name": "string",
    "merchant_logo_url": "string",
    "minimum_spend": 0,
    "mode": "ONLINE",
    "reward_rate": 0,
    "reward_value": 0,
    "reward_type": "CARD_LINKED",
    "type": "CARD_LINKED",
    "valid_day_parts": {
      "sunday": {
        "times": [
          "00:30-13:30"
        ]
      },
      "monday": {
        "times": [
          "00:30-13:30"
        ]
      },
      "tuesday": {
        "times": [
          "00:30-13:30"
        ]
      },
      "wednesday": {
        "times": [
          "00:30-13:30"
        ]
      },
      "thursday": {
        "times": [
          "00:30-13:30"
        ]
      },
      "friday": {
        "times": [
          "00:30-13:30"
        ]
      },
      "saturday": {
        "times": [
          "00:30-13:30"
        ]
      }
    },
    "terms_and_conditions": "string",
    "merchant_website": "string"
  },
  "merchant_locations": [
    {
      "id": "triple-abc-123",
      "location_name": "string",
      "is_online": true,
      "email": "string",
      "phone_number": "string",
      "address": {
        "complete_address": "7370 BAKER ST STE 100\\nPITTSBURGH, PA 15206",
        "line_1": "7370 BAKER ST STE 100",
        "line_2": "string",
        "locality": "PITTSBURGH",
        "province": "PA",
        "postal_code": "15206",
        "country_code": "US",
        "latitude": 40.440624,
        "longitude": -79.995888
     }
    }
  ]
}
"""
BASE_CLOFFER_DETAILS_DICT = json.loads(BASE_CLOFFER_DETAILS_JSON)


BASE_OFFER_SEARCH_RESULT_JSON = """{
    "activation_required": true,
    "category": "AUTOMOTIVE",
    "category_tags": "string",
    "currency_code": "USD",
    "effective_date": "2021-12-01",
    "expiration_date": "2021-12-31",
    "headline": "string",
    "id": "triple-abc-123",
    "is_activated": false,
    "max_redemptions": "1/3M",
    "mode": "ONLINE",
    "type": "CARD_LINKED",

    "external_id": "string",
    "maximum_reward_per_transaction": 0,
    "merchant_id": "triple-abc-123",
    "merchant_logo_url": "string",
    "minimum_spend": 0,
    "reward_rate": 0,
    "reward_type": "FIXED",
    "reward_value": 0,
    "score": 0,
    "type": "CARD_LINKED",
    "nearest_location": 

    {
        "complete_address": "7370 BAKER ST STE 100\\nPITTSBURGH, PA 15206",
        "latitude": 40.440624,
        "longitude": -79.995888
    }

}"""
BASE_OFFER_SEARCH_RESULT_DICT = json.loads(BASE_OFFER_SEARCH_RESULT_JSON)


BASE_OFFER_DISPLAY_RULES_JSON = """{ "id": "triple-abc-123",
    "description": "string",
    "enabled": true,
    "scope":
    {

        "level": "PORTFOLIO_MANAGER",
        "id": "triple-abc-123",
        "name": "string"

    },
    "type": "MERCHANT_NAME_EQUAL_TO",
    "value": "string",
    "action": "EXCLUDE"
}"""
BASE_OFFER_DISPLAY_RULES_DICT = json.loads(BASE_OFFER_DISPLAY_RULES_JSON)


BASE_PUBLISHER_JSON = """{
    "id": "triple-abc-123",
    "portfolio_manager_id": "triple-abc-123",
    "external_id": "string",
    "assumed_name": "string",
    "address":
    {
        "complete_address": "7370 BAKER ST STE 100\\nPITTSBURGH, PA 15206",
        "line_1": "7370 BAKER ST STE 100",
        "line_2": "string",
        "locality": "PITTSBURGH",
        "province": "PA",
        "postal_code": "15206",
        "country_code": "US",
        "latitude": 40.440624,
        "longitude": -79.995888

    },
    "revenue_share": 1.125,
    "created_at": "2021-12-01T01:59:59.000Z",
    "updated_at": "2021-12-01T01:59:59.000Z"
}"""
BASE_PUBLISHER_DICT = json.loads(BASE_PUBLISHER_JSON)


BASE_REWARD_JSON = """{
    "card_bin": "444789",
    "card_last_4": "stri",
    "merchant_complete_address": "7370 BAKER ST STE 100\\nPITTSBURGH, PA 15206",
    "merchant_name": "string",
    "offer_external_id": "string",
    "offer_headline": "string",
    "offer_id": "triple-abc-123",
    "reward_amount": 0,
    "reward_currency_code": "USD",
    "reward_details": "Lorem ipsum dolot sit hamet with a cherry.",
    "status": "REJECTED",
    "transaction_amount": 12,
    "transaction_currency_code": "USD",
    "transaction_date": "2022-05-31T15:34:22-0400",
    "transaction_id": "triple-abc-123"
}"""
BASE_REWARD_DICT = json.loads(BASE_REWARD_JSON)


BASE_TRANSACTION_JSON = """{
    "id": "triple-abc-123",
    "card_account_id": "triple-abc-123",
    "external_id": "string",
    "local_date": "2021-12-01",
    "local_time": "13:45:00",
    "debit": true,
    "amount": 12,
    "currency_code": "USD",
    "transaction_type": "PURCHASE",
    "description": "Pittsburgh Zoo",
    "merchant_category_code":
    {

        "code": "7998",
        "description": "Aquariums, Dolphinariums, Seaquariums, and Zoos"

    },
    "merchant_address":
    {

        "complete_address": "7370 BAKER ST STE 100\\nPITTSBURGH, PA 15206",
        "line_1": "7370 BAKER ST STE 100",
        "line_2": "string",
        "locality": "PITTSBURGH",
        "province": "PA",
        "postal_code": "15206",
        "country_code": "US",
        "latitude": 40.440624,
        "longitude": -79.995888

    },
    "processor_mid": "9000012345",
    "processor_mid_type": "VISA_VMID",
    "matching_status": "HISTORIC_TRANSACTION",
    "reward_details":
    [

        {
            "offer_id": "triple-abc-123",
            "amount": 0,
            "currency_code": "USD",
            "status": "REJECTED",
            "rejection": "PURCHASE_AMOUNT_TOO_LOW",
            "notes": "string"
        }

    ],
    "created_at": "2021-12-01T01:59:59.000Z",
    "updated_at": "2021-12-01T01:59:59.000Z"
}"""
BASE_TRANSACTION_DICT = json.loads(BASE_TRANSACTION_JSON)

