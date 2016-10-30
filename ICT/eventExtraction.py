import os, datetime, os.path, csv
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
		idealPoints[row[4]+'-'+row[5]+'-'+row[6]]=row[9] # cowCode-year: ideal point
os.chdir('..')

for year in range(2006, 2013):
	yearlyRecords={}
	for date in daterange(datetime.date(year, 1, 1), datetime.date(year+1, 1, 1)):
		enteringDir=os.getcwd()
		fileDateName= str(date).replace('-', '\\')
		if os.path.exists(fileDateName):
			print 'Processing: '+ fileDateName
			os.chdir(fileDateName)
			GdeltFile=fileDateName.replace('\\', '')+'.export.CSV' if os.path.exists(fileDateName.replace('\\', '')+'.export.CSV') else fileDateName.replace('\\', '')[:-2]+'.csv'
			dailyRecords={}
			with open(GdeltFile) as newsFile:
				for line in newsFile:
					seperatedLine=line.split('\t')
					if seperatedLine[7]=='CZE':seperatedLine[7]='CZR'
					if seperatedLine[17]=='CZE': seperatedLine[17]='CZR'
					if seperatedLine[7]=='KOR':seperatedLine[7]='ROK'
					if seperatedLine[17]=='KOR': seperatedLine[17]='ROK'
					if seperatedLine[7]=='GBR':seperatedLine[7]='UKG'
					if seperatedLine[17]=='GBR': seperatedLine[17]='UKG'
					if (seperatedLine[7] in cowCode.keys()) and (seperatedLine[17] in cowCode.keys()):
						if (seperatedLine[7]=='USA' or seperatedLine[17]=='USA') and not(seperatedLine[7]=='USA' and seperatedLine[17]=='USA'):
							eventKey='\"'+seperatedLine[7]+'-'+seperatedLine[17]+'-'+str(year)+'\",\"'+seperatedLine[27]+'\"' if seperatedLine[7]=='USA' else '\"'+seperatedLine[17]+'-'+seperatedLine[7]+'-'+str(year)+'\",\"'+seperatedLine[27]+'\"'
							try:
								dailyRecords[eventKey]+=1
							except:
								dailyRecords[eventKey]=1
							try:
								yearlyRecords[eventKey]+=1
							except:
								yearlyRecords[eventKey]=1
			# for key in dailyRecords.keys():
			# 	pairValue=key.split(',')[0][1:-1]
			# 	idealPointKey=cowCode[pairValue.split('-')[0]]+'-'+cowCode[pairValue.split('-')[1]]+'-'+str(year)
			# 	try: 
			# 		dailyRecords[key]=[dailyRecords[key], idealPoints[idealPointKey]]
			# 	except:
			# 		dailyRecords[key]=[dailyRecords[key], '-1'] # -1 means we don't have the distance value
			# 	try: 
			# 		yearlyRecords[key]=[yearlyRecords[key], idealPoints[idealPointKey]]
			# 	except:
			# 		yearlyRecords[key]=[yearlyRecords[key], '-1'] # -1 means we don't have the distance value
			
			# with open('GdletActorsEvents%s.raw' % GdeltFile[:-4], 'w') as fileToWrite:
			# 	fileToWrite.truncate()
			# 	for key in sorted(dailyRecords):
			# 		fileToWrite.write(key+','+str(dailyRecords[key])+'\n')
					# fileToWrite.write(key+','+str(count[0])+','+str(count[1])+'\n')
			os.chdir(enteringDir)
	os.chdir(GdeltFile[:4])
	with open('GdletActorsEvents%s.counts' % GdeltFile[:4], 'w') as fileToWrite:
		fileToWrite.truncate()
		for key in sorted(yearlyRecords):
			fileToWrite.write(key+','+str(yearlyRecords[key])+'\n')
			# fileToWrite.write(key+','+str(count[0])+','+str(count[1])+'\n')
	os.chdir('..')












