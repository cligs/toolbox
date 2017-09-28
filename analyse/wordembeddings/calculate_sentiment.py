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

lexiconfile = join(wdir, "lexicon", "roman20_words-by-1dim_nva.csv")
#text = ["homme_nom pousser_ver cri_nom épouvantable_adj mourir_ver", "gracieux_adj virtuosité_nom artiste_nom faire_ver bonheur_nom", "salle_nom être_ver vieux_adj chaise_nom bois_nom vert_adj"]
text = ["vicimte_nom escroquerie_nom", "méfiance_nom passion_nom caractère_nom"]

# L'homme poussa un cri épouvantable avant de mourir.
# La gracieuse virtuosité des artistes faisait son bonheur.
# Dans la salle était une vielle chaise en bois vert.

# James Sherwood fut la victime d'une des plus célèbres escroqueries de tous les temps.


# =================
# Functions
# =================


def read_lexiconfile(lexiconfile):
    with open(lexiconfile, "r") as infile:
        lexicon = pd.DataFrame.from_csv(infile)
        #print(lexicon.head())
        return lexicon


def get_scores(lexicon, sentence):
    scores  = []
    sentence = [token for token in re.split(" ", sentence)]
    print(sentence)
    lexicon = lexicon[lexicon.words.isin(sentence)]
    print(lexicon)
    score = np.mean(lexicon.loc[:,"scores"])*10
    print(score)



# =================
# Main function
# =================

def main(lexiconfile, text):
    lexicon = read_lexiconfile(lexiconfile)
    for sentence in text:
        scores = get_scores(lexicon, sentence)

main(lexiconfile, text)
