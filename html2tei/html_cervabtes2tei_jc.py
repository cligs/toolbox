# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/jose/.spyder2/.temp.py
"""
import re
import os
import html.parser

with open(os.path.join("input","misterio.html"), "r", errors="replace") as fin:
    content = fin.read()

    # HTML-Entities decodieren
    h = html.parser.HTMLParser()
    content = h.unescape(content)

    # Geschützte Leerzeichen löschen
    content = re.sub('\u00A0', " ", content)

    # Delete everything before <div id="obra">
    content = re.sub(r'<!DOCTYPE html>.*?(<div id="obra")', r"\1", content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'<!DOCTYPE html.*?<body>', r"", content, flags=re.DOTALL|re.IGNORECASE)
    #Delete everything after </body>
    content = re.sub(r'</body>.*?</body>.*?</html>', r'', content, flags=re.DOTALL|re.IGNORECASE)

    #Delete different tags
    content = re.sub(r'</?a(>| [^>]*>)', r'', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'</?br(>| [^>]*)>', r'', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'<img[^>]*>', r'', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'</?div[^>]*>', r'', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'<span style="font-style:normal;">.*?</span>', r'\1', content, flags=re.DOTALL|re.IGNORECASE)
    
    # Replace some elements with atributes with other cleaner elements
    content = re.sub(r'<p style="text-align: justify;text-indent:30px;">', r'<p>', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'<p style="text-align: justify;text-indent:30px;">', r'<p>', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'<p style="text-align: right;text-indent:30px;">', r'<p>', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'<p style="text-align: justify;">', r'<p>', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'(<p [^>]*?><hr.*?></p>', r'<milestone />', content, flags=re.DOTALL|re.IGNORECASE)

        #Revisar!    
    content = re.sub(r'<span .*?lang="([^"]*)".*?>(.*?)</span>', r'<seg type="foreign" xml:lang="\1">\2</seg>', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'<em(>| [^>]+)(.*?)</em>', r'<seg rend="italics">\2</seg>', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'<i(>| [^>]+)(.*?)</i>', r'<seg rend="italics">\2</seg>', content, flags=re.DOTALL|re.IGNORECASE)

    #Cleaning the HTML indent
    content = re.sub(r'^[ \t]+$', r'', content)
    content = re.sub(r'[\r\n]+', r'\r\n', content)
    content = re.sub(r'(<(/p|/h[1-6]|/?div|/head|/l|/?lg|/?body|/?back|/?text|/?front)>)', r'\1\r\n', content, flags=re.DOTALL|re.IGNORECASE)

    #Setting the <div>s searching for the <hn>
    content = re.sub(r'(</h2>)\r\n(<h3>)', r'\1\r\n<div>\r\n\2', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'(</p>)\r\n(<h3>)', r'\1\r\n</div>\r\n<div>\r\n\2', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'', r'', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'', r'', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'', r'', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'', r'', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'', r'', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'', r'', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'', r'', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'', r'', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'', r'', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'', r'', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'', r'', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'', r'', content, flags=re.DOTALL|re.IGNORECASE)



    with open (os.path.join("output", "output.html"), "w") as fout:
        fout.write(content)