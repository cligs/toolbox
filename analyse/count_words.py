# ./bin/env python3
# count_words.py
# author: #cf


txtpaths = ["/media/christof/data/repos/cligs/textbox/french/theatre17/txt/*.txt",
            "/media/christof/data/repos/cligs/textbox/french/roman19/txt/*.txt",
            "/media/christof/data/repos/cligs/textbox/french/nouvelles19/txt/*.txt",
            "/media/christof/data/repos/cligs/textbox/spanish/novela-espanola/txt/*.txt",
            "/media/christof/data/repos/cligs/textbox/spanish/novela-hispanoamericana/txt/*.txt",
            "/media/christof/data/repos/cligs/textbox/portuguese/romancesportugueses/txt/*.txt"]

import os
import re
import glob

def get_text(txtfile):
    with open(txtfile, "r") as infile:
        text = infile.read()
        return text


def get_wordcount(text):
    text = re.split("\W", text)
    text = [word for word in text if word]
    #print(text[0:50])
    count = len(text)
    return count


def count_words(txtpath):
    for txtpath in txtpaths: 
        total = 0
        counter = 0
        for txtfile in glob.glob(txtpath):
            #print(os.path.basename(txtfile))
            counter +=1
            text = get_text(txtfile)
            count = get_wordcount(text)
            #print(count)
            total = total + count
        print(txtpath, "\n", counter, "texts;", total, "words.")

count_words(txtpaths)
