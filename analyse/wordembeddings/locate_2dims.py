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
from sklearn import preprocessing as prp

#print("nx", nx.__version__)
#print("gensim", gensim.__version__)
#print("matplotlib", matplotlib.__version__)

mystyle = pygal.style.Style(
    background='white',
    plot_background='white',
    font_family="FreeSans",
    human_readable = True,
    title_font_size = 16,
    legend_font_size = 12,
    label_font_size = 12,
    major_label_font_size = 12,
    value_font_size = 14,
    major_value_font_size = 12,
    tooltip_font_size = 12,
    colors = ("#000099", "#000099", "#000099"))


# =================
# Basic parameters
# =================

wdir = "/media/christof/data/Dropbox/0-Analysen/2017/w2v/"
#wdir = "/home/Dropbox/0-Analysen/2017/w2v/"

#modelfile = join(wdir, "models", "frwiki17_mdt=skgr-opt=negsam-itr=10-dim=300-win=6-min=100.gensim")
modelfile = join(wdir, "models", "roman20_mdt=skgr-opt=negsam-itr=10-dim=300-win=6-min=50.gensim")

#wordcountsfile = join(wdir, "wordlists", "wordcounts-frwiki17.csv")
wordcountsfile = join(wdir, "wordlists", "wordcounts-roman20.csv")

# =================
# Query parameters
# =================

#wordcategory = "nom"
#numwords = 1000
#queryA1 = [["bonheur_nom", "amour_nom", "plaisir_nom", "bienfait_nom", "joie_nom"], ["malheur_nom"], "_nom", 50]
#queryA2 = [["malheur_nom", "laideur_nom", "douleur_nom", "crime_nom", "erreur_nom"], ["bonheur_nom"], "_nom", 50]
#queryA1 = [["homme_nom"], ["femme_nom"], "_nom", 50]
#queryA2 = [["femme_nom"], ["homme_nom"], "_nom", 50]
#queryB1 = [["lumière_nom", "clarté_nom", "soleil_nom"], ["obscurité_nom"], "_nom", 20]
#queryB2 = [["obscurité_nom", "sommeil_nom", "cave_nom"], ["lumière_nom"], "_nom", 20]
#queryA1 = [["amour_nom", "bonheur_nom", "joie_nom", "succès_nom", "richesse_nom"], ["horreur_nom"], ["_nom"], 20]
#queryA2 = [["horreur_nom", "erreur_nom", "échec_nom", "manque_nom", "atrocité_nom"], ["bonheur_nom"], ["_nom"], 20]
#queryA1 = [["mère_nom", "femme_nom"], ["homme_nom"], ["_nom"], 5]
#queryA2 = [["père_nom", "homme_nom"], ["femme_nom"], ["_nom"], 5]


#wordcategory = "nom"
#numwords = 1000
#queryA1 = [["bonheur_nom", "beauté_nom", "joie_nom", "succès_nom"], ["malheur_nom"], "_nom", 10]
#queryA2 = [["malheur_nom", "laideur_nom", "douleur_nom", "échec_nom"], ["bonheur_nom"], "_nom", 10]
#queryB1 = [["théorie_nom", "esprit_nom", "raison_nom", "idée_nom", "système_nom", "hypothèse_nom"], ["sentiment_nom"], "_nom", 10]
#queryB2 = [["sentiment_nom", "affection_nom", "émotion_nom"], ["esprit_nom"], "_nom", 10]

wordcategory = "nom"
numwords = 3000
queryA1 = [["bonheur_nom", "beauté_nom", "joie_nom", "succès_nom"], ["malheur_nom"], "_nom", 10]
queryA2 = [["malheur_nom", "laideur_nom", "douleur_nom", "échec_nom"], ["bonheur_nom"], "_nom", 10]
queryB1 = [["réalité_nom", "évidence_nom", "preuve_nom"], ["rêve_nom"], "_nom", 10]
queryB2 = [["rêve_nom", "imagination_nom"], ["réalité_nom"], "_nom", 10]



