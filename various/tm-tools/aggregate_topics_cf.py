# aggregate_topics.py
# Function to aggregate topic weights from individual chunks back to entire texts or authors. 
# This function is based on code by Allen Riddell; see https://de.dariah.eu/tatom/topic_model_mallet.html.

#########################
# Import statements
#########################

import numpy as np
import itertools
import operator
import os
import glob

#########################
# Functions
#########################


def get_authors(textfilespath):                                         # Assumes the filename syntax is "author_something.txt"
    authorlist = []
    for filename in glob.glob(textfilespath): 
        author = os.path.basename(filename).split('_')[0]
        authorlist.append(author)
    authorset = sorted(set(authorlist))
    #print(authorset)
    authorarray = np.array(authorlist)
    #print(authorarray)


def get_titles(textfilespath):                                          # Assumes the filename syntax is "something_titlesomething.txt"
    titlelist = []
    for filename in glob.glob(textfilespath): 
        title = os.path.basename(filename).split('_')[1]
        title = title[:-9]                                              # Removes the counter and extension from the title. Adjust as necessary.
        titlelist.append(title)
    titleset = sorted(set(titlelist))
    #print(titleset)
    titlearray = np.array(titlelist)
    #print(titlearray)






#########################
# Main
#########################

def main(textfilespath): 
    get_authors(textfilespath)
    get_titles(textfilespath)

main("./cleaned/*.txt")
