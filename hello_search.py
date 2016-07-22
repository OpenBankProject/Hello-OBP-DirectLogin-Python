# -*- coding: utf-8 -*-

# Set search query and elasticsearch index
SEARCH_QUERY="q=obp"
ES_INDEX = "metrics"

# Note: in order to use this example, you need to have an user 
# that has entitlement CanSearchWarehouse or CanSearchMetrics
USERNAME     = 'robert.x.0.gh@example.com'
PASSWORD     = '3e3a3102'
CONSUMER_KEY = 'adwf5qomvtvtya5ss3z5aizpr2b4hq054aoqa2t2'

# API server URL
BASE_URL  = "http://127.0.0.1:8080"
LOGIN_URL = '{0}/my/logins/direct'.format(BASE_URL)

# API server will redirect your browser to this URL, should be non-functional
# You will paste the redirect location here when running the script
CALLBACK_URI = 'http://127.0.0.1/cb'

# You probably don't need to change those
loginHeader  = { 'Authorization' : 'DirectLogin username="%s",password="%s",consumer_key="%s"' % (USERNAME, PASSWORD, CONSUMER_KEY)}


import sys, requests
# Helper function to merge headers
def merge(x, y):
    z = x.copy()
    z.update(y)
    return z

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

# Perform search
response = requests.get(u"{0}/obp/v2.0.0/search/{1}/{2}".format(BASE_URL, ES_INDEX, SEARCH_QUERY), headers=merge(directlogin, content_json))

# Print result
print response.status_code
print response.text

