#!/usr/bin/env python3

import bibtexparser
import os
import re
import sys
import string
import shutil
import unidecode

def remove_ce(mystring):
    cleanedstring = re.sub(r"\\ce", "", mystring)
    return(cleanedstring)    

def cleantitle(title):
    title = remove_ce(title)
    title = re.sub(r"$\mu$", "u", title)
    title = re.sub(r" ", "_", title)
    title = re.sub(r"ä", "ae", title)
    title = re.sub(r"ö", "oe", title)
    title = re.sub(r"ü", "ue", title)
    title = re.sub(r"ß", "ss", title)
    title = re.sub(r"Ä", "Ae", title)
    title = re.sub(r"Ö", "Oe", title)
    title = re.sub(r"Ü", "Ue", title)
    title = unidecode.unidecode(title)
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    validtitle = ''
    for c in title:
        if (c in valid_chars):
            validtitle = '%s%s'%(validtitle,c)
    return(validtitle)

def newfilename(myitem, file_extension):
    basefilename = "%s-%s"%(myitem["ID"],cleantitle(myitem["title"]))
    filename = "%s%s"%(basefilename, file_extension.lower())
    return(filename)

def isfilename(teststring):
    # return true, if only numbers and characters
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    onlyvalidchar = True    
    for c in teststring:
        onlyvalidchar = onlyvalidchar and (c in valid_chars)
    return onlyvalidchar


def replacepath(bibfile, oldpath, newpath):
    """search and replace oldpath with newpath in a .bib file
    """
    filedata = None
    with open(bibfile, 'r') as infile:
        filedata = infile.read()
    infile.close()
    
    # Replace the target string
    filedata = filedata.replace(oldpath, newpath)
    
    # Write the file out again
    with open(bibfile, 'w') as outfile:
        outfile.write(filedata)
    outfile.close()        
  
        
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
                oldpath= item["file"].split(":")[1]
                filename, file_extension = os.path.splitext(oldpath)
                #print(filename, file_extension)
                print("old filename: %s"%oldpath)
                newpath = '%s%s'%(myoutputfolder,newfilename(item, file_extension))
                print("new filename: %s"%newpath)
                if (oldpath == newpath):
                    print("III: File already renamed. Do nothing.")
                else:
                    if os.path.isfile(oldpath):
                        # shutil.copy2(oldpath, newpath)
                        shutil.move(oldpath, newpath)
                        replacepath(mybibfile, oldpath, newpath)
                    else:
                        print("EEE: File not found!")
    
    
