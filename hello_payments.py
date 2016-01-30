# -*- coding: utf-8 -*-

import sys, requests

# Note: in order to use this example, you need to have at least one account
# that you can send money from (i.e. be the owner).

# API server URL
BASE_URL = "http://127.0.0.1:8080"

# API server will redirect your browser to this URL, should be non-functional
# You will paste the redirect location here when running the script
CALLBACK_URI = 'http://127.0.0.1/cb'# Our account's bank
OUR_BANK = 'obp-bank-x-gh'
# Our counterpart account id (of the same currency)
OUR_COUNTERPART = 'f65e28a5-9abe-428f-85bb-6c3c38122adb'
# Our currency to use
OUR_CURRENCY = 'GBP'
# Our value to transfer
OUR_VALUE = '0.01'

URL_LOGIN  = '{0}/my/logins/direct'.format(BASE_URL)

loginData = {
     'dl_username': 'robert.x.0.gh@example.com'
    ,'dl_password': '3e3a3102' 
}


# You probably don't need to change those

# login and receive authorized token
print 'Login as {0} to {1}'.format(loginData, URL_LOGIN)
response = requests.post(URL_LOGIN, json=loginData)
#print response.status_code
if (response.status_code != 200):
    print "error: could not login"
    sys.exit(0)

# login ok - create authorization headers
token = response.text.replace("token=", "")
directlogin_json = { 'Authorization' : 'DirectLogin dl_token=%s' % token,
		     'content-type'  : 'application/json' }

directlogin      = { 'Authorization' : 'DirectLogin dl_token=%s' % token }

#get accounts for a specific bank
print "Private accounts"
r = requests.get(u"{0}/obp/v1.4.0/banks/{1}/accounts/private".format(BASE_URL, OUR_BANK), headers=directlogin)
print r.json()

accounts = r.json()['accounts']
for a in accounts:
    print a['id']

#just picking first account
our_account = accounts[0]['id']
print "our account: {0}".format(our_account)

print "Get owner transactions"
r = requests.get(u"{0}/obp/v1.4.0/banks/{1}/accounts/{2}/owner/transactions".format(BASE_URL,
    OUR_BANK,
    our_account), headers=directlogin ) #headers= {'obp_limit': '25'})
transactions = r.json()['transactions']
print "Got {0} transactions".format(len(transactions))

print "Get challenge request types"
r = requests.get(u"{0}/obp/v1.4.0/banks/{1}/accounts/{2}/owner/transaction-request-types".format(BASE_URL,
    OUR_BANK,
    our_account), headers=directlogin)

challenge_type = r.json()[0]['value']
print challenge_type

print "Initiate transaction request"
send_to = {"bank": OUR_BANK, "account": OUR_COUNTERPART}
payload = '{"to": {"account_id": "' + send_to['account'] +'", "bank_id": "' + send_to['bank'] + \
    '"}, "value": {"currency": "' + OUR_CURRENCY + '", "amount": "' + OUR_VALUE + '"}, "description": "Description abc", "challenge_type" : "' + \
    challenge_type + '"}'
r = requests.post(u"{0}/obp/v1.4.0/banks/{1}/accounts/{2}/owner/transaction-request-types/{3}/transaction-requests".format(
    BASE_URL, OUR_BANK, our_account, challenge_type), data=payload, headers=directlogin_json)
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
        BASE_URL, OUR_BANK, our_account, transation_req_id), data=body, headers=directlogin_json
    )

    challenge_response = r.json()
    if "error" in challenge_response:
        sys.exit("Got an error: " + str(challenge_response))

    print "Transaction status: {0}".format(challenge_response['status'])
    print "Transaction created: {0}".format(challenge_response["transaction_ids"])
else:
    #There was no challenge, transaction was created immediately
    print "Transaction was successfully created: {0}".format(initiate_response["transaction_ids"])
