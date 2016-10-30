import csv

trainYear=2007
testYear=2007
for testYear in range(2006,2013):
	currentPercentageFile='..\..\\DataFiles\\BayesianNetResults\\GdletEvents'+ str(testYear)+'PercentagesWithPairs.csv'
	pairCounts=[]
	with open(currentPercentageFile) as percentageFile:
		j=0
		for line in percentageFile:
			if j>0:
				seperatedLine=line.split(', ')
				pairCounts.append([seperatedLine[0][:-5]])
			j+=1

	currentCountFile='..\..\\DataFiles\\BayesianNetResults\\GdletEvents'+ str(testYear)+'Counts.csv'
	with open(currentCountFile) as countsFile:
		j=0
		for line in countsFile:
			if j>0:
				seperatedLine=line.split(', ')
				pCount=sum([int(countVal) for countVal in seperatedLine[:-1]])
				pairCounts[j-1].append(pCount)
			j+=1
	print pairCounts[0]

	#pair-count-list
	#==========================================================

	for trainYear in range(2006, 2013):
		pairRankFile='..\..\\DataFiles\\BayesianNetResults\\sortedPairsTrain'+str(trainYear)+'Test'+str(testYear)+'.csv'
		pairRankDict={}
		with open(pairRankFile) as sortedPairsFile:
			i=0
			for line in sortedPairsFile:
				if i>0:
					pairRankDict[line[:-6]]=i
				i+=1

		pairCountRank=[]
		for item in pairCounts:
			pairCountRank.append(item+[pairRankDict[item[0]]])

		with open('..\..\\DataFiles\\BayesianNetResults\\pairCountRankTrain%dTest%d.csv' %(trainYear,testYear), 'w') as fileToWrite:
			fileToWrite.truncate()
			fileToWrite.write('CountryPair, Count, Rank\n')
			for item in pairCountRank:
				fileToWrite.write(str(item)[1:-1] + '\n')
