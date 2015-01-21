#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4

from bibtexparser.bparser import BibTexParser
import os, sys

if len(sys.argv) < 3:
	print("Usage: {0} file1.bib file2.bib [...file.bib]".format(sys.argv[0]))
	exit(-1)
	
files = dict()
	
for fn in set( [ os.path.abspath(x) for x in sys.argv[1:] ] ):
	print("Reading {0}.".format(fn))
	files[fn] = BibTexParser(open(fn, 'r')).get_entry_dict().keys()

for fn, keys in files.items():
	dups = dict()
	
	for fn2, keys2 in files.items():
		if fn==fn2: continue
		
			
	