#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, random, string, requests

LOGGING     = True
BASE_URL    = "http://localhost:8080"
API_VERSION = "v1.4.0"
DL_TOKEN    = { 'Authorization' : 'DirectLogin token=' }

CONTENT_JSON  = { 'content-type'  : 'application/json' }

def setCounterParty(bank_id, account_id,counterparty_id, counterparty_iban):
    global COUNTERPARTY_BANK, OUR_COUNTERPARTY, OUR_COUNTERPARTY_ID, OUR_COUNTERPARTY_IBAN
    COUNTERPARTY_BANK = bank_id
    OUR_COUNTERPARTY = account_id
    OUR_COUNTERPARTY_ID = counterparty_id
    OUR_COUNTERPARTY_IBAN = counterparty_iban
    
def setPaymentDetails(currency,value):
    global OUR_CURRENCY, OUR_VALUE
    
    OUR_CURRENCY = currency
    OUR_VALUE =value
    
def setBaseUrl(u):
    global BASE_URL
    BASE_URL = u

def setToken(t):
    global DL_TOKEN 
    DL_TOKEN = { 'Authorization' : 'DirectLogin token=%s' % t}

def setApiVersion(v):
    global API_VERSION
    API_VERSION = v

# Helper function to merge headers
def mergeHeaders(x, y):
    z = x.copy()
    z.update(y)
    return z

# Logger
def log(m):
    if LOGGING:
        print(m)

# Login as user
def login(username, password, consumer_key):
    login_url = '{0}/my/logins/direct'.format(BASE_URL)
    login_header  = { 'Authorization' : 'DirectLogin username="%s",password="%s",consumer_key="%s"' % (username, password, consumer_key)}
    # Login and receive authorized token
    log('Login as {0} to {1}'.format(login_header, login_url))
    r = requests.get(login_url, headers=login_header)
    if (r.status_code != 200):
        log("error: could not login")
        log("text: " + r.text)
        return r.text
    t = r.json()['token']
    log("Received token: {0}".format(t))
    setToken(t)
    return t

# Request a meeting
def requestMeeting(purpose_id, provider_id):
    post_data = {
        'purpose_id'   : '%s' % purpose_id,
        'provider_id'  : '%s' % provider_id
    }
    # Send post request with attached json
    response = requests.post(u"{0}/obp/{1}/banks/THE_BANK/meetings".format(BASE_URL, API_VERSION), json=post_data, headers=mergeHeaders(DL_TOKEN, CONTENT_JSON))
    # Print result
    log("code=" + response.status_code + " text=" + response.text)
    return response.json()

def getCounterBankId():
    return COUNTERPARTY_BANK

def getCounterpartyAccountId():
    return OUR_COUNTERPARTY

def getCounterpartyId():
    return OUR_COUNTERPARTY_ID

def getCounterpartyIban():
    return OUR_COUNTERPARTY_IBAN

# Get banks
def getBanks():
    # Prepare headers
    response = requests.get(u"{0}/obp/{1}/banks".format(BASE_URL, API_VERSION), headers=mergeHeaders(DL_TOKEN, CONTENT_JSON))
    return response.json()['banks']

# Get currently logged in user
def getCurrentUser():
    # Prepare headers
    response = requests.get(u"{0}/obp/{1}/users/current".format(BASE_URL, API_VERSION), headers=mergeHeaders(DL_TOKEN, CONTENT_JSON))
    return response.json()

# Create an user
def createUser(fname, lname, email, username, password):
    post_data = {
        'last_name'  : '%s' % lname,
        'first_name' : '%s' % fname,
        'email'      : '%s' % email,
        'username'   : '%s' % username,
        'password'   : '%s' % password 
    }
    # Send post request with attached json
    response = requests.post(u"{0}/obp/{1}/users".format(BASE_URL, API_VERSION), json=post_data, headers=mergeHeaders(DL_TOKEN, CONTENT_JSON))
    # Log result
    log("code=" + response.status_code + " text=" + response.text)
    return response.json()

# Get all user's private accounts
def getPrivateAccounts(bank):
    # Prepare headers
    response = requests.get(u"{0}/obp/{1}/banks/{2}/accounts/private".format(BASE_URL, API_VERSION, bank), headers=mergeHeaders(DL_TOKEN, CONTENT_JSON))
    return response.json()['accounts']

