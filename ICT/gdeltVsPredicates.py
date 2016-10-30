import os, inspect, sys, glob, csv, datetime, operator

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + datetime.timedelta(n)

eventToPredicates={}
for date in daterange(datetime.date(2014, 5, 19), datetime.date(2014, 6, 20)):
	dateDir= str(date).replace('-', '\\')
	print dateDir
	# dateDir= '2014\\05\\19'
	os.chdir('..\..\DataFiles\\Country Resolution Lists')
	with open('CAMEO.eventcodes.txt') as codesFile:
		eventCodeDict={line.split('\t')[0]: line.split('\t')[1] for line in codesFile}
	with open('CAMEO.country.txt') as codesFile:
		countryCodeDict={line.split('\t')[0]: line.split('\t')[1] for line in codesFile}

	os.chdir('..\\'+dateDir)
	GdeltFile=dateDir.replace('\\', '')+'.export.CSV'
	predicatesFile='finalPredicates3cols.csv'
	# mapFile='URLFilenameMap.txt' #or .map

	actorsCodeUrlDict={}
	gdeltActorsCode=[]
	with open(GdeltFile) as newsFile:
		for line in newsFile:
			urlString=line.split("\t")[-1][:-1]
			# link: list of  [actor1, a1 location, actor2, a2 location, event code]
			try:
				eventCodeText=eventCodeDict[line.split("\t")[27]][:-1]
			except:
				eventCodeText=line.split("\t")[27]+": not a CAMEO code!"
			if line.split("\t")[6] and line.split("\t")[16] and line.split("\t")[7] and line.split("\t")[17]:
				gdeltActorsCode=[line.split("\t")[6], line.split("\t")[7],line.split("\t")[16], line.split("\t")[17], eventCodeText]
				try:
					actorsCodeUrlDict[urlString].append(gdeltActorsCode)
				except KeyError:
					actorsCodeUrlDict[urlString]= [gdeltActorsCode]
				try:
					eventToPredicates[eventCodeText]
				except:
					eventToPredicates[eventCodeText]={}
	# print "done with gdelt actor dict"

	predicateFileDict={}
	with open(predicatesFile) as predicatef:
		for line in predicatef:
			# filename: list of [actor1, verb, actor2]
			try:
				predicateFileDict[line.split(', ')[-2]].append(line.split(', ')[0:3])
			except:
				predicateFileDict[line.split(', ')[-2]]=[line.split(', ')[0:3]]
	# print "done with predicate file dict"

	os.chdir('NewsTextFiles')
	fileUrlDict={} 
	partsNames=glob.glob("Part*")
	for part in partsNames:
		os.chdir(part)
		try:
			mapFile=glob.glob('URLFilenameMap.*')[0]
			with open(mapFile) as mapf:
				for line in mapf:
					# filename: links
					line=line.replace(', ', '')
					if len(line.split(' :\t'))==2 :
						fileUrlDict[line.split(' :\t')[0][:-4]]=line.split(' :\t')[1][:-1]
		except:
			pass
		os.chdir('..')
	os.chdir('..')
	# print "done with file url dict"

	predicateGdeltDict={}
	for f in predicateFileDict.keys():
		try:
			predicateGdeltDict[f]={'Predicates': predicateFileDict[f],'Gdelt': actorsCodeUrlDict[fileUrlDict[f]]}

		except:
			pass

	for newsfile in predicateGdeltDict.keys():
		for event in predicateGdeltDict[newsfile]['Gdelt']:
			for predicate in predicateGdeltDict[newsfile]['Predicates']:
				try:
					eventToPredicates[event[4]][predicate[1][:-3]]+=1
				except:
					eventToPredicates[event[4]][predicate[1][:-3]]=1
				
	

	# dict of event: [list of predicates], only of the cases that both actors are present


	with open('mapGdeltPredicatesBothActorsCountryCode.csv', 'w+') as wf:
		for f in predicateGdeltDict.keys():
			wf.write(dateDir+'>'+f[4:]+': '+str(predicateGdeltDict[f])+"\n")
	print "done with map gdelt predicates dict " +dateDir
	os.chdir('..\..\..\..\Programs\\Python')
os.chdir('..\..\\DataFiles')
for event in eventToPredicates.keys():
	 eventToPredicates[event]=sorted(eventToPredicates[event].items(), key=operator.itemgetter(1), reverse=True)
with open(dateDir.replace('\\', '')+'GdeltPredicatesCount.csv', 'w+') as wff:
	for ff in eventToPredicates.keys():
		wff.write(ff+': '+str(eventToPredicates[ff])+"\n")
os.chdir('..\..\..\..\Programs\\Python')