#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: temporal.py
# Authors: christofs, uh
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
import matplotlib.pyplot as plt
from sklearn import metrics
import math


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


def save_data(data, outfile):
	"""
	save pd frame data to csv file
	@author: uh
	
	Arguments:
	data: pd data frame
	outfile: path to output file
	"""
	data.to_csv(outfile)
	
def normalize_data(data):
	"""
	normalize data in frame to 0-1-range
	
	X - min(X) / max(X) - min(X)
	
	@author: uh
	
	Arguments:
	data: pd data frame
	"""
	data_norm = data.applymap(lambda x: (x - min(data.min())) / (max(data.max()) - min(data.min())))
	return data_norm

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
    #print(len(labels))
    #print(len(sumdiffs))
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
    
    
def calculate_cosine_similarities(distfile):
	"""
	calculate cosine similarities
	@author: uh
	
	Argument:
	distfile: CSV file with (normalized) distributions
	"""
	
	distributions = pd.read_csv(distfile, index_col="year")
	cosim = metrics.pairwise.cosine_similarity(distributions)
	
	return cosim
	
    
def vis_cosim_heatmap(cosim, distfile, imgfile):
	"""
	visualize cosine similarities as heatmap
	@author: uh
	
	Arguments:
	cosim: array of cosine similarities
	distfile: CSV file with (normalized) distributions
	imgfile: image filepath
	"""
	distributions = pd.read_csv(distfile, index_col="year")
	idx =  distributions.index
	
	labels = np.arange(idx[0],idx[-1],10)
	x = np.arange(0,len(cosim),10)
	plt.xticks(x,labels,rotation=90)
	plt.yticks(x,labels)
	
	plt.imshow(cosim, cmap='hot', interpolation='nearest')
	plt.gca().invert_yaxis()
	plt.savefig(imgfile)
	print("Heatmap saved.")
	
	
def kronecker(C,m):
	return np.kron(C,m)
	
def calculate_foote_novelties(cosim, window):
	"""
	calculate foote novelties for a similarity matrix
	@author: uh
	
	Arguments:
	cosim: array of cosine similarities
	window: kernel size (4, 8, 16, 32)
	"""
	S = np.matrix(cosim)
	C = np.matrix("1 -1;-1 1")
	m = np.matrix("1 1;1 1")
	
	i = 1
	while i < math.log(window,2):
		C = kronecker(C,m)
		i += 1
	
	novelties = []
	j = 0
	while j <= len(cosim) - window:
		
		subS = S[j:j+window,j:j+window]
		
		pr = np.multiply(subS,C)
		nov = pr.sum()
		novelties.append(nov) #1 / nov
		j += 1
	
	return novelties
	
		
	
def add_novelty_plot(nvs, window):
	"""
	visualize foote novelties as line plot
	@author: uh
	
	Arguments:
	nvs: array of novelty values
	window: kernel size (4, 8, 16, 32)
	"""
	for i in range(int(window / 2)):
		nvs.insert(0,0) 
		nvs.append(0)
		
	plt.plot(nvs)

	
	

def save_novelties_plot(imgfile, distfile, cosim):
	"""
	add labels to novelty plot and save
	@author: uh
	
	Arguments:
	imgfile: image file path
	distfile: CSV file with (normalized) distributions
	cosim: array of cosine similarities
	"""
	distributions = pd.read_csv(distfile, index_col="year")
	idx =  distributions.index
	labels = np.arange(idx[0],idx[-1],10)
	x = np.arange(0,len(cosim),10)
	plt.xticks(x,labels,rotation=90)
	
	plt.savefig(imgfile)
	print("Lineplot saved.")
	
		
	
#############################################################


def analyze_topics(mastermatrixfile, topicsovertimefile):
    data = load_data_topics(topicsovertimefile)
    diffs = calculate_diffs(data)
    sumdiffs = calculate_sumdiffs(diffs)
    labels, values = transform_data(sumdiffs)
    visualize_sumdiffs(labels, values)
    
    
def analyze_tpx(mdfile, tpxfile, outfile):
	"""
	run temporal analysis for temporal expressions
	@author: uh
	
	Arguments:
	mdfile: path to metadata csv file (including column "year")
	tpxfile: path to temporal expression feature csv file
	outfile: path to data output file
	"""
	data = load_data_tpx(mdfile, tpxfile)
	data = normalize_data(data)
	save_data(data, outfile)
	
	diffs = calculate_diffs(data)
	sumdiffs = calculate_sumdiffs(diffs)
	labels, values = transform_data(sumdiffs)
	visualize_sumdiffs(labels, values)

	
	
def visualize_cosim(input_dists, imgfile):
	"""
	visualize cosine similarities for a set of distributions
	@author: uh
	
	Arguments:
	input_dists: CSV file with input distributions
	imgfile: path to output imagefile
	"""
	
	cosim = calculate_cosine_similarities(input_dists)
	vis_cosim_heatmap(cosim, input_dists, imgfile)
	
	
	
def visualize_novelties(input_dists, windows, imgfile):
	"""
	visualize foote novelties
	@author: uh
	
	Arguments:
	input_dists: CSV file with input distributions
	windows: kernel sizes as list [4, 8, 16, 32]
	imgfile: path to output imagefile
	"""
	cosim = calculate_cosine_similarities(input_dists)
	
	for w in windows:
		nvs = calculate_foote_novelties(cosim, w)
		add_novelty_plot(nvs, w)
		
	save_novelties_plot(imgfile, input_dists, cosim)
	

