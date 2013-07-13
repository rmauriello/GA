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
data$Species <- NULL        # remove labels from feature set 

N <- nrow(data)             # size of data
train.pct <- .7             # Use 70% of our data as a training set

set.seed(1234)              # initialize random seed for consistency
max.k <- 100                 # 


# !!! Fix code !!!
#    as the cbind/rowbind appear to make them into single member lists with 1 DF
#    e.g. 
# > nrow(kfold.summary[1])
#     NULL
#  > nrow(kfold.summary[[1]])
#  [1] 4
kfold.summary <- data.frame()   # for overall evaluation  
kfold.detail  <- data.frame()   # for plotting of Knn

# --------------------------------------------------------------------------------------------------------
# Multiple plot function - copied as is from R Graphics Cookbook
#
# ggplot objects can be passed in ..., or to plotlist (as a list of ggplot objects)
# - cols:   Number of columns in layout
# - layout: A matrix specifying the layout. If present, 'cols' is ignored.
#
# If the layout is something like matrix(c(1,2,3,3), nrow=2, byrow=TRUE),
# then plot 1 will go in the upper left, 2 will go in the upper right, and
# 3 will go all the way across the bottom.
#
# --------------------------------------------------------------------------------------------------------

multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  require(grid)

  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)

  numPlots <- length(plots)

  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                    ncol = cols, nrow = ceiling(numPlots/cols))
  }

 if (numPlots == 1) {
    print(plots[[1]])

  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))

    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))

      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}

# --------------------------------------------------------------------------------------------------------
# Calculate some error statistics - average over all iterations
#   - err.rates = 1:max.k list of error rates by iteration k
#   - returns a list (mean, variance)
# --------------------------------------------------------------------------------------------------------
knn.error <- function(max.k, err.rates) {
  ## OUTPUT RESULTS
  v = var(err.rates)
  m = colMeans(err.rates)

  return(list(m, v))
}

# --------------------------------------------------------------------------------------------------------
# Return ggplot object
#
# --------------------------------------------------------------------------------------------------------
gen_plot <- function(df) {
  title <- paste('knn results (train.pct = ', train.pct, ')', sep='')
  gg <- ggplot(df, aes(x=colnames(df))) + geom_point() + geom_line() + ggtitle(title)

  return(gg)
}

# --------------------------------------------------------------------------------------------------------
#   Partition data into n-folds & run Knn classification
#     - returns 
# --------------------------------------------------------------------------------------------------------
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
    for (kiter in 1:max.k) {
      # Apply the Model
      knn.fit <- knn(train = train.data,         # training set
                    test = test.data,            # test set
                    cl = train.labels,           # true labels
                    k = kiter)                   # number of NN to poll
      
      # Return generalization error for iteration k and add to errr.rates dataframe
      this.error <- sum(test.labels != knn.fit) / length(test.labels)    
      err.rates <- rbind(err.rates, this.error)                
      
      # print params and confusion matrix for each value k
#      cat('\n', 'k = ', kiter, ', train.pct = ', train.pct, '\n', sep='')
#      print(table(test.labels, knn.fit))
    }

  #Store detailed error (max.k by n columns) 
  kfold.detail <- cbind(kfold.detail, err.rates)   
    
  # Calculate error for fold n
  names(err.rates) = 'err.rate'
  this.stats = knn.error(max.k, err.rates)
  kfold.summary <- rbind(kfold.summary, this.stats)
    
  }
  rownames(kfold.summary) = paste("fold", 1:n,sep="")
  names(kfold.summary) = c('mean', 'variance')
  print(kfold.summary)
  
  rownames(kfold.detail) <- 1:max.k
  names(kfold.detail) <- paste("fold",1:n,sep="")
  print(head(kfold.detail))
  
#  gg <- vector()
#  for (i in 1:n) {
#    title <- paste('knn results (train.pct = ', train.pct, ')', sep='')
#    gg[i] <- ggplot(kfold.detail, aes(x=kfold.detail[i])) + geom_point() + geom_line() + ggtitle(title)
#  }
  
  ggplot(kfold.detail[[1]], aes(x=rownames(kfold.detail[[1]]), y=kfold.detail[[1]]['fold1'])) + geom_point() + geom_line()
#  multiplot(gg[1], gg[2], gg[3], gg[4], cols=2)

  return(vector[kfold.summary, kfold.detail])
}



# ========================================================================================================
# Main Function
#
# ========================================================================================================

n = 4
kfold.summary  <- data.frame(row.names=1:n)
kfold.detail   <- data.frame(row.names=1:max.k)

k <- knn.nfold(n,data)
kfold.summary <- k[1]
kfold.detail  <- k[2]


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
