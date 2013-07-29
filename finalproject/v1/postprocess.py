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

test     = pd.read_csv('Data/test.csv', sep = "|", header=None, names=["timestamp", "text", "userid"])
labels   = pd.read_csv("test.predictions",header=None,names=["values"])


test['timestamp'] = test['timestamp'].strip()
test['text']      = " ".join(test['text'].split()[1:])
test['userid']    = " ".join(test['userid'].split()[1:])

#
# Write out VW probabilities
#
vw = sp.exp(labels['values']) / ( 1 + sp.exp(labels['values']))


fo = open("Data/vw.probabilities", "w")
compare.to_csv(fo,cols=['1id','2vw'],index=False)  # seems to be a bug here in pandas
fo.close()


