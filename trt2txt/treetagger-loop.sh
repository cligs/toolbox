#!/bin/bash

# This file should be in the main TreeTagger directory
# It then allows to run Tree Tagger on a set of files in the sub-folder "input".

FILES=/home/christof/Programs/tt2/input/*
for file in $FILES
    do cmd/tree-tagger-french-utf8 $file > $file.trt
done

