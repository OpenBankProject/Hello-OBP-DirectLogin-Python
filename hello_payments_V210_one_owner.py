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


#########################Step 1 : Direct Login process .################

import lib.obp
import logging
#logging.basicConfig(level=logging.DEBUG)

obp = lib.obp
obp.setBaseUrl(BASE_URL)
obp.setApiVersion(API_VERSION_V210)

print("Call API - 0 'DirectLogin' -- login and set authorized token")
obp.login(USERNAME, PASSWORD, CONSUMER_KEY)

######################### Step2 - Make a Payment - SANDBOX_TAN ################
print("")
print("Set fromAccount info: from_bank_id = {0} and from_account_id= {1}.".format(FROM_BANK_ID, FROM_ACCOUNT_ID))
from_bank_id = FROM_BANK_ID
from_account_id = FROM_ACCOUNT_ID

print("")
print("Set toAccount info: to_bank_id = {0} and to_account_id= {1}.".format(TO_BANK_ID, TO_ACCOUNT_ID))
to_bank_id = TO_BANK_ID
to_account_id = TO_ACCOUNT_ID

print("")
challenge_type_sandbox_tan = "SANDBOX_TAN"
print("--------- TRANSACTION_REQUEST_TYPE : {0}".format(challenge_type_sandbox_tan))
print("")
print("Set up the OUR_CURRENCY = {0} and OUR_VALUE_LARGE = {1} ".format(OUR_CURRENCY, OUR_VALUE_LARGE))
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE_LARGE)

print("Call API - 1 'Create Transaction Request. -- V210' (with challenge)")
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=challenge_type_sandbox_tan,
                                                     to_bank_id=to_bank_id,  # for SANDBOX_TAN
                                                     to_account_id=to_account_id,  # for SANDBOX_TAN
                                                     to_counterparty_id="",  # used for SEPA
                                                     to_counterparty_iban="")  # used for COUNTERPARTY
obp.printMessageWithChallenge(initiate_response)

print("")
print("Call API - 2 'Answer Transaction Request Challenge. -- V210'")
challenge_query = initiate_response['challenge']['id']
transaction_req_id = initiate_response['id']
challenge_response = obp.answerChallengeV210(bank_id=from_bank_id,
                                             account_id=from_account_id,
                                             transation_req_id=transaction_req_id,
                                             challenge_type=challenge_type_sandbox_tan,
                                             challenge_query=challenge_query)

obp.printMessageAfterAnswerChallenge(challenge_response)

# Then we need to check the get Transactions
print("")
print("Call API - 3 'Get Transactions for Account (Full)-- V210'")
new_transaction_id = challenge_response["transaction_ids"]
getTransactions_response = obp.getTransactions(from_bank_id, from_account_id)

obp.printGetTransactions(getTransactions_response)
