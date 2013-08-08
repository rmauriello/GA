/*
 * https://raw.github.com/mortardata/mortar-examples/master/pigscripts/coffee_tweets.pig
 *
 * Count of tweets by FIPS county and by state / country?
 *
 * Loads up a week's-worth of tweets from the twitter-gardenhose (https://github.com/mortardata/twitter-gardenhose),
 * searches through them for telltale coffee snob phrases (single origin, la marzocco, etc) and rolls up the 
 * results by US state.
 *
 * NOTE: To switch between datasets of different sizes and conveniently switch between running locally 
 * or on a remote service such as Mortar, use the -f option to reference a file in the params/ directory.
 */


-- Register the python User-Defined Functions (UDFs)
   -- twitter_places.py (given Wheeling, WV) returns state (as abbreviation)
   -- coords2countycode (given latitude,longitude) return FIPS county code as string


REGISTER 'udfs/twitter_places.py' USING jython AS twitter_places;
REGISTER 'udfs/tw_parse.py' USING jython AS tw_parse;
-- REGISTER 'udfs/python/coords2countycode.py' USING jython AS coords2countycode;


%default TWEET_LOAD_PATH 's3://mauriello/twitter/tw.dump'
%default OUTPUT_PATH 's3://mauriello/twitter/output/coffee_tweets'


tweets =  LOAD '$TWEET_LOAD_PATH' 
         USING org.apache.pig.piggybank.storage.JsonLoader(
                   'coordinates:map[], 
                   created_at:chararray, 
                   current_user_retweet:map[], 
                   entities:map[], 
                   favorited:chararray, 
                   id_str:chararray, 
                   in_reply_to_screen_name:chararray, 
                   in_reply_to_status_id_str:chararray, 
                   place:map[], 
                   possibly_sensitive:chararray, 
                   retweet_count:int, 
                   source:chararray, 
                   text:chararray, 
                   truncated:chararray, 
                   user:map[], 
                   withheld_copyright:chararray, 
                   withheld_in_countries:{t:(country:chararray)}, 
                   withheld_scope:chararray');


#
# v1. All fields. Got some Pig errors and job aborted
#
alltweets =  LOAD 's3://mauriello/twitter/tw.dump.0802.gz' 
         USING JsonLoader(
                'created_at:chararray,
                id:long,
                id_str:chararray,
                text:chararray,
                source:chararray,
                truncated:chararray,
                in_reply_to_status_id:int,
                in_reply_to_status_id_str:chararray,
                in_reply_to_user_id:int,
                in_reply_to_user_id_str:chararray,
                in_reply_to_screen_name:chararray,
                user:map[],
                geo:map[],
                coordinates:map[],
                place:map[],
                contributors:chararray,
                retweet_count:int,
                favorite_count:int,
                entities:map[],
                favorited:chararray,
                retweeted:chararray,
                filter_level:chararray, 
                lang:chararray');

#
# v2. Most fields - mostly works but only get id, created, text
#
alltweets =  LOAD 's3://mauriello/twitter/tw.dump.0802.gz' 
         USING JsonLoader(
                'created_at:chararray,
                id:long,
                id_str:chararray,
                text:chararray,
                user:map[],
                geo:map[],
                coordinates:map[],
                place:map[],
                lang:chararray');


goodtweets = FILTER alltweets 
        BY created_at != 'deleted' ;


                uid_str         = tweet['user']['id_str']
                screen_name     = tweet['user']['screen_name']


#
# Example from book
#

--batting_production.pig
register 'production.py' using jython as bballudfs;
players = load 'baseball' as (name:chararray, team:chararray,
          pos:bag{t:(p:chararray)}, bat:map[]);
nonnull = filter players by bat#'slugging_percentage' is not null and bat#'on_base_percentage' is not null;
calcprod = foreach nonnull generate name, bballudfs.production(
                                          (float)bat#'slugging_percentage',     
                                          (float)bat#'on_base_percentage');

#
tweets = FOREACH goodtweets
   GENERATE created_at, 
            id_str,
            text, 
            lang,
            user#'id_str' AS uid_str:chararray,
            user#'screen_name' AS screen_name:chararray,
            geo#'coordinates' AS geo:chararray;

            coordinates#'coordinates' AS coordinates:chararray;
            place#'bounding_box'#coordinates as place;

      
            
rmf s3://mauriello/twitter/tweet-results ;
store tweets into 's3://mauriello/twitter/tweet-results' USING PigStorage('\t');

