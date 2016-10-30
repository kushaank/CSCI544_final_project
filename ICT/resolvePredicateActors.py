import csv, os, glob, sys

partVal= int(sys.argv[1])
fileDateName=sys.argv[2]
os.chdir('..\..\DataFiles')
countryResList = {}
for key, val in csv.reader(open("Country Resolution Lists\\countryResolutions.csv")):
	val=val.replace(" '",""); val=val.replace("'","")
	if list(set(val[1:-1].split(",")))[0]!='':
		countryResList[key] = list(set(val[1:-1].split(",")))
	else:
		countryResList[key] = []
os.chdir('..\..\DataFiles\\'+fileDateName+'\Predicates\Part%d' % partVal)

allFileNames=glob.glob("newsText*Predicates.csv")
allFilesFinalPredicates=[]
for newsFileName in allFileNames:
	print 'Resolving the predicates for '+ newsFileName[:-14]
	with open(newsFileName, 'rb') as csvfile:
		csvReader = csv.reader(csvfile, delimiter=',')
		allPredicates=[row for row in csvReader]
	allPredicates=allPredicates[1:]
	A0Actors=[];A1Actors=[];A2Actors=[]
	for predicate in allPredicates:
		for key in countryResList.keys():
			if key in predicate[0]:
				actor0=[key]+countryResList[key]
				if actor0 not in A0Actors:
					A0Actors.append(actor0)
			else:
				if key=='United States' or key=='United Kingdom':
					for val in countryResList[key]:
						if val in predicate[0]:
							actor0=[key]+countryResList[key]
							if actor0 not in A0Actors:
								A0Actors.append(actor0)
		for key in countryResList.keys():
			if key in predicate[2]:
				actor1=[key]+countryResList[key]
				if actor1 not in A1Actors:
					A1Actors.append(actor1)
			else:
				if key=='United States' or key=='United Kingdom':
					for val in countryResList[key]:
						if val in predicate[2]:
							actor1=[key]+countryResList[key]
							if actor1 not in A1Actors:
								A1Actors.append(actor1)
	finalPredicates=[]
	for predicate in allPredicates:
		newPredicate=[]
		foundResA0=False; foundResA1=False
		for actor0 in A0Actors:
			for resWord in actor0:
				if not foundResA0 and resWord in predicate[0]:
					foundResA0=True
					break
			if foundResA0:
				newPredicate=[actor0[0]]+predicate
				break
		for actor1 in A1Actors:
			for resWord in actor1:
				if not foundResA1 and resWord in predicate[2]:
					foundResA1=True
					break
			if foundResA1:
				newPredicate=newPredicate+[actor1[0]]
				break
		if foundResA0 and foundResA1:
			newPredicate+=[newsFileName[:-14]]
			if newPredicate[0]==newPredicate[-2] and newPredicate[4]!='':
				for key in countryResList.keys():
					if key in newPredicate[4]:
						newPredicate[-2]=key
			finalPredicates.append(newPredicate)
			for actor0 in A0Actors:
				if actor0[0] in newPredicate[1] and actor0[0] != newPredicate[0]:
					finalPredicates.append([actor0[0]]+newPredicate[1:])
	with open('finalN'+newsFileName[1:-3]+'txt', 'w') as f:
		# f.write("'actor0', 'A0', 'Verb', 'A1', 'A2','Polarity', actor1, 'File Name'\n")
		for predicate in finalPredicates:
			f.write(str(predicate)[1:-1]+'\n')
	allFilesFinalPredicates=allFilesFinalPredicates+finalPredicates
allFilesFinalPredicates.sort()
with open('allFilesFinalPredicatesBoth.csv', 'w+') as f:
	f.write("'actor0', 'A0', 'Verb', 'A1', 'A2', 'Polarity', 'Sentence', 'actor1', 'File Name', 'Date'\n")
	for predicate in allFilesFinalPredicates:
		f.write(str(predicate)[1:-1]+', '+fileDateName+'\n')

with open('allPredicates3cols.csv', 'w+') as f:
	f.write('actor0, Verb, actor1, sentence, file, date\n')
	for predicate in allFilesFinalPredicates:
		predicate3cols=predicate[0]+', '+predicate[2]+', '+predicate[-2]+', '+predicate[-3]+', '+predicate[-1]+', '+fileDateName
		f.write(predicate3cols+'\n')
