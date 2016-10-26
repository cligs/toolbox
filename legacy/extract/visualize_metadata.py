#!/usr/bin/env python3
# Filename: describe_corpus.py
# Author: #cf

"""
# Visualize some corpus properties.
"""

import pandas as pd
import matplotlib.pyplot as plt

def describe_corpus(wdir, metadatafile, category):
    with open(wdir+metadatafile, "r") as infile:
        metadata = pd.DataFrame.from_csv(infile, header=0)
        #print(metadata.head())
        
        ## Preparing data
        cat_xaxis = "decade"
        cat_bars = category 
        labels = set(metadata[cat_bars])
        print(labels)
        metadata = metadata[["idno",cat_xaxis,cat_bars]]
        grouped = metadata.groupby([cat_xaxis,cat_bars]).count()
        unstacked = grouped.unstack()
        unstacked.fillna("0", inplace=True)

        ## Plotting the data         
        myplot = grouped.unstack().plot(kind="bar", stacked=True, title="",figsize=(10, 8))
        myplot.set_title("Distribution of novels", fontsize=20)        
        myplot.set_xlabel("Decades", fontsize = 16)
        myplot.set_ylabel("Number",fontsize = 16)
        myplot.legend(labels) ## This is correct only by chance!!
        plt.setp(plt.xticks()[1], rotation=40, fontsize = 14)   
        plt.tight_layout()
        figurename = "dist_by-"+category+".png"
        plt.savefig(wdir+figurename, dpi=300)

def main(wdir, metadatafile, category):
    describe_corpus(wdir, metadatafile, category)


main("/home/ulrike/Git/novelashispanoamericanas/", "metadata.csv", "author-country")
## For category, choose: genre, subgenre, gender, narration, supergenre
