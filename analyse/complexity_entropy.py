"""
computes normalized Shannon entropy and a statistical complexity measure called
MPR. Implementation is based on the article "Cancer Biomarker Discovery"
by Beretta / Moscato in Plosone* (see section Materials and Methods) and
Rosso, Craig, Moscato: "Shakespeare and other English Renaissance authors" in
Physica A 388 (2009) 916-926.
The use of the complexity measure based on jensen shannon divergence is proposed
by Martin, Plastino, Russo, therefore the name ComplMPR
Beware: the numbers given in the Plosone paper for the jsd are wrong, because the
authors used the natural log to compute the results instead of the log2, which is
used in the formula in the paper.

todo:
    - still cannot replicate the complexity measure for the gene expression files
      (see plosone article). Check with Hugh whether Pave is calculated correctly
      (jsd should work fine)
    - fix bug with using the file with the wordcounts; getting different results
_____
*http://www.plosone.org/article/info:doi/10.1371/journal.pone.0012262

"""

import glob
import os
import math
import pandas as pd
import datetime
import re
from collections import Counter
import csv

##########################################################################
#  configuration
##########################################################################
#where to find the corpus
subdir = "txt"

#number of words to use from the wordlist
#set to 0 to use all
mfwords = 5000

#use existing wordlist
use_wordlist = False

#switch to extract only a sample
set_limit = True

#sample size
limit = 20000

#all words in lower case?
lower_case = True

#name of the file where the complete wordlist is saved
corpuswords = "data_corpuswords.csv"

#use filenames as labels in plot
filenames_labels = True

#use groups to color output and in legend (alternative to filename labels)
#groups = True

#label size
#label_size = 8

#heading of the plotted diagram
#heading = "Complexity and Entropy in German novels around 1890"

#save results to file results.csv
save_results = True

#debug
debug = False

#defines word boundaries for the tokenization
#yes, this could be done more sophisticated using nltk
#and no, you don't want to install nltk 3.0alpha with python 3 ;-)
pattern = re.compile("\W")

##########################################################################
#  functions
##########################################################################
def process_files(encoding="utf-8"):
    """
    preprocessing all files ending with *.txt in corpus subdir
    all files are tokenized
    a table of all word and their freq in all texts is created
    """
    filelist = glob.glob(subdir + os.sep + "*.txt")
    corpus_words = pd.DataFrame()
    for file in filelist:
        df = tokenize_file(file,encoding)
        corpus_words = pd.concat([corpus_words,df],axis=1)
    return corpus_words


def tokenize_file (filename,encoding):
    """
    tokenizes file and returns an unordered pandas.DataFrame
    containing the words and frequencies
    standard encoding = utf-8
    """
    all_words = {}

    #read file, tokenize it, count words
    read_text_length = 0
    with open (filename,"r",encoding=encoding) as filein:   #encoding="utf-8"
        print ("processing " + os.path.basename(filename))
        for line in filein:
            if set_limit == True:
                if read_text_length > limit:
                    break
                else:
                    read_text_length += len(line)
            words = regex_tokenizer (line)
            for w in words:
                if lower_case == True:
                    w = w.lower()
                if w not in all_words.keys():
                    all_words[w] = 1
                else:
                    all_words[w] += 1
    filename = os.path.basename(filename)
    return pd.DataFrame(pd.Series(all_words),columns=[filename])


def regex_tokenizer (line):
    """
    regex based tokenizer using unicode based whitespace
    information
    the pattern is defined above to avoid repeated compilation
    """
    words = pattern.split(line)
    while "" in words:
        words.remove("")
    return words


def save_file(corpus_words):
    """
    saves wordlists to file
    using global var save_file
    """
    print ("Saving wordlist to file " + corpuswords)
    corpus_words.to_csv(corpuswords, encoding="utf-8",na_rep=0,quoting=csv.QUOTE_NONNUMERIC)


def read_corpus():
    """
    reads wordlist from file
    """
    return pd.read_csv(corpuswords,encoding="utf-8",index_col=0)


