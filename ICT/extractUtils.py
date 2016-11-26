import csv
import fnmatch
import os
import col
from collections import defaultdict
import io
import calendar
from getBaseWord import getBase
import numpy as np
import pandas as pd
from io import StringIO
from dateutil.parser import parse
import re

def createSetFromFile(fileName):
    geopoliticalList = set()
    with open(fileName, 'r') as myfile:
        word = myfile.read()
        word = word.rstrip()
        wordArray = re.split('\t|\n|\r', word)
        #this line has more than one word in it so add each word into the set
        if len(wordArray) > 1:
            for subWord in wordArray:
                geopoliticalList.add(subWord.lower())
        else:
            geopoliticalList.add(word.lower())
    return geopoliticalList
    
def getCapitalsList():
    return createSetFromFile("GeopoliticalList/country_capital.txt")
        
def getHeadOfStateList():
    return createSetFromFile("GeopoliticalList/country_headOfState.txt")

def getNationalityList():
    return createSetFromFile("GeopoliticalList/country_nationality.txt")

#pass in any of the three lists (capitals list, nationalities list, or head of state list)
#test to see if the given phrase contains a word that is in the geopolitical list
def isValidGeopoliticalAgent(phrase, geopoliticalList) :
    phraseArray = phrase.split(" ")
    for word in phraseArray:
        subWord = ""
        for char in word:
            subWord += char.lower()
            if subWord in geopoliticalList:
                return True
    return False

def isInfinitive(agentID, df):
    if agentID == None:
        return False
    #The current word is at the df index int(agentID)-1
    #so we want to check that the previous word is "to" to make sure it is an infinitive
    if str(df.iloc[int(agentID)-2][col.WORD]) == "to":
        return True
    else:
        return False    

def getInfinitiveAgent(agentID, df):
    return str(df.iloc[int(agentID)-2][col.WORD]) + " " + str(df.iloc[int(agentID)-1][col.WORD])

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
        parentID = str(df.get_value(index, col.PARENT))
        if parentID == targetParentID: #a row's parent value is the ID of the agent we found
            return True
    return False

def getImmediateChildrenForAgent(df, targetParentID):
    immediateChildrenList = []
    lastMatchingParentIndex = 0
    for index, row in df.iterrows():
        if str(row[col.PARENT]) == targetParentID:
            immediateChildrenList.append(index + 1)
    return immediateChildrenList

#key is ID value is actual word
def getFullAgentDictionary(df, targetParentID):
    parents = []
    visited = []
    parents.append(str(targetParentID))
    fullAgent = {}
    while len(parents)>0:
        parent = parents[0]
        visited.append(str(parent))
        for index, row in df.iterrows():
            parentID = str(df.get_value(index, col.PARENT))
            currentID = str(df.get_value(index, col.ID))
            if str(parentID)==str(parent):
                if currentID not in visited:
                    parents.append(currentID)
                fullAgent[df.get_value(index,col.ID)] = df.get_value(index, col.WORD)

        parents.remove(parent)
    fullAgent[df.loc[df[col.ID] == int(targetParentID), col.ID].item()]= df.loc[df[col.ID] == int(targetParentID), col.WORD].item()
    return fullAgent

def getFullAgent(df, targetParentID):    
    fullAgent = getFullAgentDictionary(df, targetParentID)
    sortedKeys = sorted(fullAgent.keys())
    sortedValues = []
    for key in sortedKeys:
        sortedValues.append(fullAgent[key])
    return " ".join(sortedValues)

def removeFirstWord(agent):
    agent.split(' ', 1)
    return agent.split(' ', 1)[1]

def getChildNodes(df, targetParentID, dictionary):   
    '''
    returns a dictionary of ID : word of all the child nodes of a certain node ID
    '''
    if hasChild(df, targetParentID):
        for index, row in df.iterrows():
            parentID = str(df.get_value(index, col.PARENT))
            currentID = str(df.get_value(index, col.ID))
            if parentID == targetParentID: #a row's parent value is the ID of the agent we found
                dictionary[int(currentID)] = str(df.get_value(index, col.WORD))
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
            df = pd.read_table(TESTDATA, names=[col.ID,col.WORD,col.LEMMA,col.POS,col.FEATURES,col.PARENT,col.DEPENDENCY_LABELS,col.SRL])
            if targetAction in df[col.LEMMA].tolist():
                fileAndSent = key + "_Sent" + str(sentenceNumber)
                fileAndSentToValidDF[fileAndSent] = df
            sentenceNumber +=1

    return fileAndSentToValidDF

def getValidSRLsFromSRL(srl):
    twoOrMoreSRLArguments = str(srl).split(";") #3:A0=PAG;11:A0=PAG two or more arguments are separated by semicolon
    oneSRLArgument = str(srl).split(":") #28:A0=PAG one argument separates relatedID and argument with colon
    validSRLs = []
    if len(twoOrMoreSRLArguments) > 1: #there are two or more arguments
        validSRLs = twoOrMoreSRLArguments 
    elif len(oneSRLArgument) > 1: #one argument
        validSRLs.append(srl)
    return validSRLs

