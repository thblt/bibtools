# bibtools

This repository contains a set of mostly standalone Python scripts operating on BibTex databases. They almost all depend on [the bibtexparser package](https://pypi.python.org/pypi/bibtexparser/0.6.0).

These scripts have been written for my own use, and depend heavily on the database schema, and sometimes even keywords, I use. They're not a "scripting BibTex" suite.

## chkpages.py

Insure that the Pages field is made of either a single number (```\d+```) or a pair of numbers separated by exactly two dashes: ```\d+\-\-\d+```. In this second case, it also insures that the second number is greater than the first.

It reports a list of non-conforming entries.

## dc2bib.py

## find_dup_keys.py

## find_dup_titles.py

## hathidl.py

Sorry, top secret, not commited.

## missing_table.py

Generate a list of ```article```s with no ```Bdsk-File-1``` field. ```Bdsk-File-1``` is a [BibDesk][bibdesk]-specific field. It is a base64-encoded plist and provides a better mechanism[^bdskfile1] for holding link to external files, usually PDFs.

## mkcover.py

Generates standard covers in LaTeX from notices. Probably useless. I use them 

## pmiddump.py

Simple regex script to extract PMIDs from random strings.

## spring2bib.py

Converts SpringerLink URLs to BibTeX entries.

[bibdesk]: 

[^bdskfile1]: 
	> To be precise, it's a base64 encoded (keyed) archived dictionary containing a relative path and a file alias (an alias stores a full path and a file ID). It is designed to support a large range of storage procedures, as it can find a file by relative path, absolute  path, and file ID (in that order). This means that you can 
	
	- move/rename the .bib file (as it stores full paths) 
	- move/rename a linked file (as it stores file IDs) 
	- move the .bib file and linked files together (as it stores relative   
	paths) 
	- copy the .bib file and linked files togther, even between different   
	machines (as it stores relative paths) 
	