# Get a single account
def getAccount(bank, account):
    # Prepare headers
    response = requests.get(u"{0}/obp/{1}/my/banks/{2}/accounts/{3}/account".format(BASE_URL, API_VERSION, bank, account), headers=mergeHeaders(DL_TOKEN, CONTENT_JSON))
    return response.json()

# Get owner's transactions
def getTransactions(bank, account):
    response = requests.get(u"{0}/obp/{1}/banks/{2}/accounts/{3}/owner/transactions".format(BASE_URL, API_VERSION, bank, account), headers=mergeHeaders(DL_TOKEN, CONTENT_JSON))
    return response.json()['transactions']

# Get challenge types
def getChallengeTypes(bank, account):
    response = requests.get(u"{0}/obp/{1}/banks/{2}/accounts/{3}/owner/transaction-request-types".format(BASE_URL, API_VERSION, bank, account), headers=mergeHeaders(DL_TOKEN, CONTENT_JSON))
    types = response.json()['transaction_request_types']
    res = []
    for type in types:
      res.append(type['value'])
    return res

# Answer the challenge
def answerChallenge(bank, account, transation_req_id, challenge_query):
    body = '{"id": "' + challenge_query + '","answer": "123456"}'    #any number works in sandbox mode
    response = requests.post(u"{0}/obp/v1.4.0/banks/{1}/accounts/{2}/owner/transaction-request-types/sandbox/transaction-requests/{3}/challenge".format(
         BASE_URL, bank, account, transation_req_id), data=body, headers=mergeHeaders(DL_TOKEN, CONTENT_JSON)
    )
    return response.json()

def getTransactionRequest(bank, account, transation_req_id):
    response = requests.get(u"{0}/obp/{1}/banks/{2}/accounts/{3}/owner/transactions".format(BASE_URL, API_VERSION, bank, account), headers=mergeHeaders(DL_TOKEN, CONTENT_JSON))
    return response.json

def initiateTransactionRequest(bank, account, challenge_type, cp_bank, cp_account):
    send_to = {"bank": cp_bank, "account": cp_account}
    payload = '{"to": {"account_id": "' + send_to['account'] +'", "bank_id": "' + send_to['bank'] + \
    '"}, "value": {"currency": "' + OUR_CURRENCY + '", "amount": "' + OUR_VALUE + '"}, "description": "Description abc", "challenge_type" : "' + \
    challenge_type + '"}'
    response = requests.post(u"{0}/obp/v1.4.0/banks/{1}/accounts/{2}/owner/transaction-request-types/{3}/transaction-requests".format(BASE_URL, bank, account, challenge_type), data=payload, headers=mergeHeaders(DL_TOKEN, CONTENT_JSON))
    return response.json()

# Create counterparty, input data format: 
# {
#   "name":"Friend",
#   "other_account_routing_scheme":"IBAN",
#   "other_account_routing_address":"GR1301720530005053000582373",
#   "other_bank_routing_scheme":"BIC",
#   "other_bank_routing_address":"PIRBGRAAXXX",
#   "is_beneficiary":true
# }
def createCounterparty(bank_id,
                       account_id,
                       name,
                       other_account_routing_scheme,
                       other_account_routing_address,
                       other_bank_routing_scheme,
                       other_bank_routing_address):
    post_data = {
        'name'                         : '%s' % name,
        'other_account_routing_scheme' : '%s' % other_account_routing_scheme ,
        'other_account_routing_address': '%s' % other_account_routing_address,
        'other_bank_routing_scheme'    : '%s' % other_bank_routing_scheme,
        'other_bank_routing_address'   : '%s' % other_bank_routing_address,
        'is_beneficiary'               : True
    }
    # Send post request with attached json
    response = requests.post(u"{0}/obp/{1}/banks/{2}/accounts/{3}/owner/counterparties".format(BASE_URL, API_VERSION, bank_id, account_id), json=post_data, headers=mergeHeaders(DL_TOKEN, CONTENT_JSON))
    return response.json()

# Get all entitlements
def getAllEntitlements():
    response = requests.get(u"{0}/obp/{1}/entitlements".format(BASE_URL, API_VERSION), headers=mergeHeaders(DL_TOKEN, CONTENT_JSON))
    return response.json()

