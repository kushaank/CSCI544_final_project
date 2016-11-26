import extractUtils
import col

def main():
    targetVerb = "sign"
    fileAndSentToValidDF = extractUtils.getValidDataFrameDictForTargetAction(targetVerb)
    capitalsList = extractUtils.getCapitalsList()

    signCategories = ["A0", "A1", "Date/Time", "Action", "Signed Object"]
    
    outputDictionary = {}
    for fileAndSent in fileAndSentToValidDF.keys():
        if fileAndSent == "newsText22725.txt_Sent7": #only because I want to see results of one file which is faster
            df = fileAndSentToValidDF[fileAndSent]

            resultsDictionary = {}
            for category in signCategories:
                resultsDictionary[category] = None

            resultsDictionary["Action"] = targetVerb

            targetVerbRow =  df.loc[df[col.LEMMA] == targetVerb]
            targetVerbID = str(targetVerbRow[col.ID].iloc[0])

            #from Vietman, of China, in Serbia
            locationStartingWords = ["from", "of", "in"]

            resultsDictionary = extractUtils.getArgumentsForGivenID(df, targetVerbID, resultsDictionary)
            #checking if agent 1 contains a geopoliticalagent
            if extractUtils.isValidGeopoliticalAgent(resultsDictionary["A1"], capitalsList):
                #checking if agent1 is inside the signed object
                originalAgent1 = resultsDictionary["A1"]
                indexOfWith = originalAgent1.find("with")
                if indexOfWith != -1 and extractUtils.isValidGeopoliticalAgent(possibleAgent2, capitalsList):
                    possibleAgent2 = originalAgent1[indexOfWith:]
                    resultsDictionary["A1"] = possibleAgent2
                    resultsDictionary["Signed Object"] = originalAgent1[:indexOfWith]
                else:
                    print "ERROR: " + fileAndSent
            else:
                resultsDictionary["Signed Object"] = resultsDictionary.pop("A1")

            #if there is a time that is an argument to the target verb
            if "AM-TMP" in resultsDictionary:
                resultsDictionary["Date/Time"] = resultsDictionary.pop("AM-TMP")
            #otherwise grab any time in the sentence
            elif len(extractUtils.getAllAgentsWithGivenSRL(df, "AM-TMP")) > 0:
                resultsDictionary["Date/Time"] = extractUtils.getAllAgentsWithGivenSRL(df, "AM-TMP")[0]
            else:
                #TODO: extract any possible date from the sentence

            #removing the unnecessary categories from the dictionary that aren't revlevant to 'evacuate'
            for result in resultsDictionary.keys():
                if result not in signCategories:
                    resultsDictionary.pop(result)
            outputDictionary[fileAndSent] = resultsDictionary
                    
    for key in outputDictionary.keys():
        print (key + ": " + str(outputDictionary[key]) + '\n')

main()