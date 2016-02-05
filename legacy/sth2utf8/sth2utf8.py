# sth2utf8.py
 
import os
import sys
import shutil
import glob
import codecs
 
def convert_to_utf8(filename):
    text = open(filename, 'r').read()
    decoded = codecs.decode(text,'iso-8859-15')
    encoded = codecs.encode(decoded, 'utf-8')
    encoded.write()
    f.close()

def main(inputpath):
    for filename in glob.glob(inputpath):
        convert_to_utf8(filename)

main("./sth/*.xml")
