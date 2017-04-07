# -*- coding: utf-8 -*-
from __future__ import print_function  # (at top of module)
import sys, requests
import uuid
import lib.obp
from props.k1_kafka import *
#from props.apisandbox import *
import logging
logging.basicConfig(level=logging.DEBUG)

# test payment workflow
# prerequisites:
#  1 prepare your own accounts info (please try following props first) 
#    Reference : k1_kafka.py/apisandbox.py
#   
# test endpoint list: 
# 1 Create counterparty for an account - V210
# 2 Create Transaction Request. (SANDBOX_TAN)- V210
# 3 Create Transaction Request. (SEPA)- V210
# 4 Create Transaction Request. (COUNTERPARTY)- V210
# 5 Answer Transaction Request Challenge. (SANDBOX_TAN)-V210
# 6 Answer Transaction Request Challenge. (SEPA)-V210
# 7 Answer Transaction Request Challenge. (COUNTERPARTY)-V210
# 8 Get Transaction by Id. -V121
# 9 Get Transactions for Account (Full)-- V121
# 10 Get Counterparties of one Account.-- V220
# 11 Get Counterparties of one Account.-- V220

print("#########################Step 1 : Direct Login process.################")
obp = lib.obp
obp.setBaseUrl(BASE_URL)
obp.setApiVersion(API_VERSION_V210)

# login and set authorized token
print("Call API - 0 'DirectLogin'")
obp.login(USERNAME, PASSWORD, CONSUMER_KEY)

# set fromAccount info:
from_bank_id = FROM_BANK_ID
from_account_id = FROM_ACCOUNT_ID
getAccount_response_before = obp.getAccount(FROM_BANK_ID, FROM_ACCOUNT_ID)

# set fromAccount info:
from_bank_id = FROM_BANK_ID
from_account_id = FROM_ACCOUNT_ID


print("")
print("")
print("######################### Step2 - make a payment - SANDBOX_TAN ########")
# set the toAccount for SANDBOX_TAN
to_bank_id = TO_BANK_ID
to_account_id = TO_ACCOUNT_ID

TRANSACTION_REQUEST_TYPE_SANDBOX_TAN = "SANDBOX_TAN"
print("--------- TRANSACTION_REQUEST_TYPE : {0}".format(TRANSACTION_REQUEST_TYPE_SANDBOX_TAN))
#####Case1: without challenge
print("Call API - 1 'Create Transaction Request. -- V210' (no challenge)")
# set up a small value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE)
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=TRANSACTION_REQUEST_TYPE_SANDBOX_TAN,
                                                     to_bank_id=to_bank_id,
                                                     to_account_id=to_account_id,
                                                     to_counterparty_id="",  # used for SEPA
                                                     to_counterparty_iban="")  # used for COUNTERPARTY

# There was no challenge, transaction was created immediately
obp.printMessageNoChallenge(initiate_response)

#####Case2: with challenge
print("")
print("Call API - 2 'Create Transaction Request. -- V210' (with challenge)")
# set up a large value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE_LARGE)
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=TRANSACTION_REQUEST_TYPE_SANDBOX_TAN,
                                                     to_bank_id=to_bank_id,
                                                     to_account_id=to_account_id,
                                                     to_counterparty_id="",  # used for SEPA
                                                     to_counterparty_iban="")  # used for COUNTERPARTY
obp.printMessageWithChallenge(initiate_response)

print("")
print("Call API - 3 'Answer Transaction Request Challenge. -- V210'")
transaction_req_id = initiate_response['id']
challenge_id = initiate_response['challenge']['id']
challenge_response = obp.answerChallengeV210(from_bank_id, 
                                             from_account_id,
                                             transaction_req_id,
                                             TRANSACTION_REQUEST_TYPE_SANDBOX_TAN,
                                             challenge_id)

obp.printMessageAfterAnswerChallenge(challenge_response)

print("")
print("")
print("######################### Step3 - make a payment - SEPA ################")
TRANSACTION_REQUEST_TYPE_SEPA = "SEPA"
print("--------- TRANSACTION_REQUEST_TYPE : {0}".format(TRANSACTION_REQUEST_TYPE_SEPA))

to_counterparty_iban = str(uuid.uuid4())
print("Call API - 1 'Create counterparty for an account. -- V210'")
create_counterparty_response = obp.createCounterparty(bank_id=from_bank_id,
                                                      account_id=from_account_id,
                                                      name=str(uuid.uuid4()),
                                                      other_account_routing_scheme="IBAN",# for SEPA, here must be IBAN
                                                      other_account_routing_address=to_counterparty_iban,
                                                      other_bank_routing_scheme="test",
                                                      other_bank_routing_address="test")
obp.printCreateCounterparty(create_counterparty_response)

print("")
print("Call API - 2 'Create Transaction Request. -- V210' (no challenge)")
# set up a small value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE)
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=TRANSACTION_REQUEST_TYPE_SEPA,
                                                     to_bank_id="",  # used for SANDBOX_TAN
                                                     to_account_id="",  # used for SANDBOX_TAN
                                                     to_counterparty_id="",  # used for COUNTERPARTY
                                                     to_counterparty_iban=to_counterparty_iban)# used for SEPA
obp.printMessageNoChallenge(initiate_response)

