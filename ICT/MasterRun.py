import shutil, requests, sys, zipfile, os, datetime, subprocess, time
from os import listdir
from os.path import isfile, join

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + datetime.timedelta(n)

os.chdir('..\..\DataFiles')
for date in daterange(datetime.date(2013, 4, 6), datetime.date.today()):
	print date
	start_time = time.time()
	enteringDir=os.getcwd()
	dateDir= str(date).replace('-', '\\')
	GdeltFile=dateDir.replace('\\', '')+'.export.CSV.zip'
	if not os.path.exists(dateDir+'\\'+GdeltFile[:-4]):
		if not os.path.exists(dateDir):
			os.mkdir(dateDir)
		os.chdir(dateDir)
		print 'Downloading: '+ GdeltFile
		url = 'http://data.gdeltproject.org/events/'+GdeltFile
		response = requests.get(url, stream=True)
		with open(GdeltFile, 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)
		zipGdeltFile=zipfile.ZipFile(GdeltFile)
		csvFile=zipfile.ZipFile.extract(zipGdeltFile, GdeltFile[:-4])
		zipGdeltFile.close()
		os.remove(GdeltFile)
		os.chdir('..\..\..')
	os.chdir('..\\Programs\\eclipseLuna\\workspace\\PredicateExtraction')
	subprocess.call(['java', '-cp', 'bin\\ArticleExtraction7.0.jar', '-XX:+UseConcMarkSweepGC', '-Xmx10g', 'GdeltPredicateExtraction', dateDir])
	os.chdir('..\..\..\..\\DataFiles\\'+dateDir)
	print 'Compressing the data folders ...'
	listDirectories=[item for item in os.listdir('.') if not isfile(item)]
	if len(listDirectories)>=3:
		for directoryName in listDirectories:
			zf = zipfile.ZipFile(directoryName+".zip", "w", zipfile.ZIP_DEFLATED)
			for dirname, subdirs, files in os.walk(directoryName):
				zf.write(dirname)
				for filename in files:
					zf.write(os.path.join(dirname, filename))
			zf.close()
			shutil.rmtree(directoryName) 
	os.chdir(enteringDir)
	elapsed_time = time.time() - start_time
	print 'Time for '+str(date)+' is '+ str(round(elapsed_time/60,2))+ 'mins ('+str(round(elapsed_time/3600,2))+' hours)!\n\n'
