#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: locate_in_dimensions.py
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
    human_readable = True,
    title_font_size = 18,
    legend_font_size = 14,
    label_font_size = 12,
    major_label_font_size = 12,
    value_font_size = 18,
    major_value_font_size = 12,
    tooltip_font_size = 14,
    colors = ("#000099", "#000099", "#000099"))


# =================
# Basic parameters
# =================

#wdir = "/media/christof/data/Dropbox/0-Analysen/2017/w2v/"
wdir = "/home/christof/Dropbox/0-Analysen/2017/w2v/"

# =================
# Query parameters
# =================


modelfile = join(wdir, "models", "frwiki17_mdt=skgr-opt=negsam-itr=10-dim=300-win=6-min=100.gensim")
#modelfile = join(wdir, "models", "roman20_mdt=skgr-opt=negsam-itr=10-dim=300-win=6-min=50.gensim")

wordcountsfile = join(wdir, "wordlists", "wordcounts.csv")
wordcategory = "nom"
resultsfile = join(wdir, "results", "frwiki17_words-1dim_polarity-nom.csv")

#queryA1 = [["masculin_adj"], ["féminin_adj"], ["_adj"], 20]
#queryA2 = [["féminin_adj"], ["masculin_adj"], ["_adj"], 20]

#queryA1 = [["excellent_adj", "remarquable_adj", "exceptionnel_adj", "étonnant_adj", "extraordinaire_adj", "admirable_adj"], ["horrible_adj"], ["_adj"], 20]
#queryA2 = [["horrible_adj", "épouvantable_adj", "effroyable_adj", "affreux_adj", "atroce_adj"], ["excellent_adj"], ["_adj"], 20]


queryA1 = [["bonheur_nom", "beauté_nom", "joie_nom", "succès_nom", "vérité_nom"], ["malheur_nom"], "_nom", 20]
queryA2 = [["malheur_nom", "laideur_nom", "douleur_nom", "échec_nom"], ["bonheur_nom"], "_nom", 20]


#queryA1 = [["clair_adj", "lumineux_adj"], ["sombre_adj"], ["_adj"], 20]
#queryA2 = [["sombre_adj", "obscur_adj"], ["clair_adj"], ["_adj"], 20]

numwords = 500
plotfile = join(wdir, "plots", "frwiki17_words-1dim_polarity-nom.svg")
plottitle = "Words in one semantic dimension (frwiki17)"


# =================
# Functions
# =================


def get_wordlist(wordcountsfile, wordcategory, numwords):
    with open(wordcountsfile, "r") as infile:
        wordcounts = pd.DataFrame.from_csv(infile, sep=";")
        wordcounts = wordcounts[wordcounts.pos == wordcategory]
        wordlist = list(wordcounts.loc[:,"words"])
        wordlist = wordlist[0:numwords]
        return wordlist


def get_similarwords(model, query):
    """
    Returns the n words which are most similar to a list of given words.
    """
    result = model.wv.most_similar_cosmul(positive=query[0], negative=query[1], topn=query[3])
    wordlist = [item for item in query[0]]
    scorelist = [1]*len(query[0])
    for item in result:
        if item[0][-4:] in query[2]: # filters by pos
            wordlist.append(item[0])
            scorelist.append(item[1])
    print("\nwords")
    print(len(wordlist), "words")
    for word in wordlist[0:10]:
        print(word)
    print("\nscores")
    for score in scorelist[0:10]:
        print(score)
    return wordlist


def get_centroid(model, wordlist):
    vectors = []
    columns = range(0,300) # dimensions of the model
    for word in wordlist:
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


def check_distance(model, offset, wordlist, resultsfile):
    words = []
    scores = []
    for item in wordlist:
        queryvector = model[item]
        cosine = (ssd.cosine(offset, queryvector)-1)*-1 # to get cosine similarity
        words.append(item)
        scores.append(cosine)
    results = pd.DataFrame({"words":words, "scores":scores})
    results = results.sort_values(by="scores", ascending=False)
    with open(resultsfile, "w") as outfile:
        results.to_csv(outfile)
    print("\npositive words\n", results.head(10))
    print("\nnegative words\n", results.tail(10))
    print("\nsize of dataframe", results.shape)
    return results


def make_barchart(results, params, plotfile, plottitle):
    plot = pygal.HorizontalBar(
        title = plottitle,
        x_title = "Polarität",
        style = mystyle,
        show_x_guides = True,
        show_y_guides = True,
        show_legend=False,
        print_labels=False)
    for i in range(params[0], params[1]):
        plot.add(results.iloc[i,1][:-4], [{"value":results.iloc[i,0], "color":params[2]}])
    plot.render_to_file(plotfile[:-4]+"_"+params[3]+".svg")


# =================
# Main function
# =================

def main(modelfile, numwords, queryA1, queryA2, wordcountsfile, wordcategory, plotfile, plottitle, resultsfile):
    model = gensim.models.Word2Vec.load(modelfile)
    print("Model used:", modelfile)
    wordlist = get_wordlist(wordcountsfile, wordcategory, numwords)
    wordlistA1 = get_similarwords(model, queryA1)
    wordlistA2 = get_similarwords(model, queryA2)
    centroidA1 = get_centroid(model, wordlistA1)
    centroidA2 = get_centroid(model, wordlistA2)
    offset = get_offsetvector(model, centroidA1, centroidA2)
    results = check_distance(model, offset, wordlist, resultsfile)
    for params in [[0,80,"green", "pos"], [numwords-80, numwords, "red", "neg"]]:
        make_barchart(results, params, plotfile, plottitle)

main(modelfile, numwords, queryA1, queryA2, wordcountsfile, wordcategory, plotfile, plottitle, resultsfile)
