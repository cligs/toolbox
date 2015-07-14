# ./bin/env python3
# copy_subset.py
# author: #cf.
# v0.4, 2015-07-14. 

"""
# Select a subset of text files from a larger text collection.
"""

import glob
import pandas as pd
import os
import shutil

def copy_subset(wdir, fullset, metadata, outfolder):
    """ Select a subset of text files from a larger text collection."""
    
    ## Read metadata from file
    metadata = pd.read_csv(wdir+metadata, delimiter=',', index_col=0)
    #print(metadata.head())

    ## Filter the metadata table by one or several criteria
    ## USER: For categorical criteria, set filter category (column) and list of values to be selected.
    filter_category = "decade" # author_short, genre, subgenre, availability, decade, etc.
    selection_list = ["1880s", "1890s"] # See metadata file for possible values
    #metadata = metadata[metadata[filter_category].isin(selection_list)]

    ## USER: And/or, for numeric criteria, set a filter category and upper and lower bound.
    filter_category = "pub_year"
    lower_bound = "1879"
    upper_bound = "1899"
    myquery = lower_bound + "<" + filter_category + "<" + upper_bound 
    #metadata = metadata.query(myquery)
    
    ## Create a list of filenames corresponding to the filter criteria.
    subset = []
    for item in metadata.index:
        subset.append(item)
    #print(subset)
    print("Files selected:", len(subset))
    
    ## Copy the right files to a new folder.    
    if not os.path.exists(wdir+outfolder):
        os.makedirs(wdir+outfolder)
    source = wdir+fullset
    destination = wdir+outfolder
    counter = 0
    for file in glob.glob(source):
        basename = os.path.basename(file)
        idno = basename[0:6]
        #print(file)
        #print(idno, basename)
        #print(wdir+outfolder+basename)
        if idno in subset:
            counter +=1
            shutil.copy(file, destination)
    print("Files copied  :", counter)

def main(wdir, fullset, metadata, outfolder):
    copy_subset(wdir, fullset, metadata, outfolder)

main("/home/christof/Repos/cligs/romanfrancais/", "master/*.xml", "header-metadata.csv", "subset/")
