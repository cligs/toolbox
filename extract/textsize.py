# ./bin/env python3
# textlength.py
# author: #cf

"""
# Extract text length data from TXT files (and write to TEI files).
"""

################
## PARAMETERS ##
################

wdir = "../" 
inpath = "txt/*0734.txt"


#######################
## IMPORT STATEMENTS ## 
#######################

from lxml import etree
import glob
import os
import pandas as pd
import re

###############
## FUNCTIONS ##
###############

def get_textlength(wdir, inpath):
    """Get length information from texts."""
    print("idno, identifier, lines, words, chars, bytes")
    for infile in glob.glob(wdir+inpath):
        with open(infile, "r") as txtfile: 
            text = txtfile.read()
        author_title = infile[7:-11]
        idno = infile[-10:-4]
        lines = re.split("\n", text)
        size_lines = len(lines)
        words = re.split("[\W]+", text)
        #print(words[0:100])
        size_words = len(words)
        size_chars = len(text)
        size_kb = int(os.path.getsize(infile)/1024)
        #print(idno, filename, size_lines, size_words, size_chars, size_kb)
        
        print(idno, author_title)
        #print("<term type=\"textsize-divs\">"+"divs"+"</term>\n<term type=\"textsize-lines\">"+str(size_lines)+"</term>\n<term type=\"textsize-words\">"+str(size_words)+"</term>\n<term type=\"textsize-chars\">"+str(size_chars)+"</term>\n<term type=\"textsize-kb\">"+str(size_kb)+"</term>\n")
        print("      <extent>\n        <measure unit=\"div\">"+"divs"+"</measure>\n        <measure unit=\"lines\">"+str(size_lines)+"</measure>\n        <measure unit=\"words\">"+str(size_words)+"</measure>\n        <measure unit=\"chars\">"+str(size_chars)+"</measure>\n        <measure unit=\"kB\">"+str(size_kb)+"</measure>\n      </extent>")











###############
## MAIN      ##
###############

def main(wdir,inpath):
    get_textlength(wdir,inpath)

main(wdir, inpath)
