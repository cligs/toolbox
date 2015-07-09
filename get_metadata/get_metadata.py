#!/usr/bin/env python3
# Filename: get_metadata.py
# Author: #cf

"""
# Function to extract metadata from TEI header using lxml.
"""

## TODO: Test that filename idno and metadata idno are the same; notify if not.
## TODO: Generate header from data instead of hard-coding it.

import os
import glob
from lxml import etree

#######################
# Functions           #
#######################

def get_metadata(inputpath):
    all_metadata = "idno,author,title,date,decade,subgenre,label\n"
    for file in glob.glob(inputpath):
        with open(file,"r") as sourcefile:
            filename = os.path.basename(file)[:-4]
            idno_file = filename[0:6]
            #print(idno_file)

            xml = etree.parse(sourcefile)
            namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}

            ## Text idno
            xpath = "//tei:publicationStmt//tei:idno[@type='cligs']//text()"
            result = xml.xpath(xpath, namespaces=namespaces)
            idno_header = "\n".join(result)
            #print(idno_header)
            
            if idno_file != idno_header: 
                print(idno_file + " idno error!")
            #else:
                #print(idno_file + " ok")
            
            ## Date of publication (edition-first)
            xpath = "//tei:teiHeader//tei:bibl[@type='edition-first']//tei:date//text()"
            result = xml.xpath(xpath, namespaces=namespaces)
            date = "\n".join(result)
            #print(date)
            decade = date[0:3]+"0s"
            #print(decade)

            ## Author (short form)
            xpath = "//tei:author//tei:name[@type='short']//text()"
            result = xml.xpath(xpath, namespaces=namespaces)
            author_short = "\n".join(result)
            #print(author_short)

            ## Author (full form)
            xpath = "//tei:author//tei:name[@type='full']//text()"
            result = xml.xpath(xpath, namespaces=namespaces)
            author_full = "\n".join(result)
            #print(author_full)


            ## Title (short form)
            xpath = "//tei:teiHeader//tei:title[@type='short']//text()"
            result = xml.xpath(xpath, namespaces=namespaces)
            title = "\n".join(result)
            #print(title)

            ## Subgenre
            xpath = "//tei:teiHeader//tei:term[@type='subgenre']//text()"
            result = xml.xpath(xpath, namespaces=namespaces)
            subgenre = "\n".join(result)
            #print(author)

            ## Genre label
            xpath = "//tei:teiHeader//tei:term[@type='genre-label']//text()"
            result = xml.xpath(xpath, namespaces=namespaces)
            label = "\n".join(result)
            #print(label)
            
            ## Putting everything together (one row = one document)
            metadata = idno_header +","+ author_short +","+ title +","+ date +","+ decade +","+ subgenre +","+ label +"\n"
            #print(metadata)

        all_metadata = all_metadata + metadata
    #print(all_metadata)

    with open("metadata.csv", "w") as outfile:
        outfile.write(str(all_metadata))


#######################
# Main                #
########################


def main(inputpath):
    get_metadata(inputpath)

main("../../romanfrancais/master/*.xml")

