# -*- coding: utf-8 -*-
from __future__ import print_function  # (at top of module)
import sys, requests

# This test is calling in  V210 of OBP-API, Create Transaction Request for SANDBOX_TAN, SEPA, COUNTERPARTY (mapped)

# Note: in order to use this example, you need to have at least one account that you can send money from (i.e. be the owner).
# And another account to receiver money(for SEPA or COUNTERPARTY, create a new COUNTERPARTY do need to prepare for them)
# All properties are now kept in 'localtest_mapper.py',you need set up your own props.

#########################Step 1 : Login in(OAuth process) and prepare the bankaccounts to make the payment.################
# You probably don't need to change those
# connector=mapped
import uuid

from props.localtest_mapper import *
import lib.obp

obp = lib.obp
obp.setBaseUrl(BASE_URL)
obp.setApiVersion(API_VERSION_V210)

# login and set authorized token
obp.login(USERNAME, PASSWORD, CONSUMER_KEY)

# set the fromAccount info:
from_bank_id = FROM_BANK_ID
from_account_id = FROM_ACCOUNT_ID

######################### Step2 - make a payment - SANDBOX_TAN ################
print("")
print("")
# set the toAccount for SANDBOX_TAN
to_bank_id = TO_BANK_ID
to_account_id = TO_ACCOUNT_ID

challenge_type_sandbox_tan = "SANDBOX_TAN"
print("--------- TRANSACTION_REQUEST_TYPE : {0}".format(challenge_type_sandbox_tan))
#####Case1: without challenge
print("Call API - 1 'Create Transaction Request. -- V210' (no challenge)")
# set up a small value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE)
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=challenge_type_sandbox_tan,
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
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=challenge_type_sandbox_tan,
                                                     to_bank_id=to_bank_id,
                                                     to_account_id=to_account_id,
                                                     to_counterparty_id="",  # used for SEPA
                                                     to_counterparty_iban="")  # used for COUNTERPARTY
    
# There was a challenge, transaction was interrupted, and the transaction_request is 'INITIATED'
obp.printMessageWithChallenge(initiate_response)

# we need to answer the challenge
print("")
print("Then we need to answer the challenge")
challenge_id = initiate_response['challenge']['id']
transaction_req_id = initiate_response['id']

print("Call API - 3 'Answer Transaction Request Challenge. -- V210'")
print("Transaction is done , and the transaction_request is 'COMPLETED' and new Transaction id is created: :")
challenge_response = obp.answerChallengeV210(from_bank_id, from_account_id, transaction_req_id, challenge_type_sandbox_tan, challenge_id)
if "error" in challenge_response:
    sys.exit("Got an error: " + str(challenge_response))

obp.printMessageAfterAnswerChallenge(challenge_response)

######################### Step3 - make a payment - SEPA ################
print("")
print("")
challenge_type_sepa = "SEPA"
print("--------- TRANSACTION_REQUEST_TYPE : {0}".format(challenge_type_sepa))

# Create the new COUNTERPARTY for SEPA, other_account_routing_scheme must equal "IBAN"
to_counterparty_iban = str(uuid.uuid4())
create_counterparty_response = obp.createCounterparty(bank_id=from_bank_id,
                                                      account_id=from_account_id,
                                                      name=str(uuid.uuid4()),
                                                      other_account_routing_scheme="IBAN",
                                                      other_account_routing_address=to_counterparty_iban,
                                                      other_bank_routing_scheme="test",
                                                      other_bank_routing_address="test")

print("create Counterparty was successfully created:")
print("{0}".format(create_counterparty_response))

#####Case1: without challenge
print("")
print("Call API - 1 'Create Transaction Request. -- V210' (no challenge)")
# set up a small value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE)
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=challenge_type_sepa,
                                                     to_bank_id="",  # used for SANDBOX_TAN
                                                     to_account_id="",  # used for SANDBOX_TAN
                                                     to_counterparty_id="",  # used for COUNTERPARTY
                                                     to_counterparty_iban=to_counterparty_iban)
if "error" in create_counterparty_response:
    sys.exit("Got an error: " + str(create_counterparty_response))
    
