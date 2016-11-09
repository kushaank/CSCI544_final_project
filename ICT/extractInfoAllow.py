import extractUtils
import pandas as pd
from io import StringIO
import io
import col
import calendar
from collections import defaultdict
import os

def main():
    targetVerb = "allow"
    fileAndSentToValidDF = extractUtils.getValidDataFrameDictForTargetAction(targetVerb)

    evacuateCategories = ["A0", "Action", "A1", "Date/Time", "Location"]

    outputDictionary = {}
    for fileAndSent in fileAndSentToValidDF.keys():
        if fileAndSent == "newsText15497.txt_Sent10": #only because I want to see results of one file which is faster
            df = fileAndSentToValidDF[fileAndSent]
            
            resultsDictionary = {}
            for category in evacuateCategories:
                resultsDictionary[category] = None
            resultsDictionary["Action"] = targetVerb

            targetVerbRow =  df.loc[df[col.LEMMA] == targetVerb]
            targetVerbID = str(targetVerbRow[col.ID].iloc[0])

            #from Vietman, of China, in Serbia
            locationStartingWords = ["from", "of", "in"]

            #get arguments for the target word
            resultsDictionary = extractUtils.getArgumentsForGivenID(df, targetVerbID, resultsDictionary)

            for index, row in df.iterrows():
                # location
                if row[col.WORD] in locationStartingWords:
                    resultsDictionary = addLocationToDictionary(resultsDictionary, extractUtils.getFullAgent(df, str(row[col.ID])))
                # if "AM-LOC" in resultsDictionary:
                #     resultsDictionary["Location"] = resultsDictionary.pop('AM-LOC')
                #     #TODO: check if the corresponding AM-LOC has a geopolitical entity in it
                
                #date
                resultsDictionary = extractUtils.addDateToDictionary(row[col.WORD], resultsDictionary)
                
                if "A1" in resultsDictionary:
                    targetVerbID

            #removing the unnecessary categories from the dictionary that aren't revlevant to 'allow'
            for result in resultsDictionary.keys():
                if category not in evacuateCategories:
                    resultsDictionary.pop(category)
            outputDictionary[fileAndSent] = resultsDictionary
                
    print outputDictionary

main()