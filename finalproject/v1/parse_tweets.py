#
# Read tweets from STDIN and parse out locations and print county code to STDOUT
#
#
import sys
import json
import string
import re


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
    invalid_cnt    = 0

    # for line in tweet_file: 
        
    for line in sys.stdin:
        filter(lambda x: x in string.printable, line)

        try:
            tweet = json.loads(line)
            # print tweet.keys()
            
        except:
            # print "Error: Invalid JSON record"
            tweet = ""
            continue

        if 'created_at' in tweet.keys():

            try:
                text        = tweet['text']
                id_str      = tweet['user']['id_str']
                screen_name = tweet['user']['screen_name']
                # print id_str, screen_name

                if 'geo' in tweet.keys():
                    locations = tweet['geo']['coordinates']

                elif 'coordinates' in tweet.keys():
                    locations = tweet['coordinates']['coordinates']
                    # Need to reverse latitude/longitude ***
                    rev   = locations.split(',')
                    locations = [ rev[1][1:], rev[0][1:] ]
                    print "coordinates:  reversed latitude/longitude"

                elif 'place' in tweet.keys():
                    locations = tweet['place']['bounding_box']['coordinates']
                    # Watch out for nonpoint locations ***
                else:
                    continue

                # Some weirdness here with join, e.g. ",".join(out)
                out = [locations, id_str, screen_name, text]
                print out

            except:
                continue
        elif 'delete' in tweet.keys():
            deleted_cnt += 1
            continue
        else:
            print "Error - was expecting either deleted or created tweets. Moving on"
            other_cnt += 1
            continue


if __name__ == '__main__':
    main()
