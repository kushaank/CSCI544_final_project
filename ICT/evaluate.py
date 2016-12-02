import pandas as pd
import extractUtils as utils
import csv
from io import StringIO
import col
import io
import sys


def getFileNamesForVerb(targetVerb, csvfilepath):
    '''
       Get all the text news files that contain the given verb
       :param verb: the verb for which files need to be extracted
       :return: array of all the files  + .txt associated with the provided target_verb
       '''
    filePathDictionary = utils.getAbsolutePath(".txt", "NewsTextFiles")
    mycsv = csv.reader(open(csvfilepath))

    files = []

    for row in mycsv:
        # splits the csv file by the period delimeter to get the verb associated
        verb = row[1].split(".")[0].strip()
        fileName = row[len(row) - 1].strip()

        # checking that indeed the filename in the predicated.xls maps to an existing file in the newsFiles folder
        if fileName in filePathDictionary:
            if verb == targetVerb:
                files.append(fileName + ".txt")
        else:
            print "'" + fileName + "' does not exist in the newsFiles folder"
            return -1
    return files


def getValidDataFrameDictForVerb(targetVerb, csvfilename):
    files = getFileNamesForVerb(targetVerb, csvfilename)

    fileAndSentToValidDF = {}
    dict = utils.getAbsolutePathForSrlFiles(files, "ClearnlpOutput")

    for key in dict.keys():
        file = io.open(dict[key], "r", encoding='utf-8')
        srlSentenceChunks = file.read().split("\n\n")

        sentenceNumber = 0
        for chunk in srlSentenceChunks[:-1]:
            TESTDATA = StringIO(chunk)
            df = pd.read_table(TESTDATA, names=[col.ID, col.WORD, col.LEMMA, col.POS, col.FEATURES, col.PARENT,
                                                col.DEPENDENCY_LABELS, col.SRL])
            if targetVerb in df[col.LEMMA].tolist():
                fileAndSent = key + "_Sent" + str(sentenceNumber)
                # replace NaN values with "0" to avoid NaN errors in some files
                df = df.fillna("0")
                fileAndSentToValidDF[fileAndSent] = df
            sentenceNumber += 1

    return fileAndSentToValidDF


def isRelevant(dataframe):
    agentOne = utils.getAllAgentsWithGivenSRL(dataframe, "A0")
    agentTwo = utils.getAllAgentsWithGivenSRL(dataframe, "A1")
    A2 = utils.getAllAgentsWithGivenSRL(dataframe, "A2")

    geopoliticalAgentList = utils.getCapitalsList()
    geopoliticalAgentList.update(utils.getHeadOfStateList())
    geopoliticalAgentList.update(utils.getNationalityList())
    geopoliticalAgentList = list(geopoliticalAgentList)

    if agentOne in geopoliticalAgentList:
        return True
    if agentTwo in geopoliticalAgentList:
        return True
    if A2 in geopoliticalAgentList:
        return True
    for word in agentOne:
        if word.lower() in geopoliticalAgentList:
            return True
    for word in agentTwo:
        if word.lower() in geopoliticalAgentList:
            return True
    for word in A2:
        if word.lower() in geopoliticalAgentList:
            return True


def getRelevancyAccuracy(targetVerb, csvfilename):
    correctCount = 0.0
    count = 0.0
    fileNamedict = getValidDataFrameDictForVerb(targetVerb, csvfilename)
    for key in fileNamedict:
        dataframe = fileNamedict.get(key)
        if isRelevant(dataframe):
            correctCount += 1
        count += 1
    print correctCount
    print count
    return float(correctCount / count)


def printDataFrameToTest(targetVerb, csvfilename):
    fileNamedict = getValidDataFrameDictForVerb(targetVerb, csvfilename)
    for key in fileNamedict:
        dataframe = fileNamedict.get(key)
        print (key)
        print (dataframe)
        print('\n')


def main():
    csvfilename = "finalPredicates3cols.csv"
    targetVerb = "accuse"
    print (getRelevancyAccuracy(targetVerb, csvfilename))
    print printDataFrameToTest(targetVerb, csvfilename)


main()
