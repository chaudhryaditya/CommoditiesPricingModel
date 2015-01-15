import Quandl
from pprint import *
from numpy import *
from pandas import *

countriesFile = open('countries.txt', 'r')

numberOfCountriesThatWorked = 0
numberOfCountriesThatDidntWork = 0



for line in countriesFile:
    countryCode = line.strip()[:line.find('|')]
    pprint("ODA/" + countryCode + "_PPPGDP")

    try:
        myData = Quandl.get("ODA/" + countryCode + "_PPPGDP", returns = 'pandas', authtoken = "Gps8Po8snGpup7qqsoSm")

        
    except:
        numberOfCountriesThatDidntWork +=1
        continue

    
    myDataAsDataFrame = DataFrame(myData)
    print('1')

    thisCountryGDPFile = open(line.strip()[line.find('|') + 1:] + '-GDPAllYears.txt', 'w')

    print('1')


    for date in myDataAsDataFrame.index:
        thisCountryGDPFile.write(str(date.year) + '-' + str(date.month) + '-' + str(date.day) + '\t' + str(myDataAsDataFrame.ix[date]['Value']) + '\n')

    numberOfCountriesThatWorked += 1

        #myDataNumpyArray = array(myData)
    
        
print( str(numberOfCountriesThatWorked) + ' countries worked')
print( str(numberOfCountriesThatDidntWork) + ' countries did not work') 

    
    #pprint(myData)
