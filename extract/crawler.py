# -*- coding: utf-8 -*-
"""
This script takes different sites and save them in a single file
"""

import urllib.request

def cv(list_urls, file_name, output_folder, output_format="html"):
    """
    This function is the only real one. It takes a list of URLs, the name we want for the file, the output and a format 
    For example:
from toolbox.extract import crawler
list_urls = ["http://www.cervantesvirtual.com/obra-visor-din/novela-i--0/html/000df08c-82b2-11df-acc7-002185ce6064_1.html/","http://www.cervantesvirtual.com/obra-visor-din/novela-i--0/html/000df08c-82b2-11df-acc7-002185ce6064_2.html/","http://www.cervantesvirtual.com/obra-visor-din/novela-i--0/html/000df08c-82b2-11df-acc7-002185ce6064_3.html/","http://www.cervantesvirtual.com/obra-visor-din/novela-i--0/html/000df08c-82b2-11df-acc7-002185ce6064_4.html/","http://www.cervantesvirtual.com/obra-visor-din/novela-i--0/html/000df08c-82b2-11df-acc7-002185ce6064_5.html/","http://www.cervantesvirtual.com/obra-visor-din/novela-i--0/html/000df08c-82b2-11df-acc7-002185ce6064_6.html/","http://www.cervantesvirtual.com/obra-visor-din/novela-i--0/html/000df08c-82b2-11df-acc7-002185ce6064_7.html/","http://www.cervantesvirtual.com/obra-visor-din/novela-i--0/html/000df08c-82b2-11df-acc7-002185ce6064_8.html/","http://www.cervantesvirtual.com/obra-visor-din/novela-i--0/html/000df08c-82b2-11df-acc7-002185ce6064_9.html/","http://www.cervantesvirtual.com/obra-visor-din/novela-i--0/html/000df08c-82b2-11df-acc7-002185ce6064_10.html/","http://www.cervantesvirtual.com/obra-visor-din/novela-i--0/html/000df08c-82b2-11df-acc7-002185ce6064_11.html/",]
file_name = "lanza1"
output_folder = "/home/jose/cligs/ne/import/"
content = crawler.cv(list_urls, file_name, output_folder)
        
    """
    opener = urllib.request.FancyURLopener({})
    content_total = ""
    for url in list_urls:
        f = opener.open(url)
        content = f.read()
        content = content.decode('utf-8')
        content_total = content_total + content
    text_file = open(output_folder+file_name+"."+output_format, "w")
    text_file.write(content_total)
    text_file.close()
    return content
