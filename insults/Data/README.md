Input and Work Files
-----------------------
  - train.csv
  - test.csv
  
  - train.vw and test.vw - VW format inputs with one namespace, C
  - train.pos.vw and test.pos.vw - VW format inputs with multiple namespaces based on part of speech

  - diff.probabilities: shows the records that don't match between VW probabilities and sklearn. Threshold is coded to 0.3. In current pandas 0.11, there's a bug with to_csv() as the columns get printed alphabetically and it appears 'logistic' is really 'id'. First part of file is where VW gives a higher probability than LR whereas the second part VW gives a lower probability.  
 Take-away is that logistic regression is not too bad for this case.

Output Files (submission files)
-----------------------
  - vw.probabilities - Probability of Insult being true, columns = "id", "probability"
  - logistic.probabilities - 
  - naivebayes.probabilities -
