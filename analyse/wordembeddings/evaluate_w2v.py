#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: evaluate_w2v.py
# Author: #cf
# Version 0.1.0 (2017-07-10)


"""
Function to use word2vec models with gensim.
"""

# ==============
# Imports
# ==============

import re
import glob
import gensim
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from os.path import join
import random

#print("nx", nx.__version__)
#print("gensim", gensim.__version__)
#print("matplotlib", matplotlib.__version__)


# ==============
# Parameters
# ==============

wdir = "/media/christof/data/Dropbox/0-Analysen/2017/w2v/"
#modelfile = join(wdir, "models/frwiki17_mdt=skgr-opt=negsam-dim=300-win=6-min=100.gensim")
#modelfile = join(wdir, "models/frwiki17_mdt=skgr-opt=negsam-dim=300-win=6-min=100.gensim")
#modelfile = join(wdir, "models/frwiki17_mdt=skgr-opt=negsam-itr=20-dim=200-win=8-min=200.gensim")
#modelfile = join(wdir, "models/roman20_mdt=skgr-opt=negsam-itr=10-dim=200-win=6-min=200.gensim")
#modelfile = join(wdir, "models/roman20_mdt=skgr-opt=negsam-itr=10-dim=200-win=6-min=100.gensim")
modelfile = join(wdir, "models/roman20_mdt=skgr-opt=negsam-itr=10-dim=200-win=6-min=200.gensim")



wordlistsfile = join(wdir, "evaluation_lemma-pos.csv")

# ==============
# Functions
# ==============

def read_file(wordlistsfile):
    with open(wordlistsfile, "r") as infile:
        wordlists = infile.read()
        wordlists = re.split("\n", wordlists)
        return wordlists


def build_evaluator(wordlists):
    """
    """
    listoflists = []
    for wordlist in wordlists[:-1]:
        wordlist = [word for word in wordlist.split(",")]
        #print(wordlist)
        listoflists.append(wordlist)
    random.shuffle(listoflists)
    list1 = listoflists[0]
    list2 = listoflists[1]
    part1 = random.sample(list1,3)
    part2 = random.sample(list2,1)
    evaluator = part1+part2
    #print(evaluator)
    return evaluator


def find_mismatch(modelfile, query, truth):
    """
    Returns the term that does not belong to the list.
    """
    model = gensim.models.Word2Vec.load(modelfile)
    result = model.doesnt_match(query)
    if result == truth:
        #print("OK", query, result, truth)
        return True
    else:
        print("ERROR!", query, result, truth)



# ==============
# Main function
# ==============

def main(modelfile, wordlistsfile):
    wordlists = read_file(wordlistsfile)
    counter = 0
    score = 0
    while counter < 1000:
        evaluator = build_evaluator(wordlists)
        query = evaluator[0:4]
        truth = evaluator[3]
        print(query)
        if len(query) == 4 and len(truth) > 2: 
            counter +=1
            test = find_mismatch(modelfile, query, truth)
            if test == True:
                score +=1
            performance = score / counter * 100
            print(str(performance) + " (" + str(score) + "/" + str(counter) + ")")

main(modelfile, wordlistsfile)
















