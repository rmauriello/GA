
#
# pigutils.py
#

# datestr = "Mon Aug 05 04:14:32 +0000 2013" 
# ts =  int(time.mktime(time.strptime(datestr, "%a %b %d %H:%M:%S +0000 %Y")))

def outputSchema(schema_str):
    def wrap(f):
        def wrapped_f(*args):
            return f(*args)
        return wrapped_f
    return wrap

    
@outputSchema('by_minute:chararray')
def by_minute(datestr):
	return datestr[0:16]

@outputSchema('by_hour:chararray')
def by_hour(datestr):
	return datestr[0:13]

@outputSchema('by_day:chararray')
def by_day(datestr):
	return datestr[0:10]


