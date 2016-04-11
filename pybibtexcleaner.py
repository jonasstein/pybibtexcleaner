#!/usr/bin/env python3

import bibtexparser
import os.path
import re
import argparse
import sys

def remove_ce(mystring):
    #regex = re.compile(r"ce", re.IGNORECASE)    
    cleanedstring = re.sub(r"\\ce", "", mystring)
    return(cleanedstring)    

def cleantitle(title):
    title = remove_ce(title)
    title = re.sub(r"{", "", title)
    title = re.sub(r"}", "", title)
    mycleantitle = re.sub(r" ", "_", title)
    return(mycleantitle)

def newfilename(myitem):
    filename = "%s-%s"%(myitem["ID"],cleantitle(myitem["title"]))
    return(filename)

with open(sys.argv[1]) as bibtex_file:
    bibtex_str = bibtex_file.read()

bib_database = bibtexparser.loads(bibtex_str)
#print(bib_database.entries)

for item in bib_database.entries:
    if item["ENTRYTYPE"]=='article':
        print(item["ID"])

        if 'file' in item:
        
            filename = item["file"].split(":")[1]
            print("new filename: %s"%newfilename(item))
            ## If newfilename is alphanum only, then rename 
            #if os.path.isfile(filename):
            #    print("**Found:   ", filename)
            #else:    
            #    print("**Missing: ", filename)
        
        else:
            print("No file.")


        
#            if item["title"]:
                #print(item["title"])
#            else:
#                print("Warning: Title is missing!")
    #,  item["title"], item["file"])
    
