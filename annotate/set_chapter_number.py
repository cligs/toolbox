# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:35:08 2016

@author: jose
"""
import pandas as pd
import re
import glob
from collections import Counter
from lxml import etree
import os

"""
This script helps the editor to set the numbers of the chapter as attribute in the div

To use all of them just use:
df = numbering("/home/jose/cligs/ne/master/", "ne0230.xml", mode="from_head")
"""

def numbering(wdir, txtFolder, mode="from_head"):

    """
    It sets the number as int in the @n attribute when it finds a div with an empty @n attribute and then a head with number as roman number
    """

    doc = wdir+txtFolder
    with open(doc, "r", errors="replace", encoding="utf-8") as fin:
        content = fin.read()
        
        if mode == "from_head":
            roman_numbers = dict( I = 1, II = 2, III = 3, IV = 4, V = 5, VI = 6, VII = 7, VIII = 8, IX = 9, X = 10, XI = 11, XII = 12, XIII = 13, XIV = 14, XV = 15, XVI = 16, XVII = 17, XVIII = 18, XIX = 19, XX = 20, XXI = 21, XXII = 22, XXIII = 23, XXIV = 24, XXV = 25, XXVI = 26, XXVII = 27, XXVIII = 28, XXIX = 29, XXX = 30, XXXI = 31, XXXII = 32, XXXIII = 33, XXXIV = 34, XXXV = 35, XXXVI = 36, XXXVII = 37, XXXVIII = 38, XXXIX = 39, XL = 40, XLI = 41, XLII = 42, XLIII = 43, XLIV = 44, XLV = 45, XLVI = 46, XLVII = 47, XLVIII = 48, XLIX = 49, L = 50, LI = 51, LII = 52, LIII = 53, LIV = 54, LV = 55, LVI = 56, LVII = 57, LVIII = 58, LIX = 59, LX = 60, LXI = 61, LXII = 62, LXIII = 63, LXIV = 64, LXV = 65, LXVI = 66, LXVII = 67, LXVIII = 68, LXIX = 69, LXX = 70, LXXI = 71, LXXII = 72, LXXIII = 73, LXXIV = 74, LXXV = 75, LXXVI = 76, LXXVII = 77, LXXVIII = 78, LXXIX = 79, LXXX = 80, LXXXI = 81, LXXXII = 82, LXXXIII = 83, LXXXIV = 84, LXXXV = 85, LXXXVI = 86, LXXXVII = 87, LXXXVIII = 88, LXXXIX = 89, XC = 90, XCI = 91, XCII = 92, XCIII = 93, XCIV = 94, XCV = 95, XCVI = 96, XCVII = 97, XCVIII = 98, XCIX = 99, C = 100,)
             
            content = re.sub(r'<div\s+type="chapter">(\s+<head>(?:Capítulo)?\s*([IVXLC]+)[^IVXLC])', r'<div type="chapter" n="\2">\1', content)
    
            for roman_number,value in roman_numbers.items():
                content = re.sub(r'n="'+re.escape(roman_number)+'"', r'n="'+re.escape(str(value))+'"', content)

        elif mode == "consecutive":
            chapters = re.findall(r'<div\s+type="chapter">(\s+.*?<p>.+?</p>)', content, flags=re.DOTALL)
            i = 1
            for chapter in chapters:
                print(i, chapter)
                content = re.sub(r'<div\s+type="chapter">('+re.escape(chapter)+r')', r'<div type="chapter" n="'+re.escape(str(i))+r'">\1', content, flags=re.DOTALL)
                i += 1

            
        with open (os.path.join("output", wdir+txtFolder), "w", encoding="utf-8") as fout:
                fout.write(content)
    fin.close()
    return content

    
