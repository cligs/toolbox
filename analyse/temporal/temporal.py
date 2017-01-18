#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: temporal.py
# Authors: christofs
# Version 0.1.0 (2017-01-10)


"""
TEMPORAL ANALYSIS of TOPIC DATA
"""


import os
from os.path import join
import glob
import pandas as pd
import numpy as np
import pygal


def load_data_topics(topicsovertimefile):
    with open(topicsovertimefile, "r") as infile:
        data = pd.read_csv(infile, index_col="year")
        # print(data.head())
        return data
        
def load_data_tpx(mdfile, tpxfile):
	"""
	prepare temporal expression data for temporal analysis
	@author: uh
	
	Arguments:
	mdfile: path to metadata csv file (including column "year")
	tpxfile: path to temporal expression feature csv file
	"""
	md = pd.read_csv(mdfile, index_col="idno")
	tpx = pd.read_csv(tpxfile, index_col="idno")
	data = md.merge(tpx, right_index=True, left_index=True)
	data = data.groupby("year").mean()
	data = data.drop("num_words", axis=1)
	return data


def calculate_diffs(data):
    diffs = data.diff(periods=1, axis=0)
    # print(diffs.head())
    return diffs


def calculate_sumdiffs(diffs):
    sumdiffs = diffs.abs().sum(axis=1)
    # print(sumdiffs.head)
    return sumdiffs


def transform_data(sumdiffs):
    labels = list(range(1900,2013))
    values = list(sumdiffs)[1:]
    print(len(labels))
    print(len(sumdiffs))
    return labels, values


def visualize_sumdiffs(labels, values):
    plot = pygal.Line(
        interpolate='cubic',
        x_label_rotation=90,
        x_labels_major_every=20
        )
    plot.x_labels = labels
    plot.add("sumdiffs", values)
#    for i in range(0,len(labels)-1):
#        plot.add(str(labels[i]), [values[i]])
    plot.render_to_file("sumdiffplot.svg")



def analyze_topics(mastermatrixfile, topicsovertimefile):
    data = load_data_topics(topicsovertimefile)
    diffs = calculate_diffs(data)
    sumdiffs = calculate_sumdiffs(diffs)
    labels, values = transform_data(sumdiffs)
    visualize_sumdiffs(labels, values)
    
    
def analyze_tpx(mdfile, tpxfile):
	"""
	run temporal analysis for temporal expressions
	@author: uh
	
	Arguments:
	mdfile: path to metadata csv file (including column "year")
	tpxfile: path to temporal expression feature csv file
	"""
	data = load_data_tpx(mdfile, tpxfile)
	diffs = calculate_diffs(data)
	sumdiffs = calculate_sumdiffs(diffs)
	labels, values = transform_data(sumdiffs)
	visualize_sumdiffs(labels, values)

