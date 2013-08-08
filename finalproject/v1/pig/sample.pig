


http://stackoverflow.com/questions/12644392/loading-raw-json-into-pig

REGISTER 'lib/elephant-bird-2.2.3.jar';
REGISTER 'lib/json-simple-1.1.1.jar';

alltweets = LOAD '/Volumes/DATA/robert/Desktop/Projects/GA/finalproject/Data/tw100k.dump' 
    USING com.twitter.elephantbird.pig.load.JsonLoader('-nestedLoad');

nondeleted = FILTER alltweets
        BY $0#'created_at' != 'deleted' OR $0#'created_at' IS NOT NULL ;

tweets = FOREACH nondeleted GENERATE
          $0#'id_str', 
          $0#'created_at',  
          $0#'user'#'id_str' as uid_str,
          $0#'user'#'screen_name',
          $0#'geo'#'coordinates' as coordinates,
          $0#'text' 
          ;

rmf '/Volumes/DATA/robert/Desktop/Projects/GA/finalproject/Data/tweet-results';
STORE tweets into '/Volumes/DATA/robert/Desktop/Projects/GA/finalproject/Data/tweet-results' 
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
            


-- agg = FOREACH grouped_data GENEREATE group, AVG(grouped_data.SalaryNormalized)

-- cnt = foreach grpd generate group, COUNT(tweets);

