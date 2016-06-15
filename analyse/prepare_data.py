#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to prepare data for labeled LDA with MALLET. 
"""


MetadataFile = "metadata.csv"
SegPath = "lemmata-whole/*.txt"
OutputFile = "labeled-lemmata-subgenre-whole.txt"

import pandas as pd
import glob
import os

def prepare_labeled_data(SegPath,    
                       MetadataFile,
                       OutputFile):



    with open(MetadataFile, "r") as infile: 
        Metadata = pd.DataFrame.from_csv(infile, sep=";")
        print(Metadata.head())

        open(OutputFile, "w").close() # This makes sure file is empty at the beginning.
        with open(OutputFile, "a") as outfile: 
            for file in glob.glob(SegPath): 
                with open(file, "r") as infile: 
                    text = infile.read()
                idno = os.path.basename(file)[0:6]
                identifier = os.path.basename(file)[:-4]
                #print(idno)
                
                author = Metadata.loc[idno,"author-name"]
                subgenre = Metadata.loc[idno,"subgenre"]
                decade = Metadata.loc[idno,"decade"]
                #Label = author +" "+ subgenre +" "+ decade
                Label = subgenre+"1 "+subgenre+"2 "+subgenre+"3"
                print(Label)
                
                Doc = identifier +"\t" + Label + "\t" + text + "\n"
                #print(Doc)
            
                outfile.write(Doc)
            
            
            
            
            
                    




prepare_labeled_data(SegPath,    
                       MetadataFile,
                       OutputFile)