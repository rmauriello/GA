#!/usr/bin/env python

import sys
import shapely
import shapely.speedups
import shapefile
from shapely.geometry import Point, Polygon
from rtree import index
from math import log

DEBUG=1
shapely.speedups.enable()

#
# Given latitude/longitude, return the FIPS county code
#  Some rtree intersection logic from https://gist.github.com/fawcett/5251327
#
def latlon2countycode(lat,lon):
	hits = []
	try:
		# Return a list of all counties that match lon OR lat
		hits = list(idx.intersection((lon,lat,lon,lat)))
		if len(hits) == 1:                  # Exact match
			recno = hits[0]
		elif len(hits) > 1:                 # Multiple candidate counties
        #	
		# For example, 42.66326054 -87.80922716 [3180, 3193] - either kenosha or racine county. 
			for hitIdx in hits:             # Search all counties in list
				county = shapes[hitIdx]     
				poly   = Polygon(county.points)
				if poly.contains(Point(lon,lat)):
					recno = hitIdx
					break
				else:                       
					continue				
		else:
			# if DEBUG:
			# 	sys.stderr.write("Error: Latlon2countycode unexpected error. -1\n")
			recno = -1
	except:
		# Lat/Lon don't match US county shapefiles
		recno = 0
	return recno

if DEBUG: 
	sys.stderr.write("Reading shapefiles and making rtree index\n")

try:
	sf      = shapefile.Reader("../Data/shapefiles/uscounties/all_counties.shp")
	shapes  = sf.shapes()    # Get the polygons in the shapefiles
	records = sf.records()   # Get the data, particulary county name and FIPS code
except:
	sys.stderr.write("Error reading shapefiles. Exiting...\n")
	exit(-1)

# Create rtree index and load the bounding boxes from the shapefiles
idx = index.Index()
for i, shape in enumerate(shapes):
	idx.insert(i, shape.bbox)

if DEBUG:
	sys.stderr.write("Starting to parse input\n")

# Initialize county aggregator
county_sum   = {}
coords2recno = {}
cache_cnt    = 0
nocache_cnt  = 0
lookup_errs  = 0
lineno = 0
lookup_cnt = 1

#
for line in sys.stdin:
	lineno += 1
	try:
		words = line.split(',')
		lat = float(words[0].strip()[2:])
		lon = float(words[1].strip()[0:-1])

		# Really basic caching. Don't compute if we have result already
		geokey =  "%0.4f%0.4f" % (lon,lat)
		try:
			recno = coords2recno[geokey]     
			cache_cnt += 1 
		except KeyError:
			recno = latlon2countycode(lat,lon)
			nocache_cnt += 1

		if recno > 0:
			coords2recno[geokey] = recno
			county_code = records[recno][5]
			county_name = records[recno][7]

			# Count number of tweets per county
			county_sum[county_code] = county_sum.get(county_code, 0) + 1

			lookup_cnt += 1
			if DEBUG and lookup_cnt % 10000 == 0:
				sys.stderr.write(' '.join(map(str,[lineno, lookup_cnt, lat, lon, recno, county_code, county_name]	)) + "\n")

		else:
			lookup_errs += 1
			continue
	except:
		continue

#
# Scale the county data by maximum value.
#
# Need to find 2010 Census population by FIPS county dataset
#

if DEBUG:
	sys.stderr.write("IN cache  = %d\n" %    cache_cnt) 
	sys.stderr.write("OUT of cache = %d\n" %   nocache_cnt)
	sys.stderr.write("TOTAL RECORDS  = %d\n" % lineno)
	sys.stderr.write("LOOKUPS  =  %d\n" %     lookup_cnt)
	sys.stderr.write("LOOKUP errors  = %d\n" % lookup_errs)  

print "id\trate"             # d3.tsv wants a header line by default
for key,value in county_sum.items():
	print "%s\t%d" % (key,  value )

#
# Write to database
#
# import pymongo
# from pymongo import MongoClient
# client = MongoClient('localhost', 27017)
# db = client.test_database

# # Create a collection
# posts = db.posts

# Bulk insert
# new_posts = [{"author": "Mike",
# ...               "text": "Another post!",
# ...               "tags": ["bulk", "insert"],
# ...               "date": datetime.datetime(2009, 11, 12, 11, 14)},
# ...              {"author": "Eliot",
# ...               "title": "MongoDB is fun",
# ...               "text": "and pretty easy too!",
# ...               "date": datetime.datetime(2009, 11, 10, 10, 45)}]
# posts.insert(new_posts)


# Could store using Mongo's geo module


# Store county data as time series
#  Get traffic trends (total tweets, insults, categories)
#  Aggregate at hour, day, month
#

# if __name__ == '__main__':
#     main()

