
import shapely
import shapefile
import sys
from rtree import index

#
# Given latitude/longitude, return the FIPS county code
#
def latlon2countycode(lat,lon):
	try:
		hits = list(idx.intersection((lon,lat,lon,lat)))
		recno = hits[0]
		# print lat,lon, recno, records[recno][5],  records[recno][7]
		# Do more testing here in case there are multiple matches
	except:
		pass
	return recno

print "reading shapefiles and making rtree index"
sf=shapefile.Reader("../Data/shapefiles/uscounties/all_counties.shp")

shapes  = sf.shapes()    # to get the polygons in the shapefiles
records = sf.records()   # to get the data, particulary county name and FIPS code

# Create rtree index and load the bounding boxes from the shapefiles
#
idx = index.Index()
for i, shape in enumerate(shapes):
    idx.insert(i, shape.bbox)

print "Starting to parse input"
# Initialize county aggregator
county_sum = {}

for line in sys.stdin:
	words = line.split(',')
	# print "parsing line...", words[0],"EOL"
	
	try:
		lat = float(words[0].strip()[2:])
		lon = float(words[1].strip()[0:-1])

		recno = latlon2countycode(lat,lon)
		county_code = records[recno][5]
		county_name = records[recno][7]
		# Set default (1) otherwise increment count

		county_sum[county_code] = county_sum.get(county_code, 0) + 1

	except:
		continue


for key,value in county_sum.items():
	print key, value

# if __name__ == '__main__':
#     main()

