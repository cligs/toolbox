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
# 5. Write a CSV file with comma-separated values for: filename, predicted form, standard deviation, mean, and number of lines for each play.


###############################     
# User settings
###############################

# 1. Mandatory: Put all files to be analysed in the subfolder "input" (or change location in main).
# 2. Optional: Adjust the thresholds and labels (line 56ff) as needed with regard to material under scrutiny.


###############################
# Import statements
###############################

import glob
import os
import numpy as np


###############################
# Text processing
###############################

def proverse(file):
    """ Recognize whether a text is in prose or in verse and write predictions to a CSV file. """                                                                 
    with open(file, "r") as txt:                                    # Opens the file.
        basename = os.path.basename(file)                           # Retrieves just the basename from the filename.
        text = txt.read()                                           # Creates a string object from text in file.
        lines = text.split("\n")                                    # Splits text into lines with "newline" as separator.
        lengths = []                                                # Creates empty list called "lengths" for each length value of each line.
        for line in lines:                                          # Iterates over each line in the text
            length = len(line)                                      # Calculates the length of the line in characters.
            lengths.append(length)                                  # Appends the length of the line to the list of lengths. 
        number = len(lengths)                                       # Calculates the number of lines in the text.
        mean = np.mean(lengths)                                     # Calulates the mean of the line lengths in the text.
        sd = np.std(lengths)                                        # Calculates the standard deviation for the line lengths in the text
        predictedform = ()                                          # Creates an empty string for each prediction.
        if mean < 50 and sd < 10:                                   # Condition #1.
            predictedform = "verse"                                 # Prediction #1.
        elif mean < 62 and sd > 10:                                 # Condition #2.
            predictedform = "mixed?"                                # Prediction #2.
        elif mean > 62 and sd > 10:                                 # Condition #3.
            predictedform = "prose"                                 # Prediction #3.
        else:                                                       # All other cases, if any.
            predictedform = "prose"                                 # Prediction #4.
        output = basename + "," + predictedform + "," + str(sd) + "," + str(mean) + "," + str(number) + "\n" # Builds a line of comma-separated values for each text.
        #print(output)                                              # USER: Uncomment for output in terminal.
    with open("results.csv", "a") as resultfile:                    # Creates a new file in "appending" mode.
        resultfile.write(output)                                    # Adds output from current text to the results file. 
        

###############################
# Main
###############################

def main(inputpath):
    for file in glob.glob(inputpath):                               # Applies the function below to each file.                                  
        proverse(file)                                              # Calls the "proverse" function.    

main('./input/*.txt')                                               # USER: Modify path to folder with files if necessary.
