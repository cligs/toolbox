#!/usr/bin/env python3
# Filename: frequencies.py

"""
# Function to build a word frequency matrix for several texts.
"""


#########################
# Basic structure
#########################

# - Open and read one TXT text file after another.
# - Calculate the word frequencies and collect them in a table.
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


def frequencies(inpath):
    """ Build token frequency matrix for set of text files."""

    ### Empty dataframe for results.
    index = []
    freqs = pd.DataFrame(index=index)

    ### Read text files and extract tokens and types
    for file in glob.glob(inpath):
        with open(file, "r") as infile:
            textname = os.path.basename(file)[:-4]
            #textnames = textnames.append(textname)
            plaintext = infile.read()
            lowertext = plaintext.lower()
            tokens = re.findall("\w+",lowertext)
            types = Counter(tokens)
            sr_types_abs = pd.Series(types, name=textname)
            sr_types_rel = sr_types_abs / len(tokens)
            #print(sum(sr_types_rel))

    ### Collect type frequencies for all texts.
            freqs = freqs.append(sr_types_rel, ignore_index=False)
            freqs = freqs.fillna(value=0)
    freqs = freqs.T
    #print(freqs[0:10])

    textnames = ["Leblanc_1920=rp141", "Leblanc_1909=rp037"]
        
    rowsums = freqs.apply(np.sum,1)
    rowsums = pd.Series(rowsums, name="rowsums")
    #print(rowsums[0:10])
    #freqs = freqs.append(rowsums, ignore_index=False)
    #print(freqs[0:10])
    #freqs_sorted = freqs.sort(columns=textnames, ascending=False)
    
    freqs_sorted = freqs

    with open("freqs.csv", "w") as outfile:
        freqs_sorted.to_csv(outfile)



#######################
# Main                #
#######################


def main(inpath):
    frequencies(inpath)


main('./test/*.txt')
