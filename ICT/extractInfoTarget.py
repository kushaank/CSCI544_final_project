import extractUtils
import col

def main():
    targetVerb = "target"
    fileAndSentToValidDF = extractUtils.getValidDataFrameDictForTargetAction(targetVerb, "finalPredicates3cols.csv", "ClearnlpOutput")

    targetContextTags = ["A0", "Probable Action", "Improbable Action", "A1", "Date/Time", "Reason"]
    outputDictionary = {}

    for fileAndSent in fileAndSentToValidDF.keys():
        df = fileAndSentToValidDF[fileAndSent]
        resultsDictionary = {}

        for contextTag in targetContextTags:
            resultsDictionary[contextTag] = None

        targetVerbRow =  df.loc[df[col.LEMMA] == targetVerb]
        targetVerbID = str(targetVerbRow[col.ID].iloc[0])
        
        resultsDictionary = extractUtils.getArgumentsForGivenID(df, targetVerbID, resultsDictionary)

        #improbable action if the target action is preceded with a NEG
        if extractUtils.isNegatedVerb(df, targetVerbID):
            resultsDictionary["Improbable Action"] = targetVerb
        else:
            resultsDictionary["Probable Action"] = targetVerb
        
        #get the actual form of the target verb in the sentence. ex. target verb = target, but in the sentence it's "targeting"
        actualTargetVerb = extractUtils.getWordAtWordId(df, targetVerbID)
        
        argument1String = resultsDictionary.get("A0")
        #pattern: check if the target verb is inside the agent 1
        if argument1String != None:
            targetIndex = argument1String.find(actualTargetVerb)
            #the target verb is inside A1
            if targetIndex != -1:
                #update A1 to only be the words up until the target verb
                resultsDictionary["A0"] = argument1String[:targetIndex]
                
        resultsDictionary = extractUtils.addDateToDictionaryComplete(df, resultsDictionary)

        #removing the unnecessary context tags from the dictionary that aren't revlevant to 'target'
        extractUtils.removeIrrelevantContextTags(resultsDictionary, targetContextTags)
        outputDictionary[fileAndSent] = resultsDictionary
                
    extractUtils.printOutputDictionary(outputDictionary, targetContextTags)

main()