# -*- coding: utf-8 -*-
import sys, requests

API_HOST   = 'http://127.0.0.1:8080'
BANK_ID    = 'obp-bank-x-gh'
# ACCOUNT_ID = 'f65e28a5-9abe-428f-85bb-6c3c38122adb' # different id's for bnp paribas sandbox

URL_GET    = '{0}/obp/v1.2.1/banks/{1}/accounts/private'.format(API_HOST, BANK_ID)
URL_LOGIN  = '{0}/my/logins/direct'.format(API_HOST)

# Credentials
USERNAME     = 'robert.x.0.gh@example.com'
PASSWORD     = '3e3a3102'
CONSUMER_KEY = 'adwf5qomvtvtya5ss3z5aizpr2b4hq054aoqa2t2'

# Payload
loginData = {
    'dl_username': '%s' % USERNAME,
    'dl_password': '%s' % PASSWORD,
    'dl_consumer_key': '%s' % CONSUMER_KEY}

# Header
loginHeader = { 'Authorization' : 'DirectLogin username="%s",password="%s",consumer_key="%s"' % (USERNAME, PASSWORD, CONSUMER_KEY)}

# Login and receive authorized token
print 'Login as {0} to {1}'.format(loginData, URL_LOGIN)
response = requests.get(URL_LOGIN, json=loginData, headers=loginHeader)

if (response.status_code != 200):
    print "error: could not login"
    sys.exit(0)

token = response.json()['token']
print "Received token: {0}".format(token)

# Header with token
directlogin  = { 'Authorization' : 'DirectLogin token=%s' % token}

# GET request to get ACCOUNTS
print 'GET from {0}'.format(URL_GET)
response = requests.get(URL_GET, headers=directlogin)
print response.status_code
# print response.text

# JSON response
# print response.json()

# Parse account IDs
accounts = response.json()['accounts']
for a in accounts:
    print a['id']

# Pick first account
our_account = accounts[0]['id']
print "our account: {0}".format(our_account)

# POST payload with existing ACCOUTN_ID
post_data = {
    'id' : '%s' % our_account,
    'label' : 'New label',
    'bank_id': '%s' % BANK_ID,
}

# POST URL using existing ACCOUNT_ID
post_url = '{0}/obp/v1.2.1/banks/{1}/accounts/{2}'.format(API_HOST, BANK_ID, our_account)

# POST request
print 'POST {0} to {1}'.format(directlogin, post_url)
response = requests.post(post_url, json=post_data, headers=directlogin)
print response.status_code
print response.text
