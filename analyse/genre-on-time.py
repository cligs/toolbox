#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analysis of historical novels vs. novels of other subgenres.
Based on:
- temporal expressions
(- freeling annotations)

@author: Ulrike Henny
@filename: historical-novels.py 

"""
import sys
import os
import pandas as pd
import numpy as np
from lxml import etree
import glob
import re
import copy
import math
import matplotlib.pyplot as plt
from scipy import stats

# use the following to add the toolbox to syspath (if needed):
sys.path.append(os.path.abspath("/home/ulrike/Git/"))


from toolbox.extract import get_metadata
from toolbox.extract import visualize_metadata

"""
The data which is analyzed here has been previously annotated with the following workflows:
	annotate/workflow_teihdt.py
	annotate/workflow_teifw.py
"""

# path and filename settings
wdir = "/home/ulrike/Dokumente/Konferenzen/DH/2017/"
md_mode = "hist-nov"
md_csv = "metadata_" + md_mode + ".csv"
dir_visuals = os.path.join(wdir, "vis")





############################################### corpus description #####################################################

def summarize_corpus():
	"""
	Creates a metadata table.
	Visualizes some metadata.
	Makes some metadata counts.
	
	labels_histnov = ["idno", "language", "author-continent", "author-country", "author-name", "title", "year", "subgenre_hist", "subgenre_x"]
	"""
	
	# get metadata
	get_metadata.from_TEIP5(wdir,"corpora/base/*/*/*.xml", "metadata", md_mode)
	
	# visualize some metadata
	visualize_metadata.describe_corpus(wdir, md_csv, "author-continent")
	visualize_metadata.describe_corpus(wdir, md_csv, "author-country")
	visualize_metadata.describe_corpus(wdir, md_csv, "language")
	visualize_metadata.describe_corpus(wdir, md_csv, "subgenre_hist")
	visualize_metadata.describe_corpus(wdir, md_csv, "subgenre_x")
	visualize_metadata.plot_pie(wdir, md_csv, "subgenre_x")
	
	# make some counts
	md_table = pd.DataFrame.from_csv(os.path.join(wdir, "metadata_hist-nov.csv"), header=0)
	num_texts = len(md_table)
	num_language = len(md_table.groupby(["language"]))
	num_continent = len(md_table.groupby(["author-continent"]))
	num_countries = len(md_table.groupby(["author-country"]))
	num_authors = len(md_table.groupby(["author-name"]))
	num_subgenre_x = len(md_table.groupby(["subgenre_x"]))
	fr_subgenre_hist = md_table.groupby(["subgenre_hist"]).count()
	num_historical = fr_subgenre_hist["idno"]["historical"]
	num_not_historical = fr_subgenre_hist["idno"]["not_historical"]
	
	d = {"texts":[num_texts], 
	"languages":[num_language],
	"continents":[num_continent],
	"countries":[num_countries],
	"authors":[num_authors],
	"subgenre_x":[num_subgenre_x],
	"num_historical":[num_historical],
	"num_not_historical":[num_not_historical]}
	
	count_fr = pd.DataFrame(d)
	count_fr.to_csv(os.path.join(wdir, "corpus-counts.csv"), sep=",", header=True)
	print("Done: summarize corpus")
	
################################## Temporal expression features #####################################
"""
Documentation of labels:
	idno: text id in CLiGS project
	
	- absolute values -
	tpx_all_abs: total number of temporal expressions in the text

	tpx_date_abs: number of DATE expressions
	tpx_time_abs: number of TIME expressions
	tpx_duration_abs: number of DURATION expressions
	tpx_set_abs: number of SET expressions

	tpx_date_year_abs: number of DATE expressions with at least the YEAR specified
	tpx_date_year_month_abs: number of DATE expressions with at least YEAR and MONTH specified
	tpx_date_month_abs: number of DATE expressions with at least MONTH specified
	tpx_date_day_abs: number of DATE expressions with at least DAY specified
	tpx_date_month_day_abs: number of DATE expressions with at least MONTH and DAY specified
	tpx_date_full_abs: number of fully specified DATE expressions (YEAR, MONTH, DAY)

	tpx_date_chapter_first_abs: number of DATE expressions in the first chapter of the novel
	tpx_date_chapter_other_mean_abs: mean of DATE expressions in the remaining chapters of the novel 
	tpx_date_chapter_all_mean_abs: mean of DATE expressions in all chapters of the novel

	- relative values -
	(explanations see above; all values relative to the total number of words in the text)
	
	tpx_all_rel
	tpx_date_rel
	tpx_time_rel
	tpx_duration_rel
	tpx_set_rel

	tpx_date_year_rel
	tpx_date_year_month_rel
	tpx_date_month_rel
	tpx_date_day_rel
	tpx_date_month_day_rel
	tpx_date_full_rel

	tpx_date_chapter_first_rel
	tpx_date_chapter_other_mean_rel
	tpx_date_chapter_all_mean_rel
	
	
	- proportinal values -
	(values in proportion to the total number of temporal expressions in the text)
	
	tpx_date_prop: proportion of DATE expressions
	tpx_time_prop: proportion of TIME expressions
	tpx_duration_prop: proportion of DURATION expressions
	tpx_set_prop: proportion of SET expressions
	tpx_date_full_prop: proportion of fully specified DATE expressions
	tpx_date_chapter_first_prop: proportion of DATE expressions in the first chapter of the novel
	tpx_date_chapter_other_mean_prop: mean of the proportion of DATE expressions in the remaining chapters of the novel
	tpx_date_chapter_all_mean_prop: mean of the proportion of DATE expressions in the all chapters of the novel
