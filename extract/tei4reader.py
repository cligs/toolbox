#!/usr/bin/env python3
# Filename: tei4reader.py

"""
# Script for reading selected text from TEI files.
"""

import re
import os
import glob
from lxml import etree

print("Using LXML version: ", etree.LXML_VERSION)

def teireader(inpath):
    """Script for reading selected text from TEI files."""
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

def main(inpath):
    teireader(inpath)

main("./tei4/*.xml")
