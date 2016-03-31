__author__ = 'Daniel Schlör'
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import time
import urllib.parse as urlparse

def is_absolute(url):
     return bool(urlparse.urlparse(url).netloc)

errorPages = []

##################################################################################
# Extracts link to HTML view of book ("Leer obra")
# Input:    Landing page for Book
# Output:   Index page of book
#   i.e. http://www.cervantesvirtual.com/portales/pardo_bazan/obra/casualidad--0
##################################################################################
def getHtmlPage(url):
    nurl = None
    title = None
    retry_counter = 5
    while (retry_counter > 0):
        try:
            r = requests.get(url)
            link = r.text
            pattern = re.compile('<a href="([^"]*)".*Leer obra.*')
            title = BeautifulSoup(link).find_all('title')[0].get_text()
            nurl = pattern.findall(link)[0]
            if not is_absolute(nurl):       # dealing with relative paths
                nurl = urlparse.urljoin(url, nurl)
            retry_counter = 0
        except Exception as e:
            print("Error: (" + str(e) + ") Retrying... (" + str(retry_counter) + ")")
            retry_counter -= 1
            time.sleep(1)
    return (nurl, title)

#################################################################################################
# Extracts links to single HTML pages / chapters of book
#   (searching for <a href="*.html"> links)
# Input:    Index page of book
# Output:   Ordered Dictionary (by Pagenumber) with page-links
#   i.e. http://www.cervantesvirtual.com/portales/pardo_bazan/obra-visor-din/casualidad--0/html/
################################################################################################
def getPageUrls(htmlpageurl, generateSubsequalNumbers = True):
    time.sleep(1)
    retry_counter = 5
    while (retry_counter > 0):
        r = requests.get(htmlpageurl)
        anchors = BeautifulSoup(r.text).select('a[href*=".html"]')
        if len(anchors) == 0:
            print("Error: (No anchors found) Retrying... (" + str(retry_counter) + ")")
            retry_counter -= 1
            time.sleep(1)
        else:
            break
    regex = re.compile("(([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}_)([0-9]+)(.html))")
    urls = {}
    prefix = None
    suffix = None
    maxurl = -1
    for a in anchors:
        found = (regex.findall(a['href']))[0]
        if(len(found) > 2):
            prefix = found[1]
            suffix = found[3]
            url = found[0]
            if not is_absolute(found[0]):       # dealing with relative paths
                url = urlparse.urljoin(r.url, found[0])
                prefix = urlparse.urljoin(r.url, found[1])
            urls[int(found[2])] = url
            if int(found[2]) > maxurl:
                maxurl = int(found[2])

    o_urls = OrderedDict(sorted(urls.items()))
    if len(o_urls) < maxurl:
        print("WARNING: Found anchors are not subsequent!")
        print("\tTrying to guess anchors left out.")
        if generateSubsequalNumbers:
            o_urls = {}
            for i in range(1, maxurl + 1):
                o_urls[i] = prefix + str(i) + suffix
    return o_urls

###################################################################################
# Visits all pages in Dictionary and combines those to single Booktext HTML Page
# Input:    (Ordered) Dictionary with sub-Page-Links
#           Optional:   plaintext=True (default False)
#                            Remove all HTML specific non-text
# Output:   aggregated booktext
###################################################################################
def unitePages(o_urls, plaintext=False, extendIfIncomplete=True):
    booktext = ""
    retry_counter = 5
    nextpage = None
    hadNextPageErrorCtr = 0
    vals = list(o_urls.values())
    counter = 0
    while True:
        if counter < len(vals):
            url = vals[counter]
        elif nextpage is not None and extendIfIncomplete:
            url = nextpage
            hadNextPageErrorCtr += 1
        else:
            break

        counter += 1
        time.sleep(1)
        r = requests.get(url)
        code = r.status_code
        text = BeautifulSoup(r.text)
        while code != 200 and retry_counter > 0:
            print("Error: (HTTP " + str(code) + ") Retrying... (" + str(retry_counter) + ")")
            r = requests.get(url)
            code = r.status_code
            retry_counter -= 1
        text = BeautifulSoup(r.text)
        if code == 200:
            booktext = booktext + (text.get_text() if plaintext else r.text) + "\n"
        else:
            print("Error: Not for all pages valid text found.")
        anchors = text.select('img[alt="Siguiente"]')
        if len(anchors) > 0:
            nextpage = urlparse.urljoin(r.url, anchors[0].parent['href'])
        else:
            nextpage = None
    if hadNextPageErrorCtr > 0:
        print("WARNING! All indexed pages process but there were even more! [Indexed: " + str(len(vals)) + " Found: " + str(counter) + "]")
    return booktext, None

############################################
# Write booktext to file
# Input:    text:   Booktext
#           file:   Output file to write to
############################################
def write2file(text, file):
    f = open(file, 'w')
    f.write(text)
    f.close()


#####################################################
# Process extraction workflow for given Landing-page
# Input:    url to landing page for book
#####################################################
def meta2booktext(url):
    retry_counter = 3
    pageurls = None
    while (retry_counter > 0):
        htmllanding = getHtmlPage(url)
        print("Working on: \t" + url.replace("\n",""))
        if htmllanding[0] is None:
            retry_counter -= 1
            print("Error extracting HTML Index Page. Retrying... (" + str(retry_counter) + ")")
            continue
        print("Detected title:\t" + htmllanding[1])
        pageurls = getPageUrls(htmllanding[0])
        if len(pageurls) < 1:
            retry_counter -= 1
            print("Error finding subpages on HTML Index Page. Retrying... (" + str(retry_counter) + ")")
            continue
        else:
            break
    if pageurls is None or len(pageurls) < 1:
        print("Error finding subpages on HTML Index Page. Skipping page.")
        errorPages.append(url)
        return
    booktext = unitePages(pageurls)
    print("Found " + str(len(pageurls)) + " subpages.")
#    idp = re.compile("http://www.cervantesvirtual.com/nd/ark:/(\d+/[0-9a-z]+)")
    idp = re.compile(".*obra/([^/]+)")
    id = (idp.findall(url)[0]).replace("/", "-").replace("\n", "")
    write2file(booktext[0], id + ".html")


###############################################
# Batch process workflow on all links in file
# Input:    file with landing pages
###############################################
def batch(file):
    f = open(file, 'r')
    for line in f:
        meta2booktext(line)

    if len(errorPages) > 0:
        print("Error with following urls:")
        errors = ""
        for url in errorPages:
            errors = errors + url + "\n"
            print("\t" + url)
        write2file(errors, "errors.txt")
#batch('cv.txt')

meta2booktext("http://www.cervantesvirtual.com/obra/obras--0/")