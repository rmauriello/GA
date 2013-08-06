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
		pop_county    = pd.read_csv("../Data/fipscounties.csv",sep=",",header=0)
		tweets_county = pd.read_csv("../Data/tweet_counts.tsv",sep="\t",header=0,names=['code','value'])
	except:
		print "Could not open file. Exiting"
		exit(-1)


	# Compare Actual vs. Expected tweets

	j = pd.merge(tweets_county,pop_county, on='code')
	# j['random'] = map(int, np.random.rand(1,len(j))[0] * 100)

	us_pop      = j['pop'].sum()
	tweet_tot   = j['value'].sum() 
	county_perc = j['pop']/float(us_pop)
	# tweet_perc  = j['random']/float(tweet_tot)
	tweet_perc  = j['value']/float(tweet_tot)


	# This is what we want.
	j['LQ'] = (tweet_perc/county_perc)


	j['LQN'] = np.log(j[j['LQ'] > 0]['LQ'])

	# Let's scale to [0,1]
	min = j['LQN'].min()
	max = j['LQN'].max()

	scale_factor = 1.0/(max - min)
	j['scaled'] = (j['LQN'] - min) * scale_factor

	d = j[j['LQ'] > 0][['code','scaled']]

	fo = open("twitterN.tsv","w")
	d.to_csv(fo, cols=['code','scaled'], index=None,sep="\t",float_format="%0.5f")
	fo.close()
	

if __name__ == '__main__':
    main()
