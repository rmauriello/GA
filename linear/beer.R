beer <- read.csv('http://www-958.ibm.com/software/analytics/manyeyes/datasets/af-er-beer-dataset/versions/1.txt', header=TRUE, sep='\t')
head(beer)

summary(beer$WR)
beer$good <- (beer$WR > 4.3)

beer$Ale <- grepl('Ale', beer$Type)
beer$IPA <- grepl('IPA', beer$Type)
beer$Stout <- grepl('Stout', beer$Type)
beer$Lager <- grepl('Lager', beer$Type)

head(beer)

model <- glm(good ~ Ale + Stout + IPA + Lager, data=beer, family='binomial')

train.idx <- sample(1:nrow(beer), .7*nrow(beer))
training <- beer[train.idx,]
test <- beer[-train.idx,]

model <- glm(good ~ Ale + Stout + IPA + Lager, data=training, family='binomial')
model <- naiveBayes(good ~ Ale + Stout + IPA, data=training)

install.packages('ROCR')
library('ROCR')


pred <- prediction(test.predict, test$good) 
perf <- performance(pred, measure='acc') #Simple accuracy, what % were right?

perf <- performance(pred, measure='prec') #What % of the elements I predicted to be in the class actually?
perf <- performance(pred, measure='recall') #What % of the elements that are in class, did I predict to be in this class?

perf <- performance(pred, measure='f') #F-measure a balance between them
perf <- performance(pred, measure='auc') #Area Under the Curve, another way to balance them
