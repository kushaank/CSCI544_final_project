# -*- coding: utf-8 -*-
import csv, re, os, sys, glob, time, unicodedata, shutil, collections, inspect, xml.etree.ElementTree as ET


def downloadGdeltFile(fileDateName):
	enteringDir=os.getcwd()
	if  not os.path.exists('..\..\..\..\DataFiles\\'+fileDateName):
		os.mkdirs('..\..\..\..\DataFiles\\'+fileDateName)
		os.chdir('..\..\..\..\DataFiles\\'+fileDateName)
		GdeltFile=dateDir.replace('\\', '')+'.export.CSV.zip'
		print 'Downloading: '+ GdeltFile
		url = 'http://data.gdeltproject.org/events/'+GdeltFile
		response = requests.get(url, stream=True)
		with open(GdeltFile, 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)
		zipGdeltFile=zipfile.ZipFile(GdeltFile)
		csvFile=zipfile.ZipFile.extract(zipGdeltFile, GdeltFile[:-4])
		zipGdeltFile.close()
		os.remove(GdeltFile)
	os.chdir(enteringDir)
#---------------------------------------------------------------------------------


def urlExtraction(fileDateName):
	enteringDir=os.getcwd()
	os.chdir('..\..\..\..\DataFiles\\'+fileDateName)
	GdeltFile=fileDateName.replace('\\', '')+'.export.CSV'
	fileToWrite=open('URLs.txt', 'w')
	uniqueUrls=[]
	print 'Extracting Urls from %s file ...' % GdeltFile
	with open(GdeltFile) as newsFile:
		for line in newsFile:
			urlString=line.split("\t")[-1]
			if urlString not in uniqueUrls:
				uniqueUrls.append(urlString)
	for urlString in uniqueUrls:
		fileToWrite.write(urlString)
	fileToWrite.close()
	print 'Urls extracted.'
	os.chdir(enteringDir)
#---------------------------------------------------------------------------------


def editNews(newsFile):
	enteringDir=os.getcwd()
	properEOL=['.', ',', ';', '!', '"', '\'']
	excludeTerms=['Notes:', 'Comments:', 'See also:', 'Credit:', 'http://', '# comments', 'Click here', '!!', 'commentConfig:', '\xe2', '|', '~', '\xc2','\xc3', '\xef', '\xe2']
	emailRegExp=re.compile('[\S\s]*[\w]+@[\w]+\.[\w]+[\S\s]*')
	editedNewsFile=''
	newsFile=str(newsFile)
	if newsFile!='':
		for line in newsFile.split('\n'):
			if len(line)>2 and line[-4:-1]!='...':
				if line[-1] in properEOL or line[-2] in properEOL:
					if emailRegExp.match(line)!=None: # if emailRegExp is in the line
						continue
					else:
						flag=False
						for st in excludeTerms:
							if st in line:
								flag=True
								break
						if not flag:
							editedNewsFile=editedNewsFile+'\n'+line
	return editedNewsFile
	os.chdir(enteringDir)
#---------------------------------------------------------------------------------


def moveSRLFiles(fileDateName):
	enteringDir=os.getcwd()
	os.chdir('..\..\..\..\DataFiles\\'+fileDateName+'\\NewsTextFiles')
	partsNames=glob.glob("Part*")
	for part in partsNames:
		os.chdir(part)
		allFileNames=glob.glob("*.srl")
		for fileName in allFileNames:
			try:
				if not os.path.exists('..\..\\ClearnlpOutput\\'+part):
					os.makedirs('..\..\\ClearnlpOutput\\'+part)
				shutil.move(fileName, '..\..\\ClearnlpOutput\\'+part)
			except:
				pass
		print part,
		os.chdir('..')
	os.chdir(enteringDir)
#---------------------------------------------------------------------------------


