#!/usr/bin/env python3
# Filename: mallet2wordle.py

"""
# Transform MALLET output for visualization with wordle.net.
"""


#########################
# Remarks
#########################

# Takes as input the MALLET output file containing rows of topic, word, weight information.
# You will have to ask MALLET to output this file using the "--topic-word-weights-file FILENAME" option.
# Produces as output a plain text file containing, for each topic, the top-100 words with their relative score.
# Paste this output, for the topic you are interested in, into the "advanced" wordle page: http://www.wordle.net/advanced
# This script will work best with Python3. You need to have numpy and pandas installed.
# The sample file included in the toolbox repo comes from a collection of 376 French plays from theatre-classique.fr.


#########################
# Import statements
#########################

import numpy as np
import itertools
import operator
import os
import pandas as pd
from collections import Counter

def mallet2wordle(infile,outfile):
    """Transform MALLET output for visualization with wordle.net."""
    ### Load the data from MALLET.
    word_scores = pd.read_table(infile, header=None, sep="\t")
    word_scores = word_scores.sort(columns=[0,2], axis=0, ascending=[True, False])
    word_scores_grouped = word_scores.groupby(0)
    number_of_topics = len(word_scores.groupby(0).size())

    ### For each topic, find the top-100 words with their scores.
    top_topic_words_with_scores = ""
    for i in range(0,number_of_topics-1):
        topic_word_scores = word_scores_grouped.get_group(i)
        top_topic_word_scores = topic_word_scores.iloc[0:100]
        topic_words = top_topic_word_scores.loc[:,1].tolist()
        word_scores = top_topic_word_scores.loc[:,2].tolist()

        top_topic_words_with_scores = top_topic_words_with_scores + "tp" + str(i) + "\n"
        j = 0
        for word in topic_words:
            score = word_scores[j]
            j += 1
            line = word + ":" + str(int(score)) + "\n"
            top_topic_words_with_scores = top_topic_words_with_scores + line
        top_topic_words_with_scores = top_topic_words_with_scores + "\n"
    with open(outfile, "w") as outfile:
        outfile.write(top_topic_words_with_scores)

def main(infile, outfile):
    mallet2wordle(infile,outfile)

main("topic-word-weights.txt","scores-for-wordle.txt")
