#!/usr/bin/env python3
# Filename: my_tmw.py

"""
# Topic Modeling Pipeline for todays particular project.
"""


import tmw
#print(help(topmod))

### Set the general working directory.
wdir = "/home/christof/Repos/clgs/toolbox/tmw/scenes/"

### tei4reader (standard option)
inpath = wdir + "0_tei/*.xml"
outfolder = wdir + "1_txt/"
#tmw.tei4reader(inpath,outfolder)

### tei4reader_scenes (reads text and splits plays at scene boundaries)
inpath = wdir + "0_tei/*.xml"
outfolder = wdir + "2_scenes/"
tmw.tei4reader_scenes(inpath,outfolder)

### segmenter
inpath = wdir + "1_txt/*.txt"
outpath = wdir + "2_segments/"
segment_length = 2000
#tmw.segmenter(inpath,outpath,segment_length)

### segments_to_bins: inpath, outfile
inpath = wdir + "2_segments/*.txt"
outfile = wdir + "segments-and-bins.csv"
#tmw.segments_to_bins(inpath,outfile)

### scenes_to_bins
inpath = wdir + "2_scenes/*.txt"
outfolder = wdir + "2_scenes_bins/"
outfile = wdir + "scenes-and-bins.csv"
tmw.scenes_to_bins(inpath,outfolder,outfile)

### pretokenize
inpath = wdir + "2_segments/*.txt"
outfolder = wdir + "3_tokenized/"
#tmw.pretokenize(inpath,outfolder)

### call_treetagger
infolder = wdir + "3_tokenized/"
outfolder = wdir + "4_tagged/"
tagger = "/home/christof/Programs/TreeTagger/cmd/tree-tagger-french"
#tmw.call_treetagger(infolder, outfolder, tagger) 

### make_lemmatext
inpath = wdir + "4_tagged/*.trt"
outfolder = wdir + "5_lemmata/"
#tmw.make_lemmatext(inpath,outfolder)

### call_mallet_import
infolder = wdir + "5_lemmata"
stoplist = wdir + "fr-lem.txt"
outfile = wdir + "tc30.mallet"
#tmw.call_mallet_import(infolder,outfile,stoplist)

### call_mallet_model
inputfile = wdir + "tc30.mallet"
outfolder = wdir + "6_mallet-results/"
num_topics = "30"
optimize_interval = "100"
num_iterations = "10000"
num_top_words = "20"
doc_topics_max = "30"
num_threads = "4"
#tmw.call_mallet_modeling(inputfile,outfolder,num_topics,optimize_interval,num_iterations,num_top_words,doc_topics_max)

### generate_wordlescores
word_weights_file = wdir + "6_mallet-results/" + "word-weights.txt"
wordlescores_file = wdir + "6_mallet-results/" + "wordle-scores.txt"
topics = 30
words = 100
#tmw.generate_wordlescores(word_weights_file,wordlescores_file,topics,words)

### aggregate_using_metadata
corpuspath = wdir + "5_lemmata"
outfolder = wdir + "7_aggregates/"
topics_in_texts = wdir + "6_mallet-results/topics-in-texts.txt"
metadatafile = wdir + "tc30-metadata.csv"
targets = ["author","decade","genre","insp-type","insp-region"] # depending on available metadata
#tmw.aggregate_using_metadata(corpuspath,outfolder,topics_in_texts,metadatafile,targets)

### create_topicscores_heatmap
inpath = wdir + "7_aggregates/*.csv"
outfolder = wdir + "8_heatmaps/"
rows_shown = 16
dpi = 200
#tmw.create_topicscores_heatmap(inpath,outfolder,rows_shown,dpi)

