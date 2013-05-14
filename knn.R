# load required libraries for this tutorial
library(class)
library(ggplot2)

## PREPROCESSING
data <- iris                # create copy of iris dataframe
labels <- data$Species      # store labels
data$Species <- NULL        # remove labels from feature set (note: could

## TRAIN/TEST SPLIT
# initialize random seed for consistency
# this allows our data to look the same every single time the experiment is run
set.seed(1234) 

# we want to use 70% of our data as a training set
N <- nrow(data)
train.pct <- .7

train.index <- sample(1:N, train.pct * N)       # random sample of records (training set)
train.data <- data[train.index, ]       # perform train/test split
test.data <- data[-train.index, ]       # note use of neg index...different than Python!

train.labels <- as.factor(as.matrix(labels)[train.index, ])     # extract training set labels
test.labels <- as.factor(as.matrix(labels)[-train.index, ])     # extract test set labels

## Apply the Model
# initialize results object
err.rates <- data.frame()

max.k <- 100


knn.nfold <- function(n, train.data ) {
  # create n-fold partition of dataset
  # perform knn classification n times
  # n-fold generalization error = average over all iterations
  
  # Take the training data and partition into N-folds
  # 
  for (i in 1:n) {
    train_kfold_index = sample(train.index, round(nrow(train.data)/n) )
    #
    # Perform knn classification
    #
    for (k in 1:max.k) {
      knn_errors <- get_knn(k,train.data,train_kfold_index) #
      print k, knn_errors
    }
  }
}

#
# perform fit for various values of k
#    returns error rate
#
get_knn <- function(kiter,train.data, train_kfold_index)
  knn.fit <- knn(
    train = train.data,         # training set
    test = test.data,           # test set
    cl = train.labels,          # true labels
    k = kiter                   # number of NN to poll
  )

  # print params and confusion matrix for each value k
  cat('\n', 'k = ', k, ', train.pct = ', train.pct, '\n', sep='')
  print(table(test.labels, knn.fit))

  # Return  generalation error 
  return sum(test.labels != knn.fit) / length(test.labels)
}

## OUTPUT RESULTS
results <- data.frame(1:max.k, err.rates)   # create results summary data frame
names(results) <- c('k', 'err.rate')        # label columns of results df

# create title for results plot
title <- paste('knn results (train.pct = ', train.pct, ')', sep='')

# create results plot
results.plot <- ggplot(results, aes(x=k, y=err.rate)) + geom_point() + geom_line()
results.plot <- results.plot + ggtitle(title)

# draw results plot
results.plot

## NOTES
# Which range of k provided the lowest error results?
# If you change the random seed variable, do our stats change? 
# Why is it important to set the same seed on all data?

# what happens for high values (eg 100) of max.k? have a look at this plot:
# > results.plot <- ggplot(results, aes(x=k, y=err.rate)) + geom_smooth()

# our implementation here is pretty naive, meant to illustrate concepts rather
# than to be maximally efficient...see alt impl in DMwR package (with feature
# scaling):
#
# > install.packages('DMwR')
# > library(DMwR)
# > knn

# R docs
# http://cran.r-project.org/web/packages/class/class.pdf
# http://cran.r-project.org/web/packages/DMwR/DMwR.pdf
