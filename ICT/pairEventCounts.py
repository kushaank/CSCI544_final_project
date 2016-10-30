import os, sys, datetime, os.path, csv, operator, numpy as np
yearList=[2006,2007,2011,2012]
for year in yearList:
	currentCountFile='..\..\\DataFiles\\BayesianNetResults\\GdletEvents'+ str(year)+'Counts.csv'
	countPairs=[]
	with open(currentCountFile) as countsFile:
		i=0
		for line in countsFile:
			if i>0:
				seperatedLine=line.split(', ')
				countPairs.append(sum([int(countVal) for countVal in seperatedLine[:-1]]))
			i+=1
	with open('..\..\\DataFiles\\BayesianNetResults\\totalEventCount%d.csv' %year, 'w') as cToWrite:
		cToWrite.truncate()
		cToWrite.write(str(countPairs)[1:-1])