import csv, os, glob,inspect, sys
numDivisions= int(sys.argv[1])
fileDateName=sys.argv[2]
os.chdir('..\..\DataFiles\\'+fileDateName+'\Predicates')
finalPredicatesList=[]
finalPredicates3cols=[]
for i in range(1, numDivisions+1):
	os.chdir('Part%d' % i)
	with open("allFilesFinalPredicatesBoth.csv") as f:
		finalPredicatesList = finalPredicatesList+f.readlines()
	with open("allPredicates3cols.csv") as f3c:
		finalPredicates3cols = finalPredicates3cols+f3c.readlines()
	os.chdir('..')
finalPredicatesList.sort()
finalPredicates3cols.sort()
extraTitle="'actor0', 'A0', 'Verb', 'A1', 'A2', 'Polarity', 'Sentence', 'actor1', 'File Name', 'Date'\n"
extraTitle3cols='actor1, Verb, actor2, sentence, file, date\n'
while extraTitle in finalPredicatesList: finalPredicatesList.remove(extraTitle)
while extraTitle3cols in finalPredicates3cols: finalPredicates3cols.remove(extraTitle3cols)
os.chdir('..')
with open('finalPredicatesList.csv', 'w+') as f: 
	f.write("'actor0', 'A0', 'Verb', 'A1', 'A2', 'Polarity', 'Sentence', 'actor1', 'File Name', 'Date'\n")
	for predicate in finalPredicatesList:
		f.write(predicate)
with open('finalPredicates3cols.csv', 'w+') as f3c: 
	f3c.write('actor1, Verb, actor2, sentence, file, date\n')
	for predicate in finalPredicates3cols:
		f3c.write(predicate)