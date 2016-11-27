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
    targetVerb = "target"
    fileAndSentToValidDF = extractUtils.getValidDataFrameDictForTargetAction(targetVerb)

    targetCategories = ["A0", "Probable Action","Improbable Action", "A1", "Date/Time", "Location", "Reason"]
    outputDictionary = {}

    for fileAndSent in fileAndSentToValidDF.keys():
        if fileAndSent == "newsText13707.txt_Sent2": #only because I want to see results of one file which is faster
            df = fileAndSentToValidDF[fileAndSent]
            resultsDictionary = {}
            for category in targetCategories:
                resultsDictionary[category] = None

            targetVerbRow =  df.loc[df[col.LEMMA] == targetVerb]
            targetVerbID = str(targetVerbRow[col.ID].iloc[0])
            
            resultsDictionary = extractUtils.getArgumentsForGivenID(df, targetVerbID, resultsDictionary)

            #improbable action if the target action is preceded with a NEG
            if isNegatedVerb(df, targetVerbID):
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

            #removing the unnecessary categories from the dictionary that aren't revlevant to 'evacuate'
            for result in resultsDictionary.keys():
                if result not in targetCategories:
                    resultsDictionary.pop(result)
            outputDictionary[fileAndSent] = resultsDictionary
                
    for key in outputDictionary.keys():
        print (key + ": " + str(outputDictionary[key]) + '\n')

main()