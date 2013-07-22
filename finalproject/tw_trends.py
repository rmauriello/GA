#
# Use the Twitter API to get the top world and US trends 
#  - write out to ..
#

import twitter
import pprint as pprint
import json
import urllib
import sys


CONSUMER_KEY = 
CONSUMER_SECRET = 
OAUTH_TOKEN = 
OAUTH_TOKEN_SECRET = 

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

print twitter_api


# WORLD_WOE_ID = 1

WORLD_WOE_ID = 1118129
US_WOE_ID = 23424977

# Prefix id with the underscore for query string parameterization.
# Without the underscore, the twitter package appends the id value
# to the URL itself as a special case keyword argument

def get_trends():

    world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
    # us_trends = twitter_api.trends.place(_id=US_WOE_ID)


    print json.dumps(world_trends, indent=1)
    for i in range( len(world_trends[0]['trends'])):
        try:
            print i,  world_trends[0]['trends'][i]['name']
        except:
            print "Error with printing", sys.exc_info()[0]
            try:
                print i, world_trends[0]['trends'][i]['name'].decode('utf8')
            except:
                e = sys.exc_info()[0]
                print "Error with UTF8 decoding", e, world_trends[0]['trends'][i]['name']
                try:
                    print i,  world_trends[0]['trends'][i]['name'].decode('unicode-escape')
                except:
                    print "Error with Unicode escaping"
                    pass
          
    # print json.dumps(us_trends, indent =1) 
    # for i in range( len(world_trends[0]['trends'])):
    #     try:
    #         print i,  us_trends[0]['trends'][i]['name'].decode('utf8')
    #     except:  # to catch stuff like 'Malha\\u00e7\\u00e3o'
    #         print i,  us_trends[0]['trends'][i]['name'].decode('unicode-escape')
      
if __name__ == '__main__':
  get_trends()
