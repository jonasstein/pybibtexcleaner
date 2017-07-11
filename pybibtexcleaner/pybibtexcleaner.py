#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Jonas Stein
License: GPL-3
Version: 1.0.2
"""

import bibtexparser
import os
import re
import sys
import string
import shutil
import unidecode
import configparser


def remove_ce(mystring):
    cleanedstring = re.sub(r"\\ce", "", mystring)
    return(cleanedstring)


def cleantitle(title):
    """First substitute common non ascii characters,
    then return all ascii letter and numbers of the string
    """
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
            validtitle = '%s%s' % (validtitle, c)
    return(validtitle)


def newfilename(myitem, file_extension):
    basefilename = "%s-%s" % (myitem["ID"], cleantitle(myitem["title"]))
    filename = "%s%s" % (basefilename, file_extension.lower())
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


def backupfile(thefilename):
    """store a copy in filename_ISODATE.pybak
    """
    thebackupfilename = '%s.pybak' % thefilename
    shutil.copy2(thefilename, thebackupfilename)
    return(thebackupfilename)


def printLog(messagetype, message, beVerbose):

    if beVerbose:
        print("%s%s%s: %s" % (messagetype, messagetype, messagetype, message))
    else:
        if not (messagetype == "I"):
            print("%s%s%s: %s" %
                  (messagetype, messagetype, messagetype, message))


def fixJabRefsRelativePaths(bibfileToFix, relPath):
    """ replace file        = {:inserted/ with full path
    """
    replacepath(
        bibfileToFix,
        "file        = {:inserted/", "file        = {:%sinserted/" % relPath)


if __name__ == "__main__":
    configFileName = 'pybibtexcleaner.ini'
    justSimulate = False  # True
    verboseLog = False  # True

    if os.path.isfile(configFileName):
        config = configparser.ConfigParser()
        config.read(configFileName)
    else:
        sys.exit("Error: Configuration %s not found! Stop execution." %
                 configFileName)

    mybibfile = config['PATHS']['bibfileInput']
    printLog("I", "read bibtex database %s" % mybibfile, verboseLog)

    fixJabRefsRelativePaths(mybibfile, config['PATHS'][
                            'relativePathToInserted'])

    if (~justSimulate):
        myBibfileBackup = backupfile(mybibfile)

    with open(myBibfileBackup) as bibtex_file:
        bibtex_str = bibtex_file.read()

    bib_database = bibtexparser.loads(bibtex_str)
    mydocumentsfolder = config['PATHS']['documentsFolder']

    for item in bib_database.entries:
        if item["ENTRYTYPE"] == 'article':
            printLog("=", "Processing: %s" % item["ID"], verboseLog)

            if 'file' in item:
                oldpath = item["file"].split(":")[1]

                filename, file_extension = os.path.splitext(oldpath)
                newpath = '%s%s' % (mydocumentsfolder,
                                    newfilename(item, file_extension))

                if (oldpath == newpath):
                    printLog("I", "old filename: %s" % oldpath, verboseLog)
                    printLog("I", "new filename: %s" % newpath, verboseLog)
                    printLog("I", "File already renamed. Do nothing.",
                             verboseLog)

                else:
                    if os.path.isfile(oldpath):
                        if (justSimulate):
                            printLog("W", "Simulation Mode: mv %s %s" %
                                     (oldpath, newpath), verboseLog)

                        else:
                            shutil.move(oldpath, newpath)
                            replacepath(mybibfile, oldpath, newpath)
                    else:
                        printLog("E", "At key %s file not found: %s" %
                                 (item["ID"], oldpath), verboseLog)
                        # print("""find . -name "%s*" -exec mv '{}' %s \;
                        # """%(item["ID"],oldpath))
