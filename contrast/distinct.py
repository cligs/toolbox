#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: distinct.py
# Author: Christof Schöch

##################################################################
###  MASTERMATRIX for Contrastive Genre Analysis               ###
##################################################################

import re
import os
import glob
import pandas as pd
import numpy as np


#################################
# read_tei                      #
#################################

from lxml import etree
#print("Using LXML version: ", etree.LXML_VERSION)

def read_tei(inpath, outfolder):
    """Script for reading selected text from TEI P5 files."""
    print("\nLaunched read_tei.")

    if not os.path.exists(outfolder):
        os.makedirs(outfolder)     
        
    for file in glob.glob(inpath):
        with open(file, "r"):
            filename = os.path.basename(file)[:-4]
            #print(filename[:5]) # = idno

            ### The following options may help with parsing errors.
            #parser = etree.XMLParser(collect_ids=False, recover=True)
            parser = etree.XMLParser(recover=True)
            xml = etree.parse(file, parser)
            
            ### The TEI P5 files do have a default namespace.
            namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}
            ### Removes tags but conserves their text content.
            etree.strip_tags(xml, "{http://www.tei-c.org/ns/1.0}seg")

            ### Removes elements and their text content.
            #etree.strip_elements(xml, "speaker")
            etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}note")
            #etree.strip_elements(xml, "stage")
            etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}head")

            ### XPath defining which text to select
            xp_bodytext = "//tei:body//text()"
            #xp_alltext = "//text()"

            ### Applying one of the above XPaths
            text = xml.xpath(xp_bodytext, namespaces=namespaces)
            text = "\n".join(text)

            ### Some cleaning up
            text = re.sub("[ ]{1,20}", " ", text)
            text = re.sub("\t\n", "\n", text)
            text = re.sub("\n{1,10}", "\n", text)
            text = re.sub("\n \n", "\n", text)
            text = re.sub("\n.\n", "\n", text)
            text = re.sub("[ ]{1,20}", " ", text)

            outtext = str(text)
            outfile = outfolder + filename + ".txt"
        with open(outfile,"w") as output:
            output.write(outtext)
    print("Done.")
    


#################################
# call_treetagger               #
#################################

def call_treetagger(inpath, outfolder, tagger):
    """Function to call TreeTagger from Python"""
    print("\nLaunched call_treetagger.")
    import subprocess

    counter = 0    
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)

    for file in glob.glob(inpath): 
        #print(os.path.basename(infile))
        counter+=1
        outfile = os.path.join(outfolder, os.path.basename(file)[:-4]+".trt")
        #print(outfile)
        command = tagger + " < " + file + " > " + outfile
        subprocess.call(command, shell=True)
    print("Files treated: ", counter)
    print("Done.")



#################################
# select_features               #
#################################

