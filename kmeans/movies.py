#
# Parse this file into a collection of product ids (ASIN) and review text.
#
# Prints dictionary:
#   reviews['productID'] = [review1, review2, ...] 
#
# Input:
	# review/userId: A141HP4LYPWMSR
	# review/profileName: Brian E. Erland "Rainbow Sphinx"
	# review/helpfulness: 7/7
	# review/score: 3.0
	# review/time: 1182729600
	# review/summary: "There Is So Much Darkness Now ~ Come For The Miracle"
	# review/text: Synopsis: On the daily trek from Juarez, Mexico to El Paso,...

# Output
	# number of reviews 156
	# B00004CQT3 ["well,this just goes to show why you don't blindly accept a critics review....]
	# B00004CQT4 ['It is a funny movie, but I think there is way too much cursing, ...]

from nltk import clean_html

f = open('Data/movies.txt.small.txt')

reviews = {}
record = {}
recordID = 0
for line in f:

	if line.strip() != "":
		# Parse the lines and stuff into the dictionary
		rightline = line.split("/")[1]
		key   = rightline.split(":")[0].strip()
		value = " ".join(rightline.split(":")[1:]).strip()
		value = clean_html(value)

		record[key] = value
	else:   
		# Get values from record and store into movies dictionary
		
		productId = record['productId']
		text      = record['text']
		reviews.setdefault(productId, []).append(text)
		record = {}

print "number of reviews", len(reviews)
for key, value in reviews.items():
	print key, reviews[key]