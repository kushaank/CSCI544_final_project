import csv
import sys
import os
import fnmatch
from collections import defaultdict


filePathDictionary = defaultdict(int)

for root, dirnames, filenames in os.walk("NewsTextFiles"):
    for filename in fnmatch.filter(filenames, '*.txt'):
        #get the full file path
        relativePath = os.path.join(root, filename)
        fullFilePath = os.path.abspath(relativePath)
        fileNameWithoutExtension = os.path.splitext(filename)[0].strip()
        filePathDictionary[fileNameWithoutExtension] = fullFilePath

mycsv = csv.reader(open("finalPredicates3cols.csv"))
for row in mycsv:
    verb = row[1].split(".")[0].strip()
    fileName = row[len(row)-1].strip()
    if fileName in filePathDictionary:
        if verb == "claim":
            print("YES")
        

# print(allFiles)