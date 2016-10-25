#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analysis of historical novels vs. novels of other subgenres.
Based on:
- temporal expressions
- freeling annotations

@author: Ulrike Henny
@filename: historical-novels.py 

"""
import sys
import os
import pandas as pd
from lxml import etree
import glob
import re
import copy

# use the following to add the toolbox to syspath (if needed):
sys.path.append(os.path.abspath("/home/ulrike/Git/"))


from toolbox.extract import get_metadata
from toolbox.extract import visualize_metadata

"""
The data which is analyzed here has been previously annotated with the following workflows:
	annotate/workflow_teihdt.py
	annotate/workflow_teifw.py
"""

wdir = "/home/ulrike/Dokumente/Konferenzen/DH/2017/"


def summarize_corpus():
	"""
	Creates a metadata table.
	Visualizes some metadata.
	Makes some metadata counts.
	
	labels_histnov = ["idno", "language", "author-continent", "author-country", "author-name", "title", "year", "subgenre_hist", "subgenre_x"]
	"""
	
	# get metadata
	md_mode = "hist-nov"
	get_metadata.from_TEIP5(wdir,"corpora/base/*/*/*.xml", "metadata", md_mode)
	md_csv = "metadata_" + md_mode + ".csv" 
	
	# visualize some metadata
	visualize_metadata.describe_corpus(wdir, md_csv, "author-continent")
	visualize_metadata.describe_corpus(wdir, md_csv, "author-country")
	visualize_metadata.describe_corpus(wdir, md_csv, "language")
	visualize_metadata.describe_corpus(wdir, md_csv, "subgenre_hist")
	visualize_metadata.describe_corpus(wdir, md_csv, "subgenre_x")
	visualize_metadata.plot_pie(wdir, md_csv, "subgenre_x")
	
	# make some counts
	md_table = pd.DataFrame.from_csv(wdir + "metadata_hist-nov.csv", header=0)
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
	count_fr.to_csv(wdir + "corpus-counts.csv", sep=",", header=True)
	print("Done")
	


def generate_hdt_features():
	"""
	Generates features based on the results of annotation with HeidelTime
	
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
	tpx_date_chapter_other_abs: mean of DATE expressions in the remaining chapters of the novel 
	

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
	tpx_date_chapter_other_rel
	
	
	- proportinal values -
	(values in proportion to the total number of temporal expressions in the text)
	
	tpx_date_prop: proportion of DATE expressions
	tpx_time_prop: proportion of TIME expressions
	tpx_duration_prop: proportion of DURATION expressions
	tpx_set_prop: proportion of SET expressions
	tpx_date_full_prop: proportion of fully specified DATE expressions
	tpx_date_chapter_first_prop: proportion of DATE expressions in the first chapter of the novel
	"""



# path to XML files annotated with HeidelTime
ht_inpath = wdir + "corpora/hdt_chapterwise/*.xml"

# labels for data frame
labels_abs = ["tpx_all_abs", "tpx_date_abs", "tpx_time_abs", "tpx_duration_abs", "tpx_set_abs"]
"""
, "tpx_date_year_abs", 
"tpx_date_year_month_abs", "tpx_date_month_abs", "tpx_date_day_abs", "tpx_date_month_day_abs", "tpx_date_full_abs", 
"tpx_date_chapter_first_abs", "tpx_date_chapter_other_abs"]
"""
labels_rel = ["tpx_all_rel", "tpx_date_rel", "tpx_time_rel", "tpx_duration_rel", "tpx_set_rel"]
""" 
, "tpx_date_year_rel", 
"tpx_date_year_month_rel", "tpx_date_month_rel", "tpx_date_day_rel", "tpx_date_month_day_rel", "tpx_date_full_rel", 
"tpx_date_chapter_first_rel", "tpx_date_chapter_other_rel"
 """
labels_prop = ["tpx_date_prop", "tpx_time_prop", "tpx_duration_prop", "tpx_set_prop"]
""" 
 "tpx_date_full_prop", "tpx_date_chapter_first_prop" 
 """
labels = copy.copy(labels_abs) #+ labels_rel + labels_prop
labels.append("num_words")


# read existing metadata
md_table = pd.DataFrame.from_csv(wdir + "metadata_hist-nov.csv", header=0)
idnos = md_table.idno

# crate new data frame
ht_fr = pd.DataFrame(columns=labels, index=idnos)
 
# XPath expressions for TimeML requests
xpaths = {"tpx_all_abs" : "count(//TIMEX3)",
"tpx_date_abs" : "count(//TIMEX3[@type='DATE'])",
"tpx_time_abs" : "count(//TIMEX3[@type='TIME'])",
"tpx_duration_abs" : "count(//TIMEX3[@type='DURATION'])",
"tpx_set_abs" : "count(//TIMEX3[@type='SET'])"}
""",
"tpx_date_year_abs" : "count(//TIMEX3[@type='DATE'][substring(@value,1,1) != 'X' and substring(@value,2,1) != 'X' and substring(@value,3,1) != 'X' and substring(@value,4,1) != 'X'])",
"tpx_date_year_month_abs" : "count(//TIMEX3[@type='DATE'][substring(@value,1,1) != 'X' and substring(@value,2,1) != 'X' and substring(@value,3,1) != 'X' and substring(@value,4,1) != 'X' and substring(@value,6,1) != 'X' and substring(@value,7,1) != 'X')])",
"tpx_date_month_abs" : "count(//TIMEX3[@type='DATE'][substring(@value,6,1) != 'X' and substring(@value,7,1) != 'X'])",
"tpx_date_day_abs" : "count(//TIMEX3[@type='DATE'][substring(@value,9,1) != 'X' and substring(@value,10,1) != 'X'])",
"tpx_date_month_day_abs" : "count(//TIMEX3[@type='DATE'][substring(@value,6,1) != 'X' and substring(@value,7,1) != 'X' and substring(@value,9,1) != 'X' and substring(@value,10,1) != 'X'])",
"tpx_date_full_abs" : "count(//TIMEX3[@type='DATE'][substring(@value,1,1) != 'X' and substring(@value,2,1) != 'X' and substring(@value,3,1) != 'X' and substring(@value,4,1) != 'X' and substring(@value,6,1) != 'X' and substring(@value,7,1) != 'X' and substring(@value,9,1) != 'X' and substring(@value,10,1) != 'X'])",
"tpx_date_chapter_first_abs" : "count(//TIMEX3[@type='DATE'][ends-with(parent::div/@xml:id,'d1')])",
"tpx_date_chapter_other_abs" : "count(//TIMEX3[@type='DATE'][not(ends-with(parent::div/@xml:id,'d1'))]) div (count(//wrapper) - 1)" """

# loop through files to get HeidelTime results, first step: absolute values
# subsequent steps build on absolute values
for file in glob.glob(ht_inpath):
	
	idno = os.path.basename(file)[0:6]
	xml = etree.parse(file)
	
	# apply xpaths
	for label in labels_abs:
		xpath = xpaths[label]
		result = xml.xpath(xpath)
		
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
		
		# calculate relative value
		result = ht_fr.loc[idno,label_abs] / num_words
		
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
		
		# calculate proportion
		result = ht_fr.loc[idno,label_abs] / tpx_all_one
	
		# Write the result into the data frame
		ht_fr.loc[idno,label] = result
	


print(ht_fr)
ht_fr.to_csv(wdir + "corpus-counts-hdt.csv", sep=",", header=True)




"""
freeling-Ergebnisse auswerten
-- welche sinnvoll für time&space einzusetzen?
-- Zahl der Wörter, Sätze
-- TXM?
"""



"""
Kombination verschiedener Merkmale
- z.B. wie groß ist der zeitlichen Abstand zwischen Handlungszeit und erster Veröffentlichung des Textes?
-- für "Handlungszeit" den Median der Jahresangaben nehmen
-- Veröffentlichungsjahr minus Handlungszeit

- wie viele Named Entities (Personen, Orte) lassen sich über Normdaten finden?
"""


"""
Visualisieren einzelner Features
"""

"""
Signifikanz-Tests für einzelne Features
"""


"""
Anwendung: Clustern oder Masch.Lernen mit Features
"""


# summarize_corpus()


