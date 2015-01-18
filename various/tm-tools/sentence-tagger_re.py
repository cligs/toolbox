# sentence-tagger.py
# Function to tag each sentence in the body of a TEI file as a sentence using TEI markup.


########################
# Overview
########################

# Open each XML file in a folder and apply the following
# 1. Read the file as an element tree
# 2. Select each "p", and in each "p", identify sentence boundaries
# 3. Markup every sentence boundary using the "s" element.
# 4. Save file to a new folder with a new name. 


########################
# Import statements   
########################

import re
import regex
import glob


########################
# Functions           
########################

def tag_sentences(file): 
    """Open TEI file, identify and markup sentence boundaries, write new file to new folder."""
    with open(file,"r") as mutandum:                                    # Opens the file
        mutandum = mutandum.read()                                      # Reads the file and keep the content in the string container "mutandum"
        mutandum = re.sub("<p>","<p><s ana=\"\">",mutandum)                      # Adds sentence start-tag at beginning of paragraphs.
        mutandum = re.sub("</p>"," </s></p>",mutandum)                  # Adds sentence end-tag at end of paragraphs.
        mutandum = regex.sub("(?<=\p{Ll})(\.)(\s)(?=\p{Lu})",". </s><s ana=\"\">",mutandum)          # Regular expression identifies sentence boundaries within paragraphs.
        mutandum = regex.sub("(?<=\p{Ll})(\s)?(;)(\s)(?=\p{Lu})"," ; </s><s ana=\"\">",mutandum)     # Dito.
        mutandum = regex.sub("(?<=\p{Ll})(\s)?(:)(\s)(?=\p{Lu})"," : </s><s ana=\"\">",mutandum)     # Dito.
        mutandum = regex.sub("(?<=\p{Ll})(\s)?(\!)(\s)(?=\p{Lu})"," ! </s><s ana=\"\">",mutandum)    # Dito.
        mutandum = regex.sub("(?<=\p{Ll})(\s)?(\?)(\s)(?=\p{Lu})"," ? </s><s ana=\"\">",mutandum)    # Dito.
        mutandum = regex.sub("(?<=\.\.\.)(\s)(?=\p{Lu})"," </s><s ana="">",mutandum)               # Dito.

    outputfilename = "tei-rn-st/"+ file[9:-4] + "_st" + ".xml"         # Builds filename for outputfile from original filenames with label "_sent".
    with open(outputfilename,"w", encoding="utf8") as output:
        output.write(mutandum)
       

#######################
# Main                #
#######################


def main(inputpath):
    for file in glob.glob(inputpath):
        tag_sentences(file)
            
main('./tei-rn/*.xml')                                          # USER: Set path to inputfiles.

