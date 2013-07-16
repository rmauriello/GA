#
# Parse this file into a collection of product ids (ASIN) and customer.
#
# Returns:
#    products[productId] = [title, [customerId1, customerId2, CustomerId3...]]
#
# Id:   1
# ASIN: 0827229534
#   title: Patterns of Preaching: A Sermon Sampler
#   group: Book
#   salesrank: 396585
#   similar: 5  0804215715  156101074X  0687023955  0687074231  082721619X
#   categories: 2
#    |Books[283155]|Subjects[1000]|Religion & Spirituality[22]|Christianity[12290]|Clergy[12360]|Preaching[12368]
#    |Books[283155]|Subjects[1000]|Religion & Spirituality[22]|Christianity[12290]|Clergy[12360]|Sermons[12370]
#   reviews: total: 2  downloaded: 2  avg rating: 5
#     2000-7-28  cutomer: A2JW67OY8U6HHK  rating: 5  votes:  10  helpful:   9
#     2003-12-14  cutomer: A2VE83MZF98ITY  rating: 5  votes:   6  helpful:   5

import re

from nltk import clean_html

f = open('Data/amazon-meta.txt.small.txt')
f.readline() # skip header line

recordcount = 0
products = {}
record = {}
customer_list = []

for line in f:
	if line.strip() != "":
		# Parse the lines and stuff into the current record dictionary	
		# Handle all the cases here (:, |, other)	
		
		words = line.split(":")

		if len(words) < 2:
			# only key found - could do other parsing for |, etc. "
			continue
		else:	
			# Create key, values for each record blocks
			key      = words[0].strip()	

			if key == "ASIN":
				key = "productId"
			elif re.search(".*cus*tomer$", key):             # Could do better job here
				key   = "customer"
				value = words[1].strip().split()[0].strip()  # customerId
				customer_list.append(value)

			# Finally store appropriate key,values 			
			value    = ":".join(words[1:]).strip()
			if key == "customer":
				record['customer'] = customer_list
			else:			
				record[key] = value

	else:  
		# Otherwise done with record block. 
		# Store only certain fields in "record" into product dictionary
		# Regardless, reinitialize the record and customer list
		recordcount += 1	
		if "productId" in record.keys() and "title" in record.keys():
			productId       = record['productId']
			title           = record['title']

			if "customer" in record.keys():
				customers = " ".join(record['customer'])
			else:
				customers = ""

			product_info  = title + ":" + customers
			products.setdefault(productId, []).append(product_info)
		else:
			# Did not find productId and title in this record.. Skipping to next block"
			continue

		record = {}
		customer_list = []

f.close()

# For a given productId, return title and associate customers
#    products[productId] = [title, [customer1, customer2]]
#
print "number of products", len(products)
for key, value in products.items():
	print key, products[key]