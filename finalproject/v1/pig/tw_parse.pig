/*


*/

%default TWEET_LOAD_PATH 's3://mauriello/twitter/tw.dump'

-- Use following for AWS pig
REGISTER 's3://mauriello/lib/json-simple-1.1.1.jar';
REGISTER 's3://mauriello/lib/elephant-bird-2.2.3.jar';
REGISTER 's3://mauriello/udfs/pigutils.py' USING jython as myudfs;

-- Use following for local pig
REGISTER 'lib/json-simple-1.1.1.jar';
REGISTER 'lib/elephant-bird-2.2.3.jar';
REGISTER '/Volumes/DATA/robert/Desktop/Projects/GA/finalproject/v1/pig/udfs/python/pigutils.py' USING jython AS myudfs;


#
# This should work but doesn't. Got some Pig errors and job aborted
#
alltweets =  LOAD '$TWEET_LOAD_PATH' 
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


--alltweets = LOAD 's3://mauriello/twitter/tw.dump.0806.gz' 
--            USING com.twitter.elephantbird.pig.load.JsonLoader('-nestedLoad');


alltweets = LOAD '/Volumes/DATA/robert/Desktop/Projects/GA/finalproject/Data/tw.dump.{0[0-9][0-1][0-9]}.gz' 
            USING com.twitter.elephantbird.pig.load.JsonLoader('-nestedLoad');


nondeleted = FILTER alltweets
        BY $0#'created_at' != 'deleted' OR $0#'created_at' IS NOT NULL ;

tweets = FOREACH nondeleted GENERATE
          $0#'id_str', 
          $0#'created_at' as timestamp,  
          $0#'user'#'id_str' as uid_str,
          $0#'user'#'screen_name',
          $0#'geo'#'coordinates' as coordinates,
          $0#'text' ;

grpd = GROUP tweets by timestamp ;

      -- grpd: {group: bytearray,tweets: {(bytearray,timestamp: bytearray,uid_str: bytearray,bytearray,coordinates: bytearray,bytearray)}}
      -- Mon Aug 05 04:11:29 +0000 2013  {(364237198411169792,Mon Aug 05 04:11:29 +0000 2013,289114860,martha34k,{(37.25306022),(-80.03383463)},<U+1F46C><U+1F46C><U+1F46C><U+1F64D><U+1F46C>
      <U+1F46C><U+1F46C>),(...),(...) }

-- in the FOREACH, key field is "group". It's like a SQL alias
-- Want to count all the items in the bag {  }

tweets_by_sec    = FOREACH grpd GENERATE group, COUNT(tweets.timestamp) as rate;
    
    -- tweets_by_sec: {group: bytearray,rate: long}


-- Not quite sure what ALL is doing. Joining the bags from all the mappers into one big bag?
tweets_by_sec_all = GROUP tweets_by_sec ALL;
    -- tweets_by_sec_all: {group: chararray,tweets_by_sec: {(group: bytearray,rate: long)}}

max_rate         = FOREACH tweets_by_sec_all GENERATE group, MAX( tweets_by_sec.rate);
    -- max_rate: {group: chararray,long}


--tweets_by_minute = FOREACH tweets_by_sec GENERATE group,
--            COUNT( (chararray) myudfs.by_minute( (chararray)tweets.timestamp)) as rate_minute;

tweets_minute   = GROUP tweets BY  myudfs.by_minute(timestamp) ;

tweets_by_minute = FOREACH tweets_minute GENERATE group,
                COUNT( tweets) as rate_minute;

tweets_hour    = GROUP tweets BY myudfs.by_hour(timestamp) ;

tweets_by_hour = FOREACH tweets_hour GENERATE group,
                COUNT( tweets) as rate_hour;

-- rmf '/Volumes/DATA/robert/Desktop/Projects/GA/finalproject/Data/tweet-results';

STORE tweets_by_minute into '/Volumes/DATA/robert/Desktop/Projects/GA/finalproject/Data/tweet-results' USING PigStorage();


STORE tweets_by_minute into '/Volumes/DATA/robert/Desktop/Projects/GA/finalproject/Data/tweet-rate-minute' USING PigStorage();

STORE tweets_by_hour into '/Volumes/DATA/robert/Desktop/Projects/GA/finalproject/Data/tweet-rate-hour' 
    USING PigStorage();



STORE tweets_by_minute into 's3://mauriello/twitter/tweet-rate-minute' 
    USING PigStorage();

STORE tweets_by_hour into 's3://mauriello/twitter/tweet-rate-hour' 
    USING PigStorage();



-- This should work also but does not
-- 

alltweets =  LOAD '/Volumes/DATA/robert/Desktop/Projects/GA/finalproject/Data/tw10k.dump'
         USING JsonLoader('
                created_at:chararray,
                id:long,
                id_str:chararray,
                text:chararray,
                user:map[]
                ');

tweets = FOREACH nonull
   GENERATE id_str,
            created_at, 
            (chararray)user#'id_str' as uid_str,
            (chararray)user#'screen_name'  as screen_name,
            (chararray)geo#'coordinates' as coordinates,
            text,     
            user:map[]
            ');        
          