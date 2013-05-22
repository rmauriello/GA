#
# Use knn and bayes inference to write a good model that classifies each row according to 
#   good or bad credit risk.
#
setwd("/Volumes/DATA/robert/Desktop/Projects/GA")
credit <- read.csv("homework_1.txt",sep=" ")


names(credit)=c("status", "duration", "credit_history", "purpose", "credit_amt", "savings",
                "employment", "installment_rate", "personal", "others", "residence", "property",
                "age", "other_plans", "housing", "num_credits", "job", "num_people", "telephone", 
                "foreign", "i1", "i2", "i3", "i4", "y")



# Cluster using Knn

