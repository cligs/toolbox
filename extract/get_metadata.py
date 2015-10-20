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

def get_metadata(wdir, inpath, metadatafile):
    """Get metadata from teiHeader, write it to CSV."""

    ## USER: Set list of metadata items to extract (see xpaths for list)
    ## labels = ("idno_header","author_short","author_viaf", "author-gender", "title_short", "title_viaf", "pub_year", "supergenre", "genre", "subgenre", "genre-label", "narration", "availability")
    labels = ("idno","author-name", "author-gender", "title", "year", "supergenre", "genre", "subgenre", "genre-label", "genre-subtitle", "narration", "availability", "setting", "protagonist-gender", "author-country", "author-continent", "narrator")

    ## Dictionary of all relevant xpaths with their labels
    xpaths = {"title": '//tei:title[@type="short"]//text()',
              "author-name": '//tei:author//tei:name[@type="short"]//text()', 
              "author_viaf":'//tei:author//tei:idno[@type="viaf"]//text()',
              "author-gender":'//tei:term[@type="author-gender"]//text()',
              "title_viaf":'//tei:title//tei:idno[@type="viaf"]//text()',
              "year":'//tei:bibl[@type="edition-first"]//tei:date//text()',
              "supergenre":'//tei:term[@type="supergenre"]//text()',
              "genre": '//tei:term[@type="genre"]//text()',
              "subgenre":'//tei:term[@type="subgenre"]//text()',
              "genre-label":'//tei:term[@type="genre-label"]//text()',
              "genre-subtitle":'//tei:term[@type="genre-subtitle"]//text()',
              "idno": '//tei:idno[@type="cligs"]//text()',
              "narration": '//tei:term[@type="narrative-perspective"]//text()',
              "availability": '//tei:availability//@status',
              "setting": '//tei:term[@type="setting"]//text()',
              "protagonist-gender": '//tei:term[@type="protagonist-gender"]//text()',
              "author-country": '//tei:term[@type="author-country"]//text()',
              "author-continent": '//tei:term[@type="author-continent"]//text()',
              "narrator": '//tei:term[@type="narrator"]//text()'
              }
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
        #print(file)
        xml = etree.parse(file)
        ## Before starting, verify that file idno and header idno are identical.
        idno_file = os.path.basename(file)[0:6]
        idno_header = xml.xpath(xpaths["idno"], namespaces=namespaces)[0]
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
                
    ## Add decade column based on pub_year
    metadata["decade"] = metadata["year"].map(lambda x: str(x)[:-1]+"0s")
    
    ## Check result and write CSV file to disk.
    #print(metadata.head())
    metadata.to_csv(wdir+metadatafile, sep=",", encoding="utf-8")
    print("Done. Number of documents and metadata columns:", metadata.shape)

def main(wdir,inpath, metadatafile):
    get_metadata(wdir,inpath, metadatafile)

main("/home/jose/CLiGS/pruebas/20150921_jctne_900l_10b_70t_70mfwd/master/", "*.xml", "metadata_from_header.csv")
