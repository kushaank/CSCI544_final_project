import extractUtils
import pandas as pd
from io import StringIO
import io

ID = "ID"
WORD = "Word"
LEMMA = "Lemma"
POS = "POS"
FEATURES = "Features"
PARENT = "Parent"
DEPENDENCY_LABELS = "Dependency Labels"
SRL = "SRL"

A0 = "A0"
A1= "A1"

def main():
    targetVerb = "urge"
    fileAndSentToValidDF = extractUtils.getValidDataFrameDictForTargetAction(targetVerb)

    outputDictionary = {}
    for fileAndSent in fileAndSentToValidDF.keys():
        df = fileAndSentToValidDF[fileAndSent]
        #print df
        resultsDictionary = {}
        resultsDictionary["A0"] = None
        resultsDictionary["A1"] = None
        resultsDictionary["PA"] = None
        resultsDictionary["action"] = targetVerb
        # search for row which has the target verb
        targetVerbRow = df.loc[df[LEMMA] == targetVerb]
        # grab the ID of that verb at that row
        targetVerbID = str(targetVerbRow[ID].iloc[0])

        # look at the SRL column in this chunk to see which row has the target verb identification as an argument
        for index, row in df.iterrows():
            srl = df.get_value(index, SRL)
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

                agentID = ""
                paID = ""
                if relatedID == targetVerbID:  # our current row has an agent that corresponds to our target action
                    argumentNumber = argumentNumberFull.split("=")[0]  # just want to extract the 'A0' from 'A0=PAG'
                    if argumentNumber == 'A2':
                        paID = str(df.get_value(index, ID))
                        fullAgent = extractUtils.getFullAgent(df, paID)
                        word = df.get_value(index, WORD)
                        resultsDictionary['PA'] = word
                    else:
                        agentID = str(df.get_value(index, ID))  # the ID of the row of the SRL with the agent
                        fullAgent = extractUtils.getFullAgent(df, agentID)
                        resultsDictionary[argumentNumber] = fullAgent
        #print resultsDictionary
        outputDictionary[fileAndSent] = resultsDictionary
    #print outputDictionary

main()

