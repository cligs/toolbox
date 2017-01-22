#!/usr/bin/env python3
# Filename: md2tei.py


"""
# Function to transform simple Markdown files into simple, clean TEI files.
"""


import re
import glob
import os


filepath = "./md/*.txt"
teiheader = "teiHeader.xml"


# ==============================
# Functions
# ==============================


def read_md(file):
    with open(file,"r") as sourcefile:
        md = sourcefile.read()
        filename, ext = os.path.basename(file).split(".")
        print("Now working on: ", filename)
        return md, filename


def read_header(teiheader):
    with open(teiheader,"r") as infile:
        header = infile.read()
        return header


def md2tei(md, header):

    # Define the parts
    header = header
    front = "<front>\n<div>\n<p></p>\n</div>\n</front>"
    body = "\n<body>\n<div>\n<p>" + md + "</p>\n</div>\n</body>"
    back = "\n<back>\n<div><p></p>\n</div>\n</back>"
    finale = "\n</text></TEI>"

    # Clean the body
    body = re.sub("\\\\!", "!", body)
    body = re.sub("\\\\\(", "(", body)
    body = re.sub("\\\\\)", ")", body)
    body = re.sub("<p>---", "<p>--", body)
    body = re.sub("&", "&amp;", body)

    # Add inline italics
    body = re.sub("\*(.*?)\*", "<seg rend=\"italic\">\\1</seg>", body)

    # Add structure
    body = re.sub("\n\n", "</p>\n<p>", body)
    body = re.sub("<p>\#.*? (.*?)</p>", "</div>\n<div>\n<head>\\1</head>", body)
    body = re.sub("</p>\n<p></p>\n<p></p>\n</div>", "</p>\n</div>", body)

    # Turn spaces into milestones
    body = re.sub("</p>\n<p></p>\n<p>", "</p>\n<milestone unit=\"line\"/>\n<p>", body)
    body = re.sub("</p>\n<p> </p>\n<p>", "</p>\n<milestone unit=\"line\"/>\n<p>", body)
    body = re.sub("<milestone unit=\"line\"/>\n<p>.?</p>", "<milestone unit=\"line\"/>", body)

    # Clean up a bit
    body = re.sub("</head>\n</div>\n<div>\n<head></head>\n<p>", "</head>\n<p>", body)

    # Put the parts together
    tei = header + front + body + back + finale
    return tei


def save_tei(tei, filename):
    filename = "./md/" + filename + ".xml"
    with open(filename, "w") as outputfile:
        outputfile.write(tei)


def main(filepath, teiheader):
    for file in glob.glob(filepath):
        md, filename = read_md(file)
        header = read_header(teiheader)
        tei = md2tei(md, header)
        save_tei(tei, filename)

main(filepath, teiheader)