print("")
print("Call API - 3 'Create Transaction Request. -- V210' (with challenge)")
# set up a large value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE_LARGE)
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=TRANSACTION_REQUEST_TYPE_SEPA,
                                                     to_bank_id="",  # used for SANDBOX_TAN
                                                     to_account_id="",  # used for SANDBOX_TAN
                                                     to_counterparty_id="",  # used for COUNTERPARTY
                                                     to_counterparty_iban=to_counterparty_iban) # used for SEPA
obp.printMessageWithChallenge(initiate_response)

print("")
print("Call API - 4 'Answer Transaction Request Challenge. -- V210'")
transaction_req_id = initiate_response['id']
challenge_id = initiate_response['challenge']['id']
challenge_response = obp.answerChallengeV210(from_bank_id,
                                             from_account_id,
                                             transaction_req_id,
                                             TRANSACTION_REQUEST_TYPE_SEPA,
                                             challenge_id)

obp.printMessageAfterAnswerChallenge(challenge_response)

print("")
print("")
print("######################### Step4 - make a payment - COUNTERPARTY #######")
TRANSACTION_REQUEST_TYPE_COUNTERPARTY = "COUNTERPARTY"
print("--------- TRANSACTION_REQUEST_TYPE : {0}".format(TRANSACTION_REQUEST_TYPE_COUNTERPARTY))
print("Call API - 1 'Create counterparty for an account. -- V210'")
create_counterparty_response = obp.createCounterparty(bank_id=from_bank_id,
                                                      account_id=from_account_id,
                                                      name=str(uuid.uuid4()),
                                                      other_account_routing_scheme="OBP",
                                                      other_account_routing_address="test",
                                                      other_bank_routing_scheme="OBP",
                                                      other_bank_routing_address="test")
obp.printCreateCounterparty(create_counterparty_response)

print("")
print("Call API - 2 'Create Transaction Request. -- V210' (no challenge)")
# set up a small value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE)
to_counterparty_id = create_counterparty_response['counterparty_id']
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=TRANSACTION_REQUEST_TYPE_COUNTERPARTY,
                                                     to_bank_id="",  # used for SANDBOX_TAN
                                                     to_account_id="",  # used for SANDBOX_TAN
                                                     to_counterparty_id=to_counterparty_id,
                                                     to_counterparty_iban="")  # used for SEPA
obp.printMessageNoChallenge(initiate_response)


print("")
print("Call API - 3 'Create Transaction Request. -- V210' (with challenge)")
# set up a large value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE_LARGE)
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=TRANSACTION_REQUEST_TYPE_COUNTERPARTY,
                                                     to_bank_id="",  # used for SANDBOX_TAN
                                                     to_account_id="",  # used for SANDBOX_TAN
                                                     to_counterparty_id=to_counterparty_id,
                                                     to_counterparty_iban="")  # used for SEPA
obp.printMessageWithChallenge(initiate_response)

print("")
print("Call API - 4 'Answer Transaction Request Challenge. -- V210'")
transaction_req_id = initiate_response['id']
challenge_id = initiate_response['challenge']['id']
challenge_response = obp.answerChallengeV210(from_bank_id,
                                             from_account_id,
                                             transaction_req_id,
                                             TRANSACTION_REQUEST_TYPE_COUNTERPARTY,
                                             challenge_id)
obp.printMessageAfterAnswerChallenge(challenge_response)

print("")
print("")
print("######################## Step5 - Get Transactions #####################")
print("--------- Check the new transaction records")
print("Call API - 1 'Get Transaction by Id.-- V121'")

newTransactionId = challenge_response["transaction_ids"]
getTransaction_response = obp.getTransaction(FROM_BANK_ID, FROM_ACCOUNT_ID, newTransactionId)
obp.printGetTransaction(getTransaction_response, newTransactionId)

print("Call API - 2 'Get Transactions for Account (Full)-- V121'")
getTransactions_response = obp.getTransactions(FROM_BANK_ID, FROM_ACCOUNT_ID)
obp.printGetTransactions(getTransactions_response)


print("")
print("")
print("######################## Step6 - Get Counterparties ################")
print("--------- Get the Counterparties")
print("Call API - 1 'Get Counterparties of one Account..-- V220'")
obp.setApiVersion(API_VERSION_V220)

getCounterparties_response = obp.getCounterparties(FROM_BANK_ID, FROM_ACCOUNT_ID)
obp.printGetCounterparties(getCounterparties_response)

print("")
print("")
print("######################## Step7 - Get Bank Account, check balance ##")
print("--------- Get the Bank and check the balance")
print("Call API - 1 'Get Account by Id (Core)  -- V220'")
obp.setApiVersion(API_VERSION_V220)

print("The Bank Detail before make transactions:")
obp.printGetAccount(getAccount_response_before)
balance_before = getAccount_response_before['balance']['amount']
getAccount_response = obp.getAccount(FROM_BANK_ID, FROM_ACCOUNT_ID)
print("The Bank Detail after make transactions:")
obp.printGetAccount(getAccount_response)
balance_after = getAccount_response['balance']['amount']

print("Check the balance changed, we make 6 times transfer in this script, total transfer should be 3003 (1000+1+1000+1+1000+1):")
print("The Balance changed between before and after: {0}".format(round((float(balance_before) - float(balance_after)),2)))
print("Note: for connector = kafka/obpjvm, the balance will not change for now! double checked your BASE_URL")


