Insult Prediction Project
  
  Based off a Kaggle competition, given a training set of labels (1 = Insult, 0 = not Insult) then predict labels for the test set.
  
  The sklearn script, insults_sklearn.py will use sklearn Naive Bayes or Logistic Regression and calculate AUC. 
  
  
  The Vowpal Wabbit (VW) scripts, vwprep.py and vwpost.py will prepare datasets for VW and then compare probabilities against the
  sklearn probabilities.
  
  
