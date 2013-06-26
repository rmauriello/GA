#
#  Predict salary (Pounds) based on job descriptions from online postings
#  Simple model using 200K training set results in MAE of 13,010
#    Increasing training set made MAE bigger but this is probably overfitting with small sets
#
# Variables:
# Id, numeric counter
# Title - job description, often including location
# FullDescription - detailed job description
# LocationRaw - 
# LocationNormalized - city
# ContractType - full_time, part_time, NA (almost always full-time according to boxplots)
# ContractTime - permanent, contract, NULL (boxplots very different)
# Company - recruiting company or actual?
# Category - job category, e.g. engineering **
# SalaryRaw - salary, often as range (pounds)
# SalaryNormalized - salaray as actual number (pounds)
# SourceName - URL (of job posting?)

require('plyr')
require('DAAG')
require('ggplot2')
require('tm')

mae <- function(x,y) { 
  if (length(x) != length(y) ) {
    print("Vectors not equal. Exiting ...")
  }
  mean(abs((x - y)))
}

mse <- function(x , y) {
  if (length(x) != length(y) ) {
    print("Vectors not equal. Exiting ...")
  }
  mean( (x-y)^2 )
}

# --------------------------------------------------------------------------------------------------------
#   Partition data into folds & run a set of linear regression models with lm
#     Returns a list of k-fold average MAE for each model
# --------------------------------------------------------------------------------------------------------
model.nfold <- function(n, data, locations=NULL) {  
  #
  err.rates   <- data.frame()                     # initialize results object 
  for (k in 1:n) {
    #
    # Split the data into training (train.pct %) and test (1 - train.pct %) data
    #
    if (!missing(locations)) {
      top_20cities           <- sort(table(data$City),decreasing=TRUE)[1:20]
      
      locations$top20_flag   <- (locations$city1 %in% top_20cities)
      locations_short        <- locations[locations$top20_flag,]
      data                   <- merge(data,locations_short,by.x = "City", by.y="city1")
      data$city              <- as.numeric(as.factor(data$City))
      data$city2             <- as.numeric(as.factor(data$city2))
      print(head(locations$top20_flag))
    }
    
    train.index <- sample(1:N, train.pct * N)       # Create random sample of records (training set)
    train.data  <- data[train.index, ]              # Split into train/test
    test.data   <- data[-train.index, ]             # note use of neg index...different than Python!
    #
    # Perform fit for various values of k
    #
    lm1 <- lm(Salary ~ 1 , data=train.data) #   
    lm2 <- lm(Salary ~ city + category + ctime + ctype + company, data=train.data)     
    lm3 <- lm(Salary ~ title + city + category + ctime + ctype + company, data=train.data)     
    lm4 <- lm(Salary ~ title + city + category + ctime + ctype + company + city:category, 
                    data=train.data)
    lm5 <- lm(Salary ~ title + city + category + ctime + ctype + company + city:category + company:category, 
              data=train.data)
    lm6 <- lm(Salary ~ title + city + category + ctime + ctype + company + company:category, 
              data=train.data)
    
    list_of_models <- list(lm1,lm2,lm3,lm4,lm5,lm6)

    for (m in 1:6) {
      salary.lm <- list_of_models[[m]]
      if (!missing(locations)) {
          salary.lm <- lm(Salary ~ title + city + city2  + category + ctime + ctype + company, 
                      data=train.data) # 
      }

      # Calculate an error metric for this fold k and add to err.rates dataframe
      test.predict <- predict(salary.lm, test.data)
      this.error   <- mae(test.data$Salary, test.predict)
      err.rates    <- rbind(err.rates, cbind(m,this.error))      
    }    
  }
  return(err.rates)
}


# --------------------------------------------------------------------------------------------------------
#   Partition data into n-folds & run linear regression with lm 
#     - returns 
# --------------------------------------------------------------------------------------------------------

get_dtm <- function(data) {  
  src <- DataframeSource(data.frame(data$Title)) # Using just Title for simplicity
  c <- Corpus(src)
  c <- tm_map(c, stripWhitespace)
  c <- tm_map(c, tolower)
  c <- tm_map(c, removeWords, stopwords("english"))

  # Create a dtm where each "document" is the rowid
  dtm <- DocumentTermMatrix(c)
}

textmodel.nfold <- function(n, data, locations=NULL) {  

  # Create a dtm where each "document" is the rowid and look at the Title field
  dtm <- get_dtm(data)


  # Each of these words becomes a column containing a binary flag
  # This list came from a perusal of titles for each quantile
  data <- cbind(data, as.matrix(dtm[, job_titles]))

  err.rates   <- data.frame()                     # initialize results object 
  for (k in 1:n) {
    
    # Split the data into training (train.pct %) and test (1 - train.pct %) data
    train.index <- sample(1:N, train.pct * N)       # Create random sample of records (training set)
    train.data  <- data[train.index, ]              # Split into train/test
    test.data   <- data[-train.index, ]             # note use of neg index...different than Python!
  
    # Could use paste() and as.formula() here
    salary.lm <- lm(Salary ~ title + city + category + ctime + ctype + company + company:category +
                             teacher + chef + support + assistant+ administrator + operator + technician + 
                             analyst + consultant + engineer + engineering + trainee + care + manager + nurse + developer, 
                     data=train.data)    
    
    # Calculate an error metric for this fold k and add to err.rates dataframe
    test.predict <- predict(salary.lm, test.data)
    this.error   <- mae(test.data$Salary, test.predict)
    err.rates    <- rbind(err.rates, this.error)          
  }
  return(err.rates)
}


