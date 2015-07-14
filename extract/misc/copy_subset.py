# copy_subset.py
# Script to select a subset of text files from a larger text collection.
# v0.3, 2014-06-14, by #cf.


#######################
# Overview
#######################

# 1. Reads metadata from CSV file.
# 2. Defines subset of files via filters based on metadata.
# 3. Copies subset of files to new folder

#######################
# Import statements
#######################

import glob
import pandas as pd
import os
import shutil


#######################
# Functions
#######################

def copy_subset(fullset,metadata):
    """ Reads metadata from file, builds subset of filenames, copys those files to new folder"""
    metadata = pd.read_csv(metadata, delimiter=',', index_col=0)
    #print(metadata)
    filtered = metadata[metadata.date >= 1630]
    filtered = metadata[metadata.date <= 1789]
    filtered = metadata[metadata.acts >= 3]
    filtered = filtered[filtered.genre == "Tragi-comédie"]
    #filtered = filtered[filtered.form == "prose"]
    #filtered = filtered[filtered.author == "AllainvalA"]
    #print(filtered)
    subset = []
    for item in filtered.index:
        item = item + ".xml"
        subset.append(item)
    print(subset)
    print("Number of files selected: ", len(subset))
    for file in glob.glob(fullset):
        if os.path.basename(file) in subset:
            shutil.copy(file, "./subset")


#######################
# Main
#######################

def main(fullset,metadata):
    copy_subset(fullset,metadata)

main("./tei4/*.xml","tc727.csv")
