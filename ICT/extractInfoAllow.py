import extractUtils
import col

def main():
    capitalsList = extractUtils.getCapitalsList()
    targetVerb = "allow"
    fileAndSentToValidDF = extractUtils.getValidDataFrameDictForTargetAction(targetVerb)
    
    allowContextTags = ["A0", "Probable Action", "Improbable Action", "A1", "Allowed Action", "Allowed Object", "Date/Time", "Location"]

    outputDictionary = {}
    for fileAndSent in fileAndSentToValidDF.keys():
        df = fileAndSentToValidDF[fileAndSent]                        
        resultsDictionary = {}
        for contextTag in allowContextTags:
            resultsDictionary[contextTag] = None

        targetVerbRow =  df.loc[df[col.LEMMA] == targetVerb]
        targetVerbID = str(targetVerbRow[col.ID].iloc[0])

        if extractUtils.isNegatedVerb(df, targetVerbID):
            resultsDictionary["Improbable Action"] = targetVerb
        else:
            resultsDictionary["Probable Action"] = targetVerb
            
        #from Vietman, of China, in Serbia
        locationStartingWords = ["in", "to", "from", "into"]

        #get arguments for the target word
        resultsDictionary = extractUtils.getArgumentsForGivenID(df, targetVerbID, resultsDictionary)

        #only add the location if its 
        if "AM-LOC" in resultsDictionary:
            potentialLocation = resultsDictionary.pop('AM-LOC')
            if extractUtils.isValidGeopoliticalAgent(potentialLocation, capitalsList):
                resultsDictionary = extractUtils.addLocationToDictionary(resultsDictionary, potentialLocation)

        for index, row in df.iterrows():
            # location
            if "Location" not in resultsDictionary.keys(): 
                if row[col.WORD] in locationStartingWords:
                    locationID = str(row[col.ID])
                    locationPhrase = extractUtils.getFullAgent(df, locationID)
                    if extractUtils.isValidGeopoliticalAgent(locationPhrase, capitalsList):
                        resultsDictionary = extractUtils.addLocationToDictionary(resultsDictionary, locationPhrase)

            #date #TODO: try on 15497_sent10
            # resultsDictionary = extractUtils.addDateToDictionary(row[col.WORD], resultsDictionary)
        resultsDictionary = extractUtils.addDateToDictionaryComplete(df, resultsDictionary)

        #if there is a a1 for 'allow' and it is an infinitive
        argument1ID = extractUtils.getArgumentIDsForGivenID(df, targetVerbID).get("A1")
        if "A1" in resultsDictionary.keys() and extractUtils.isInfinitive(argument1ID, df):
            allowedActionID = argument1ID
            
            #the argument1 of "allow" is typically an infinitive which represents the "allowed action"
            resultsDictionary["Allowed Action"] = extractUtils.getInfinitiveAgent(allowedActionID, df)

            #the argument0 of the "allowed action" is typically the agent1 for the sentences with "allow"
            agent2ID = extractUtils.getArgumentIDsForGivenID(df, allowedActionID).get("A0")
            if agent2ID != None:
                resultsDictionary["A1"] = extractUtils.getFullAgent(df, agent2ID)

            #the righter child of the allowed action is the allowed object
            allowedActionDictionary = extractUtils.getFullAgentDictionary(df, allowedActionID)
            sortedKeys = list(allowedActionDictionary.keys())
            sortedKeys.sort()
            sortedValues = []
            
            for key in sortedKeys:
                if int(key) > int(allowedActionID):
                    sortedValues.append(allowedActionDictionary[key])

            resultsDictionary["Allowed Object"] = " ".join(sortedValues)

            #remove the context tags that get populated that aren't in the "allowContextTags context tag array"
            extractUtils.removeIrrelevantContextTags(resultsDictionary, allowContextTags)
            outputDictionary[fileAndSent] = resultsDictionary

    extractUtils.printOutputDictionary(outputDictionary, allowContextTags)
main()