#!/usr/bin/env python
#
# Read the model predictions from Vowpal Wabbit and generate probabilities
# 
# Writes two files:
#   1) vw.probabilities: record_id, probability_of_insult_is_true
#   2) diff.probabilities: vw_probability, logistic_probability, original comment text
#

import pandas as pd
import scipy as sp
import numpy as np

train    = pd.read_csv("Data/train.csv")
test     = pd.read_csv('Data/test.csv')
labels   = pd.read_csv("Data/test.predictions.C",header=None,names=["values"])
logistic = pd.read_csv("Data/logistic.probabilities")

#
#  For logistic regression, VW returns (alpha + beta)
#     Pr(True)  = Pi(x) = exp(a + bx) / (1 + exp(a +bx))
#     Pr(False) = 1 - Pi(x) = 1 - ( exp(a + bx) / (1 + exp(a +bx)) )
#
compare = pd.DataFrame({'1id': test['id'],
						'2vw': sp.exp(labels['values']) / ( 1 + sp.exp(labels['values'])),
						'3logistic': logistic['prob_true'],
						'4comment': test['Comment']
						})

insults    = labels[labels['values'] > 0.0]['values'].count()

print "VW predictions > 0:", labels[labels['values'] > 0.0]['values'].count()
print "VW predictions < 0:", labels[labels['values'] < 0.0]['values'].count()
print "VW insult percentage", insults *1.0/ len(labels)

print "Baseline percentage from train is ", 1.0*train[train['Insult'] == 1]['Insult'].count() /len(train['Insult'])	
print "Baseline percentage from logistic regression (sklearn) is ", 1.0*logistic[logistic['prob_true'] > 0.5]['prob_true'].count() /len(logistic['prob_true'])	

#
# Write out VW probabilities
#
vw = sp.exp(labels['values']) / ( 1 + sp.exp(labels['values']))



fo = open("Data/vw.probabilities", "w")
compare.to_csv(fo,cols=['1id','2vw'],index=False)  # seems to be a bug here in pandas
fo.close()

#
# Write out records with "high" difference between VW and Logistic
#
diff1 = compare[compare['2vw'] - compare['3logistic'] > 0.3]
diff2 = compare[compare['3logistic'] - compare['2vw'] > 0.3]

fo = open("Data/diff.probabilities", "w")
diff1.to_csv(fo,index=False,float_format="%f", cols=['1id','2vw','3logistic','4comment'])
fo.write("-------------------------------------------------------------------\n")
diff2.to_csv(fo,index=False,float_format="%f", cols=['1id','2vw','3logistic','4comment'])

fo.close()

