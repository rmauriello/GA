#!/usr/bin/env python

#
# Input:
#   Twitter counts (insults, total) by county
#   Population by county (2010 census)
# Output:
#   scaled Location Quotient by FIPS county code
#

import pandas as pd
import numpy as np


def main():
	
	try:
		pop_county    = pd.read_csv("../Data/fipscounties.csv",sep = ",",header=0)
		tweets_county = pd.read_csv("../Data/tweet-parsed-14d/tw-counts-14d.tsv",sep ="\t",header=0,names=['code','value'])
	except:
		print "Could not open file. Exiting"
		exit(-1)


	# Compare Actual vs. Expected tweets

	j = pd.merge(tweets_county,pop_county, on='code')
	

	# Let's calculate tweet count, linearly scale to [0,1]
	# Should correlate to US population
	#

	j['tweets'] = j['value']/float(j.value.max())

	min = float(j['tweets'].min()) # 
	max = float(j['tweets'].max()) # s/b 1

	scale_factor = 1.0/(max - min)
	j['value'] = (j['tweets'] - min) * scale_factor

	d = j[:][['code','value']]

	fo = open("twitter.tsv","w")
	j.to_csv(fo, cols=['code','value'], index=None,sep="\t",float_format="%0.9f")
	fo.close()


	# Let's calculate population ratio and log scale to [0,1]
	# Should not necessarily correlate to US population
	#
	us_pop      = j['pop'].sum()
	tweet_tot   = j['value'].sum() 
	tweet_perc  = j['value']/float(tweet_tot)
	county_perc = j['pop']/float(us_pop)

	# Assume tweets correlate to population - calculate ratio
	#  - ratio > 1: 
	#          = 1:
	#          < 1: 

	j['LQ']     = (tweet_perc/county_perc)

	# Log transform
	j['LQN']    = np.log(j[j['LQ'] > 0]['LQ'])


	# Calculate scale factor
	min = j['LQN'].min()
	max = j['LQN'].max()
	scale_factor = 1.0/(max - min)
	j['scaled'] = (j['LQN'] - min) * scale_factor

	# Write to normalized file, ignoring the log(0) record
	d = j[j['LQ'] > 0][['code','scaled']]

	fo = open("twitterN.tsv","w")
	d.to_csv(fo, cols=['code','scaled'], index=None,sep="\t",float_format="%0.5f")
	fo.close()
	


if __name__ == '__main__':
    main()
