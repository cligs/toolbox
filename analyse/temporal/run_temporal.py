#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: temporal.py
# Authors: christofs
# Version 0.1.0 (2017-01-10)


"""
TEMPORAL ANALYSIS of TOPIC DATA
"""


import temporal
from os.path import join


### Set the general working directory.
wdir = "/home/ulrike/Dokumente/GS/Veranstaltungen/FJR2017/"

"""
### Set parameters as used in the topic model
NumTopics = 300
NumIterations = 3000
OptimizeIntervals = 1000
param_settings = str(NumTopics) + "tp-" + str(NumIterations) + "it-" + str(OptimizeIntervals) + "in"

### Set other parameters
mastermatrixfile = join(wdir, "7_aggregates", param_settings, "mastermatrix.csv")
topicsovertimefile = join(wdir, "7_aggregates", param_settings, "avgtopicscores_by-year.csv")

### Run the functions
temporal.analyze(mastermatrixfile, topicsovertimefile)
"""

#temporal.analyze_tpx(wdir + "metadata-rv.csv", wdir + "tpx-corpus-counts.csv", wdir + "tpx-by-year.csv")

temporal.visualize_cosim("/home/ulrike/Dokumente/GS/Veranstaltungen/FJR2017/avgtopicscores_by-year.csv", "/home/ulrike/Dokumente/GS/Veranstaltungen/FJR2017/cosim-topics.png")
#temporal.visualize_cosim("/home/ulrike/Dokumente/GS/Veranstaltungen/FJR2017/tpx-by-year.csv", "/home/ulrike/Dokumente/GS/Veranstaltungen/FJR2017/cosim-tpx.png")