def select_features(inpath, outfolder, mode, type, ngrams, stoplist):
    """Function to extract features from TreeTagger output."""
    print("\nLaunched select_features.")

    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    with open(stoplist, "r") as stopfile: 
        stoplist = stopfile.read()
    counter = 0
    for file in glob.glob(inpath):
        with open(file,"r") as infile:
            counter+=1
            text = infile.read()
            splittext = re.split("\n",text)
            
            features = []
            for line in splittext:
                splitline = re.split("\t",line)
                if len(splitline) == 3:
                    lemma = splitline[2]
                    pos = splitline[1]
                    token = splitline[0]
                    ## Choose features according to parameters "mode" and "torl"
                    if type == "lemma": 
                        if mode == "enNONE":
                            if "<unknown>" not in lemma and "@card@" not in lemma and "NP" not in pos:
                                features.append(lemma.lower())               
                        elif mode == "enALL":
                            if "<unknown>" not in lemma and "@card@" not in lemma:
                                features.append(lemma.lower())               
                        elif mode == "enNN":
                            if "@card@" not in lemma and "<unknown>" not in lemma and "'" not in token and "NN" in pos:
                                features.append(lemma.lower())               
                        elif mode == "enVB":
                            if "@card@" not in lemma and "<unknown>" not in lemma and "'" not in token and "VB" in pos and "boarding" not in token and "branded" not in token and "good-humor" not in lemma:
                                features.append(lemma.lower())               
                        elif mode == "enADJ":
                            if "@card@" not in lemma and "<unknown>" not in lemma and "'" not in token and "JJ" in pos:
                                features.append(lemma.lower())               
                        elif mode == "enCC":
                            if "@card@" not in lemma and "<unknown>" not in lemma and "'" not in token and "CC" in pos:
                                features.append(lemma.lower())               
                        elif mode == "enADV":
                            if "@card@" not in lemma and "<unknown>" not in lemma and "'" not in token and "RB" in pos:
                                features.append(lemma.lower())               
                    elif type == "token": 
                        if mode == "enNONE":
                            if "<unknown>" not in lemma and "@card@" not in lemma and "NP" not in pos:
                                features.append(token.lower())               
                        elif mode == "enALL":
                            if "<unknown>" not in lemma and "@card@" not in lemma:
                                features.append(token.lower())               
                        elif mode == "enNN":
                            if "@card@" not in lemma and "<unknown>" not in lemma and "'" not in token and "NN" in pos:
                                features.append(token.lower())               
                    elif type == "pos": 
                        if mode == "enALL":
                            if "<unknown>":
                                features.append(pos)
                        elif mode == "enNOP":
                            pos = re.sub("\$","", pos)
                            pos = re.sub(",","PUNC", pos)
                            pos = re.sub("\'\'","PUNC", pos)
                            pos = re.sub("LS","PUNC", pos)
                            pos = re.sub("``","PUNC", pos)
                            pos = re.sub(":","PUNC", pos)
                            pos = re.sub(";","PUNC", pos)
                            pos = re.sub("!","PUNC", pos)
                            pos = re.sub("!","PUNC", pos)
                            pos = re.sub("\(","PUNC", pos)
                            pos = re.sub("\)","PUNC", pos)
                            if "SENT" not in pos and "PUNC" not in pos and "SYM" not in pos:
                                features.append(pos)
            #print(features[0:10])
            
            ## Continue with list of features, but remove undesired features         
            if type == "lemma": 
                features = ' '.join([feature for feature in features if len(feature) > 1 and feature not in stoplist])
                features = re.sub("[ ]{1,4}"," ", features)
                features = re.sub("'","",features)

            if type == "pos" and ngrams == "uni":
                features = ' '.join([feature for feature in features if feature not in stoplist])
                #print(lemmata)

            if type == "pos" and ngrams == "bi": 
                bigrams = []
                for i in range(0, len(features)-1):
                    bigram = features[i]+"+"+features[i+1]
                    bigrams.append(bigram)
                features = bigrams
                features = ' '.join([feature for feature in features])

            ## For all cases, save files.        
            #print(features[0:50])
            newfilename = os.path.basename(file)[:-4]+".txt"
            with open(os.path.join(outfolder, newfilename),"w") as output:
                output.write(str(features))
    print("Files treated: ", counter)
    print("Done.")


#################################
# count_features                #
#################################

from collections import Counter

def count_features(inpath, forna, outfolder, resultfile): 
    """Establish a raw frequency count of words in each document."""
    print("Launched count_features.")

    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    results = pd.DataFrame()
    for file in glob.glob(inpath):
        with open(file, "r") as infile:
            filename = os.path.basename(file)[:-4]
            text = infile.read()
            #print(filename, text[0:100])
            
            ## Prepare the text
            text = text.lower()
            #text = re.split("\W", text)
            text = re.split(" ", text)
            filtered = []
            for token in text: 
                if len(token) > 0: 
                    filtered.append(token)
            text = filtered
            #print(text[0:100])
 
            ## Count words and collect results
            word_count = Counter(text)
            word_count = pd.Series(word_count, name=filename)
            #print(word_count)
            results = results.append(word_count, ignore_index=False)
    results = results.fillna(forna)            
    results = results.T
    #results['rowsums'] = results.sum(axis=1)
    #results = results.sort("rowsums", ascending=False)
    #print(results.head(), results.tail())
        
    ## Save dataframe to file
    outfilename = os.path.join(outfolder, resultfile)
    print(outfilename)
    with open(outfilename, "w") as out:
        results.to_csv(out, sep=',', encoding='utf-8')
    print("Done.")


#################################
# build_mastermatrix            #
#################################

