#!/usr/bin/env python3
# Filename: tei2txt.py

"""
# Function to transform plain text files into simple, clean TEI files.
# Makes use of "re"; see: http://docs.python.org/2/library/re.html
"""


#########################
# Basic structure
#########################

# - Open and read an TXT text file.
# - Add TEI header to top of the file
# - Turn each paragraph into a TEI p
# - Do some cleanup
# - Write new XML file to disk.



#######################
# Import statements   #
#######################

import re
import glob


#######################
# Functions           #
#######################


def read_file(file,xmlmutandum):
    """ Opens the file. Needs to come first."""
    print(file)
    with open(file,"r") as mutandum:
        mutandum = mutandum.read()
    with open(xmlmutandum,"w") as output:
        output.write(mutandum)

def add_paragraphs(xmlmutandum):
    """ Turns all plain text paragraphs in a TEI p. """
    with open(xmlmutandum,"r") as mutandum:
        mutandum = mutandum.read()
        mutandum = re.sub("\n","</p>\n<p>",mutandum)  # could be "\n\n" as well.
    with open(xmlmutandum,"w") as output:
        output.write(mutandum)

def add_teiheader(xmlmutandum,teiheader):
    """ Replaces the existing HTML header with a teiHeader and final TEI tags and saves as XML."""
    with open(teiheader,"r") as teiheader:
        teiheader = teiheader.read()
    with open(xmlmutandum,"r") as mutandum:
        mutandum = mutandum.read()
        mutandum = re.sub("\A",teiheader,mutandum)
        mutandum = re.sub("\Z","</div></body><back><div></div></back></text></TEI>",mutandum)
    with open(xmlmutandum,"w") as output:
        output.write(mutandum)

def convert_headings(xmlmutandum):
    """Removes all attributes from h1 and turns it into head."""
    with open(xmlmutandum,"r") as mutandum:
        mutandum = mutandum.read()
        mutandum = re.sub(r"<p>(CHAPITRE [\w]*)</p>","</div><div><head>\\1</head>",mutandum)
        mutandum = re.sub(r"<p>([0-9]+)</p>","</div><div><head>\\1</head>",mutandum)
    with open(xmlmutandum,"w") as output:
        output.write(mutandum)

def cleanup_xml(xmlmutandum):
    """Several smaller deletions of possibly meaningless markup. Deactivate lines selectively as needed."""
    with open(xmlmutandum,"r") as mutandum:
        mutandum = mutandum.read()
        mutandum = re.sub("<p>\n</div></body>","\n</div></body>",mutandum)
        mutandum = re.sub("</p><p></p><p>","</p><p>",mutandum)
        mutandum = re.sub("<p></p>\n<p></p>","",mutandum)
        mutandum = re.sub("<p></p>\n","",mutandum)
        mutandum = re.sub("\n\n","\n",mutandum)
        mutandum = re.sub("\n\n","\n",mutandum)
    with open(xmlmutandum,"w") as output:
        output.write(mutandum)

def write_xmloutput(file,xmlmutandum):
    """Convenience function which saves transformed file to new filename. Needs to come last."""
    with open(xmlmutandum,"r") as mutandum:
        mutandum = mutandum.read()
    xmloutput = "./tei/" + file[6:-4] + ".xml"                       # Builds filename for outputfile from original filenames but correct extension.
    with open(xmloutput,"w") as output:
        output.write(mutandum)


#######################
# Main                #
#######################


def main(inputpath,xmlmutandum,teiheader):
    for file in glob.glob(inputpath):
        read_file(file,xmlmutandum)
        add_paragraphs(xmlmutandum)
        add_teiheader(xmlmutandum,teiheader)
        convert_headings(xmlmutandum)
        cleanup_xml(xmlmutandum)
        write_xmloutput(file,xmlmutandum)


main('./txt/*.txt',"MUTANDUM.xml","teiHeader.xml")

