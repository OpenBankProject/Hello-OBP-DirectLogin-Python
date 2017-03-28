# -*- coding: utf-8 -*-
from __future__ import print_function  # (at top of module)
import sys, requests
import lib.obp
from props.localtest_kafka import *

# test payment workflow
# prerequisites:
#  1 run OBP-API and run OBP-Kafka_Python 
#  2 in props
#    get_counterparties_from_OBP_DB = false
#    connector=kafka_vMar2017
#  3 prepare your own accounts info  
#    Reference : localtest_kafka.py
#
# test endpoint list: 
# 1 Create Transaction Request. (SANDBOX_TAN)- V210
# 2 Create Transaction Request. (SEPA)- V210
# 3 Create Transaction Request. (COUNTERPARTY)- V210
# 4 Answer Transaction Request Challenge. (SANDBOX_TAN)-V210
# 5 Answer Transaction Request Challenge. (SEPA)-V210
# 6 Answer Transaction Request Challenge. (COUNTERPARTY)-V210
# 7 Get Transaction by Id. -V121
# 8 Get Transactions for Account (Full)-- V210

#########################Step1 : Direct Login process ################
obp = lib.obp
obp.setBaseUrl(BASE_URL)
obp.setApiVersion(API_VERSION_V210)

print("Call API - 0 'DirectLogin'")
obp.login(USERNAME, PASSWORD, CONSUMER_KEY)

# set fromAccount info:
from_bank_id = FROM_BANK_ID
from_account_id = FROM_ACCOUNT_ID

######################### Step2 : make a payment - SANDBOX_TAN  ################
print("")
print("")
# set receiver bank account:
to_bank_id = TO_BANK_ID
to_account_id = TO_ACCOUNT_ID

TRANSACTION_REQUEST_TYPE_SANDBOX_TAN = "SANDBOX_TAN"
print("--------- TRANSACTION_REQUEST_TYPE : {0}".format(TRANSACTION_REQUEST_TYPE_SANDBOX_TAN))
print("Call API - 1 'Create Transaction Request. -- V210' (no challenge)")
# set up a small value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE)
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=TRANSACTION_REQUEST_TYPE_SANDBOX_TAN,
                                                     to_bank_id=to_bank_id,  # for SANDBOX_TAN
                                                     to_account_id=to_account_id,  # for SANDBOX_TAN
                                                     to_counterparty_id="",  # used for SEPA
                                                     to_counterparty_iban="")  # used for COUNTERPARTY
obp.printMessageNoChallenge(initiate_response)

print("")
print("Call API - 2 'Create Transaction Request. -- V210' (with challenge)")
# set up a large value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE_LARGE)
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=TRANSACTION_REQUEST_TYPE_SANDBOX_TAN,
                                                     to_bank_id=to_bank_id,  # for SANDBOX_TAN
                                                     to_account_id=to_account_id,  # for SANDBOX_TAN
                                                     to_counterparty_id="",  # used for SEPA
                                                     to_counterparty_iban="")  # used for COUNTERPARTY


obp.printMessageWithChallenge(initiate_response)

print("")
print("Call API - 3 'Answer Transaction Request Challenge. -- V210'")
transaction_req_id = initiate_response['id']
challenge_query = initiate_response['challenge']['id']
challenge_response = obp.answerChallengeV210(from_bank_id,
                                             from_account_id,
                                             transaction_req_id,
                                             TRANSACTION_REQUEST_TYPE_SANDBOX_TAN,
                                             challenge_query)

obp.printMessageAfterAnswerChallenge(challenge_response)

# ######################### Step3 - make a payment - SEPA ################
print("")
print("")
# set receiver COUNTERPARTY_IBAN:
to_counterparty_iban = TO_COUNTERPARTY_IBAN

TRANSACTION_REQUEST_TYPE_SEPA = "SEPA"
print("--------- TRANSACTION_REQUEST_TYPE : {0}".format(TRANSACTION_REQUEST_TYPE_SEPA))
#####Case1: without challenge
print("Call API - 1 'Create Transaction Request. -- V210' (no challenge)")
# set up a small value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE)
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=TRANSACTION_REQUEST_TYPE_SEPA,
                                                     to_bank_id="",  # for SANDBOX_TAN
                                                     to_account_id="",  # for SANDBOX_TAN
                                                     to_counterparty_id="",  # used for SEPA
                                                     to_counterparty_iban=to_counterparty_iban)  # used for COUNTERPARTY
