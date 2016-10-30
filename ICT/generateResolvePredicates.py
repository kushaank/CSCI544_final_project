import os, csv, sys, glob, yaml, collections, unicodedata, xml.etree.ElementTree as ET

def coreNlpDictList(xmlFileName):
	corefDictList=[]
	tree = ET.parse(xmlFileName)
	root = tree.getroot()
	for coref in root[0][1].findall('coreference'):
		maxResText=unicodedata.normalize('NFKD', coref.findall('mention')[0].find('text').text).encode('ascii','ignore') if type(coref.findall('mention')[0].find('text').text)==unicode else coref.findall('mention')[0].find('text').text
		# create a list of dicts of the all coref
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
	return corefDictList

def extractSentences(data):
	# Both increaments are for i, not a mistake
	i=0
	newsSentences=[]
	while i<len(data):
		sentence=[]
		while data[i]:
			if len(data[i])==8:
				sentence.append(data[i])
			i+=1
		i+=1
		newsSentences.append(sentence)
	return newsSentences

def resolvePredicates(predicateFilePath,fileDateName,countryResList):
	predicateFileName=predicateFilePath.split('\\')[-1][:-14]
	with open(predicateFilePath, 'rb') as csvf:
		csvR = csv.reader(csvf, delimiter=',')
		allPredicate=[row for row in csvR]
	A0Actors=[];A1Actors=[];A2Actors=[]
	for predicate in allPredicate:
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
	for predicate in allPredicate:
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
	with open(predicateFilePath.split('news')[0]+'\\finalN'+predicateFileName[1:]+'Predicates.txt', 'w') as f:
		for predicate in finalPredicates:
			f.write(str(predicate)[1:-1]+'\n')

reload(sys)
sys.setdefaultencoding("utf-8")
partVal= int(sys.argv[1])
fileDateName=sys.argv[2]
dataPath='..\..\\DataFiles\\'+fileDateName+'\\'
with open('..\..\\DataFiles\\Country Resolution Lists\\countryResolutions.txt') as jsonfile:
	countryResList=yaml.load(jsonfile)
coreNLPPresence=glob.glob(dataPath+"CoreNLPOutput")!=[]
allFileNames=glob.glob(dataPath+'ClearnlpOutput\Part%d\\newsText*.txt.srl' % partVal)

for newsFileName in allFileNames:
	if os.stat(newsFileName)[6]!=0:
		srlFileName=newsFileName.split('\\')[-1]
		with open(newsFileName) as semanticFile:
			semanticReader = csv.reader(semanticFile, delimiter="\t")
			data = list(semanticReader)
		# Generate the coreference if the corenlp data is present
		xmlFileName=dataPath+'CoreNLPOutput\\Part%d\\' % partVal +srlFileName[:-7]+ 'xml'
		if coreNLPPresence and len(ET.parse(xmlFileName).getroot()[0])>1:
			corefDictList=coreNlpDictList(xmlFileName)
		newsSentences=extractSentences(data)
		allPredicates=[]
		for sentence in newsSentences:
			sentencePredicates=[]
			wholeSentence=''
			for item in sentence:
				' '.join([wholeSentence,item[1]])
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
			print 'Genrating the predicates for '+ srlFileName[:-4]
			with open(dataPath+'Predicates\\Part%d\\' % partVal +srlFileName[:-8]+'Predicates.csv', 'w') as f: 
				f.truncate()
				w = csv.DictWriter(f, allPredicates[0].keys())
				w.writeheader()
				for predicate in allPredicates:
					w.writerow(predicate)
			currentPredicateFilePath=dataPath+'Predicates\\Part%d\\newsText%dPredicates.csv' % (partVal, int(srlFileName[8:-8]))
			resolvePredicates(currentPredicateFilePath,fileDateName,countryResList)
