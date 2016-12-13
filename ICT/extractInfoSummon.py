import extractUtils
import col

def main():
    targetVerb = "summon"
    fileAndSentToValidDF = extractUtils.getValidDataFrameDictForTargetAction(targetVerb)

    summonContextTags = ["A0", "Probable Action", "Improbable Action", "A1", "Date/Time", "Reason Action", "Reason"]
    
    outputDictionary = {}
    for fileAndSent in fileAndSentToValidDF.keys():
        df = fileAndSentToValidDF[fileAndSent]

        resultsDictionary = {}
        for contextTag in summonContextTags:
            resultsDictionary[contextTag] = None

        targetVerbRow =  df.loc[df[col.LEMMA] == targetVerb]
        targetVerbID = str(targetVerbRow[col.ID].iloc[0])

        if extractUtils.isNegatedVerb(df, targetVerbID):
            resultsDictionary["Improbable Action"] = targetVerb
        else:
            resultsDictionary["Probable Action"] = targetVerb

        resultsDictionary = extractUtils.getArgumentsForGivenID(df, targetVerbID, resultsDictionary)

        #if there is a AM-PRP argument for 'summon' and it is an infinitive
        amPrpId = extractUtils.getArgumentIDsForGivenID(df, targetVerbID).get("AM-PRP")
        if amPrpId != None and extractUtils.isInfinitive(amPrpId, df):
            reasonAction = extractUtils.getInfinitiveAgent(amPrpId, df)
            resultsDictionary["Reason Action"] = reasonAction
            fullReasonAgent = extractUtils.getFullAgent(df, amPrpId)
            resultsDictionary["Reason"] = fullReasonAgent[len(reasonAction):]
        else:
            #there is no SRL for the reason action infinitive, then check all the children of agent 1 to see if any contain the infinitive
            argument1ID = extractUtils.getArgumentIDsForGivenID(df, targetVerbID).get("A1")
            if argument1ID != None:
                immediateChildrenIds = extractUtils.getImmediateChildrenForAgent(df, argument1ID)
                for childId in immediateChildrenIds:
                    if extractUtils.isInfinitive(childId, df):
                        reasonAction = extractUtils.getInfinitiveAgent(childId, df)
                        resultsDictionary["Reason Action"] = reasonAction
                        fullReasonAgent = extractUtils.getFullAgent(df, childId)
                        resultsDictionary["Reason"] = fullReasonAgent[len(reasonAction):]
        

        resultsDictionary = extractUtils.addDateToDictionaryComplete(df, resultsDictionary)

        #if the reason isn't populated from the infinitive pattern check above and AM-TMP still exists because it wasn't a date
        if resultsDictionary["Reason"] == None:
            if resultsDictionary.get("AM-TMP") != None:
                resultsDictionary["Reason"] = resultsDictionary.pop("AM-TMP")

        #removing the unnecessary categories from the dictionary that aren't revlevant to 'summon'
        extractUtils.removeIrrelevantContextTags(resultsDictionary, summonContextTags)
        outputDictionary[fileAndSent] = resultsDictionary
                    
    extractUtils.printOutputDictionary(outputDictionary, summonContextTags)

main()