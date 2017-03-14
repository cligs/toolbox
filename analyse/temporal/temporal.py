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
import scipy.spatial.distance as distance
import scipy.stats as stats
from scipy.optimize import curve_fit
import math


def load_data_topics(topicsovertimefile):
    with open(topicsovertimefile, "r") as infile:
        data = pd.read_csv(infile, index_col="year")
        # print(data.head())
        return data
        
        
def load_data_tpx(mdfile, tpxfile, yearstep):
	"""
	prepare temporal expression data for temporal analysis
	@author: uh
	
	Arguments:
	mdfile: path to metadata csv file (including column "year")
	tpxfile: path to temporal expression feature csv file
	yearstep: step for grouping the years (e.g. 1, 2, 10)
	"""
	md = pd.read_csv(mdfile, index_col="idno")
	tpx = pd.read_csv(tpxfile, index_col="idno")
	data = md.merge(tpx, right_index=True, left_index=True)
	
	new_col = data["year"].apply(lambda x: int(math.floor(x/float(yearstep))*float(yearstep)))
	data["year_new"] = new_col
	
	data = data.groupby("year_new").mean()
	
	data = data.drop("year", axis=1)
	#data = data.drop("decade", axis=1)
	
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
	normalize data in frame to z-scores
	
	@author: uh
	
	Arguments:
	data: pd data frame
	"""
	
	"""
	rel_cols = [col for col in data.columns if '_rel' in col]
	prop_cols = [col for col in data.columns if '_prop' in col]
	
	rel_frame_norm = pd.DataFrame(stats.zscore(data[rel_cols]),index=data.index)
	prop_frame_norm = pd.DataFrame(stats.zscore(data[prop_cols]),index=data.index)
	data_norm = rel_frame_norm.merge(prop_frame_norm, left_index=True, right_index=True)
	"""
	
	data_norm = pd.DataFrame(stats.zscore(data), index=data.index)
	
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


def visualize_sumdiffs(labels, values, outfile="sumdiffplot.svg"):
    plot = pygal.Line(
        interpolate='cubic',
        x_label_rotation=90,
        x_labels_major_every=20
        )
    plot.x_labels = labels
    plot.add("sumdiffs", values)
#    for i in range(0,len(labels)-1):
#        plot.add(str(labels[i]), [values[i]])
    plot.render_to_file(outfile)
    
    
    
def calculate_similarities(distfile, mode="cosine"):
	"""
	calculate similarities / distances
	@author: uh
	
	Argument:
	distfile: CSV file with (normalized) distributions
	mode (str): kind of measure (cosine similarity, euclidean distance)
	"""
	
	distributions = pd.read_csv(distfile, index_col="year_new")
	if mode == "cosine":
		sim = metrics.pairwise.cosine_similarity(distributions)
	elif mode == "euclidean":
		sim = metrics.pairwise.euclidean_distances(distributions)
	else:
		print("Please indicate a valid mode for calculating similarities")
	
	return sim
	
	
    
def vis_similarity_heatmap(sim, distfile, imgfile, yearstep):
	"""
	visualize similarities as heatmap
	@author: uh
	
	Arguments:
	sim: array of cosine similarity / euclidean distance values
	distfile: CSV file with (normalized) distributions
	imgfile: image filepath
	yearstep: step for grouping the years (e.g. 1, 2, 10)
	"""
	distributions = pd.read_csv(distfile, index_col="year_new")
	idx =  distributions.index
	
	
	xlabelstep = 1
	if yearstep < 5:
		xlabelstep = 5
		
	labels = np.arange(idx[0],idx[-1],yearstep * xlabelstep)
	x = np.arange(0,len(sim),xlabelstep)
	
	plt.xticks(x,labels,rotation=90)
	plt.yticks(x,labels)
	
	plt.imshow(sim, cmap='hot', interpolation='nearest')
	plt.gca().invert_yaxis()
	plt.savefig(imgfile, dpi=300)
	print("Heatmap saved.")
	plt.clf()
	
	
	
def kronecker(C,m):
	return np.kron(C,m)
	
def calculate_foote_novelties(sim, window):
	"""
	calculate foote novelties for a similarity matrix
	@author: uh
	
	Arguments:
	sim: array of similarity / distance values
	window: kernel size (4, 8, 16, 32)
	"""
	S = np.matrix(sim)
	C = np.matrix("1 -1;-1 1")
	m = np.matrix("1 1;1 1")
	
	i = 1
	while i < math.log(window,2):
		C = kronecker(C,m)
		i += 1
		
	
	novelties = []
	j = 0
	while j <= len(sim) - window:
		
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

	
	

def save_novelties_plot(imgfile, distfile, sim, yearstep):
	"""
	add labels to novelty plot and save
	@author: uh
	
	Arguments:
	imgfile: image file path
	distfile: CSV file with (normalized) distributions
	sim: array of similarity / distance values
	yearstep: step for grouping the years (e.g. 1, 2, 10)
	"""
	distributions = pd.read_csv(distfile, index_col="year_new")
	idx =  distributions.index
	
	
	xlabelstep = 1
	if yearstep < 5:
		xlabelstep = 5
		
	labels = np.arange(idx[0],idx[-1],yearstep * xlabelstep)
	x = np.arange(0,len(sim),xlabelstep)
	
	plt.xticks(x,labels,rotation=90)
	#plt.tight_layout()

	plt.savefig(imgfile, dpi=300)
	print("Lineplot saved.")
	plt.clf()
	
		
	
##################### MAIN ########################################


def analyze_topics(mastermatrixfile, topicsovertimefile):
    data = load_data_topics(topicsovertimefile)
    diffs = calculate_diffs(data)
    sumdiffs = calculate_sumdiffs(diffs)
    labels, values = transform_data(sumdiffs)
    visualize_sumdiffs(labels, values)
    
    
def analyze_tpx(mdfile, tpxfile, outfile, yearstep=1, outfile_sumdiff="sumdiff.svg"):
	"""
	run temporal analysis for temporal expressions
	@author: uh
	
	Arguments:
	mdfile: path to metadata csv file (including column "year")
	tpxfile: path to temporal expression feature csv file
	outfile: path to data output file
	yearstep: step for grouping the years (e.g. 1, 2, 10)
	outfile_sumdiff: path to sumdiff image file
	"""
	data = load_data_tpx(mdfile, tpxfile, yearstep)
	data = normalize_data(data)
	save_data(data, outfile)
	
	diffs = calculate_diffs(data)
	sumdiffs = calculate_sumdiffs(diffs)
	labels, values = transform_data(sumdiffs)
	visualize_sumdiffs(labels, values, outfile_sumdiff)
	
	print("done")

	
	
def visualize_similarity(input_dists, imgfile, yearstep=1, mode="cosine"):
	"""
	visualize similarities / distances for a set of distributions
	@author: uh
	
	Arguments:
	input_dists: CSV file with input distributions
	imgfile: path to output imagefile
	yearstep: step for grouping the years (e.g. 1, 2, 10)
	mode (str): kind of measure (cosine similarity, euclidean distance)
	"""
	
	sim = calculate_similarities(input_dists, mode)
	vis_similarity_heatmap(sim, input_dists, imgfile, yearstep)
	
	
	
def visualize_novelties(input_dists, windows, imgfile, yearstep=1, mode="cosine"):
	"""
	visualize foote novelties
	@author: uh
	
	Arguments:
	input_dists: CSV file with input distributions
	windows: kernel sizes as list [4, 8, 16, 32]
	imgfile: path to output imagefile
	yearstep: step for grouping the years (e.g. 1, 2, 10)
	mode (str): kind of measure (cosine similarity, euclidean distance)
	"""
	sim = calculate_similarities(input_dists, mode)
	
	for w in windows:
		nvs = calculate_foote_novelties(sim, w)
		add_novelty_plot(nvs, w)
		
	save_novelties_plot(imgfile, input_dists, sim, yearstep)
	
def func(x, a, b, c, d, e, f):
	return a*x**5 + b*x**4 + c*x**3 + d*x**2 + e*x + f

def dist_to_baseline(md_file, all_texts_infile, texts_by_year_infile, outfile_bl):
	"""
	calculate the distance of each text to the baseline of the first ten years (average distribution)
	@author: uh
	
	Arguments:
	md_file: path to metadata file
	all_texts_infile: path to file of distributions for all the (single) texts
	texts_by_year_infile: path to file of distributions aggregated by year
	outfile_bl (str): path to output image file
	"""
	
	# calculate baseline for the first ten years
	baseline = pd.read_csv(texts_by_year_infile).iloc[0:10,1:].mean()
	
	# get distributions for all texts and metadata
	data = pd.read_csv(all_texts_infile)
	md = pd.read_csv(md_file)
	
	# calculate distance to baseline
	bl = np.array(baseline)
	
	values = []
	# get year and distance value for each text
	for idx,row in data.iterrows():
		idno = data.iloc[idx]["idno"]
		year = md.loc[md["idno"] == idno].year
		
		dt = np.array(data.iloc[idx,1:])
		dist = distance.cosine(bl, dt)
		values.append((int(year), float(dist)))
	
	slope, intercept, r_value, p_value, std_err = stats.linregress(values)
	
	x = [x[0] for x in values]
	y = [y[1] for y in values]
	popt, pcov = curve_fit(func, x, y)
	
	"""
	The result is:
	popt[0] = a , popt[1] = b, popt[2] = c and popt[3] = d of the function,
	so f(x) = popt[0]*x**3 + popt[1]*x**2 + popt[2]*x + popt[3].
	"""
	
	
	xy_chart = pygal.XY(legend_at_bottom=True, range=(0.0,1.0))
	xy_chart.title = 'Cosine distances from 1900s'
	xy_chart.add('novels', values, stroke=False)
	xy_chart.add('regression line 1', [(x, slope * x + intercept) for x in range(1900,1999)])
	xy_chart.add('regression line 2', [(x, func(x, *popt)) for x in range(1900,1999)])
	xy_chart.render_to_file(outfile_bl)
	print("Done")

	
