import extractUtils
import col

#checks all the immediate children of a target verb and makes sure none of their SRLs have a NEG in it
def isNegatedVerb(df, targetParentID):
    immediateChildIDs = extractUtils.getImmediateChildrenForAgent(df, targetParentID)
    for childID in immediateChildIDs:
        srls = str(df.iloc[int(childID)-1][col.SRL])
        if "NEG" in srls:
            return True
    return False

def main():
    capitalsList = extractUtils.getCapitalsList()
    targetVerb = "warn"
    fileAndSentToValidDF = extractUtils.getValidDataFrameDictForTargetAction(targetVerb)

    warnCategories = ["A0", "Action", "A1", "Probable Warned Action", "Improbable Warned Action", "Warned Object", "Date/Time"]

    outputDictionary = {}
    for fileAndSent in fileAndSentToValidDF.keys():
        if fileAndSent == "newsText7732.txt_Sent0": #only because I want to see results of one file which is faster
            df = fileAndSentToValidDF[fileAndSent]

            resultsDictionary = {}
            for category in warnCategories:
                resultsDictionary[category] = None

            resultsDictionary["Action"] = targetVerb

            targetVerbRow =  df.loc[df[col.LEMMA] == targetVerb]
            targetVerbID = str(targetVerbRow[col.ID].iloc[0])

            resultsDictionary = extractUtils.getArgumentsForGivenID(df, targetVerbID, resultsDictionary)
            
            argument1ID = extractUtils.getArgumentIDsForGivenIDTEST(df, targetVerbID).get("A1")
            thatExists = False
            
            #if argument1 of the target verb is not a geopolitical entity, check if that specific word at the index is a "warned action"
            possibleWarnedAction = df.iloc[int(argument1ID)-1][col.WORD].lower()
            if not extractUtils.isValidGeopoliticalAgent(possibleWarnedAction, capitalsList):
                if isNegatedVerb(df, argument1ID):
                    resultsDictionary["Improbable Warned Action"] = possibleWarnedAction
                else:
                    resultsDictionary["Probable Warned Action"] = possibleWarnedAction

                #take all the words following the warned action and classify them as the "warned Object"
                warnedObject = extractUtils.getFullAgent(df, argument1ID)
                #take the full agent of the warned action and snip out the text before and including the warned action to be left with only the text after it
                #ex. warned action = "is". fullAgent = "that Somalia is at risk of another famine". warned object = "at risk of another famine"
                argument1Word = df.iloc[int(argument1ID)-1][col.WORD].lower()
                argument1WordIndex = warnedObject.find(argument1Word)
                warnedObject = warnedObject[argument1WordIndex + len(argument1Word):]
                resultsDictionary["Warned Object"] = warnedObject
            
            #check if "THAT" exists as a child of A1 of the targetverb
            if argument1ID != None:
                immediateChildrenIds = extractUtils.getImmediateChildrenForAgent(df, argument1ID)
                #check if the left most child is "that"
                childId = immediateChildrenIds[0]
                childWord = df.iloc[int(childId)-1][col.WORD].lower()
                childAgent = extractUtils.getFullAgent(df, childId)
                #if the first child is "that", the next child is agent2
                if childWord == "that":
                    thatExists = True
                    possibleAgent2 = None
                    if len(immediateChildrenIds) > 1:
                        #second child from the left under the "warned action"
                        nextChildId = immediateChildrenIds[1]
                        possibleAgent2 = extractUtils.getFullAgent(df, nextChildId)
    #                 if extractUtils.isValidGeopoliticalAgent(possibleAgent2, capitalsList):
                        resultsDictionary["A1"] = "that " + possibleAgent2
                #if the first child is not "that" but is still a geopolitical agent, consider it A1
                #ex. "Russia has warned China will supply" instead of "Russia has warned "that" China will supply"
                elif extractUtils.isValidGeopoliticalAgent(childAgent, capitalsList):
                    resultsDictionary["A1"] = childAgent
               
            if resultsDictionary.get("AM-TMP") != None :
                resultsDictionary["Date/Time"] = resultsDictionary.pop("AM-TMP")
            else:
                for index, row in df.iterrows():
                    resultsDictionary = extractUtils.addDateToDictionary(row[col.WORD], resultsDictionary)

            #removing the unnecessary categories from the dictionary that aren't revlevant to 'warn'
            for result in resultsDictionary.keys():
                if result not in warnCategories:
                    resultsDictionary.pop(result)
            outputDictionary[fileAndSent] = resultsDictionary

    print outputDictionary

main()