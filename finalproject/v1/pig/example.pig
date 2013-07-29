/*
 * https://raw.github.com/mortardata/mortar-examples/master/pigscripts/coffee_tweets.pig
 *
 * Which US state is home to the highest concentration of coffee snobs?
 *
 * Loads up a week's-worth of tweets from the twitter-gardenhose (https://github.com/mortardata/twitter-gardenhose),
 * searches through them for telltale coffee snob phrases (single origin, la marzocco, etc) and rolls up the 
 * results by US state.
 *
 * NOTE: To switch between datasets of different sizes and conveniently switch between running locally 
 * or on a remote service such as Mortar, use the -f option to reference a file in the params/ directory.
 */


-- Register the python User-Defined Functions (UDFs) we will use
-- ** twitter_places.py (given Wheeling, WV) returns state (as abbreviation)
-- ** coffee.py (given text) returns if text found in list of coffee snob terms

REGISTER 'udfs/twitter_places.py' USING streaming_python AS twitter_places;
REGISTER 'udfs/coffee.py' USING streaming_python AS coffee;

REGISTER 'udfs/twitter_places.py' USING jython AS twitter_places;
REGISTER 'udfs/coffee.py' USING jython AS coffee;


-- coords2countycode (given latitude,longitude) return FIPS county code as string
-- ** REGISTER '../udfs/python/coords2countycode.py' USING streaming_python AS coords2countycode;


-- ** Let's start off with S3 native (s3n) even though it has 5GB file limit
-- ** Don't have to create buckets and other tools can access files 
-- ** Use S3/S3N for persistent storage and HDFS for temporary use
 
-- %default TWEET_LOAD_PATH 's3n://twitter-gardenhose-mortar/example'
-- %default OUTPUT_PATH 's3n://mortar-example-output-data/$EMAIL_S3_ESCAPED/coffee_tweets'

%default TWEET_LOAD_PATH 's3://mauriello/twitter/tw.dump'
%default OUTPUT_PATH 's3://mauriello/twitter/output/coffee_tweets'

-- Load up tweets specified in env parameter file supplied at runtime (env/x.params)
--   coordinates, place, (no location in load)
-- 


      --   USING org.apache.pig.piggybank.storage.JsonLoader(
tweets =  LOAD '$TWEET_LOAD_PATH' 
         USING JsonLoader(
                   'coordinates:map[], created_at:chararray, current_user_retweet:map[], entities:map[], favorited:chararray, id_str:chararray, in_reply_to_screen_name:chararray, in_reply_to_status_id_str:chararray, place:map[], possibly_sensitive:chararray, retweet_count:int, source:chararray, text:chararray, truncated:chararray, user:map[], withheld_copyright:chararray, withheld_in_countries:{t:(country:chararray)}, withheld_scope:chararray');


tweets =  LOAD 's3://mauriello/twitter/tw1k.dump' 
         USING JsonLoader(
                   'coordinates:map[], created_at:chararray, entities:map[], favorited:chararray, id_str:chararray,   place:map[], source:chararray, text:chararray,  user:map[]');



-- Filter to get only tweets that have a location in the US
--  also, 'country' as name and 'full_name' as place name, e.g. "Paris, Paris"
--  https://dev.twitter.com/docs/platform-objects/places

tweets_with_place = 
    FILTER tweets 
        BY place IS NOT NULL 
       AND place#'country_code' == 'US' 
       AND place#'place_type' == 'city';


tweets_with_coords = 
    FILTER tweets 
        BY coordinates IS NOT NULL;


-- Parse out the US state name from the location
-- and determine whether this is a coffee tweet.
-- ** Use the Python UDF twitter_places and coffee registered above

coffee_tweets = 
    FOREACH tweets_with_place
   GENERATE text, 
            place#'full_name' AS place_name,
            twitter_places.us_state(place#'full_name') AS us_state,
            coffee.is_coffee_tweet(text) AS is_coffee_tweet;


coffee_tweets = 
    FOREACH tweets_with_place
   GENERATE text, 
            place#'full_name' AS place_name;

-- Filter to make sure we only include results with
-- where we found a US State
with_state = 
    FILTER coffee_tweets
        BY us_state IS NOT NULL;

-- Group the results by US state
grouped = 
    GROUP with_state 
       BY us_state;

-- Calculate the percentage of coffee tweets
-- for each state
coffee_tweets_by_state = 
    FOREACH grouped
   GENERATE group as us_state,
            SUM(with_state.is_coffee_tweet) AS num_coffee_tweets,
            COUNT(with_state) AS num_tweets,
            100.0 * SUM(with_state.is_coffee_tweet) / COUNT(with_state) AS pct_coffee_tweets;

coffee_tweets_by_county = 
    FOREACH grouped
   GENERATE group as us_state,
            SUM(with_state.is_coffee_tweet) AS num_coffee_tweets,
            COUNT(with_state) AS num_tweets,
            100.0 * SUM(with_state.is_coffee_tweet) / COUNT(with_state) AS pct_coffee_tweets;


-- Order by percentage to get the largest
-- coffee snobs at the top
ordered_output = 
    ORDER coffee_tweets_by_state 
       BY pct_coffee_tweets DESC;

-- Remove any existing output and store the results to S3
rmf $OUTPUT_PATH;
STORE ordered_output 
 INTO '$OUTPUT_PATH'
USING PigStorage('\t');


rmf s3://mauriello/twitter/coffee-results
store coffee_tweets into 's3://mauriello/twitter/coffee-results' USING PigStorage('\t');
  
store ordered_output into 's3://mauriello/twitter/coffee-results';   
