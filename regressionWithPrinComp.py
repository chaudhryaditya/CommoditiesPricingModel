from numpy import *
import scipy as sp
from pandas import *
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
import pandas.rpy.common as com
from pprint import *
from random import *
from matplotlib.pyplot import *
from numpy.random import *


countriesFile = open('countries.txt', 'r')

numberOfCountriesThatWorked = 0

allVariablesFile = open('allCountriesGDP+AluminumPrice.csv', 'w')


listOfCountriesThatWorked = []
listOfExplanatoryVariables = []

i = 0

thisCountryWorks = False
for line in countriesFile:

    try:
        thisCountryGDPFile = open(line.strip()[line.find('|') + 1:] + '-GDPAllYears.txt', 'r')

    except:
        continue
    
   # print('1')

    stringContainingEntireFile = thisCountryGDPFile.read()
    firstYear = stringContainingEntireFile[: stringContainingEntireFile.find('-')]
   # firstLine = str(thisCountryGDPFile.readline().strip())

   # print(firstLine)

    #firstYear = firstLine[: firstLine.find('-')]
    #print(firstYear)

    if int(firstYear) == 1980 and stringContainingEntireFile.count('\n') == 40:
        thisCountryGDPFile.close()
        thisCountryGDPFile = open(line.strip()[line.find('|') + 1:] + '-GDPAllYears.txt', 'r')

        
        numberOfCountriesThatWorked += 1
        listOfCountriesThatWorked.append(line.strip()[line.find('|') + 1:] + '-GDPAllYears.txt')
        listOfExplanatoryVariables.append((line.strip()[line.find('|') + 1:] + ' GDP').replace(' ','').replace('.','').replace(',', '').replace("'", '').replace('-', ''))
    thisCountryGDPFile.close()



dictionaryOfGDPForAllCountriesForAllYears = {}



for countryFile in listOfCountriesThatWorked:
    thisCountryGDPFile = open(countryFile, 'r')

    numberOfEntries = 0
    
    for line in thisCountryGDPFile:
        line = line.strip()
        numberOfEntries += 1
       # thisYearGDPList = dictionaryOfGDPForAllCountriesForAllYears[line[:line.find'\t']]


        if line[:line.find('\t')] not in dictionaryOfGDPForAllCountriesForAllYears.keys():
       # if dictionaryOfGDPForAllCountriesForAllYears[line[:line.find('\t')]]  == None:
            dictionaryOfGDPForAllCountriesForAllYears[line[:line.find('\t')]] = [line[line.find('\t') + 1:]]

        else:
            #print(line[:line.find('\t')] + '\t' + str(dictionaryOfGDPForAllCountriesForAllYears[line[:line.find('\t')]] ))
           dictionaryOfGDPForAllCountriesForAllYears[line[:line.find('\t')]].append(line[line.find('\t') + 1:])

    if numberOfEntries != 40:
        print(countryFile)
    #print('After:' + countryFile)
    #pprint(dictionaryOfGDPForAllCountriesForAllYears)
    thisCountryGDPFile.close()


#pprint(dates)


aluminiumPricesDict = {}

aluminiumPricesFile = open('aluminiumPricesAllYears.txt', 'r')

for line in aluminiumPricesFile:
    line = line.strip()

    
    aluminiumPricesDict[line[:line.find('\t')]] = line[line.find('\t') + 1:]

#pprint(aluminiumPricesDict)

aluminiumPricesFile.close()

dates = list(aluminiumPricesDict.keys())
dates.sort()



allVariablesFile.write('Year')

for country in listOfExplanatoryVariables:
    country = country.replace(',' , '')
    allVariablesFile.write(',' + country)
    #print(country)


allVariablesFile.write(',Aluminium Price For Year')


allVariablesFile.write('\n')



for date in dates:
    allVariablesFile.write(date)
    #if len(dictionaryOfGDPForAllCountriesForAllYears[date]) == 144:
    # print('YOOOOOOOOOO\t' + str(date) + '\t' + str(len(dictionaryOfGDPForAllCountriesForAllYears[date])))

    relevantKeyForGDPsDict = 'date'

    for key in dictionaryOfGDPForAllCountriesForAllYears.keys():
        if date[:date.find('-')] in key:
            relevantKeyForGDPsDict = key
            
    for number in dictionaryOfGDPForAllCountriesForAllYears[relevantKeyForGDPsDict]:
        allVariablesFile.write(',' + str(number))

    allVariablesFile.write(',' + str(aluminiumPricesDict[date]))

    allVariablesFile.write('\n')

    
print( str(numberOfCountriesThatWorked) + ' countries worked = ' + str(len(listOfExplanatoryVariables)) + ' should also equal = ' + str(len(listOfCountriesThatWorked)))

