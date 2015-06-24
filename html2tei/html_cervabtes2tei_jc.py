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
    content = re.sub(r'<p style="font-size:12pt;text-align: justify;text-indent:30px;">', r'<p>', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'<p style="text-align: justify;">', r'<p>', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'<p [^>]*?>\s*<hr.*?>\s*</p>', r'<milestone />', content, flags=re.DOTALL|re.IGNORECASE)

        #Revisar!    
    content = re.sub(r'<span .*?lang="([^"]*)".*?>(.*?)</span>', r'<seg type="foreign" xml:lang="\1">\2</seg>', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'<em(>| [^>]+)(.*?)</em>', r'<seg rend="italics">\2</seg>', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'<i(>| [^>]+)(.*?)</i>', r'<seg rend="italics">\2</seg>', content, flags=re.DOTALL|re.IGNORECASE)

    #Cleaning the HTML indent
        # We should also clean this character:"	". It looks like a tab, but it isn't. For example in misterio.html	
    content = re.sub(r'^[\s]+', r'', content)
    content = re.sub(r'^\t+', r'', content)
    content = re.sub(r'[\r\n]+', r'\r\n', content)
    content = re.sub(r'(<(/p|/h[1-6]|/?div|/head|/l|/?lg|/?body|/?back|/?text|/?front)>)', r'\1\r\n', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'([^\s<>])[\r\n]+([^\s<>])', r'\1 \2', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'(>)[\r\n]+([^\s<>])', r'\1 \2', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'<p> +', r'<p>', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'[\r\n]+', r'\r\n', content)

    #Setting the <div>s searching for the <hn>
    #It takes in the <hn> the textual information about the chapter or part
    content = re.sub(r'(</h[1-5]>)[\s]+([^<\r\n ][^\r\n]*)([\r\n]*)', r' : \2 \1\3', content, flags=re.DOTALL|re.IGNORECASE)
    # It sets divs. Actually we should use an if structure to analyse how many levels of <hn> are in the HTML document and clouse them as good as it can.
    content = re.sub(r'(</h2>)\s*?(<h3>)', r'\1\r\n<div>\r\n\2', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'(</p>)\s*?(<h3>)', r'\1\r\n</div>\r\n<div>\r\n\2', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'(</p>)\s*?(<h2>)', r'\1\r\n</div>\r\n</div>\r\n<div>\r\n\2', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'<(/?)h[1-6]>', r'<\1head>', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'\Z', r'</div>\r\n</div>', content, flags=re.DOTALL|re.IGNORECASE)


    with open (os.path.join("output", "output.html"), "w") as fout:
        fout.write(content)