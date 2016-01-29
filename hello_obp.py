# -*- coding: utf-8 -*-
import requests

API_HOST = 'http://127.0.0.1:8080'
URL_LOGIN = '{0}/my/logins/direct'.format(API_HOST)
BANK_ID = 'obp-bank-x-gh'
loginData = {
    'username': 'robert.x.0.gh@example.com',
    'password': '3e3a3102'
}

print 'Posting {0} to {1}'.format(loginData, URL_LOGIN)
response = requests.post(URL_LOGIN, json=loginData)
print response.status_code
#print response.text

TOKEN = response.text.split("=")[1]
URL_IMPORT = '{0}/obp/v1.2.1/banks/{1}/accounts/private'.format(API_HOST, BANK_ID)

data = {
        'token': TOKEN 
}

print 'Posting {0} to {1}'.format(data, URL_IMPORT)
response = requests.post(URL_IMPORT, json=data)
print response.status_code
print response.text

