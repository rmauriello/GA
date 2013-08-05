#!/usr/bin/env python

import sys
import shapely
import shapefile
from shapely.geometry import Point, Polygon
from rtree import index
from math import log


# 42.66326054 -87.80922716 [3180, 3193] - either kenosha or racine county. 

#
# Given latitude/longitude, return the FIPS county code
#  Some rtree intersection logic from https://gist.github.com/fawcett/5251327
#
def latlon2countycode(lat,lon):
	try:
		hits = list(idx.intersection((lon,lat,lon,lat)))
		if len(hits) == 1:
			recno = hits[0]
		elif len(hits) > 1:
			# print "multiple hits: ", lat, lon, hits
			for hitIdx in hits:
				county = shapes[hitIdx]  # county needs to be polygon?
				poly   = Polygon(county.points)
				if poly.contains(Point(lon,lat)):
					# print "\t\t found ", hitIdx, records[hitIdx][5], records[hitIdx][7]
					recno = int(hitIdx)
					break
		else:
			recno = -1
	except:
		recno = -1
	return int(recno)

# print "#Reading shapefiles and making rtree index"
try:
	sf      = shapefile.Reader("../Data/shapefiles/uscounties/all_counties.shp")
	shapes  = sf.shapes()    # Get the polygons in the shapefiles
	records = sf.records()   # Get the data, particulary county name and FIPS code
except:
	# print "#Error reading shapefiles. Exiting..."
	exit(-1)

# Create rtree index and load the bounding boxes from the shapefiles
idx = index.Index()
for i, shape in enumerate(shapes):
    idx.insert(i, shape.bbox)

# print "#Starting to parse input"
# Initialize county aggregator
county_sum = {}

for line in sys.stdin:
	
	try:
		words = line.split(',')
		# print "parsing line...", words[0],"EOL"

		lat = float(words[0].strip()[2:])
		lon = float(words[1].strip()[0:-1])

		recno = latlon2countycode(lat,lon)
		if recno > 0:
			county_code = records[recno][5]
			county_name = records[recno][7]

			# Set default (1) otherwise increment count
			# 	
			county_sum[county_code] = county_sum.get(county_code, 0) + 1
			# try:
			# 	county_sum[county_code] += 1
			# except KeyError:
			# 	county_sum[county_code] = 1

			# print recno, county_code, county_name
		else:
			# print "Error with recno"
			continue
	except:
		continue

#
# Scale the county data by maximum value.
#
# Need to find 2010 Census population by FIPS county dataset
#


max_sum = max(county_sum.values())
print "id\trate"             # d3.tsv wants a header line by default
for key,value in county_sum.items():
	print "%s\t%0.5f" % (key,  abs(log(float(value)/max_sum))/70.0 )

# if __name__ == '__main__':
#     main()

