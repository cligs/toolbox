#!/usr/bin/env python3
# Filename: get_metadata.py

"""
# Function to transform html files from ELG into simple, clean TEI files.
"""

## TODO: von re auf lxml umstellen


import re
import glob

#######################
# Functions           #
#######################

def get_metadata(inputpath):
    all_metadata = "idno,author,date,title\n"
    for file in glob.glob(inputpath):
        with open(file,"r") as sourcefile:
            t_text = sourcefile.read()

            date = re.search("<bibl type=\"edition-first\">.*?<date>.{4}",t_text, re.DOTALL)
            date = date.group(0)
            date = str(date[-4:])
            #print(date)
            
            title = re.search("<title type=\"short\">[\w]*?</title>", t_text, re.DOTALL)
            title = title.group(0)
            title = re.sub("<title type=\"short\">([\w]*?)</title>","\\1", title)
            #print(title)

            #cligs_idno = re.search("<idno type=\"cligs\"></idno>", t_text, re.DOTALL)

            cligs_idno = ""

            author = ""
            author = re.search("<idno type=\"cligs\">[^<]*?</idno>", t_text, re.DOTALL)
            author = author.group(0)
            author = re.sub("<idno type=\"cligs\">([\w]*?)</idno>","\\1", title)
            print(author)

            metadata = cligs_idno +","+ author +","+ date +","+ title +"\n"
            #print(metadata)

        all_metadata = all_metadata + metadata
        print(all_metadata)

        with open("romanfrancais.csv", "w") as outfile:
            outfile.write(str(all_metadata))


#######################
# Main                #
########################


def main(inputpath):
    get_metadata(inputpath)

main("./tei/*.xml")