def generatePredicates(fileDateName_Part):
	enteringDir=os.getcwd()
	repCount=0
	countryResList = {}
	for key, val in csv.reader(open("..\..\..\..\DataFiles\\CountryResolutionLists\\countryResolutions.csv")):
		val=val.replace(" '",""); val=val.replace("'","")
		if list(set(val[1:-1].split(",")))[0]!='':
			countryResList[key] = list(set(val[1:-1].split(",")))
		else:
			countryResList[key] = []
	fileDateName= fileDateName_Part.split('\\Part')[0]
	partVal= int(fileDateName_Part.split('\\Part')[1])
	print 'Genrating predicates of part: '+fileDateName_Part
	dataPath="..\..\..\..\\DataFiles\\"+fileDateName
	coreNLPPresence=glob.glob(dataPath+'\\CoreNLPOutput')!=[]
	allFileNames=glob.glob(dataPath+'\\ClearnlpOutput\\Part%d\\newsText*.txt.srl' % partVal)
	for srlFileNamePath in allFileNames:
		if os.stat(srlFileNamePath)[6]!=0:
			srlFileName=srlFileNamePath.split('\\')[-1]
			with open(srlFileNamePath) as semanticFile:
				reader = csv.reader(semanticFile, delimiter="\t")
				data = list(reader)
			corefDictList=[]
			xmlFileName=dataPath+'\\CoreNLPOutput\\Part%d\\' % partVal +srlFileName[:-7]+ 'xml'
			if coreNLPPresence and len(ET.parse(xmlFileName).getroot()[0])>1:
				tree = ET.parse(xmlFileName)
				root = tree.getroot()
				for coref in root[0][1].findall('coreference'):
					if type(coref.findall('mention')[0].find('text').text)==unicode:
						maxResText=unicodedata.normalize('NFKD', coref.findall('mention')[0].find('text').text).encode('ascii','ignore')
					else:
						maxResText=coref.findall('mention')[0].find('text').text
					for mention in coref.findall('mention'):
						corefDict={}
						corefDict['sentenceNum']=mention.find('sentence').text
						if type(mention.find('text').text)==unicode:
							corefDict['corefText']=unicodedata.normalize('NFKD', mention.find('text').text).encode('ascii','ignore')
						else:
							corefDict['corefText']= mention.find('text').text
						corefDict['maxResolution']=maxResText
						corefDictList.append(corefDict)
			i=0
			newsSentences=[]
			while i<len(data):
				sentence=[]
				while data[i]!=[]:
					if len(data[i])==8:
						sentence.append(data[i])
					i=i+1
				i=i+1
				newsSentences.append(sentence)
			allPredicates=[]
			for sentence in newsSentences:
				sentencePredicates=[]
				wholeSentence=''
				for item in sentence:
					wholeSentence=wholeSentence+item[1]+' '
					item[7]=item[7].split(';')
					if 'pb=' in item[4]:
						predicate={'VerbID':'-1', 'A0':'', 'A0.35_Verb':'', 'A1':'', 'A2':'', 'SentenceID':-1,'Polarity':'Affirmative'}
						predicate['VerbID']=item[0]
						predicate['A0.35_Verb']=item[2]+'.'+item[4].split('.')[1][0:2]
						if  ':' in sentence[sentence.index(item)-1][7]:
							previousItemLast=sentence[sentence.index(item)-1][7]
							if previousItemLast.split(':')[0]==item[0] and 'NEG' in previousItemLast.split(':')[1]:
								predicate['A0.75_Polarity']='Negative'
						predicate['SentenceID']=newsSentences.index(sentence)+1
						sentencePredicates.append(predicate)
				for item in sentence:
					for arg in item[7]:
						if ':' in arg:
							# Add the items before the actor to the actor phrase
							agn=item[1]
							agnInd=item[0]
							tempItem=item
							if sentence.index(tempItem)!=0:
								tempItem=sentence[sentence.index(tempItem)-1]
								while tempItem[5]==agnInd:
									agn=tempItem[1]+' '+agn
									if sentence.index(tempItem)!=0:
										tempItem=sentence[sentence.index(tempItem)-1]
									else:
										break
							# Add the items after the actor to the actor phrase
							tempItem=item
							if sentence.index(tempItem)!=len(sentence)-1:
								tempItem=sentence[sentence.index(tempItem)+1]
								while tempItem[5]==agnInd:
									agn=agn+' '+tempItem[1]
									if sentence.index(tempItem)!=len(sentence)-1:
										tempItem=sentence[sentence.index(tempItem)+1]
										if int(tempItem[5])==int(sentence[sentence.index(tempItem)-1][0]):
											agnInd=str(int(tempItem[5]))
									else:
										break
							if arg.split(':')[1][0:2] in ['A0', 'A1', 'A2']:
								for predicate in sentencePredicates:
									if arg.split(':')[0]==predicate['VerbID']:
										predicate[predicate.keys()[predicate.keys().index(arg.split(':')[1][0:2])]]=agn
				for predicate in sentencePredicates:
					if predicate['A0']!='' and predicate['A1']!='' :
						predicate['RelatedSentence']=wholeSentence
						if corefDictList:
							for corefDict in corefDictList:
								if predicate['A0']==corefDict['corefText'] and predicate['SentenceID']==int(corefDict['sentenceNum']):
									predicate['A0']=corefDict['maxResolution']
								if predicate['A1']==corefDict['corefText'] and predicate['SentenceID']==int(corefDict['sentenceNum']):
									predicate['A1']=corefDict['maxResolution']
						allPredicates.append(collections.OrderedDict(sorted(predicate.items())[:-2]))
			if len(allPredicates)>0:
				# print 'Genrating the predicates from '+ srlFileName[:-4]
				with open(dataPath+'\\Predicates\\Part%d\\' % partVal +srlFileName[:-8]+'Predicates.csv', 'w') as f: 
					f.truncate()
					w = csv.DictWriter(f, allPredicates[0].keys())
					w.writeheader()
					for predicate in allPredicates:
						w.writerow(predicate)
	currentDir=dataPath+'\\Predicates\\Part%d' % partVal
	resolvePredicates(currentDir,fileDateName,countryResList)
	os.chdir(enteringDir)
