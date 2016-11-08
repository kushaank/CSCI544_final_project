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
    targetVerb = "evacuate"
    files = extractUtils.getFileNamesForVerb(targetVerb)
    dict = extractUtils.getAbsolutePathForSrlFiles(files, "ClearnlpOutput")

    sentences = []
    for key in dict.keys():
        file = io.open("/Users/eamonb/Documents/CS544/Projects/group project/CSCI544_final_project/ICT/ClearnlpOutput/ClearnlpOutput/Part9/newsText4934.txt.srl", "r", encoding='utf-8')
        srlSentenceChunks = file.read().split("\n\n")

        for chunk in srlSentenceChunks[:-1]:
            TESTDATA = StringIO(chunk)
            df = pd.read_table(TESTDATA, names=[ID,WORD,LEMMA,POS,FEATURES,PARENT,DEPENDENCY_LABELS,SRL])
            if targetVerb in df[LEMMA].tolist():
                sentences.append(df)
            break
        break
    
    resultsDictionary = {}
    resultsDictionary["action"] = targetVerb
    #search for row which has the target verb
    targetVerbRow =  df.loc[df[LEMMA] == targetVerb]

    #grab the ID of that verb at that row
    targetVerbID = str(targetVerbRow[ID].iloc[0])

    locationStartingWords = ["from", "of", "in"]

    for index, row in df.iterrows():

        wordValue = str(df.get_value(index, WORD))
        wordId = df.get_value(index, ID)
        if wordValue in locationStartingWords:
            print extractUtils.getFullAgent(df, wordId)

        srl = df.get_value(index, SRL)
        twoOrMoreSRLArguments = str(srl).split(";") #3:A0=PAG;11:A0=PAG two or more arguments are separated by semicolon
        oneSRLArgument = str(srl).split(":") #28:A0=PAG one argument separates relatedID and argument with colon
        validSRLs = []
        if len(twoOrMoreSRLArguments) > 1: #there are two or more arguments
            validSRLs = twoOrMoreSRLArguments
        elif len(oneSRLArgument) > 1: #one argument
            validSRLs.append(srl)

        for srlSection in validSRLs: #["3:A0=PAG", "11:A0=PAG"]
            argumentSplit = srlSection.split(":")
            relatedID = str(argumentSplit[0]) #3
            argumentNumberFull = argumentSplit[1] #'A0=PAG'

            if relatedID == targetVerbID: #our current row has an agent that corresponds to our target action
                argumentNumber = argumentNumberFull.split("=")[0] # just want to extract the 'A0' from 'A0=PAG'
                agentID = str(df.get_value(index, ID))  #the ID of the row of the SRL with the agent
                agentWord = str(df.get_value(index, WORD))
                
                resultsDictionary[argumentNumber] = extractUtils.getFullAgent(df, agentID)
                
    # print df
    # print resultsDictionary

main()