#!/usr/bin/env python3
# Filename: make_freqslist.py
# Author: #cf
# Date: 2016


"""
Creates an overall item frequency list for a corpus.
Items can be raw tokens, word tokens, lowercase word tokens, or lemmas.
TODOs: Solution for frequent apostrophe'd words; Lemma mode. 
"""


#####################
# Parameters
#####################

WorkDir = "/media/christof/data/Dropbox/0-Analysen/2016/wordlist/"
TextPath = WorkDir + "txt/*.txt"
Modes = ["tokens", "words", "lower"] # tokens|words|lower|lemmas
Tokenizer = "\W"
Punctuation = "[.,:;!?«»]"



#####################
# Import statements
#####################

import os
import re
import glob
import pandas as pd
from collections import Counter
#import treetaggerwrapper


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
        #print(Filename, "; chars:", len(Text))
    return Text


def get_tokens(Text, Tokenizer):
    """
    Turn a string into a list of tokens.
    """
    Text = re.sub("peut-être", "peut_être", Text)
    Text = re.sub("aujourd'hui", "aujourd_hui", Text)    
    Tokens = re.split(Tokenizer, Text)
    Tokens = [Token for Token in Tokens if len(Token) != 0]
    #print(Tokens[0:10])
    #print("Tokens,", len(Tokens))
    return Tokens


def get_words(Text, Tokenizer, Punctuation):
    """
    Same as Tokens, but exclude punctuation.
    """
    Tokens = get_tokens(Text, Tokenizer)
    Words = [Word for Word in Tokens if Word not in Punctuation]
    #print(Words[0:10])
    #print("word tokens,", len(Words))
    return Words


def get_lower(Text, Tokenizer, Punctuation):
    """
    Same as words, but also makes all items lowercase. 
    """
    Words = get_words(Text, Tokenizer, Punctuation)
    Lower = [Word.lower() for Word in Words]
    #print(Lower[0:10])
    #print("lower word tokens,", len(Lower))    
    return Lower

def get_lemmas(Text):
    """
    Same as lower, but reduces all forms to their lemma.
    """
    return Lemmas

def get_itemfreqs(AllItems):
    """
    Get the overall frequency of each item in the text collection.
    """
    ItemFreqs = Counter(AllItems)
    #print(ItemFreqs.most_common(10))
    return ItemFreqs

def save_csv(ItemFreqs, Mode): 
    """
    Transform to DataFrame, sort descending, save to file.
    """
    ItemFreqs = pd.DataFrame.from_dict(ItemFreqs, orient="index").reset_index()
    ItemFreqs.columns = [Mode, "freqs"]
    ItemFreqs.sort_values(["freqs", Mode], ascending=[False, True], inplace=True)
    ItemFreqs = ItemFreqs.reset_index(drop=True)
    #print(ItemFreqs.head())
    #print(ItemFreqs.iloc[100:105,:])
    #print(ItemFreqs.iloc[1000:1005,:])
    #print(ItemFreqs.iloc[-5:,:])
    ItemFreqsFile = WorkDir + "wordlist_"+Mode+".csv"
    with open(ItemFreqsFile, "w") as OutFile: 
        ItemFreqs.to_csv(OutFile)



####################
# Main
####################


def main(TextPath, Modes, Tokenizer, Punctuation): 
    print("Launched.")
    for Mode in Modes: 
        print("Getting", Mode)
        AllItems = []
        for File in glob.glob(TextPath): 
            Text = read_file(File)
            if Mode == "tokens": 
                Tokens = get_tokens(Text, Tokenizer)
                AllItems = AllItems + Tokens
            if Mode == "words": 
                Words = get_words(Text, Tokenizer, Punctuation)
                AllItems = AllItems + Words
            if Mode == "lower": 
                Lower = get_lower(Text, Tokenizer, Punctuation)
                AllItems = AllItems + Lower
            #elif Mode == "lemmas": 
                #Lemmas = get_lemmas(Text)
                #    AllItems = AllItems + Lemmas
        ItemFreqs = get_itemfreqs(AllItems)
        save_csv(ItemFreqs, Mode)    
    print("Done.")

main(TextPath, Modes, Tokenizer, Punctuation)






