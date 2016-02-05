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


def basic_stats(inpath):
    """ Read files, calculate data, calculate metrics, save results."""

    ### Empty dataframe for results.
    #index = ["no_sent", "no_types", "no_tokens", "no_hapax", "no_chars", "no_syll", "avg_tokenlen", "avg_sentlen", "ttr", "htyr", "htor", "yuleK", "fk"]
    index = ["no_sent", "no_types", "no_tokens", "no_hapax"]
    all_output = pd.DataFrame(index=index)
    all_output = all_output.T
    #print(all_output)

    ### Read text files
    for file in glob.glob(inpath):
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
            sr_hapax = sr_types[sr_types < 2]
            #print(sr_hapax)

    ### Calculate some basic statistics: tokens, types, chars
            #print("\n------\n",textname)
            #print("---\nSome basic statistics")
            no_sentences = len(sentences)
            #print("Number of sentences in", textname, ":", no_sentences)
            no_types = len(sr_types)
            #print("Number of types in", textname, ":", no_types)
            no_tokens = len(sr_tokens)
            #print("Number of tokens in", textname, ":", no_tokens)
            no_hapax = len(sr_hapax)
            #print(no_hapax)
            """
            no_tokenchars = 0 #Without whitespace.
            for word in tokens:
                tokenlength = len(word)
                no_tokenchars = no_tokenchars + tokenlength
            #print("Number of characters in", textname, ":", no_tokenchars)
            no_syllables = 0  #Very much simplified definition of syllable!
            for word in tokens:
                for letter in word:
                    if letter == "a" or letter == "e" or letter == "i" or letter == "o" or letter == "u" or letter == "y":
                        no_syllables += 1
            #print(no_syllables)
            """

            """
            ### Calculate some basic derived metrics
            #print("---\nSome derived metrics")
            avg_tokenlength = no_tokenchars / no_tokens
            #print("Average token length (in chars) in", textname, ":", avg_tokenlength)
            avg_sentencelength = no_tokens / no_sentences
            #print("Average sentence length (in tokens) in", textname, ":", avg_sentencelength)
            ttr = no_types / no_tokens
            #print("Type-token-ratio (TTR) for", textname, ":", ttr)
            htyr = no_hapax / no_types #Relative to number of types, not tokens.
            #print(htyr)
            htor = no_hapax / no_tokens #Relative to number of tokens not types.
            #print(htor)
            yule_indicator = int(np.sum(df_types**2))
            #print(yule2)
            yuleK = 10.000 * (yule_indicator - no_tokens) / no_tokens**2
            #print("Yule's K characteristic for", textname, ":", yuleK)

            fleshkincaid = (0.39 * no_tokens / no_sentences) + ( 11.8 * no_syllables) / no_tokens - 15.59
            #print(fleshkincaid)
            """

            ### Combine all values for one text, combine all texts, save as a table.
            columns = [textname]
            index = index
            #print(index)
            #results = [no_sentences, no_types, no_tokens, no_hapax, no_tokenchars, no_syllables, avg_tokenlength, avg_sentencelength, ttr, htyr, htor, yuleK, fleshkincaid]
            results = [no_sentences, no_types, no_tokens, no_hapax]
            #print(results)
            output = pd.Series(results, index=index, name=textname)
            #print(output)

            all_output = all_output.append(output, ignore_index=False)
            #print(all_output)

    with open("results.csv", "w") as outfile:
        all_output.to_csv(outfile)


#######################
# Main                #
#######################


def main(inpath):
    basic_stats(inpath)


main('./data/*.txt')
