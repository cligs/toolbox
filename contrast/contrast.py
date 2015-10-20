#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: contrast.py
# Author: Christof Schöch

##################################################################
###  Contrastive Genre Analysis                                ###
##################################################################

# TODO: Use os.path.join everywhere for cross-platform compatibility.

import re
import os
import glob
import pandas as pd


##################################################################
###  PREPROCESSING                                             ###
##################################################################


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

def call_treetagger(infolder, outfolder, tagger):
    """Function to call TreeTagger from Python"""
    print("\nLaunched call_treetagger.")
    import subprocess

    inpath = infolder + "*.txt"
    infiles = glob.glob(inpath)
    counter = 0
    
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)

    for infile in infiles: 
        #print(os.path.basename(infile))
        counter+=1
        outfile = outfolder + os.path.basename(infile)[:-4] + ".trt"
        #print(outfile)
        command = tagger + " < " + infile + " > " + outfile
        subprocess.call(command, shell=True)
    print("Files treated: ", counter)
    print("Done.")



#################################
# select_tokens                 #
#################################

def select_tokens(inpath, outfolder, mode):
    """Function to extract tokens from TreeTagger output."""
    print("\nLaunched select_tokens.")

    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    counter = 0
    for file in glob.glob(inpath):
        with open(file,"r") as infile:
            counter+=1
            text = infile.read()
            splittext = re.split("\n",text)
            
            tokens = []
            for line in splittext:
                splitline = re.split("\t",line)
                if len(splitline) == 3:
                    lemma = splitline[2]
                    pos = splitline[1]
                    token = splitline[0]
                    ## Choose tokens / lemmata according to parameter "mode"
                    if mode == "enNONE":
                        if "<unknown>" not in lemma and "NP" not in pos:
                            tokens.append(lemma.lower())               
                    elif mode == "enALL":
                        if "<unknown>" not in lemma:
                            tokens.append(lemma.lower())               
            tokens = ' '.join([word for word in tokens])
            newfilename = os.path.basename(file)[:-4] + ".txt"
            #print(outfolder, newfilename)
            with open(os.path.join(outfolder, newfilename),"w") as output:
                output.write(str(tokens))
    print("Files treated: ", counter)
    print("Done.")



##################################################################
###  BASIC CORPUS DATA (mastermatrix)                          ###
##################################################################


#################################
# count_words                   #
#################################

from collections import Counter

def count_words(inpath, outfolder, resultfile): 
    """Establish a raw frequency count of words in each document."""
    print("Launched count_words.")

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
            text = re.split("\W", text)
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
    results = results.fillna(0.0000000001)            
    results = results.T
    #results['rowsums'] = results.sum(axis=1)
    #results = results.sort("rowsums", ascending=False)
    #print(results.head(), results.tail())
        
    ## Save dataframe to file
    outfilename = outfolder+resultfile
    with open(outfilename, "w") as out:
        results.to_csv(out, sep=',', encoding='utf-8')
    print("Done.")


#################################
# build_mastermatrix            #
#################################

def build_mastermatrix(wordcounts, metadata, outfolder, mastermatrixfile): 
    """Build a matrix combining metadata and word counts."""
    print("Launched build_mastermatrix.")
    
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
    outfilename = outfolder+mastermatrixfile
    with open(outfilename, "w") as out:
        mastermatrix.to_csv(out, sep=',', encoding='utf-8')
    print("Done.")
    


##################################################################
###  BASIC STATISTICS                                          ###
##################################################################


#################################
# get_summarystats              #
#################################

def get_summarystats(mastermatrixfile, outfolder, summarystatsfile): 
    """Get a number of basic statistical indicators about the collection."""
    print("Launched get_summarystats.")
    
    with open(mastermatrixfile, "r") as infile: 
        mastermatrix = pd.DataFrame.from_csv(infile)
        #print(mastermatrix)

    summarystats = mastermatrix.iloc[:,0:8]
    #print(summarystats)

    ## Total number of tokens in each text
    texts_tokennumber = mastermatrix.iloc[0:,8:].sum(axis=1)
    #print(texts_tokennumber)
    
    summarystats["totaltokens"] = texts_tokennumber
    #print(summarystats)

    ## Total frequency of each token in the collection
    #coll_tokenfreqs = mastermatrix.iloc[0:,8:].sum(axis=0)
    #print(coll_tokenfreqs)    
    #mastermatrix = mastermatrix.append(coll_tokenfreqs, ignore_index=True)
    #print(mastermatrix)


    ## Save dataframe to file
    outfilename = outfolder+summarystatsfile
    with open(outfilename, "w") as out:
        summarystats.to_csv(out, sep=',', encoding='utf-8')
    print("Done.")



#################################
# get_relativefreqs             #
#################################

def get_relativefreqs(mastermatrixfile, summarystatsfile):
    """Get the relative frequencies of each token in each text."""
    print("Launched get_relativefreqs.") 
    
    with open(mastermatrixfile, "r") as infile: 
        mastermatrix = pd.DataFrame.from_csv(infile)
        #print(mastermatrix)
       
        ## Relative frequencies of each token in each text
        tokennumber_pertext = mastermatrix.iloc[0:,8:].sum(axis=1)
        #print(tokennumber_pertext)        
        tokenfreqs_absolute = mastermatrix.iloc[:,8:-1]
        #print(tokenfreqs_absolute)
        
        tokenfreqs_relative = tokenfreqs_absolute.div(tokennumber_pertext, axis=0)
        print(tokenfreqs_relative)
    print("Done.")
        


##################################################################
###  CONTRASTIVE STATISTICS                                    ###
##################################################################



#################################
# calculate_ratioRelFreqs       #
#################################

## TODO: Make sure items with a joint frequency of less than 5 get excluded.

def calculate_ratioRelFreqs(mastermatrixfile, partition, ratioRelFreqsFile):
    """Calculate the ratio of relative frequencies for two partitions."""
    print("Launched get_ratioRelFreqs.") 
    
    with open(mastermatrixfile, "r") as infile: 
        mastermatrix = pd.DataFrame.from_csv(infile)
        #print(mastermatrix)
        
        ## Partition the collection into two groups based on metadata
        partitioned = mastermatrix.groupby(partition).sum()
        partitioned.dropna(axis=1, how="any", inplace=True)
        #print(partitioned)
        
        ## Calculate relative token frequencies
        tokennumber_perpartition = partitioned.iloc[0:,8:].sum(axis=1)
        #print(tokennumber_perpartition)        
        tokenfreqs_absolute = partitioned.iloc[:,8:-1]
        #print(tokenfreqs_absolute)
        tokenfreqs_relative = tokenfreqs_absolute.div(tokennumber_perpartition, axis=0)
        #print(tokenfreqs_relative)

        ## Calculate the ratio of relative frequencies, for each token        
        ratioRelFreqs = tokenfreqs_relative.iloc[0,8:-1] / tokenfreqs_relative.iloc[1,8:-1]
        ratioRelFreqs.sort(ascending=False)
        print("===\nRatio of relative frequencies, extreme values:")
        print(ratioRelFreqs.head(30), ratioRelFreqs.tail(30))
        print("===")
    print("Done.")
    


#################################
# calculate_Zeta                #
#################################


# 1. Partition the data into two partions (reuse from ratioRelFreqs), based on "sel" files.
# 2. Segment each text into segments (reuse from tmw) 
# 3. Build word_count matrix with data for each segment 
# 4. Build mastermatrix
# 5. Reduce mastermatrix to binary format per segment
# 6. Add up segment scores to full texts again
# 7. Apply ratio of relative frequencies






















































