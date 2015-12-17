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
    h = html.parser.HTMLParser()
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
    text = re.sub(r'<p> +', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'[\r\n]+', r'\r\n', text)
    text = re.sub(r' +', r' ', text)
    text = re.sub(r'<p(>| [^>]*>)\s*</p>', r' ', text)
    text = re.sub(r'[\t ]', r' ', text)
    text = re.sub(r'\r?\n[\t ]*([^<\s])', r' \1', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r' +', r' ', text, flags=re.DOTALL|re.IGNORECASE|re.M)

    return text

def deletingNonBody(text):
    """
        It deletes the possible several elements before and after the <body>
    """
    text = re.sub(r'<head>.*?</head>', r'', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'<!--.*?-->', r'', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'<script>.*?</script>', r'', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'<div id="footer".*?</div>', r'', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'(<div style="display:Visible;padding-bottom: 1em;"><span style="display:.*?">(.*?)</span>.*?<div class="Parrafo">)', r'\1\n<head>\2</head>', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<center>\s*<table.*?(<div class="Parrafo">)', r'\1', text, flags=re.DOTALL|re.IGNORECASE|re.M)

    text = re.sub(r'<center>\s*<table class="noprint" frame="above".*?(<div class="Parrafo">)', r'\1\n\2', text, flags=re.DOTALL|re.IGNORECASE|re.M)

    text = re.sub(r'<p><br></p>', r'', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'<!DOCTYPE html>', r'', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'<html.*?>', r'', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'<body .*?>', r'', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'<div id="mw-page-base" class="noprint"></div>', r'', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'\A.*?(<div class="Parrafo">)', r'\1', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'<center>\s*<table class="noprint" frame="above".*?\Z', r'', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'<center><b>(.*?)</b></center>', r'<ab>\1</ab>', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'</?center>', r'', text, flags=re.DOTALL|re.IGNORECASE|re.M)

    text = re.sub(r'', r'', text, flags=re.DOTALL|re.IGNORECASE|re.M)


    # Delete everything before <div id="obra">
    return text

def deletingElements(text):
    """
    Delete different tags
    """

    return text

def replacingBasicElements(text):

    text = re.sub(r'(<div style="display:Visible;padding-bottom: 1em;"><span style="display:.*?">(.*?)</span>.*?<div class="Parrafo">)', r'\1\n<head>\2</head>', text, flags=re.DOTALL|re.IGNORECASE)


    text = re.sub(r'<div class="poem">(.*?)</div>', r'<lg>\1</lg>', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'(<lg>\s*?)(<p>)*?([^<]*?)(<br ?/?>|</p>)', r'\1<l>\3</l>', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'(</l>\s+)([^<].*?)(<br ?/?>|</p>)', r'\1<l>\2</l>', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'(</l>\s+)([^<].*?)(<br ?/?>|</p>)', r'\1<l>\2</l>', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'(</l>\s+)([^<].*?)(<br ?/?>|</p>)', r'\1<l>\2</l>', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'(</l>\s+)([^<].*?)(<br ?/?>|</p>)', r'\1<l>\2</l>', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'(</l>\s+)([^<].*?)(<br ?/?>|</p>)', r'\1<l>\2</l>', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'(</l>\s+)([^<].*?)(<br ?/?>|</p>)', r'\1<l>\2</l>', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'(</l>\s+)([^<].*?)(<br ?/?>|</p>)', r'\1<l>\2</l>', text, flags=re.DOTALL|re.IGNORECASE|re.M)

    text = re.sub(r'<div class="Parrafo">', r'<div>', text, flags=re.DOTALL|re.IGNORECASE|re.M)

    text = re.sub(r'<(i|em)>', r'<seg rend="italic">', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'</(i|em)>', r'</seg>', text, flags=re.DOTALL|re.IGNORECASE|re.M)


    text = re.sub(r'<p><br>\n', r'<p>', text, flags=re.DOTALL|re.IGNORECASE|re.M)
    text = re.sub(r'</l></p>', r'</l>', text, flags=re.DOTALL|re.IGNORECASE|re.M)


    return text


def settingTeiHeader(text):
    text = re.sub(r'\A',r'<?xml version="1.0" encoding="UTF-8"?>\r\n<?xml-model href="https://raw.githubusercontent.com/cligs/toolbox/master/tei/cligs.rnc" type="application/relax-ng-compact-syntax"?>\r\n<TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:xi="http://www.w3.org/2001/XInclude">\r\n	<teiHeader>\r\n		<fileDesc>\r\n			<titleStmt>\r\n				<title type="main"></title>\r\n				<title type="sub"></title>\r\n				<title type="short"></title>\r\n				<title type="idno">\r\n					<idno type="viaf"></idno></title>\r\n				<author>\r\n					<idno type="viaf"></idno>\r\n					<name type="short"></name>\r\n					<name type="full"></name>\r\n				</author>\r\n				<principal xml:id="jct">José Calvo Tello</principal>\r\n			</titleStmt>\r\n			<publicationStmt>\r\n                <publisher>CLiGS</publisher>\r\n				<availability status="publicdomain">\r\n                    <p>The text is freely available.</p>\r\n				</availability>\r\n				<date when="2015">2015</date>\r\n				<idno type="cligs">ne01</idno>\r\n			</publicationStmt>\r\n			<sourceDesc>\r\n				<bibl type="digital-source"><date when="1000"></date>, <idno></idno>, <ref target="#"/>.</bibl>\r\n				<bibl type="print-source"><date when="1000"></date></bibl>\r\n				<bibl type="edition-first"><date when="1000"></date></bibl>\r\n			</sourceDesc>\r\n		</fileDesc>\r\n		<encodingDesc>\r\n			<p>.</p>\r\n		</encodingDesc>\r\n		<profileDesc>\r\n			<abstract>\r\n				<p>.</p>\r\n			</abstract>\r\n			<textClass>\r\n				<keywords scheme="keywords.csv">\r\n					<term type="supergenre">narrative</term>\r\n					<term type="genre">novel</term>\r\n					<term type="subgenre" cert="low" resp="x"></term>\r\n					<term type="genre-label"></term>\r\n					<term type="narrative-perspective" cert="low" resp="#jct"></term>\r\n					<term type="publication">book</term>\r\n					<term type="form">prose</term>\r\n					<term type="author-gender">male</term>\r\n					<term type="protagonist-gender">male</term>\r\n					<term type="setting" cert="low" resp="#jct"></term>\r\n					<term type="subgenre-lithist"></term>\r\n				</keywords>\r\n			</textClass>\r\n		</profileDesc>\r\n		<revisionDesc>\r\n			<change when="2015-08-13" who="#jct">Initial TEI version.</change>\r\n		</revisionDesc>\r\n	</teiHeader>\r\n    <text>\r\n    	<front>\r\n    	</front>\r\n    	<body>\r\n'    , text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'\Z', r'\r\n		</body>\r\n		<back>\r\n			<div>\r\n					<p></p>\r\n			</div>\r\n		</back>\r\n	</text>\r\n</TEI>', text, flags=re.DOTALL|re.IGNORECASE)

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
            #content=setDivs(content)


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