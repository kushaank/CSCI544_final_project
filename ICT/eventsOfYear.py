import os, sys, datetime, os.path, csv, numpy as np
os.chdir('..\..\\DataFiles')
allCommonNodes=[]
for year in range(2006, 2013):
	nodes=[]
	with open("BayesianNetResults\\eventsOfYear%d.csv" %year) as f:
		allCommonNodes=allCommonNodes+[line[2:-2] for line in f if len(line)>4]
allCommonNodes=list(set(allCommonNodes))
print len(allCommonNodes)
with open('Country Resolution Lists\\nonEmptyEvents.csv', 'w') as fileToWrite:
	fileToWrite.truncate()
	for node in sorted(allCommonNodes)[:-1]:
		fileToWrite.write('\''+node+'\''+'\n')
os.chdir('..\..\Programs\Python')