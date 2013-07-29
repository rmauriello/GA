#!/usr/bin/env python
#
# Read Twitter JSON file and filter
#
# Usage:
#     preprocess.py < STDIN > STDOUT
#
# Each line should be a JSON object {}
# Looks like if the stream is interrupted, it terminates with no JSON but "Error with twitter request..."
# 
# Todos:
#   Error handling needs a lot of work.
#   Parsing of retweets
#   
#

import sys
import json
import string
import re
import time, datetime    

def cleanup_tweet(line):
  dict_out ={}
  
  text = text.replace("'", "")        # Remove apostrophes (inside words, etc.)
  text = text.replace("\"", "")       # Remove quote (inside words, etc.)
  
  text = re.sub(r"\W+", " ", text)    # Replace at least 1 nonalphanumeric characters with space
  text = text.replace("[-_,.:|]","") # Delete - or _ 

  text = text.lower()                 # Convert all to lowercase
  # text = text.decode('unicode-escape')

  text = text.split()
  words = []
  for word in text:                   # Remove duplicate words, e.g. the the
    if word in words:
      continue
    words.append(word)

  return " ".join(words)             # Convert list back into string
  

def main():
	valid_cnt      = 0
	created_cnt    = 0
	deleted_cnt    = 0
	other_cnt      = 0
	invalid_cnt    = 0

	for line in sys.stdin:
		filter(lambda x: x in string.printable, line)

		# Catch any exceptions
		try:
			parsed = json.loads(line)
			valid_cnt += 1
		except:
			print "Error: Invalid JSON record"
			invalid_cnt += 1
			parsed = ""
			continue

		if 'created_at' in parsed.keys():
			try:
				# Create some unique identifier based on timestamp + counter
	
				datestr = parsed['created_at']
				ts =  int(time.mktime(time.strptime(datestr, "%a %b %d %H:%M:%S +0000 %Y")))
				ts =  ts * 1000 + created_cnt
				
				text = parsed['text'].decode('unicode-escape').strip()
				text = re.sub(r"\W+", " ", text)    # Replace at least 1 nonalphanumeric characters with space
				text = text.replace("[-_,.:|]","") # Delete - or _ 

				print  ts,  "|C ", text.strip().lower(), "|name", parsed['user']['screen_name']
	
				created_cnt += 1
			except:
				continue

		elif 'delete' in parsed.keys():
			deleted_cnt += 1
			continue
		else:
			# print "Error - was expecting either deleted or created tweets. Moving on"
			other_cnt += 1
			continue

	# print "Valid JSON records: ", valid_cnt
	# print "\tCreated: s/b 20286 ", created_cnt
	# print "\tDeleted: s/b 0 ",  deleted_cnt
	# print "\tOther: ", other_cnt
	# print "Invalid JSON records", invalid_cnt
        
if __name__ == '__main__':
    main()

