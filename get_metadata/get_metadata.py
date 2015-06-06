# ./bin/env python3
# get_metadata.py

"""
# Script to extract some metadata from the CLiGs standard teiHeader and write it into a CSV file.
# 6.6.2015, by #cf.
"""

from lxml import etree
import glob
import os

def get_metadata(inputpath):
    """Get metadata from teiHeader, write it to CSV."""
    for file in glob.glob(inputpath):
        idno = os.path.basename(file)[0:6]
    
        xml = etree.parse(file)
        namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}
    
        xpath = '//tei:title[@type="short"]//text()'
        shorttitle = xml.xpath(xpath, namespaces=namespaces)[0]

        xpath = '//tei:author//tei:idno[@type="cligs"]//text()'
        shortauthor = xml.xpath(xpath, namespaces=namespaces)[0]

        xpath = '//tei:bibl[@type="edition-first"]//tei:date//text()'
        date = xml.xpath(xpath, namespaces=namespaces)[0]

        xpath = '//tei:term[@type="genre"]//text()'
        genre = xml.xpath(xpath, namespaces=namespaces)[0]
        
        xpath = '//tei:term[@type="subgenre"]//text()'
        subgenre = xml.xpath(xpath, namespaces=namespaces)[0]

        metadata_row = idno + "," + shortauthor + "," + shorttitle + "," + date + "," + genre + "," + subgenre + "\n"
        print(metadata_row)
        with open("metadata.csv", "a") as metadatafile: # appending!
            metadatafile.write(metadata_row)

def main(inputpath):
    get_metadata(inputpath)
    print("\nDone.")

main('../../romanfrancais/master/rf*.xml')
