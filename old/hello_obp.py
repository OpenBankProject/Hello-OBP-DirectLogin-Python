# -*- coding: utf-8 -*-

# Note: in order to use this example, you need to have at least one account

# Our account's bank
OUR_BANK = 'obp-bankx-n'

# username, password and consumer key
USERNAME     = 'robert.x.d.n@example.com'
PASSWORD     = '8596d7de'
CONSUMER_KEY = 'fj43ona2cxxo3xrqyojdwzfpktwhj5avzwnee0jm'

# API server URL
BASE_URL  = "https://apisandbox.openbankproject.com"
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
response = requests.get(u"{0}/obp/v1.4.0/banks/{1}/accounts/private".format(BASE_URL, OUR_BANK), headers=directlogin)
print(response.status_code)

print (response.text)
# Print accounts 
accounts = response.json()['accounts']
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
response = requests.post(u"{0}/obp/v1.4.0/banks/{1}/accounts/{2}".format(BASE_URL, OUR_BANK, our_account), json=post_data, headers=merge(directlogin, content_json))

# Print result
print(response.status_code)
print(response.text)
