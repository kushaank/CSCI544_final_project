import os, inspect, sys, datetime

startDayStr=sys.argv[1]
startDay = datetime.date(int(startDayStr.split('\\')[0]), int(startDayStr.split('\\')[1]), int(startDayStr.split('\\')[2]))
daysToAdd=int(sys.argv[2])-1
wantedDate = startDay + datetime.timedelta(days=daysToAdd)
wantedDateStr= str(wantedDate).replace('-', '\\')

sys.stdout.write(wantedDateStr)