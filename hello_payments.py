# -*- coding: utf-8 -*-

import sys, requests

# Note: in order to use this example, you need to have at least one account
# that you can send money from (i.e. be the owner).

USERNAME     = 'robert.x.0.gh@example.com'
PASSWORD     = '3e3a3102'
CONSUMER_KEY = 'adwf5qomvtvtya5ss3z5aizpr2b4hq054aoqa2t2'

# API server URL
BASE_URL  = "http://127.0.0.1:8080"
LOGIN_URL = '{0}/my/logins/direct'.format(BASE_URL)

# API server will redirect your browser to this URL, should be non-functional
# You will paste the redirect location here when running the script
CALLBACK_URI = 'http://127.0.0.1/cb' # Our account's bank

OUR_BANK = 'obp-bank-x-gh'
# Our counterpart account id (of the same currency)
OUR_COUNTERPART = 'f65e28a5-9abe-428f-85bb-6c3c38122adb'
# Our currency to use
OUR_CURRENCY = 'GBP'

# Our value to transfer
# values below 1000 do not requre challenge request
OUR_VALUE = '0.01'
OUR_VALUE_LARGE = '1000.00'

# Header
loginHeader = { 'Authorization' : 'DirectLogin username="%s",password="%s",consumer_key="%s"' % (USERNAME, PASSWORD, CONSUMER_KEY)}
# Payload
loginData = {
    'dl_username': '%s' % USERNAME,
    'dl_password': '%s' % PASSWORD,
    'dl_consumer_key': '%s' % CONSUMER_KEY}

# login and receive authorized token
print 'Login as {0} to {1}'.format(loginHeader, LOGIN_URL)
r = requests.get(LOGIN_URL, json=loginData, headers=loginHeader)

if (r.status_code != 200):
    print "error: could not login"
    sys.exit(0)

# login ok - create authorization headers
token = r.json()['token']

print "Received token: {0}".format(token)

directlogin  = { 'Authorization' : 'DirectLogin token=%s' % token}
content_json = { 'content-type'  : 'application/json' }
limit        = { 'obp_limit'     : '25' }

def merge(x, y):
    z = x.copy()
    z.update(y)
    return z

#get accounts for a specific bank
print "Private accounts"
r = requests.get(u"{0}/obp/v1.4.0/banks/{1}/accounts/private".format(BASE_URL, OUR_BANK), headers=directlogin)
#print r.json()

accounts = r.json()['accounts']
for a in accounts:
    print a['id']

#just picking first account
our_account = accounts[0]['id']
print "our account: {0}".format(our_account)

print
print "Get owner transactions"
r = requests.get(u"{0}/obp/v1.4.0/banks/{1}/accounts/{2}/owner/transactions".format(BASE_URL,
    OUR_BANK,
    our_account), headers=merge(directlogin, limit)
)
transactions = r.json()['transactions']
print "Got {0} transactions".format(len(transactions))

print "Get challenge request types"
r = requests.get(u"{0}/obp/v1.4.0/banks/{1}/accounts/{2}/owner/transaction-request-types".format(BASE_URL,
    OUR_BANK,
    our_account), headers=directlogin
)
challenge_type = r.json()[0]['value']
print challenge_type

print
print "Initiate transaction requesti (small value)"

send_to = {"bank": OUR_BANK, "account": OUR_COUNTERPART}

payload = '{"to": {"account_id": "' + send_to['account'] +'", "bank_id": "' + send_to['bank'] + \
    '"}, "value": {"currency": "' + OUR_CURRENCY + '", "amount": "' + OUR_VALUE + '"}, "description": "Description abc", "challenge_type" : "' + \
    challenge_type + '"}'

r = requests.post(u"{0}/obp/v1.4.0/banks/{1}/accounts/{2}/owner/transaction-request-types/{3}/transaction-requests".format(
    BASE_URL, OUR_BANK, our_account, challenge_type), data=payload, headers=merge(directlogin, content_json))

initiate_response = r.json()

if "error" in initiate_response:
    sys.exit("Got an error: " + str(initiate_response))

if (initiate_response['challenge'] != None):
    #we need to answer the challenge
    challenge_query = initiate_response['challenge']['id']
    transation_req_id = initiate_response['id']['value']

    print "Challenge query is {0}".format(challenge_query)
    body = '{"id": "' + challenge_query + '","answer": "123456"}'    #any number works in sandbox mode
    r = requests.post(u"{0}/obp/v1.4.0/banks/{1}/accounts/{2}/owner/transaction-request-types/sandbox/transaction-requests/{3}/challenge".format(
        BASE_URL, OUR_BANK, our_account, transation_req_id), data=body, headers=merge(directlogin, content_json)
    )

    challenge_response = r.json()
    if "error" in challenge_response:
        sys.exit("Got an error: " + str(challenge_response))

    print "Transaction status: {0}".format(challenge_response['status'])
    print "Transaction created: {0}".format(challenge_response["transaction_ids"])
else:
    #There was no challenge, transaction was created immediately
    print "Transaction was successfully created: {0}".format(initiate_response["transaction_ids"])

print
print "Initiate transaction request (large value)"
send_to = {"bank": OUR_BANK, "account": OUR_COUNTERPART}

payload = '{"to": {"account_id": "' + send_to['account'] +'", "bank_id": "' + send_to['bank'] + \
    '"}, "value": {"currency": "' + OUR_CURRENCY + '", "amount": "' + OUR_VALUE_LARGE + '"}, "description": "Description abc", "challenge_type" : "' + \
    challenge_type + '"}'

r = requests.post(u"{0}/obp/v1.4.0/banks/{1}/accounts/{2}/owner/transaction-request-types/{3}/transaction-requests".format(
    BASE_URL, OUR_BANK, our_account, challenge_type), data=payload, headers=merge(directlogin, content_json))

initiate_response = r.json()

if "error" in initiate_response:
    sys.exit("Got an error: " + str(initiate_response))

if (initiate_response['challenge'] != None):
    #we need to answer the challenge
    challenge_query = initiate_response['challenge']['id']
    transation_req_id = initiate_response['id']['value']

    print "Challenge query is {0}".format(challenge_query)
    body = '{"id": "' + challenge_query + '","answer": "123456"}'    #any number works in sandbox mode
    r = requests.post(u"{0}/obp/v1.4.0/banks/{1}/accounts/{2}/owner/transaction-request-types/sandbox/transaction-requests/{3}/challenge".format(
        BASE_URL, OUR_BANK, our_account, transation_req_id), data=body, headers=merge(directlogin, content_json)
    )

    challenge_response = r.json()
    if "error" in challenge_response:
        sys.exit("Got an error: " + str(challenge_response))

    print "Transaction status: {0}".format(challenge_response['status'])
    print "Transaction created: {0}".format(challenge_response["transaction_ids"])
else:
    #There was no challenge, transaction was created immediately
    print "Transaction was successfully created: {0}".format(initiate_response["transaction_ids"])

