import extractUtils
import pandas as pd
from io import StringIO
import io
import col
import calendar

def main():
    targetVerb = "suspend"
    files = extractUtils.getFileNamesForVerb(targetVerb)
    dict = extractUtils.getAbsolutePathForSrlFiles(files, "ClearnlpOutput")

    fileAndSentToValidDF = extractUtils.getValidDataFrameDictForTargetAction(targetVerb)

    outputDictionary = {}
    for fileAndSent in fileAndSentToValidDF.keys():
        if fileAndSent == "newsText720.txt_Sent0": #only because I want to see results of one file which is faster
            df = fileAndSentToValidDF[fileAndSent]
            resultsDictionary = {}
            resultsDictionary["action"] = targetVerb
            # search for row which has the target verb
            targetVerbRow = df.loc[df[col.LEMMA] == targetVerb]

            # grab the ID of that verb at that row
            targetVerbID = str(targetVerbRow[col.ID].iloc[0])

            resultsDictionary = extractUtils.getArgumentsForGivenID(df, targetVerbID, resultsDictionary)

            # look at the SRL column in this chunk to see which row has the target verb identification as an argument
            for index, row in df.iterrows():
                #extract reason from SRL
                if "AM-CAU" in resultsDictionary:
                    resultsDictionary["Reason"] = resultsDictionary.pop('AM-CAU')

                #extract location from SRL
                if "AM-DIS" in resultsDictionary:
                    resultsDictionary["Location"] = resultsDictionary.pop('AM-DIS')
                
                # see if the word corresponds to any day/month and if yes add it to the date/location param
                        # see if the word corresponds to any day/month and if yes add it to the date/location param
                resultsDictionary = extractUtils.addDateToDictionary(row[col.WORD], resultsDictionary)

            outputDictionary[fileAndSent] = resultsDictionary

    print outputDictionary


main()

