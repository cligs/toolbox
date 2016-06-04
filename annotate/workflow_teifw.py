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
infolder = "/media/christof/data/Dropbox/0-Analysen/2016/sourdine/txm2/tei-test"

# where the annotation working files and results should go
outfolder = "/media/christof/data/Dropbox/0-Analysen/2016/sourdine/txm2/out"

# language of the texts (possible up to now: fr, es)
lang = "fr"

# path to FreeLing installation
FreeLingPath = "/home/christof/Programs/FreeLing4/"


import sys
import os

# use the following to add the toolbox to syspath (if needed):
sys.path.append(os.path.abspath("/home/christof/repos/cligs/"))

import prepare_tei
import annotate_fw


# by default, it should be enough to change the options above and leave this as is

prepare_tei.prepare("split", infolder, outfolder)
annotate_fw.annotate_fw(FreeLingPath, os.path.join(outfolder, "txt/*.txt"), os.path.join(outfolder, "fl/"), os.path.join(outfolder, "anno/"), lang)
prepare_tei.prepare("merge", outfolder, os.path.join(outfolder, "teia"))
