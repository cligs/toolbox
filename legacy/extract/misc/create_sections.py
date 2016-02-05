#!/usr/bin/env python3
# Filename: mg_sections.py

"""
# Script for turning plain text files into sections, respecting paragraph boundaries.
"""

import re
import os
import glob
import matplotlib.pyplot as plt

def segmenter(inpath, target_len):
    for file in glob.glob(inpath):
        with open(file, "r") as infile:
            filename = os.path.basename(file)[:-4]
            idno = filename[:5]
            print(idno)
            text = infile.read()

            paras = text.split("\n")
            print(len(paras))
            #lens = [len(para) for para in paras]
            #plt.hist(lens)
            #plt.show()

            sections = ""
            actual_len = 0
            counter = 0
            section = "ID-0000 "
            for i in range(len(paras)-1):
                if actual_len < target_len:
                    section = section + paras[i] + " "
                    actual_len = len(section)
                else:
                    sections = sections + "\n\n" + section
                    counter += 1
                    section = "ID-{:04d} ".format(counter)
                    actual_len = 0

        outfile = "./sec/" + filename + ".txt"
        with open(outfile,"w") as output:
            output.write(sections)

def main(inpath, target_len):
    segmenter(inpath, target_len)

main("./txt/*.txt", 2000)
