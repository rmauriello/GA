#!/usr/bin/env python
#
# Labels need to be -1 and 1. No header row
#
# Usage:
#   vwprep.py [-p] inputfile outputfile
#
# Read CSV training file and write out Vowpal Wabbit (VW) file
#   Training file has label, date, feature1, feature2, ...
#      e.g. Insult,Date,Comment
#           1,20120618192155Z,"""You fuck your dad."""
#
#   VW file has [Label] [Importance [Tag]]|Namespace Features |Namespace Features ... |Namespace Features
#       e.g.   
#        <Insult> | This is comment 1, no feature building needed
#         0 |c i really don't understand your point.\xa0 It seems that you are mixing apples and oranges.
#         0 |c Yeah and where are you now?
#
#  Looks like the test.csv has a slightly different format
#       What's the file format for test.vw?

# Use VW to create model using train.vw
#    vw -c -d train.vw --loss_function logistic -f model --l2 0.0001

# Use VW to create predictions using model above
#    vw -c -k -t test.vw -i model -p test.predictions
# 
#   Output will have format of ? 
#    
import csv
import re
import os,sys
import decode
import argparse
import nltk
import nltk.tag
from nltk import tokenize
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
#
# Take a line of text and clean it up
#
def tokenize(text):
  dict_out ={}
  NAMESPACE = "C"
  
  text = text.replace("'", "")        # Remove apostrophes (inside words, etc.)
  text = text.replace("\"", "")       # Remove quote (inside words, etc.)
  
  text = re.sub(r"\W+", " ", text)    # Replace at least 1 nonalphanumeric characters with space
  text = re.sub("[-_]+","", text)     # Delete - or _ 
  text = text.lower()                 # Convert all to lowercase
  # text = text.decode('unicode-escape')

  text = text.split()
  words = []
  for word in text:                   # Remove duplicate words, e.g. the the
    if word in words:
      continue
    words.append(word)

  words = " ".join(words)             # Convert list back into string
  dict_out[NAMESPACE]  = words
  return dict_out

#
# Take a line of text and create dictionary of part of speech (POS) to list of words
#   - how much cleanup does the NLTK tokenizer do?
#
# Using default tag (Penn Treebank)
#   http://www.monlp.com/2011/11/08/part-of-speech-tags/
# 

def tokenize_pos(sentence):
  stopwords = nltk.corpus.stopwords.words('english')

  sentence = sentence.replace("'", "")        # Remove apostrophes (inside words, etc.)
  sentence = sentence.replace("\"", "")       # Remove quote (inside words, etc.)
  
  sentence = re.sub("[-_,.]+","", sentence)   # Delete - or _ 
  sentence = sentence.lower()
  sentence = nltk.clean_html(sentence)        # Remove HTML tags

  words = word_tokenize(sentence)             # Use the NLTK tokenizer 
                                              # Remove stopwords
  words    = [w for w in words if w.lower() not in stopwords]
  pos_list = pos_tag(words)                   # Use pos_tag() to map word to part of speech (POS)

  pos_dict = {}
  for i in range(len(pos_list)):      # Reverse mapping, POS to word
      key    = pos_list[i][1]
      value  = pos_list[i][0]
      pos_dict.setdefault(key, []).append(" " + value)  # Initialize key, otherwise append value
  return pos_dict

def main():
  try:
    reader = csv.reader(open(args.files[0]))
    next(reader)                                        # skip header row
  except:
    print "Error: could not read ", args.files[0]


  # stopwords = nltk.corpus.stopwords.words('english')
  POS_TAGS = ['CC','CD', 'DT','EX','FW','IN', 'JJ','JJR', 'LS', 'MD', 
  'NN','NNS', 'NNP','NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB','RBR', 'RBS', 'RP', 'TO', 
  'UH', 'VB', 'VBG', 'VBN','VBP', 'VBZ', 'WDT','WP', 'WP$', 'WRB']

  # First column (label) should be either 0 or 1 (train) 
  for line in reader:
    if line[0] < 0:
      next
    else:        
      label = line[0]
      if label == "0":
        label =   "-1"

      if NAMESPACE == "C":
        tokens = tokenize(line[2])
      elif NAMESPACE == "POS":
        tokens = tokenize_pos(line[2])
      else:
        print "ERROR - only two namespace options defined"
        exit

      # Initialize lineout to be the label
      lineout = label
      for key in tokens:
        if key not in POS_TAGS:
        # if key in [':', '.', "-NONE-", "\"",  "\'\'", "$"]:
          next
        else:
          lineout = lineout + " |" + key  + " " + (''.join( str(x) for x in tokens[key])) + " "
      print lineout


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', action='store_true')
  parser.add_argument('files', nargs='*')  
  args = parser.parse_args()

  if args.p:
    NAMESPACE = "POS"

  else:
    NAMESPACE = "C"

  if "train" in args.files[0]:
    OUTFMT = "train"
  else:
    OUTFMT = "test"
   
  main()