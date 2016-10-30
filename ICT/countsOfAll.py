import re, os, glob, sys

fileDateList=['2014\\05\\19','2014\\05\\20','2014\\05\\21','2014\\05\\22','2014\\05\\23','2014\\05\\24','2014\\05\\25','2014\\05\\26','2014\\05\\27','2014\\05\\28','2014\\05\\29','2014\\05\\30','2014\\05\\31','2014\\06\\01','2014\\06\\02','2014\\06\\03','2014\\06\\04','2014\\06\\05','2014\\06\\06','2014\\06\\07','2014\\06\\08','2014\\06\\09','2014\\06\\10','2014\\06\\11','2014\\06\\12','2014\\06\\13','2014\\06\\14','2014\\06\\15','2014\\06\\16','2014\\06\\17','2014\\06\\08','2014\\06\\19']

predicatesCount=0
bothPredicatesCount=0
newsTextCount=0
os.chdir('..\\..\\DataFiles')
for fileDateName in fileDateList: 
	print fileDateName
	os.chdir(fileDateName+'\\NewsTextFiles')
	partList=glob.glob("Part*")
	for part in partList:
		os.chdir(part)
		newsTextCount+=len(glob.glob("newsText*.txt"))
		os.chdir('..')
	os.chdir('..')

	os.chdir('Predicates')
	for part in partList:
		os.chdir(part)
		predicatesFilesList=glob.glob("newsText*Predicates.csv")
		for predicatesFile in predicatesFilesList:
			with open (predicatesFile) as f:
				predicatesCount+=len(f.readlines())-1
		with open ('allPredicates3cols.csv') as f1:
			bothPredicatesCount+=len(f1.readlines())-1
		os.chdir('..')
	print '\n predicatesCount: '+str(predicatesCount)
	os.chdir('..\..\..\..')

print '\n newsTextCount: '+str(newsTextCount)
print '\n predicatesCount: '+str(predicatesCount)
print '\n bothPredicatesCount: '+str(bothPredicatesCount)