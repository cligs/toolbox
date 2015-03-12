mallet2wordle.py
================

Transform MALLET output for visualization with wordle.net.

## Remarks

* Takes as input the MALLET output file containing rows of topic, word, weight information.
* You will have to ask MALLET to output this file using the "--topic-word-weights-file FILENAME" option.
* Produces as output a plain text file containing, for each topic, the top-100 words with their relative score.
* Paste this output, for the topic you are interested in, into the "advanced" wordle page: http://www.wordle.net/advanced
* This script will work best with Python3. You need to have numpy and pandas installed.
* The sample file included in the toolbox repo comes from a collection of 376 French plays from theatre-classique.fr.
