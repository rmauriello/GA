#!/usr/bin/env python 
# 
# Insult Predictions: 
#   Given a training dataset of text (unicode) with labels (1=insult, 0=not insult),
#   predict labels in the test dataset
#   
#  Perhaps ngrams would help, e.g. "fuck up", "fuck you"
#
#  How many non-English text is present?
#

import pandas as pd
import numpy as np
import scipy as sp
import sklearn

from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import auc_score  

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer

#
# Take a line of text and clean it up
#
def pre_process(text):
  
  text = text.replace("'", "")              # Remove apostrophes (inside words, etc.)
  text = text.replace("[\"\'\`]", "")       # Remove double and single quotes

  text = text.replace(r"\W+", " ")          # Replace at least 1 nonalphanumeric characters with space
  text = text.replace("[-_]+","")           # Delete - or _ 
  text = text.lower()                       # Convert all to lowercase
  text = text.decode('unicode-escape')

  text = text.split()
  words = []
  for word in text:                         # Remove duplicate words, e.g. the the
    if word in words:
      continue
    words.append(word)
  words = " ".join(words)                   # Convert list back into string
  return words


def main():
    # Create the training & test sets
    data   = pd.read_csv('Data/train.csv')          # Insult, Date, Comment 
    target = data.Insult                            # y_train
    test = pd.read_csv('Data/test.csv')             # id, Date, Comment

    # Use pre_process() on each element of the vector, data['Comment']
    data['Comment'] = data['Comment'].apply(pre_process)            

    # Pick a tokenizer
    #    Remove stop words, 
    #    Make n-grams of one to five words- doesn't appear to make any difference
    #    Binary = False? - TDM counts occurrence not frequency of word in document

      # v = CountVectorizer(stop_words='english', 
      #                     ngram_range=(1, 5), 
      #                     binary=False,
      #                     strip_accents="unicode")    # preprocessing strips the text
    v = TfidfVectorizer(stop_words='english', 
                        ngram_range=(1, 5))
    # v = HashingVectorizer()
    X_train = v.fit_transform(data['Comment'])      # Learn the vocabulary dictionary and 
                                                    # return the count vectors.
    X_test  = v.transform(test.Comment)             # Extract token counts out of raw text documents using 
                                                    # the vocabulary fitted with fit or the one provided 
                                                    # in the constructor

    # Use a model  
    clf = LogisticRegression().fit(X_train, list(target))
    clf.score(X_train, target)

    # Use 10-fold cross validation with different splits (random?)
    scores = cross_val_score(clf, X_train, target, score_func=auc_score, cv=10)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() / 2))
    probs = clf.predict_proba(X_test)[:,1]

    insults    = probs[probs[:] > 0.5].sum()
    print "insult percentage", insults / len(probs)


    # Print the probabilities
    output = pd.DataFrame( {'id': test['id'], 'probs_true': pd.Series(probs) } )
    fo = open("Data/logistic.probabilities", "w")
    output.to_csv(fo,cols=['id','prob_true'],index=False,float_format="%f")
    fo.close()


if __name__ == "__main__":
    main()