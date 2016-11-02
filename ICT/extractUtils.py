import csv
import fnmatch
import os
from collections import defaultdict
import io
from getBaseWord import getBase
import numpy as np
import pandas as pd
from io import StringIO

def getAbsolutePath(fileType, directoryName):
    '''
    Create map between file name and the absolute file path of every news file
    :return: absolute path
    '''
    filePathDictionary = defaultdict(int)
    for root, dirnames, filenames in os.walk(directoryName):
        for filename in fnmatch.filter(filenames, '*' + fileType):
            relativePath = os.path.join(root, filename)
            fullFilePath = os.path.abspath(relativePath)
            fileNameWithoutExtension = os.path.splitext(filename)[0].strip()
            filePathDictionary[fileNameWithoutExtension] = fullFilePath
    return filePathDictionary

def getAbsolutePathForTargetVerb(files, fileType, directoryName):
    '''
    Create map between file name and the absolute file path of every news file
    :return: absolute path
    '''
    filePathDictionary = defaultdict(int)
    for root, dirnames, filenames in os.walk(directoryName):
        for filename in fnmatch.filter(filenames, '*' + fileType):
            fileNameWithoutExtension = os.path.splitext(filename)[0].strip()
            if fileNameWithoutExtension in files:
                relativePath = os.path.join(root, filename)
                fullFilePath = os.path.abspath(relativePath)
                filePathDictionary[fileNameWithoutExtension] = fullFilePath
    return filePathDictionary

def getFileNamesForVerb(target_verb):
    '''
    Get all files associated with the given verb
    :param verb: the verb for which files need to be extracted
    :return: all the files associated with the verb
    '''
    filePathDictionary = getAbsolutePath(".txt", "NewsTextFiles")
    mycsv = csv.reader(open("finalPredicates3cols.csv"))

    files = []

    for row in mycsv:
        #splits the csv file by the period delimeter to get the verb associated
        verb = row[1].split(".")[0].strip()
        fileName = row[len(row) - 1].strip()
        if fileName in filePathDictionary:
            if verb == target_verb:
                files.append(fileName+".txt")
    return files

def main():
    files = getFileNamesForVerb("accuse")
    dict = getAbsolutePathForTargetVerb(files, ".srl", "ClearnlpOutput")

    sentences = []
    for key in dict.keys():
        file = io.open(dict[key], "r", encoding='utf-8')
        srlSentenceChunks = file.read().split("\n\n")

        for chunk in srlSentenceChunks[:-1]:
            TESTDATA = StringIO(chunk)
            df = pd.read_table(TESTDATA, names=["ID","Word","Lemma","POS","Features","Parent","Dependency Labels","SRL"])
            if "accuse" in df["Lemma"].tolist():
                sentences.append(df)

        break





main()


