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

def main():
    targetVerb = "allow"
    fileAndSentToValidDF = extractUtils.getValidDataFrameDictForTargetAction(targetVerb)

    evacuateCategories = ["A0", "Action", "A1", "Date/Time", "Location"]

    outputDictionary = {}
    for fileAndSent in fileAndSentToValidDF.keys():
        if fileAndSent == "newsText15497.txt_Sent12": #only because I want to see results of one file which is faster
            df = fileAndSentToValidDF[fileAndSent]
            
            resultsDictionary = {}
            for category in evacuateCategories:
                resultsDictionary[category] = None
            resultsDictionary["Action"] = targetVerb

            targetVerbRow =  df.loc[df[LEMMA] == targetVerb]
            targetVerbID = str(targetVerbRow[ID].iloc[0])

            #from Vietman, of China, in Serbia
            locationStartingWords = ["from", "of", "in"]

            #get all SRL for the row
            resultsDictionary = extractUtils.getArgumentsForGivenID(df, targetVerbID, resultsDictionary)

            for index, row in df.iterrows():
                # location
                if row[WORD] in locationStartingWords:
                    resultsDictionary = addLocationToDictionary(resultsDictionary, extractUtils.getFullAgent(df, str(row[ID])))
                # if "AM-LOC" in resultsDictionary:
                #     resultsDictionary["Location"] = resultsDictionary.pop('AM-LOC')
                #     #TODO: check if the corresponding AM-LOC has a geopolitical entity in it
                
                #date
                if row[WORD] in calendar.day_name:
                    resultsDictionary["Date/Time"] = row[WORD]

                if row[WORD] in calendar.month_name:
                    resultsDictionary["Date/Time"] = row[WORD]

                if row[WORD] in calendar.day_abbr:
                    resultsDictionary["Date/Time"] = row[WORD]

                if row[WORD] in calendar.month_abbr:
                    resultsDictionary["Date/Time"] = row[WORD]
                
                if "A1" in resultsDictionary:
                    targetVerbID

            for result in resultsDictionary.keys():
                if category not in evacuateCategories:
                    resultsDictionary.pop(category)
            outputDictionary[fileAndSent] = resultsDictionary
                
    print outputDictionary

main()