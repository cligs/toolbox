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


Check for existing FreeLing servers from the command line:
netstat -tlnp | grep analyzer
Kill existing FreeLing server:
kill 6899 (for example)

"""

############ Options ##############

# where the TEI master files are

infolder = "/home/ulrike/Git/IDE/novelashispanoamericanas/master/"

# where the annotation working files and results should go
outfolder = "/home/ulrike/Git/IDE/novelashispanoamericanas/annotiert/"

# language of the texts (possible up to now: fr, es, it, pt)
lang = "es"

server = True

print(infolder)
import sys
import os
import time
start_time = time.time()

# use the following to add the toolbox to syspath (if needed):
sys.path.append(os.path.abspath("/home/ulrike/Git/"))

from toolbox.annotate import prepare_tei
from toolbox.annotate import annotate_fw


# by default, it should be enough to change the options above and leave this as is

prepare_tei.prepare("split", infolder, outfolder)
annotate_fw.annotate_fw(os.path.join(outfolder, "txt/*.txt"), os.path.join(outfolder, "fl/"), os.path.join(outfolder, "annotated_temp/"), lang, server)
prepare_tei.prepare("merge", outfolder, os.path.join(outfolder, "annotated"))

print("--- %s seconds ---" % (time.time() - start_time))