# --------------------------------------------------------------------------------------------------------
#   Partition data into n-folds & run linear regression with lm 
#     - returns 
# --------------------------------------------------------------------------------------------------------

setwd("/Volumes/DATA/robert/Desktop/Projects/GA/salary") 
train_all   <- read.csv('data/train.csv')
test        <- read.csv('data/test.csv')
loc_tree    <- read.csv('data/Location_Tree2.csv',header=FALSE,
                      col.names=c('uk','country','city1','city2','city3','city4','city5' ))

job_titles <- c('teacher','chef','support','assistant','administrator', 
                                     'operator','technician','analyst', 'consultant',  
                                     'engineer','engineering', 'trainee', 
                                     'care', 'manager','nurse','developer')


N <- nrow(train_all)             # size of data
train.pct <- .7             # Use 70% of our data as a training set

# Rename some columns to make life easier
train_all  <- rename(train_all,  c("LocationNormalized" = "City"))
train_all  <- rename(train_all,  c("SalaryNormalized" = "Salary"))
test <- rename(test, c("LocationNormalized" = "City"))


# Code the categories by taking levels - R does it automatically but it's a lot faster to code
train_all$title    <- as.numeric(as.factor(train_all$Title))
train_all$city     <- as.numeric(as.factor(train_all$City))
train_all$category <- as.numeric(as.factor(train_all$Category))
train_all$ctime    <- as.numeric(as.factor(train_all$ContractTime))
train_all$ctype    <- as.numeric(as.factor(train_all$ContractType))
train_all$company  <- as.numeric(as.factor(train_all$Company))

test$title    <- as.numeric(as.factor(test$Title))
test$city     <- as.numeric(as.factor(test$City))
test$category <- as.numeric(as.factor(test$Category))
test$ctime    <- as.numeric(as.factor(test$ContractTime))
test$ctype    <- as.numeric(as.factor(test$ContractType))
test$company  <- as.numeric(as.factor(test$Company))


#
# Make some initial plots to 
#
#ggplot(data=train_all,aes(x=company,y=Salary)) + geom_point() # some variability
#ggplot(data=train_all,aes(x=category,y=Salary)) + geom_point() # *** 
#ggplot(data=train_all,aes(x=ctype,y=Salary)) + geom_point()
#ggplot(data=train_all,aes(x=city,y=Salary)) + geom_point()
#
#ggplot(data=train_all,aes(x=ctime,y=Salary)) + geom_point()    # minor
#ggplot(data=train_all,aes(x=category,y=company,color=Salary)) + geom_point()  + geom_jitter() 


# --------------------------------------------------------------------------------------------------------
# Run the linear model
#  with and without the location tree
# 
# Run using the tm package to parse some text-heavy columns to create additional columns to use in the model
#    - With anything bigger than the smallest training set, takes a long time on desktop and laptop
# 
# Generally model 5 works best. Adding interaction terms in model 6 makes things slightly worse
# --------------------------------------------------------------------------------------------------------

print("Evaluating linear models with MAE, 10 fold CV")
errors <- model.nfold(10,train_all)
model_errors <- aggregate(errors, by=errors['m'], FUN=mean)
print(model_errors)

#print("Evaluating linear models and location tree with MAE, 10 fold CV")
#errors <- model.nfold(2,train_all,loc_tree)
#model_errors <- aggregate(errors, by=errors['m'], FUN=mean)
#print(model_errors)

print("Evaluating with some key job titles, 10 fold CV")
errors <- textmodel.nfold(10,train_all[1:5000,])
print(colMeans(errors))

# Finally, we need to work with the actual test data

# We should train our final model with all the training data #train_all
  
train_dtm <- get_dtm(train_all)
test_dtm  <- get_dtm(test)

train_all <- cbind(train_all, as.matrix(train_dtm[,job_titles]))
test      <- cbind(test, as.matrix(test_dtm[, job_titles]))

print("final model")
finalmodel <- lm(Salary ~ title + city + category + ctime + ctype + company + company:category  + 
                  teacher + chef+ support+ assistant+ 
                  administrator + operator + technician + analyst + consultant + engineer + engineering + trainee +
                  care + manager + nurse + developer, 
                data=train_all)  

print("predictions")
predictions <- predict(finalmodel, test)

# What are these predictions going to be?

# Put the submission together and write it to a file
print("writing submission file")
submission <- data.frame(Id=test$Id, Salary=predictions)
write.csv(submission, "my_submission.csv", row.names=FALSE)

print("done...")