obp.printMessageNoChallenge(initiate_response)

#####Case2: with challenge
print("")
print("Call API - 2 'Create Transaction Request. -- V210' (with challenge)")
# set up a large value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE_LARGE)
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=TRANSACTION_REQUEST_TYPE_SEPA,
                                                     to_bank_id="",  # for SANDBOX_TAN
                                                     to_account_id="",  # for SANDBOX_TAN
                                                     to_counterparty_id="",  # used for SEPA
                                                     to_counterparty_iban=to_counterparty_iban)  # used for COUNTERPARTY

obp.printMessageWithChallenge(initiate_response)

# we need to answer the challenge
challenge_query = initiate_response['challenge']['id']
transaction_req_id = initiate_response['id']

print("")
print("Call API - 3 'Answer Transaction Request Challenge. -- V210'")
challenge_response = obp.answerChallengeV210(from_bank_id, from_account_id, transaction_req_id, TRANSACTION_REQUEST_TYPE_SEPA, challenge_query)

obp.printMessageAfterAnswerChallenge(challenge_response)

######################### Step4 - make a payment - COUNTERPARTY ################
print("")
print("")

# set receiver COUNTERPARTY_ID:
to_counterparty_id = TO_COUNTERPARTY_ID

TRANSACTION_REQUEST_TYPE_COUNTERPARTY = "COUNTERPARTY"
print("--------- TRANSACTION_REQUEST_TYPE : {0}".format(TRANSACTION_REQUEST_TYPE_COUNTERPARTY))
print("Call API - 1 'Create Transaction Request. -- V210' (no challenge)")
# set up a small value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE)
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=TRANSACTION_REQUEST_TYPE_COUNTERPARTY,
                                                     to_bank_id="",  # for SANDBOX_TAN
                                                     to_account_id="",  # for SANDBOX_TAN
                                                     to_counterparty_id=to_counterparty_id,  # used for SEPA
                                                     to_counterparty_iban="")  # used for COUNTERPARTY
obp.printMessageNoChallenge(initiate_response)


print("")
print("Call API - 2 'Create Transaction Request. -- V210' (with challenge)")
# set up a large value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE_LARGE)
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=TRANSACTION_REQUEST_TYPE_COUNTERPARTY,
                                                     to_bank_id="",  # for SANDBOX_TAN
                                                     to_account_id="",  # for SANDBOX_TAN
                                                     to_counterparty_id=to_counterparty_id,  # used for SEPA
                                                     to_counterparty_iban="")  # used for COUNTERPARTY
obp.printMessageWithChallenge(initiate_response)

print("")
print("Call API - 3 'Answer Transaction Request Challenge. -- V210'")
challenge_query = initiate_response['challenge']['id']
transaction_req_id = initiate_response['id']
print("Transaction is done , and the transaction_request is 'COMPLETED' and new Transaction id is created: :")
challenge_response = obp.answerChallengeV210(from_bank_id,
                                             from_account_id,
                                             transaction_req_id,
                                             TRANSACTION_REQUEST_TYPE_COUNTERPARTY,
                                             challenge_query)

obp.printMessageAfterAnswerChallenge(challenge_response)

######################## Step5 - Get Transactions ################
print("")
print("")
print("--------- Check the new transaction records")
print("Call API - 1 'Get Transaction by Id.-- V121'")

newTransactionId = challenge_response["transaction_ids"]
getTransaction_response = obp.getTransaction(FROM_BANK_ID, FROM_ACCOUNT_ID, newTransactionId)
obp.printGetTransaction(getTransaction_response, newTransactionId)

print("Call API - 2 'Get Transactions for Account (Full)-- V121'")
getTransactions_response = obp.getTransactions(FROM_BANK_ID, FROM_ACCOUNT_ID)
obp.printGetTransactions(getTransactions_response)
