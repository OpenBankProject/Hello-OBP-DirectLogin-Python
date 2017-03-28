# -*- coding: utf-8 -*-
from __future__ import print_function  # (at top of module)
import sys, requests
import lib.obp
import uuid
#import logging
#logging.basicConfig(level=logging.DEBUG)

# This test is calling in  V210 of OBP-API, Create Transaction Request for SANDBOX_TAN
# over Socgen1-k https://socgen-k-api.openbankproject.com/

#########################Step 1 :  Direct Login process .################
from props.socgen1_k_two_owners import * #17

obp = lib.obp
obp.setBaseUrl(BASE_URL)
obp.setApiVersion(API_VERSION_V210)

print("Call API - 0 'DirectLogin' -- login and set authorized token")
obp.login(USERNAME, PASSWORD, CONSUMER_KEY)


########################### Step2 - Make a Payment - SANDBOX_TAN ################
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
initiate_response = obp.createTransactionRequestV210(from_bank_id=FROM_BANK_ID,
                                                     from_account_id=FROM_ACCOUNT_ID,
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

######################### Step3 - make a payment - SEPA ################
print("")
print("")
challenge_type_sepa = "SEPA"
print("--------- TRANSACTION_REQUEST_TYPE : {0}".format(challenge_type_sepa))
print("Call API -1 'Create counterparty for an account --Socgen1-k' ")
# Create the new COUNTERPARTY for SEPA, other_account_routing_scheme must equal "IBAN"
to_counterparty_iban = str(uuid.uuid4())
create_counterparty_response = obp.createCounterparty(bank_id=FROM_BANK_ID,
                                                      account_id=FROM_ACCOUNT_ID,
                                                      name=str(uuid.uuid4()),
                                                      other_account_routing_scheme="IBAN",
                                                      other_account_routing_address=to_counterparty_iban,
                                                      other_bank_routing_scheme="BankId",
                                                      other_bank_routing_address="00100")
obp.printCreateCounterparty(create_counterparty_response)

print("")
print("Call API - 2 'Create Transaction Request. -- V210' (with challenge)")
# set up a large value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE_LARGE)
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(from_bank_id=FROM_BANK_ID,
                                                     from_account_id=FROM_ACCOUNT_ID,
                                                     transaction_request_type=challenge_type_sepa,
                                                     to_bank_id="",  # used for SANDBOX_TAN
                                                     to_account_id="",  # used for SANDBOX_TAN
                                                     to_counterparty_id="",  # used for COUNTERPARTY
                                                     to_counterparty_iban=to_counterparty_iban)

# There was a challenge, transaction was interrupted, and the transaction_request is 'INITIATED'
obp.printMessageWithChallenge(initiate_response)

# we need to answer the challenge
challenge_id = initiate_response['challenge']['id']
transaction_req_id = initiate_response['id']
print("")
print("Call API - 3 'Answer Transaction Request Challenge. -- V210'")
print("Transaction is done , and the transaction_request is 'COMPLETED' and new Transaction id is created: :")
challenge_response = obp.answerChallengeV210(from_bank_id, from_account_id, transaction_req_id, challenge_type_sepa, challenge_id)

# obp.printMessageAfterAnswerChallenge(challenge_response)
print("The response is: {0}".format(challenge_response))
    

######################### Step3 - make a payment - COUNTERPARTY ################
print("")
print("")
challenge_type_counterparty = "COUNTERPARTY"
print("--------- TRANSACTION_REQUEST_TYPE : {0}".format(challenge_type_counterparty))

# Create the new COUNTERPARTY,  toCounterparty.other_account_routing_scheme =="OBP" && toCounterparty.other_bank_routing_scheme=="OBP")
print("Call API -1 'Create counterparty for an account --Socgen1-k' ")
create_counterparty_response = obp.createCounterparty(bank_id=FROM_BANK_ID,
                                                      account_id=FROM_ACCOUNT_ID,
                                                      name=str(uuid.uuid4()),
                                                      other_account_routing_scheme="BankAccountID",
                                                      other_account_routing_address="1000203892",
                                                      other_bank_routing_scheme="BankId",
                                                      other_bank_routing_address="00100")

obp.printCreateCounterparty(create_counterparty_response)

print("{0}".format(create_counterparty_response))
to_counterparty_id = create_counterparty_response['counterparty_id']

#####Case1: without challenge
print("")
# set up a small value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE)
print("Call API - 2 'Create Transaction Request. -- V210' (with challenge)")
# set up a large value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE_LARGE)
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(from_bank_id=FROM_BANK_ID,
                                                     from_account_id=FROM_ACCOUNT_ID,
                                                     transaction_request_type=challenge_type_counterparty,
                                                     to_bank_id="",  # used for SANDBOX_TAN
                                                     to_account_id="",  # used for SANDBOX_TAN
                                                     to_counterparty_id=to_counterparty_id, # used for COUNTERPARTY
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


######################### Step4 - Print all transactions ################
print("")
print("Then we need to check the get Transactions")
print("Call API - 1 'Get Transactions for Account (Full)-- V210'")
new_transaction_id = challenge_response["transaction_ids"]
getTransactions_response = obp.getTransactions(FROM_BANK_ID, FROM_ACCOUNT_ID)
obp.printGetTransactions(getTransactions_response)