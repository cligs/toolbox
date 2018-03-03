#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: visualize_w2v.py
# Author: #cf
# Version 0.1.0 (2017-07-10)


"""
Function to visualize a word2vec model with t-SNE.
"""

# ==============
# Imports
# ==============

import re
import glob
import pandas as pd
import gensim
from os.path import join
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import pygal


# ==============
# Parameters
# ==============

#wdir = "/home/christof/Dropbox/0-Analysen/2017/w2v/"
wdir = "/media/christof/data/Dropbox/0-Analysen/2017/w2v/"
#modelfile = join(wdir, "models/frwiki17_skgr-400dm-hsoftm-5wn-200mc.gensim")
#modelfile = join(wdir, "models/frwiki17_mdt=skgr-opt=negsam-dim=300-win=6-min=100.gensim")
#modelfile = join(wdir, "models/roman20_mdt=skgr-opt=negsam-itr=10-dim=300-win=6-min=50.gensim")
modelfile = join(wdir, "models/roman20_mdt=skgr-opt=negsam-itr=10-dim=200-win=6-min=100.gensim")
keyword = "topn-nom"
numwords = "5800"
labeltext = keyword + "-" + str(numwords)
#wordlistfile = join(wdir, "wordlists", "wordlist_"+labeltext+".txt")
wordlistfile = join(wdir, "wordlists", "wordlist_lemma-pos_topn=5800-nom.txt")
scatterplotfile = join(wdir, "visualizations", "tsne-plot_"+labeltext+".svg")


# ==============
# Functions
# ==============

from pygal.style import Style

mystyle = Style(
    font_family = "FreeSans",
    label_font_family = "FreeSans",
    label_font_size = 6,
    value_font_size = 6,
    value_label_font_size = 6,
    tooltip_font_size = 10,
    title_font_size = 18,
    stroke=False,
    show_legend = False,
    print_values = True,
    print_labels = True,
    human_readable = True,
    colors=('#1d3549', '#1d3549', '#1d3549')
)

def load_model(modelfile):
    """
    Loads an existing gensim model and returns it.
    Isolates and returns a list of the vocabulary items.
    """
    print("load_model")
    model = gensim.models.Word2Vec.load(modelfile)
    return model


def select_vocab(model, wordlistfile):
    """
    Selects only part of the entire model.
    Based on a wordlist you need to supply.
    """
    print("select_vocab")
    with open(wordlistfile, "r") as infile:
        wordlist = infile.read()
        wordlist = re.split("\n", wordlist)
        vocab = wordlist[:-1]
        model = model[vocab]
        return vocab, model


def perform_tsne(model):
    """
    Transforms the n-dimensional model to just two dimensions.
    """
    print("perform_tsne")
    tsne = TSNE(n_components=2)
    reduced_model = tsne.fit_transform(model)
    return reduced_model


def prepare_data(vocab, reduced_model):
    """
    Brings the vocabulary list and the two-dimensional data together.
    Returns a pandas dataframe.
    """
    print("prepare_data")
    data = pd.concat([pd.DataFrame(reduced_model), pd.Series(vocab)], axis=1)
    data.columns = ['x', 'y', 'word']
    #print(data.head())
    return data


def visualize_tsne(data, scatterplotfile, labeltext):
    """
    Creates and saves a scatterplot of the data with labels.
    """
    print("visualize_tsne")
    positivelist = ["sourd_nom","espéranto_nom","langue_nom","locuteur_nom","patois_nom", "syllabe_nom", "dialecte_nom", "phonème_nom", "prose_nom", "rime_nom"]
    plot = pygal.XY(style=mystyle,
        show_legend=False,
        title = "Subspace of the word2vec model for " + labeltext)
    for i in range(0,5800):
        if data.iloc[i,2] in positivelist:
            color = "red"
            size = 1
            plot.print_labels = True
            plot.add(data.iloc[i,2], [{"value": (data.iloc[i,0], data.iloc[i,1], ), "label":data.iloc[i,2][:-4], "color":color, "node": {"r": size}}])
        else:
            color = "blue"
            size = 0.7
            plot.print_labels = False
            plot.add(data.iloc[i,2], [{"value": (data.iloc[i,0], data.iloc[i,1], ), "label":data.iloc[i,2][:-4], "color":color, "node": {"r": size}}])
    plot.value_formatter=lambda x: '{:3.2f}'.format(x)
    plot.show_legend = False
    plot.render_to_file(scatterplotfile)


# ==============
# Main function
# ==============

def main(modelfile, wordlistfile, scatterplotfile, labeltext):
    model = load_model(modelfile)
    print("full model size (types):", len(model.wv.vocab))
    vocab,model = select_vocab(model, wordlistfile)
    reduced_model = perform_tsne(model)
    data = prepare_data(vocab, reduced_model)
    visualize_tsne(data, scatterplotfile, labeltext)

main(modelfile, wordlistfile, scatterplotfile, labeltext)
















