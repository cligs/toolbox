#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: locate_in_dimensions.py
# Author: #cf
# Version 0.2.0 (2017-07-31)


"""
Script to do sentiment analysis of sentences based on word2vec.
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
import itertools

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
# Parameters
# =================

wdir = "/media/christof/data/Dropbox/0-Analysen/2017/w2v/"
#wdir = "/home/Dropbox/0-Analysen/2017/w2v/"

#modelfile = join(wdir, "models", "roman20_mdt=skgr-opt=negsam-itr=10-dim=300-win=6-min=50.gensim")
modelfile = join(wdir, "models", "frwiki17_mdt=skgr-opt=negsam-itr=10-dim=300-win=6-min=100.gensim")
topicfile = join(wdir, "topics-with-words_100tp-2000it-100in.csv")
plotfile = join(wdir, "plots", "roman20_topic-coherences.svg")
numwords = 12

# =================
# Functions
# =================


def get_topics(topicfile):
    with open(topicfile, "r") as infile:
        topics = pd.read_csv(infile, sep=";",
            header=None,
            index_col=None,
            names=["topic", "score", "words"])
        return topics 

def get_coherences(model, topics, numwords):
    coherences = []
    for i in range(0,topics.shape[0]):
        words = topics.iloc[i,2] 
        words = re.split(" ", words)
        words = words[0:numwords]
        words = [word for word in words if "xxx" not in word]
        combinations = itertools.permutations(words,2)
        similarities = []
        for item in combinations: 
            similarities.append(model.similarity(item[0], item[1]))
        coherences.append(np.mean(similarities))
    topics["coherence"] = coherences
    results = topics[["topic", "score", "coherence", "words"]]
    results = results.sort_values(by="coherence", ascending=False)
    #print(results.head())
    return results
    
def save_results(topics):
    with open("topics-with-coherences.csv", "w") as outfile:
        topics.to_csv(outfile)


def plot_results(results, plotfile, numwords):
    plot = pygal.Bar(show_legend=False,
        title="Topic coherences based on word2vec",
        style=mystyle)
    for i in range(0,100):
        words = re.split(" ", results.iloc[i,3])
        words = [word[:-4] for word in words[0:numwords]]
        words = "-".join(words)
        plot.add(str(results.iloc[i,0]), [{"value":results.iloc[i,2], "label": words, "color":"darkgreen", "formatter": lambda x: '{:04.2f}'.format(x)}])
    plot.render_to_file(plotfile)
        

# =================
# Main function
# =================

def main(modelfile, topicfile, numwords, plotfile):
    model = gensim.models.Word2Vec.load(modelfile)
    topics = get_topics(topicfile)
    results = get_coherences(model, topics, numwords)
    save_results(results)
    plot_results(results, plotfile, numwords)

main(modelfile, topicfile, numwords, plotfile)











