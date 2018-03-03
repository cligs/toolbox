#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: call_treetagger.py
# Authors: cf


import csv
import os
import glob
import re
from os.path import join
import treetaggerwrapper as ttw

wdir = "/home/christof/Documents/frwiki17/"
plaintextpath = join(wdir, "plain-text/*.txt")
taggedfolder = join(wdir, "annotated", "")
preparedfolder = join(wdir, "lemma-pos", "")
stoplistfile = join(wdir, "stoplist_fr.txt")


# ==================
# TreeTagger
# ==================

def call_ttw(file, language):
    tagger = ttw.TreeTagger(TAGLANG=language)
    with open(file, "r") as textfile:
        text = textfile.read()
        text = re.sub("’","'", text)
        tagged = tagger.tag_text(text)
        tagged = '\n'.join([line for line in tagged if line])
        #print(tagged)
        return tagged


def save_results(tagged, outfolder, filename):
    print("saving", filename) 
    outfile = join(outfolder, filename)
    with open(outfile, "w") as out:
        out.write(tagged)


def run_treetagger(plaintextpath, language, taggedfolder):
    print("prepare_text")
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    for file in glob.glob(plaintextpath):
        filename,ext = os.path.basename(file).split(".")
        filename = filename + ".csv"
        tagged = call_ttw(file, language)
        save_results(tagged, taggedfolder, filename)


#run_treetagger(plaintextpath, language, taggedfolder)


# ==================
# Prepare texts
# ==================


def read_csv(file):
    """
    Open and read the CSV files containing the tagged text.
    Returns a string.
    """
    #print("read_csv")
    with open(file, newline="\n") as infile:
        tagged = []
        rawtext = csv.reader(infile, delimiter="\t")
        for item in rawtext:
            tagged.append(item)
        return tagged


def read_stoplist(stoplistfile):
    """
    Open and read the file with stopwords to be filtered out.
    One word per line.
    Returns a list of words. 
    """
    #print("read_stoplist")
    with open(stoplistfile, "r") as infile: 
        stoplist = infile.read()
        stoplist = re.split("\n", stoplist)
        return stoplist


def build_tokens(tagged, stoplist):
    """
    Based on the tagged text, and applying some rules,
    build and select specific tokens.
    Returns each sentence on one line.
    Currently: returns lemmata with pos. 
    """
    #print("build_tokens")
    tokens = []
    for item in tagged:
        #print(item)
        if len(item) == 3:
            word = item[0]
            pos = item[1][0:3]
            lemma = item[2]
            if "|" in lemma and len(word) > 2 and lemma not in stoplist:
                tokens.append(word + "_" + pos)
            elif pos == "SEN":
                tokens.append("  \n") # does this create the "\nWORD"-problem?
            elif len(lemma) > 2 and lemma not in stoplist:
                tokens.append(lemma + "_" + pos)
    tokens = ' '.join([token.lower() for token in tokens])
    tokens = re.sub("\n ","\n",tokens)
    #print(tokens[0:1000])
    return tokens


def save_results(prepared, filename):
    """
    Saves the series of tokens to a text file for further usage. 
    """
    #print("save_results") 
    with open(filename, "w") as out:
        out.write(prepared)


def prepare_text(taggedfolder, stoplistfile, preparedfolder):
    """
    Input: Texts annotated with TreeTagger.
    Output: Text in which each token is modeled as "lemma_pos".
    """
    #print("prepare_text")
    if not os.path.exists(preparedfolder):
        os.makedirs(preparedfolder)
    for file in glob.glob(taggedfolder + "*.csv"):
        filename,ext = os.path.basename(file).split(".")
        print("preparing", filename)
        filename = join(preparedfolder, filename + ".txt")
        tagged = read_csv(file)
        stoplist = read_stoplist(stoplistfile)
        prepared = build_tokens(tagged, stoplist)
        save_results(prepared, filename)


prepare_text(taggedfolder, stoplistfile, preparedfolder)
