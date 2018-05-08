#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Annotation Workflow

- converts TEI master files to annotated TEI files
- annotation with Freeling and WordNet

The final results are stored in a folder "teia".
Run this file directly.


@author: Ulrike Henny
@filename: workflow_teifw.py 

"""

############ Options ##############

# where the TEI master files are
infolder = "/home/jose/cligs/ne/master/"

# where the annotation working files and results should go
outfolder = "/home/jose/cligs/ne/exported_corpora/anno/"

# language of the texts (possible up to now: fr, es, it, pt)
lang = "es"

server = True

print(infolder)
import sys
import os

# use the following to add the toolbox to syspath (if needed):
#sys.path.append(os.path.abspath("/home/ulrike/Git/"))

from toolbox.annotate import prepare_tei
from toolbox.annotate import annotate_fw


# by default, it should be enough to change the options above and leave this as is

prepare_tei.prepare("split", infolder, outfolder)
annotate_fw.annotate_fw(os.path.join(outfolder, "txt/*.txt"), os.path.join(outfolder, "fl/"), os.path.join(outfolder, "anno/"), lang, server)
prepare_tei.prepare("merge", outfolder, os.path.join(outfolder, "teia"))

print("--- %s seconds ---" % (time.time() - start_time))
