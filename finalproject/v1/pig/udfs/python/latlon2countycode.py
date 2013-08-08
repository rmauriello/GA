import sys
# import shapely

# import shapefile
# from shapely.geometry import Point, Polygon
# from rtree import index
#
# Given latitude/longitude, return the FIPS county code
#  Some rtree intersection logic from https://gist.github.com/fawcett/5251327
#

# sf      = shapefile.Reader("/Volumes/DATA/robert/Desktop/Projects/GA/finalproject/Data/shapefiles/uscounties/all_counties.shp")
# shapes  = sf.shapes()    # Get the polygons in the shapefiles
# records = sf.records()   # Get the data, particulary county name and FIPS code


@outputSchema('latlon2countycode:int')
def latlon2countycode(lat,lon):

	return round(lat + lon)


# def latlon2countycode(lat,lon):
# 	hits = []
# 	try:
# 		# Return a list of all counties that match lon OR lat
# 		hits = list(idx.intersection((lon,lat,lon,lat)))
# 		if len(hits) == 1:                  # Exact match
# 			recno = hits[0]
# 		elif len(hits) > 1:                 # Multiple candidate counties
#         #	
# 		# For example, 42.66326054 -87.80922716 [3180, 3193] - either kenosha or racine county. 
# 			for hitIdx in hits:             # Search all counties in list
# 				county = shapes[hitIdx]     
# 				poly   = Polygon(county.points)
# 				if poly.contains(Point(lon,lat)):
# 					recno = hitIdx
# 					break
# 				else:                       
# 					continue				
# 		else:
# 			# if DEBUG:
# 			# 	sys.stderr.write("Error: Latlon2countycode unexpected error. -1\n")
# 			recno = -1
# 	except:
# 		# Lat/Lon don't match US county shapefiles
# 		recno = 0
# 	return recno
