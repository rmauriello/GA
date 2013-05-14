#
# create n-fold partition of dataset
# perform knn classification n times
# n-fold generalization error = average over all iterations
# 
# load required libraries for this tutorial
library(class)
library(ggplot2)

## PREPROCESSING
data <- iris                # create copy of iris dataframe
labels <- data$Species      # store labels
data$Species <- NULL        # remove labels from feature set (note: could

N <- nrow(data)             # 
train.pct <- .7             # Use 70% of our data as a training set

set.seed(1234)              # initialize random seed for consistency
kfold.plots = data.frame()   
kfold.errors = data.frame()

max.k <- 100                # 

#
# Calculate some error statistics - average over all iterations
#
knn.error <- function(max.k, err.rates) {
  ## OUTPUT RESULTS
  
}

# Return ggplot object
#
gen_plot <- function(results) {

  # create title for results plot
  title <- paste('knn results (train.pct = ', train.pct, ')', sep='')

# create results plot
  results.plot <- ggplot(results, aes(x=k, y=err.rate)) + geom_point() + geom_line()
  results.plot <- results.plot + ggtitle(title)

# draw results plot
  results.plot
}

# ========================================================================================================
# Partition data into n-folds & run Knn classification
#
# ========================================================================================================

knn.nfold <- function(n, data ) {  
  for (f in 1:n) {  
    #
    # Split the data into training (train.pct %) and test (1 - train.pct %) data
    #
    train.index <- sample(1:N, train.pct * N)       # random sample of records (training set)
    train.data <- data[train.index, ]       # perform train/test split
    test.data <- data[-train.index, ]       # note use of neg index...different than Python!
    
    train.labels <- as.factor(as.matrix(labels)[train.index, ])     # extract training set labels
    test.labels <- as.factor(as.matrix(labels)[-train.index, ])     # extract test set labels
    err.rates <- data.frame()                                       # initialize results object

    #
    # Perform fit for various values of k
    #
    for (k in 1:max.k) {
      #   
      # Apply the Model
      knn.fit <- knn(train = train.data,         # training set
                    test = test.data,            # test set
                    cl = train.labels,           # true labels
                    k = kiter)                   # number of NN to poll
      
      # Return generalization error for iteration k and add to errr.rates dataframe
      this.error <- (sum(test.labels != knn.fit) / length(test.labels))    
      err.rates = rbind(err_rates,this.error)                
    
      # print params and confusion matrix for each value k
      cat('\n', 'k = ', k, ', train.pct = ', train.pct, '\n', sep='')
      print(table(test.labels, knn.fit))
    }

  # Calculate error dataframe  
  results <- data.frame(1:max.k, err.rates)   # create results summary data frame
  names(results) <- c('k', 'err.rate')        # label columns of results df

  # Calculate error for fold n
  knn.error(max.k, err.rates)    
  
  # Create a plot and store
  kfold.plots[f] = gen_plot(results) 
}




knn.nfold(4,data)


#multiplot(...)             # Plot up to N (4?) knn error plots



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
