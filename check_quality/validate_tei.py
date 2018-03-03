# -*- coding: utf-8 -*-
# @date: April 27, 2016.
# @author: christof, ulrike

import os
import glob
from lxml import etree
from lxml import isoschematron
import sys



class FileResolver(etree.Resolver):
    def resolve(self, url, pubid, context):
        return self.resolve_filename(url, context)



def main(teipath, rngfile, schematronfile):
    """
    Arguments:
    teipath (str): path to the TEI files, e.g. /home/ulrike/Dokumente/Git/textbox/es/novela-espanola/tei/*.xml
    rngfile (str): path to the schema file, e.g. /home/ulrike/Schreibtisch/basisformat.rng
    schematronfile (str): path to the schematron file, e.g. /home/ulrike/Schreibtisch/keywords.sch
    
    Example:
    from toolbox.check_quality import validate_tei
    validate_tei.main("/home/ulrike/Git/novelashispanoamericanas/master/nh0001.xml", "/home/ulrike/Git/novelashispanoamericanas/cligs_importance.rnc", "/home/ulrike/Git/novelashispanoamericanas/keywords.sch")
    """
    for teifile in glob.glob(teipath): 
        
        idno = os.path.basename(teifile)
        #print(idno)
        
        parser = etree.XMLParser(recover=True)
        parser.resolvers.add(FileResolver())
        
        teiparsed = etree.parse(teifile, parser)
        #teiparsed = etree.parse(teifile)
        
        # RelaxNG validation
        rngparsed = etree.parse(rngfile)
        rngvalidator = etree.RelaxNG(rngparsed)
       
        validation_rng = rngvalidator.validate(teiparsed)
        log_rng = rngvalidator.error_log
        
        # Schematron validation
        sct_doc = etree.parse(schematronfile, parser)
        schematron = isoschematron.Schematron(sct_doc)
        
        validation_sch = schematron.validate(teiparsed)
        log_sch = schematron.error_log
        
        if validation_rng == True: 
            print(idno, "valid with RNG!")
        else:
            print(idno, "sorry, not valid with RNG!")
            print(log_rng)
            #print(log.last_error)
            #print(log.last_error.domain_name)
            #print(log.last_error.type_name)
        if validation_sch == True:
            print(idno, "valid with schematron!")
        else:
            print(idno, "sorry, not valid with schematron!")
            print(log_sch)	    


if __name__ == "__main__":
    main(int(sys.argv[1])) 
