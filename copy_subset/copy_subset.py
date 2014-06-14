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
    by_date = metadata[metadata.date > 1720]                            # Sample data: ca. 1700-1800.
    by_date_genre = by_date[by_date.genre == "comedy"]                  # Sample data: comedy, tragedy, other.
    by_date_genre_form = by_date_genre[by_date_genre.form == "prose"]   # Sample data: prose, verse, mixed.
    print(by_date_genre_form)
    subset = []
    for item in by_date_genre_form.index:
        item = item + ".txt"
        subset.append(item)
    print(subset)
    for file in glob.glob(fullset):
        if os.path.basename(file) in subset:
            shutil.copy(file, "./subset")


#######################
# Main
#######################

def main(fullset,metadata):
    copy_subset(fullset,metadata)

main("./fullset/*.txt","metadata.csv")
