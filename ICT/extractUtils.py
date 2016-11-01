import csv
import fnmatch
import os
from collections import defaultdict
import en
import nltk
import io
from getBaseWord import getBase

def getAbsolutePath():
    '''
    Create map between file name and the absolute file path of every news file
    :return: absolute path
    '''
    filePathDictionary = defaultdict(int)
    for root, dirnames, filenames in os.walk("NewsTextFiles"):
        for filename in fnmatch.filter(filenames, '*.txt'):
            relativePath = os.path.join(root, filename)
            fullFilePath = os.path.abspath(relativePath)
            fileNameWithoutExtension = os.path.splitext(filename)[0].strip()
            filePathDictionary[fileNameWithoutExtension] = fullFilePath
    return filePathDictionary

def extractSentencesForVerb(target_verb):
    '''
    Get all files associated with the given verb
    :param verb: the verb for which files need to be extracted
    :return: all the files associated with the verb
    '''
    filePathDictionary = getAbsolutePath()
    mycsv = csv.reader(open("finalPredicates3cols.csv"))
    dict = {}
    count = 0
    for row in mycsv:
        #splits the csv file by the period delimeter to get the verb associated
        verb = row[1].split(".")[0].strip()
        fileName = row[len(row) - 1].strip()
        if fileName in filePathDictionary:
            if verb == target_verb:
                # get all the words in the file
                file = io.open(filePathDictionary[fileName], "r",encoding='utf-8')

                sentences = file.read().split("\n\n")
                sentences[:] = (value for value in sentences if value != '\t')

                for sentenceNum in range(len(sentences)):
                    dictKey = fileName
                    sentence = sentences[sentenceNum]
                    if getBase(sentence,target_verb) is True:
                        if dictKey not in dict:
                            dict[dictKey] = []
                            dict[dictKey].append(sentenceNum+1)
                        else:
                            dict[dictKey].append(sentenceNum+1)

    return dict


def main():
    print extractSentencesForVerb("accuse")

main()


