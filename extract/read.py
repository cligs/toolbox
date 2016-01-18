#!/usr/bin/env python3
# Filename: teireader.py

"""
# Scripts for reading selected text from TEI files.
"""

import re
import os
import glob
from lxml import etree
 
def read_tei5(wdir, inpath, outfolder, xpath):
    """Script for reading selected text from TEI P5 files."""
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
            outfile = outfolder + filename + ".txt"
        with open(outfile,"w") as output:
            output.write(outtext)
        
    print("Done. Files treated: " + str(counter))


def read_tei4(inpath):
    """Script for reading selected text from TEI P4 (legacy) files."""
    for file in glob.glob(inpath):
        with open(file, "r") as infile:
            filename = os.path.basename(file)[:-4]
            idno = filename[:5]
            print(idno)
            ### The following options help with parsing errors; cf: http://lxml.de/parsing.html
            parser = etree.XMLParser(collect_ids=False, recover=True)
            xml = etree.parse(file, parser)

            ### The TEI P4 files do not have a namespace.
            #namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}

            ### Removes tags but conserves their text content.
            #etree.strip_tags(xml, "{http://www.tei-c.org/ns/1.0}hi")

            ### Removes elements and their text content.
            etree.strip_elements(xml, "speaker")
            etree.strip_elements(xml, "note")
            #etree.strip_elements(xml, "stage")
            etree.strip_elements(xml, "head")

            ### XPath defining which text to select
            xp_bodyprose = "//tei:body//tei:p//text()"
            xp_bodyverse = "//tei:body//tei:l//text()"
            xp_bodytext = "//body//text()"
            xp_alltext = "//text()"
            xp_castlist = "//tei:castList//text()"
            xp_stage = "//tei:stage//text()"
            xp_hi = "//tei:body//tei:hi//text()"
            xp_speakers = "//tei:body//tei:speaker//text()"

            ### Applying one of the above XPaths
            text = xml.xpath(xp_bodytext)
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
            outfile = "./txt/" + filename + ".txt"
        with open(outfile,"w") as output:
            output.write(outtext)




def main(wdir, inpath, outfolder, xpath):
    read_tei5(wdir, inpath, outfolder, xpath)
    read_tei4(inpath)

if __name__ == "__main__":
    import sys
    read_tei5(int(sys.argv[1]))
    read_tei4(int(sys.argv[1]))

