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


def upper_repl(match):
     return match.group(1).upper()

def cleaningHTML(text):
    """
        It decodes the HTML entities and it deletes some anoying characters
    """
    # HTML-Entities decodieren
    h = html.parser.HTMLParser(convert_charrefs=True)
    text = h.unescape(text)
    
    # Geschützte Leerzeichen löschen
    text = re.sub('\u00A0', " ", text)
    text = re.sub(r'&', r'&amp;', text)
    text = re.sub(r'<a .*?>', r'', text)
    text = re.sub(r'</a>', r'', text)
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
    return text

    
def settingTeiHeader(text):
    text = re.sub(r'\A',r'<?xml version="1.0" encoding="UTF-8"?>\r\n<?xml-model href="https://raw.githubusercontent.com/cligs/toolbox/master/tei/cligs.rnc" type="application/relax-ng-compact-syntax"?>\r\n<TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:xi="http://www.w3.org/2001/XInclude">\r\n	<teiHeader>\r\n		<fileDesc>\r\n			<titleStmt>\r\n				<title type="main"></title>\r\n				<title type="sub"></title>\r\n				<title type="short"></title>\r\n				<title type="idno">\r\n					<idno type="viaf"></idno></title>\r\n				<author>\r\n					<idno type="viaf"></idno>\r\n					<name type="short"></name>\r\n					<name type="full"></name>\r\n				</author>\r\n				<principal xml:id="jct">José Calvo Tello</principal>\r\n			</titleStmt>\r\n			<publicationStmt>\r\n                <publisher>CLiGS</publisher>\r\n				<availability status="publicdomain">\r\n                    <p>The text is freely available.</p>\r\n				</availability>\r\n				<date when="2016">2016</date>\r\n				<idno type="cligs">ne02</idno>\r\n			</publicationStmt>\r\n			<sourceDesc>\r\n				<bibl type="digital-source"><date when="1000"></date>, <idno></idno>, <ref target="#"/>.</bibl>\r\n				<bibl type="print-source"><date when="1000"></date></bibl>\r\n				<bibl type="edition-first"><date when="1000"></date></bibl>\r\n			</sourceDesc>\r\n		</fileDesc>\r\n		<encodingDesc>\r\n			<p>.</p>\r\n		</encodingDesc>\r\n		<profileDesc>\r\n			<abstract source="#">\r\n				<p>.</p>\r\n			</abstract>\r\n			<textClass>\r\n				<keywords scheme="keywords.csv" cert="low">\r\n					<term type="author-continent">Europe</term>\r\n					<term type="author-country">Spain</term>\r\n					<term type="author-gender">male</term>\r\n\r\n					<term type="publication">book</term>\r\n					<term type="form">prose</term>\r\n					<term type="supergenre">narrative</term>\r\n					<term type="genre">novel</term>\r\n					<term type="subgenre" subtype="2"></term>\r\n					<term type="subgenre" subtype="1"></term>\r\n					<term type="subsubgenre"></term>\r\n					<term type="genre-label"></term>\r\n\r\n					<term type="narrative-perspective"></term>\r\n					<term type="setting"></term>\r\n					<term type="protagonist-gender">male</term>\r\n\r\n					<term type="subgenre-lithist"></term>\r\n\r\n					<term type="narrator"></term>\r\n					<term type="setting-name"></term>\r\n					<term type="setting-territory"></term>\r\n					<term type="setting-country"></term>\r\n					<term type="setting-continent"></term>\r\n					\r\n					<term type="representation"></term>\r\n					<term type="protagonist-name"></term>\r\n					<term type="protagonist-profession"></term>\r\n					<term type="protagonist-social-level"></term>\r\n					<term type="time-period"></term>\r\n					<term type="time-span"></term>\r\n					<term type="text-movement"></term>\r\n					<term type="group-text"></term>\r\n					<term type="author-text-relation">none</term>\r\n					<term type="protagonist-age"></term>\r\n					<term type="type-end"></term>\r\n					<term type="time-year">18??</term>\r\n					<term type="subgenre-edit" resp="#"></term>\r\n				</keywords>\r\n			</textClass>\r\n		</profileDesc>\r\n		<revisionDesc>\r\n			<change when="2016-03-16" who="#jct">Initial TEI version.</change>\r\n		</revisionDesc>\r\n	</teiHeader>\r\n    <text>\r\n    	<front>\r\n    	</front>\r\n    	<body>\r\n'    , text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'\Z', r'\r\n</div>\r\n		</body>\r\n		<back>\r\n			<div>\r\n					<p></p>\r\n			</div>\r\n		</back>\r\n	</text>\r\n</TEI>', text, flags=re.DOTALL|re.IGNORECASE)

    return text

