#!/usr/bin/env python3
# Filename: perform_lda.py

"""
# Script to test Allen Riddell's python implementation of LDA.
# See: https://github.com/ariddell/lda and http://pythonhosted.org/lda/.
# Takes as input folder with plain text files, one file per document.
"""

import os
import lda
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

def perform_lda(datafolder, stopwordfile, ntopics, ntopwords, niterations):
    """Script to test Allen Riddell's python implementation of LDA."""

    ### Get list of documents (each document in one plain text file)
    files = os.listdir(datafolder)
    filenames = []
    for file in files:
        filename = os.path.join(datafolder, file)
        filenames.append(filename)

    ### Create sparse term-document matrix from documents
    with open(stopwordfile, "r") as stopwords:
        stopwords = stopwords.read().split()
    vectorizer = CountVectorizer(input='filename', stop_words=stopwords)
    dtm = vectorizer.fit_transform(filenames)  # a sparse matrix
    vocab = vectorizer.get_feature_names()  # a list
    titles = os.listdir(datafolder)

    ### Perform the actual modeling
    model = lda.LDA(n_topics=ntopics, n_iter=niterations, random_state=1)
    model.fit(dtm)  # model.fit_transform(X) is also available
    topic_word = model.topic_word_  # model.components_ also works

    ### Display the top topic words
    n_top_words = ntopwords
    topics_with_words = ""
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        display_topic_words = 'Topic {}: {}'.format(i, ' '.join(topic_words))
        #print(display_topic_words)
        topics_with_words = topics_with_words + display_topic_words + "\n"
    with open("topics_with_words.txt", "w") as outfile:
        outfile.write(str(topics_with_words))

    ### Display selection of documents with their filename/title and top topic(s)
    doc_topic = model.doc_topic_
    docs_with_top_topics = ""
    for i in range(10):
        display_top_topic = "{}: top topic {}".format(titles[i], doc_topic[i].argmax()) # top topic
        display_top_topic = "{}: top topics {}".format(titles[i][:-4], doc_topic[i].argsort()[-3:][::-1]) # 3 top topics
        #print(display_top_topic)
        docs_with_top_topics = docs_with_top_topics + display_top_topic + "\n"
    with open("docs_with_topics.txt", "w") as outfile:
        outfile.write(str(docs_with_top_topics))

    ### Display the convergence graph
    plt.plot(model.loglikelihoods_[5:]) #skip first few entries
    #plt.show()
    plt.savefig("convergence.png")

def main(datafolder, stopwordfile, ntopics, ntopwords, niterations):
    perform_lda(datafolder, stopwordfile, ntopics, ntopwords, niterations)

main("./comedias/", "stopwords_ES.txt", 10, 10, 100)
