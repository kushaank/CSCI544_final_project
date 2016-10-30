import os, inspect, sys, datetime

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + datetime.timedelta(n)

startDayStr=sys.argv[1]
startDay = datetime.date(int(startDayStr.split('\\')[0]), int(startDayStr.split('\\')[1]), int(startDayStr.split('\\')[2]))
sys.stdout.write(str((datetime.date.today()-startDay).days))