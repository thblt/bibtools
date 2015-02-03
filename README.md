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

## mkcover.py

## pmiddump.py

## spring2bib.py