# There was no challenge, transaction was created immediately
obp.printMessageNoChallenge(initiate_response)

#####Case2: with challenge
print("")
print("Call API - 2 'Create Transaction Request. -- V210' (with challenge)")
# set up a large value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE_LARGE)
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=challenge_type_sepa,
                                                     to_bank_id="",  # used for SANDBOX_TAN
                                                     to_account_id="",  # used for SANDBOX_TAN
                                                     to_counterparty_id="",  # used for COUNTERPARTY
                                                     to_counterparty_iban=to_counterparty_iban)
if "error" in initiate_response:
    sys.exit("Got an error: " + str(initiate_response))
    
# There was a challenge, transaction was interrupted, and the transaction_request is 'INITIATED'
obp.printMessageWithChallenge(initiate_response)

# we need to answer the challenge
challenge_id = initiate_response['challenge']['id']
transaction_req_id = initiate_response['id']
print("")
print("Call API - 3 'Answer Transaction Request Challenge. -- V210'")
print("Transaction is done , and the transaction_request is 'COMPLETED' and new Transaction id is created: :")
challenge_response = obp.answerChallengeV210(from_bank_id, from_account_id, transaction_req_id, challenge_type_sepa, challenge_id)

obp.printMessageAfterAnswerChallenge(challenge_response)

######################### Step4 - make a payment - COUNTERPARTY ################
print("")
print("")
challenge_type_counterparty = "COUNTERPARTY"
print("--------- TRANSACTION_REQUEST_TYPE : {0}".format(challenge_type_counterparty))

# Create the new COUNTERPARTY,  toCounterparty.other_account_routing_scheme =="OBP" && toCounterparty.other_bank_routing_scheme=="OBP")
create_counterparty_response = obp.createCounterparty(bank_id=from_bank_id,
                                                      account_id=from_account_id,
                                                      name=str(uuid.uuid4()),
                                                      other_account_routing_scheme="OBP",
                                                      other_account_routing_address="test",
                                                      other_bank_routing_scheme="OBP",
                                                      other_bank_routing_address="test")
if "error" in create_counterparty_response:
    sys.exit("Got an error: " + str(create_counterparty_response))

print("create Counterparty was successfully created:")
print("{0}".format(create_counterparty_response))
to_counterparty_id = create_counterparty_response['counterparty_id']

#####Case1: without challenge
print("")
print("Call API - 1 'Create Transaction Request. -- V210' (no challenge)")
# set up a small value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE)
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=challenge_type_counterparty,
                                                     to_bank_id="",  # used for SANDBOX_TAN
                                                     to_account_id="",  # used for SANDBOX_TAN
                                                     to_counterparty_id=to_counterparty_id,
                                                     to_counterparty_iban="")  # used for SEPA

# There was no challenge, transaction was created immediately
obp.printMessageNoChallenge(initiate_response)

#####Case2: with challenge
print("")
print("Call API - 3 'Create Transaction Request. -- V210' (with challenge)")
# set up a large value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE_LARGE)
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(from_bank_id=from_bank_id,
                                                     from_account_id=from_account_id,
                                                     transaction_request_type=challenge_type_counterparty,
                                                     to_bank_id="",  # used for SANDBOX_TAN
                                                     to_account_id="",  # used for SANDBOX_TAN
                                                     to_counterparty_id=to_counterparty_id,
                                                     to_counterparty_iban="")  # used for SEPA
# There was a challenge, transaction was interrupted, and the transaction_request is 'INITIATED'
obp.printMessageWithChallenge(initiate_response)

# we need to answer the challenge
challenge_id = initiate_response['challenge']['id']
transaction_req_id = initiate_response['id']
print("")
print("Call API - 3 'Answer Transaction Request Challenge. -- V210'")
print("Transaction is done , and the transaction_request is 'COMPLETED' and new Transaction id is created: :")
challenge_response = obp.answerChallengeV210(from_bank_id, from_account_id, transaction_req_id, challenge_type_counterparty,
                                             challenge_id)
if "error" in challenge_response:
    sys.exit("Got an error: " + str(challenge_response))

obp.printMessageAfterAnswerChallenge(challenge_response)
