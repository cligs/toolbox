# tei2txt.py
# Script to extract selected text from several XML/TEI documents and save them to new TXT files. 
# Relies on "lxml" for parsing the XML file, on XPath for selecting parts of the XML file, and on "re" for text cleanup. 

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

for file in glob.glob('../sampletexts/*.xml'):               # Enter absolute or relative path to folder with XML files and define filename filter.
    xmltree = etree.parse(file)                              # Loads and parses the XML input file.
    textonly = xmltree.xpath('//text()')                     # Either (default): extracts all text from XML (activate only one).
#   textonly = xmltree.xpath('//body//p//text()')            # Or: Extracts all text of p in body (activate only one).
#   textonly = xmltree.xpath('//body//hi//text()')           # Or: Extracts all text of hi in body (activate only one).
#   textonly = xmltree.xpath('//body//s//text()')            # Or: Extracts all text of s in body (activate only one).
#   textonly = xmltree.xpath('//body//s[@ana="de"]//text()') # Or: Extracts all text of s with attr. ana="de" in body (activate only one).
#   textonly = xmltree.xpath('//body//head/text()')          # Or: Extracts all text of head in body (activate only one).
#   textonly = xmltree.xpath('//body//p//text()')            # Or: Extracts all speaker text from body in prose plays (activate only one).
#   textonly = xmltree.xpath('//body//l//text()')            # Or: Extracts all speaker text from body in verse plays (activate only one).
    textonly = " ".join(textonly)                            # Puts all text pieces together as a string.
    textonly = re.sub(r'\t',"",textonly)                     # Removes unnecessary indents.
    textonly = re.sub(r'\n\n',"\n",textonly)                 # Removes some of the unnecessary newlines (activate if useful)    
#   textonly = re.sub(r'\n\n',"\n",textonly)                 # Removes some of the unnecessary newlines (do twice if useful)    
    txtoutput = file[:-4] + ".txt"                           # Builds filename for outputfile from original filenames but correct extension.
    with open(txtoutput,"w") as output:                      # Writes selected text to TXT file in folder specified above.
        output.write(textonly)
