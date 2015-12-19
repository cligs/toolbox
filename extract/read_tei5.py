#!/usr/bin/env python3
# Filename: teireader.py

"""
# Script for reading selected text from TEI files.
"""

import re
import os
import glob
from lxml import etree
 
def teireader(wdir, inpath, outfolder, xpath):
    """Script for reading selected text from TEI files."""
    inpath  = wdir + inpath
    outfolder = wdir + outfolder
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    ## Do the following for each file in the inpath.
    counter = 0
    for file in glob.glob(inpath):
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
            #etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}reg")
            #etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}orig")
            etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}note")
            #etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}l")
            #etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}p")
            etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}head")
            #etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}stage")
            etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}speaker")

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
            outfile = outfolder + filename + ".txt"
        with open(outfile,"w") as output:
            output.write(outtext)
        
    print("Done. Files treated: " + str(counter))


def main(wdir, inpath, outfolder, xpath):
    teireader(wdir, inpath, outfolder, xpath)

main("", "tei/*.xml", "txt/", "bodytext")



