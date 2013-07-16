#
# Parse this file into a collection of product ids (ASIN) and customer.
#
# Returns
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

products = {}
record = {}
customer_list = []

recordID = 0
for line in f:
	if line.strip() != "":
		# Parse the lines and stuff into the current record dictionary	
		# Handle all the cases here (:, |, other)	
		words = line.split(":")

		# Most keys and values don't require modification except ASIN and customer
		key      = words[0].strip()
		value    = " ".join(words[1:]).strip()
		print "key + value: ", key, value
		# value = clean_html(value)
	
		if key == "ASIN":
			key = "productId"
		elif re.search(".*cus*tomer", key):
			key   = "customer"
			value = words[1].strip().split()[0]
			customer_list.append(value)

		# Finally store all the values 
		# Could only store certain values with additional logic
		if key == "customer":
			record.setdefault(key, []).append(customer_list)
		else:			
			record.setdefault(key, []).append(value)

	else:   
		# Otherwise done with record block. Store record into product dictionary
		productId       = record['productId']
		title           = record['title']
		customer_list   = record['customer'] 

		products.setdefault(productId, []).append(title)
		record = {}
		customer_list = []


# For a given productId, return title and associate customers
#    products[productId] = [title, [customer1, customer2]]
#
print "number of products", len(products)
for key, value in products.items():
	print key, reviews[key]