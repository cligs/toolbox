# -*- coding: utf-8 -*-
# @date: April 27, 2016.
# @author: christof

import os
import glob
from lxml import etree
import sys


def main(teipath, rngfile):
	"""
	Arguments:
	teipath (str): path to the TEI files, e.g. /home/ulrike/Dokumente/Git/textbox/es/novela-espanola/tei/*.xml
	rngfile (str): path to the schema file, e.g. /home/ulrike/Schreibtisch/basisformat.rng
	
	Example:
	from toolbox import check_quality
	check_quality.validate_tei("/home/ulrike/Dokumente/Git/textbox/es/novela-espanola/tei/*.xml", "/home/ulrike/Schreibtisch/basisformat.rng")
	"""
    for teifile in glob.glob(teipath): 
        idno = os.path.basename(teifile)
        #print(idno)
        rngparsed = etree.parse(rngfile)
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
            print(log)
            #print(log.last_error)
            #print(log.last_error.domain_name)
            #print(log.last_error.type_name)


if __name__ == "__main__":
    main(int(sys.argv[1])) 
