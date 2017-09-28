#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: get_wordcounts.py
# Author: #cf
# Version 0.1.0 (2017-07-12)


"""
Function to extract word counts from model.
"""


#=============
# Imports
#=============

import re
import glob
import gensim
import pandas as pd
from os.path import join


# =================
# Basic parameters
# =================

wdir = "/media/christof/data/Dropbox/0-Analysen/2017/w2v/"
#wdir = "/home/Dropbox/0-Analysen/2017/w2v/"


# =================
# Query parameters
# =================

modelfile = join(wdir, "models", "frwiki17_mdt=skgr-opt=negsam-itr=10-dim=300-win=6-min=100.gensim")
#modelfile = join(wdir, "models", "roman20_mdt=skgr-opt=negsam-itr=10-dim=300-win=6-min=50.gensim")

resultsfile = join(wdir, "wordlists", "wordcounts-frwiki17.csv")

#=============
# Functions
#=============

def get_vocabulary(model):
    """
    Retrieve a list of all types in the model's vocabulary.
    """
    vocabulary = model.wv.vocab
    vocabulary = list(vocabulary.keys())
    vocabulary = vocabulary
    return vocabulary


def get_counts(model, vocabulary):
    """
    Returns the word count for each type in the vocabulary.
    """
    print("get_count")
    counts = []
    for word in vocabulary: 
        count = model.wv.vocab[word].count
        counts.append(count)
    return counts


def get_pos(vocabulary):
    pos = [item[-3:] for item in vocabulary]
    #print(pos[0:10])    
    return pos
    


def save_results(vocabulary, results, resultsfile):
    """
    Merge the vocabulary and the counts into a dataframe.
    Save the dataframe to file.
    """
    results = results.sort_values(by="counts", axis=0, ascending=False)
    with open(resultsfile, "w") as outfile:
        results.to_csv(outfile, sep=";")
    print(results.head())
    

#=============
# Main function
#=============

def main(modelfile, resultsfile):
    print("Model used:", modelfile)
    model = gensim.models.Word2Vec.load(modelfile)
    vocabulary = get_vocabulary(model)
    counts = get_counts(model, vocabulary)
    pos = get_pos(vocabulary)
    results = pd.DataFrame({"counts":counts, "words":vocabulary, "pos":pos})    
    save_results(vocabulary, results, resultsfile)

main(modelfile, resultsfile)