#pprint(dictionaryOfGDPForAllCountriesForAllYears['2019-12-31'])
#pprint(listOfExplanatoryVariables[143])
#pprint(dictionaryOfGDPForAllCountriesForAllYears['2019-12-31'][142])

#for date in dates:
    #pprint(dictionaryOfGDPForAllCountriesForAllYears[date][142])



countriesFile.close()
allVariablesFile.close()


#NOTE:Create model for this set of explanatory variables

#NOTE: Read in data
ro.r('allData = read.csv("allCountriesGDP+AluminumPrice.csv", header=TRUE)')
#print(ro.r['allData'])



#PrinComp everything except the first and last columns
ro.r('independentVariables = allData[-1]')

ro.r('independentVariables = independentVariables[-144]')

ro.r('fit <- princomp(independentVariables, cor=TRUE)')

x = ro.r('fit')

#print(x)

#Select principle components that are significant (i.e. the ones with proportion of variance explaines greater than let's say 10% for now

ro.r('vars <- fit$sdev^2')
ro.r('propOfVarianceExplained <- vars/sum(vars)')

listOfPropOfVarianceExplained = list(ro.r('propOfVarianceExplained'))

#pprint(listOfPropOfVarianceExplained)

dictOfPrinCompVariables = {'scores': [],
                           'loadings': {},
                           'scale': {},
                           'center': {}}

indexOfLastRelevantPrinComp = 1

for index in range(1,len(listOfPropOfVarianceExplained)):
    #print(listOfPropOfVarianceExplained[index - 1])
    if listOfPropOfVarianceExplained[index - 1] > .1:

        #Scores

        
        print('got here')

       # print('fit$scores[,' + str(index) + ']')
        listOfScoresForThisPrinComp = list(ro.r('fit$scores[,' + str(index) + ']'))
        dictOfPrinCompVariables['scores'].append(listOfScoresForThisPrinComp)


        #Loadings

        listOfRowNamesForLoadings = list(ro.r('rownames(fit$loadings)'))
        #pprint(listOfRowNamesForLoadings)
        
        for key in listOfRowNamesForLoadings:
           # print('loadings(fit)[,' + str(index) + ']["' + key + '"]')
            number = str(ro.r('loadings(fit)[,' + str(index) + ']["' + key + '"]'))
           # print(number)
           # print(number[number.find('\n') + 1])
            numberAsFLoat = float(number[number.find('\n') + 1:len(number)])
           # print(numberAsFLoat)
            dictOfPrinCompVariables['loadings'][key] = numberAsFLoat

            
        
      #Scale

        listOfRowNamesForScale = list(ro.r('names(fit$scale)'))
       # pprint(listOfRowNamesForLoadings)
        
        for key in listOfRowNamesForScale:
           # print('fit$scale["' + key + '"]')
            number = str(ro.r('fit$scale["' + key + '"]'))
           # print(number)
           # print(number[number.find('\n') + 1])
            numberAsFLoat = float(number[number.find('\n') + 1:len(number)])
           # print(numberAsFLoat)
            dictOfPrinCompVariables['scale'][key] = numberAsFLoat

        #Center

        listOfRowNamesForCenter = list(ro.r('names(fit$center)'))
       # pprint(listOfRowNamesForLoadings)
        
        for key in listOfRowNamesForCenter:
           # print('fit$center["' + key + '"]')
            number = str(ro.r('fit$center["' + key + '"]'))
           # print(number)
           # print(number[number.find('\n') + 1])
            numberAsFLoat = float(number[number.find('\n') + 1:len(number)])
           # print(numberAsFLoat)
            dictOfPrinCompVariables['center'][key] = numberAsFLoat


        indexOfLastRelevantPrinComp = index

#pprint(dictOfPrinCompVariables)

print(indexOfLastRelevantPrinComp)


#NOTE: Calculate model

ro.r('model <- lm(allData[[145]] ~ fit$scores[,1:' + str(indexOfLastRelevantPrinComp) + '])')
print(ro.r('summary(model)'))

#Extract and store information from model

modelDict = {'estimates': [],
             'SE': []}


for i in range(indexOfLastRelevantPrinComp + 1):
    modelDict['estimates'].append(float(ro.r('summary(model)$coefficients[' + str(i + 1) + ',1]')[0]))
    modelDict['SE'].append(float(ro.r('summary(model)$coefficients[' + str(i + 1) + ',2]')[0]))

#pprint(modelDict)
    
#NOTE: Get scores for current values

listOfScoresToPlugIntoModel = []

for prinComp in range(len(dictOfPrinCompVariables['scores'])):  #for each relevant principal component
    scoreForThisPrincomp = float(ro.r('predict(fit, newdata=independentVariables[' + str(len(dictOfPrinCompVariables['scores'][0])) + ',1:' + str(len(dictOfPrinCompVariables['loadings'].keys())) + '])')[0]) #calcuate socre for this principal component based on current values
    #pprint(scoreForThisPrincomp)
    listOfScoresToPlugIntoModel.append(scoreForThisPrincomp)


