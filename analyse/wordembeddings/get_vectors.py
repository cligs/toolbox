#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: query_w2v.py
# Author: #cf
# Version 0.2.0 (2017-07-31)


"""
Script to identify vectors between abstractions from words.
Similar to what Ryan Heuser does here: http://ryanheuser.org/word-vectors-3/
"""


# =================
# Import statements
# =================

from os.path import join
import re
import glob
import gensim
import pandas as pd
import numpy as np
from scipy.spatial import distance as ssd
import pygal

#print("nx", nx.__version__)
#print("gensim", gensim.__version__)
#print("matplotlib", matplotlib.__version__)

mystyle = pygal.style.Style(
    background='white',
    plot_background='white',
    font_family="FreeSans",
    title_font_size = 18,
    legend_font_size = 14,
    label_font_size = 20,
    major_label_font_size = 12,
    value_font_size = 20,
    major_value_font_size = 12,
    tooltip_font_size = 12)


# =================
# Basic parameters
# =================

wdir = "/media/christof/data/Dropbox/0-Analysen/2017/w2v/"
#wdir = "/home/Dropbox/0-Analysen/2017/w2v/"
#modelfile = join(wdir, "models", "frwiki17_mdt=skgr-opt=negsam-itr=10-dim=300-win=6-min=100.gensim")
modelfile = join(wdir, "models", "roman20_mdt=skgr-opt=negsam-itr=10-dim=300-win=6-min=50.gensim")


# =================
# Query parameters
# =================

# query: list of positive words, list of negative words, part of speech, number of words to give back
wordlistfile = join(wdir, "roman20_top1000.txt") 
queryA1 = [["corps_nom", "chaise_nom"], ["esprit_nom"], "_nom", 200]
queryA2 = [["esprit_nom", "pensée_nom", "bonté_nom"], ["corps_nom"], "_nom", 200]
queryB1 = [["beauté_nom", "bonheur_nom"], ["laid_adj"], "_nom", 200]
queryB2 = [["haine_nom", "laideur_nom"], ["beau_adj"], "_nom", 200]


# =================
# Functions
# =================


def get_wordlist(wordlistfile):
    with open(wordlistfile, "r") as infile:
        wordlist = infile.read()
        wordlist = [word for word in re.split("\n", wordlist) if word]
        print(wordlist[0:10])
        return wordlist

def get_similarwords(model, query):
    """
    Returns the n words which are most similar to a list of given words.
    """
    result = model.wv.most_similar_cosmul(positive=query[0], negative=query[1], topn=query[3])
    wordlist = []
    scorelist = []
    for item in result:
        if query[2] in item[0]: 
            wordlist.append(item[0])
            scorelist.append(item[1])
    #print(wordlist[0:10])
    #print(len(wordlist), "words")
    #print(scorelist)
    return wordlist
    #wordlist = "\n".join([word for word in wordlist])
    #with open("wordlist.txt", "w") as outfile:
    #    outfile.write(wordlist)


def get_centroid(model, wordlist):
    vectors = []
    columns = range(0,300)
    for word in wordlist:
        #print(word)
        vector = model[word]
        vectors.append(vector)
    alldata = pd.DataFrame(vectors, columns=columns, index=wordlist)
    centroid = np.mean(alldata, axis=0)
    #print(centroid[0:3])
    return centroid


def get_offsetvector(model, centroid1, centroid2):
    offset = centroid1 - centroid2
    #print(offset[0:3])
    return offset
    

def check_distance(model, offsetA, offsetB, query3):
    words = []
    scoresA = []
    scoresB = []
    for item in query3: 
        queryvector = model[item]
        cosineA = (ssd.cosine(offsetA, queryvector)-1)*-1 # to get cosine similarity
        cosineB = (ssd.cosine(offsetB, queryvector)-1)*-1 # to get cosine similarity
        words.append(item)
        scoresA.append(cosineA)
        scoresB.append(cosineB)
        #print(item, cosineA, cosineB)
    results = pd.DataFrame({"words":words, "scoresA":scoresA, "scoresB":scoresB})
    #results = results.sort_values(by=["scoresA", "scoresB"], ascending=False)
    print(results.head())
    print(results.shape)
    return results


def plot_results(results):
    plot = pygal.XY(
        style = mystyle,
        show_legend=False,
        print_labels=False)
    for i in range(0,1000):
        plot.add(results.iloc[i,2], [{"value":(results.iloc[i,0],results.iloc[i,1]), "label":results.iloc[i,2], "color":"blue"}])
    plot.render_to_file("words-on-opposition.svg")
    


# =================
# Main function
# =================

def main(modelfile, queryA1, queryA2, queryB1, queryB2, wordlistfile):
    model = gensim.models.Word2Vec.load(modelfile)
    wordlist = get_wordlist(wordlistfile)
    print("Model used:", modelfile)
    wordlistA1 = get_similarwords(model, queryA1)
    wordlistA2 = get_similarwords(model, queryA2)
    wordlistB1 = get_similarwords(model, queryB1)
    wordlistB2 = get_similarwords(model, queryB2)
    centroidA1 = get_centroid(model, wordlistA1)
    centroidA2 = get_centroid(model, wordlistA2)
    centroidB1 = get_centroid(model, wordlistB1)
    centroidB2 = get_centroid(model, wordlistB2)
    offsetA = get_offsetvector(model, centroidA1, centroidA2)
    offsetB = get_offsetvector(model, centroidB1, centroidB2)
    results = check_distance(model, offsetA, offsetB, wordlist)
    plot_results(results)

main(modelfile, queryA1, queryA2, queryB1, queryB2, wordlistfile)