"""
# labels for tpx data frame
labels_abs = ["tpx_all_abs", "tpx_date_abs", "tpx_time_abs", "tpx_duration_abs", "tpx_set_abs", "tpx_date_year_abs", 
"tpx_date_year_month_abs", "tpx_date_month_abs", "tpx_date_day_abs", "tpx_date_month_day_abs", "tpx_date_full_abs", 
"tpx_date_chapter_first_abs", "tpx_date_chapter_other_mean_abs", "tpx_date_chapter_all_mean_abs"]

labels_rel = ["tpx_all_rel", "tpx_date_rel", "tpx_time_rel", "tpx_duration_rel", "tpx_set_rel", "tpx_date_year_rel", 
"tpx_date_year_month_rel", "tpx_date_month_rel", "tpx_date_day_rel", "tpx_date_month_day_rel", "tpx_date_full_rel", 
"tpx_date_chapter_first_rel", "tpx_date_chapter_other_mean_rel", "tpx_date_chapter_all_mean_rel"]

labels_prop = ["tpx_date_prop", "tpx_time_prop", "tpx_duration_prop", "tpx_set_prop", "tpx_date_full_prop", 
"tpx_date_chapter_first_prop", "tpx_date_chapter_other_mean_prop", "tpx_date_chapter_all_mean_prop"]

labels = copy.copy(labels_abs) + copy.copy(labels_rel) + copy.copy(labels_prop)




def generate_tpx_features():
	"""
	Generates features based on the results of annotation with HeidelTime
	"""

	# path to XML files annotated with HeidelTime
	ht_inpath = os.path.join(wdir, "corpora/hdt_chapterwise/*.xml")

	labels.append("num_words")

	# read existing metadata
	md_table = pd.DataFrame.from_csv(wdir + md_csv, header=0)
	idnos = md_table.idno

	# create new data frame
	ht_fr = pd.DataFrame(columns=labels, index=idnos)
	 
	# XPath expressions for TimeML requests
	namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}

	xpaths = {"tpx_all_abs" : "count(//TIMEX3)",
	"tpx_date_abs" : "count(//TIMEX3[@type='DATE'])",
	"tpx_time_abs" : "count(//TIMEX3[@type='TIME'])",
	"tpx_duration_abs" : "count(//TIMEX3[@type='DURATION'])",
	"tpx_set_abs" : "count(//TIMEX3[@type='SET'])",
	"tpx_date_year_abs" : "count(//TIMEX3[@type='DATE'][substring(@value,1,1) != 'X' and substring(@value,2,1) != 'X' and substring(@value,3,1) != 'X' and substring(@value,4,1) != 'X'])",
	"tpx_date_year_month_abs" : "count(//TIMEX3[@type='DATE'][substring(@value,1,1) != 'X' and substring(@value,2,1) != 'X' and substring(@value,3,1) != 'X' and substring(@value,4,1) != 'X' and substring(@value,6,1) != 'X' and substring(@value,7,1) != 'X'])",
	"tpx_date_month_abs" : "count(//TIMEX3[@type='DATE'][substring(@value,6,1) != 'X' and substring(@value,7,1) != 'X'])",
	"tpx_date_day_abs" : "count(//TIMEX3[@type='DATE'][substring(@value,9,1) != 'X' and substring(@value,10,1) != 'X'])",
	"tpx_date_month_day_abs" : "count(//TIMEX3[@type='DATE'][substring(@value,6,1) != 'X' and substring(@value,7,1) != 'X' and substring(@value,9,1) != 'X' and substring(@value,10,1) != 'X'])",
	"tpx_date_full_abs" : "count(//TIMEX3[@type='DATE'][substring(@value,1,1) != 'X' and substring(@value,2,1) != 'X' and substring(@value,3,1) != 'X' and substring(@value,4,1) != 'X' and substring(@value,6,1) != 'X' and substring(@value,7,1) != 'X' and substring(@value,9,1) != 'X' and substring(@value,10,1) != 'X'])",
	"tpx_date_chapter_first_abs" : "count(//TIMEX3[@type='DATE'][substring(ancestor::tei:div/@xml:id,string-length(ancestor::tei:div/@xml:id) - 1,2) ='d1'])",
	"tpx_date_chapter_other_mean_abs" : "count(//TIMEX3[@type='DATE'][substring(ancestor::tei:div/@xml:id,string-length(ancestor::tei:div/@xml:id) - 1,2) !='d1']) div (count(//wrapper) - 1)",
	"tpx_date_chapter_all_mean_abs" : "count(//TIMEX3[@type='DATE']) div count(//wrapper)"}



	# loop through files to get HeidelTime results, first step: absolute values
	# subsequent steps build on absolute values
	for file in glob.glob(ht_inpath):
		
		idno = os.path.basename(file)[0:6]
		xml = etree.parse(file)
		
		# apply xpaths
		for label in labels_abs:
			xpath = xpaths[label]
			result = xml.xpath(xpath, namespaces=namespaces)
			
			# check the results of XPath
			"""
			if math.isnan(result):
				result = "is not a number"
			"""
			
			# Write the result into the data frame
			ht_fr.loc[idno,label] = result


	# second step: relative values (relative to the total number of words in the text)
	for file in glob.glob(ht_inpath):
		
		idno = os.path.basename(file)[0:6]
		
		# calculate total number of words in the text
		num_words = 0
		xml = etree.parse(file)
		# get XML snippets chapterwise
		wrappers = xml.xpath("//wrapper//text()")
		for wrap in wrappers:
			
			# tokenize and count
			words = re.split(r"[\s\n]+", wrap)
			num_words += len(words)
		
		ht_fr.loc[idno,"num_words"] = num_words
		
		# apply xpaths
		for label in labels_rel:
			# set corresponding absolute value label
			label_abs = label[:-3] + "abs"
			
			# fetch absolute value
			abs_val = ht_fr.loc[idno,label_abs]
			
			# check data type
			if math.isnan(abs_val):
				result = abs_val
			else:
				# calculate relative value
				result = abs_val  / num_words
			
			
			# Write the result into the data frame
			ht_fr.loc[idno,label] = result


	# third step: calculate proportions
	for file in glob.glob(ht_inpath):
		
		idno = os.path.basename(file)[0:6]
		tpx_all = ht_fr.loc[idno,"tpx_all_abs"]
		tpx_all_one = tpx_all / 100
		
		for label in labels_prop:
			# set corresponding absolute value label
			label_abs = label[:-4] + "abs"
			
			# fetch absolute value
			abs_val = ht_fr.loc[idno,label_abs]
			
			# check data type
			if math.isnan(abs_val):
				result = abs_val
			else:
				# calculate proportion
				result = abs_val / tpx_all_one
			
			# Write the result into the data frame
			ht_fr.loc[idno,label] = result
		

	ht_fr.to_csv(wdir + "corpus-counts-hdt.csv", sep=",", header=True)

	print("Done: generate tpx features")



"""
freeling-Ergebnisse auswerten
-- welche sinnvoll für time&space einzusetzen?
-- Zahl der Wörter, Sätze
-- TXM?
"""
# tbd


"""
Kombination verschiedener Merkmale
- z.B. wie groß ist der zeitlichen Abstand zwischen Handlungszeit und erster Veröffentlichung des Textes?
-- für "Handlungszeit" den Median der Jahresangaben nehmen
-- Veröffentlichungsjahr minus Handlungszeit

