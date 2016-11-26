import extractUtils
import col

def main():
    targetVerb = "evacuate"
    fileAndSentToValidDF = extractUtils.getValidDataFrameDictForTargetAction(targetVerb)

    evacuateCategories = ["Location", "A0", "A1", "Date/Time", "Action"]
    
    outputDictionary = {}
    for fileAndSent in fileAndSentToValidDF.keys():
        if fileAndSent == "newsText3702.txt_Sent0": #only because I want to see results of one file which is faster

            df = fileAndSentToValidDF[fileAndSent]
            
            resultsDictionary = {}
            for category in evacuateCategories:
                resultsDictionary[category] = None

            resultsDictionary["Action"] = targetVerb

            targetVerbRow =  df.loc[df[col.LEMMA] == targetVerb]
            targetVerbID = str(targetVerbRow[col.ID].iloc[0])

            #from Vietman, of China, in Serbia
            locationStartingWords = ["from", "of", "in"]

            resultsDictionary = extractUtils.getArgumentsForGivenID(df, targetVerbID, resultsDictionary)

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
                
                #date
                resultsDictionary = extractUtils.addDateToDictionary(row[col.WORD], resultsDictionary)

            #removing the unnecessary categories from the dictionary that aren't revlevant to 'evacuate'
            for result in resultsDictionary.keys():
                if result not in evacuateCategories:
                    resultsDictionary.pop(result)
            outputDictionary[fileAndSent] = resultsDictionary
                
    for key in outputDictionary.keys():
        print (key + ": " + str(outputDictionary[key]) + '\n')

main()