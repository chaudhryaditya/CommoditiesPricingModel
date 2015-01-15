# CommoditiesPricingModel

Written in Python and calling R, this model currently pulls macroeconomic data from Quandl.com and uses principle component analysis to conduct multiple regression to generate a model to price commodities. The code then runs Monte Carlo simulations to output, graphically and textually, a confidence interval for what the price of the commodity in question "should be" based on historical data.

Dependencies:

Python 3
Quandl Python Library
Ystockuote
Numpy
Scipy
Rpy
Pandas
