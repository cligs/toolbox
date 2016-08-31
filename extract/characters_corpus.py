# -*- coding: utf-8 -*-
"""
This script gives a list of the caracters that appear in a corpus. This can be usefull for using
this characters to analize or clean better the texts.

Created on Tue Aug 30 14:20:58 2016

@author: jose
"""

import pandas as pd
import re
import glob
import os
import numpy as np

def main(basic_wdir, input_wdir):
    """
    Example of how to use it:
    main ("/home/jose/cligs/ne/", "master/*.xml")
    """
    # An empty string is created 
    total_characters = ""

    # We open each file
    for doc in glob.glob(basic_wdir+input_wdir):
        idno_file = os.path.basename(doc)
        print(idno_file)
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()
            
            # The file is divided in letters as a set
            caracteres = ''.join(set(content))
            # We added to the string that will contain everything
            total_characters = caracteres + total_characters
    
    # When we are done with all the files, we do the same so the characters are not repeated
    total_characters = ''.join(set(total_characters))
    print("========\n All the charactes found in this corpus:\n\n", total_characters,"\n\n========")

    # A file with all the characters is created  
    with open (os.path.join(basic_wdir+"characters.txt"), "w", encoding="utf-8") as fout:
        fout.write(total_characters)
    return total_characters
    