def replacingBasicElementsFromEpubLibre(text):
    """
    It replaces some elements and its styles with TEI elements
    """
    text = re.sub(r'<div class="vineta"><img[^<]*?</div>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    
    
    # Replace some elements with atributes with other cleaner elements

    text = re.sub(r'<p class="ind">', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
    
    text = re.sub(r'<p class="cursiva\d*">(.*?)</p>', r'<p><seg rend="italic">\1</seg></p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="calibre[0-9]+">', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="saltoinicio\d*">', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="salto[0-9]+">', r'<milestone />\n<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="saltoc">', r'<milestone />\n<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="sinopsis">.*?</div>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="ilustra">.*?</div>', r'', text, flags=re.DOTALL|re.IGNORECASE) 
    text = re.sub(r'<div class="info">.*?</div>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<br class="calibre9" />', r' ', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<sup(|[^>]*)>(<a[^>]*?>)?\[.*?\](</a>)?</sup>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<span(|[^>]*)>\s*</span>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<a(|[^>]*)>\s*</a>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="(tlogo|tautor|ttitulo|trevision|tfirma)">.*?</p>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<h1 class="ttitulo">(.*?)</h1>\s*(<p class="titulo">.*?</p>)', r'<head>\1: \2</head>', text, flags=re.DOTALL|re.IGNORECASE)
       
    text = re.sub(r'<img[^>]*?>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="(bloque|ala)?derecha[0-9]*">(.*?)</p>', r'<ab>\2</ab>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="asangre[0-9]?">', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
    #text = re.sub(r'<p class="centrado1">(.*?)</p>', r'<quote>\n<p>\1</p>\n</quote>', text, flags=re.DOTALL|re.IGNORECASE)
    #text = re.sub(r'<p class="extenso">(.*?)</p>', r'<quote>\n<p>\1</p>\n</quote>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<span class="(normal|calibre)[0-9]*">(.*?)</span>', r'<seg rend="italic">\2</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<p><span class="(cap[0-9]*|versalita|smallcaps)">(..?)</span>', r'<p>\2', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<span class="(versalita|smallcaps)[0-9]*">(.*?)</span>', r'<seg rend="smallcaps">\2</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<div class="poema[0-9]*">(.*?)</div>', r'<lg>\1</lg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="poe">(.*?)</div>', r'<lg>\1</lg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="versos?">(.*?)</div>', r'<lg>\1</lg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="estrofas?">(.*?)</div>', r'<lg>\1</lg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="citar\d?">(.*?)</div>', r'<lg>\1</lg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<blockquote class="verso\d*">(.*?)</blockquote>', r'<lg>\1</lg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<blockquote class="versosinpie\d*">(.*?)</blockquote>', r'<lg>\1</lg>', text, flags=re.DOTALL|re.IGNORECASE)
    

    text = re.sub(r'<p class="verso">(.*?)</p>', r'<l>\1</l>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="normal1">(.*?)</p>', r'<l>\1</l>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="cursiva">(.*?)</p>', r'<p><seg rend="italic">\1</seg></p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<em(|[^>]*)>(.*?)</em>', r'<seg rend="italic">\2</seg>', text, flags=re.IGNORECASE)

    text = re.sub(r'<p class="estrofa1">', r'\n\n<p>', text, flags=re.DOTALL|re.IGNORECASE)
     
    text = re.sub(r'<i(|[^>]*)>(.*?)</i>', r'<seg rend="italic">\2</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<b(|[^>]*)>(.*?)</b>', r'<seg rend="bold">\2</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<sup(|[^>]*)>(.*?)</sup>', r'<seg rend="sup">\2</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<span class="cursiva[0-9]*">(.*?)</span>', r'<seg rend="italic">\1</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<sub(|[^>]*)>(.*?)</sub>', r'<seg rend="subscript">\2</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<small(|[^>]*)>(.*?)</small>', r'<seg rend="small">\2</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<span class="nosep\d*">(.*?)</span>', r'<seg rend="italic">\1</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<strong(|[^>]*)>(.*?)</strong>', r'<seg rend="bold">\2</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<p class="cita">(.*?)</p>', r'<quote>\n<p>\1</p>\n</quote>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="micita">(.*?)</p>', r'<quote>\n<p>\1</p>\n</quote>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="acotacion\d*">(.*?)</div>', r'<quote>\n\1\n</quote>', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<cite.*?>(.*?)</cite>', r'<seg type="cite">\1</seg>', text, flags=re.DOTALL|re.IGNORECASE)
    
    # Setting quotes in floatingText element
    text = re.sub(r'<div class="(mi)?cita">(.*?)</div>', r'<floatingText>\n<body>\n<div>\n\2\n</div>\n</body>\n</floatingText>\n', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<p class="salto25x">([IVXCL\d]+)</p>', r'<head>\1</head>', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<p class="salto25x\d+">', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
         
    text = re.sub(r'</head>\s*<p class="subtil">(.*?)</p>', r': \1</head>', text, flags=re.DOTALL|re.IGNORECASE)
   
    text = re.sub(r'<div class="bloquederecha1">(.+?)</div>', r'<quote>\1</quote>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="cursiva[0-9]*">', r'<div rend="italic">', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="calibre" id="calibre_link-[0-9]+">', r'<div>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="centrado">[… ]+?</p>', r'<milestone />', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="asteriscos">[\* ]*</p>', r'<milestone />', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="centrado">\[…\]</p>', r'<milestone />', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="asteriscos1">[\. ]+</p>', r'<milestone />', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<hr (class="calibre12" )?/>', r'<milestone />', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="banner">(.*?)</div>', r'<floatingText>\n<body>\n<div>\n\1\n</div>\n</body>\n</floatingText>\n', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<blockquote class="banner\d*">(.*?)</blockquote>', r'<floatingText>\n<body>\n<div>\n\1\n</div>\n</body>\n</floatingText>\n', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<blockquote class="carta\d*">(.*?)</blockquote>', r'<floatingText>\n<body>\n<div>\n\1\n</div>\n</body>\n</floatingText>\n', text, flags=re.DOTALL|re.IGNORECASE)
    #text = re.sub(r'<blockquote class="cita">(.*?)</blockquote>', r'<floatingText>\n<body>\n<div>\n\1\n</div>\n</body>\n</floatingText>\n', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<blockquote class="calibre\d*">(.*?)</blockquote>', r'<floatingText>\n<body>\n<div>\n\1\n</div>\n</body>\n</floatingText>\n', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<html.*?<body>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</body></html>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(</p>)\s*(<head>.*?</head>)', r'\1</div>\n<div>\n\2', text, flags=re.DOTALL|re.IGNORECASE)
    """ #Used for 219    
    text = re.sub(r'<p class="sub">(.*?)</p>', r'<head>\1</head>', text, flags=re.DOTALL|re.IGNORECASE)
    """
    text = re.sub(r'<h[1-6][^>]*>(.*?)</h[1-6]>', r'<head>\1</head>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="(tsub|sub)?tit(ulo)?[0-9]*">(.*?)</p>', r'<head>\3</head>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="(subcapitulo|capitulonombre)">(.*?)</p>', r'<head>\2</head>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="tit-cap">(.*?)</p>', r'<head>\1</head>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<span class="ncap">(.*?)</span>', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<span class="ncap">(.*?)</span>', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<span class="palabra">(.*?)</span>', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<span class="sigla\d*">(.*?)</span>', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(<p>—?)<span class="inicial">(.*?)</span>', r'\1\2', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(<p>—?¿?)<big class="calibre\d*">(.*?)</big>', r'\1\2', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<head>\s*</head>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</head>\s*<head>', r': ', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p [^>]*?>\s*\* *\* *\*</p>', r'<milestone />', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="sep">\* \* \*</p>', r'<milestone />', text, flags=re.DOTALL|re.IGNORECASE)



    """
    #Setting divs after ps. Used for 219
    text = re.sub(r'(</p>|</div>)(\s*<head>.*?</head>.*?)(<head>|</div>|<div>)', r'\1\n<div>\2</div>\n\3', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(</p>|</div>)(\s*<head>.*?</head>.*?)(<head>|</div>|<div>)', r'\1\n<div>\2</div>\n\3', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(</p>|</div>)(\s*<head>.*?</head>.*?)(<head>|</div>|<div>)', r'\1\n<div>\2</div>\n\3', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(</p>|</div>)(\s*<head>.*?</head>.*?)(<head>|</div>|<div>)', r'\1\n<div>\2</div>\n\3', text, flags=re.DOTALL|re.IGNORECASE)
    """

    # Cleaning some <milestone />
    text = re.sub(r'(<div>\s*)<milestone />', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(</div>\s*)<milestone />', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(</head>\s*)<milestone />', r'\1', text, flags=re.DOTALL|re.IGNORECASE)

    # Setting some floatingTexts
    #text = re.sub(r'(<div(| [^>]*?)>((?!<div).)*</div>)(\s*<p)', r'<floatingText>\n<body>\n\1\n</body>\n</floatingText>\n\4', text, flags=re.DOTALL|re.IGNORECASE)

    #text = re.sub(r'(<div(|[^>]+?)>.*?</div>)(\s*<p)', r'<floatingText>\n<body>\n<div>\n\1\n</div>\n</body>\n</floatingText>\n\3', text, flags=re.DOTALL|re.IGNORECASE)
    
    # Floating Texts

    text = re.sub(r'<p(| [^>]+)>[\s\r\n]*</p>', r'', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'\n[ \t]+', r'\n', text, flags=re.IGNORECASE)
    text = re.sub(r'[\r\n]+', r'\r\n', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div>[\r?\n]*</div>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(<div>((?!<div>).)*</div>\r?\n)\Z', r'<!--\1-->', text, flags=re.DOTALL|re.IGNORECASE)
    

    text = re.sub(r'<div class="cita[0-9]*">(.*?)</div>', r'<quote>\1</quote>', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<p class="cita[0-9]*">(.*?</p>)', r'<quote>\n<p>\1</quote>', text, flags=re.DOTALL|re.IGNORECASE)

        
    text = re.sub(r'<br class="calibre[0-9]*" />', r'', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'(<p>—?. ?)<span class="palabra">(.*?)</span>', r'\1<seg rend="small">\2</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<p class="saltoinicio"><span class="inicial">(.*)</span><span class="palabra">(.*?)</span>', r'<p>\1\2', text, flags=re.IGNORECASE)
    text = re.sub(r'<p class="saltoinicio"><span class="inicial">(.*)</span>', r'<p>\1', text, flags=re.IGNORECASE)
    text = re.sub(r'<p>(.)<span>(.*)</span>', r'<p>\1\2', text, flags=re.IGNORECASE)
    text = re.sub(r'<span class="inicial">(.*)</span>', r'\1', text, flags=re.IGNORECASE)

    
    text = re.sub(r'(<head>.*?)<seg rend="(smallcaps|small)">(.*?)</seg>(.*?</head>)', r'\1\3\4', text, flags=re.DOTALL|re.IGNORECASE)
   
    text = re.sub(r'<div[^>]*?>\s*</div>', r'', text, flags=re.DOTALL|re.IGNORECASE)
        
    text = re.sub(r'<div class="tablacentro\d*">\s*<table class="text\d*">\s*<tr class="calibre\d*">\s*<td class="calibre\d*">(.*?)\s*</td>\s*</tr>\s*</table>\s*</div>', r'<lg>\1\n</lg>', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'<p class="traduccion">(.*?)</p>', r'<ab type="translation">\1</ab>', text, flags=re.IGNORECASE)

    #text = re.sub(r'<p class="centrado">(.*?)</p>', r'<head>\1</head>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="centrado\d*">(.*?)</p>', r'<ab>\1</ab>', text, flags=re.DOTALL|re.IGNORECASE)
    
    #text = re.sub(r'<blockquote class="calibre18">(.*?)</blockquote>', r'<floatingText>\n<body>\n\1\n</body>\n</floatingText>\n', text, flags=re.DOTALL|re.IGNORECASE)

    """
    #The next lines were used for 232, a theater-like novel
    
    text = re.sub(r'<p>(.*?</seg>)(\.\—.*?)</p>', r'<sp>\n<speaker>\1</speaker>\n<p>\2</p>\n</sp>', text, flags=re.IGNORECASE)
    """
    """
    #The next lines were used for 109, a theater-like novel
    text = re.sub(r'<p>(.*?</seg>\.)(.*?)</p>', r'<sp>\n<speaker>\1</speaker>\n<p>\2</p>\n</sp>', text, flags=re.IGNORECASE)
    text = re.sub(r'<p>(.*?</seg>)( +<seg rend="italic">.*?)</p>', r'<sp>\n<speaker>\1</speaker>\n<p>\2</p>\n</sp>', text, flags=re.IGNORECASE)
    text = re.sub(r'<seg rend="italic">(\(.*?)</seg>', r'<stage>\1</stage>', text, flags=re.IGNORECASE)
    """
    """
    #The next lines were used for 224, a theater-like novel
    text = re.sub(r'<p>(.<seg rend="small">.*?</seg>\.)(.*?)</p>', r'<sp>\n<speaker>\1</speaker>\n<p>\2</p>\n</sp>', text, flags=re.IGNORECASE)
    #text = re.sub(r'<p>(.*?</seg>)( +<seg rend="italic">.*?)</p>', r'<sp>\n<speaker>\1</speaker>\n<p>\2</p>\n</sp>', text, flags=re.IGNORECASE)
    text = re.sub(r'<seg rend="italic">(\(.*?)</seg>', r'<stage>\1</stage>', text, flags=re.IGNORECASE)
    """
    """
    # Code used for paradox rey
    text = re.sub(r'<div class="clear">\s*</div>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="banner\d*">(.*?)</p>', r'<ab>\1</ab>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="francesa\d*">(.*?)</p>', r'<ab>\1</ab>', text, flags=re.DOTALL|re.IGNORECASE)
    """
    """
    text = re.sub(r'<p class="personaje">(.*?)</p>\s*<p>(.*?)</p>', r'<sp>\n<speaker>\1</speaker>\n<p>\2</p>\n</sp>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<span class="descrip">(.*?)</span>', r'<stage>\1</stage>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="(?:descrip\d*|entrada|fin)">(.*?)</p>', r'<stage>\1</stage>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="cuadro">(.*?)</p>', r'<head>\1</head>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="descrip1">(.*?)</div>', r'<stage>\1</stage>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="puntos">.*?</div>', r'<milestone />', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="tablacentro">(.*?)</div>', r'<lg>\1</lg>', text, flags=re.DOTALL|re.IGNORECASE)
    """
    text = re.sub(r'<p class="decla">(.*?\. )(.*?)</p>', r'<sp>\n<speaker>\1</speaker>\n<p>\2</p>\n</sp>', text, flags=re.IGNORECASE)
    text = re.sub(r'<p class="(?:descrip|decla1)">(.*?)</p>', r'<stage>\1</stage>', text, flags=re.IGNORECASE)


    text = re.sub(r'(<seg\s+rend\s*=\s*"small(?:caps)?">)(.*?)(?=</seg>)', lambda m: m.group(1) + m.group(2).lower(), text)
    
    text = re.sub(r'(<seg\s+rend\s*=\s*"small(?:caps)?">)(.*?)(</seg>)', r'\2', text, flags=re.IGNORECASE)
    
    
    return text


def setDivs(text):
    """
    Setting the <div>s searching for the <ead>
    """

    # It deletes the <h1> and its next <p>
    text = re.sub(r'(\A.*?)(<head)', r'\1<div>\r\n\2', text, flags=re.DOTALL|re.IGNORECASE)
    
    # That closes the <div> of an <h2> and opens another one
    text = re.sub(r'(</p>|</ab>|</lg>|<milestone />|</floatingText>|</sp>|</stage>)\s*?(<head>)', r'\1\r\n</div>\r\n<div>\r\n\2', text, flags=re.DOTALL|re.IGNORECASE)

    return text
    
def lInLg(text):
    """
    It replaces some elements and its styles with TEI elements
    """
    while re.search(r'(<lg>)(((?!</lg>).)*?)<(/?)p>', text, flags=re.DOTALL|re.IGNORECASE) is not None:
        text = re.sub(r'(<lg>)(((?!</lg>).)*?)<(/?)p>', r'\1\2<\4l>', text, flags=re.DOTALL|re.IGNORECASE)
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
        
        #It replaces some HTML elements with TEI elements    
        content=replacingBasicElementsFromEpubLibre(content)
        
        content=setDivs(content)

        
        #We introduce the teiHeader
        content=settingTeiHeader(content)

        # It writes the result in the output folder

        content=lInLg(content)

     
            
            # It writes the result in the output folder
    
        with open (os.path.join("output", docFormatOut), "w", encoding="utf-8") as fout:
                fout.write(content)
        print(doc)
        print("Processed documents: ",i)
        i+=1

main()