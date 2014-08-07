#!/bin/bash

# This file should be in the main TreeTagger directory
# It then allows to run Tree Tagger on a set of files in the sub-folder "input".

FILES=/home/christof/repos/clgs/dev-texts/romanpolicier/derived/1_pretoken/*
for file in $FILES
    do cmd/tree-tagger-french $file > $file.trt
done

