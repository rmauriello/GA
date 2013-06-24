Title
========================================================

This is an R Markdown document. Markdown is a simple formatting syntax for authoring web pages (click the **MD** toolbar button for help on Markdown).

When you click the **Knit HTML** button a web page will be generated that includes both content as well as the output of any embedded R code chunks within the document. You can embed an R code chunk like this:


```r
summary(cars)
```

```
##      speed           dist    
##  Min.   : 4.0   Min.   :  2  
##  1st Qu.:12.0   1st Qu.: 26  
##  Median :15.0   Median : 36  
##  Mean   :15.4   Mean   : 43  
##  3rd Qu.:19.0   3rd Qu.: 56  
##  Max.   :25.0   Max.   :120
```

```r

#
# 
# Variables: Id, Title - job description, often including location
# FullDescription - detailed job description LocationRaw -
# LocationNormalized - city ContractType - full_time, part_time, NA
# (almost always full-time according to boxplots) ContractTime -
# permanent, contract, NULL (boxplots very different) Company - recruiting
# company or actual?  Category - job category, e.g. engineering **
# SalaryRaw - salary, often as range (pounds) SalaryNormalized - salaray
# as actual number (pounds) SourceName - URL (of job posting?)

require("plyr")
```

```
## Loading required package: plyr
```

```r

setwd("/Volumes/DATA/robert/Desktop/Projects/GA/salary")

df <- read.csv("data/train.csv")
test <- read.csv("data/test.csv")


# Rename some columns to make life easier
df2 <- df

df2 <- rename(df2, replace = c(LocationNormalized = "City"))
df2 <- rename(df2, c(SalaryNormalized = "Salary"))
test <- rename(test, c(LocationNormalized = "City"), warn_missing = TRUE)


# Remove *** and city from description
df2$city <- as.numeric(as.factor(df2$City))
df2$category <- as.numeric(as.factor(df2$Category))
df2$ctime <- as.numeric(as.factor(df2$ContractTime))
df2$ctype <- as.numeric(as.factor(df2$ContractType))
df2$company <- as.numeric(as.factor(df2$Company))


test$city <- as.numeric(as.factor(test$City))
test$category <- as.numeric(as.factor(test$Category))
test$ctime <- as.numeric(as.factor(test$ContractTime))
test$ctype <- as.numeric(as.factor(test$ContractType))
test$company <- as.numeric(as.factor(test$Company))



# Code the categories

salary.glm <- glm(Salary ~ city + category + ctime + ctype + company, data = df2)
summary(salary.glm)
```

```
## 
## Call:
## glm(formula = Salary ~ city + category + ctime + ctype + company, 
##     data = df2)
## 
## Deviance Residuals: 
##    Min      1Q  Median      3Q     Max  
## -29109  -10109   -3829    6038  137961  
## 
## Coefficients:
##              Estimate Std. Error t value Pr(>|t|)    
## (Intercept) 28335.886    642.377   44.11  < 2e-16 ***
## city            1.241      0.601    2.07    0.039 *  
## category     -169.583     26.303   -6.45  1.2e-10 ***
## ctime        4631.938    169.310   27.36  < 2e-16 ***
## ctype       -1482.168    261.217   -5.67  1.4e-08 ***
## company        -5.617      0.426  -13.18  < 2e-16 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1 
## 
## (Dispersion parameter for gaussian family taken to be 241149598)
## 
##     Null deviance: 2.609e+12  on 9999  degrees of freedom
## Residual deviance: 2.410e+12  on 9994  degrees of freedom
## AIC: 221396
## 
## Number of Fisher Scoring iterations: 2
```

```r

plot(predict(salary.lm, test))
```

```
## Error: object 'salary.lm' not found
```

```r

cv.glm(df2, salary.glm, K = 10)
```

```
## Error: could not find function "cv.glm"
```

```r


# Calculate MAE (mean absolute error)

```


You can also embed plots, for example:


```r
plot(cars)
```

![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-2.png) 