- wie viele Named Entities (Personen, Orte) lassen sich über Normdaten finden?
"""

##################################################### additional features ########################################
"""
Extraction of additional features, e.g. annotation features in combination with metadata, or annotation features combined with external data
"""

# How many years are there between the publication of the novel and the dates mentioned in the texts?
md_table = pd.DataFrame.from_csv(os.path.join(wdir, md_csv), header=0)
ht_table = pd.DataFrame.from_csv(os.path.join(wdir, "corpus-counts-hdt.csv"), header=0)
working_table = ht_table.join(md_table)



##################################################### visualization ##############################################

"""
visualize the distribution of specific feature values
"""

# to do: verallgemeinern für andere Subgroups
def plot_features(tpx_feature, plot_type="scatter"):
	"""
	Make a scatter or bar plot showing the number of specific temporal expressions in historical vs. non-historical novels
	
	Arguments:
	tpx_feature (string): Name of the temporal expression feature to plot
	plot_type (string): scatter or bar
	"""

	md_table = pd.DataFrame.from_csv(os.path.join(wdir, md_csv), header=0)
	ht_table = pd.DataFrame.from_csv(os.path.join(wdir, "corpus-counts-hdt.csv"), header=0)
	working_table = ht_table.join(md_table)

	# get data points and sort
	data = copy.copy(working_table[tpx_feature])
	data_sorted = data.sort_values(ascending=False)

	# get ids of historical novels
	idnos_hist = md_table[md_table["subgenre_hist"] == "historical"].index.tolist()
	# get ids of non-historical novels
	idnos_not_hist = md_table[md_table["subgenre_hist"] == "not_historical"].index.tolist()

	# split data into subgroups
	data_hist = data[idnos_hist]
	data_not_hist = data[idnos_not_hist]
		

	# get ranks
	ranks = {}
	for idx, val in enumerate(data_sorted.index):
		ranks[val] = idx
		
	if plot_type == "scatter":

		# visualize as scatterplot
		plt.figure(figsize=(20,6))

					# rank as x values, alternative: range(len(data_hist))
		plt.scatter([ranks[idno] for idno in idnos_hist],
					# counts as y values
					data_hist,
					marker = "D",
					color = "#3366CC",
					alpha = 1,
					s = 50,
					label = tpx_feature + ", historical novel"
		)

		plt.scatter([ranks[idno] for idno in idnos_not_hist],
					# counts as y values
					data_not_hist,
					marker = "o",
					color = "#DC3912",
					alpha = 1,
					s = 50,
					label = tpx_feature + ", non-historical novel"
		)
		plt.title("Novels and number of temporal expressions (TPX)")
		plt.ylabel("Number of TPX")
		plt.xlabel("Novel rank")
		plt.xlim(-5,len(data) + 5)

		plt.legend(loc='upper right')
		plt.tight_layout()

		figurename = "scatter-"+ tpx_feature +".png"
		plt.savefig(os.path.join(dir_visuals, figurename), dpi=300)
		plt.close()
	
	elif plot_type == "bar":
		# visualize as barplot
		plt.figure(figsize=(20,6))

					# rank as x values, alternative: range(len(data_hist))
		plt.bar([ranks[idno] for idno in idnos_hist],
					# counts as y values
					data_hist,
					align = "center",
					color = "#3366CC",
					alpha = 1,
					edgecolor = "#3366CC",
					label = tpx_feature + ", historical novel"
		)

		plt.bar([ranks[idno] for idno in idnos_not_hist],
					# counts as y values
					data_not_hist,
					align = "center",
					color = "#DC3912",
					alpha = 1,
					edgecolor = "#DC3912",
					label = tpx_feature + ", non-historical novel"
		)
		plt.title("Novels and number of temporal expressions (TPX)", fontsize=40)
		plt.ylabel("Number of TPX", fontsize=30)
		plt.xlabel("Novel rank", fontsize=30)
		plt.xlim(-2,len(data) + 2)
		plt.xticks(fontsize=28)
		plt.yticks(fontsize=28)

		
		plt.legend(loc='upper right', prop={'size':30})
		plt.tight_layout()

		figurename = "bar-"+ tpx_feature +".png"
		plt.savefig(os.path.join(dir_visuals, figurename), dpi=300)
		plt.close()
	
	
	print("Plotted " + figurename)
	
	
def plot_other_features(tpx_feature, md_feature, plot_type="bar"):
	"""
	Make a scatter or bar plot showing the number of specific temporal expressions in different subgroups of novels
	
	Arguments:
	tpx_feature (string): Name of the temporal expression feature to plot
	md_feature (string): Metadata feature to consider for the creation of subgroups
	plot_type (string): scatter or bar
	"""

	md_table = pd.DataFrame.from_csv(os.path.join(wdir, md_csv), header=0)
	ht_table = pd.DataFrame.from_csv(os.path.join(wdir, "corpus-counts-hdt.csv"), header=0)
	working_table = ht_table.join(md_table)

	# get data points and sort
	data = copy.copy(working_table[tpx_feature])
	data_sorted = data.sort_values(ascending=False)

	# get ids of historical novels
	idnos_hist = md_table[md_table["subgenre_hist"] == "historical"].index.tolist()
	# get ids of non-historical novels
	idnos_not_hist = md_table[md_table["subgenre_hist"] == "not_historical"].index.tolist()

	# split data into subgroups
	data_hist = data[idnos_hist]
	data_not_hist = data[idnos_not_hist]
		

	# get ranks
	ranks = {}
	for idx, val in enumerate(data_sorted.index):
		ranks[val] = idx
		
	if plot_type == "scatter":

		# visualize as scatterplot
		plt.figure(figsize=(20,6))

					# rank as x values, alternative: range(len(data_hist))
		plt.scatter([ranks[idno] for idno in idnos_hist],
					# counts as y values
					data_hist,
					marker = "D",
					color = "#3366CC",
					alpha = 1,
					s = 50,
					label = tpx_feature + ", historical novel"
		)

		plt.scatter([ranks[idno] for idno in idnos_not_hist],
					# counts as y values
					data_not_hist,
					marker = "o",
					color = "#DC3912",
					alpha = 1,
					s = 50,
					label = tpx_feature + ", non-historical novel"
		)
		plt.title("Novels and number of temporal expressions (TPX)")
		plt.ylabel("Number of TPX")
		plt.xlabel("Novel rank")
		plt.xlim(-5,len(data) + 5)

		plt.legend(loc='upper right')
		plt.tight_layout()

		figurename = "scatter-"+ tpx_feature +".png"
		plt.savefig(os.path.join(dir_visuals, figurename), dpi=300)
		plt.close()
	
	elif plot_type == "bar":
		# visualize as barplot
		plt.figure(figsize=(20,6))

					# rank as x values, alternative: range(len(data_hist))
		plt.bar([ranks[idno] for idno in idnos_hist],
					# counts as y values
					data_hist,
					align = "center",
					color = "#3366CC",
					alpha = 1,
					edgecolor = "#3366CC",
					label = tpx_feature + ", historical novel"
		)

		plt.bar([ranks[idno] for idno in idnos_not_hist],
					# counts as y values
					data_not_hist,
					align = "center",
					color = "#DC3912",
					alpha = 1,
					edgecolor = "#DC3912",
					label = tpx_feature + ", non-historical novel"
		)
		plt.title("Novels and number of temporal expressions (TPX)", fontsize=40)
		plt.ylabel("Number of TPX", fontsize=30)
		plt.xlabel("Novel rank", fontsize=30)
		plt.xlim(-2,len(data) + 2)
		plt.xticks(fontsize=28)
		plt.yticks(fontsize=28)

		
		plt.legend(loc='upper right', prop={'size':30})
		plt.tight_layout()

		figurename = "bar-"+ tpx_feature +".png"
		plt.savefig(os.path.join(dir_visuals, figurename), dpi=300)
		plt.close()
	
	
	print("Plotted " + figurename)


################################################### significance testing ##################################
"""
significance testing
"""

def do_wilcoxon_ranksum_test(tpx_feature):
	"""
	Do the Wilcoxon Ranksum Test to see if the two distributions differ significantly.
	If p <= 0.05, we are highly confident that the distributions differ significantly.
	
	Arguments:
	tpx_feature (string): Name of the temporal expression feature to test
	"""

	md_table = pd.DataFrame.from_csv(os.path.join(wdir, md_csv), header=0)
	ht_table = pd.DataFrame.from_csv(os.path.join(wdir, "corpus-counts-hdt.csv"), header=0)
	working_table = ht_table.join(md_table)

	# get data points
	data = copy.copy(working_table[tpx_feature])

	# get ids of historical novels
	idnos_hist = md_table[md_table["subgenre_hist"] == "historical"].index.tolist()
	# get ids of non-historical novels
	idnos_not_hist = md_table[md_table["subgenre_hist"] == "not_historical"].index.tolist()

	# split data into subgroups
	data_hist = data[idnos_hist]
	data_not_hist = data[idnos_not_hist]

	test_stat = stats.ranksums(data_hist, data_not_hist)
	return test_stat


"""
Anwendung: Clustern oder Masch.Lernen mit Features
"""
# tbd

########################################## Helper functions ####################################

"""
Convenience functions
"""
def plot_all_tpx_features(plot_type="scatter"):
	"""
	Make plots for all temporal expression features.
	
	Arguments:
	plot_type (string): scatter or bar
	"""
	for feature in labels:
		plot_features(feature, plot_type)
		

def calculate_all_test_stats():
	"""
	Calculate test statistics for all temporal expression features.
	"""
	# frame to hold statistics
	stats_fr = pd.DataFrame(columns=["test-statistic", "p-value"], index=labels)
	
	# do significance test for all features
	for feature in labels:
		z_stat, p_val = do_wilcoxon_ranksum_test(feature)
		stats_fr.loc[feature, "test-statistic"] = z_stat
		stats_fr.loc[feature, "p-value"] = p_val
		
	# save results to csv file
	stats_fr.to_csv(wdir + "test-statistics-tpx.csv", sep=",", header=True)
	
	print("Done: All features tested.")
	


######################################### Main part ############################################

# summarize_corpus()
# generate_tpx_features()
# plot_all_tpx_features()
# calculate_all_test_stats()


plot_all_tpx_features("bar")


