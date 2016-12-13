import extractUtils
import col

def main():
    targetVerb = "evacuate"
    fileAndSentToValidDF = extractUtils.getValidDataFrameDictForTargetAction(targetVerb, "finalPredicates3cols.csv", "ClearnlpOutput")

    evacuateContextTags = ["A0", "Probable Action", "Improbable Action", "A1", "Date/Time", "Location", "Reason"]
    
    outputDictionary = {}
    for fileAndSent in fileAndSentToValidDF.keys():
        df = fileAndSentToValidDF[fileAndSent]
        
        resultsDictionary = {}
        for contextTag in evacuateContextTags:
            resultsDictionary[contextTag] = None

        targetVerbRow = df.loc[df[col.LEMMA] == targetVerb]
        targetVerbID = str(targetVerbRow[col.ID].iloc[0])

        if extractUtils.isNegatedVerb(df, targetVerbID):
            resultsDictionary["Improbable Action"] = targetVerb
        else:
            resultsDictionary["Probable Action"] = targetVerb

        #from Vietman, of China, in Serbia
        locationStartingWords = ["from", "of", "in"]

        resultsDictionary = extractUtils.getArgumentsForGivenID(df, targetVerbID, resultsDictionary)

        #date
        resultsDictionary = extractUtils.addDateToDictionaryComplete(df, resultsDictionary)

        for index, row in df.iterrows():
            #reason
            if "AM-TMP" in resultsDictionary:
                resultsDictionary["Reason"] = resultsDictionary.pop("AM-TMP")

            # location
            if row[col.WORD] in locationStartingWords:
                resultsDictionary = extractUtils.addLocationToDictionary(resultsDictionary, extractUtils.getFullAgent(df, str(row[col.ID])))
            if "AM-LOC" in resultsDictionary:
                resultsDictionary = extractUtils.addLocationToDictionary(resultsDictionary, resultsDictionary.pop('AM-LOC'))
                #TODO: check if the corresponding AM-LOC has a geopolitical entity in it

        #removing the unnecessary context tags from the dictionary that aren't revlevant to 'evacuate'
        extractUtils.removeIrrelevantContextTags(resultsDictionary, evacuateContextTags)
        outputDictionary[fileAndSent] = resultsDictionary
               
    extractUtils.printOutputDictionary(outputDictionary, evacuateContextTags)

main()