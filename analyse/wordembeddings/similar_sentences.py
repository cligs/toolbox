#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: similar_sentences.py
# Author: #cf
# Version 0.1.0 (2017-08-18)


"""
Function to find sentences with similar meaning in a large collection of texts using a word2vec model built with gensim.
The script takes tagged text as input, where a text file consists of one line per sentence and each word is represented in the form "lemma_POS", separated by a single whitespace. 
"""


# =================
# Imports
# =================

from os.path import join
import re
import glob
import gensim
import pandas as pd
import numpy as np
import itertools

# =================
# Parameters
# =================

wdir = "/media/christof/data/Dropbox/0-Analysen/2017/w2v/"
#wdir = "/home/christof/Dropbox/0-Analysen/2017/w2v/"

modelfile = join(wdir, "models", "frwiki17_mdt=skgr-opt=negsam-itr=10-dim=300-win=6-min=100.gensim")
#modelfile = join(wdir, "models", "roman20_mdt=skgr-opt=negsam-itr=10-dim=300-win=6-min=50.gensim")

textfile = join(wdir, "texts", "rv0008.txt")


# =================
# Functions
# =================


def read_tagged(textfile):
    print(textfile)
    with open(textfile, "r") as infile:
        text = infile.read()
        return text


def make_sentences(text):
    sentences = re.split("\n", text)
    #print(sentences[0:5])
    return sentences


def select_lemmata(sentences):
    selectedsentences = []
    for sent in sentences[0:1000]:
        sent = re.split(" ", sent)
        sent = [lemma for lemma in sent if lemma[-4:] in ["_nom"]]#, "_ver"]]
        if len(sent) == 4:
            print(sent)
            selectedsentences.append(sent)
    #print(len(selectedsentences), "sentences")
    return selectedsentences


def compare_sentencepairs(model, sentpair):
    sentsims = []
    for word1 in sentpair[0]:
        wordsims = []        
        for word2 in sentpair[1]:
            try: 
                wordsim = model.similarity(word1, word2)
                #print(word1, word2, wordsim)
                wordsims.append(wordsim)
            except:
                break
            try: 
                maxwordsim = max(wordsims)
                sentsims.append(maxwordsim)
            except:
                break
    overallsentsim = np.mean(sentsims)
    #print(overallsentsim)
    return overallsentsim
        



# =================
# Main function
# =================

def main(modelfile, textfile):
    model = gensim.models.Word2Vec.load(modelfile)
    text = read_tagged(textfile)
    sentences = make_sentences(text)
    selectedsentences = select_lemmata(sentences)
    allsentencepairs = itertools.combinations(selectedsentences, 2)
    for sentpair in allsentencepairs:
        sentsim = compare_sentencepairs(model, sentpair)
        if sentsim > 0.6: 
            print("\n", sentpair[0], "\n", sentpair[1], "\n Similarity:", sentsim)
       
main(modelfile, textfile)





















def wordpair_similarity(Model, PairQuery):
    """
    Returns the similarity score, between 0 and 1, for two words based on the model.
    """
    print("--word_similarity")
    Result = Model.similarity(PairQuery[0], PairQuery[1])
    print("Query:", PairQuery)
    print("Result:", Result)



def nword_similarity(Model, NWordsQuery):
    """
    Returns the similarity score, between 0 and 1, for two words based on the model.
    """
    print("--word_similarity")
    Result = Model.n_similarity(NWordsQuery[0], NWordsQuery[1])
    print("Query:", NWordsQuery)
    print("Result:", Result)


def several_similarity(Model, SeveralSimQuery):
    """
    Returns the terms most similar to a group of words.
    """
    print("several_similarity")
    Result = Model.wv.most_similar_cosmul(positive=SeveralSimQuery[0], negative=SeveralSimQuery[1], topn=SeveralSimQuery[2])
    print("Query:", SeveralSimQuery)
    for item in SeveralSimQuery[0]:
        print(item)
    for Item in Result:
        print(Item[0])
    #print("Result:", Result)
    wordlist = ""
    for item in SeveralSimQuery[0]:
        wordlist = wordlist + item + "\n"
    for item in Result:
        #print(item[0], "\t", item[1])
        wordlist = wordlist + item[0] + "\n"
    with open("wordlist.txt", "w") as outfile:
        outfile.write(wordlist)




def similar_words(Model, SimilarQuery):
    """
    Returns the n words which are most similar in the data.
    """
    print("--similar_words")
    Result = Model.similar_by_word(SimilarQuery[0], SimilarQuery[1])
    print("Query:", SimilarQuery)
    wordlist = SimilarQuery[0]+"\n"
    for item in Result:
        print(item[0], "\t", item[1])
        wordlist = wordlist + item[0] + "\n"
    with open("wordlist.txt", "w") as outfile:
        outfile.write(wordlist)
    return Result


