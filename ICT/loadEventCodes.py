import csv, os, glob, sys, gensim, time
os.chdir('..\..\DataFiles')
st=time.time()
# modelGoogleNews = gensim.models.Word2Vec.load_word2vec_format('word2vector\\GoogleNews-vectors-negative300.bin', binary=True)
dt=(time.time() -st)/60
print '\n'+str(round(dt, 2))+' mins for importing modelGoogleNews.\n'


removeList=[' or ', ' for ', 'others', ' and ', ' such ', ' as ', ' in ', ' of ', ' to ', ' on ', ' a ', ' other ', ' with ', ', ',' (', ')', ' not specified below' ]
listOfEventCodes=[]
with open("Country Resolution Lists\CAMEO.eventcodes.txt") as f:
	mreader = csv.reader(f, delimiter='\t')
	for row in mreader:
		row[1]=row[1].lower()
		for word in removeList:
			if word in row[1]:
				row[1]=row[1].replace(word, ' ')
		row[1]=row[1].replace('  ', ' ')
		row[1]=filter(None, row[1].split(' '))
		listOfEventCodes.append(row)

os.chdir('..\Programs\Python')
listOfEventCodes.remove(listOfEventCodes[0])

eventDict={}
for row in listOfEventCodes:
	eventDict[row[0]]=row[1]
	# codeLen=len(row[0])
	# while codeLen>1:
	# 	eventDict[row[0]]+=eventDict[row[0][0:codeLen]]
	# 	codeLen=codeLen-1
	eventDict[row[0]]=list(set(eventDict[row[0]]))
for row in listOfEventCodes:
	eventDict[row[0]]=[[modelGoogleNews.most_similar(positive=eventDict[row[0]], topn=3)], eventDict[row[0]]]
allWordsResultsFile = csv.writer(open("justCodeResults.csv" , "w"))
for key, val in sorted(eventDict.items()):
	allWordsResultsFile.writerow([key]+val)


