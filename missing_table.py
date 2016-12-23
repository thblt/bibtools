import os, re, subprocess, sys
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import author as bpAuthor, editor as bpEditor

def valnot(entry, key): # Value or Nothing
	if key in entry.keys():
		return entry[key]
	return " "

if len(sys.argv) < 2:
	print("Usage: {0} in.bib [in2.bib...]".format(sys.argv[0]))
	exit(-1)

bibs = []
for file in sys.argv[1:]:
	bibs.append (BibTexParser(open(file, 'r')).get_entry_dict())

for bib in bibs:
	for key, entry in bib.items():
		if entry["type"] == "article":
			if not "bdsk-file-1" in entry:
				print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}".format(valnot(entry, "author"), valnot(entry, "title"), valnot(entry, "year"), valnot(entry, "journal"), valnot(entry, "volume"), valnot(entry, "number"), valnot(entry, "pages")))