# Get user's entitlements
def getEntitlements(user, bank):
    response = requests.get(u"{0}/obp/{1}/banks/{2}/users/{3}/entitlements".format(BASE_URL, API_VERSION, bank, user), headers=mergeHeaders(DL_TOKEN, CONTENT_JSON))
    return response.json()

# Add system role to user
def addRole(role, user):
    post_data = {
        'bank_id'   : '',
        'role_name' : '%s' % role 
    }
    # Send post request with attached json
    response = requests.post(u"{0}/obp/{1}/users/{2}/entitlements".format(BASE_URL, API_VERSION, user), json=post_data, headers=mergeHeaders(DL_TOKEN, CONTENT_JSON))
    # Log result
    return response.text

# Add entitlement to user
def addEntitlement(entitlement, user, bank=''):
    post_data = {
        'bank_id'   : '%s' % bank,
        'role_name' : '%s' % entitlement 
    }
    # Send post request with attached json
    response = requests.post(u"{0}/obp/{1}/users/{2}/entitlements".format(BASE_URL, API_VERSION, user), json=post_data, headers=mergeHeaders(DL_TOKEN, CONTENT_JSON))
    # Log result
    return response.text



# Answer Transaction Request Challenge. - V210
def answerChallengeV210(bank, account, transation_req_id, challenge_type, challenge_query):
    body = '{"id": "' + challenge_query + '","answer": "123456"}'    #any number works in sandbox mode
    response = requests.post(u"{0}/obp/{1}/banks/{2}/accounts/{3}/owner/transaction-request-types/{4}/transaction-requests/{5}/challenge".format(
        BASE_URL, API_VERSION, bank, account, challenge_type, transation_req_id), data=body, headers=mergeHeaders(DL_TOKEN, CONTENT_JSON)
    )
    return response.json()

# Create Transaction Request. - V210
# Note : previous called 'initiateTransactionRequest', now keep it the same and OBP-API endpoint name
def createTransactionRequestV210(from_bank_id,
                                 from_account_id,
                                 transaction_request_type,
                                 to_bank_id,
                                 to_account_id,
                                 to_counterparty_id,
                                 to_counterparty_iban):
    if(transaction_request_type== "SANDBOX_TAN"):
        send_to = {"bank": to_bank_id, "account": to_account_id}
        payload = '{"to": {"account_id": "' + send_to['account'] +'", "bank_id": "' + send_to['bank'] + \
                  '"}, "value": {"currency": "' + OUR_CURRENCY + '", "amount": "' + OUR_VALUE + '"}, "description": "Description abc"}'
    elif(transaction_request_type== "SEPA"):
        send_to = {"iban": to_counterparty_iban}
        payload = '{"to": {"iban": "' + send_to['iban'] +\
                  '"}, "value": {"currency": "' + OUR_CURRENCY + '", "amount": "' + OUR_VALUE + '"}, "description": "Description abc", "charge_policy" : "' + \
                  "SHARED" + '"}'
    elif   (transaction_request_type== "COUNTERPARTY"):
        send_to = {"counterparty_id": to_counterparty_id}
        payload = '{"to": {"counterparty_id": "' + send_to['counterparty_id']  + \
                  '"}, "value": {"currency": "' + OUR_CURRENCY + '", "amount": "' + OUR_VALUE + '"}, "description": "Description abc", "charge_policy" : "' + \
                  "SHARED" + '"}'
    else: # FREE_FORM
        send_to = {"bank": to_bank_id, "account": to_account_id}
        payload = '{"to": {"account_id": "' + send_to['account'] +'", "bank_id": "' + send_to['bank'] + \
                  '"}, "value": {"currency": "' + OUR_CURRENCY + '", "amount": "' + OUR_VALUE + '"}, "description": "Description abc", "challenge_type" : "' + \
                  transaction_request_type + '"}'
    response = requests.post(u"{0}/obp/{1}/banks/{2}/accounts/{3}/owner/transaction-request-types/{4}/transaction-requests".format(BASE_URL, API_VERSION, from_bank_id, from_account_id, transaction_request_type), data=payload, headers=mergeHeaders(DL_TOKEN, CONTENT_JSON))
    return response.json()