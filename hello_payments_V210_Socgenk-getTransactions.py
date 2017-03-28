# -*- coding: utf-8 -*-
from __future__ import print_function  # (at top of module)
import sys, requests

# This test is calling in  V210 of OBP-API, Create Transaction Request for SANDBOX_TAN
# over Socgen1-k https://socgen-k-api.openbankproject.com/
# or over Socgen2-k https://socgen2-k-api.openbankproject.com/
# or local : http://127.0.0.1:8080 (You need set up local test environment)

# Note: 
# All needed users and accounts are now kept in 'localtest_Socgen1-k.py' or 'localtest_Socgen2-k.py'' or 'localtest_Socgen2-k'', 
# You can pick up one to test the sandbox you want, just modify the following lines to switch props
from props.socgen1_k import *
#from props.socgen2_k import *
# from props.localtest_Socgen2_k_local import *


#########################Step 1 :  Direct Login process .################

import lib.obp
import logging
#logging.basicConfig(level=logging.DEBUG)

obp = lib.obp
obp.setBaseUrl(BASE_URL)
obp.setApiVersion(API_VERSION_V210)

print("Call API - 0 'DirectLogin' -- login and set authorized token")
obp.login(USERNAME, PASSWORD, CONSUMER_KEY)

# Then we need to check the get Transactions
print("")
print("Call API - 3 'Get Transactions for Account (Full)-- V210'")
getTransactions_response = obp.getTransactions(FROM_BANK_ID, FROM_ACCOUNT_ID)

obp.printGetTransactions(getTransactions_response)
