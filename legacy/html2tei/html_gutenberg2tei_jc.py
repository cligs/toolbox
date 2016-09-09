# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/jose/.spyder2/.temp.py
"""
import re
import os
import html.parser
import glob

def cleaningHTML(text):
    """
        It decodes the HTML entities and it deletes some anoying characters
    """
    # HTML-Entities decodieren
    h = html.parser.HTMLParser(convert_charrefs=True)
    text = h.unescape(text)
    
    #Delete classes in the <hn> elements
    text = re.sub(r'<(/?h[1-6])[^>]*>', r'<\1>', text, flags=re.DOTALL|re.IGNORECASE)
    
    #
    text = re.sub(r'<(/?)P(| [^>]+)>', r'<\1p\2>', text, flags=re.DOTALL)
    text = re.sub(r'<(/?)H([1-6])>', r'<\1h\2>', text, flags=re.DOTALL)

    
    # Geschützte Leerzeichen löschen
    text = re.sub('\u00A0', " ", text)
    return text

def cleaningIndent(text):
    """
    Cleaning the HTML indent
    """
    text = re.sub(r'^[\s \t]+', r'', text)
    text = re.sub(r'[\s \t]+$', r'', text)
    text = re.sub(r'[\r\n]+', r'\r\n', text)
    text = re.sub(r'(<(/p|/h[1-6]|/?div|/head|/l|/?lg|/?body|/?back|/?text|/?front)>)', r'\1\r\n', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'([^\r\n<>])[\r\n]+([^\r\n<>])', r'\1 \2', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'([^>$])\r\n *(<seg)', r'\1 \2', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(>)[\r\n]+([^\s<>])', r'\1 \2', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p> +', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'[\r\n]+', r'\r\n', text)
    text = re.sub(r' +', r' ', text)
    text = re.sub(r'<p(>| [^>]*>)\s*</p>', r' ', text)
    text = re.sub(r'[\t ]', r' ', text)
    return text

def deletingNonBody(text):
    """
        It deletes the possible several elements before and after the <body>
    """
    # Delete everything before <div id="obra">
    text = re.sub(r'\A.*?(<h2)', r"\1", text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<pre>.*?</pre>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</body>\s*</html>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    return text

def deletingElements(text):
    """
    Delete different tags
    """
    #With the next 
    text = re.sub(r'(<span class="letrre"><img[^>]*?alt="([^"]*?)"[^>]*?></span>)', r'\1\2', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<img[^>]*alt="(.)"[^>]*?>', r'\1', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<img[^>]*?>', r'', text, flags=re.DOTALL|re.IGNORECASE)


    text = re.sub(r'<img[^>]*?>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</?a(>|\s[^>]*?>)', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<a[^>]*?>\[[0-9]*?\]</a>', r'', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<!--.*?-->', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<hr[^>]*?>\s(<h[1-6]>)', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<span\s*class="pagenum">[0-9\s\{\}]*?</span>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(</h[1-6]>\s*)<p class="(?:c|head)">(.*?)</p>', r' - \2 \1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<!DOCTYPE.*?>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<html.*?>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<head>.*?</head>', r'', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<p class="onda">[/\\]*</p>', r'', text, flags=re.DOTALL|re.IGNORECASE)

    return text

def replacingBasicElements(text):
    text = re.sub(r'<em(>| [^>]+>)(.*?)</em>', r'<seg rend="italics">\2</seg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<i(>| [^>]+)(.*?)</i>', r'<seg rend="italics">\2</seg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<b>(.*?)</b>', r'<seg rend="bold">\1</seg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<span style="margin-left: [0-9\.]*em;">(.+?)</span><br />', r'<l>\1</l>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<span style="margin-left: 25%;">(.+?)</span><br />', r'<l>\1</l>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<span style="margin-left: [23]em;">(.+?)</span><br ?/?>', r'<l>\1</l>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<seg rend="italics">(.+?)</seg><br />', r'<l>\1</l>', text, flags=re.IGNORECASE)

    text = re.sub(r'<span class="i[0-9]">(.+?)<br /></span>', r'<l>\1</l>', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<p class="poem">(.*?)</p>', r'<lg>\1</lg>', text, flags=re.DOTALL|re.IGNORECASE)


    text = re.sub(r'(</l>\s*)</div>', r'\1</lg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div [^>]*?>(\s*<l>)', r'<lg>\1', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'(</l>\s*)<br />\s*</p>', r'\1</lg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p[^>]*?>\s*<br />(\s*<l>)', r'<lg>\1', text, flags=re.DOTALL|re.IGNORECASE)


    #We delete 2 <hr /> followed by each other
    text = re.sub(r'<hr[^>]*?>(\s*<hr[^>]*?>)', r'\1', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'(<(div|h[1-6])[^>]*?>\s*)<hr[^>]*?>', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<hr[^>]*?>(\s*<(div|h[1-6])[^>]*?>)', r'\1', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<div class="footnote">.*?</div>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    

    text = re.sub(r'<p>[\* ]+</p>', r'<milestone unit="section" />', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="nind">[\s]*<span class="letrre"></span>', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="(?:r|r smcap|c)">(.*?)</p>', r'<ab>\1</ab>', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<div class="stanza">(.*?)</div>', r'<lg>\n\1</lg>\n', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="poem">(.*?)</div>', r'<lg>\n\1</lg>\n', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<small(?:|[^>]*?)>(.*?)</small>', r'<seg rend="small">\1</seg>', text, flags=re.IGNORECASE|re.DOTALL)

    text = re.sub(r'^<span class="i[01]">(.*?)<br></span>$', r'<l>\1</l>', text, flags=re.IGNORECASE|re.M)

    #text = re.sub(r'<br />', r'', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<lg>\s+<span style="margin-left: 1em;">(.*?)</span>', r'<lg>\n<l>\1', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'(<l>.*?)<br>\n', r'\1</l>\n<l>', text, flags=re.IGNORECASE)

    text = re.sub(r'(</seg>)(\n</lg>)', r'\1</l>\2', text, flags=re.IGNORECASE)

    text = re.sub(r'<hr[^>]*?>', r'<milestone unit="section" />', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<br */?>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="blockquot">(.*?)</div>', r'<floatingText>\n<body>\n<div>\1</div>\n</body>\n</floatingText>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<span class="smcap">(.*?)</span>', r'<seg rend="smallcaps">\1</seg>', text, flags=re.IGNORECASE)

    text = re.sub(r'<p id="[^"]+?">', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<span class="lettre">(.*?)</span>', r'\1', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<p class="nind">', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)


    text = re.sub(r'<sup>(.*?)</sup>', r'<seg rend="sup">\1</seg>', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<table border="0" cellpadding="0" cellspacing="0" summary="">(.*?)</table>', r'<lg>\1</lg>', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<tr><td align="left">(.*?)</td></tr>', r'<l>\1</l>', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<p class="date">(.*?)</p>', r'<milestone unit="section" />\n<ab>\1</ab>', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<p +class="cb?">[\. \*\n\—]+</p>', r'<milestone unit="section" />', text, flags=re.DOTALL|re.IGNORECASE)

    return text

def setDivs(text):
    """
    Setting the <div>s searching for the <hn>
    """
    #It takes in the <hn> the textual information about the chapter or part
    text = re.sub(r'(</h[1-5]>)[\s]+([^<\r\n ][^\r\n]*)([\r\n]*)', r' : \2 \1\3', text, flags=re.DOTALL|re.IGNORECASE)

    # It deletes the <h1> and its next <p>
    text = re.sub(r'<h1.*?\r?\n<p.*?\r?\n', r'', text, flags=re.DOTALL|re.IGNORECASE)

    # It deletes the <h1> and its next <p>
    text = re.sub(r'(\A.*?)(<h[2-4])', r'\1<div>\r\n\2', text, flags=re.DOTALL|re.IGNORECASE)


    # It it looks in the document if there is any <h3>. If there is, then it will close the divs both from h2 and h3        
    listh3=re.findall("<h3",text)
    if not listh3:
        print("<h3> not found")
        # That closes the <div> of an <h2> and opens another one
        text = re.sub(r'(</p>|</ab>|</lg>|<milestone unit="section" />)\s*?(<h2>)', r'\1\r\n</div>\r\n<div>\r\n\2', text, flags=re.DOTALL|re.IGNORECASE)

        # That closes the last <div> from <h2>
        text = re.sub(r'\Z', r'</div>\r\n		</body>\r\n		<back>\r\n			<div>\r\n					<p></p>\r\n			</div>\r\n		</back>\r\n	</text>\r\n</TEI>', text, flags=re.DOTALL|re.IGNORECASE)

    else:
        print("<h3> found")
        # That opens the <div> of a <h3>
        text = re.sub(r'(</h2>)\s*?(<h3>)', r'\1\r\n<div>\r\n\2', text, flags=re.DOTALL|re.IGNORECASE)
        # That closes the div of a <h3> and opens one more for a new <h3>
        text = re.sub(r'(</p>|</ab>|</lg>|<milestone unit="section" />)\s*?(<h3>)', r'\1\r\n</div>\r\n<div>\r\n\2', text, flags=re.DOTALL|re.IGNORECASE)
        # That closes the divs both from <h3> and <h2> and open another for <h2>
        text = re.sub(r'(</p>|</ab>|</lg>|<milestone unit="section" />)\s*?(<h2>)', r'\1\r\n</div>\r\n</div>\r\n<div>\r\n\2', text, flags=re.DOTALL|re.IGNORECASE)
        
        # That closes the last divs from <h2> and <h3>
        text = re.sub(r'\Z', r'</div>\r\n</div>\r\n		</body>\r\n		<back>\r\n			<div>\r\n					<p></p>\r\n			</div>\r\n		</back>\r\n	</text>\r\n</TEI>', text, flags=re.DOTALL|re.IGNORECASE)

    #That changes the <hn> to <head> (also the closing tags!)      
    text = re.sub(r'<(/?)h[1-6]>', r'<\1head>', text, flags=re.DOTALL|re.IGNORECASE)

    return text

def settingTeiHeader(text):
    text = re.sub(r'\A',r'<?xml version="1.0" encoding="UTF-8"?>\r\n<?xml-model href="https://raw.githubusercontent.com/cligs/reference/16dbc551229adc490b871b934b9bee8cd4172303/tei/standard/cligs.rnc" type="application/relax-ng-compact-syntax"?>\r\n<TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:xi="http://www.w3.org/2001/XInclude">\r\n	<teiHeader>\r\n		<fileDesc>\r\n			<titleStmt>\r\n				<title type="main"></title>\r\n				<title type="sub"></title>\r\n				<title type="short"></title>\r\n				<title type="idno">\r\n					<idno type="viaf"></idno></title>\r\n				<author>\r\n					<idno type="viaf"></idno>\r\n					<name type="short"></name>\r\n					<name type="full"></name>\r\n				</author>\r\n				<principal xml:id="jct">José Calvo Tello</principal>\r\n			</titleStmt>\r\n			<publicationStmt>\r\n                <publisher>CLiGS</publisher>\r\n				<availability status="free">\r\n                    <p>The text is freely available.</p>\r\n				</availability>\r\n				<date when="2016">2016</date>\r\n				<idno type="cligs">ne02</idno>\r\n			</publicationStmt>\r\n			<sourceDesc>\r\n				<bibl type="digital-source"><date when="1000"></date>, <idno></idno>, <ref target="#"/>.</bibl>\r\n				<bibl type="print-source"><date when="1000"></date></bibl>\r\n				<bibl type="edition-first"><date when="1000"></date></bibl>\r\n			</sourceDesc>\r\n		</fileDesc>\r\n		<encodingDesc>\r\n			<p>.</p>\r\n		</encodingDesc>\r\n		<profileDesc>\r\n			<abstract source="#">\r\n				<p>.</p>\r\n			</abstract>\r\n			<textClass>\r\n				<keywords scheme="keywords.csv" cert="low">\r\n					<term type="author-continent">Europe</term>\r\n					<term type="author-country">Spain</term>\r\n					<term type="author-gender">male</term>\r\n\r\n					<term type="publication">book</term>\r\n					<term type="form">prose</term>\r\n					<term type="supergenre">narrative</term>\r\n					<term type="genre">novel</term>\r\n					<term type="subgenre" subtype="2"></term>\r\n					<term type="subgenre" subtype="1"></term>\r\n					<term type="subsubgenre"></term>\r\n					<term type="genre-label"></term>\r\n\r\n					<term type="narrative-perspective"></term>\r\n					<term type="setting"></term>\r\n					<term type="protagonist-gender">male</term>\r\n\r\n					<term type="subgenre-lithist"></term>\r\n\r\n					<term type="narrator"></term>\r\n					<term type="setting-name"></term>\r\n					<term type="setting-territory"></term>\r\n					<term type="setting-country"></term>\r\n					<term type="setting-continent"></term>\r\n					\r\n					<term type="representation"></term>\r\n					<term type="protagonist-name"></term>\r\n					<term type="protagonist-profession"></term>\r\n					<term type="protagonist-social-level"></term>\r\n					<term type="time-period"></term>\r\n					<term type="time-span"></term>\r\n					<term type="text-movement"></term>\r\n					<term type="group-text"></term>\r\n					<term type="author-text-relation">none</term>\r\n					<term type="protagonist-age"></term>\r\n					<term type="type-end"></term>\r\n					<term type="time-year">18??</term>\r\n					<term type="subgenre-edit" resp="#"></term>\r\n					<term type="quality-lithist" resp="#"></term>\r\n				</keywords>\r\n			</textClass>\r\n		</profileDesc>\r\n		<revisionDesc>\r\n			<change when="2016-03-16" who="#jct">Initial TEI version.</change>\r\n		</revisionDesc>\r\n	</teiHeader>\r\n    <text>\r\n    	<front>\r\n    	</front>\r\n    	<body>\r\n'    , text, flags=re.DOTALL|re.IGNORECASE)
    return text


def main():
    i=1
    for doc in glob.glob("input/*.html"):
    
        # It takes the base name of the html file, it cuts its ending and keeps a new xml name
        basenamedoc = os.path.basename(doc)[:-4]  
        docFormatOut=basenamedoc+"xml"    
    
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()
        
            # it cleans the HTML from entities, etc        
            content=cleaningHTML(content)
            
            # It deletes elements before <body> and after </body>
            content=deletingNonBody(content)

            content=deletingElements(content)

            content=replacingBasicElements(content)

            #It sets divs 
            content=setDivs(content)


            #We introduce the teiHeader
            content=settingTeiHeader(content)
            
            #It cleans the white space
            content=cleaningIndent(content)
        
        
            
            
            # It writes the result in the output folder
    
            with open (os.path.join("output", docFormatOut), "w", encoding="utf-8") as fout:
                fout.write(content)
        print(doc)
        print("Processed documents: ",i)
        i+=1

main()