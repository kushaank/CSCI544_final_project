import extractUtils
import col

def main():
    targetVerb = "sign"
    fileAndSentToValidDF = extractUtils.getValidDataFrameDictForTargetAction(targetVerb, "finalPredicates3cols.csv", "ClearnlpOutput")
    capitalsList = extractUtils.getCapitalsList()

    signContextTags = ["A0", "Probable Action", "Improbable Action", "A1", "Date/Time", "Action", "Signed Object"]
    
    outputDictionary = {}
    for fileAndSent in fileAndSentToValidDF.keys():
        if fileAndSent == "newsText22725.txt_Sent7": #only because I want to see results of one file which is faster
            df = fileAndSentToValidDF[fileAndSent]

            resultsDictionary = {}
            for contextTag in signContextTags:
                resultsDictionary[contextTag] = None
                
            targetVerbRow =  df.loc[df[col.LEMMA] == targetVerb]
            targetVerbID = str(targetVerbRow[col.ID].iloc[0])

            if extractUtils.isNegatedVerb(df, targetVerbID):
                resultsDictionary["Improbable Action"] = targetVerb
            else:
                resultsDictionary["Probable Action"] = targetVerb

            resultsDictionary = extractUtils.getArgumentsForGivenID(df, targetVerbID, resultsDictionary)
            #checking if agent 1 contains a geopoliticalagent
            if extractUtils.isValidGeopoliticalAgent(resultsDictionary["A1"], capitalsList):
                #checking if agent1 is inside the signed object
                originalAgent1 = resultsDictionary["A1"]
                indexOfWith = originalAgent1.find("with")
                possibleAgent2 = originalAgent1[indexOfWith:]
                if indexOfWith != -1 and extractUtils.isValidGeopoliticalAgent(possibleAgent2, capitalsList):
                    resultsDictionary["A1"] = possibleAgent2
                    resultsDictionary["Signed Object"] = originalAgent1[:indexOfWith]
                else:
                    print "ERROR: " + fileAndSent
            else:
                resultsDictionary["Signed Object"] = resultsDictionary.pop("A1")

            resultsDictionary = extractUtils.addDateToDictionaryComplete(df, resultsDictionary)
            
            #remove the context tags that get populated that aren't in the "signContextTags context tag array"
            extractUtils.removeIrrelevantContextTags(resultsDictionary, signContextTags)
            outputDictionary[fileAndSent] = resultsDictionary

    extractUtils.printOutputDictionary(outputDictionary, signContextTags)


main()