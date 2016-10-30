import json, csv #, collections
destinationPath='..\..\\DataFiles\\Country Resolution Lists\\'
with open(destinationPath+'country_nationality.txt') as fcn: countryNationality = list(csv.reader(fcn, delimiter="\t"))

with open(destinationPath+'country_capital.txt') as fcc: countryCapital = list(csv.reader(fcc, delimiter="\t"))

with open(destinationPath+'country_headOfState.txt') as fchos: countryHeadOfState = list(csv.reader(fchos, delimiter="\t"))

with open(destinationPath+'CAMEO.knowngroup.txt') as fkg: knownGroup = list(csv.reader(fkg, delimiter="\t"))

countries=[countryNationality[i][0] for i in range(len(countryNationality))]
countries.extend([countryCapital[i][0] for i in range(len(countryCapital))])
countries.extend([countryHeadOfState[i][0] for i in range(len(countryHeadOfState))])
countries.extend([knownGroup[i][1] for i in range(len(knownGroup))])
countries=list(set(countries))

countryResList={}
for country in countries:
	countryResRec=[]
	[countryResRec.extend(val) for val in countryNationality if val[0]==country]
	[countryResRec.extend(val) for val in countryCapital if val[0]==country]
	[countryResRec.extend(val) for val in countryHeadOfState if val[0]==country]
	[countryResRec.extend(val[1:]) for val in knownGroup if val[1]==country]
	countryResRec=list(set(countryResRec))
	if country in countryResRec: countryResRec.remove(country)
	countryResList[country]=countryResRec

# countryResList=collections.OrderedDict(sorted(countryResList.items()))

with open(destinationPath+'countryResolutions.txt', 'w') as outfile:
  json.dump(countryResList, outfile)
