# split-text.py
# Script to split all files in a folder into chunks of a certain length in words and write them to another folder.
# This script has been written by Allen Riddell, see https://de.dariah.eu/tatom/preprocessing.html#chunking. It is only slightly adapted here.
# The script assumes texts are encoded in UTF-8 but can be adapted for other character encodings. 

##############################
# Overview
##############################

# Does the following to all files in the input_dir folder
# 1. Open the file
# 2. Create chunks of text of the specified size, including a final chunk of rest size
# 3. Build filenames for each chunk
# 4. Save each chunk to folder with the generated filename



##############################
# Import statements
##############################

import os
import string
import logging
import glob


##############################
# split_text function
##############################

def split_text(num_words,filename,output_dir):
    """Split a long text file into chunks of approximately `num_words` words and write each chunk to a new file."""
    with open(filename, 'r', encoding="utf8") as input:                 # USER: Set encoding scheme here.
        words = input.read().split(' ')
    chunks = []
    current_chunk_words = []
    current_chunk_word_count = 0
    for word in words:
        current_chunk_words.append(word)
        if word not in string.whitespace:
            current_chunk_word_count += 1
        if current_chunk_word_count == num_words:
            chunk = ' '.join(current_chunk_words)
            chunks.append(chunk)
            current_chunk_words = []
            current_chunk_word_count = 0
    final_chunk = ' '.join(current_chunk_words)
    chunks.append(final_chunk)
    fn = os.path.basename(filename)
    fn_base, fn_ext = os.path.splitext(fn)
    for i, chunk in enumerate(chunks):
        chunk_filename = "{}-{:04d}{}".format(fn_base, i, fn_ext)
        with open(os.path.join(output_dir, chunk_filename), 'w') as f:
            f.write(chunk)
    print(fn + " => " + str(len(chunks)) + " chunks")


##########################
# Main
##########################

def main(num_words,input_dir,output_dir):
    for filename in glob.glob(input_dir): 
        split_text(num_words,filename,output_dir)

main(300,"./tc-lem1/*.txt","./tc-lem2/")                                   # USER: Set arguments here