def build_mastermatrix(wordcounts, metadata, outfolder, mastermatrixfile): 
    """Build a matrix combining metadata and word counts."""
    print("Launched build_mastermatrix.")

    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    
    with open(metadata, "r") as infile: 
        metadata = pd.DataFrame.from_csv(infile)
    #print(metadata.head())
    with open(wordcounts, "r") as infile: 
        wordcounts = pd.DataFrame.from_csv(infile)
        wordcounts = wordcounts.T
        wordcounts["idno"] = wordcounts.index
    #print(wordcounts.head())
    mastermatrix = pd.merge(metadata, wordcounts, how="inner", on="idno")
    #print(mastermatrix.head())
    
    ## Save dataframe to file
    outfilename = os.path.join(outfolder,mastermatrixfile)
    with open(outfilename, "w") as out:
        mastermatrix.to_csv(out, sep=',', encoding='utf-8')
    ## Save dataframe to file (reading version)
    outfilename = os.path.join(outfolder,mastermatrixfile[:-4]+"_T.csv")
    mastermatrix = mastermatrix.T
    with open(outfilename, "w") as out:
        mastermatrix.to_csv(out, sep=',', encoding='utf-8')
    print("Done.")
    
    

##################################################################
###  Distinctiveness Measures for Contrastive Genre Analysis   ###
##################################################################



#################################
# calculate_rrf                 #
#################################


## TODO: Make sure items with a joint frequency of less than 5 get excluded.

def calculate_rrf(mastermatrixFile, partition, rrfFile):
    """Calculate the ratio of relative frequencies for two partitions."""
    print("Launched get_ratioRelFreqs.") 
    
    with open(mastermatrixFile, "r") as infile: 
        mastermatrix = pd.DataFrame.from_csv(infile)
        #print(mastermatrix)
        
        ## Partition the collection into two groups based on metadata
        partitioned = mastermatrix.groupby(partition).sum()
        #partitioned.dropna(axis=1, how="any", inplace=True)
        #print(partitioned)
        
        ## Calculate relative token frequencies
        tokennumber_perpartition = partitioned.iloc[0:,14:].sum(axis=1)
        #print(tokennumber_perpartition)        
        tokenfreqs_absolute = partitioned.iloc[:,14:-1]
        #print(tokenfreqs_absolute)
        tokenfreqs_relative = tokenfreqs_absolute.div(tokennumber_perpartition, axis=0)
        #print(tokenfreqs_relative)

        ## Calculate the ratio of relative frequencies, for each token        
        rrf = tokenfreqs_relative.iloc[0,14:-1] / tokenfreqs_relative.iloc[1,14:-1]
        rrf = 1/rrf
        rrf.sort(ascending=False)
        print("===\nRatio of relative frequencies for "+partition+", extreme values:")
        print(rrf.head(20), rrf.tail(20))
        rrf.to_csv(rrfFile[:-4]+"_"+partition+".csv", index=True, sep=',')
        print("===")
    print("Done.")
    


#################################
# calculate_tf-idf              #
#################################

def calculate_tfidf(mastermatrixFile, partition, target, outfolder, tfidfFile): 
    """Get the top-n distinctive words for a partition."""
    print("Launched calculate_tfidf")

    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    
    with open(mastermatrixFile, "r") as infile: 
        mastermatrix = pd.DataFrame.from_csv(infile)
        #print(mastermatrix)

        ## Split mastermatrix into metadata and values
        metadata = mastermatrix.iloc[:,0:14]
        valuematrix = mastermatrix.iloc[:,14:]
        ## Binarize the part of the values
        valuematrix[valuematrix > 0] = 1
        #print(valuematrix)
        ## Join the matrices again
        binarymatrix = pd.merge(metadata, valuematrix, how="inner", left_index=True, right_index=True)
        #print(binarymatrix)
        ## Get the document frequencies for entire collection
        collDocFreqs = binarymatrix.iloc[:,14:].sum()
        #print(collDocFreqs)
        
        ## Partition the collection based on metadata
        partitioned = mastermatrix.groupby(partition).sum()
        partitioned.drop("$pubyear", axis=1, inplace=True) # Why is this still here?       
        ## Get (absolute) frequencies for target among partitions
        targetFreqs = partitioned.loc[target,:]
        #print(targetFreqs)
        targetLength = targetFreqs.sum()
        #print(targetLength)
        targetFreqsRel = targetFreqs.div(targetLength, axis=0) * 100000
        #print(targetFreqsRel)
                        
        ## Compute the tf-idf scores
        tf = targetFreqsRel
        #print("==tf==\n", tf)
        df = collDocFreqs 
        #print("==df==\n", df)
        N = len(mastermatrix)
        #print("==N==\n", N)
        idf = np.log(N/df)
        #print("==idf==\n", idf)
        tfidf = tf*idf
        tfidf.order(ascending=False, inplace=True)
        print("\n== Top 20 tfidf for "+target+" among "+partition+" ==\n", tfidf[0:20])
        tfidf.to_csv(tfidfFile, index=True, sep=',')
        print("Done.")