#returns the arguments (strings) for given ID
def getArgumentsForGivenID(df, targetVerbID, resultsDictionary):
    resultsDictionaryCopy = resultsDictionary.copy()
    for index, row in df.iterrows():
        srl = df.get_value(index, col.SRL)
        validSRLs = getValidSRLsFromSRL(srl)

        for srlSection in validSRLs: #["3:A0=PAG", "11:A0=PAG"]
            argumentSplit = srlSection.split(":")
            relatedID = str(argumentSplit[0]) #3
            argumentNumberFull = argumentSplit[1] #'A0=PAG'

            #getting all the arguments that correspond to the target Verb
            if relatedID == targetVerbID:  # our current row has an agent that corresponds to our target action
                argumentNumber = argumentNumberFull.split("=")[0]  # just want to extract the 'A0' from 'A0=PAG'
                agentID = str(df.get_value(index, col.ID))  # the ID of the row of the SRL with the agent

                resultsDictionaryCopy[argumentNumber] = getFullAgent(df, agentID)#Grab agent 0 or agent 1
    return resultsDictionaryCopy

#returns a list of agents that contain the given SRL tag in the sentence
def getAllAgentsWithGivenSRL(df, desiredSrl):
    agentList = []
    for index, row in df.iterrows():
        srl = df.get_value(index, col.SRL)
        validSRLs = getValidSRLsFromSRL(srl)

        for srlSection in validSRLs: #["3:A0=PAG", "11:A0=PAG"]
            argumentSplit = srlSection.split(":")
            relatedID = str(argumentSplit[0]) #3
            argumentNumberFull = argumentSplit[1] #'A0=PAG'

            argumentNumber = argumentNumberFull.split("=")[0]  # just want to extract the 'A0' from 'A0=PAG'
            if desiredSrl == argumentNumber:
                agentID = str(df.get_value(index, col.ID))  # the ID of the row of the SRL with the agent
                agentList.append(getFullAgent(df, agentID))
    return agentList

#returns the actual ID of agent1 and agent 2 for the given ID (if any)
def getArgumentIDsForGivenID(df, targetVerbID, resultsDictionary):
    resultsDictionaryCopy = resultsDictionary.copy()
    for index, row in df.iterrows():
        srl = df.get_value(index, col.SRL)
        validSRLs = getValidSRLsFromSRL(srl)

        for srlSection in validSRLs: #["3:A0=PAG", "11:A0=PAG"]
            argumentSplit = srlSection.split(":")
            relatedID = str(argumentSplit[0]) #3
            argumentNumberFull = argumentSplit[1] #'A0=PAG'

            #getting all the arguments that correspond to the target Verb
            if relatedID == targetVerbID:  # our current row has an agent that corresponds to our target action
                argumentNumber = argumentNumberFull.split("=")[0]  # just want to extract the 'A0' from 'A0=PAG'
                agentID = str(df.get_value(index, col.ID))  # the ID of the row of the SRL with the agent

                resultsDictionaryCopy[argumentNumber] = agentID#Grab agent 0 or agent 1
    return resultsDictionaryCopy

#returns the actual ID of agent1 and agent 2 for the given ID (if any)
#TODO: replace other functions with this function which doesn't use the dictionary unnecesarily'
def getArgumentIDsForGivenIDTEST(df, targetVerbID):
    resultsDictionary = {}
    for index, row in df.iterrows():
        srl = df.get_value(index, col.SRL)
        validSRLs = getValidSRLsFromSRL(srl)

        for srlSection in validSRLs: #["3:A0=PAG", "11:A0=PAG"]
            argumentSplit = srlSection.split(":")
            relatedID = str(argumentSplit[0]) #3
            argumentNumberFull = argumentSplit[1] #'A0=PAG'

            #getting all the arguments that correspond to the target Verb
            if relatedID == targetVerbID:  # our current row has an agent that corresponds to our target action
                argumentNumber = argumentNumberFull.split("=")[0]  # just want to extract the 'A0' from 'A0=PAG'
                agentID = str(df.get_value(index, col.ID))  # the ID of the row of the SRL with the agent

                resultsDictionary[argumentNumber] = agentID#Grab agent 0 or agent 1
    return resultsDictionary

def addLocationToDictionary(resultsDictionary, location):
    if resultsDictionary["Location"] == None:
        resultsDictionary["Location"] = location
    else:
        resultsDictionary["Location"] = resultsDictionary.pop("Location")+ ", " + location
    return resultsDictionary

#DANGEROUS, for some reason giving a lot of false positives. considers comma and - as valid dates
def is_date(string):
    try: 
        parse(string)
        return True
    except ValueError:
        return False

def valid_year(year):
    if year and year.isdigit():
        if int(year) >=1700 and int(year) <=2020:
            return True
    return False

def valid_date(word):
    if word in calendar.day_name or word in calendar.month_name or word in calendar.day_abbr or word in calendar.month_abbr or valid_year(word):
        return True
    return False

def addDateToDictionary(word, resultsDictionary):
    if valid_date(word):
        resultsDictionary["Date/Time"] = word
    return resultsDictionary

def main():

    main()