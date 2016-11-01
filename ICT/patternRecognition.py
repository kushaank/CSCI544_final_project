import csv
import fnmatch
import os
from collections import defaultdict
from nltk.stem.wordnet import WordNetLemmatizer

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
        if count == 0:
            #splits the csv file by the period delimeter to get the verb associated
            verb = row[1].split(".")[0].strip()
            fileName = row[len(row) - 1].strip()
            if fileName in filePathDictionary:
                if verb == target_verb:
                    # get all the words in the file
                    file = open(filePathDictionary[fileName], "r")
                    sentences = file.read().split('\n')
                    print sentences
                    for sentenceNum in range(len(sentences)):
                        dictKey = fileName + "_Sent:" + str(sentenceNum)

                        sentence = sentences[sentenceNum]
                        rootVerb = WordNetLemmatizer().lemmatize(target_verb,'v')
                        print rootVerb
                        if rootVerb in sentence.split() and dictKey not in dict:
                            dict[dictKey] = sentences[sentenceNum]
        count+=1

    return dict


def main():
    print extractSentencesForVerb("accuse")

main()