def preprocess_mfw_table (corpus):
    """
    sorts the table containing the frequency lists
    by the sum of all word freq
    returns the corpus list shortened to the most frequent words
    number defined by mfwords
    """
    nr = []
    #cols = corpus.columns
    for i in corpus.index:
        nr += [corpus.loc[i].sum()]
    su = pd.Series(nr,index=corpus.index,name="sum")


    corpus = corpus.fillna(0)   
    corpus = corpus.loc[corpus.sum(axis=1).sort_values(inplace=False, ascending=False).index] 
    #print(corpus)
 
    #slice only mfwords from total list
    if mfwords != 0:
        corpus = corpus[:mfwords]
    return corpus  #

def JSDvsEntropy (corpus_words):
    entropies = [] #stores the entropies of all texts
    jsds = [] #stores all distance measures
    #compute Pave, the average probablity distribution, which is used
    #as reference in the jcd for each text

    Pave = p_ave(corpus_words)

    for text in corpus_words.columns:
        text_words = corpus_words[text]
        p_text_words = prob (text_words)
        #compute for all texts the normalized Shannon entropy (step a)
        entropy = normalized_entropy(p_text_words)
        entropies += [entropy]
        #compute the jsd from a texts to Pave (step b i)

        jsd_res = jsd(p_text_words,Pave)
        jsds += [jsd_res]
        if debug==True:
            print (text + ": jsd: " + str(jsd_res) + "  nse: " + str(entropy) + " -- " + text)
    entropies = pd.Series(entropies,name="entropy",index=corpus_words.columns)
    #print(entropies)
    jsds  = pd.Series(jsds,name="jsd",index=corpus_words.columns)   
    results = pd.concat([jsds,entropies],axis=1)
    results.reset_index(level=0, inplace=True)
    results.rename(columns={"index": "idno"}, inplace=True)
    results.replace(".txt", "", regex=True, inplace=True)
    print(results)
    return results




#reads in all files and tokenizes them and creates a wordfreq. list in a dataframe
def ComplMPR (corpus_words):
    """
    it consists of the product of:
      a) the normalized Shannon entropy
      b) and a disequilibrium, a fixed reference state, which is computed as the product of
           i) the Jensen-Shannon divergence and
          ii) a normalization constant equal to the inverse of maximum possible values
              of jsd
    this function assumes that the complete wordlist DataFrame has been already
    truncated to the smaller set you want to actually use for the computation
    therefore corpus_words.index contains all words to be computed on
    returns a list with the normalized entropies and a list with the complexity measures
    """
#    jsd_all = []  #stores all jcd  for debugging
    entropies = [] #stores the entropies of all texts
    complMPR = [] #stores all complexity measures
    jsd_res = 0

    #calculate the normalization constant (step b ii)
    N = len(corpus_words.index)
    Q_0 = q_0(N)
    if debug==True:
        print("N: " + str(N) + "\nQ_0: " + str(Q_0)  )

    for text in corpus_words.columns:
        text_words = corpus_words[text]
        p_text_words = prob (text_words)
        #compute for all texts the normalized Shannon entropy (step a)
        entropy = normalized_entropy(p_text_words)
        entropies += [entropy]
        #compute the jsd from a text to Pe
        jsd_res = jsd(p_text_words,p_eq(p_text_words))

        complMPR += [Q_0 * jsd_res * entropy]
        if debug==True:
            print (text + ": jsd: " + str(jsd_res) + "  nse: " + str(entropy) + " -- " + text)
    entropies = pd.Series(entropies,name="entropy",index=corpus_words.columns)
    complMPR  = pd.Series(complMPR,name="complexity",index=corpus_words.columns)
    return pd.concat([entropies,complMPR],axis=1)

