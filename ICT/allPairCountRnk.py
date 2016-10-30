import csv, os, sys, os.path, glob

rankDict={}
pairCountRank='..\..\\DataFiles\\BayesianNetResults\\pairCountRankTrain2012Test2012.csv'
with open(pairCountRank) as pairCountRankFile:
	j=0
	for line in pairCountRankFile:
		if j>0:
			seperatedLine=line.split(', ')
			rankDict[seperatedLine[0].replace('\'', '')]=[]
		j+=1

titleText='Country-Pair'
trainTestOrderedPairs=glob.glob("..\..\\DataFiles\\BayesianNetResults\\pairCountRankTrain*Test*.csv")
for fileName in trainTestOrderedPairs:
	yearDict={}
	with open(fileName) as readDataFile:
		j=0
		for line in readDataFile:
			if j>0:
				seperatedLine=line.split(', ')
				yearDict[seperatedLine[0].replace('\'', '')]=seperatedLine[1:]
			j+=1
	for pair in rankDict.keys():
		if pair in yearDict.keys():
			rankDict[pair].append(yearDict[pair])
		else:
			rankDict[pair].append([0, 10000])
	titleText=titleText+','+fileName[-8:-4]+'-Count,Train'+fileName[-16:-12]+'-Test'+fileName[-8:-4]+'-Rank'

with open('..\..\\DataFiles\\BayesianNetResults\\allPairsCountRank.csv', 'w') as fileToWrite:
	fileToWrite.truncate()
	fileToWrite.write(titleText+'\n')
	for pair,dataList in rankDict.items():
		fileToWrite.write(pair+','+str(dataList).replace('[','').replace(']','').replace('\'','').replace('\\n','') + '\n')