#wordcategory = "adj"
#numwords = 500
#queryA1 = [["excellent_adj", "remarquable_adj", "exceptionnel_adj", "étonnant_adj", "extraordinaire_adj", "admirable_adj"], ["horrible_adj"], ["_adj"], 20]
#queryA2 = [["horrible_adj", "épouvantable_adj", "effroyable_adj", "affreux_adj", "atroce_adj"], ["excellent_adj"], ["_adj"], 20]
#queryB1 = [["raisonnable_adj"], ["passionnel_adj"], "_adj", 20]
#queryB2 = [["passionnel_adj"], ["raisonnable_adj"], "_adj", 20]
#queryB1 = [["sombre_adj", "obscur_adj", "souterrain_adj"], ["clair_adj"], "_adj", 20]
#queryB2 = [["clair_adj", "lumineux_adj", "aveuglant_adj"], ["sombre_adj"], "_adj", 20]



#wordcategory = "adj"
#numwords = 1000
#queryA1 = [["sombre_adj", "obscur_adj", "souterrain_adj"], ["clair_adj"], "_adj", 20]
#queryA2 = [["clair_adj", "lumineux_adj", "aveuglant_adj"], ["sombre_adj"], "_adj", 20]
#queryB1 = [["lent_adj", "vieux_adj", "antique_adj"], ["rapide_adj"], ["_adj"], 20]
#queryB2 = [["rapide_adj", "jeune_adj", "bref_adj"], ["lent_adj"], ["_adj"], 20]


resultsfile = join(wdir, "results", "roman20_words-2dim_nom.csv")
plotfile = join(wdir, "plots", "roman20_words-2dim_nom.svg")
plottitle = "Words in two semantic dimensions (roman20)"




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
    wordlist = []
    scorelist = []
    for item in result:
        if item[0][-4:] in query[2]: # filters by pos
            wordlist.append(item[0])
            scorelist.append(item[1])
    print(wordlist[0:10])
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
    

def check_distance(model, offsetA, offsetB, query3, resultsfile):
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
    results.sort_values(by="scoresB", ascending=False, inplace=True)
    print("\n\n", results.head(), "\n", results.tail())
    results.sort_values(by="scoresA", ascending=False, inplace=True)
    print("\n\n", results.head(), "\n", results.tail())
    with open(resultsfile, "w") as outfile:
        results.to_csv(outfile)
    return results


def get_colors(numwords, xvals, yvals):
    colors = []
    scaler = prp.MinMaxScaler(feature_range=(0,255))
    xvals = scaler.fit_transform(xvals.reshape(-1,1))
    scaler = prp.MinMaxScaler(feature_range=(0,255))
    yvals = scaler.fit_transform(yvals.reshape(-1,1))
    for i in range(0,numwords): 
        r = int(yvals[i])
        g = int(xvals[i])      
        b = int(yvals[i])        
        color = "rgb"+str((r,g,b))
        colors.append(color)
    #print(colors)
    return colors
    


def plot_results(results, numwords, plotfile, plottitle):
    colors = get_colors(numwords, xvals=results.iloc[:,0], yvals=results.iloc[:,1])
    print("plot_results")
    plot = pygal.XY(
        title = plottitle,
        x_title = "<= negatif | positif =>",
        y_title = "<= rêve | réalité  =>",
        style = mystyle,
        show_x_guides = True,
        show_y_guides = True,
        show_legend=False,
        print_labels=False)
    for i in range(0,numwords):
        plot.add(results.iloc[i,2][:-4], [{"value":(float('{:04.3f}'.format(results.iloc[i,0])),float('{:04.3f}'.format(results.iloc[i,1]))), "color":colors[i]}], dots_size=2)
    plot.render_to_file(plotfile)
    


# =================
# Main function
# =================

def main(modelfile, queryA1, queryA2, queryB1, queryB2, wordcountsfile, wordcategory, numwords, resultsfile, plotfile, plottitle):
    model = gensim.models.Word2Vec.load(modelfile)
    wordlist = get_wordlist(wordcountsfile, wordcategory,numwords)
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
    results = check_distance(model, offsetA, offsetB, wordlist, resultsfile)
    plot_results(results, numwords, plotfile, plottitle)

main(modelfile, queryA1, queryA2, queryB1, queryB2, wordcountsfile, wordcategory, numwords, resultsfile, plotfile, plottitle)
