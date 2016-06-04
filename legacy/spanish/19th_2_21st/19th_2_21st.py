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
        text_mod = re.sub(r'([A-ZÑÉÍÓÍÁÜ]{2,})(É)([MLST][EOA]S?[^A-ZÑÉÍÓÍÁÜ])', r'\1E\3',text_mod)
        text_mod = re.sub(r'([A-ZÑÉÍÓÍÁÜ]{2,})(Ó)([MLST][EOA]S?[^A-ZÑÉÍÓÍÁÜ])', r'\1O\3',text_mod)
        text_mod = re.sub(r'([A-ZÑÉÍÓÍÁÜ]{2,})(Á)([MLST][EOA]S?[^A-ZÑÉÍÓÍÁÜ])', r'\1A\3',text_mod)
        text_mod = re.sub(r'([A-ZÑÉÍÓÍÁÜ]{2,})(Í)([MLST][EOA]S?[^A-ZÑÉÍÓÍÁÜ])', r'\1I\3',text_mod)

        text_mod = re.sub(r'([A-zñéíóúáü]{2,})(é)([mlst][eoa]s?[^a-zñéíóúáü])', r'\1e\3',text_mod)
        text_mod = re.sub(r'([A-zñéíóúáü]{2,})(ó)([mlst][eoa]s?[^a-zñéíóúáü])', r'\1o\3',text_mod)
        text_mod = re.sub(r'([A-zñéíóúáü]{2,})(á)([mlst][eoa]s?[^a-zñéíóúáü])', r'\1a\3',text_mod)
        text_mod = re.sub(r'([A-zñéíóúáü]{2,})(í)([mlst][eoa]s?[^a-zñéíóúáü])', r'\1i\3',text_mod)
		
        # Change the orthographic of monosyllabic words that has changed its orthographic systematic in the last century like "fué">"fue", "oir">"oír", "dió">"dio", "á">"a" "ó">"o", "vió">"vio", "é">"e", "hé" >"he", "vá">"va", "tí">"ti", "vé">"ve", "dá">"da"
        text_mod = re.sub(r'([^A-ZÑÉÍÓÍÁÜ]FU)É([^A-ZÑÉÍÓÍÁÜ])', r'\1E\2',text_mod)
        text_mod = re.sub(r'([^A-zñéíóúáü][Ff]u)é([^A-zñéíóúáü])', r'\1e\2',text_mod)
        text_mod = re.sub(r'([^A-ZÑÉÍÓÍÁÜ]FU)Í([^A-ZÑÉÍÓÍÁÜ])', r'\1I\2',text_mod)
        text_mod = re.sub(r'([^A-zñéíóúáü][Ff]u)í([^A-zñéíóúáü])', r'\1i\2',text_mod)
        
        text_mod = re.sub(r'([^A-ZÑÉÍÓÍÁÜ]O)I(RL?[AOE]?S?[^A-ZÑÉÍÓÍÁÜ])', r'\1Í\2',text_mod)
        text_mod = re.sub(r'([^A-ZÑÉÍÓÍÁÜ][Oo])i(rl?[aoe]?s?[^A-ZÑÉÍÓÍÁÜ])', r'\1í\2',text_mod)

        text_mod = re.sub(r'([^A-ZÑÉÍÓÍÁÜ]SONRE)I(R[^A-ZÑÉÍÓÍÁÜ])', r'\1Í\2',text_mod)
        text_mod = re.sub(r'([^A-zñéíóúáü][Ss]onre)i(r[^A-zñéíóúáü])', r'\1í\2',text_mod)

        text_mod = re.sub(r'([^A-ZÑÉÍÓÍÁÜ]RE)I(R[^A-ZÑÉÍÓÍÁÜ])', r'\1Í\2',text_mod)
        text_mod = re.sub(r'([^A-zñéíóúáü][Rr]e)i(r[^A-zñéíóúáü])', r'\1í\2',text_mod)

        text_mod = re.sub(r'([^A-ZÑÉÍÓÍÁÜ]DI)Ó([^A-ZÑÉÍÓÍÁÜ])', r'\1o\2',text_mod)
        text_mod = re.sub(r'([^A-zñéíóúáü][Dd]i)ó([^A-zñéíóúáü])', r'\1o\2',text_mod)

        text_mod = re.sub(r'([^A-zÑÉÍÓÍÁÜ])Á([^A-ZÑÉÍÓÍÁÜ])', r'\1A\2',text_mod)
        text_mod = re.sub(r'([^A-zñéíóúáü])á([^A-zñéíóúáü])', r'\1a\2',text_mod)

        text_mod = re.sub(r'([^A-ZÑÉÍÓÍÁÜ])Ó([^A-ZÑÉÍÓÍÁÜ])', r'\1O\2',text_mod)
        text_mod = re.sub(r'([^A-zñéíóúáü])ó([^A-zñéíóúáü])', r'\1o\2',text_mod)

        text_mod = re.sub(r'([^A-ZÑÉÍÓÍÁÜ])É([^A-ZÑÉÍÓÍÁÜ])', r'\1E\2',text_mod)
        text_mod = re.sub(r'([^A-zñéíóúáü])é([^A-zñéíóúáü])', r'\1e\2',text_mod)

        text_mod = re.sub(r'([^A-ZÑÉÍÓÍÁÜ]VI)Ó([^A-ZÑÉÍÓÍÁÜ])', r'\1O\2',text_mod)
        text_mod = re.sub(r'([^A-zñéíóúáü][Vv]i)ó([^A-zñéíóúáü])', r'\1o\2',text_mod)

        text_mod = re.sub(r'([^A-ZÑÉÍÓÍÁÜ]H)É([^A-ZÑÉÍÓÍÁÜ])', r'\1E\2',text_mod)
        text_mod = re.sub(r'([^A-zñéíóúáü][Hh])é([^A-zñéíóúáü])', r'\1e\2',text_mod)

        text_mod = re.sub(r'([^A-ZÑÉÍÓÍÁÜ]V)Á([^A-ZÑÉÍÓÍÁÜ])', r'\1A\2',text_mod)
        text_mod = re.sub(r'([^A-zñéíóúáü][Vv])á([^A-zñéíóúáü])', r'\1a\2',text_mod)

        text_mod = re.sub(r'([^A-ZÑÉÍÓÍÁÜ]T)Í([^A-ZÑÉÍÓÍÁÜ])', r'\1I\2',text_mod)
        text_mod = re.sub(r'([^A-zñéíóúáü][Tt])í([^A-zñéíóúáü])', r'\1i\2',text_mod)

        text_mod = re.sub(r'([^A-ZÑÉÍÓÍÁÜ]V)É([^A-ZÑÉÍÓÍÁÜ])', r'\1E\2',text_mod)
        text_mod = re.sub(r'([^A-zñéíóúáü][Vv])é([^A-zñéíóúáü])', r'\1e\2',text_mod)

        text_mod = re.sub(r'([^A-ZÑÉÍÓÍÁÜ]D)Á([^A-ZÑÉÍÓÍÁÜ])', r'\1A\2',text_mod)
        text_mod = re.sub(r'([^A-zñéíóúáü][Dd])á([^A-zñéíóúáü])', r'\1a\2',text_mod)
		
        # Steps to divide the text into nice <div>s using the <h1>-<h6>
        #text_mod = re.sub(r'(<text>.*?)<h3>(.+?)</h3>(.+?)(<h3>.+?</h3>)', r'\1<div><head>\2</head>\3</div>\4',text_mod, flags=re.DOTALL)
        #text_mod = re.sub(r'<h3>(.*?)</h3>(.+?)(</body>)', r'<div><head>\1</head>\2</div>\3',text_mod, flags=re.DOTALL)
		
        # Steps to divide the text into nice <div>s using the <h1>-<h6>
        #text_mod = re.sub(r'(<text>.*?)<h2>(.+?)</h2>(.+?)(<h2>.+?</h2>)', r'\1<div><head>\2</head>\3</div>\4',text_mod, flags=re.DOTALL)
        #text_mod = re.sub(r'<h2>(.*?)</h2>(.+?)(</body>)', r'<div><head>\1</head>\2</div>\3',text_mod, flags=re.DOTALL)
        # Steps to divide the text into nice <div>s using the <h1>-<h6>
        #text_mod = re.sub(r'(<text>.*?)<h1>(.+?)</h1>(.+?)(<h1>.+?</h1>)', r'\1<div><head>\2</head>\3</div>\4',text_mod, flags=re.DOTALL)
        #text_mod = re.sub(r'<h1>(.*?)</h1>(.+?)(</body>)', r'<div><head>\1</head>\2</div>\3',text_mod, flags=re.DOTALL)
		
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

