# -*- coding: utf-8 -*-
"""
@author: Ulrike Henny
@filename: spellchecking.py

Submodule for checking the orthography of a text collection. The expected input are plain text files.

To install further dictionaries: sudo apt-get install myspell-es (etc.)
See http://pythonhosted.org/pyenchant/ for more information about the spellchecking library used
"""

import enchant
from enchant import checker
import collections
import pandas as pd
import os
import glob


def check_collection(inpath, outpath, lang, nefile):
	"""
	Checks the orthography of the text in a collection. The expected input are plain text files.
	
	Arguments:
	inpath (string): path to the input files, including file name pattern
	outpath (string): path to the output file, including the output file's name
	lang (string): which dictionary to use, e.g. "es", "fr", "de"
	"""

	try:
		enchant.dict_exists(lang)
	except:
		print("The dictionary " + lang + "doesn't exist. Please choose another dictionary.")
		
	chk = checker.SpellChecker(lang)
	
	all_words = []
	all_num = []
	all_idnos = []

	print("...checking...")
	for file in glob.glob(inpath):
		idno = os.path.basename(file)[-10:-4]
		all_idnos.append(idno)
		
		err_words = []

		with open(file, "r", encoding="UTF-8") as fin:
			intext = fin.read().lower()
			chk.set_text(intext)

		with open(nefile, "r", encoding="UTF-8") as nef:
			nes = nef.read().lower()

		for err in chk:
			if err.word not in nes: 
				err_words.append(err.word)
			all_words.append(err_words)

		err_num = collections.Counter(err_words)
		all_num.append(err_num)
		
		print("..." + str(len(err_num)) + " different errors found in " + idno)
		
	df = pd.DataFrame(all_num,index=all_idnos).T
	df = df.fillna(0)
	df["sum"] = df.sum(axis=1)
	df = df.sort("sum", ascending=False)

	df.to_csv(outpath)
	print("done")



def main(inpath, outpath, lang, nefile):
    check_collection(inpath, outpath, lang, nefile)
    
if __name__ == "__main__":
    import sys
    check_collection(int(sys.argv[1]))


