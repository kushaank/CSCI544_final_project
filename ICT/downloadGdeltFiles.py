import shutil, requests, sys, zipfile, os, datetime

# def daterange(start_date, end_date):
# 	for n in range(int ((end_date - start_date).days)):
# 		yield start_date + datetime.timedelta(n)

# os.chdir('..\..\DataFiles')
# for date in daterange(datetime.date(2014, 3, 20), datetime.date.today()):
# 	dateDir= str(date).replace('-', '\\')
# 	GdeltFile=dateDir.replace('\\', '')+'.export.CSV.zip'
# 	if not os.path.exists(dateDir+'\\'+GdeltFile[:-4]):
# 		if not os.path.exists(dateDir):
# 			os.mkdir(dateDir)
# 		os.chdir(dateDir)
# 		print 'Downloading: '+ GdeltFile
# 		url = 'http://data.gdeltproject.org/events/'+GdeltFile
# 		response = requests.get(url, stream=True)
# 		with open(GdeltFile, 'wb') as out_file:
# 			shutil.copyfileobj(response.raw, out_file)
# 		zipGdeltFile=zipfile.ZipFile(GdeltFile)
# 		csvFile=zipfile.ZipFile.extract(zipGdeltFile, GdeltFile[:-4])
# 		zipGdeltFile.close()
# 		os.remove(GdeltFile)
# 		os.chdir('..\..\..')


os.chdir('..\..\DataFiles')
for year in range(2013, 2014):
	if not os.path.exists(str(year)):
		os.mkdir(str(year))
	os.chdir(str(year))
	for month in range(1, 13):
		if month <10:
			os.mkdir('0'+str(month))
			os.chdir('0'+str(month))
			GdeltFile=str(year)+'0'+str(month)+'.zip'
		else:
			os.mkdir(str(month))
			os.chdir(str(month))
			GdeltFile=str(year)+str(month)+'.zip'
		os.mkdir('01')
		os.chdir('01')
		print 'Downloading: '+ GdeltFile
		url = 'http://data.gdeltproject.org/events/'+GdeltFile
		response = requests.get(url, stream=True)
		with open(GdeltFile, 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)
		zipGdeltFile=zipfile.ZipFile(GdeltFile)
		csvFile=zipfile.ZipFile.extract(zipGdeltFile, GdeltFile[:-3]+'csv')
		zipGdeltFile.close()
		os.remove(GdeltFile)
		os.chdir('..\..')
	os.chdir('..')