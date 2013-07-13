#!/usr/bin/env python 
# 
# Insult Predictions: 
#   Given a training dataset of text (unicode) with labels (1=insult, 0=not insult),
#   predict labels in the test dataset
#  
# Best score: 0.836
# Best parameters set:
#   lr__penalty: 'l1'
#   tfidf__norm: None
#   tfidf__use_idf: True
#   vect__binary: True
#   vect__max_df: 0.75
#   vect__ngram_range: (1, 3)
#   vect__stop_words: None
#   vect__strip_accents: None
  
# Best score: 0.833
# Best parameters set:
#   lr__penalty: 'l1'
#   tfidf__norm: None
#   tfidf__use_idf: True
#   vect__max_df: 0.75
#   vect__ngram_range: (1, 5)
  

# Best score: 0.825
#   lr__penalty: 'l1'
#   tfidf__use_idf: True
#   vect__max_df: 0.5
#   vect__ngram_range: (1, 1)

#   0.819:  nb__alpha: 1.0
#     vect__max_df: 0.5
#     vect__ngram_range: (1, 1)

# Best score: 0.819
# Best parameters set:
#   nb__alpha: 1.0
#   tfidf__norm: None
#   tfidf__use_idf: False
#   vect__max_df: 0.5
#   vect__ngram_range: (1, 1)

# Best score: 0.819
# Best parameters set:
#   sgdc__alpha: 1e-05
#   sgdc__penalty: 'elasticnet'
#   tfidf__norm: 'l2'
#   tfidf__use_idf: False
#   vect__max_df: 0.5
#   vect__ngram_range: (1, 5)

# Best score: 0.812
# Best parameters set:
#   sgdc__alpha: 1e-05
#   sgdc__penalty: 'elasticnet'
#   tfidf__norm: 'l1'
#   tfidf__use_idf: True
#   vect__max_df: 0.75
#   vect__ngram_range: (1, 5)


# Best score: 0.799
#   nb__alpha: 0.0
#   tfidf__use_idf: False
#   vect__max_df: 0.5
#   vect__ngram_range: (1, 1)


import pandas as pd
import numpy as np
import scipy as sp
import sklearn

from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes  import MultinomialNB
from sklearn.svm import SVC

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier


from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline

from pprint import pprint
from time import time
import logging

#
# Take a line of text and clean it up: 
#    Doesn't seem to do much for accuracy, 0.01?
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



if __name__ == "__main__":

    # Create the training & test sets
    data   = pd.read_csv('Data/train.csv')          # Insult, Date, Comment 
    target = data.Insult                            # y_train
    test = pd.read_csv('Data/test.csv')             # id, Date, Comment

    # Use pre_process() on each element of the vector, data['Comment']
    # data['Comment'] = data['Comment'].apply(pre_process)            

    # Set up pipeline of two vectors and two predictors
    pipeline = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('lr', LogisticRegression()),
        # ('svm', SVC()),
        # ('sgdc', SGDClassifier()),
        # ('nb', MultinomialNB() ),
        # ('rfc', RandomForestClassifier())
    ])

    v = CountVectorizer(stop_words='english', 
                        ngram_range=(1, 5), 
                        max_df=0.75,
                        binary=False,
                        strip_accents="unicode")  
    parameters = {
        'vect__max_df': (0.5, 0.75, 1.0),
        'vect__ngram_range': ((1, 1), (1, 3)),  # unigrams or bigrams
        'vect__stop_words': ("english", None),  # unigrams or bigrams
        'vect__binary': (True,False),
        'vect__strip_accents': ('ascii','unicode',None),
        'tfidf__use_idf': (True, False), 
        'tfidf__norm': ('l1', 'l2', None),  
        'lr__penalty': ("l1", "l2"),
        # 'svm_': (100, 200, 500), 
        # 'sgdc__alpha': (0.00001, 0.000001),
        # 'sgdc__penalty': ('l2', 'elasticnet'),
        # 'nb__alpha': (0.0, 1.0),
        # 'rfc__n_estimators': (10, 50, 100),
        # 'rfc__max_features': ('auto','sqrt', 'log2', None),

    }
    # find the best parameters for both the feature extraction and the
    # classifier
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)

    print "Performing grid search..."
    print "pipeline:", [name for name, _ in pipeline.steps]
    print "parameters:"
    pprint(parameters)
    t0 = time()


    grid_search.fit(data['Comment'], target)
    print "done in %0.3fs" % (time() - t0)
    print

    print "Best score: %0.3f" % grid_search.best_score_
    print "Best parameters set:"
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print "\t%s: %r" % (param_name, best_parameters[param_name])

    exit(0)