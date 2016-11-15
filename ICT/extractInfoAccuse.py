import extractUtils
import pandas as pd
from io import StringIO
import io
import col
import calendar

def main():
    targetVerb = "accuse"
    files = extractUtils.getFileNamesForVerb(targetVerb)
    dict = extractUtils.getAbsolutePathForSrlFiles(files, "ClearnlpOutput")

    fileAndSentToValidDF = extractUtils.getValidDataFrameDictForTargetAction(targetVerb)

    outputDictionary = {}
    for fileAndSent in fileAndSentToValidDF.keys():
        if fileAndSent == "newsText3185.txt_Sent0":
            df = fileAndSentToValidDF[fileAndSent]
            resultsDictionary = {}
            resultsDictionary["action"] = targetVerb
            # search for row which has the target verb
            targetVerbRow = df.loc[df[col.LEMMA] == targetVerb]

            # grab the ID of that verb at that row
            targetVerbID = str(targetVerbRow[col.ID].iloc[0])

            # tracks the ID for the word "of" to extract the possible action from the subtree of that node
            IDForOf = -1

            # look at the SRL column in this chunk to see which row has the target verb identification as an argument
            for index, row in df.iterrows():
                srl = df.get_value(index, col.SRL)

                twoOrMoreSRLArguments = str(srl).split(";")  # 3:A0=PAG;11:A0=PAG two or more arguments are separated by semicolon

                oneSRLArgument = str(srl).split(":")  # 28:A0=PAG one argument separates relatedID and argument with colon

                validSRLs = []
                if len(twoOrMoreSRLArguments) > 1:  # there are two or more arguments
                    validSRLs = twoOrMoreSRLArguments
                elif len(oneSRLArgument) > 1:  # one argument
                    validSRLs.append(srl)

                for srlSection in validSRLs:  # ["3:A0=PAG", "11:A0=PAG"]
                    argumentSplit = srlSection.split(":")
                    relatedID = str(argumentSplit[0])  # 3
                    argumentNumberFull = argumentSplit[1]  # 'A0=PAG'

                    if relatedID == targetVerbID:  # our current row has an agent that corresponds to our target action
                        argumentNumber = argumentNumberFull.split("=")[0]  # just want to extract the 'A0' from 'A0=PAG'
                        agentID = str(df.get_value(index, col.ID))  # the ID of the row of the SRL with the agent

                        word = df.get_value(index, col.WORD)
                        resultsDictionary[argumentNumber] = word
                        resultsDictionary[argumentNumber] = extractUtils.getFullAgent(df, agentID)

                        # extracting the ID for of to find possible action
                        if argumentNumber == "A2":
                            IDForOf = row[col.ID]

                        ##get the child of the node 'accused', usually called "of", then get child of that to obtain the possible action/ action


                #if the correspoinding row has the preposition "of" get the possible action which is A2 for the target action
                if row[col.PARENT] == int(IDForOf):
                    resultsDictionary["possible action"] = resultsDictionary["A2"]

                #check if this is a passive action
                if row[col.POS] == "VBP":
                    if int(df.get_value(index, col.PARENT)) == int(targetVerbID):
                        resultsDictionary["passive"] = "true"

                # see if the word corresponds to any day/month and if yes add it to the date/location param
                resultsDictionary = extractUtils.addDateToDictionary(row[col.WORD], resultsDictionary)


            outputDictionary[fileAndSent] = resultsDictionary
    print outputDictionary

main()