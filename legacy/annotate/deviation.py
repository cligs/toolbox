#!/usr/bin/env python3
# Filename: deviation.py

"""
# Function for quantitative deviation analysis.
"""


#########################
# Basic structure
#########################

# - Open and read one TXT text file after another.
# - Calculate the relative frequency of some feature in each text.
# - Create a historgram and compare with normal distribution.


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
from matplotlib import pyplot as plt


#######################
# Functions           #
#######################


def deviation(inpath, feature):
    """ Function for quantitative deviation analysis."""
    texts = []
    counts = []
    for file in glob.glob(inpath):
        with open(file, "r") as infile:
            textname = os.path.basename(file)[-9:-4]
            texts.append(textname)
            plaintext = infile.read()
            plaintext = plaintext.lower()
            tokens = re.findall("\w+",plaintext)
            textlength = len(tokens)
            features = re.findall(feature,plaintext)
            count = len(features)
            rel_count = count/textlength*10000
            counts.append(rel_count)
    print(texts)
    print(counts)
    
    plt.hist(counts)
    plt.show()


def main(inpath, feature):
    deviation(inpath, feature)

main("./data/*.txt", "lui")
