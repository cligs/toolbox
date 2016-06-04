# ./bin/env python3
# prettyprint_xml.py
# author: #cf

"""
# Pretty print XML files.
"""

from lxml import etree
import glob
import os

def prettyprint_xml(wdir, inpath, outfolder):
    """Pretty print XML files."""
    counter = 0
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    for file in glob.glob(wdir + inpath):
        basename = os.path.basename(file)
        #print(file)
        counter +=1
        parser = etree.XMLParser(remove_blank_text=True)
        xml = etree.parse(file, parser)
        pretty_xml = etree.tostring(xml, pretty_print=True, encoding='utf-8')
        #print(pretty_xml)        
        newfilename = wdir+outfolder+basename
        with open(newfilename,"wb") as outputfile:
            outputfile.write(pretty_xml)
    print("Done. Number of documents prettified: " + str(counter))

def main(wdir,inpath, outfolder):
    prettyprint_xml(wdir,inpath, outfolder)

main("/home/christof/Repos/cligs/romanfrancais/", "master/*.xml", "pretty/")
