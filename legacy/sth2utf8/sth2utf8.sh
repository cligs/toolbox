#!/bin/bash

# sth2utf8.sh

## Bash file for converting files from ISO-8859-15 to UTF-8. 
## This file could be anywhere on the system where you can find it.
## Set the path in FILES to the folder in which the input files. 
## Run this file from the terminal using: bash sth2utf8.sh


FILES=/home/christof/repos/clgs/toolbox/sth2utf8/sth/*.xml

for file in $FILES
 do iconv -f iso-8859-15 -t utf-8 $file > $file.utf8; done
