#
#
#
install.packages('DMwR')
library(DMwR)

data(algae)
summary(algae)

hist(algae$mxPH, prob = T)  # Plot histogram of mxPH

plot(algae$NH4, xlab = '')  # Plot of NH4, without x label
#
# Add three lines to the plot corresponding to mean(NH4), mean+SD, median
abline(h = mean(algae$NH4, na.rm = T), lty = 1)  
abline(h = mean(algae$NH4, na.rm = T) + sd(algae$NH4, na.rm = T), lty = 2)
abline(h = median(algae$NH4, na.rm = T), lty = 3)  

# Perform linear regression of P04 on OPO4
lm(PO4 ~ oPO4, data = algae)
clean.algae <- knnImputation(algae, k = 10) # Fills in NA values by using Knn

#
# Perform regression on subset 
# ANOVA
#
lm.a1 <- lm(a1 ~ ., data = clean.algae[, 1:12]) 
summary(lm.a1)
anova(lm.a1) 

lm2.a1 <- update(lm.a1, . ~ . - season)      # Update the model by removing season
summary(lm2.a1)
anova(lm.a1, lm2.a1)

final.lm <- step(lm.a1)                      # 
