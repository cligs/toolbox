#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: gensim_word2vec.py
# Author: #cf
# Version 0.1.0 (2016-09-24)


"""
Function to try out word-to-vec with gensim.
"""


##################
# Parameters
##################

# Working Directory
WorkDir = "/"
# Path to files used for building the model.
TextPath = WorkDir + "both-lem/*.txt"
# Filename for saving/loading the model.
ModelFile = "both-lem.gensim"
# What should the script do?
Mode = ["NSimilarity"] # "BuildModel"|"PairSimilarity"|"NSimilarity"|"FourthTerm"|"DoesntMatch"



##################
# Queries
##################

# Calculate similarity score (input: two terms)
#PairSimilarity = ["machine", "outil"] 
#PairSimilarity = ["femme", "fille"] 
#PairSimilarity = ["père", "fils"] 
PairSimilarity = ["café", "cigarette"] 
#PairSimilarity = ["cigare", "cigarette"] 
#PairSimilarity = ["pipe", "cigare"] 

NSimilarity = [["police","voiture"],["automobile","flic"]]

# Calculate the most similar term.
# Input: [[positive terms], [negative terms]]
FourthTerm = [["oncle"], ["homme"]] # A+B-C=?
#FourthTerm = ["femme", "amant", "homme"] # A+B-C=?
#FourthTerm = ["ville", "époux", "homme"] # A+B-C=?
#FourthTerm = ["homme", "tante", "femme"] # A+B-C=?

# Find the term that does not belong in the list
#DoesntMatch = ["argent", "billet", "monnaie", "musée"]
DoesntMatch = ["femme", "oncle", "fille", "soeur"]





##################
# Imports
##################

import re
import glob
import gensim 



##################
# Functions
##################

def extract_sentences(TextPath): 
    """
    Turns a collection of plain text files into a list of lists of word tokens.
    It may or may not make sense to lemmatize the texts first.
    """
    print("--extract_sentences")
    Sentences = []
    for File in glob.glob(TextPath):
        with open(File, "r") as InFile: 
            Text = InFile.read()
            Text = re.sub("\n", " ", Text)
            Text = re.sub("--", "", Text)
            Text = re.sub("\.\.\.", ".", Text)
            Text = Text.lower()
            SentencesOne = []
            Text = re.split("[.!?]", Text)
            for Sent in Text: 
                Sent = re.split("\W", Sent)
                Sent = [Token for Token in Sent if Token]
                SentencesOne.append(Sent)  
            Sentences.extend(SentencesOne)
    return Sentences


def build_model(Sentences, ModelFile): 
    """
    Builds a word vector model of the text files given as input.
    """
    print("--build_model")
    Model = gensim.models.Word2Vec(Sentences, min_count=5, size=100, workers=2)
    Model.save(ModelFile)



def wordpair_similarity(ModelFile, PairSimilarity):
    """
    Returns the similarity score, between 0 and 1, for two words based on the model.
    """
    print("--word_similarity")
    Model = gensim.models.Word2Vec.load(ModelFile)
    Result = Model.similarity(PairSimilarity[0], PairSimilarity[1])
    print("Query:", PairSimilarity)
    print("Result:", Result)



def nword_similarity(ModelFile, NSimilarity):
    """
    Returns the similarity score, between 0 and 1, for two words based on the model.
    """
    print("--word_similarity")
    Model = gensim.models.Word2Vec.load(ModelFile)
    Result = Model.similarity(NSimilarity[0], NSimilarity[1])
    print("Query:", NSimilarity)
    print("Result:", Result)



def fourth_term(ModelFile, FourthTerm):
    """
    Returns the most similar term for a set of positive and negative terms.
    """
    print("--fourth_term")
    Model = gensim.models.Word2Vec.load(ModelFile)
    Result = Model.most_similar(positive=[Word for Word in FourthTerm[0]], 
                                negative=[Word for Word in FourthTerm[1]], 
                                topn=3)
    print("Query:", FourthTerm)
    print("Result:", Result)


def doesnt_match(ModelFile, DoesntMatch):
    """
    Returns the term that does not belong to the list.
    """
    print("--doesnt_match")
    Model = gensim.models.Word2Vec.load(ModelFile)
    Result = Model.doesnt_match([Word for Word in DoesntMatch])
    print("Query:", DoesntMatch)
    print("Result:", Result)




################
# Main function
################

def main(Mode, TextPath, ModelFile, 
         PairSimilarity, NSimilarity, FourthTerm, DoesntMatch):
    print("Launched.")
    print("Model used:", ModelFile)
    
    if "BuildModel" in Mode: 
        Sentences = extract_sentences(TextPath)
        build_model(Sentences, ModelFile)
    if "PairSimilarity" in Mode:
        wordpair_similarity(ModelFile, PairSimilarity)
    if "NSimilarity" in Mode:
        nword_similarity(ModelFile, NSimilarity)
    if "FourthTerm" in Mode: 
        fourth_term(ModelFile, FourthTerm)
    if "DoesntMatch" in Mode: 
        doesnt_match(ModelFile, DoesntMatch)
        
    
    print("Done.")
    
main(Mode, TextPath, ModelFile, 
     PairSimilarity, NSimilarity, FourthTerm, DoesntMatch)