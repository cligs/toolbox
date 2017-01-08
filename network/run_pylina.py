#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# file: run_pyzeta.py
# author: #cf
# version: 0.0.1

import pylina
import glob
import os


workdir = '/media/christof/data/Dropbox/0-Analysen/2017/teatro1/'
teipath = os.path.join(workdir, "tei/*.xml")
zffolder = os.path.join(workdir, "myzf", "")
matrixfolder = os.path.join(workdir, "matrices", "")
graphfolder = os.path.join(workdir, "graphs", "")
analysisfile = os.path.join(workdir, "analysis.csv")
threshold = 100
plotfolder = os.path.join(workdir, "plots", "")


for teifile in glob.glob(teipath):
    idno, myzf = pylina.extract(teifile, zffolder)
    matrix = pylina.matrix(idno, myzf, matrixfolder)
    graph = pylina.graph(idno, matrix, graphfolder)
    pylina.analyze(graph, analysisfile)
    pylina.draw(graph, threshold, plotfolder)
