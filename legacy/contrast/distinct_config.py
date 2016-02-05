#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: distinct_config.py
# Author: Christof Schöch

##################################################################
###  CONFIG FILE for Contrastive Genre Analysis                ###
##################################################################

################################
###   GENERAL SETTINGS       ###
################################

### Import the "distinct" module
import distinct as dt
import os
### Path to the working directory.
wdir = "/home/christof/Dropbox/0-Analysen/2015/genre10" 
### Path to the TreeTagger file (language-dependent!)
tagger = "/home/christof/Programs/TreeTagger/cmd/tree-tagger-english"

################################
###    FOCUS of ANALYSIS     ###
################################

type = "lemma"   # pos|token|lemma
mode = "enVB" # lemma: enNONE|enALL|enNN|enVB; pos: enALL|enNOP
ngrams = "uni" # pos only


################################
###    MASTERMATRIX          ###
################################

### read_tei (optional)
### Extract selected plain text from XML/TEI files.
inpath = os.path.join(wdir, "texts", "tei", "*.xml")
outfolder = os.path.join(wdir, "texts", "txt")
#dt.read_tei(inpath, outfolder)

### call_treetagger
### Perform lemmatization and POS tagging.
inpath = os.path.join(wdir, "texts", "txt", "*.txt")
outfolder = os.path.join(wdir, "texts", "tgd")
tagger = tagger
#dt.call_treetagger(inpath, outfolder, tagger) 

### select_features
### Choose selected tokens from tagged text.
inpath = os.path.join(wdir, "texts", "tgd", "*.trt")
type = type
mode = mode
ngrams = ngrams
stoplist = os.path.join(wdir, "code", "stoplist_EN-"+type+".txt")
outfolder = os.path.join(wdir, "texts", "sel", type, mode, ngrams)
dt.select_features(inpath, outfolder, mode, type, ngrams, stoplist)

### count_features
### Establish a raw frequency count of words in each document.
type = type
mode = mode
ngrams = ngrams
inpath = os.path.join(wdir, "texts", "sel", type, mode, ngrams, "*.txt")
forna = 0            # for tfidf
#forna = 0.00000001  # for rrf + specy
outfolder = os.path.join(wdir, "data")
resultfile = type+"-"+mode+"-"+ngrams+"-counts.csv"
dt.count_features(inpath, forna, outfolder, resultfile)

### build_mastermatrix
### Build a matrix combining metadata and word counts.
type = type
mode = mode
ngrams = ngrams
featurecounts = os.path.join(wdir, "data", type+"-"+mode+"-"+ngrams+"-counts.csv")
metadata = os.path.join(wdir, "texts", "metadata.csv")
outfolder = os.path.join(wdir, "data")
mastermatrixfile = "mastermatrix_"+type+"-"+mode+"-"+ngrams+".csv"
dt.build_mastermatrix(featurecounts, metadata, outfolder, mastermatrixfile)


################################
###   DISTINCTIVENESS        ###
################################

### calculate_topfeature
### Get the top-n distinctive words for a partition (term frequency inverse document frequency).
type = type
mode = mode
ngrams = ngrams
mastermatrixFile = os.path.join(wdir, "data", "mastermatrix_"+type+"-"+mode+"-"+ngrams+".csv") 
partition = "$subgenre" # $subgenre|$title|$detective|$historical|$horror
target = "detective" 
# detective|horror|historical|scifi|other 
# StudyScarlet|Parasite|Refugees|SignFour|HoundBaskervilles|MysteryCloomber|FirmGirdlestone|LostWorld|PoisonBelt|ValleyFear
outfolder = os.path.join(wdir, "results")
topfeaturesFile = os.path.join(outfolder, "topfeatures"+partition+"-"+target+"_"+type+"-"+mode+"-"+ngrams+".csv")
dt.calculate_topfeatures(mastermatrixFile, partition, target, outfolder, topfeaturesFile)

### calculate_tfidf (forna=0)
### Get the top-n distinctive words for a partition (term frequency inverse document frequency).
type = type
mode = mode
ngrams = ngrams
mastermatrixFile = os.path.join(wdir, "data", "mastermatrix_"+type+"-"+mode+"-"+ngrams+".csv") 
partition = "$subgenre" # $subgenre|$title|$detective|$historical|$horror
target = "detective" 
# detective|horror|historical|scifi|other 
# StudyScarlet|Parasite|Refugees|SignFour|HoundBaskervilles|MysteryCloomber|FirmGirdlestone|LostWorld|PoisonBelt|ValleyFear
outfolder = os.path.join(wdir, "results")
tfidfFile = os.path.join(outfolder, "tfidf_"+partition+"-"+target+"_"+type+"-"+mode+"-"+ngrams+".csv")
dt.calculate_tfidf(mastermatrixFile, partition, target, outfolder, tfidfFile)

### calculate_rrf (forna=0.00000001)
### Get the ratio of relative frequencies for two partitions
type = type
mode = mode
ngrams = ngrams
mastermatrixFile = os.path.join(wdir, "data", "mastermatrix_"+type+"-"+mode+"-"+ngrams+".csv") 
partition = "$detective"
outfolder = os.path.join(wdir, "results")
rrfFile = os.path.join(outfolder, "rrf_"+partition+"-"+target+"_"+type+"-"+mode+"-"+ngrams+".csv")
#dt.calculate_rrf(mastermatrixFile, partition, rrfFile)

### calculate_specy (specificity) (forna=0.00000001) - IN DEVELOPMENT
### Get the top-n distinctive words for a partition, as in TXM.
mastermatrixFile = wdir + "/results/mastermatrix.csv" 
partition = "$subgenre" # $subgenre|$title
target = "historical" # crime|horror|historical StudyScarlet|Parasite|Refugees|SignFour
outfolder = wdir + "/results/"
feature = "feature"
specyFile = outfolder + "specificity_"+ partition +"-"+ target +"_"+ mode +"-"+ feature +".csv"
#dt.calculate_specy(mastermatrixFile, partition, target, specyFile)







################################
###   SIGNIFICANCE           ###
################################


### test_significance
### Check whether the distribution of feature frequencies are significantly different in two partitions.
type = type
mode = mode
ngrams = ngrams
mastermatrixFile = os.path.join(wdir, "data", "mastermatrix_"+type+"-"+mode+"-"+ngrams+".csv") 
partition = "$subgenre" # $subgenre|$title|$detective|$historical|$horror
target = "detective" 
# detective|horror|historical|scifi|other 
# StudyScarlet|Parasite|Refugees|SignFour|HoundBaskervilles|MysteryCloomber|FirmGirdlestone|LostWorld|PoisonBelt|ValleyFear
outfolder = os.path.join(wdir, "results")
tfidfFile = os.path.join(outfolder, "tfidf_"+partition+"-"+target+"_"+type+"-"+mode+"-"+ngrams+".csv")
#dt.calculate_tfidf(mastermatrixFile, partition, target, outfolder, tfidfFile)


















