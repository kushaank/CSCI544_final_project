import extractUtils
import pandas as pd
from io import StringIO
import io
import calendar

def main():
    targetVerb = "suspend"
    files = extractUtils.getFileNamesForVerb(targetVerb)
    dict = extractUtils.getAbsolutePathForSrlFiles(files, "ClearnlpOutput")

    ID = "ID"
    WORD = "Word"
    LEMMA = "Lemma"
    POS = "POS"
    FEATURES = "Features"
    PARENT = "Parent"
    DEPENDENCY_LABELS = "Dependency Labels"
    SRL = "SRL"

    A0 = "A0"
    A1 = "A1"

    sentences = []
    for key in dict.keys():

        path = "/Users/kushaankumar/Desktop/CSCI544_final_project/ICT/ClearnlpOutput/ClearnlpOutput/Part2/newsText720.txt.srl"
        file = io.open(path,"r", encoding='utf-8')
        srlSentenceChunks = file.read().split("\n\n")

        for chunk in srlSentenceChunks[:-1]:
            TESTDATA = StringIO(chunk)
            df = pd.read_table(TESTDATA, names=[ID, WORD, LEMMA, POS, FEATURES, PARENT, DEPENDENCY_LABELS, SRL])
            if targetVerb in df[LEMMA].tolist():
                sentences.append(df)
            break
        break
    resultsDictionary = {}
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

            if relatedID == targetVerbID:  # our current row has an agent that corresponds to our target action
                argumentNumber = argumentNumberFull.split("=")[0]  # just want to extract the 'A0' from 'A0=PAG'
                agentID = str(df.get_value(index, ID))  # the ID of the row of the SRL with the agent

                # need more children examples
                # childrenDictionary = {}

                # for index1, row1 in df.iterrows():
                #     parent = df.get_value(index1, PARENT)
                #     if str(parent) == agentID: #a row's parent value is the ID of the agent we found
                #         print df.get_value(index1, ID)
                #         childrenDictionary[df.get_value(index1, ID)] = str(df.get_value(index1, WORD))

                word = df.get_value(index, WORD)
                resultsDictionary[argumentNumber] = word
                resultsDictionary[argumentNumber] = extractUtils.getFullAgent(df, agentID)



        #extract reason from SRL
        if "AM-CAU" in resultsDictionary:
            resultsDictionary["Reason"] = resultsDictionary.pop('AM-CAU')

        #extract location from SRL
        if "AM-DIS" in resultsDictionary:
            resultsDictionary["Location"] = resultsDictionary.pop('AM-DIS')
        # see if the word corresponds to any day/month and if yes add it to the date/location param
        if row[WORD] in calendar.day_name:
            resultsDictionary["Date/Time"] = row[WORD]

        if row[WORD] in calendar.month_name:
            resultsDictionary["Date/Time"] = row[WORD]

        if row[WORD] in calendar.day_abbr:
            resultsDictionary["Date/Time"] = row[WORD]

        if row[WORD] in calendar.month_abbr:
            resultsDictionary["Date/Time"] = row[WORD]

    print resultsDictionary
    # print childrenDictionary


main()