pprint(listOfScoresToPlugIntoModel)


#NOTE: Plug in scores for current values into model

##currentPredictedValue = modelDict['estimates'][0]
##
##
##for i in range(indexOfLastRelevantPrinComp):
##    currentPredictedValue += modelDict['estimates'][i + 1] * listOfScoresToPlugIntoModel[i]
##

##print(currentPredictedValue)


#NOTE: Run Monte-Carlo simulation with 10,000 trials

listOfPredictedPrices = []
for simNumber in range(10000):
    currentPredictedValueForThisSim = normal(modelDict['estimates'][0], modelDict['SE'][0]) #intercept
    
    for i in range(indexOfLastRelevantPrinComp):    #Explanatory variables
        currentPredictedValueForThisSim += normal(modelDict['estimates'][i + 1], modelDict['SE'][i + 1]) * listOfScoresToPlugIntoModel[i]

    listOfPredictedPrices.append(currentPredictedValueForThisSim)


listOfPredictedPrices.sort()

alpha = .05

lowerBoundOfCIIndex = int(len(listOfPredictedPrices) * alpha/2)
upperBoundOfCIIndex = int(len(listOfPredictedPrices) * (1 - alpha/2))

print('I am ' + str((1 - alpha) * 100) + '% confident that the current price of aluminium should be between ' + str(listOfPredictedPrices[lowerBoundOfCIIndex]) + ' and ' + str(listOfPredictedPrices[upperBoundOfCIIndex]))



hist(listOfPredictedPrices, bins = 20)
title('Monte Carlo Simulation for Aluminium Price')
xlabel('Price ($)')
ylabel('Frequency')
show()


                           
##
##stringOfExplanatoryVariables = ''
##
##shuffle(listOfExplanatoryVariables)
##
##for variable in listOfExplanatoryVariables:
##   # variable = variable.replace(' ', '.')
##    stringOfExplanatoryVariables += variable + ' + '
##
##stringOfExplanatoryVariables = stringOfExplanatoryVariables[: stringOfExplanatoryVariables.rfind('+')]
###pprint(stringOfExplanatoryVariables)
##
##
##rCommandForMultipleRegression = 'Aluminium.Price.For.Year ~ ' + stringOfExplanatoryVariables
##
##rCommandForMultipleRegression = 'model = lm(formula = ' + rCommandForMultipleRegression + ', data =  allData)'
##
###pprint( rCommandForMultipleRegression)
##
##ro.r(rCommandForMultipleRegression)
##
###print(ro.r('summary(model)'))
##
##
##
##
##
###NOTE:Remove least significant explanatory variable
##
##pValues  = list(ro.r('summary(model)$coefficients[,4]'))[1:]    #list(ro.r('anova(model)[["Pr(>F)"]]'))
##
##pprint(pValues)
##
##trimmedListOfExplanatoryVariables = list(ro.r('rownames(summary(model)$coefficients[,0])'))[1:]    #list(ro.r('rownames(anova(model)[5])'))
##
##
##pprint(trimmedListOfExplanatoryVariables)
##
##dictOfExplanatoryVariablesAndPValues = {}
##
##
##for index in range(len(trimmedListOfExplanatoryVariables)):
##    if not pValues[index]  == 'NA_real_':
##        dictOfExplanatoryVariablesAndPValues[trimmedListOfExplanatoryVariables[index]] = pValues[index]
##
##
##
##
##
##
##maxPValue = 0
##variableBelongingToMaxPValue = ''
##
##
##for explanatoryVariable in trimmedListOfExplanatoryVariables:
##    if dictOfExplanatoryVariablesAndPValues[explanatoryVariable] > maxPValue:
##        variableBelongingToMaxPValue = explanatoryVariable
##        maxPValue = dictOfExplanatoryVariablesAndPValues[explanatoryVariable]
##
##x = listOfExplanatoryVariables.remove(variableBelongingToMaxPValue)
##
##if(maxPValue < .01):
##    print('YOOOOOOO' + str(maxPValue) + '\t' + variableBelongingToMaxPValue)
##
##    pprint(dictOfExplanatoryVariablesAndPValues)
##    print(ro.r('summary(model)'))
##    break
##
### pprint(dictOfExplanatoryVariablesAndPValues)
##
### pprint(listOfExplanatoryVariables)
##print(ro.r('anova(model)'))
##print(variableBelongingToMaxPValue + '\t' + str(maxPValue))
##
##print('Number of Explanatory Variables = ' + str(len(listOfExplanatoryVariables)))

print('------------------------------------------------')
#print(ro.r('summary(model)'))
