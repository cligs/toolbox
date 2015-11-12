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
    #h = html.parser.HTMLParser()
    #text = h.unescape(text)
    
    # Geschützte Leerzeichen löschen
    text = re.sub('\u00A0', " ", text)
    return text


def settingTeiHeader(text):
    text = re.sub(r'\A',r'<?xml version="1.0" encoding="UTF-8"?>\r\n<?xml-model href="https://raw.githubusercontent.com/cligs/toolbox/master/tei/cligs.rnc" type="application/relax-ng-compact-syntax"?>\r\n<TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:xi="http://www.w3.org/2001/XInclude">\r\n	<teiHeader>\r\n		<fileDesc>\r\n			<titleStmt>\r\n				<title type="main"></title>\r\n				<title type="sub"></title>\r\n				<title type="short"></title>\r\n				<title type="idno">\r\n					<idno type="viaf"></idno></title>\r\n				<author>\r\n					<idno type="viaf"></idno>\r\n					<name type="short"></name>\r\n					<name type="full"></name>\r\n				</author>\r\n				<principal xml:id="jct">José Calvo Tello</principal>\r\n			</titleStmt>\r\n			<publicationStmt>\r\n                <publisher>CLiGS</publisher>\r\n				<availability status="publicdomain">\r\n                    <p>The text is freely available.</p>\r\n				</availability>\r\n				<date when="2015">2015</date>\r\n				<idno type="cligs">ne01</idno>\r\n			</publicationStmt>\r\n			<sourceDesc>\r\n				<bibl type="digital-source"><date when="1000"></date>, <idno></idno>, <ref target="#"/>, <ref target="#"/>.</bibl>\r\n				<bibl type="print-source"><date when="1000"></date></bibl>\r\n				<bibl type="edition-first"><date when="1000"></date></bibl>\r\n			</sourceDesc>\r\n		</fileDesc>\r\n		<encodingDesc>\r\n			<p>.</p>\r\n		</encodingDesc>\r\n		<profileDesc>\r\n			<abstract>\r\n				<p>.</p>\r\n			</abstract>\r\n			<textClass>\r\n				<keywords scheme="keywords.csv">\r\n					<term type="supergenre">narrative</term>\r\n					<term type="genre">novel</term>\r\n					<term type="subgenre" cert="low" resp="x"></term>\r\n					<term type="genre-label"></term>\r\n					<term type="narrative-perspective" cert="low" resp="#jct"></term>\r\n					<term type="publication">book</term>\r\n					<term type="form">prose</term>\r\n					<term type="author-gender">male</term>\r\n					<term type="protagonist-gender">male</term>\r\n					<term type="setting"></term>\r\n				</keywords>\r\n			</textClass>\r\n		</profileDesc>\r\n		<revisionDesc>\r\n			<change when="2015-08-13" who="#jct">Initial TEI version.</change>\r\n		</revisionDesc>\r\n	</teiHeader>\r\n    <text>\r\n    	<front>\r\n    	</front>\r\n    	<body>\r\n'    , text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'\Z', r'\r\n		</body>\r\n		<back>\r\n			<div>\r\n					<p></p>\r\n			</div>\r\n		</back>\r\n	</text>\r\n</TEI>', text, flags=re.DOTALL|re.IGNORECASE)

    return text

def replacingBasicElementsFromFineReader(text):
    """
    It replaces some elements and its styles with TEI elements
    """

    text = re.sub(r'<span [^>]*?>[0-9\- \.]*</span>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<img[^>]*>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<br[^/>]+/>(\s<p)', r'\1', text, flags=re.IGNORECASE)



    text = re.sub(r'<span[^>]*font-style:italic;[^>]*>(.*?)</span>', r'<seg rend="italics">\1</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<span[^>]*font-variant:small-caps[^>]*>(.*?)</span>', r'<seg rend="small-caps">\1</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<span[^>]*font-weight:bold[^>]*>(.*?)</span>', r'<seg rend="bold">\1</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<sup(|[^>]*)>(.*?)</sup>', r'<seg rend="sup">\2</seg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<sub(|[^>]*)>(.*?)</sub>', r'<seg rend="sub">\2</seg>', text, flags=re.DOTALL|re.IGNORECASE)

    #We put the title using the bookmark
    text = re.sub(r'^(.*?name="bookmark.*)$', r'<head>\1</head>', text, flags=re.IGNORECASE|re.M)
    text = re.sub(r'<head>(<.*?>)+(.*?)(<.*?>)</head>', r'<head>\2</head>', text, flags=re.IGNORECASE|re.M)

    #Deleting some rubish at the beginnint of the line
    text = re.sub(r'(<p><span class="[^"]*?">)\s*(<[^>]*?>)?[:y\[](<[^>]*?>)?(—)', r'\1\2\3\4', text, flags=re.IGNORECASE)
    text = re.sub(r'(<p><span class="[^"]*?">)[:y■\[](—)', r'\1\2', text, flags=re.IGNORECASE)
    text = re.sub(r'(<p><span class="[^"]*?">)--', r'\1—', text, flags=re.IGNORECASE)
    text = re.sub(r'(<p><span class="[^"]*?">)— ?[ji] ?', r'\1¡', text)


    text = re.sub(r'<div[^>]*>\s*</div>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p[^>]*>\s*</p>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<seg[^>]*>\s*</seg>', r'', text, flags=re.DOTALL|re.IGNORECASE)

    
    text = re.sub(r'-</span></p>\s*<p><span class="[^"]*?">([a-zéíóúáñ])', r'\1', text, flags=re.DOTALL)
    text = re.sub(r'([a-zéíóúáñ,])</span></p>\s*<p><span class="[^"]*?">([a-zéíóúáñ])', r'\1 \2', text, flags=re.DOTALL)
    text = re.sub(r'-</span></p>\s*<p><span class="[^"]*?">([a-zéíóúáñ])', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'([a-zéíóúáñ,])</p>\s*<p>([a-zéíóúáñ])', r'\1 \2', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<div[^>]*>\s*</div>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p[^>]*>\s*</p>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<seg[^>]*>\s*</seg>', r'', text, flags=re.DOTALL|re.IGNORECASE)


    return text

def replacingBasicText(text):
    text = re.sub(r'&gt;', r'»', text, flags=re.IGNORECASE)
    text = re.sub(r'&lt;', r'«', text, flags=re.IGNORECASE)
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

        content=replacingBasicText(content)
        
        
        #It replaces some HTML elements with TEI elements    
        content=replacingBasicElementsFromFineReader(content)
        
        

        # It writes the result in the output folder
    
        with open (os.path.join("output", docFormatOut), "w", encoding="utf-8") as fout:
                fout.write(content)
        print(doc)
        print("Processed documents: ",i)
        i+=1

main()