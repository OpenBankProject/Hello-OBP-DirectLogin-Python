# -*- coding: utf-8 -*-

API_HOST   = 'http://127.0.0.1:8080'
BANK_ID    = 'obp-bank-x-gh'
ACCOUNT_ID = 'f65e28a5-9abe-428f-85bb-6c3c38122adb'

URL_GET    = '{0}/obp/v1.2.1/banks/{1}/accounts/private'.format(API_HOST, BANK_ID, ACCOUNT_ID)
URL_POST   = '{0}/obp/v1.2.1/banks/{1}/accounts/{2}'.format(API_HOST, BANK_ID, ACCOUNT_ID)
URL_LOGIN  = '{0}/my/logins/direct'.format(API_HOST)

loginData = {
    'dl_username': 'robert.x.0.gh@example.com',
    'dl_password': '3e3a3102',
    'dl_consumer_key': 'adwf5qomvtvtya5ss3z5aizpr2b4hq054aoqa2t2'
}

post_data = {
    'id' : '%s' % ACCOUNT_ID,
    'label' : 'New label',
    'bank_id': '%s' % BANK_ID
}



###################################

import sys, requests

# login and receive authorized token
print 'Login as {0} to {1}'.format(loginData, URL_LOGIN)
response = requests.post(URL_LOGIN, json=loginData)
#print response.status_code
if (response.status_code != 200):
    print "error: could not login"
    sys.exit(0)

# login ok - create authorization headers
token = response.text.replace("token=", "")
directlogin = { 'Authorization' : 'DirectLogin dl_token=%s' % token }


print 'POST {0} to {1}'.format(directlogin, URL_POST)
response = requests.post(URL_POST, json=post_data, headers=directlogin)
print response.status_code
print response.text

print 'GET from {0}'.format(URL_GET)
response = requests.get(URL_GET, headers=directlogin)
print response.status_code
print response.text

