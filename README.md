# bibtools

This repository contains a set of mostly standalone Python scripts operating on BibTex databases. They almost all depend on [the bibtexparser package](https://pypi.python.org/pypi/bibtexparser/0.6.0).

These scripts have been written for my own use, and depend heavily on the database schema, and sometimes even keywords, I use. They're not a "scripting BibTex" suite.

## chkpages.py

Insure that the Pages field is made of either a single number (```\d+```) or a pair of numbers separated by exactly two dashes: ```\d+\-\-\d+```. In this second case, it also insures that the second number is greater than the first.

It reports a list of non-conforming entries.

## dc2bib.py

## find_dup_keys.py

Identifies duplicate keys accross multiple .bib files.

## find_dup_titles.py

Find duplicated titles in a BibTeX file. Somehow eases the process of finding duplicates.

## hathidl.py

Sorry, top secret, not commited.

## missing_table.py

Used to print a list of article I still need to find a PDF version of. Technically, it lists the entries of type ```article```s with no ```Bdsk-File-1``` field. ```Bdsk-File-1``` is a [BibDesk][bibdesk]-specific field. It is a base64-encoded plist and [provides a better mechanism for linking entries to external files](http://bibdesk-users.661331.n2.nabble.com/Path-implications-when-sharing-bib-files-with-Bdsk-File-1-entries-td661338.html), usually PDFs.

## mkcover.py

Generates standard covers in LaTeX from notices. Probably useless.

## pmiddump.py

Simple regex script to extract PMIDs from random strings.

## spring2bib.py

Converts SpringerLink URLs to BibTeX entries.

[bibdesk]: http://bibdesk.sourceforge.net/

