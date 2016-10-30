import shutil, sys, zipfile, os, datetime, time
from os import listdir
from os.path import isfile, join

# def daterange(start_date, end_date):
# 	for n in range(int ((end_date - start_date).days)):
# 		yield start_date + datetime.timedelta(n)

def zipFile(date):
	enteringDir=os.getcwd()
	dateDir= date.replace('-', '\\')
	start_time = time.time()
	print 'zipping the files for:'+dateDir
	os.chdir(dateDir)
	listDirectories=[item for item in os.listdir('.') if not isfile(item)]
	for directoryName in listDirectories:
		zf = zipfile.ZipFile(directoryName+".zip", "w", zipfile.ZIP_DEFLATED)
		# print directoryName
		for dirname, subdirs, files in os.walk(directoryName):
			zf.write(dirname)
			for filename in files:
				zf.write(os.path.join(dirname, filename))
		zf.close()
		shutil.rmtree(directoryName) 
	elapsed_time = time.time() - start_time
	print elapsed_time
	os.chdir(enteringDir)

os.chdir('..\..\DataFiles')
# for date in daterange(datetime.date(2013, 8, 1), datetime.date(2013, 10, 1)): #datetime.date.today()):
date = sys.argv[1]
zipFile(date)