#---------------------------------------------------------------------------------


def resolvePredicates(currentDir,fileDateName,countryResList):
	enteringDir=os.getcwd()
	allFileNames=glob.glob(currentDir+'\\newsText*Predicates.csv')
	allFilesFinalPredicates=[]
	for predicateFilePath in allFileNames:
		predicateFileName=predicateFilePath.split('\\')[-1][:-14]
		# print 'Country Resolution for '+ predicateFileName
		allPredicates=[]
		with open(predicateFilePath, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',')
			for row in spamreader:
				allPredicates.append(row)
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
				newPredicate+=[predicateFileName]
				if newPredicate[0]==newPredicate[-2] and newPredicate[4]!='':
					for key in countryResList.keys():
						if key in newPredicate[4]:
							newPredicate[-2]=key
				finalPredicates.append(newPredicate)
				for actor0 in A0Actors:
					if actor0[0] in newPredicate[1] and actor0[0] != newPredicate[0]:
						finalPredicates.append([actor0[0]]+newPredicate[1:])
		with open(currentDir+'\\finalN'+predicateFileName[1:]+'Predicates.txt', 'w') as f:
			# f.write("'actor0', 'A0', 'Verb', 'A1', 'A2','Polarity', actor1, 'File Name'\n")
			for predicate in finalPredicates:
				f.write(str(predicate)[1:-1]+'\n')
		print 'Predicates: '+predicateFileName, 
		allFilesFinalPredicates=allFilesFinalPredicates+finalPredicates
	allFilesFinalPredicates.sort()
	with open(currentDir+'\\allFilesFinalPredicatesBoth.csv', 'w+') as f:
		f.write("'actor0', 'A0', 'Verb', 'A1', 'A2', 'Polarity', 'Sentence', 'actor1', 'File Name', 'Date'\n")
		for predicate in allFilesFinalPredicates:
			f.write(str(predicate)[1:-1]+', '+fileDateName+'\n')
	with open(currentDir+'\\allPredicates3cols.csv', 'w+') as f:
		f.write('actor0, Verb, actor1, sentence, file, date\n')
		for predicate in allFilesFinalPredicates:
			predicate3cols=predicate[0]+', '+predicate[2]+', '+predicate[-2]+', '+predicate[-3]+', '+predicate[-1]+', '+fileDateName
			f.write(predicate3cols+'\n')
	print '\n Predicates done for part: '+fileDateName
	os.chdir(enteringDir)
#---------------------------------------------------------------------------------


def mergeFinalPredicates(fileDateName):
	enteringDir=os.getcwd()
	os.chdir('..\..\..\..\DataFiles\\'+fileDateName+'\Predicates')
	numDivisions=len(glob.glob("Part*"))
	finalPredicatesList=[]
	finalPredicates3cols=[]
	for i in range(1, numDivisions+1):
		os.chdir('Part%d' % i)
		with open("allFilesFinalPredicatesBoth.csv") as f:
			finalPredicatesList = finalPredicatesList+f.readlines()
		with open("allPredicates3cols.csv") as f3c:
			finalPredicates3cols = finalPredicates3cols+f3c.readlines()
		os.chdir('..')
	finalPredicatesList.sort()
	finalPredicates3cols.sort()
	extraTitle="'actor0', 'A0', 'Verb', 'A1', 'A2', 'Polarity', 'Sentence', 'actor1', 'File Name', 'Date'\n"
	extraTitle3cols='actor1, Verb, actor2, sentence, file, date\n'
	while extraTitle in finalPredicatesList: finalPredicatesList.remove(extraTitle)
	while extraTitle3cols in finalPredicates3cols: finalPredicates3cols.remove(extraTitle3cols)
	os.chdir('..')
	with open('finalPredicatesList.csv', 'w+') as f: 
		f.write("'actor0', 'A0', 'Verb', 'A1', 'A2', 'Polarity', 'Sentence', 'actor1', 'File Name', 'Date'\n")
		for predicate in finalPredicatesList:
			f.write(predicate)
	with open('finalPredicates3cols.csv', 'w+') as f3c: 
		f3c.write('actor1, Verb, actor2, sentence, file, date\n')
		for predicate in finalPredicates3cols:
			f3c.write(predicate)
	print '\n Merging Predicates is done! :)'
	os.chdir(enteringDir)
#---------------------------------------------------------------------------------

