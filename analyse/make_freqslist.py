#!/usr/bin/env python3
# Filename: make_freqslist.py
# Author: #cf
# Date: 2016


"""
Creates an overall relative frequency list for items in a text collection.
Items can be raw word tokens, lowercase word tokens, or lemmata (using TreeTagger).
Data can be relative frequency per 1000 words or proportion of texts containing item at least once.
TODOs: Solution for frequent apostrophe'd / hyphenated words; Complete punctuation. 
"""


#####################
# Parameters
#####################

WorkDir = "/" # ends on slash
TextPath = WorkDir + "test/*.txt"
Modes = ["raw-words", "lower-words", "lemmata"] # raw-words|lower-words|lemmata
Types = ["props", "freqs"] #props|freqs
Tokenizer = "[\W]"
Punctuation = "[.,:;!?«»\(\)]"
FreqFilePrefix = "fr-20th-novel"



#####################
# Import statements
#####################

import os
import re
import glob
import pandas as pd
from collections import Counter
import treetaggerwrapper as ttw


#####################
# Functions
#####################

def read_file(File):
    """
    # Read a text file and return as string.
    """
    with open(File, "r") as InFile: 
        Text = InFile.read()
        Filename, Ext = os.path.basename(File).split(".")
    return Text


def get_words(Text, Tokenizer, Punctuation):
    """
    Turn a string into a list of word tokens (excluding punctuation).
    """
    Text = re.sub("peut-être", "peut_être", Text)
    Text = re.sub("aujourd'hui", "aujourd_hui", Text)  
    Text = re.sub("après-midi", "après_midi", Text)  
    Text = re.sub("d'ailleurs", "d_ailleurs", Text)  
    Text = re.sub("c'est-à-dire", "c_est_à_dire", Text)  
    Words = re.split(Tokenizer, Text)
    Words = [Word for Word in Words if len(Word) != 0]
    Words = [Word for Word in Words if Word not in Punctuation]
    return Words


def get_lower(Text, Tokenizer, Punctuation):
    """
    Same as words, but also makes all items lowercase. 
    """
    Words = get_words(Text, Tokenizer, Punctuation)
    Lower = [Word.lower() for Word in Words]
    return Lower

def get_lemmata(Text, Punctuation):
    tagger = ttw.TreeTagger(TAGLANG='fr')
    Tagged = tagger.tag_text(Text)
    Lemmata = []
    AmbLemmata = []
    for Item in Tagged: 
        Item = re.split("\t", Item)
        Lemma = Item[2]
        if Lemma == "d": 
            Lemma = "de"
        if Lemma == "n": 
            Lemma = "ne"
        if Lemma == "l": 
            Lemma = "le"
        if Lemma == "j": 
            Lemma = "je"
        if Lemma == "t": 
            Lemma = "tu"
        if Lemma == "qu": 
            Lemma = "que"
        if Lemma == "la|le": 
            Lemma = "la"
        if Lemma == "sommer|être": 
            Lemma = "être"
        if Lemma == "suivre|être": 
            Lemma = "être"
        if Lemma == "foi|fois": 
            Lemma = "fois"
        if Lemma == "ouvrer|ouvrir": 
            Lemma = "ouvrir"
        if Lemma == "sen|sens": 
            Lemma = "sens"
        if Lemma == "jacque|jacques": 
            Lemma = "jacques"
        if "|" in Lemma: 
            AmbLemmata.append(Lemma)
            Lemma = re.split("\|", Lemma)[0]
        Lemmata.append(Lemma)
    AmbLemmata = Counter(AmbLemmata)
    Lemmata = [Lemma for Lemma in Lemmata if Lemma not in Punctuation]
    Lemmata = [Lemma for Lemma in Lemmata if Lemma not in ["--", "---", "...", "@card@", "@ord@"]]
    return Lemmata
    

def get_itemfreqs(AllItems, Type, Mode, TextCounter):
    """
    Get the overall frequency of each item in the text collection.
    Calculate relative frequency or proportion of texts containing the item.
    Sort by descending frequency / proportion, transform to DataFrame.
    """    
    ItemFreqs = Counter(AllItems)
    ItemFreqs = pd.DataFrame.from_dict(ItemFreqs, orient="index").reset_index()
    ItemFreqs.columns = [Mode, "freqs"]
    ItemFreqs.sort_values(["freqs", Mode], ascending=[False, True], inplace=True)
    ItemFreqs = ItemFreqs.reset_index(drop=True)
    if Type == "freqs":
        ItemFreqsRel = pd.DataFrame(ItemFreqs.loc[:,"freqs"].div(len(AllItems))*1000)
        ItemFreqsRel.columns = ["per1000"]
        ItemFreqs = pd.concat([ItemFreqs, ItemFreqsRel], axis=1, join="outer")
        ItemFreqs = ItemFreqs.drop("freqs", axis=1)
    elif Type == "props": 
        ItemFreqsRel = pd.DataFrame(ItemFreqs.loc[:,"freqs"].div(TextCounter)*100)
        ItemFreqsRel.columns = ["in%texts"]
        ItemFreqs = pd.concat([ItemFreqs, ItemFreqsRel], axis=1, join="outer")
        ItemFreqs = ItemFreqs.drop("freqs", axis=1)
    return ItemFreqs


def save_csv(ItemFreqs, FreqFilePrefix, Type, Mode): 
    """
    Save to file.
    """
    ItemFreqsFile = WorkDir + FreqFilePrefix +"_"+ Type +"-"+ Mode+".csv"
    print("Saving", os.path.basename(ItemFreqsFile))
    with open(ItemFreqsFile, "w") as OutFile: 
        ItemFreqs.to_csv(OutFile)



####################
# Main
####################

def main(TextPath, Modes, Types, Tokenizer, Punctuation, FreqFilePrefix): 
    print("Launched.")
    for Type in Types:
        for Mode in Modes: 
            AllItems = []
            TextCounter = 0
            for File in glob.glob(TextPath): 
                TextCounter +=1
                Text = read_file(File)
                if Mode == "raw-words": 
                    Words = get_words(Text, Tokenizer, Punctuation)
                    if Type == "props":
                        Words = list(set(Words))
                    AllItems = AllItems + Words
                if Mode == "lower-words": 
                    Lower = get_lower(Text, Tokenizer, Punctuation)
                    if Type == "props":
                        Lower = list(set(Lower))
                    AllItems = AllItems + Lower
                if Mode == "lemmata": 
                    Lemmata = get_lemmata(Text, Punctuation)
                    if Type == "props":
                        Lemmata = list(set(Lemmata))
                    AllItems = AllItems + Lemmata
            ItemFreqs = get_itemfreqs(AllItems, Type, Mode, TextCounter)
            save_csv(ItemFreqs, FreqFilePrefix, Type, Mode)    
    print("Done.")

main(TextPath, Modes, Types, Tokenizer, Punctuation, FreqFilePrefix)






