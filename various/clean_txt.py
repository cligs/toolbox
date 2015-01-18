# clean_txt.py
# Function to remove some unwanted elided words from French text for use in topic modeling, such as "j'" in "j'ai".
# Makes use of "re"; see: http://docs.python.org/2/library/re.html


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
    """Deletion of unwanted elided words."""
    with open(file,"r") as text:
        text = text.read()                                               # Creates a string object with the text
        text = re.sub("([\s|[\w|\W]')"," ",text)                         # Removes some words based on regular expression.
        basename = os.path.basename(file)                                # Retrieves just the basename from the filename.
        cleanfilename = basename[:-4] + ".txt"                           # Builds filename for outputfile from basename.
    with open(os.path.join(output_dir, cleanfilename),"w") as output:    # Builds path for clean files from output directory and filename.
        output.write(text)                                               # Writes the new cleaned files. 


#######################
# Main                #
#######################


def main(inputpath,output_dir):
    for file in glob.glob(inputpath):
        clean_txt(file,output_dir)
            
main('./tctxt2/*.txt','./tctxt3/')