#################################
# calculate_specy (specificity) #                  IN DEVELOPMENT
#################################

def calculate_specy(mastermatrixFile, partition, target, specyFile): 
    """Get the top-n distinctive words for a partition."""
    print("Launched calculate_specificity")
    
    with open(mastermatrixFile, "r") as infile: 
        mastermatrix = pd.DataFrame.from_csv(infile)
        #print(mastermatrix)

        ## Split mastermatrix into metadata and values
        #metadata = mastermatrix.iloc[:,0:10]
        valuematrix = mastermatrix.iloc[:,15:]
        ## Sum over all texts
        collFreqs = valuematrix.sum()
        #print(collFreqs)
        ## Transform values to relative frequencies
        collSize = collFreqs.sum()
        
        ## Partition the collection based on metadata
        partitioned = mastermatrix.groupby(partition).sum()
        partitioned.drop("$pubyear", axis=1, inplace=True) # Why is this still here?       
        ## Get (absolute) frequencies for target among partitions
        targetFreqs = partitioned.loc[target,:]
        #print(targetFreqs)
        targetSize = targetFreqs.sum()
        #print(targetLength)
        targetFreqsRel = targetFreqs.div(targetSize, axis=0) * 100000
        #print(targetFreqsRel)
                        
        ## Compute the specificity scores
        ## Rename in accordance with TXM scheme
        f = targetFreqs
        #print("== f ==:", f)
        t = targetSize
        #print("== t ==:", t)
        F = collFreqs
        #print("== F ==:", F)
        T = collSize
        #print("== t ==:", T)

        ## Do actual calculation     
        ## TODO: Replace this dummy calculation by the real thing!     
        ft = f.div(t)
        FT = F.div(T) 
        specy = ft.div(FT)
        specy.order(ascending=False, inplace=True)
         
        print("\n== Top 20 specy for "+target+" among "+partition+" ==\n", specy[0:20])
        specy.to_csv(specyFile, index=True, sep=',')
        print("Done.")



#################################
# calculate_topfeatures         #
#################################

def calculate_topfeatures(mastermatrixFile, partition, target, outfolder, topfeaturesFile): 
    """Get the top-n most frequent words for a partition."""
    print("Launched calculate_topfeatures")

    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    
    with open(mastermatrixFile, "r") as infile: 
        mastermatrix = pd.DataFrame.from_csv(infile)
        #print(mastermatrix)

        ## Split mastermatrix into metadata and values
        metadata = mastermatrix.iloc[:,0:14]
        valuematrix = mastermatrix.iloc[:,14:]
        ## Binarize the part of the values                                        ### Why is this being done??? ###
        valuematrix[valuematrix > 0] = 1
        #print(valuematrix)
        ## Join the matrices again
        binarymatrix = pd.merge(metadata, valuematrix, how="inner", left_index=True, right_index=True)
        #print(binarymatrix)
        ## Get the document frequencies for entire collection
        collDocFreqs = binarymatrix.iloc[:,14:].sum()
        #print(collDocFreqs)
        
        ## Partition the collection based on metadata
        partitioned = mastermatrix.groupby(partition).sum()
        partitioned.drop("$pubyear", axis=1, inplace=True) # Why is this still here?       
        ## Get (absolute) frequencies for target among partitions
        targetFreqs = partitioned.loc[target,:]
        #print(targetFreqs)
        targetLength = targetFreqs.sum()
        #print(targetLength)
        targetFreqsRel = targetFreqs.div(targetLength, axis=0) * 100000
        #print(targetFreqsRel)
                        
        ## Compute the tf-idf scores
        topfeatures = targetFreqsRel
        topfeatures.order(ascending=False, inplace=True)
        print("\n== Top 20 features for "+target+" among "+partition+" ==\n", topfeatures[0:20])
        topfeatures.to_csv(topfeaturesFile, index=True, sep=',')
        print("Done.")










