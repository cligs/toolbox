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

def get_metadata(wdir, inpath, metadatafile, mode):
    """Get metadata from teiHeader, write it to CSV."""

    ## USER: Set list of metadata items to extract (see xpaths for list)
    ## We can choose only the obligatory metadata, the optional or the beta. 
    ## labels = ("idno_header","author_short","author_viaf", "author-gender", "title_short", "title_viaf", "pub_year", "supergenre", "genre", "subgenre", "genre-label", "narration", "availability")
     
    labels_obl = ["idno","author-name", "author-gender", "title", "year", "supergenre", "genre",   "genre-subtitle", "availability"]
    labels_opt = ["genre-label","narrative-perspective", "narrator","protagonist-gender","setting","subgenre","subsubgenre",]
    labels_beta = [ "author-country", "author-continent",  "group-text", "protagonist-name", "protagonist-social-level", "representation", "setting-continent", "setting-country", "setting-name", "setting-territory", "subgenre-lithist", "text-movement", "time-period", "time-span", "author-text-relation", "protagonist-profession","protagonist-age","type-end"]
    
    ## Dictionary of all relevant xpaths with their labels
    xpaths = {
              "title": '//tei:title[@type="short"]//text()',
              "author-name": '//tei:author//tei:name[@type="short"]//text()', 
              "author_viaf":'//tei:author//tei:idno[@type="viaf"]//text()',
              "author-gender":'//tei:term[@type="author-gender"]//text()',
              "title_viaf":'//tei:title//tei:idno[@type="viaf"]//text()',
              "year":'//tei:bibl[@type="edition-first"]//tei:date//text()',
              "supergenre":'//tei:term[@type="supergenre"]//text()',
              "genre": '//tei:term[@type="genre"]//text()',
              "genre-subtitle":'//tei:term[@type="genre-subtitle"]//text()',
              "idno": '//tei:idno[@type="cligs"]//text()',
              "availability": '//tei:availability//@status',
              "author-country": '//tei:term[@type="author-country"]//text()',
              "author-continent": '//tei:term[@type="author-continent"]//text()',
              "genre-label":'//tei:term[@type="genre-label"]//text()',
              "narrative-perspective": '//tei:term[@type="narrative-perspective"]//text()',
              "narrator": '//tei:term[@type="narrator"]//text()',
              "setting": '//tei:term[@type="setting"]//text()',
              "protagonist-gender": '//tei:term[@type="protagonist-gender"]//text()',
              "subgenre":'//tei:term[@type="subgenre"][@subtype > parent::tei:keywords/tei:term[@type="subgenre"]/@subtype or not(parent::tei:keywords/tei:term[@type="subgenre"][2])]//text()',
              "subsubgenre":'//tei:term[@type="subsubgenre"]//text()',
              "protagonist-name": '//tei:term[@type="protagonist-name"]//text()',
              "protagonist-social-level": '//tei:term[@type="protagonist-social-level"]//text()',
              "representation": '//tei:term[@type="representation"]//text()',
              "setting-continent": '//tei:term[@type="setting-continent"]//text()',
              "setting-country": '//tei:term[@type="setting-country"]//text()',
              "setting-name": '//tei:term[@type="setting-name"]//text()',
              "setting-territory": '//tei:term[@type="setting-territory"]//text()',
              "subgenre-lithist":'//tei:term[@type="subgenre-lithist"][@subtype > parent::tei:keywords/tei:term[@type="subgenre-lithist"]/@subtype]//text()',
              "text-movement": '//tei:term[@type="text-movement"]//text()',
              "time-period": '//tei:term[@type="time-period"]//text()',
              "time-span": '//tei:term[@type="time-span"]//text()',
              "group-text": '//tei:term[@type="group-text"]//text()',
              "author-text-relation": '//tei:term[@type="author-text-relation"]//text()',
              "protagonist-profession": '//tei:term[@type="protagonist-profession"]//text()',
              "type-end": '//tei:term[@type="type-end"]//text()',
              "protagonist-age": '//tei:term[@type="protagonist-age"]//text()'
              }

    # Mode is selected: obligatory, optional or beta
    if mode =="obl":
        labels=labels_obl
    elif mode =="opt-obl":
        labels=labels_obl+labels_opt
    elif mode =="beta-opt-obl":
        labels=labels_obl+labels_opt+labels_beta
            
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
    metadata=metadata.sort("idno",ascending=True)  
    metadatafile=metadatafile+"_"+mode+".csv"
    metadata.to_csv(wdir+metadatafile, sep=",", encoding="utf-8")
    print("Done. Number of documents and metadata columns:", metadata.shape)

def main(wdir,inpath, metadatafile, mode):
    get_metadata(wdir,inpath, metadatafile, mode)

main("/home/ulrike/Dokumente/Git/textbox/es/novela-hispanoamericana/tei/", "*.xml", "metadata-from-header", "opt-obl") #The last value choose between the three modes: only obligatory, only optional (the normal mode) and beta
