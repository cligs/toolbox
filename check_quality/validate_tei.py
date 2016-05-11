# -*- coding: utf-8 -*-
# @date: April 27, 2016.
# @author: christof

import os
import glob
from lxml import etree

teipath = "./testtei/tc*.xml"
rngfile = "cligs.rng"

def validate_tei(teipath, rngfile):
    for teifile in glob.glob(teipath): 
        idno = os.path.basename(teifile)
        #print(idno)
        rngparsed = etree.parse("cligs.rng")
        rngvalidator = etree.RelaxNG(rngparsed)
        parser = etree.XMLParser(recover=True)
        teiparsed = etree.parse(teifile, parser)
        #teiparsed = etree.parse(teifile)
        validation = rngvalidator.validate(teiparsed)
        log = rngvalidator.error_log
        if validation == True: 
            print(idno, "valid!")
        else:
            print(idno, "sorry, not valid!")
            #print(log.last_error)
            #print(log.last_error.domain_name)

def main(teipath, rngfile):
    validate_tei(teipath, rngfile)

if __name__ == "__main__":
    main(int(sys.argv[1])) 
