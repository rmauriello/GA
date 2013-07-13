Insult Prediction Project
  
  Based off a Kaggle competition, given a training set of labels (1 = Insult, 0 = not Insult) then predict labels for the test set.
  
  The sklearn script, insults_sklearn.py will use sklearn Naive Bayes or Logistic Regression and calculate AUC. 

  insult_search_parms.py uses grid_search() to find optimal parameters:
	Classifiers used included logistic regression, naive Bayes, and stochastic gradient descent.
	Tried using random forest classifier but it didn't work with GridSearchCV.
        The best one appears to be logistic regression

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
  
  
  The Vowpal Wabbit (VW) scripts, vwprep.py and vwpost.py will prepare datasets for VW and then compare probabilities against the
  sklearn probabilities.
  
  
