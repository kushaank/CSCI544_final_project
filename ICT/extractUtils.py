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
    childNodeDictionary = {}
    dictionary = {}
    for index, row in df.iterrows():
        currentID = str(df.get_value(index, ID))
        if currentID == targetParentID: #a row's parent value is the ID of the agent we found
            print currentID
            targetWord = str(df.get_value(index, WORD))
            dictionary[targetParentID] = targetWord
            childNodeDictionary = getChildNodes(df, targetParentID, dictionary)

    return getFullAgentFromChildNodes(childNodeDictionary)

def getChildNodes(df, targetParentID, dictionary):   
    '''
    returns a dictionary of ID : word of all the child nodes of a certain node ID
    '''
    if hasChild(df, targetParentID):
        for index, row in df.iterrows():
            parentID = str(df.get_value(index, PARENT))
            currentID = str(df.get_value(index, ID))
            if parentID == targetParentID: #a row's parent value is the ID of the agent we found
                dictionary[currentID] = str(df.get_value(index, WORD))
                dictionary.update(getChildNodes(df, currentID, dictionary))
        return dictionary
    else:
        print dictionary
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

def main():
    targetVerb = "evacuate"
    files = getFileNamesForVerb(targetVerb)
    dict = getAbsolutePathForSrlFiles(files, "ClearnlpOutput")

    sentences = []
    for key in dict.keys():
        file = io.open("/Users/eamonb/Documents/CS544/Projects/group project/CSCI544_final_project/ICT/ClearnlpOutput/ClearnlpOutput/Part30/newsText17789.txt.srl", "r", encoding='utf-8')
        srlSentenceChunks = file.read().split("\n\n")

        for chunk in srlSentenceChunks[:-1]:
            TESTDATA = StringIO(chunk)
            df = pd.read_table(TESTDATA, names=[ID,WORD,LEMMA,POS,FEATURES,PARENT,DEPENDENCY_LABELS,SRL])
            if targetVerb in df[LEMMA].tolist():
                sentences.append(df)
            break
        break
    
    resultsDictionary = {}
    resultsDictionary["action"] = targetVerb
    #search for row which has the target verb
    targetVerbRow =  df.loc[df[LEMMA] == targetVerb]

    #grab the ID of that verb at that row
    targetVerbID = str(targetVerbRow[ID].iloc[0])
    # dict = {"9":"nationals"}
    # print getFullAgentFromChildNodes(getChildrenNodes(df, "9", dict))

    # print df

    for index, row in df.iterrows():
        srl = df.get_value(index, SRL)
        twoOrMoreSRLArguments = str(srl).split(";") #3:A0=PAG;11:A0=PAG two or more arguments are separated by semicolon
        oneSRLArgument = str(srl).split(":") #28:A0=PAG one argument separates relatedID and argument with colon
        validSRLs = []
        if len(twoOrMoreSRLArguments) > 1: #there are two or more arguments
            validSRLs = twoOrMoreSRLArguments
        elif len(oneSRLArgument) > 1: #one argument
            validSRLs.append(srl)

        for srlSection in validSRLs: #["3:A0=PAG", "11:A0=PAG"]
            argumentSplit = srlSection.split(":")
            relatedID = str(argumentSplit[0]) #3
            argumentNumberFull = argumentSplit[1] #'A0=PAG'

            if relatedID == targetVerbID: #our current row has an agent that corresponds to our target action
                argumentNumber = argumentNumberFull.split("=")[0] # just want to extract the 'A0' from 'A0=PAG'
                agentID = str(df.get_value(index, ID))  #the ID of the row of the SRL with the agent
                agentWord = str(df.get_value(index, WORD))
                
                resultsDictionary[argumentNumber] = getFullAgent(df, agentID)
                
    print df
    print resultsDictionary

main()


