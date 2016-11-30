# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 07:24:56 2016

@author: jose
"""

from lxml import etree
import glob
import os


def main(inputtei, output, xpath_filter, xpath_information, split):
    """
    This sript takes the linguistic annotated output from freeling and filters with xpath_filter and takes some information with xpath_information.

    Example of how to call it:
    main(inputtei="/home/jose/cligs/ne/annotated/teia/*.xml", output="/home/jose/cligs/ne/annotated/lemmata/", xpath_filter="[@ctag='NC']", xpath_information="@lemma", split=False)
    """
    # For every xml file in the folder
    for doc in glob.glob(inputtei):
        file_name = os.path.splitext(os.path.split(doc)[1])[0]
        print(file_name)
    
        # The XML file is parsed as root element
        root_document = etree.parse(doc).getroot()
        
        # Namespaces are defined
        specific_namespaces = {'tei':'http://www.tei-c.org/ns/1.0','xi':'http://www.w3.org/2001/XInclude'}
        
        # The xpath is used
        linguistic_features = ( root_document.xpath("//tei:w"+xpath_filter+"/"+xpath_information+"", namespaces=specific_namespaces))
        #print(linguistic_features)

        if split == True:
            
            count = 0        
            while len(linguistic_features) > 60:
                part_linguistic_features = linguistic_features[0:60]
                del linguistic_features[0:60]
                # And the output is saved as a file in the output folder
                with open (os.path.join(output+file_name+"$"+str(count)+".txt"), "w", encoding="utf-8") as fout:
                    fout.write(" ".join(part_linguistic_features))
                count = count+1
        else:
            with open (os.path.join(output+file_name+".txt"), "w", encoding="utf-8") as fout:
                fout.write(" ".join(linguistic_features))
            
