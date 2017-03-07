# -*- coding: utf-8 -*-
from __future__ import print_function  # (at top of module)
import sys, requests

# This test is calling in  V210 of OBP-API, Create Transaction Request for SANDBOX_TAN, SEPA, COUNTERPARTY (kafka)

# Note: in order to use this example, you need to have at least one account that you can send money from (i.e. be the owner).
# And another account to receiver money(toBankAccount and  toCounterparty fields should be correct)
# All properties are now kept in 'localtest_kafka.py',you need set up your own props.

#########################Step 1 : Login in(OAuth process) and prepare the bankaccounts to make the payment.################
# You probably don't need to change those
# connector=mapped
from props.localtest_kafka import *
import lib.obp

obp = lib.obp
obp.setBaseUrl(BASE_URL)
obp.setApiVersion(API_VERSION_V210)

# login and set authorized token
obp.login(USERNAME, PASSWORD, CONSUMER_KEY)

# set fromAccount info:
from_bank_id = FROM_BANK_ID
from_account_id = FROM_ACCOUNT_ID

# check all request types,now support: SANDBOX_TAN, SEPA, COUNTERPARTY and FREE_FORM
print("Get support Transaction Request Types :")
transaction_request_type = obp.getChallengeTypes(from_bank_id, from_account_id)
print(transaction_request_type)

######################### Step2 - make a payment - SANDBOX_TAN ################
print("")
print("")
# set receiver bank account:
to_bank_id = TO_BANK_ID
to_account_id = TO_ACCOUNT_ID

challenge_type_sandbox_tan = "SANDBOX_TAN"
print("--------- TRANSACTION_REQUEST_TYPE : {0}".format(challenge_type_sandbox_tan))
#####Case1: without challenge
print("create transaction request small value (without challenge)")
# set up a small value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE)
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=challenge_type_sandbox_tan,
                                                     to_bank_id=to_bank_id,  # for SANDBOX_TAN
                                                     to_account_id=to_account_id,  # for SANDBOX_TAN
                                                     to_counterparty_id="",  # used for SEPA
                                                     to_counterparty_iban="")  # used for COUNTERPARTY

if "error" in initiate_response:
    sys.exit("Got an error: " + str(initiate_response))

# There was no challenge, transaction was created immediately
print("Transaction was successfully created:")
print("{0}".format(initiate_response))

#####Case2: with challenge
print("")
print("create transaction request large value (with challenge)")
# set up a large value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE_LARGE)
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=challenge_type_sandbox_tan,
                                                     to_bank_id=to_bank_id,  # for SANDBOX_TAN
                                                     to_account_id=to_account_id,  # for SANDBOX_TAN
                                                     to_counterparty_id="",  # used for SEPA
                                                     to_counterparty_iban="")  # used for COUNTERPARTY
if "error" in initiate_response:
    sys.exit("Got an error: " + str(initiate_response))

# we need to answer the challenge
challenge_query = initiate_response['challenge']['id']
transaction_req_id = initiate_response['id']

challenge_response = obp.answerChallengeV210(from_bank_id, from_account_id, transaction_req_id, challenge_type_sandbox_tan, challenge_query)
if "error" in challenge_response:
    sys.exit("Got an error: " + str(challenge_response))

print("Transaction status: {0}".format(challenge_response['status']))
print("Transaction created: {0}".format(challenge_response["transaction_ids"]))

######################### Step3 - make a payment - SEPA ################
print("")
print("")
# set receiver COUNTERPARTY_IBAN:
to_counterparty_iban = TO_COUNTERPARTY_IBAN

challenge_type_sepa = "SEPA"
print("--------- TRANSACTION_REQUEST_TYPE : {0}".format(challenge_type_sepa))
#####Case1: without challenge
print("create transaction request small value (without challenge)")
# set up a small value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE)
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=challenge_type_sepa,
                                                     to_bank_id="",  # for SANDBOX_TAN
                                                     to_account_id="",  # for SANDBOX_TAN
                                                     to_counterparty_id="",  # used for SEPA
                                                     to_counterparty_iban=to_counterparty_iban)  # used for COUNTERPARTY
if "error" in initiate_response:
    sys.exit("Got an error: " + str(initiate_response))

# There was no challenge, transaction was created immediately
print("Transaction was successfully created:")
print("{0}".format(initiate_response))

#####Case2: with challenge
print("")
print("create transaction request large value (with challenge)")
# set up a large value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE_LARGE)
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=challenge_type_sepa,
                                                     to_bank_id="",  # for SANDBOX_TAN
                                                     to_account_id="",  # for SANDBOX_TAN
                                                     to_counterparty_id="",  # used for SEPA
                                                     to_counterparty_iban=to_counterparty_iban)  # used for COUNTERPARTY
if "error" in initiate_response:
    sys.exit("Got an error: " + str(initiate_response))

# we need to answer the challenge
challenge_query = initiate_response['challenge']['id']
transaction_req_id = initiate_response['id']

challenge_response = obp.answerChallengeV210(from_bank_id, from_account_id, transaction_req_id, challenge_type_sepa, challenge_query)
if "error" in challenge_response:
    sys.exit("Got an error: " + str(challenge_response))

print("Transaction status: {0}".format(challenge_response['status']))
print("Transaction created: {0}".format(challenge_response["transaction_ids"]))

######################### Step4 - make a payment - COUNTERPARTY ################
print("")
print("")

# set receiver COUNTERPARTY_ID:
to_counterparty_id = TO_COUNTERPARTY_ID

challenge_type_counterparty = "COUNTERPARTY"
print("--------- TRANSACTION_REQUEST_TYPE : {0}".format(challenge_type_counterparty))
#####Case1: without challenge
print("create transaction request small value (without challenge)")
# set up a small value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE)
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=challenge_type_counterparty,
                                                     to_bank_id="",  # for SANDBOX_TAN
                                                     to_account_id="",  # for SANDBOX_TAN
                                                     to_counterparty_id=to_counterparty_id,  # used for SEPA
                                                     to_counterparty_iban="")  # used for COUNTERPARTY
if "error" in initiate_response:
    sys.exit("Got an error: " + str(initiate_response))

# There was no challenge, transaction was created immediately
print("Transaction was successfully created:")
print("{0}".format(initiate_response))

#####Case2: with challenge
print("")
print("create transaction request large value (with challenge)")
# set up a large value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE_LARGE)
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=challenge_type_counterparty,
                                                     to_bank_id="",  # for SANDBOX_TAN
                                                     to_account_id="",  # for SANDBOX_TAN
                                                     to_counterparty_id=to_counterparty_id,  # used for SEPA
                                                     to_counterparty_iban="")  # used for COUNTERPARTY
if "error" in initiate_response:
    sys.exit("Got an error: " + str(initiate_response))

# we need to answer the challenge
challenge_query = initiate_response['challenge']['id']
transaction_req_id = initiate_response['id']

challenge_response = obp.answerChallengeV210(from_bank_id, from_account_id, transaction_req_id, challenge_type_counterparty,
                                             challenge_query)
if "error" in challenge_response:
    sys.exit("Got an error: " + str(challenge_response))

print("Transaction status: {0}".format(challenge_response['status']))
print("Transaction created: {0}".format(challenge_response["transaction_ids"]))