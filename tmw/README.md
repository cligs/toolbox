TMW - Topic Modeling Workflow
=================================

This Python module provides a full topic modeling workflow, from textual input all the way to topic distribution heatmaps. Makes use of TreeTagger and Mallet. This module is experimental in nature and quality. It has not been written by a programmer. It has not been optimized for performance in any way. It is not well-documented. It is not guaranteed to run or be useful. 

## Version
* 0.1.0

## Requirements
* UNIX-based operating system (tested on Ubuntu 14.04)
* Python 3 (tested with Python 3.4)
* TreeTagger, including parameter files
* Mallet

## Input data
* Textual data: one XML or TXT file per document, filename = document identifier
* Metadata: CSV-file with document-level metadata, including document identifier
* Stoplist: a plain text file with stopwords for the desired language

## Functions
* tei4reader
* segmenter
* sort_into_bins
* pretokenize
* call_treetagger
* make_lemmatext
* call_mallet_import
* call_mallet_model
* generate_wordlescores
* aggregate_using_metadata
* create_topicscores_heatmap

## Questions, remarks?
For questions or remarks about this module, please use the issue tracker here on Github or drop me a line at c.schoech@gmail.com. 
