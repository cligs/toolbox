#!/usr/bin/env python3
# Filename: extract_text_mod.py

# Script that changes the orthography of some words that were written differently in the 19th Century 
# Made by JCT
# Makes use of "re"; see: http://docs.python.org/2/library/re.html

#######################
# Good to know 
#######################

# 1. By default, expects files to be in a subfolder called "input"
# 2. By default, expects there to be an empty folder called "output" for the output


#######################
# Import statements 
#######################

import re
import os
import glob
import time



#######################
# Functions 
#######################

def mod(file,outputfolder):
    if not os.path.exists(outputfolder):
        os.makedirs(outputfolder)
    with open(file,"r", encoding="utf8") as text:
        text = text.read() 
        # Change
        text_mod = text
        # Delete the accent on words like "reunióse" or "preguntóle", that now they don't have any accent any more
        text_mod = re.sub(r'<!DOCTYPE html>((?!div id=\"obra\").)*(<div id=\"obra\")', r'\2',text_mod)
        text_mod = re.sub(r'</body>((?!</body>).)*</body>\r\n</html>', r'',text_mod)
        text_mod = re.sub(r'<\/?a[^>]*>', r'',text_mod)
        text_mod = re.sub(r'<br ?/?>', r'',text_mod)
        text_mod = re.sub(r'<br clear=\"all\">', r'',text_mod)
        text_mod = re.sub(r'<img[^>]*>', r'',text_mod)
        text_mod = re.sub(r'</?div[^>]*>', r'',text_mod)
        text_mod = re.sub(r'<p style=\"text-align: justify;text-indent:30px;\">', r'<p>',text_mod)
        text_mod = re.sub(r'<p style=\"text-align: right;text-indent:30px;\">', r'<p>',text_mod)
        text_mod = re.sub(r'<p style=\"text-align: justify;\">', r'<p>',text_mod)
        text_mod = re.sub(r'<span style=\"font-style:normal;\">(((?!</span>).)*)</span>', r'\1',text_mod)
        text_mod = re.sub(r'<span lang=[^>]*>', r'<hi>',text_mod)
        text_mod = re.sub(r'</span>', r'</hi>',text_mod)
        text_mod = re.sub(r'(<(/p|/h[1-6]|/?div|/head|/l|/?lg|/?body|/?back|/?text|/?front)>)', r'\1\r\n',text_mod)
		text_mod = re.sub(r'^[ \t]*', r'')
		text_mod = re.sub(r'[ \t]*$', r'')
		text_mod = re.sub(r'[\r\n]+', r'\r\n')
		text_mod = re.sub(r'^<!DOCTYPE html PUBLIC[^\r\n]*$', r'')
		text_mod = re.sub(r'<(/?)em>', r'<\1hi>')
		text_mod = re.sub(r'(</h2>)\r\n(<h3>)', r'\1\r\n<div>\r\n\2')
		text_mod = re.sub(r'(</p>)\r\n(<h3>)', r'\1\r\n</div>\r\n<div>\r\n\2')
		text_mod = re.sub(r'(</p>)\r\n(<h2>)', r'\1\r\n</div>\r\n</div>\r\n<div>\r\n\2')
		text_mod = re.sub(r'<(/?)h[1-6]>', r'<\1head>')
		text_mod = re.sub(r'<table width=\"70%\" align=\"center\"><tr>(<td>)', r'<quote>\1')
		text_mod = re.sub(r'(<quote>((?!</table>).)*</td>)</tr></table>', r'\1</quote>')
		text_mod = re.sub(r'<(/?)td[^>]*>', r'<\1p>')
		text_mod = re.sub(r'<p></p>', r'')
		text_mod = re.sub(r'</tr><tr>', r'')
		text_mod = re.sub(r'(</quote>)</quote>', r'\1')
		text_mod = re.sub(r'<table cellpadding=\"0\" cellspacing=\"0\" align=\"center\" width=\"462\"><tr>', r'<lg>')
		text_mod = re.sub(r'(<lg>((?!</table>)[^\r\n])*)</tr></table>', r'\1</lg>')
		text_mod = re.sub(r'</?p>(</?lg>)', r'\1')
		text_mod = re.sub(r'(<lg>((?!</lg>).)*)<(/?)p[^>]*>', r'\1<\3l>')
		text_mod = re.sub(r'<p style=\"text-align:center;\">[^\r\n]*$', r'')
		text_mod = re.sub(r'<sup>.*?</sup>', r'')
		text_mod = re.sub(r'<!--.*?-->', r'')
		text_mod = re.sub(r'[\r\n]*\Z', r'</div>')

        #We get the base path
        basename = os.path.basename(file) 
		#Make create a new path that will be txt
        newfilename = basename[:-4] + ".txt" 
		#We print the name of the foldier that is creating as output
        print(outputfolder, newfilename)
		# That I don't get:
        with open(os.path.join(outputfolder, newfilename),"w") as output: 
            output.write(text_mod) 


#######################
# Main                #
#######################


def main(inputpath,outputfolder):
    numberoffiles = 0
    for file in glob.glob(inputpath):
        mod(file,outputfolder)
        numberoffiles +=1
    print("total number of files treated: " + str(numberoffiles))
    time.sleep(5)

 
main('./input/*.xml','output/')

