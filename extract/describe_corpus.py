#!/usr/bin/env python3
# Filename: describe_corpus.py
# Author: #cf

"""
# Visualize some corpus properties.
"""


##################
### Parameters ###
##################

#wdir = "/home/christof/Dropbox/0-Analysen/2015/hybrid/rf692/"
wdir = "/home/christof/Repos/cligs/romanfrancais/"
metadatafile = "metadata.csv"
categories = ["author"] # author|subgenre|gender|decade|genre|narration|supergenre
outfolder = "visuals/"
stacked = True
dpi = 300
mode = "overall" # bydecades|overall
display = "print" # print|save|mute


##################
### Functions  ###
##################

import pandas as pd
import matplotlib.pyplot as plt
import os

def describe_corpus(wdir, metadatafile, category, outfolder, stacked, dpi, display):
    """Visualize corpus properties."""
    print("Launched describe_corpus for "+category)
    metadata, no_of_entries = read_metadata(metadatafile)
    if mode == "bydecades":
        selected = select_bydecade(metadata, category)
        visualize_bydecades(category, selected, outfolder, stacked, dpi, no_of_entries)
        display_data(category, selected, outfolder, no_of_entries, display, mode)
    elif mode == "overall":
        selected = select_overall(metadata, category)
        visualize_overall(category, selected, outfolder, stacked, dpi, no_of_entries)
        display_data(category, selected, outfolder, no_of_entries, display, mode) 
    else:
        print("Error. Please indicate a valid value for \"mode\".")

def read_metadata(metadatafile):
    """Read metadata from CSV file."""
    print("  Reading metadata...")
    with open(wdir+metadatafile, "r") as infile:
        metadata = pd.DataFrame.from_csv(infile, header=0)
        #print(metadata.head())
        no_of_entries = metadata.shape[0]
        return metadata, no_of_entries

def select_bydecade(metadata, category, ):
    """Select data to be visualized."""
    print("  Selecting metadata...")
    cat_xaxis = "decade"
    cat_bars = category 
    labels = set(metadata[cat_bars])
    #print("Labels:", labels)
    metadata = metadata[["idno",cat_xaxis,cat_bars]]
    selected = metadata.groupby([cat_xaxis,cat_bars]).count()
    return selected

def visualize_bydecades(category, selected, outfolder, stacked, dpi, no_of_entries):
    """Visualize selected data."""
    print("  Visualizing data...")
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    myplot = selected.unstack().plot(kind="bar", stacked=True, title="",figsize=(10, 8))
    myplot.set_title("Distribution of novels", fontsize=20)        
    myplot.set_xlabel("Category", fontsize = 16)
    myplot.set_ylabel("Number",fontsize = 16)
    if category == "subgenre": 
        myplot.legend(["blanche","policier"]) ## subgenre
    elif category == "gender":
        myplot.legend(["female","male", "other/mixed"]) ## gender
    plt.setp(plt.xticks()[1], rotation=40, fontsize = 14)   
    plt.tight_layout()
    figurename = outfolder+"distvis-bydecades_"+category+"_"+str(no_of_entries)+".png"
    plt.savefig(wdir+figurename, dpi=dpi)

def select_overall(metadata, category): 
    print("  Selecting metadata...")
    selected = metadata[category].value_counts()
    return selected

def visualize_overall(category, selected, outfolder, stacked, dpi, no_of_entries):
    print("  Visualizing data...")
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    stacked = False # overriding options
    myplot = selected.plot(kind="bar")
    myplot.set_title("Novels per "+category, fontsize=15)        
    myplot.set_xlabel(category+"s", fontsize = 12)
    myplot.set_ylabel("Number of novels",fontsize = 12)
    plt.setp(plt.xticks()[1], rotation=90, fontsize = 9)   
    plt.tight_layout()
    figurename = outfolder+"distvis-overall_"+category+"_"+str(no_of_entries)+".png"
    plt.savefig(wdir+figurename, dpi=dpi)

def display_data(category, selected, outfolder, no_of_entries, display, mode): 
    if display == "print":
        print("\n====================\n")
        print(selected)
        print("======================\n")
    elif display == "save":
        dataname = outfolder+"distdata_"+mode+"_"+category+"_"+str(no_of_entries)+".csv"
        with open(dataname, "w") as outfile: 
            selected.to_csv(dataname)

def main(wdir, metadatafile, categories, outfolder, stacked, dpi, display):
    for category in categories:
        describe_corpus(wdir, metadatafile, category, outfolder, stacked, dpi, display)
    print("Done.")

main(wdir, metadatafile, categories, outfolder, stacked, dpi, display)
