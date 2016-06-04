# pretoken.py
# Function to prepare text files for lemmatization and POS-tagging with TreeTagger.
# Basically splits hyphenated words apart and removes elided words to make sure TreeTagger doesn't get confused over them.
# Makes use of "re"; see: http://docs.python.org/2/library/re.html


#######################
# Good to know   
#######################

# 1. By default, expects files to be in a subfolder called "in". 
# 2. By default, expects there to be an empty folder called "out" for the output.


#######################
# Import statements   
#######################

import re
import os
import glob


#######################
# Functions           
#######################

def clean_txt(file,output_dir):
    """Deletion of unwanted elided and hyphenated words."""
    with open(file,"r") as text:
        text = text.read()                                               # Creates a string object from the text
        text = re.sub("J'","Je ",text)                                   # Removes some words based on regular expression.
        text = re.sub("j'","je ",text)                                   # Removes some words based on regular expression.
        text = re.sub("S'","Se ",text)                                   # Removes some words based on regular expression.
        text = re.sub("s'","se ",text)                                   # Removes some words based on regular expression.
        text = re.sub("C'","Ce ",text)                                   # Removes some words based on regular expression.
        text = re.sub("c'","ce ",text)                                   # Removes some words based on regular expression.
        text = re.sub("N'","Ne ",text)                                   # Removes some words based on regular expression.
        text = re.sub("n'","ne ",text)                                   # Removes some words based on regular expression.
        text = re.sub("D'","De ",text)                                   # Removes some words based on regular expression.
        text = re.sub("d'","de ",text)                                   # Removes some words based on regular expression.
        text = re.sub("L'","L ",text)                                # Removes some words based on regular expression.
        text = re.sub("l'","l ",text)                                # Removes some words based on regular expression.
        text = re.sub("T'","T ",text)                                   # Removes some words based on regular expression.
        text = re.sub("t'","t ",text)                                   # Removes some words based on regular expression.
        text = re.sub("-le"," le",text)                                  # Removes some words based on regular expression.
        text = re.sub("-moi"," moi",text)                                  # Removes some words based on regular expression.
        text = re.sub("-je"," je",text)                                  # Removes some words based on regular expression.
        text = re.sub("-il"," il",text)                                  # Removes some words based on regular expression.
        text = re.sub("-elle"," elle",text)                              # Removes some words based on regular expression.
        text = re.sub("-nous"," nous",text)                              # Removes some words based on regular expression.
        text = re.sub("-vous"," vous",text)                              # Removes some words based on regular expression.on.
        text = re.sub("-nous"," nous",text)                              # Removes some words based on regular expressi
        text = re.sub("-ce"," ce",text)                                  # Removes some words based on regular expression.
        text = re.sub("-tu"," tu",text)                                      # Removes some words based on regular expression.
        text = re.sub("-toi"," toi",text)                                      # Removes some words based on regular expression.
        text = re.sub("jusqu'à'","jusque à",text)                                      # Removes some words based on regular expression.
        text = re.sub("aujourd'hui","aujourdhui",text)                                      # Removes some words based on regular expression.
        text = re.sub("-t","",text)                                      # Removes some words based on regular expression.
        text = re.sub("-y"," y",text)                                      # Removes some words based on regular expression.
        text = re.sub("-en"," en",text)                                      # Removes some words based on regular expression.
        text = re.sub("-ci"," ci",text)                                      # Removes some words based on regular expression.
        text = re.sub("-là"," là",text)                                      # Removes some words based on regular expression.
        #text = re.sub("là-bas","là bas",text)                                      # Removes some words based on regular expression.
        text = re.sub("Qu'il","Qu il",text)                                      # Removes some words based on regular expression.
        text = re.sub("qu'il","qu il",text)                                      # Removes some words based on regular expression.
        text = re.sub("-même"," même",text)                                      # Removes some words based on regular expression.
        basename = os.path.basename(file)                                # Retrieves just the basename from the filename.
        cleanfilename = basename[:-4] + ".txt"                           # Builds filename for outputfile from basename.
        print(cleanfilename)
    with open(os.path.join(output_dir, cleanfilename),"w") as output:    # Builds path for clean files from output directory and filename.
        output.write(text)                                               # Writes the new cleaned files. 


#######################
# Main                #
#######################


def main(inputpath,output_dir):
    for file in glob.glob(inputpath):
        clean_txt(file,output_dir)
            
main('./in/*.txt','./out/')

