# clean_txt.py
# Function to remove some unwanted elided words from French text for use in topic modeling, such as "j'" in "j'ai".
# Makes use of "re"; see: http://docs.python.org/2/library/re.html


#######################
# Import statements   
#######################

import re
import glob


#######################
# Functions           
#######################

def clean_txt(file):
    """Deletion of unwanted elided words."""
    with open(file,"r") as text:
        text = text.read()
        text = re.sub("([\s|[\w|\W]')"," ",text)            # Regular expression to remove some words.
        newfile = file[:-4] + "n.txt"                       # Builds filename for outputfile from original filenames.
    with open(newfile,"w") as output:
        output.write(text)
        

#######################
# Main                #
#######################


def main(inputpath):
    for file in glob.glob(inputpath):
        clean_txt(file)
            
main('./chunks/*.txt')

