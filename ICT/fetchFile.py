import shutil, requests, sys, zipfile, os

os.chdir('..\..\DataFiles')
date = sys.argv[1]
dateDir= date.replace('-', '\\')
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
