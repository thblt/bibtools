"""
bibdesk2jabref.py - Converts BibDesk's file associations to JabRef's
                    File/URL fields.

This script assumes that: 

- The relative path of each associated file is valid according to the
  .bib file's current location. For extra safety, it will fail if a
  linked file does not exist.

- Some weirdness in the way the plist is decoded will be
  consistent. Use print() to look it out: lots of unparsed binary
  data, and the relative path in the middle of a plist.

"""

import os, sys
from itertools import count
from bibtexparser import load as bt_load
from biplist import * # Python stdlib's plistlib fails to parse
                      # BibDesk's binary plist files. I don't know why
                      # (and I don't really care). This one works.
from base64 import b64decode

if len(sys.argv) != 2:
    print("Usage:\n\t{0} file.bib".format(sys.argv[0]))
    exit(-1)

jabrefFormats = { # a dictionary associating lowercase extensions to JabRef's formats
    "epub": "ePUB",
    "html": "URL",
    "jpeg": "JPG image",
    "jpg": "JPG image",
    "pdf": "PDF"
    }

skipFields = (
        "date-added",    # BibDesk extension
        "date-modified", # BibDesk extension
        "ENTRYTYPE",     # Created by bibtexparser
        "ID",            # Created by bibtexparser
        "_type",         # Used by the present script to hold an entry's BibTeX type.
        "local-url"      # Don't know why there are still some of these.
)

filePath = sys.argv[1]
basePath = os.path.split(filePath)[0]

with open(filePath, 'r') as inputFile:
    refs = bt_load(inputFile)
    output = dict()
    for ref in refs.entries:
        entryFiles = []
        entryUrls = []
        entryDoi = None
        refId = ref["ID"]
    # Process file associations
        for i in count(1,1):
            fieldName = "bdsk-file-{0}".format(i)
            if fieldName in ref:
                try:
                    data = readPlistFromString(b64decode(ref[fieldName]))
                    relPath = data["$objects"][4] # I don't know why either. But it works (on my files anyway)
                    # This below will obviously fail if the extension isn't
                    # recognized. This is Good and Expected Behavior
                    # (although failing nicely may be cool)
                    format = jabrefFormats[os.path.splitext(relPath)[1][1:].lower()] 
                    if not os.path.exists(os.path.join(basePath, relPath)):
                        print("Error: {0} doesn't exist (expected from field {1} in {2}).".format(relPath, fieldName, refId))
                        exit(-1)
                    entryFiles.append((relPath, format))
                    del ref[fieldName]
                except Exception as e:
                    print(e)
                    exit(-1)
            else:
                break

        # Process URLs
        for i in count(1,1):
            fieldName = "bdsk-url-{0}".format(i)
            if fieldName in ref:
                url = ref[fieldName]
                # This if block is a custom hack due to some old
                # import I can't remember of, which added DOI
                # URLs. You may want to remove it.
                if url.startswith("http://dx.doi.org/"):
                       entryDoi = url[18:]
                       if ("doi" in ref) and (ref["doi"] != entryDoi):
                               print("Error: DOI url doesn't match existing doi field in {0}.".format(refId))
                               exit(-1)
                        
                else:
                       entryUrls.append(ref[fieldName])
                del ref[fieldName]
            else:
                break
        
        # Last sanity checks
        if len(entryUrls) > 1:
                print("Error: More than one URLs on {0}, and I know no syntax for that.".format(refId))
                exit(-1)
        
        if (len(entryUrls) == 1) and ("url" in ref) and (entryUrls[0] != ref["url"]):
                print("Oups: conflicting bdsk-url-1 and url fields in {0}".format(refId))
                exit(-1)
                
        # Creating output
        output[refId] = { "_type" : ref["ENTRYTYPE"] }
        for key, value in ref.items():
            output[refId][key] = value
            
        if len(entryUrls):
            output[refId]["url"] = entryUrls[0]

        if len(entryFiles):
            output[refId]["file"] = ";".join([":{0}:{1}".format(f,t) for f,t in entryFiles])
                
# Rendering output
for entry, fields in output.items():
        print("@{0}{{{1},".format(fields["_type"], entry))
        for key, value in [(key, value) for (key, value) in fields.items() if not key in skipFields]:
                print("\t{0}{1}= {{{2}}},".format(key, " "*(16-len(key)), value)) 
        print("}\n")
        

        

        
