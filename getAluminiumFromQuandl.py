import Quandl
from pprint import *
from numpy import *
from pandas import *





myData = Quandl.get("ODA/PALUM_USD", returns = 'pandas', authtoken = "Gps8Po8snGpup7qqsoSm")

 


myDataAsDataFrame = DataFrame(myData)

commodityPricesFile = open('aluminiumPricesAllYears.txt', 'w')



for date in myDataAsDataFrame.index:
    commodityPricesFile.write(str(date.year) + '-' + str(date.month) + '-' + str(date.day) + '\t' + str(myDataAsDataFrame.ix[date]['Value']) + '\n')

