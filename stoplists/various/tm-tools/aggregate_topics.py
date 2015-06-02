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


def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def topic_triples(topicsfilepath): 
    doctopic_triples = []
    mallet_docnames = []
    with open(topicsfilepath) as f:
        f.readline()                                                    # read one line in order to skip the header
        for line in f:
            docnum, docname, *values = line.rstrip().split('\t')
            mallet_docnames.append(docname)
            for topic, share in grouper(2, values):
                triple = (docname, int(topic), float(share))
                doctopic_triples.append(triple)

    doctopic_triples = sorted(doctopic_triples, key=operator.itemgetter(0,1))
    mallet_docnames = sorted(mallet_docnames)                               # sort the document names rather than relying on MALLET's ordering
    num_docs = len(mallet_docnames)                                         # collect into a document-term matrix
    num_topics = len(doctopic_triples) // len(mallet_docnames)
    #print(num_docs) #ok
    #print(num_topics) #ok
    #print(mallet_docnames[0:3]) #ok

    doctopic = np.zeros((num_docs, num_topics))                             # the following works because we know that the triples are in sequential order
    for triple in doctopic_triples:
        docname, topic, share = triple
        row_num = mallet_docnames.index(docname)
        doctopic[row_num, topic] = share

"""
    novel_names = []                                                        # Creates an empty list of filenames on the novel-level.
    for fn in filenames:
        basename = os.path.basename(fn)
        name, ext = os.path.splitext(basename)
        name = name.rstrip('0123456789-')                                   # Removes the index from the chunk-files 
        novel_names.append(name)                                            # Adds each novel-level file name to the list of filenames.
    #print(len(novel_names)) #ok
    #print(novel_names[0:3]) #ok
"""


titlearray = np.asarray(titlelist)                                   # turn this into an array so we can use NumPy functions
num_groups = len(set(titlelist))                                      # use method described in preprocessing section: "set" removes duplicates

doctopic_grouped = np.zeros((num_groups, num_topics))
for i, name in enumerate(sorted(set(titlelist))):
    doctopic_grouped[i, :] = np.mean(doctopic[titlelist == name, :], axis=0)
doctopic = doctopic_grouped
print(len(doctopic)) #ok

"""
    with open("doctopic.csv", "w") as table: 
        table.write(str(doctopic))
"""




#########################
# Main
#########################

def main(textfilespath,topicsfilepath): 
    get_authors(textfilespath)
    get_titles(textfilespath)
    topic_triples(topicsfilepath)
    

main("./cleaned/*.txt","/home/christof/Programs/mallet/results/polar100_topics-in-texts.txt")


"""
CORPUS_PATH = os.path.join('..','..','..','clgs-rep','polar','cleaned')  # path to where files are located
filenames = sorted([os.path.join(CORPUS_PATH, fn) for fn in os.listdir(CORPUS_PATH)])
#print(len(filenames)) #ok
#print(filenames[:2]) #ok
"""

  

