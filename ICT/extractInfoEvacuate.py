import extractUtils
import pandas as pd
from io import StringIO
import io
import calendar
from collections import defaultdict
import os

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

def addLocationToDictionary(resultsDictionary, location):
    if resultsDictionary["Location"] == None:
        resultsDictionary["Location"] = location
    else:
        resultsDictionary["Location"] = resultsDictionary.pop("Location")+ ", " + location
    return resultsDictionary

def main():
    targetVerb = "evacuate"
    fileAndSentToValidDF = extractUtils.getValidDataFrameDictForTargetAction(targetVerb)

    outputDictionary = {}
    for fileAndSent in fileAndSentToValidDF.keys():
        if fileAndSent == "newsText1234.txt_Sent13": #only because I want to see results of one file which is faster
            df = fileAndSentToValidDF[fileAndSent]
            resultsDictionary = {}
            resultsDictionary["Location"] = None
            resultsDictionary["A0"] = None
            resultsDictionary["A1"] = None
            resultsDictionary["date"] = None
            resultsDictionary["action"] = targetVerb

            #search for row which has the target verb
            targetVerbRow =  df.loc[df[LEMMA] == targetVerb]

            #grab the ID of that verb at that row
            targetVerbID = str(targetVerbRow[ID].iloc[0])

            #from Vietman, of China, in Serbia
            locationStartingWords = ["from", "of", "in"]

            for index, row in df.iterrows():
                wordValue = str(df.get_value(index, WORD))
                wordId = str(df.get_value(index, ID))

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

                    if relatedID == targetVerbID:  # our current row has an agent that corresponds to our target action
                        argumentNumber = argumentNumberFull.split("=")[0]  # just want to extract the 'A0' from 'A0=PAG'
                        agentID = str(df.get_value(index, ID))  # the ID of the row of the SRL with the agent

                        word = df.get_value(index, WORD)
                        resultsDictionary[argumentNumber] = word
                        resultsDictionary[argumentNumber] = extractUtils.getFullAgent(df, agentID)

                #extract location from SRL
                if "AM-LOC" in resultsDictionary:
                    resultsDictionary["Location"] = resultsDictionary.pop('AM-LOC')
                    #TODO: check if the corresponding AM-LOC has a geopolitical entity in it

                if row[WORD] in locationStartingWords:
                    resultsDictionary = addLocationToDictionary(resultsDictionary, extractUtils.getFullAgent(df, str(row[ID])))

                # see if the word corresponds to any day/month and if yes add it to the date/location param
                if row[WORD] in calendar.day_name:
                    resultsDictionary["Date/Time"] = row[WORD]

                if row[WORD] in calendar.month_name:
                    resultsDictionary["Date/Time"] = row[WORD]

                if row[WORD] in calendar.day_abbr:
                    resultsDictionary["Date/Time"] = row[WORD]

                if row[WORD] in calendar.month_abbr:
                    resultsDictionary["Date/Time"] = row[WORD]

            outputDictionary[fileAndSent] = resultsDictionary
                
    print outputDictionary

main()