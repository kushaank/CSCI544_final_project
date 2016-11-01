import csv
import fnmatch
import os
from collections import defaultdict
import nltk.data

filePathDictionary = defaultdict(int)

for root, dirnames, filenames in os.walk("NewsTextFiles"):
    for filename in fnmatch.filter(filenames, '*.txt'):
        # get the full file path
        relativePath = os.path.join(root, filename)
        fullFilePath = os.path.abspath(relativePath)
        fileNameWithoutExtension = os.path.splitext(filename)[0].strip()
        filePathDictionary[fileNameWithoutExtension] = fullFilePath

mycsv = csv.reader(open("finalPredicates3cols.csv"))
for row in mycsv:
    verb = row[1].split(".")[0].strip()
    fileName = row[len(row) - 1].strip()
    if fileName in filePathDictionary:
        if verb == "claim":
            i=1

text = "my name is eamon. hello how are you"
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
delimeter = '\n-----\n'
sentenceWithDelimeters = delimeter.join(sent_detector.tokenize(text.strip()))
sentences = sentenceWithDelimeters.split(delimeter)
for sentence in sentences:
    print(sentence)