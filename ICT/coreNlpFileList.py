import os, glob, sys, zipfile
date = sys.argv[1]
numDivisions= int(sys.argv[2])
os.chdir('..\..\\DataFiles\\%s' %date)
print 'Unziping news files'
zipedFile=zipfile.ZipFile('NewsTextFiles.zip')
allFiles=zipfile.ZipFile.extractall(zipedFile)
zipedFile.close()
os.chdir('NewsTextFiles')
print 'Generating news file list'
for i in range(1,numDivisions+1):
	os.chdir('Part%d' %i)
	fileToWriteNames=open('stanfordNlpFileList.lst', 'w+')
	fileToWriteNames.truncate()
	allFileNames=glob.glob("newsText*.txt")
	for newsFileName in allFileNames:
		newsFileNamePath='..\..\..\DataFiles\\'+date+'\NewsTextFiles\Part'+str(i)+'\\'+newsFileName
		fileToWriteNames.write("%s\n" %newsFileNamePath)
	fileToWriteNames.close()
	os.chdir('..')
