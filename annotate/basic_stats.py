#!/usr/bin/env python3
# Filename: basic_stats.py

"""
# Function to calculate some basic statistics about texts.
"""


#########################
# Basic structure
#########################

# - Open and read one TXT text file after another.
# - Calculate some basic numbers concerning the text
# - Based on these, calculate some descriptive metrics.
# - Save everything to a CSV file.



#######################
# Import statements   #
#######################

import os
import re
import glob
from collections import Counter
import pandas as pd
from itertools import groupby
import numpy as np



#######################
# Functions           #
#######################


def basic_stats(file): 
    """ Read file, calculate data, calculate metrics."""
    ### Read text files
    with open(file, "r") as infile: 
        textname = os.path.basename(file)[:-4]
        plaintext = infile.read()
        plaintext = plaintext.lower()
        tokens = re.findall("\w+",plaintext)
        #print(text)
        sr_tokens = pd.Series(tokens)
        #print(sr_tokens)
        df_tokens = pd.DataFrame(sr_tokens)
        #print(df_types)
        types = Counter(tokens)
        #print(types)
        sr_types = pd.Series(types)
        #print(sr_types)
        df_types = pd.DataFrame(sr_types)
        #print(df_types)
        sentences =  re.split("[\.|!|?]",plaintext)
        #print(sentences)

        ### Calculate some basic statistics: tokens, types, chars
        #print("\n------\n",textname)
        #print("---\nSome basic statistics")
        no_sentences = len(sentences)
        #print("Number of sentences in", textname, ":", no_sentences)
        no_types = len(sr_types)
        #print("Number of types in", textname, ":", no_types)
        no_tokens = len(sr_tokens)
        #print("Number of tokens in", textname, ":", no_tokens)
        no_tokenchars = 0 #Without whitespace. 
        for word in tokens: 
            tokenlength = len(word)
            no_tokenchars = no_tokenchars + tokenlength
        #print("Number of characters in", textname, ":", no_tokenchars)
                
        ### Calculate some basic derived metrics
        #print("---\nSome derived metrics")       
        avg_tokenlength = no_tokenchars / no_tokens
        #print("Average token length (in chars) in", textname, ":", avg_tokenlength)
        avg_sentencelength = no_tokens / no_sentences
        #print("Average sentence length (in tokens) in", textname, ":", avg_sentencelength)
        ttr = no_types / no_tokens
        #print("Type-token-ratio (TTR) for", textname, ":", ttr)
        hapax = []
        for word,freq in df_types: 
            if freq == 1:
                hapax = hapax.append(word)
        no_hapax = len(hapax)
        print("Number of hapax legomena:", no_hapax)
        
        yule1 = no_tokens
        yule2 = int(np.sum(df_types**2))
        #print(yule2)
        yuleK = 10.000 * (yule2 - yule1) / yule1**2
        #print("Yule's K characteristic for", textname, ":", yuleK)
        
        ### Combine all values for one text, combine all texts, save as a table. 
        columns = [textname]
        index = ["no_sentences", "no_types", "no_tokens", "no_tokenchars", "avg_tokenlength", "avg_sentencelength", "ttr", "yuleK"]
        #print(index)
        results = [no_sentences, no_types, no_tokens, no_tokenchars, avg_tokenlength, avg_sentencelength, ttr, yuleK]
        #print(results)
        output = pd.Series(results, index=index, name=textname)
        #print(output)
        
        all_output = pd.DataFrame(output)
        #print(all_output)
        
        with open("all_output.csv", "w") as outfile: 
            all_output.to_csv(outfile)
    
    
    
           
        
        

#######################
# Main                #
#######################


def main(inpath):
    for file in glob.glob(inpath):
        basic_stats(file)


main('./data/*.txt')
