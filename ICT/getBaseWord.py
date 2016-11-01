import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn

query = "The Indian economy is the worlds tenth largest by nominal GDP and third largest by purchasing power parity"

def is_noun(tag):
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']

def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

def is_adverb(tag):
    return tag in ['RB', 'RBR', 'RBS']

def is_adjective(tag):
    return tag in ['JJ', 'JJR', 'JJS']

def penn_to_wn(tag):
    if is_adjective(tag):
        return wn.ADJ
    elif is_noun(tag):
        return wn.NOUN
    elif is_adverb(tag):
        return wn.ADV
    elif is_verb(tag):
        return wn.VERB
    return wn.NOUN

def getBase(query, target_verb):
    tags = nltk.pos_tag(word_tokenize(query))
    for tag in tags:
        wn_tag = penn_to_wn(tag[1])
        if WordNetLemmatizer().lemmatize(tag[0],wn_tag) == target_verb:
            return True
    return False