# -*- coding: utf-8 -*-
#This document is meant to be used with the Plugin "Python Script" for Notepad++: http://npppythonscript.sourceforge.net/
#It works on the document that is opened in Notepad++, that is why the python script doesn't load or save any document
#The names of the class follow the names of the ePUBs from Clásicos Hispánicos (www.clasicoshispanicos.com)

#########Changes on !!!#########
editor.rereplace(r"head>", r"h2>")
editor.rereplace(r"<lg>", r"<div class=\"poem\">")
editor.rereplace(r"</lg>", r"</div>")
editor.rereplace(r"<l>", r"<p class=\"otroverso\">")
editor.rereplace(r"</l>", r"</p>")


editor.rereplace(r"", r"")