#reads in all files and tokenizes them and creates a wordfreq. list in a dataframe
def ComplM (corpus_words):
    """
    it consists of the product of:
      a) the normalized Shannon entropy
      b) and the Jensen-Shannon divergence of one text to the average (Pave)

    this function assumes that the complete wordlist DataFrame has been already
    truncated to the smaller set you want to actually use for the computation
    therefore corpus_words.index contains all words to be computed on
    returns a list with the normalized entropies and a list with the complexity measures
    """
#    jsd_all = []  #stores all jcd  for debugging
    entropies = [] #stores the entropies of all texts
    complM = [] #stores all complexity measures
    jsd_res = 0


    #compute Pave, the average probablity distribution, which is used
    #as reference in the jcd for each text
    Pave = p_ave(corpus_words)

    for text in corpus_words.columns:
        text_words = corpus_words[text]
        p_text_words = prob (text_words)
        #compute for all texts the normalized Shannon entropy (step a)
        entropy = normalized_entropy(p_text_words)
        entropies += [entropy]
        #compute the jsd from a texts to Pave (step b i)

        jsd_res = jsd(p_text_words,Pave)

        complM += [jsd_res * entropy]
        if debug==True:
            print (text + ": jsd: " + str(jsd_res) + "  nse: " + str(entropy) + " -- " + text)
    entropies = pd.Series(entropies,name="entropy",index=corpus_words.columns)
    complM  = pd.Series(complM,name="complexity",index=corpus_words.columns)
    return pd.concat([entropies,complM],axis=1)


#computes jensen-shannon divergence for 2 lists in form of pandas.Series
#return one value
def jsd (p_1,p_2):
    """
    computes the Jensen Shannon divergence between two lists of values
    see Regina Berretta1,2, Pablo Moscato: Cancer Biomarker Discovery:
    The Entropic Hallmark. Plos One August 18, 2010, for details on the formula.
    The values in this text don't match my results using the jsd and also
    not 2 other implementations of the jsd (mystery solved: the formula in the
    paper uses log2 to compute entropy while the results of the paper are
    really computed using the natural log.
    >>> jsd(prob(pd.Series([2,2,2,2,2])),prob(pd.Series([2,2,2,2,2])))
    0.0
    >>> jsd(prob(pd.Series([2,2,2,2,2])),prob(pd.Series([5,2,5,1,3])))
    0.035851483945529505
    >>> jsd(prob(pd.Series([4,3,2,1,0.1])),prob(pd.Series([2,2,2,2,2])))
    0.082684827683680462
    >>> jsd(prob(pd.Series([4,3,2,1,0.1])),prob(pd.Series([5,2,5,1,3])))
    0.077848851295847954
    """
    J1 = entropy ((p_1 + p_2) / 2)
    J2 = (entropy(p_1) + entropy(p_2)) / 2
    if debug == True:
        print ("J1: " + str(J1) + "  J2: " + str(J2))
    JS = J1 - J2
    if debug == True:
        print ("jsd: " + str(JS))
    return JS


def prob (values):
    """
    computes probabilites by dividing all values through the sum of all values.
    returns a pandas.Series containing the probablities
    Usage:
    >>> prob(pd.Series([1,2,3]))
    0    0.166667
    1    0.333333
    2    0.500000
    dtype: float64
    """
    if not isinstance(values,pd.core.series.Series):
        values = pd.Series(values)
    return (values / values.sum())

def p_eq(series):
    """
    Computes the equilibrium
    >>> p_eq(pd.Series([3,2,1,3,2,1]))

    """
    l = len (series)
    return pd.Series([1/l]*l,index=series.index)

def p_ave (df):
    """
    Computes p ave, that is the average probability for each word over all texts
    #df = {"one" : pd.Series([3,5],index=['a','b']), "two": pd.Series([1,4],index=['a','c']),"three": pd.Series([7,2],index=['b','c'])}
    >>> df = pd.concat([pd.Series([3,5],index=['a','b'],name="one"),pd.Series([1,4],index=['a','c'],name="two"),pd.Series([7,2],index=['b','c'],name="three")],axis=1)
    >>> p_ave(df)
    a    0.181818
    b    0.545455
    c    0.272727
    dtype: float64
    """

    df = df.fillna(0)
    p = []
    for row in df.index:
        p +=  [(df.loc[row].sum() / df.loc[row].count())]
    p_ave = pd.Series(p,index=df.index)
    #get the ratio = probabilities
    p_ave = prob(p_ave)
    return p_ave



