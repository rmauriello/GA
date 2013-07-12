#!/usr/bin/env python
#
# Usage:
#   vwprep.py [-p] inputfile outputfile
#
# Read CSV training file and write out Vowpal Wabbit (VW) file
#   Training file has label, date, feature1, feature2, ...
#      e.g. Insult,Date,Comment
#           1,20120618192155Z,"""You fuck your dad."""
#   Test file has label, date, feature1, feature2, ...
#      e.g. id, Date, Comment
#         11,20120531222107Z, @CrankyVince has found our slice of the Internets!  FUCK YOU.
#
#   VW file has [Label] [Importance [Tag]]|Namespace Features |Namespace Features 
#       e.g. <Insult> | This is comment 1, no feature building needed
#         0 |c i really don't understand your point.\xa0 It seems that you are mixing apples and oranges.
#         0 |c Yeah and where are you now?
#
# Use VW to create model using train.vw
#    vw -c -d train.pos.vw --loss_function logistic -f model.pos --l1 0.0001

# Use VW to create predictions using model above (-t says not to use labels)
#    vw -c -k -t test.pos.vw -i model.pos -p test.predictions.POS
# 
#    
import csv, re, os,sys
import decode
import argparse

import nltk
import nltk.tag
from nltk import tokenize, word_tokenize, pos_tag
from nltk.corpus import stopwords
#
# Take a line of text and clean it up
#
def tokenize(text):
  dict_out ={}
  
  text = text.replace("'", "")        # Remove apostrophes (inside words, etc.)
  text = text.replace("\"", "")       # Remove quote (inside words, etc.)
  
  text = re.sub(r"\W+", " ", text)    # Replace at least 1 nonalphanumeric characters with space
  text = text.replace("[-_,.:|]","") # Delete - or _ 

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
  return words

#
# Take a line of text and create dictionary of part of speech (POS) to list of words
#   - how much cleanup does the NLTK tokenizer do?
#
# Using default tag (Penn Treebank):  http://www.monlp.com/2011/11/08/part-of-speech-tags/
# 
def tokenize_pos(sentence):
  stopwords = nltk.corpus.stopwords.words('english')

  sentence = sentence.replace("'", "")        # Remove apostrophes (inside words, etc.)
  sentence = sentence.replace("\"", "")       # Remove quote (inside words, etc.)
  sentence = sentence.replace(":", "")       # Remove quote (inside words, etc.)
  sentence = sentence.replace("[-_,.;:|]","") # Delete - or _ 
  sentence = sentence.lower()
  sentence = nltk.clean_html(sentence)        # Remove HTML tags

  words = word_tokenize(sentence)             # Use the NLTK tokenizer 
                                              
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

  try:
    writer = open(args.files[1], "w")
  except:
    print "Error: could not write to file", args.files[1]

  # stopwords = nltk.corpus.stopwords.words('english')
  POS_TAGS = ['CC','CD', 'DT','EX','FW','IN', 'JJ','JJR', 'LS', 'MD', 
  'NN','NNS', 'NNP','NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB','RBR', 'RBS', 'RP', 'TO', 
  'UH', 'VB', 'VBG', 'VBN','VBP', 'VBZ', 'WDT','WP', 'WP$', 'WRB']

  # First column (label) for each input line should be either 0 or 1 (train) or row number (test) 
  for line in reader:
    if line[0] < 0:             # Labels in test and train should be at least 0
      next
    else:        
      label = line[0]
      if label == "0":
        label =   "-1"

      lineout = label           # Initialize lineout to be the label
      if NAMESPACE == "C":      # No parts of speech
        tokens = tokenize(line[2])
        lineout = lineout + " |C " + (''.join( str(x) for x in tokens))

      elif NAMESPACE == "POS":  # Use each part of speech as a namespace for VW
        tokens = tokenize_pos(line[2])
        for key in tokens:
          if key not in POS_TAGS:
            next
          else:
            lineout = lineout + " |" + key  + " " + (''.join( str(x) for x in tokens[key])) + " "
      else:
        print "ERROR - only two namespace options defined"
        exit
      writer.write(lineout + "\n")
  writer.close()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', action='store_true')
  parser.add_argument('files', nargs='*')  
  args = parser.parse_args()

  if args.p:
    NAMESPACE = "POS"
  else:
    NAMESPACE = "C"
   
  main()