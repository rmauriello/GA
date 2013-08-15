#!/usr/bin/env python
#
# Read tweets from STDIN and parse out locations and print county code to STDOUT
#
#
import sys
# import ujson as json
import json
import string
import re
import time

DEBUG = 1
# @outputSchema('us_state:chararray')

# datestr = parsed['created_at']
# ts =  int(time.mktime(time.strptime(datestr, "%a %b %d %H:%M:%S +0000 %Y")))
# ts =  ts * 1000 + created_cnt

# text = parsed['text'].decode('unicode-escape').strip()
# text = re.sub(r"\W+", " ", text)    # Replace at least 1 nonalphanumeric characters with space
# text = text.replace("[-_,.:|]","") # Delete - or _ 

# print  ts,  "|C ", text.strip().lower(), "|name", parsed['user']['screen_name']
    

def clean_tweets(t):
    data = []
    deleted_tweets = 0
    for line in t:    
        filter(lambda x: x in string.printable, line)
        if re.match(r'^{"delete".*',line):
            deleted_tweets += 1
            next
        else:
            data.append(json.loads(line))
    return data

def main():
    i=0
    valid_cnt      = 0
    created_cnt    = 0
    deleted_cnt    = 0
    other_cnt      = 0
    nogeo_cnt      = 0
    invalid_cnt    = 0

    # for line in tweet_file: 
        
    for line in sys.stdin:
        filter(lambda x: x in string.printable, line)

        try:
            tweet = json.loads(line)
            valid_cnt += 1
            # print tweet.keys()
            
        except:
            # print "Error: Invalid JSON record"
            invalid_cnt += 1
            tweet = ""
            continue

        if 'created_at' in tweet.keys():
            
            try:
                # Store timestamp information (Sun Jul 14 19:33:39 +0000 2013)
                datestr         = tweet['created_at']
                ts =  int(time.mktime(time.strptime(datestr, "%a %b %d %H:%M:%S +0000 %Y")))
                ts =  ts * 1000 + created_cnt

                tid_str         = tweet['id_str']
                text            = tweet['text']
                text            = text.replace("\t", "") 
                uid_str         = tweet['user']['id_str']
                screen_name     = tweet['user']['screen_name']
                followers_count = tweet['user']['followers_count']
                friends_count   = tweet['user']['friends_count']
                protected       = tweet['user']['protected']


                if 'geo' in tweet.keys():
                    locations = tweet['geo']['coordinates']

                elif 'coordinates' in tweet.keys():
                    locations = tweet['coordinates']['coordinates']
                    # Need to reverse latitude/longitude ***
                    rev   = locations.split(',')
                    locations = [ rev[1][1:], rev[0][1:] ]
                    sys.stderr.write("Found coordinates instead of geo:  reversed to get latitude/longitude\n")

                elif 'place' in tweet.keys():
                    locations = tweet['place']['bounding_box']['coordinates']

                    # Watch out for nonpoint locations
                else:
                    sys.stderr.write("Expecting geo information but didn't find anything. Moving on...\n")
                    nogeo_cnt += 1
                    continue

                
                print '\t'.join(map(str, [tid_str, datestr, uid_str, screen_name, locations, text]  ))

                created_cnt += 1
            except:
                continue
        elif 'delete' in tweet.keys():
            deleted_cnt += 1
            continue
        else:
            sys.stderr.write("Error - was expecting either deleted or created tweets. Moving on...\n" ) 
            other_cnt += 1
            continue

    if DEBUG:
        sys.stderr.write("Valid tweets  = %d\n" %    valid_cnt) 
        sys.stderr.write("\tGood tweets  = %d\n" %    created_cnt) 
        sys.stderr.write("\t\tGood tweets w/o geo = %d\n" %    nogeo_cnt) 
        
        sys.stderr.write("\tDeleted tweets  = %d\n" %   deleted_cnt)
        sys.stderr.write("\tOther tweets  = %d\n" % other_cnt)
        sys.stderr.write("Invalid tweets  = %d\n" %    invalid_cnt) 

if __name__ == '__main__':
    main()