def entropy (values):
    """
    computes the Shannon entropy
     S(E) = minus sum of (p(i) * log(p(i)))
    where p is the probability of the event x
    so first one has to compute the probability of the events
    and then feed this list to entropy
    >>> entropy(prob(pd.Series([2,2,2,2])))
    1.3862943611198906
    >>> entropy(prob(pd.Series([1,2,3,4])))
    1.2798542258336676
    """
    #apply it to all values
    values = values.apply(help_se)
    return - values.sum()


def help_se (value):
    """
    small function to calculate the basis value for Shannon Entropy
    maybe it is better to switch to math.log2 here?
    and actually this is the reason the results published in thr paper by
    Regina Berretta1,2, Pablo Moscato are wrong
    """
    if value == 0:
        return 0
    else:
        return value * math.log(value)


#unused function, useful for debugging the entropy func
#see http://rosettacode.org/wiki/Entropy#Python
def entropy_S(s):
    """
    computes entropy on a string
    >>> entropy_S("1223334444")
    1.8464393446710154
    >>> entropy_S("11223344")
    2.0

    """
    p, lns = Counter(s), float(len(s))
    return -sum( count/lns * math.log(count/lns, 2) for count in p.values())


def normalized_entropy (values):
    """calculates Normalized Shannon Entropy
    assumes values are not raw values but already probabilities
    >>> normalized_entropy(prob([5,2,5,1,3]))
    0.9158830010682758
    >>> normalized_entropy(prob([2,2,2,2,2]))
    1.0000000000000002
    >>> normalized_entropy(prob([4,3,2,1,0.1]))
    0.8218574117493731
    """

    if not isinstance(values,pd.core.series.Series):
        values = pd.Series(values)

    #apply it to all values
    values = values.apply(help_se)
    #do the rest of the formula
    result = - values.sum() / math.log(values.count())
    return result


#helper function to compute Q_0, the normalization constant which is only
#dependent on N
#formula not given in the Plosone paper but in the Physica A

def q_0 (N):
    """
    >>> q_0(10)
    1.9025971948407798
    """
    if N != 0:
        q = -2 * (( ((N + 1) / N ) * math.log (N+1)) - 2 * math.log(2*N) + math.log(N))**-1
    else:
        print ("Warning: N: 0 --doesn't make sense")
        q = 1
    return q

def testme():
    groupnames = {}
    with open (subdir + os.sep + "groups.csv","r",encoding="utf-8") as filein:
        for line in filein:
            (text,group) = line.split("\t")
            groupnames[text] = group
    for i in groupnames.keys():
        print (i + " : " + groupnames[i])


def file_name (filename):
    """
    small helper function to get rid of the extension
    and shorten the name and the the title
    """
    tf = []
    ntitle = ""
    (author,title) = filename.split("_")
    if ",-" in author:
        (author,firstname) = author.split(",-")
    if ".txt" in title:
        title = title[:-4]
    if " " in title:
        tf = title.split(" ")
        for w in tf:
            if w not in ["Der","Das","Die","Ein","Eine","Und"]:
                ntitle += w
                title = ntitle
                break
    return author + "_" + title

def date_time():
    dt = datetime.datetime.now()
    return dt.strftime("%Y-%m-%d_%H-%M-%S")

##########################################################################
#  main
##########################################################################

def main():
    if use_wordlist == False:
        corpus = process_files(encoding="utf-8")
        save_file(corpus)
    else:
        corpus = read_corpus()
    corpus = preprocess_mfw_table(corpus)
    results =  JSDvsEntropy(corpus)
    if save_results == True:
        results.to_csv("entropy_results.csv")
    #plot2(results,"jsdentr")

main()

