# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import re
import os


def replacingElements(text):
    """
    It replaces the TEI elements with XHTML elements
    """
    # Replace some elements with atributes with other cleaner elements
    text = re.sub(r'<text>', r'<div class="text">', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</text>', r'</div>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<front>', r'<div class="front">', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</front>', r'</div>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<body>', r'<div class="body">', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</body>', r'</div>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<back>', r'<div class="back">', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</back>', r'</div>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div\s+type="(.*?)"\s+n="(\d+)">', r'<div class="\1" id="\1\2">', text, flags=re.DOTALL|re.IGNORECASE)    
    text = re.sub(r'<div\s+type="(.*?)">', r'<div class="\1">', text, flags=re.DOTALL|re.IGNORECASE)    
    text = re.sub(r'head>', r'h2>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<lg>', r'<div class="lg">', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</lg>', r'</div>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<l>', r'<p class="l">', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</l>', r'</p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<quote>', r'<div class="quote">', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</quote>', r'</div>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<floatingText>', r'<div class="floatingText">', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</floatingText>', r'</div>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<milestone [^>]*?/>', r'<hr />', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<ab>(.*?)</ab>', r'<p class="ab">\1</p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<sp>', r'<div class="sp">', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</sp>', r'</div>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<casList>', r'<div class="casList">', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</casList>', r'</div>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(\r?\n[ \t]*)<stage>', r'\1<div class="stage">', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</stage>([ \t]*\r?\n)', r'</div>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<stage>', r'<span class="stage">', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</stage>', r'</span>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<speaker>', r'<p class="speaker">', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</speaker>', r'</p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<seg ', r'<span ', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</seg>', r'</span>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(<span )([^>]*)type', r'\1\2class', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(<span )([^>]*)rend', r'\1\2class', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(<span )([^>]*)(class="[^"]*)"([^>]*)class="([^"]*)"', r'\1\2\3 \5"\4', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'', r'', text, flags=re.DOTALL|re.IGNORECASE)



    text = re.sub(r'', r'', text, flags=re.DOTALL|re.IGNORECASE)

    return text

def settingHead(text):
    """
        It deletes the possible several elements before and after the <body>
    """
    title=re.findall(r'<title type="main">(.*)</title>', text)
    text = re.sub(r'<\?xml.*?</teiHeader>', r"", text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</TEI>', r"", text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'\A',r'<h1>'+title[0]+'</h1>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'\A',r'<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"\n  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n\n<html xmlns="http://www.w3.org/1999/xhtml">\n<head>\n  <link href="../Styles/styles.css" rel="stylesheet" type="text/css" />\n\n  <title>'+title[0]+'</title>\n</head>\n\n<body>\n'    , text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'\Z',r'</body>\r\n</html>' , text, flags=re.DOTALL|re.IGNORECASE)
    return text

listdocs=["ne0198.xml",
"ne0320.xml"]

i=0
for doc in listdocs:
    
    with open(os.path.join("input",doc), "r",  errors="replace", encoding="utf-8") as fin:
        content = fin.read()
    

        #It replaces some HTML elements with TEI elements    
        content=replacingElements(content)

        
        
        #We introduce the teiHeader
        content=settingHead(content)
        
        # Improvement!: That should actually save the document as xml

        # It writes the result in the output folder
        with open (os.path.join("output", doc), "w", errors="replace",  encoding="utf-8") as fout:
            fout.write(content)
    print(doc)
    i+=1