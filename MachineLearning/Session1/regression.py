#This is meant for an interactive Python shell
#Tested on jupyter
#Created by abulyomon@gmail.com for JOSA's Data Science Bootcamp

#Load the data
import pandas
cars = pandas.read_csv("AlWaseet.csv")
#Take a look
cars.describe()

###LINEAR
#Visualize
import matplotlib.pyplot as plt
plt.xlabel("Milage in KM")
plt.ylabel("Price in JOD")
plt.xlim([0,200000])

plt.scatter(cars['MILEAGE'], cars['PRICE'])
plt.show()
#Do they relate?
cars['PRICE'].corr(cars['MILEAGE'])
#FYI
cars['MILEAGE'].corr(cars['PRICE'])
#Let's regress
import statsmodels.formula.api as stats

formula1 = 'PRICE ~ MILEAGE'
model1 = stats.ols(formula1, data = cars).fit()
model1.summary()
#S INTERPRETATION
#Remove outlier
cars = cars[cars.PRICE < max(cars.PRICE)]
model1v2 = stats.ols(formula1, data = cars).fit()
model1v2.summary()

#Plot again
plt.xlabel("Mileage in KM")
plt.ylabel("Price in JOD")
plt.xlim([0,200000])
plt.scatter(cars['MILEAGE'], cars['PRICE'])
plt.plot(cars['MILEAGE'], model1v2.predict(cars))
plt.show()
## BREAK
#### More variables
import datetime
cars['AGE'] = datetime.date.today().year - cars['YEAR'] #Guess what, ignore the warning!
cars.describe()

plt.xlabel("Age in Years")
plt.ylabel("Price in JOD")
plt.xlim([0,20])
plt.scatter(cars['AGE'], cars['PRICE'])
plt.show()

cars['AGE'].corr(cars['PRICE'])

formula2 = 'PRICE ~ MILEAGE + AGE'
model2 = stats.ols(formula2, data = cars).fit()
model2.summary()
#S INTERPRETATION
formula3 = 'PRICE ~ MILEAGE + AGE + CHASSIS_FR + CHASSIS_FL \
            + CHASSIS_RR + CHASSIS_RL'
model3 = stats.ols(formula3, data = cars).fit()
model3.summary()

cars['CHASSIS'] = cars['CHASSIS_FR'] + cars['CHASSIS_FL'] + cars['CHASSIS_RR'] \
+ cars['CHASSIS_RL'] #Ok, yes ignore the warning, again!

formula3 = 'PRICE ~ MILEAGE + AGE + CHASSIS'
model3 = stats.ols(formula3, data = cars).fit()
model3.summary()

cars['MILEAGE'].corr(cars['AGE'])
#DAMN!
plt.xlim([0,200000])
plt.scatter(cars['MILEAGE'],cars['AGE'])
plt.show()

formula4 = 'PRICE ~ AGE + CHASSIS'
model4 = stats.ols(formula4, data=cars).fit()
model4.summary()

###LOGISTIC
lformula1 = 'CHASSIS ~ PRICE + MILEAGE + AGE'
lmodel1 = stats.logit(lformula1, data=cars).fit()
lmodel1.summary()
#Interpret coefficients
import math
for (var, coef) in  lmodel1.params.iteritems():
    if (var == "Intercept"):
        continue
    print var, math.exp(coef)
#Try another model
lformula2 = 'CHASSIS ~ AGE'
lmodel2 = stats.logit(lformula2, data=cars).fit()
lmodel2.summary()
#Check prediction power
(map(lambda x:round(x), lmodel1.predict()) == cars.CHASSIS) #OVERFITTING!
#S A COMMENT ON PREDICTION
