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



### TOPICS ###
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



### TEMPORAL EXPRESSIONS ###

"""
yearsteps = [1,2,5]
md_file = join(wdir, "metadata_rv.csv")

for step in yearsteps:
	
	tpx_infile = join(wdir, "tpx-corpus-counts.csv")
	tpx_outfile = join(wdir,"tpx-by-year-" + str(step) + ".csv")
	sumdiff_outfile = join(wdir, "sumdiff_" + str(step) + ".svg")
	
	temporal.analyze_tpx(md_file, tpx_infile, tpx_outfile, step, sumdiff_outfile)

	windows = [4,8,16]
	infile = join(wdir, "tpx-by-year-" + str(step) + ".csv")
	
	outfile_novelties_cosine = join(wdir, "novelties-tpx-cosine-" + str(step) + ".png")
	outfile_novelties_eucl = join(wdir, "novelties-tpx-eucl-" + str(step) + ".png")
	
	temporal.visualize_novelties(infile, windows, outfile_novelties_cosine, step, "cosine")
	temporal.visualize_novelties(infile, windows, outfile_novelties_eucl, step, "euclidean")
	
	outfile_cosine = join(wdir, "cosim-tpx-" + str(step) + ".png")
	outfile_eucl = join(wdir, "eucl-tpx-" + str(step) + ".png")
	
	temporal.visualize_similarity(infile, outfile_cosine, step, "cosine")
	temporal.visualize_similarity(infile, outfile_eucl, step, "euclidean")



"""



# calculate distances to first ten year baseline
md_file = join(wdir, "metadata_rv.csv")
all_texts_infile = join(wdir, "tpx-corpus-counts.csv")
texts_by_year_infile = join(wdir,"tpx-by-year-2.csv")
	
outfile_bl = join(wdir, "dist_to_baseline_tpx_2.svg")
	
temporal.dist_to_baseline(md_file, all_texts_infile, texts_by_year_infile, outfile_bl)

