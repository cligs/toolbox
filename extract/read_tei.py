#!/usr/bin/env python3
# Submodule name: read_tei.py

"""
Submodule with functions for reading selected metadata from TEI files.
To use the function of this file you have to import extract as library
@author: Christof Schöch
"""

import re
import os
import glob
from lxml import etree
import pandas as pd

def from_TEIP5(teiPath, txtFolder, xpath):
    """
    Extracts selected text from TEI P5 files and writes TXT files.
    xpath (string): "alltext", "bodytext, "seg" or "said".
    
    For example:
    from toolbox.extract import read_tei
    read_tei.from_TEIP5("/home/jose/CLiGS/ne/master/*.xml","/home/jose/CLiGS/ne/txt","bodytext")
    """
    if not os.path.exists(txtFolder):
        os.makedirs(txtFolder)
    ## Do the following for each file in the inpath.
    counter = 0
    for file in glob.glob(teiPath):
        with open(file, "r"):
            filename = os.path.basename(file)[:-4]
            idno = filename[:6] # assumes idno is at the start of filename.
            #print("Treating " + idno)
            counter +=1
            xml = etree.parse(file)
            namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}

            ### Removes tags but conserves their text content.
            ### USER: Uncomment as needed.
            etree.strip_tags(xml, "{http://www.tei-c.org/ns/1.0}seg")
            #etree.strip_tags(xml, "{http://www.tei-c.org/ns/1.0}said")
            #etree.strip_tags(xml, "{http://www.tei-c.org/ns/1.0}hi")

            ### Removes elements and their text content.
            ### USER: Uncomment as needed.
            #etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}reg", with_tail=False)
            #etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}orig", with_tail=False)
            etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}note", with_tail=False)
            etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}quote", with_tail=False)
            #etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}l", with_tail=False)
            #etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}p", with_tail=False)
            etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}head", with_tail=False)
            #etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}stage", with_tail=False)
            etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}speaker", with_tail=False)

            ### XPath defining which text to select
            xp_bodytext = "//tei:body//text()"
            xp_alltext = "//text()"
            xp_seg = "//tei:body//tei:seg//text()"
            xp_said = "//tei:body//tei:said//text()"
            #xp_bodyprose = "//tei:body//tei:p//text()"
            #xp_bodyverse = "//tei:body//tei:l//text()"
            #xp_castlist = "//tei:castList//text()"
            #xp_stage = "//tei:stage//text()"
            #xp_hi = "//tei:body//tei:hi//text()"
            
            ### Applying one of the above XPaths, based on parameter passed.
            ### USER: use on of the xpath values used here in the parameters.
            if xpath == "bodytext": 
                text = xml.xpath(xp_bodytext, namespaces=namespaces)
            if xpath == "alltext": 
                text = xml.xpath(xp_alltext, namespaces=namespaces)
            if xpath == "seg": 
                text = xml.xpath(xp_seg, namespaces=namespaces)
            if xpath == "said": 
                text = xml.xpath(xp_said, namespaces=namespaces)
            text = "\n".join(text)

            ### Some cleaning up
            text = re.sub("[ ]{2,8}", " ", text)
            text = re.sub("\n{2,8}", "\n", text)
            text = re.sub("[ \n]{2,8}", " \n", text)
            text = re.sub("\t{1,8}", "\t", text)

            # TODO: Improve whitespace handling.
            
            outtext = str(text)
            outfile = txtFolder + filename + ".txt"
        with open(outfile,"w") as output:
            output.write(outtext)
        
    print("Done. Files treated: " + str(counter))


def from_TEIP4(teiFolder, txtFolder):
    """
    Extracts selected text from TEI P4 (legacy) files and writes TXT files.
    """
    print("\nread_tei4...")
    teiPath  = teiFolder + "*.xml"
    if not os.path.exists(txtFolder):
        os.makedirs(txtFolder)
    for file in glob.glob(teiPath):
        with open(file, "r") as infile:
            filename = os.path.basename(file)[:-4]
            idno = filename[:5]
            print(idno)
            ### The following options help with parsing errors; cf: http://lxml.de/parsing.html
#            parser = etree.XMLParser(recover=True)
#            xml = etree.parse(file, parser)
            xml = etree.parse(file)

            ### The TEI P4 files do not have a namespace.
            #namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}

            ### Removes tags but conserves their text content.
            #etree.strip_tags(xml, "{http://www.tei-c.org/ns/1.0}hi")

            ### Removes elements and their text content.
            etree.strip_elements(xml, "speaker", with_tail=False)
            etree.strip_elements(xml, "note", with_tail=False)
            #etree.strip_elements(xml, "stage", with_tail=False)
            etree.strip_elements(xml, "head", with_tail=False)

            ### XPath defining which text to select
            xp_bodyprose = "//body//p//text()"
            xp_bodyverse = "//body//l//text()"
            xp_bodytext = "//body//text()"
            xp_alltext = "//text()"
            xp_allLines = "//l//text()"
            xp_teiHeader = "//teiHeader//text()"
            xp_castlist = "//castList//text()"
            xp_stage = "//stage//text()"
            xp_hi = "//body//hi//text()"
            xp_speakers = "//body//speaker//text()"

            ### Applying one of the above XPaths
            text = xml.xpath(xp_alltext)
            text = "\n".join(text)

            ### Some cleaning up
            text = re.sub("  ", "", text)
            #text = re.sub("    ", "", text)
            #text = re.sub("\n{1,6}", "", text)
            text = re.sub("\n{1,6}", "\n", text)
            text = re.sub("\n{1,6}", "\n", text)
            text = re.sub("\n \n", "\n", text)
            text = re.sub("\t\n", "", text)

            ### Marking scene transitions
            #text = re.sub("ACTE[^$]*?\n", "", text)
            #text = re.sub("SCÈNE[^$]*?\n", "###\n", text)

            outtext = str(text)
            outfile = txtFolder + filename + ".txt"
        with open(outfile,"w") as output:
            output.write(outtext)
            
            
def main(teiFolder, txtFolder, xpath):
    from_TEIP5(teiFolder, txtFolder, xpath)
    from_TEIP4(teiFolder, txtFolder)
    
if __name__ == "__main__":
    import sys
    from_TEIP5(int(sys.argv[1]))
    from_TEIP4(int(sys.argv[1]))
