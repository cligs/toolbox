#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: contrast_config.py
# Author: Christof Schöch

##################################################################
###  CONFIG FILE for: Contrastive Genre Analysis               ###
##################################################################

################################
###   GENERAL SETTINGS       ###
################################

import contrast
### Path to the working directory.
wdir = "" # end with slash; empty if wdir = current dir.
### Path to the TreeTagger file (language-dependent!)
tagger = "/home/christof/Programs/TreeTagger/cmd/tree-tagger-english"


################################
###    PREPROCESSING         ###
################################

### read_tei (optional)
### Extract selected plain text from XML/TEI files.
inpath = wdir + "data/tei/*.xml"
outfolder = wdir + "data/txt/"
contrast.read_tei(inpath,outfolder)

### call_treetagger
### Perform lemmatization and POS tagging.
infolder = wdir + "data/txt/"
outfolder = wdir + "data/tgd/"
tagger = tagger
contrast.call_treetagger(infolder, outfolder, tagger) 

### select_tokens
### Choose selected tokens from tagged text.
inpath = wdir + "data/tgd/*.trt"
outfolder = wdir + "data/sel/"
mode = "enNONE" # enNONE = english-no named entities
contrast.select_tokens(inpath, outfolder, mode)



################################
###    BASIC CORPUS DATA     ###
################################

### count_words
### Establish a raw frequency count of words in each document.
inpath = wdir + "data/sel/*.txt"  # sel|txt
outfolder = wdir + "results/"
resultfile = "wordcounts.csv"
contrast.count_words(inpath, outfolder, resultfile)

### build_mastermatrix
### Build a matrix combining metadata and word counts.
wordcounts = wdir + "results/wordcounts.csv"
metadata = wdir + "data/metadata.csv"
outfolder = wdir + "results/"
mastermatrixfile = "mastermatrix.csv"
contrast.build_mastermatrix(wordcounts, metadata, outfolder, mastermatrixfile)


################################
###   BASIC STATISTICS       ###
################################

### get_summarystats
### Get a number of basic statistical indicators about the collection.
mastermatrixfile = wdir + "results/mastermatrix.csv" 
summarystatsfile = wdir + "summarystats.csv"
outfolder = wdir + "results/"
contrast.get_summarystats(mastermatrixfile, outfolder, summarystatsfile)


### get_relativefreqs
### Get the relative frequencies of each token in each text.
mastermatrixfile = wdir + "results/mastermatrix.csv" 
summarystatsfile = wdir + "summarystats.csv"
contrast.get_relativefreqs(mastermatrixfile, summarystatsfile)


################################
###   CONTRASTIVE STATISTICS ###
################################

### calculate_ratioRelFreqs
### Get the ratio of relative frequencies for two partitions
mastermatrixfile = wdir + "results/mastermatrix.csv" 
partition = "$subgenre"
outfolder = wdir + "results/"
ratioRelFreqsFile = outfolder + "ratioRelFreqs.csv"
contrast.calculate_ratioRelFreqs(mastermatrixfile, partition, ratioRelFreqsFile)










