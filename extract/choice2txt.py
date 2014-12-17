#!/usr/bin/env python3
# Filename: choice2txt.py

"""
# Script to extract selected text from several TEI documents which use the "choice" mechanism and save them to new TXT files.
"""

from lxml import etree
import re
import glob
import os

def tei2txt(file):
    """Extract (selected) text content from XML/TEI and write to TXT file."""
    ## Provides information about file being treated.
    basename = os.path.basename(file)
    namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}
    print("Treating file: ", basename)
    ### Loads and parses the XML input file.
    in_xml = etree.parse(file)
    
    ### Removes selected element from XML file. 
    for toremove in in_xml.xpath("//tei:orig", namespaces=namespaces):
        toremove.getparent().remove(toremove)
    #print(etree.tostring(in_xml, pretty_print=True, xml_declaration=True))

    ### Defines XPath for selection of text.
    xpathexpr = '//tei:body//text()'
    ### Applies text extraction.
    out_txt = in_xml.xpath(xpathexpr, namespaces=namespaces) 
    ### Puts all text pieces together as a string.
    #out_txt = str(out_txt)
    out_txt = "".join(out_txt)       

    ### Removes unnecessary indents.
    out_txt = re.sub(r'\t',"",out_txt)
    ### Removes some of the unnecessary newlines / whitespaces (activate if useful)
    out_txt = re.sub(r'\n\n',"\n",out_txt)
    out_txt = re.sub(r'    ',"",out_txt)
    out_txt = re.sub(r'  ',"",out_txt)
    out_txt = re.sub(r'\n\n',"",out_txt) 

    ### Builds filename for outputfile from original filenames but correct extension.
    txtoutput = "./txt/"+ basename[:-4] + ".txt"       
    ### Writes selected text to TXT file in folder specified above.         
    with open(txtoutput,"w") as output:                  
        output.write(out_txt)

###############################
# Main
###############################

def main(inputpath):
    numberoffiles = 0
    for file in glob.glob(inputpath):
        tei2txt(file)
        numberoffiles += 1
    print("Number of files treated: ", numberoffiles)

## USER: Enter path to files.
main('./tei/*.xml')                                
