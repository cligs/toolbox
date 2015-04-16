#!/usr/bin/env python3
# Filename: aggregate_topics.py


def aggregate_using_bins_and_metadata(corpuspath,outfolder,topics_in_texts,metadatafile,bindatafile,target):
    """Function to aggregate topic scores based on metadata about segments."""
    print("\nLaunched aggregate_using_metadata.")

    import numpy as np
    import itertools
    import operator
    import os
    import pandas as pd

    ## USER: Set path to where the individual chunks are located.
    CORPUS_PATH = os.path.join(corpuspath)
    filenames = sorted([os.path.join(CORPUS_PATH, fn) for fn in os.listdir(CORPUS_PATH)])
    print("Number of files to treat: ", len(filenames)) #ok
    print("First three filenames: ", filenames[:3]) #ok

    def grouper(n, iterable, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        args = [iter(iterable)] * n
        return itertools.zip_longest(*args, fillvalue=fillvalue)

    doctopic_triples = []
    mallet_docnames = []
    ### USER: Set path to results from Mallet.
    with open(topics_in_texts) as f:
        f.readline()
        for line in f:
            docnum, docname, *values = line.rstrip().split('\t')
            mallet_docnames.append(docname)
            for topic, share in grouper(2, values):
                triple = (docname, int(topic), float(share))
                doctopic_triples.append(triple)

    doctopic_triples = sorted(doctopic_triples, key=operator.itemgetter(0,1))
    mallet_docnames = sorted(mallet_docnames)
    num_docs = len(mallet_docnames)
    num_topics = len(doctopic_triples) // len(mallet_docnames)
    print("Number of documents: ", num_docs)
    print("Number of topics: ", num_topics)

    doctopic = np.zeros((num_docs, num_topics))
    for triple in doctopic_triples:
        docname, topic, share = triple
        row_num = mallet_docnames.index(docname)
        doctopic[row_num, topic] = share

    #### Define aggregation criterion #
    metadata = pd.DataFrame.from_csv(metadatafile, header=0, sep=",")
    bindata = pd.DataFrame.from_csv(bindatafile, header=0, sep=",")
    print(bindata.head())
    label_names = []
    for item in filenames:
        basename = os.path.basename(item)
        filename, ext = os.path.splitext(basename)
        textidno = filename[1:7]
        metadata_target = target
        genre_label = metadata.loc[textidno,metadata_target]
        binidno = filename[1:12]
        bin_target = "binids"
        bin_label = bindata.loc[binidno,bin_target]
        print("textidno, binidno, genre_label, bin_label: ", textidno, binidno, genre_label, bin_label)
        label_name = str(genre_label) + "$" + str(bin_label)
        outputfilename = "topics_by_BINS-and "+ target.upper() + ".csv"
        label_names.append(label_name)
    label_names_set = set(label_names)
    label_names = np.asarray(label_names)
    num_groups_labels = len(set(label_names))

    print("Number of different labels:", len(label_names_set))
    print("Number of entries: ", len(label_names))
    print("Some label names: ", label_names[10:61])
    print("Number of different labels: ", len(set(label_names)))


    ### Group topic scores according to label
    doctopic_grouped = np.zeros((num_groups_labels, num_topics))
    for i, name in enumerate(sorted(set(label_names))):
        doctopic_grouped[i, :] = np.mean(doctopic[label_names == name, :], axis=0)
        doctopic = doctopic_grouped
        #print(len(doctopic)) #ok
        #np.savetxt("doctopic.csv", doctopic, delimiter=",")

    rownames = sorted(set(label_names))
    colnames = ["tp" + "{:03d}".format(i) for i in range(doctopic.shape[1])]
    df = pd.DataFrame(doctopic, index=rownames, columns=colnames)
    df.to_csv(outputfilename, sep='\t', encoding='utf-8')

def main(corpuspath,outfolder,topics_in_texts,metadatafile,bindatafile,target):
    aggregate_using_bins_and_metadata(corpuspath,outfolder,topics_in_texts,metadatafile,bindatafile,target)

main("5_lemmata", "/home/christof/Repos/cligs/toolbox/tmw/demo/7_aggregates/"  , "/home/christof/Repos/cligs/toolbox/tmw/demo/6_mallet/topics-in-texts.txt", "tc30-metadata.csv", "scenes-and-bins.csv", "genre")