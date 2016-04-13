#!/usr/bin/env python3

import bibtexparser
import os
import re
import sys
import string
import shutil
#import subprocess

def remove_ce(mystring):
    cleanedstring = re.sub(r"\\ce", "", mystring)
    return(cleanedstring)    

def cleantitle(title):
    title = remove_ce(title)
    title = re.sub(r" ", "_", title)
    title = re.sub(r"ä", "ae", title)
    title = re.sub(r"ö", "oe", title)
    title = re.sub(r"ü", "ue", title)
    title = re.sub(r"ß", "ss", title)
    title = re.sub(r"Ä", "Ae", title)
    title = re.sub(r"Ö", "Oe", title)
    title = re.sub(r"Ü", "Ue", title)
    title = re.sub(r"µ", "mu", title)
    
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    validtitle = ''
    for c in title:
        if (c in valid_chars):
            validtitle = '%s%s'%(validtitle,c)
    return(validtitle)

def newfilename(myitem, file_extension):
    basefilename = "%s-%s"%(myitem["ID"],cleantitle(myitem["title"]))
    print(basefilename)    
    filename = "%s%s"%(basefilename, file_extension.lower())
    return(filename)

def isfilename(teststring):
    # return true, if only numbers and characters
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    onlyvalidchar = True    
    for c in teststring:
        onlyvalidchar = onlyvalidchar and (c in valid_chars)
    return onlyvalidchar

    
if __name__ == "__main__":
    mybibfile = sys.argv[1]
    mynewbibfile = '%s-new.bib'%mybibfile
    myoutputfolder = sys.argv[2]
    
    shutil.copy2(mybibfile, mynewbibfile)
    
    with open(mybibfile) as bibtex_file:
        bibtex_str = bibtex_file.read()
    
    bib_database = bibtexparser.loads(bibtex_str)
    #print(bib_database.entries)
    
    for item in bib_database.entries:
        if item["ENTRYTYPE"]=='article':
            print(item["ID"])
    
            if 'file' in item:
                fullpathtopaper = item["file"].split(":")[1]
                filename, file_extension = os.path.splitext(fullpathtopaper)
                #print(filename, file_extension)
                print("old filename: %s"%fullpathtopaper)
                mynewfilename = newfilename(item, file_extension)
                print("new filename: %s"%mynewfilename)
                                
                if os.path.isfile(fullpathtopaper):
                    shutil.copy2(fullpathtopaper, ('%s/%s'%(myoutputfolder,mynewfilename)))

                cmd = "sed -i 's/%s/%s/g' %s"%(fullpathtopaper.replace('/','\/'),mynewfilename.replace('/','\/'),mynewbibfile)
                print('cmd: ', cmd)                
                #os.system(cmd)
                
            else:
                print("No file.")
    

        
#            if item["title"]:
                #print(item["title"])
#            else:
#                print("Warning: Title is missing!")
    #,  item["title"], item["file"])
    
