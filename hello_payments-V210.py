# -*- coding: utf-8 -*-
from __future__ import print_function  # (at top of module)
import sys, requests

# This test is calling in  V210 of OBP-API, Create Transaction Request for SANDBOX_TAN, SEPA, COUNTERPARTY

# Note: in order to use this example, you need to have at least one account that you can send money from (i.e. be the owner).
# And another account to receiver money(the Counterparty fields should be correct)
# All properties are now kept in 'localtest.py', you need set up your own props.

#########################Step 1 : Login in(OAuth process) and prepare the bankaccounts to make the payment.################
# You probably don't need to change those
from props.localtest import *
import lib.obp

obp = lib.obp
obp.setBaseUrl(BASE_URL)
obp.setApiVersion(API_VERSION_V210)
obp.setCounterParty(COUNTERPARTY_BANK, OUR_COUNTERPARTY, OUR_COUNTERPARTY_ID, OUR_COUNTERPARTY_IBAN)

# login and set authorized token
obp.login(USERNAME, PASSWORD, CONSUMER_KEY)
banks = obp.getBanks()
# get a bank id
our_bank = banks[1]['id']
print("our bank: {0}".format(our_bank))

# get accounts for a specific bank
print(" --- Private accounts")
accounts = obp.getPrivateAccounts(our_bank)
for a in accounts:
    print(a['id'])

# just picking first account #
our_account = accounts[0]['id']
print("our account: {0}".format(our_account))

#get reciver bankaccount info (the counterparty fields)
cp_bank = obp.getCounterBankId()
cp_account = obp.getCounterpartyAccountId()
cp_cunterparty_id = obp.getCunterpartyId()
cp_cunterparty_iban = obp.getCunterpartyIban()

# check all request types,now support: SANDBOX_TAN, SEPA, COUNTERPARTY and FREE_FORM
print(" --- Get challenge request types")
challenge_types = obp.getChallengeTypes(our_bank, our_account)
print(challenge_types)

######################### Step2 - make a payment - SANDBOX_TAN ################
print("")
print("")
challenge_type_sandbox_tan = "SANDBOX_TAN"
print("--------- TRANSACTION_REQUEST_TYPE : {0}".format(challenge_type_sandbox_tan))
#####Case1: without challenge
print("create transaction request small value (without challenge)")
# set up a small value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE)
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(our_bank, our_account, challenge_type_sandbox_tan, cp_bank, cp_account,
                                                     cp_cunterparty_id, cp_cunterparty_iban)
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
initiate_response = obp.createTransactionRequestV210(our_bank, our_account, challenge_type_sandbox_tan, cp_bank, cp_account,
                                                     cp_cunterparty_id, cp_cunterparty_iban)
if "error" in initiate_response:
    sys.exit("Got an error: " + str(initiate_response))

# we need to answer the challenge
challenge_query = initiate_response['challenge']['id']
transaction_req_id = initiate_response['id']

challenge_response = obp.answerChallengeV210(our_bank, our_account, transaction_req_id, challenge_type_sandbox_tan, challenge_query)
if "error" in challenge_response:
    sys.exit("Got an error: " + str(challenge_response))

print("Transaction status: {0}".format(challenge_response['status']))
print("Transaction created: {0}".format(challenge_response["transaction_ids"]))

######################### Step3 - make a payment - SEPA ################
print("")
print("")
challenge_type_sepa = "SEPA"

print("--------- TRANSACTION_REQUEST_TYPE : {0}".format(challenge_type_sepa))
#####Case1: without challenge
print("create transaction request small value (without challenge)")
# set up a small value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE)
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(our_bank, our_account, challenge_type_sepa, cp_bank, cp_account, cp_cunterparty_id,
                                                     cp_cunterparty_iban)
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
initiate_response = obp.createTransactionRequestV210(our_bank, our_account, challenge_type_sepa, cp_bank, cp_account, cp_cunterparty_id,
                                                     cp_cunterparty_iban)
if "error" in initiate_response:
    sys.exit("Got an error: " + str(initiate_response))

# we need to answer the challenge
challenge_query = initiate_response['challenge']['id']
transaction_req_id = initiate_response['id']

challenge_response = obp.answerChallengeV210(our_bank, our_account, transaction_req_id, challenge_type_sepa, challenge_query)
if "error" in challenge_response:
    sys.exit("Got an error: " + str(challenge_response))

print("Transaction status: {0}".format(challenge_response['status']))
print("Transaction created: {0}".format(challenge_response["transaction_ids"]))

######################### Step4 - make a payment - COUNTERPARTY ################
print("")
print("")
challenge_type_counterparty = "COUNTERPARTY"
print("--------- TRANSACTION_REQUEST_TYPE : {0}".format(challenge_type_counterparty))
#####Case1: without challenge
print("create transaction request small value (without challenge)")
# set up a small value in payment detail
obp.setPaymentDetails(OUR_CURRENCY, OUR_VALUE)
# call 'Create Transaction Requests - V210' endpoint
initiate_response = obp.createTransactionRequestV210(our_bank, our_account, challenge_type_counterparty, cp_bank, cp_account,
                                                     cp_cunterparty_id, cp_cunterparty_iban)
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
initiate_response = obp.createTransactionRequestV210(our_bank, our_account, challenge_type_counterparty, cp_bank, cp_account,
                                                     cp_cunterparty_id, cp_cunterparty_iban)
if "error" in initiate_response:
    sys.exit("Got an error: " + str(initiate_response))

# we need to answer the challenge
challenge_query = initiate_response['challenge']['id']
transaction_req_id = initiate_response['id']

challenge_response = obp.answerChallengeV210(our_bank, our_account, transaction_req_id, challenge_type_counterparty, challenge_query)
if "error" in challenge_response:
    sys.exit("Got an error: " + str(challenge_response))

print("Transaction status: {0}".format(challenge_response['status']))
print("Transaction created: {0}".format(challenge_response["transaction_ids"]))
