import csv

currentPercentageFile='..\..\\DataFiles\\BayesianNetResults\\IntersectionEvents\\GdletEvents2012PercentagesWithPairs.csv'
pairCounts=[]
with open(currentPercentageFile) as percentageFile:
	j=0
	for line in percentageFile:
		if j>0:
			seperatedLine=line.split(', ')
			pairCounts.append([seperatedLine[0][:-5]])
		j+=1

currentCountFile='..\..\\DataFiles\\BayesianNetResults\\IntersectionEvents\\GdletEvents2012Counts.csv'
with open(currentCountFile) as countsFile:
	j=0
	for line in countsFile:
		if j>0:
			seperatedLine=line.split(', ')
			pCount=sum([int(countVal) for countVal in seperatedLine[:-1]])
			pairCounts[j-1].append(pCount)
		j+=1


#pair-count-list
#==========================================================

pairRankFile='..\..\\DataFiles\\BayesianNetResults\\IntersectionEvents\\sortedPairsTrain20062011Test2012.csv'
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

with open('..\..\\DataFiles\\BayesianNetResults\\IntersectionEvents\\pairCountRankTrain20062011Test2012.csv', 'w') as fileToWrite:
	fileToWrite.truncate()
	fileToWrite.write('CountryPair, Count, Rank\n')
	for item in pairCountRank:
		fileToWrite.write(str(item)[1:-1] + '\n')
