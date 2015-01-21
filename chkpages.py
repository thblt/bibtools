import os, re, subprocess, sys
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import author as bpAuthor, editor as bpEditor
from jinja2 import Environment, FileSystemLoader
from tempfile import TemporaryDirectory

if len(sys.argv) < 2:
	print("Usage:\n\t{0} file.bib [...file2.bib]".format(sys.argv[0]))
	exit(-1)
	
matcher = re.compile('^([0-9]+)(\-\-[0-9]+)?$')

tempdir = TemporaryDirectory()

# Main code

for file in sys.argv[1:]:
	refs = (BibTexParser(open(file, 'r')).get_entry_dict())
	for id, ref in refs.items():
		if "pages" in ref:
			if not matcher.match(ref["pages"]):
				print(file, id, ref["pages"])