import csv
import fnmatch
import os
from collections import defaultdict
import io
from getBaseWord import getBase
import numpy as np
import pandas as pd
from io import StringIO

ID = "ID"
WORD = "Word"
LEMMA = "Lemma"
POS = "POS"
FEATURES = "Features"
PARENT = "Parent"
DEPENDENCY_LABELS = "Dependency Labels"
SRL = "SRL"

A0 = "A0"
A1= "A1"

def getAbsolutePath(fileType, directoryName):
    '''
    Create map between every file name without its extension and the absolute file path to the file
    :return: filePathDictionary
    '''
    filePathDictionary = defaultdict(int)
    for root, dirnames, filenames in os.walk(directoryName):
        for filename in fnmatch.filter(filenames, '*' + fileType):
            relativePath = os.path.join(root, filename)
            fullFilePath = os.path.abspath(relativePath)
            fileNameWithoutExtension = os.path.splitext(filename)[0].strip()
            filePathDictionary[fileNameWithoutExtension] = fullFilePath
    return filePathDictionary

def getAbsolutePathForSrlFiles(files, directoryName):
    '''
    Create map between file name and the absolute file path of every news file
    :return: absolute path
    '''
    filePathDictionary = defaultdict(int)
    for root, dirnames, filenames in os.walk(directoryName):
        for filename in fnmatch.filter(filenames, '*.srl'):
            fileNameWithoutExtension = os.path.splitext(filename)[0].strip()
            if fileNameWithoutExtension in files:
                relativePath = os.path.join(root, filename)
                fullFilePath = os.path.abspath(relativePath)
                filePathDictionary[fileNameWithoutExtension] = fullFilePath
    return filePathDictionary

def getFileNamesForVerb(target_verb):
    '''
    Get all the text news files that contain the given verb
    :param verb: the verb for which files need to be extracted
    :return: array of all the files  + .txt associated with the provided target_verb
    '''
    filePathDictionary = getAbsolutePath(".txt", "NewsTextFiles")
    mycsv = csv.reader(open("finalPredicates3cols.csv"))

    files = []

    for row in mycsv:
        #splits the csv file by the period delimeter to get the verb associated
        verb = row[1].split(".")[0].strip()
        fileName = row[len(row) - 1].strip()

        #checking that indeed the filename in the predicated.xls maps to an existing file in the newsFiles folder
        if fileName in filePathDictionary:
            if verb == target_verb:
                files.append(fileName + ".txt")
        else:
            print "'" + fileName + "' does not exist in the newsFiles folder"
            return -1
    return files

def hasChild(df, targetParentID):
    for index, row in df.iterrows():
        parentID = str(df.get_value(index, PARENT))
        if parentID == targetParentID: #a row's parent value is the ID of the agent we found
            return True
    return False

def getFullAgent(df, targetParentID):    
    '''
    given a certain node, returns a string of the agent and all its child nodes in order
    :return: String
    '''
    targetParentId = str(targetParentID)
    childNodeDictionary = {}
    dictionary = {}
    for index, row in df.iterrows():
        currentID = str(df.get_value(index, ID))
        if currentID == targetParentID: #a row's parent value is the ID of the agent we found
            targetWord = str(df.get_value(index, WORD))
            dictionary[int(targetParentID)] = targetWord
            childNodeDictionary = getChildNodes(df, targetParentID, dictionary)

    return getFullAgentFromChildNodes(childNodeDictionary)

def removeFirstWord(agent):
    agent.split(' ', 1)
    return agent.split(' ', 1)[1]

def getChildNodes(df, targetParentID, dictionary):   
    '''
    returns a dictionary of ID : word of all the child nodes of a certain node ID
    '''
    if hasChild(df, targetParentID):
        for index, row in df.iterrows():
            parentID = str(df.get_value(index, PARENT))
            currentID = str(df.get_value(index, ID))
            if parentID == targetParentID: #a row's parent value is the ID of the agent we found
                dictionary[int(currentID)] = str(df.get_value(index, WORD))
                dictionary.update(getChildNodes(df, currentID, dictionary))
        return dictionary
    else:
        return dictionary

def getFullAgentFromChildNodes(dictionary):
    '''
    given a dictionary of ID: word, sorts the dictionary on order of ID and returns a String of the entire agent with child nodes included
    :return: String
    '''
    sortedKeys = sorted(dictionary.keys())
    sortedValues = []
    for key in sortedKeys:
        sortedValues.append(dictionary[key])
    return " ".join(sortedValues)

def getValidDataFrameDictForTargetAction(targetAction) :
    files = getFileNamesForVerb(targetAction)

    fileAndSentToValidDF = {}
    dict = getAbsolutePathForSrlFiles(files, "ClearnlpOutput")

    for key in dict.keys():
        file = io.open(dict[key], "r", encoding='utf-8')
        srlSentenceChunks = file.read().split("\n\n")
        
        sentenceNumber = 0
        for chunk in srlSentenceChunks[:-1]:
            TESTDATA = StringIO(chunk)
            df = pd.read_table(TESTDATA, names=[ID,WORD,LEMMA,POS,FEATURES,PARENT,DEPENDENCY_LABELS,SRL])
            if targetAction in df[LEMMA].tolist():
                fileAndSent = key + "_Sent" + str(sentenceNumber)
                fileAndSentToValidDF[fileAndSent] = df
            sentenceNumber +=1

    return fileAndSentToValidDF

def main():

    main()