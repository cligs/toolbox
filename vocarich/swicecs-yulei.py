#!/usr/bin/env python3
# Filename: swicecs-yulei.py

"""
# Skript to measure vocabulary richness, more precisely Yule's I.
# Yule's I: the inverse of Yule's K measure; higher number is higher diversity and richer vocabulary.
# Adapted from: http://swizec.com/blog/measuring-vocabulary-richness-with-python/swizec/2528
"""

from itertools import groupby
import glob
import os
import re

def yule(file):
    """Calculate Yule's I measure."""
    with open(file,"r") as f:
        text = f.read()
    filename = os.path.basename(file)[:-4]
    d = {}
    for w in filter(lambda w: len(w) > 2, [w.strip("0123456789!:,.?(){}[]-") for w in re.split("\W+",text)]):
        w = w.lower()
        try:
            d[w] += 1
        except KeyError:
            d[w] = 1


    M1 = float(len(d))
    M2 = sum([len(list(g))*(freq**2) for freq,g in groupby(sorted(d.values()))])
    yulei = (M1*M1)/(M2-M1)

    #print(d)
    print("Yule's I for", filename  , "is: ", yulei)
    print("M1 (number of different word types): ", M1)
    print("M2 (sum of the products of each observed frequency to the power of two and the number of word types observed with that frequency): ", M2)

    try:
        return (M1*M1)/(M2-M1)
    except ZeroDivisionError:
        return 0

def main(inputpath):
    for file in glob.glob(inputpath):
        yule(file)

main("./data/*.txt")
