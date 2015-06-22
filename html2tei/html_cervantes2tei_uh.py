# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/ulrike/.spyder2/.temp.py
"""

import re
import os
import html.parser
from bs4 import BeautifulSoup

with open(os.path.join("input","in.html"), "r") as fin:
    content = fin.read()
    
    # HTML-Entities decodieren
    h = html.parser.HTMLParser()
    content = h.unescape(content)

    # Geschützte Leerzeichen löschen
    content = re.sub('\u00A0', " ", content)
    
    # HTML-Gerüst entfernen
    content = re.sub('<!DOCTYPE.*</head>', "", content, flags=re.DOTALL)
    content = re.sub('</body>.*</html>', "", content, flags=re.DOTALL)
    #content = re.sub('<body>.*?<br>', "", content, flags=re.DOTALL)
    #content = re.sub('<br><br><a name.*?<br /><br /></div>', "", content, flags=re.DOTALL)
    
    
    # überflüssige Elemente/Attribute entfernen
    content = re.sub('<a name="\d+"></a>', "", content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('<a[\s>].*?</a>', "", content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('<p style.*?>', "<p>", content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('<br\s?/?>', "", content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('<br[^>]+clear="all">', "", content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('<img.*?>', "", content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('<sup>.*?</sup>', "", content, flags=re.DOTALL|re.IGNORECASE)
    #content = re.sub('<sup>.*?</sup>.*?<a.*?</a>', "", content, flags=re.DOTALL)
    # Seitenumbrueche entfernen
    content = re.sub('<span[^<]+—[\dA-Z]+→[^<>]+</span>', '', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('<font[^<]+-\[?[\dA-Z]+\]?-[^<>]*</font>', "", content, flags=re.DOTALL|re.IGNORECASE)
    
    
    #Umwandlung von Inline-Elementen in TEI
    content = re.sub('<em>(.*?)</em>', r'<seg rend="italic">\1</seg>', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('<i>(.*?)</i>', r'<seg rend="italic">\1</seg>', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('<p>(\*  \*  \*)</p>', r'<milestone rend="asterisks"/>', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('<p>\*\*\*</p>', '<milestone rend="asterisks"/>', content, flags=re.DOTALL|re.IGNORECASE)  
    content = re.sub('<span[\n\s]+lang=\n?"[a-z]+"[\n\s]+xml:lang=\n?"([a-z]+)"[^<>]*>([^<>]+)</span>', r'<seg type="foreign" xml:lang="\1">\2</seg>', content, flags=re.DOTALL|re.IGNORECASE)
    
    # Umwandlung von Blockelementen, Struktur erstellen
    #content = re.sub('<div align="center">[\n\s]*<h[23]>([^<>]+)</h[23]>[\n\s]*</div>', r'<head>\1</head>', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('<div align="center"><h3>(- [A-Z]+ -)</h3></div>  <div align="center">([^<>]+)</div>', r'<test>\1: \2</test>', content, flags=re.DOTALL)
    content = re.sub('<head>', r"</div><div><head>", content, flags=re.DOTALL|re.IGNORECASE)     
    # content = re.sub('<div align="center"><h2>([^<>]+)</h2></div>[\s\n]*</div>', r'</div></div><div><head>\1</head>', content, flags=re.DOTALL)    
    # content = re.sub('<div align="center">([^<>]+)</div>', r'<head>\1</head>', content, flags=re.DOTALL)
    # <div align="center">[^<>]*<span class="h2">[^<>]*<strong>([A-Z]+)</strong>[^<>]*</span>[^<>]*</div>
    # </div><div><head>$1</head>
    
    
    # Tabellen --> Verse
    content = re.sub('<table[^>]+>', "", content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('</table>', "", content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('<tr>', "", content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('</tr>', "", content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('<td[^>]*></td>', "", content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('<td nowrap="yes">', "", content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('<td[^>]*style="white-space:nowrap;">', "<td>", content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('<td>(.*?)</td>', r'<l>\1</l>', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('</p>[\s\n]*<l>', "</p><lg><l>", content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub('</l>[\s\n]*<p>', "</l></lg><p>", content, flags=re.DOTALL|re.IGNORECASE)
    
       
    #content = re.sub('^\s*</div>', "", content, flags=re.MULTILINE)
    #content = re.sub('</p>\s*$', "</p></div>", content, flags=re.MULTILINE)
    
    #content = re.sub('\s{2,}', " ", content)
    #content = re.sub('\n{2,}', "", content)
    
    soup = BeautifulSoup(content)
    soup = soup.prettify()
    
    with open (os.path.join("output", "out.html"), "w") as fout:
        fout.write(str(soup))
