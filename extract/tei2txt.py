# tei2txt.py
# Script to extract selected text from several TEI documents and save them to new TXT files. 
# Relies on "lxml" for parsing the TEI file, on XPath for selecting parts of the TEI file, and on "re" for text cleanup. 
# Note: the namespace solution used here makes this incompatible with plain XML or TEI P4; in these cases, use xml2txt.py.

###############################
# Overview of functions
###############################

# 1. Load several XML files from a folder one after the other.
# 2. For each file, parse the file to build a Python element tree representation. 
# 3. For each file, extract selected text from XML according to one of several alternative XPath expressions.
# 4. For each file, write new TXT file to the folder.  

###############################
# User settings
###############################

# 1. Modify the path to the working directory
# 2. Modify the filename filter
# 3. Select which XPath expression to use and/or adapt it to your needs.
# 4. Select which cleanup procedures should be used and/or adapt them to your needs.

###############################
# Import statements
###############################

from lxml import etree
import re
import glob

###############################
# Actual text processing
###############################

def tei2txt(file): 
    """Load TEI files from folder, extract selected text, save to new TXT files"""                                      
    xmltree = etree.parse(file)                          # Loads and parses the XML input file.
    namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}   # Defines the namespace to be used in the xpathexpr.
    
#   xpathexpr = '//text()'                               # Default XPath expression: all text from XML (activate only one!)
    xpathexpr = '//tei:body//tei:p//text()'              # Or: All text of p in body in prose texts.
#   xpathexpr = '//tei:body//tei:l//text()'              # Or: All text of l in body in verse plays.
#   xpathexpr = '//tei:body//tei:hi//text()'             # Or: All text of hi in body.
#   xpathexpr = '//tei:body//tei:s//text()'              # Or: All text of s in body 
#   xpathexpr = '//tei:body//tei:s[@ana="de"]//text()'   # Or: All text of s with attr. ana="de" in body.
#   xpathexpr = '//tei:body//tei:stage//text()'          # Or: All stage directions in body.
#   xpathexpr = '//tei:body//tei:head/text()'            # Or: All text of head in body.

    textonly = xmltree.xpath(xpathexpr, namespaces=namespaces) # Extracts the text according to the XPath expression "xpathexpr".
    textonly = " ".join(textonly)                        # Puts all text pieces together as a string.
    textonly = re.sub(r'\t',"",textonly)                 # Removes unnecessary indents.
    textonly = re.sub(r'\n\n',"\n",textonly)             # Removes some of the unnecessary newlines (activate if useful)    
#   textonly = re.sub(r'\n\n',"\n",textonly)             # Removes some of the unnecessary newlines (do twice if useful)    
    txtoutput = file[:-4] + ".txt"                       # Builds filename for outputfile from original filenames but correct extension.
    with open(txtoutput,"w") as output:                  # Writes selected text to TXT file in folder specified above.
        output.write(textonly)

###############################
# Main
###############################

def main(inputpath): 
    for file in glob.glob(inputpath): 
        tei2txt(file)

main('./input/Piege.xml')                                # Enter absolute or relative path to folder with XML files and define filename filter.
