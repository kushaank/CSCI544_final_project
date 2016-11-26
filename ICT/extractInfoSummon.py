import extractUtils
import col

def getDatesInSentence(df):
    datesList = []
    for index, row in df.iterrows():
        word = df.get_value(index, col.WORD)
        if extractUtils.valid_date(word):
            datesList.append(word)
    return datesList

def main():
    targetVerb = "summon"
    fileAndSentToValidDF = extractUtils.getValidDataFrameDictForTargetAction(targetVerb)
    capitalsList = extractUtils.getCapitalsList()

    signCategories = ["A0", "A1", "Date/Time", "Reason Action", "Reason"]
    
    outputDictionary = {}
    for fileAndSent in fileAndSentToValidDF.keys():
        if fileAndSent == "newsText13488.txt_Sent3": #only because I want to see results of one file which is faster
            df = fileAndSentToValidDF[fileAndSent]

            resultsDictionary = {}
            for category in signCategories:
                resultsDictionary[category] = None

            resultsDictionary["Action"] = targetVerb

            targetVerbRow =  df.loc[df[col.LEMMA] == targetVerb]
            targetVerbID = str(targetVerbRow[col.ID].iloc[0])

            resultsDictionary = extractUtils.getArgumentsForGivenID(df, targetVerbID, resultsDictionary)

            #if there is a AM-PRP argument for 'summon' and it is an infinitive
            amPrpId = extractUtils.getArgumentIDsForGivenID(df, targetVerbID, resultsDictionary).get("AM-PRP")
            if amPrpId != None and extractUtils.isInfinitive(amPrpId, df):
                reasonAction = extractUtils.getInfinitiveAgent(amPrpId, df)
                resultsDictionary["Reason Action"] = reasonAction
                fullReasonAgent = extractUtils.getFullAgent(df, amPrpId)
                resultsDictionary["Reason"] = fullReasonAgent[len(reasonAction):]
            else:
                #there is no SRL for the reason action infinitive, then check all the children of agent 1 to see if any contain the infinitive
                argument1ID = extractUtils.getArgumentIDsForGivenIDTEST(df, targetVerbID).get("A1")
                if argument1ID != None:
                    immediateChildrenIds = extractUtils.getImmediateChildrenForAgent(df, argument1ID)
                    for childId in immediateChildrenIds:
                        if extractUtils.isInfinitive(childId, df):
                            reasonAction = extractUtils.getInfinitiveAgent(childId, df)
                            resultsDictionary["Reason Action"] = reasonAction
                            fullReasonAgent = extractUtils.getFullAgent(df, childId)
                            resultsDictionary["Reason"] = fullReasonAgent[len(reasonAction):]
            
            datesInSentence = getDatesInSentence(df)
            
            #if the reason isn't populated from the infinitive pattern check
            if resultsDictionary["Reason"] == None:
                if resultsDictionary.get("AM-TMP") != None:
                    potentialReason = resultsDictionary["AM-TMP"]
                    potentialReasonArray = potentialReason.split(" ")
                    validDate = False
                    for word in potentialReasonArray:
                        if word in datesInSentence:
                            #if AMP-TMP has a valid date word in it, then Date/Time = AM-TMP
                            resultsDictionary["Date/Time"] = resultsDictionary.pop("AM-TMP")
                            validDate = True
                            break
                    #if not, then Reason = AM-TMP
                    if validDate == False:
                        resultsDictionary["Reason"] = resultsDictionary.pop("AM-TMP")

            #if AM-TMP was not assigned to Reason yet, then it is considered a Date/Time
            if resultsDictionary.get("AM-TMP") != None :
                resultsDictionary["Date/Time"] = resultsDictionary.pop("AM-TMP")
            else:
                for index, row in df.iterrows():
                    resultsDictionary = extractUtils.addDateToDictionary(row[col.WORD], resultsDictionary)

            #removing the unnecessary categories from the dictionary that aren't revlevant to 'evacuate'
            for result in resultsDictionary.keys():
                if result not in signCategories:
                    resultsDictionary.pop(result)
            outputDictionary[fileAndSent] = resultsDictionary
                    
    for key in outputDictionary.keys():
        print (key + ": " + str(outputDictionary[key]) + '\n')

main()