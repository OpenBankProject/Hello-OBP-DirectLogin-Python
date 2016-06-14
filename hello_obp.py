# -*- coding: utf-8 -*-

import sys, requests
# Helper function to merge headers
def merge(x, y):
    z = x.copy()
    z.update(y)
    return z

# Note: in order to use this example, you need to have at least one account

USERNAME     = 'robert.x.0.gh@example.com'
PASSWORD     = '3e3a3102'
CONSUMER_KEY = 'adwf5qomvtvtya5ss3z5aizpr2b4hq054aoqa2t2'

# API server URL
BASE_URL  = "http://127.0.0.1:8080"
LOGIN_URL = '{0}/my/logins/direct'.format(BASE_URL)

# API server will redirect your browser to this URL, should be non-functional

# You will paste the redirect location here when running the script
CALLBACK_URI = 'http://127.0.0.1/cb'

# Our account's bank
OUR_BANK = 'obp-bank-x-gh'

# You probably don't need to change those
loginHeader  = { 'Authorization' : 'DirectLogin username="%s",password="%s",consumer_key="%s"' % (USERNAME, PASSWORD, CONSUMER_KEY)}

# Login and receive authorized token
print 'Login as {0} to {1}'.format(loginHeader, LOGIN_URL)
r = requests.get(LOGIN_URL, headers=loginHeader)

if (r.status_code != 200):
    print "error: could not login"
    sys.exit(0)

# Login OK - create authorization headers
token = r.json()['token']

print "Received token: {0}".format(token)

# Prepare headers
directlogin  = { 'Authorization' : 'DirectLogin token=%s' % token}
content_json = { 'content-type'  : 'application/json' }
limit        = { 'obp_limit'     : '25' }

# Get all private accounts for this user
response = requests.get(u"{0}/obp/v1.4.0/banks/{1}/accounts/private".format(BASE_URL, OUR_BANK), headers=directlogin)
print response.status_code

# Print accounts 
accounts = response.json()['accounts']
for a in accounts:
    print a['id']

# Just picking first account
our_account = accounts[0]['id']
print "our account: {0}".format(our_account)

# Prepare post data and set new label value
post_data = {
    'id' : '%s' % our_account,
    'label' : 'New label',
    'bank_id': '%s' % OUR_BANK 
}

# Send post request with attached json with new label value
response = requests.post(u"{0}/obp/v1.4.0/banks/{1}/accounts/{2}".format(BASE_URL, OUR_BANK, our_account), json=post_data, headers=merge(directlogin, content_json))
print response.status_code

# Print result
print response.text
