import extractUtils
import pandas as pd
from io import StringIO
import io
import col
import calendar
from collections import defaultdict
import os

def main():
    capitalsList = extractUtils.getCapitalsList()
    targetVerb = "allow"
    fileAndSentToValidDF = extractUtils.getValidDataFrameDictForTargetAction(targetVerb)
    
    evacuateCategories = ["A0", "Action", "A1", "Allowed Action", "Object", "Reason", "Date/Time", "Location"]

    outputDictionary = {}
    for fileAndSent in fileAndSentToValidDF.keys():
        if fileAndSent == "newsText13647.txt_Sent18": #only because I want to see results of one file which is faster
            df = fileAndSentToValidDF[fileAndSent]

            resultsDictionary = {}
            for category in evacuateCategories:
                resultsDictionary[category] = None
            resultsDictionary["Action"] = targetVerb

            targetVerbRow =  df.loc[df[col.LEMMA] == targetVerb]
            targetVerbID = str(targetVerbRow[col.ID].iloc[0])

            #from Vietman, of China, in Serbia
            locationStartingWords = ["in", "to", "from", "into"]

            #get arguments for the target word
            resultsDictionary = extractUtils.getArgumentsForGivenID(df, targetVerbID, resultsDictionary)

            for index, row in df.iterrows():
                # location
                if row[col.WORD] in locationStartingWords:
                    locationID = str(row[col.ID])
                    locationPhrase = extractUtils.getFullAgent(df, locationID)
                    if extractUtils.isValidGeopoliticalAgent(locationPhrase, capitalsList):
                        resultsDictionary = extractUtils.addLocationToDictionary(resultsDictionary, locationPhrase)
                
                #only add the location if its 
                if "AM-LOC" in resultsDictionary:
                    potentialLocation = resultsDictionary.pop('AM-LOC')
                    if extractUtils.isValidGeopoliticalAgent(potentialLocation, capitalsList):
                        resultsDictionary = extractUtils.addLocationToDictionary(resultsDictionary, potentialLocation)

                #date
                resultsDictionary = extractUtils.addDateToDictionary(row[col.WORD], resultsDictionary)
            
            #if there is a a1 for 'allow' and it is an infinitive
            argument1ID = extractUtils.getArgumentIDsForGivenID(df, targetVerbID, resultsDictionary).get("A1")
            if "A1" in resultsDictionary.keys() and extractUtils.isInfinitive(argument1ID, df):
                #the argument1 of "allow" is typically an infinitive which represents the "allowed action"
                resultsDictionary["Allowed Action"] = extractUtils.getInfinitiveAgent(argument1ID, df)

                #the argument0 of the "allowed action" is typically the agent1 for the sentences with "allow"
                agent2ID = extractUtils.getArgumentIDsForGivenID(df, argument1ID, resultsDictionary)["A0"]
                resultsDictionary["A1"] = extractUtils.getFullAgent(df, agent2ID)
            
            #removing the unnecessary categories from the dictionary that aren't revlevant to 'evacuate'
            for result in resultsDictionary.keys():
                if result not in evacuateCategories:
                    resultsDictionary.pop(result)
            outputDictionary[fileAndSent] = resultsDictionary

    print outputDictionary

main()