# -*- coding: utf-8 -*-

from __future__ import print_function    # (at top of module)
import sys, time, requests


# Note: in order to use this example, you need to have at least one account
# that you can send money from (i.e. be the owner).
# All properties are now kept in one central place

from props.danskebank import *
#from props.socgen import *

ROLES=['CanQueryOtherUser']
ENTITLEMENTS=['CanQueryOtherUser']

# You probably don't need to change those
import lib.obp
obp = lib.obp

obp.setBaseUrl(BASE_URL)
obp.setApiVersion(API_VERSION)

# Login and set authorized token
obp.login(USERNAME, PASSWORD, CONSUMER_KEY)

# Get all entitlements 
print ("")
print (" --- Get user's entitlements")
all_entitlements = obp.getAllEntitlements()
print ("all entitlements:\n{0}".format(all_entitlements))

# Get current user 
print ("")
print (" --- Get current user")
user = obp.getCurrentUser()
user_id = user['user_id']
print ("current user id: {0}".format(user))

# Get user entitlements 
print ("")
print (" --- Get user's entitlements")
entitlements = obp.getAllEntitlements()
if 'error' not in entitlements:
  print ("user {0} entitlements:\n{1}".format(user_id, entitlements))
else:

  # Add CanGetEntitlementsForAnyUserAtOneBank entitlement
  print ("")
  print (" --- Add CanGetEntitlementsForAnyUserAtAnyBank entitlement")
  response = obp.addEntitlement('CanGetEntitlementsForAnyUserAtAnyBank', user_id, OUR_BANK)
  print ("response:\n{0}".format(response))


# Add system roles from list
for role in ROLES:
  print ("")
  print (" --- Add {0} role".format(role))
  response = obp.addRole(role, user_id)
  print ("response:\n{0}".format(response))

# Add entitlements from list
for entitlement in ENTITLEMENTS:
  print ("")
  print (" --- Add {0} entitlement".format(entitlement))
  response = obp.addEntitlement(entitlement, user_id, OUR_BANK)
  print ("response:\n{0}".format(response))

print ("")
