toolbox
=======

## 
>ARRAS should not be thought of as a black box into which one inserts a text along with a set of commands and out of which one receives a completed analysis. A better analogy is a toolbox containing a set of tools, each designed for a particular task. The ARRAS design always presumes a human inquirer at the center. This ARRAS amplifies, rather than replaces, specific perceptual and cognitive functions. (John B. Smith, "A New Environment for Literary Analysis", *Perspectives in Computing* 4.2/3, 1984)

## What is the toolbox?

The toolbox is a collection of small work-in-progress scripts and code snippets for text processing produced by CLiGS.

Note that all functions are designed for Python 3 and are experimental in nature and quality. Each folder contains one or several Python scripts and some sample texts for testing. Currently, we are transitioning towards the toolbox as a module (see below). 

## Experimental feature: toolbox as module

This allows using the scripts as a repo-based module. The basic idea is that you clone the toolbox repository from GitHub and add the path to the folder containing the toolbox to your Python sys.path (using the script "activate_toolbox.py" which is included here). Then, you can import modules and submodules from the toolbox in your custom text processing scripts anywhere on your computer and use the functions provided in the toolbox. You may want to create your own branch of the toolbox to customize the functions as necessary. 

## Requirements

* pandas
* numpy
* requests
* lxml
* ...

## Module structure

In order to use the module efficiently, you need to know which submodules are included and which functions are included in each submodule. The following is intended as a quick overview, please see the submodules themselves for details. 

* extract.py
    * read_tei5
    * read_tei4
    * get_metadata
    * get_metadataP4
* crawl.py
    * crawl_tc
    * convert_encoding
* check_quality
    * spellchecking.py
        * check_collection
        * correct_words
    * validate_tei.py
        * validate_tei
    * elements_used.py
* annotate
    * use_heideltime.py
        * apply_ht

To get more information about a submodule, especially what each function does and which parameters they take, just use the usual help command in Python, for example: 

```
help(extract)
```
or
```
help(extract.read_tei5)
```


## Example

If you want to read text from a TEI P5 file, you could use the following import statement and function call in your script: 

```
from toolbox import extract

extract.read_tei5("/folder/with/tei/files/", "/folder/for/text/files", "bodytext")            
```
