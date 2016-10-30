import csv, re, os, sys, glob, time, unicodedata, collections,inspect, xml.etree.ElementTree as ET
t0 = time.time()
partVal= int(sys.argv[1])
fileDateName=sys.argv[2]
os.chdir('..\..\DataFiles\\'+fileDateName)
coreNLPPresence=glob.glob("CoreNLPOutput")!=[]
os.chdir('ClearnlpOutput\Part%d' % partVal)
allFileNames=glob.glob("newsText*.txt.srl")

for newsFileName in allFileNames:
	if os.stat(newsFileName)[6]!=0:
		with open(newsFileName) as semanticFile:
			reader = csv.reader(semanticFile, delimiter="\t")
			data = list(reader)
		
		corefDictList=[]
		if coreNLPPresence and len(ET.parse('..\\..\\CoreNLPOutput\\Part%d\\' % partVal +newsFileName[:-7]+ 'xml' ).getroot()[0])>1:
			# Generate the co-reference dictionary 
			xmlFileName='..\\..\\CoreNLPOutput\\Part%d\\' % partVal +newsFileName[:-7]+ 'xml'
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
			print 'Genrating the predicates for '+ newsFileName[:-4]
			with open('..\\..\\Predicates\\Part%d\\' % partVal +newsFileName[:-8]+'Predicates.csv', 'w') as f: 
				f.truncate()
				w = csv.DictWriter(f, allPredicates[0].keys())
				w.writeheader()
				for predicate in allPredicates:
					w.writerow(predicate)
t1 = time.time(); total = int(t1-t0)
print 'Time of '+inspect.getfile(inspect.currentframe())+' : '+ str(total)+ ' secs\n\n'