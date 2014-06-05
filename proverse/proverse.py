# proverse.py
# Script to recognize dramatic text as being in verse or prose.


###############################
# Overview of functions
###############################

# 1. Load files from a folder.
# 2. For each file containing one play, make a list of the length in characters of each line.
# 3. For each such list, calculate the mean and the standard deviation. 
# 4. Based on these scores, decide whether a play is in prose or in verse (or mixed). 
# 5. Write a file with the filename, the scores and the decision for each play.


###############################     
# User settings
###############################

# 1. Mandatory: Modify the path to the working directory or put your TreeTagger files in the default "trt" directory.
# 2. Optional: Adjust the thresholds as needed with regard to material under scrutiny.


###############################
# Import statements
###############################

import glob
import csv
import os
import itertools
import numpy as np


###############################
# Text processing
###############################

def proverse(file):
    """ Recognize whether a text is in prose or in verse """
    with open(file, "r") as txt: 
        text = txt.read()                                               # Creates a string object with the text
        lines = text.split("\n")
        lengths = []
        for line in lines:
            length = len(line)
            lengths.append(length)
        number = len(lengths)
        mean = np.mean(lengths)
        sd = np.std(lengths)
        basename = os.path.basename(file)                               # Retrieves just the basename from the filename.
        print("Result for " + basename + ": mean = " + str(mean) + "; sd = " + str(sd) + "; number of lines = " + str(number))
        
        








"""
        newfilename = basename[:-8] + ".csv"                            # Builds filename for outputfile from basename.
    with open(os.path.join("./csv", newfilename),"w") as output:        # Builds path for clean files from output directory and filename.
        output.write(text)                                              # Writes the new cleaned files. 


def trt2txt(file):
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
        
"""

###############################
# Main
###############################

def main(inputpath):
    for file in glob.glob(inputpath):
        proverse(file)

main('./input/*.txt')                                                   # Enter absolute or relative path to folder with XML files and define filename filter.
