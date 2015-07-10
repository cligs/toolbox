# ./bin/env python3
# get_metadata.py
# author: #cf

"""
# Extract metadata from the CLiGs teiHeader and write it to CSV.
"""

from lxml import etree
import glob
import os
import pandas as pd

def get_metadata(wdir,inpath):
    """Get metadata from teiHeader, write it to CSV."""

    ## USER: Set list of metadata items to extract
    ## Possible values: "author_short","title_short", "date", "supergenre", "genre", "subgenre"
    labels = ("author_short","title_short", "date", "supergenre", "genre", "subgenre")

    ## Dictionary of all relevant xpaths with their labels
    xpaths = {"title_short": '//tei:title[@type="short"]//text()',
              "author_short": '//tei:author//tei:name[@type="short"]//text()', 
              "date":'//tei:bibl[@type="edition-first"]//tei:date//text()',
              "supergenre":'//tei:term[@type="supergenre"]//text()',
              "genre": '//tei:term[@type="genre"]//text()',
              "subgenre":'//tei:term[@type="subgenre"]//text()',
              "idno_header": '//tei:idno[@type="cligs"]//text()'}
    namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}
    idnos = []
    
    ## Get list of file idnos and create empty dataframe
    for file in glob.glob(wdir + inpath):
        idno_file = os.path.basename(file)[0:6]
        idnos.append(idno_file)
    metadata = pd.DataFrame(columns=labels, index=idnos)
    #print(metadata)

    ## For each file, get the results of each xpath
    for file in glob.glob(wdir + inpath):
        xml = etree.parse(file)
        ## Before starting, verify that file idno and header idno are identical.
        idno_file = os.path.basename(file)[0:6]
        idno_header = xml.xpath('//tei:idno[@type="cligs"]//text()', namespaces=namespaces)[0]
        if idno_file != idno_header: 
            print("Error: "+ idno_file+ " = "+idno_header)
        for label in labels:
            xpath = xpaths[label]
            result = xml.xpath(xpath, namespaces=namespaces)
            ## Check whether something was found; if not, let the result be "n.av."
            if len(result) == 1: 
                result = result[0]
            else: 
                result = "n.av."
            ## Write the result to the corresponding cell in the dataframe
            metadata.loc[idno_file,label] = result
            
    print(metadata.head())
    metadata.to_csv(wdir+"header-metadata.csv", sep=",", encoding="utf-8")
            
def main(wdir,inpath):
    get_metadata(wdir,inpath)

main("/home/christof/Repos/cligs/romanfrancais/", "master/*.xml")
