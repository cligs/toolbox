# -*- coding: utf-8 -*-
"""

2018-09-17
@author: ulrike
"""

import os
import glob




def generate_trigrams(indir, outdir):
	"""
	Takes input text files with one item per line and produces output text files with one trigram per line.
	
	indir: input directory with files in .txt format containing one item per line (e.g. tokens, lemmata)
	outdir: output directory
	"""
	
	if not os.path.exists(os.path.join(outdir)):
		os.makedirs(os.path.join(outdir))
        
	for doc in glob.glob(os.path.join(indir,"*.txt")):
		
		filename = os.path.split(doc)[1]
		print("doing " + filename + "...")
		
		# clear old file
		with open(os.path.join(outdir, filename), "w", encoding="utf-8") as outtext:
			outtext.write("")
		
		counter = 0
		
		with open(doc, "r", encoding="utf-8") as intext:
			
			lines = intext.readlines()
			textlength = len(lines)
			
			
			while counter < (textlength - 3):
			
				head = lines[counter : counter + 3]
				head = [x[:-1] for x in head]
				tri = " ".join(head)
				
				with open(os.path.join(outdir, filename), "a", encoding="utf-8") as outtext:
					outtext.write(tri + "\n")
	
				counter += 1
				
	print("all done!")	
			
		
		
		
generate_trigrams("/home/ulrike/Dokumente/GS/Veranstaltungen/2018_Japan/Spanish_Am/Lemmatized/", "/home/ulrike/Dokumente/GS/Veranstaltungen/2018_Japan/Spanish_Am/Lemmatized_Tri/")
