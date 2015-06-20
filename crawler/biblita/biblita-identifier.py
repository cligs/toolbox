#!/usr/bin/env python3
# Filename: biblita-identifier.py

import re

with open("1.html", "r") as infile: 
	alldata = infile.read()
	#print(alldata)
	
	data = re.findall("bibit[\d]{5,7}",alldata)
	print(len(data))
	print(data)
	
