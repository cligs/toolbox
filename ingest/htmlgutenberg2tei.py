# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 23:48:59 2015

@author: ulrike
"""

import re
import html.parser

with open("in1.html", "r") as fin:
    content = fin.read()
    
    h = html.parser.HTMLParser()
    content = h.unescape(content)

    content = re.sub(r'<!DOCTYPE.*?<body>', r'', content, flags=re.DOTALL)
    content = re.sub(r'<pre>.*?</pre>', r'', content, flags=re.DOTALL)
    content = re.sub(r'</body>.*?</html>', r'', content, flags=re.DOTALL)
    
    content = re.sub(r'<p class="c">([A-Z]+)</p>', r'<ab type="trailer">\1</ab>', content, flags=re.DOTALL)
    content = re.sub(r'<i>(.*?)</i>', r'<hi rend="italic">\1</hi>', content, flags=re.DOTALL)
    content = re.sub(r'<p style="margin-top:5%;">', r'<p>', content, flags=re.DOTALL)
    content = re.sub(r'<h2><a name="([A-Z]+)" id="\1"></a>\1</h2>', r'</div><div><head>\1</head>', content, flags=re.DOTALL)

    content = re.sub(r'\u00A0', " ", content)
    content = re.sub(r'\s{2,}', " ", content)
    content = re.sub(r'\n{2,}', "", content)
    
    with open ("out.html", "w") as fout:
        fout.write(content)