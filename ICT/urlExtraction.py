import os,inspect, sys
dateDir= sys.argv[1]
os.chdir('..\..\DataFiles\\'+dateDir)
GdeltFile=dateDir.replace('\\', '')+'.export.CSV'
fileToWrite=open('URLs.txt', 'w')
uniqueUrls=[]
with open(GdeltFile) as newsFile:
	for line in newsFile:
		urlString=line.split("\t")[-1]
		if urlString not in uniqueUrls:
			uniqueUrls.append(urlString)
for urlString in uniqueUrls:
	fileToWrite.write(urlString)
fileToWrite.close()
# The following line sends the number of urls as the output of this file
sys.stdout.write(str(len(uniqueUrls)))