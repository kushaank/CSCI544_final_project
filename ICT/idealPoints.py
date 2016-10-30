import os, datetime, os.path, csv, sys

class TwoWayDict(dict):
	def __setitem__(self, key, value):
		if key in self:
			del self[key]
		if value in self:
			del self[value]
		dict.__setitem__(self, key, value)
		dict.__setitem__(self, value, key)
	def __delitem__(self, key):
		dict.__delitem__(self, self[key])
		dict.__delitem__(self, key)
	def __len__(self):
		return dict.__len__(self) // 2

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + datetime.timedelta(n)

classRangeSize=.5
os.chdir('..\..\\DataFiles\\Country Resolution Lists')
cowCode=TwoWayDict()
with open("states2011.csv") as f:
	mreader = csv.reader(f, delimiter=',')
	for row in mreader:
		cowCode[row[0]]=row[1]

idealPoints={}
with open("IdealPointDistances.txt") as f:
	mreader = csv.reader(f, delimiter='\t')
	for row in mreader:
		distanceValue=row[9]
		try:
			# classLabel='['+str(int(float(distanceValue)/classRangeSize)*classRangeSize)+'-'+str((int(float(distanceValue)/classRangeSize)*classRangeSize)+classRangeSize)+')'
			classLabel=int(float(distanceValue)/classRangeSize)*classRangeSize
			idealPoints[row[4]+'-'+row[5]+'-'+row[6]]=str(classLabel)
		except:
			pass
os.chdir('..')

for year in range(2006, 2013):
	os.chdir(str(year))
	with open('IdealPoints%s.raw' % year, 'w') as fileToWrite:
		fileToWrite.truncate()
		# fileToWrite.write("USA-CowCode-year , IdealPointDisBin\n")
		for key in sorted(idealPoints):
			if key[-4:]==str(year):
				try:
					idealPointKey=cowCode[key.split('-')[0]]+'-'+cowCode[key.split('-')[1]]+'-'+str(year)
					fileToWrite.write('\"'+idealPointKey+'\",'+idealPoints[key]+'\n')
				except:
					pass
	os.chdir('..')

