# -*- coding: utf-8 -*-

# Note: in order to use this example, you need to have at least one account
from settings import (
    API_BASE_URL,
    API_HOST,
    MY_BANK,
    CLIENT_KEY,
)
# Our account's bank
OUR_BANK = MY_BANK

# username, password and consumer key
USERNAME     = 'Robert.Uk.01'
PASSWORD     = '356609'
CONSUMER_KEY = CLIENT_KEY

# API server URL
BASE_URL  = API_HOST
#BASE_URL  = "http://localhost:8080"



LOGIN_URL = '{0}/my/logins/direct'.format(BASE_URL)
LOGIN_HEADER  = { 'Authorization' : 'DirectLogin username="%s",password="%s",consumer_key="%s"' % (USERNAME, PASSWORD, CONSUMER_KEY)}

import sys, requests
# Helper function to merge headers
def merge(x, y):
    z = x.copy()
    z.update(y)
    return z

# Login and receive authorized token
print('Login as {0} to {1}'.format(LOGIN_HEADER, LOGIN_URL))
r = requests.get(LOGIN_URL, headers=LOGIN_HEADER)

if (r.status_code != 200):
    print("error: could not login")
    sys.exit(0)

# Login OK - create authorization headers
token = r.json()['token']
print("Received token: {0}".format(token))

# Prepare headers
directlogin  = { 'Authorization' : 'DirectLogin token=%s' % token}
content_json = { 'content-type'  : 'application/json' }
limit        = { 'obp_limit'     : '25' }

# Get all private accounts for this user
response = requests.get(u"{0}/obp/v2.1.0/banks/{1}/accounts".format(BASE_URL, OUR_BANK), headers=directlogin)
print(response.status_code)

print (response.text)
# Print accounts 
accounts = response.json()
for a in accounts:
    print(a['id'])

# Just picking first account
our_account = accounts[0]['id']
print("our account: {0}".format(our_account))

# Prepare post data and set new label value
post_data = {
    'id' : '%s' % our_account,
    'label' : 'New label',
    'bank_id': '%s' % OUR_BANK 
}

# Send post request with attached json with new label value
response = requests.post(u"{0}/obp/v2.1.0/banks/{1}/accounts/{2}".format(BASE_URL, OUR_BANK, our_account), json=post_data, headers=merge(directlogin, content_json))

# Print result
print(response.status_code)
print(response.text)
