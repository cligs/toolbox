# proverse.py
# Script to recognize dramatic text as being in verse or prose.
# Version 0.5, 6.6.2014, by #cf. New: delete speaker names.  


###############################
# Overview of functions
###############################

# 1. Load files from a folder.
# 2. For each file containing one play, make a list of the length in characters of each line.
# 3. For each such list, calculate the mean and the standard deviation, as well as the mean and sd of the differences between subsequent lines. 
# 4. Based on these scores, decide whether a play is in prose, in verse or mixed. 
# 5. Write a CSV file with comma-separated values for: filename, predicted form, various indicators for each play.
# Note: the best indicator, and the only one used in this version, is the standard deviation of the differences between subsequent lines.


###############################     
# User settings
###############################

# 1. Mandatory: Put all files to be analysed in the subfolder "input" (or change location in main).
# 2. Optional: Adjust the thresholds and labels (line 52ff) as needed with regard to material under scrutiny.


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
        alllines = text.split("\n")                                 # Splits text into lines with "newline" as separator.
        # Preprocessing: Separate speaker names from speeches.
        lines = []                                                  # Create a list object for the speeches.
        speakers = []                                               # Create a list object for the speaker names.
        for line in alllines:                                       # Iterates over each line in the text.
            if line[0:3].isupper():                                 # Checks whether the first three characters in a line are uppercase. 
                speakers.append(line)                               # If yes, adds the line to the list of speakers. 
            else:                                                   # If no,
                lines.append(line)                                  # Add the line to the list of lines.
        #print(lines[0:10])                                         # USER: Activate for inspection.
        #print(speakers[0:10])                                      # USER: Activate for inspection.
        # Calculations on numbers of characters per line 
        lengths = []                                                # Creates empty list called "lengths" for each length value of each line.
        for line in lines:                                          # Iterates over each line in the text
            length = len(line)                                      # Calculates the length of the line in characters.
            lengths.append(length)                                  # Appends the length of the line to the list of lengths. 
        #print(lengths[0:10])                                       # USER: Activate for inspection.
        number = len(lengths)                                       # Calculates the number of lines in the text.
        mean = np.mean(lengths)                                     # Calulates the mean of the line lengths in the text.
        sd = np.std(lengths)                                        # Calculates the standard deviation for the line lengths in the text
        # Calculations on length changes between lines in sequence
        diffs = []                                                  # Creates empty list for the differences in length of subsequent lines.
        for i in range(0,len(lengths)-1):                           # Iterates over the list of line lengths as many times as there are lines, minus one.
            diff = abs(lengths[i] - lengths[i+1])                   # Calculates the absolute difference between each line and the next.
            diffs.append(diff)                                      # Adds each such absolute difference to a list of differences.
        #print(diffs[0:10])                                         # USER: Activate for inspection.
        mean_df = np.mean(diffs)                                    # Calculates the mean of the differences.
        sd_df = np.std(diffs)                                       # Calculates the standard deviation of the differences.
        # Calculation of predictions based on data
        predictedform = ()                                          # Creates an empty string for each prediction.
        if sd_df < 18:                                              # Condition #1.
            predictedform = "verse"                                 # Prediction #1.
        elif sd_df > 18 and sd_df < 40:                             # Condition #2
            predictedform = "mixed"                                 # Prediction #2
        else:                                                       # Condition #2.
            predictedform = "prose"                                 # Prediction #2.
        output = basename + "," + predictedform + "," + str(sd) + "," + str(mean) + "," + str(number) + "," + str(mean_df) + "," + str(sd_df) + "\n" # Builds a line of comma-separated values for each text.
        #print(output)                                              # USER: Activate for inspection.
    with open("results.csv", "a") as resultfile:                 # Creates a new file in "appending" mode.
        resultfile.write(output)                                    # Adds output from current text to the results file. 
        

###############################
# Main
###############################

def main(inputpath):
    for file in glob.glob(inputpath):                               # Applies the function below to each file.                                  
        proverse(file)                                              # Calls the "proverse" function.    

main('./input/*.txt')                                               # USER: Modify path to folder with files if necessary.
