# trt2txt.py
# Script to extract lemmas from TreeTagger output and write them to a new file containing lemma-based pseudo-text.


###############################
# Overview of functions
###############################

# 1. Load TreeTagger output CSV files from a folder one after the other.
# 2. For each file, and each line, just extract the lemma.
# 4. For each file, create a TXT file containing all the lemmas.


###############################     
# User settings
###############################

# 1. Mandatory: Modify the path to the working directory or put your TreeTagger files in the default "trt" directory.
# 2. Optional: Select which cleanup procedures should be used and/or adapt them to your needs.


###############################
# Import statements
###############################

import re
import glob
import csv
import os
import itertools


###############################
# Text processing
###############################

def txt2csv(file):
    """ Rename TreeTagger files from TXT to CSV """
    with open(file, "r") as txt: 
        text = txt.read()                                               # Creates a string object with the text
        basename = os.path.basename(file)                               # Retrieves just the basename from the filename.
        newfilename = basename[:-8] + ".csv"                            # Builds filename for outputfile from basename.
    with open(os.path.join("./csv", newfilename),"w") as output:        # Builds path for clean files from output directory and filename.
        output.write(text)                                              # Writes the new cleaned files. 


def trt2txt(file):
    """ Load CSV files from folder, extract selected data, save to new TXT files"""
    with open(file, newline="\n") as trtfile:
        trtcontent = csv.reader(trtfile, delimiter="\t")
        lemmas = []
        for row in trtcontent:
            lemma = row[2:3]
            if "." not in lemma and "," not in lemma and ";" not in lemma and "!" not in lemma and "?" not in lemma and "<unknown>" not in lemma and "..." not in lemma:
                lemmas.append(lemma)
        lemmas = list(itertools.chain.from_iterable(lemmas))
    txtoutput = "./txt/" + file[6:-4] + ".txt"                          # Builds filename path from inputfile with new extension.
    with open(txtoutput,"w") as output:                                 # Writes selected text to TXT file in folder specified above.
        output.write(" ".join(lemmas))
        

###############################
# Main
###############################

def main(inputpath):
    for file in glob.glob(inputpath):
        txt2csv(file)
    for file in glob.glob("./csv/*.csv"):
        trt2txt(file)

main('./trt/*.trt')                                                   # Enter absolute or relative path to folder with XML files and define filename filter.
