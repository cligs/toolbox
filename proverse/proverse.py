# proverse.py
# Script to recognize dramatic text as being in verse or prose.
# Version 0.2, 5.6.2014, by #cf. 


###############################
# Overview of functions
###############################

# 1. Load files from a folder.
# 2. For each file containing one play, make a list of the length in characters of each line.
# 3. For each such list, calculate the mean and the standard deviation. 
# 4. Based on these scores, decide whether a play is in prose or in verse (or mixed). 
# 5. (tbd.: Write a file with the filename, the scores and the decision for each play.)


###############################     
# User settings
###############################

# 1. Mandatory: Modify the path to the working directory or put your TreeTagger files in the default "trt" directory.
# 2. Optional: Adjust the threshold (line 54) as needed with regard to material under scrutiny.


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
        form = ()
        if sd < 20:
            form = "verse"
        else: 
            form = "prose"
        print("Guess for " + basename + ": " + form + ". Data: mean=" + str(mean) + "; sd=" + str(sd) + "; lines=" + str(number) + ".")
        
        

###############################
# Main
###############################

def main(inputpath):
    for file in glob.glob(inputpath):
        proverse(file)

main('./input/*.txt')                                                   # Enter absolute or relative path to folder with XML files and define filename filter.
