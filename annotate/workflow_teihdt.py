#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Annotation Workflow

- converts TEI master files to annotated TEI files
- annotation with heideltime

The final results are stored in a folder "teia".
Run this file directly.


@author: Ulrike Henny
@filename: workflow_teihdt.py 

"""

############ Options ##############

# where the TEI master files are
infolder = "/home/ulrike/Dokumente/GS/Veranstaltungen/DHd17/corpus_master/to_do"

# where the annotation working files and results should go
outfolder = "/home/ulrike/Dokumente/GS/Veranstaltungen/DHd17/corpus_hdt"

# language of the texts (possible up to now: fr, es)
lang = "SPANISH"

# path to heideltime installation
heideltimePath = "/home/ulrike/Programme/heideltime/heideltime-standalone"


import sys
import os

# use the following to add the toolbox to syspath (if needed):
sys.path.append(os.path.abspath("/home/ulrike/Dokumente/Git/"))

from toolbox.annotate import prepare_tei
from toolbox.annotate import use_heideltime


# by default, it should be enough to change the options above and leave this as is

#prepare_tei.prepare("split", infolder, outfolder)
#use_heideltime.apply_ht(heideltimePath, os.path.join(outfolder, "txt"), os.path.join(outfolder, "hdt"), lang)
#use_heideltime.wrap_body("/home/ulrike/Dokumente/GS/Veranstaltungen/DHd17/corpus_hdt/hdt", "/home/ulrike/Dokumente/GS/Veranstaltungen/DHd17/corpus_hdt/anno")
prepare_tei.prepare("merge", outfolder, os.path.join(outfolder, "teia"))
