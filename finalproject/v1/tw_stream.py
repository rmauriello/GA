#
# Connect to the Twitter stream and write to a file
#
# Use OAUTH to access Twitter's live 1% stream of tweets
#  Write to STDOUT
#


import sys
import json
import string, re

import oauth2 as oauth
import urllib2 as urllib
import sys
import pandas as pd

def filter_tweets(text):
    filter(lambda x: x in string.printable, line)
    if re.match(r'^{"delete".*',line):
        deleted_tweets += 1
        next
    else:
        data.append(json.loads(line))


#
# Construct, sign, and open a twitter request using the hard-coded credentials above.
#
def twitterreq(url, method, parameters):
  try:
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                               token=oauth_token,
                                               http_method=http_method,
                                               http_url=url, 
                                              parameters=parameters)
  except:
    e = sys.exc_info()[0]
    sys.stderr.write("Error from oauth request: " + str(e) + "\n")
    

  try:
    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)
  except:
    e = sys.exc_info()[0]
    sys.stderr.write("Error from sign request: " + str(e) + "\n")
        
  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)
  return response

#
# Bounding box for contiguous US is:   '-124.7625,24.5210,-66.9326,49.3845'
#
def fetchsamples():
  # url = "https://stream.twitter.com/1/statuses/sample.json"
  url = "https://stream.twitter.com/1/statuses/filter.json"
  parameters={}
  parameters['locations'] = '-124.7625,24.5210,-66.9326,49.3845'   # For contiguous US?
  # parameters['locations']="-122.75,36.8,-121.75,37.8"            # For San Francisco 
  


  try:
    response = twitterreq(url, "GET", parameters)
    for line in response:
      print line.strip()
      # - filtering here ..self.
  except:
    e = sys.exc_info()[0]
    sys.stderr.write("Error from Twitter request: " + url + "\n")


if __name__ == '__main__':

  #
  # Get authorization using OAUTH. Expecting tokens as key, value
  #
  try:
    tokens = pd.read_csv("../Data/twitter_tokens.txt", header=None)
    access_token_key    = tokens[1][0].strip()
    access_token_secret = tokens[1][1].strip()

    consumer_key        = tokens[1][2].strip()
    consumer_secret     = tokens[1][3].strip()

  except:
    sys.stderr.write("Error reading tokens file. Exiting...\n")

    exit(-1)


  _debug = 0

  oauth_token         = oauth.Token(key=access_token_key, secret=access_token_secret)
  oauth_consumer      = oauth.Consumer(key=consumer_key, secret=consumer_secret)
  signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

  # http_method = "GET"
  http_method = "POST"

  http_handler  = urllib.HTTPHandler(debuglevel=_debug)
  https_handler = urllib.HTTPSHandler(debuglevel=_debug)

  fetchsamples()
