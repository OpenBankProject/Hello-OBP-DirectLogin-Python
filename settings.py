# -*- coding: utf-8 -*-
"""
Settings for the hello scripts.

You most likely need to edit a few of them, e.g. API_HOST and the OAuth
credentials.
"""

# Get the OAuth credentials prior from the API, e.g.
# https://apisandbox.openbankproject.com/consumer-registration
CLIENT_KEY = 'fz3as2gadnzustw5sbnokwspqnit4obdwpsowuif'
CLIENT_SECRET = 'g32v25gmasvwuav0vemu4jjdbh5x0jit22luclwm'


# URL you are redirected to when OAuth has succeeded. Doesn't need to exist for
# the example scripts.
CALLBACK_URL = 'http://127.0.0.1/cb'

# API host to talk to
#API_HOST = 'http://127.0.0.1:8080'
#API_HOST = 'https://apisandbox.openbankproject.com'
API_HOST = 'https://danskebank.openbankproject.com'

# API version to use
API_VERSION = '2.1.0'

# API BASE URL
#API_BASE_URL = '{}/obp/v{}'.format(API_HOST, API_VERSION)
API_BASE_URL = '{}/obp/v{}'.format(API_HOST, API_VERSION)

# For initial testing, you might want to get some sample data:
# https://raw.githubusercontent.com/OpenBankProject/OBP-API/develop/src/main/scala/code/api/sandbox/example_data/example_import.json
# The account data below was taken from there

# My bank we want to send money from
MY_BANK = 'dan.01.uk.uk'
# My account is picked automatically at the moment
# MY_ACCOUNT = 'Robert.Uk.01'

# The counterparty we want to send money to

COUNTERPARTY_BANK = 'dan.01.uk.uk'
COUNTERPARTY_ACCOUNT_ID = 'be4c3b50-fa7a-4e38-989b-e6d3c874a368'

# Currency used for payment
PAYMENT_CURRENCY = 'GBP'

# Payment value to transfer; values < 100 will not be challenged
PAYMENT_VALUE = '0.01'

# Payment description
PAYMENT_DESCRIPTION = 'Hello Payments v2.1!'
