#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4

from bibtexparser.bparser import BibTexParser
import os, sys

if len(sys.argv) != 2:
	print("Usage: {0} file.bib".format(sys.argv[0]))
	exit(-1)
	
	
files = BibTexParser(open(sys.argv[1], 'r')).get_entry_dict()

titles = set()

for key, fields in files.items():
	title = fields["title"]
	if title in titles: continue
	titles.add(title)
	count = 0
	for key2, fields2 in files.items():
		if fields2["title"] == title:
			count += 1
	
	if count > 1:
		print("{1} occurencess of:\t{0}".format(title, count))
			
	
		
			
	