from sklearn import linear_model
import matplotlib as pl



diabetes = datasets.load_diabetes()

diabetes_X_train = diabetes.data[:-20]
diabetes_X_test  = diabetes.data[-20:]
diabetes_y_train = diabetes.target[:-20]
diabetes_y_test  = diabetes.target[-20:]


regr = linear_model.LinearRegression()
regr.fit(diabetes_X_train, diabetes_y_train)

# >> LinearRegression(copy_X=True, fit_intercept=True, normalize=False)
print regr.coef_

# The mean square error
np.mean((regr.predict(diabetes_X_test)-diabetes_y_test)**2)

# Explained variance score: 1 is perfect prediction
# and 0 means that there is no linear relationship
# between X and Y.
regr.score(diabetes_X_test, diabetes_y_test) 

# Plot results

pl.clf()          # Clear plots

pl.plot(diabetes_X_test, regr.fit(diabetes_X_train, diabetes_y_train));

pl.title('Linear regression of sample diabetes data\n'
         'Centroids are marked with white cross')
pl.xlim(x_min, x_max)
pl.ylim(y_min, y_max)
pl.xticks(())
pl.yticks(())
pl.show()