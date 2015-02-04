#!/usr/bin/env python3
# Filename: teireader.py

"""
# Script for reading selected text from TEI files.
"""

import re
import os
import glob
from lxml import etree

def teireader(inpath):
    """Script for reading selected text from TEI files."""
    for file in glob.glob(inpath):
        with open(file, "r") as infile:
            filename = os.path.basename(file)[:-4]
            idno = filename[:5]
            print(idno)
            xml = etree.parse(file)
            namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}

            ### Removes tags but conserves their text content.
            #etree.strip_tags(xml, "{http://www.tei-c.org/ns/1.0}hi")

            ### Removes elements and their text content.
            #etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}note")
            etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}l")
            #etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}p")
            etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}head")
            #etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}stage")
            #etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}speaker")

            ### XPath to define which text to select
            xp_bodyprose = "//tei:body//tei:p//text()"
            xp_bodyverse = "//tei:body//tei:l//text()"
            xp_bodytext = "//tei:body//text()"
            xp_alltext = "//text()"
            xp_castlist = "//tei:front//tei:castList//text()"
            xp_stage = "//tei:body//tei:stage//text()"
            text = xml.xpath(xp_bodytext, namespaces=namespaces)

            ### Some cleaning up
            text = "\n".join(text)
            text = re.sub("  ", "", text)
            #text = re.sub("    ", "", text)
            #text = re.sub("\n{1,6}", "", text)
            text = re.sub("\n{1,6}", "\n", text)
            text = re.sub("\n{1,6}", "\n", text)

            outtext = str(text)
            outfile = "./txt/" + filename + ".txt"
        with open(outfile,"w") as output:
            output.write(outtext)

def main(inpath):
    teireader(inpath)

main("./tei/*.xml")
