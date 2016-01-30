# -*- coding: utf-8 -*-

import requests

SECRET_TOKEN = 'thisisasecret'
API_HOST = 'http://127.0.0.1:8080'
URL_IMPORT = '{}/obp/vsandbox/v1.0/data-import?secret_token={}'.format(API_HOST, SECRET_TOKEN)

data = {
    'banks': [{
        'id': 'obp-bank-new',
        'short_name': 'Bank New',
        'full_name': 'The Bank of New',
        'logo': 'https://static.openbankproject.com/images/sandbox/bank_x.png',
        'website': 'https://www.example.com',
    }],
    'users': [{
        'email': 'foo@bar.com',
        'password': 'qwertyuiop',
        'display_name': 'Foo Bar',
    }],
    'accounts': [{
        'id': 'a65e28a5-9abe-428f-85bb-6c3c38122adb',
        'bank': 'obp-bank-new',
        'label': 'New bank account for Foo',
        'number': '007',
        'type': 'CURRENT PLUS',
        'balance': {
            'currency': 'GBP',
            'amount': '42',
        },
        'IBAN': 'BA12 1234 5123 4518 4490 1189 007',
        'owners': ['foo@bar.com'],
        'generate_public_view': True,
        'generate_accountants_view': True,
        'generate_auditors_view': True,
    }],
}

print 'Posting to {}'.format(URL_IMPORT)
response = requests.post(URL_IMPORT, json=data)
print response.status_code
print response.text
