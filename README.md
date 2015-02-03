# bibtools

This repository contains a set of mostly standalone Python scripts operating on BibTex databases. They almost all depend on [the bibtexparser package](https://pypi.python.org/pypi/bibtexparser/0.6.0)

## chkpages.py

Insure that the Pages field is made of either a single number (```\d+```) or a pair of numbers separated by exactly two dashes: ```\d+\-\-\d+```. In this second case, it also insures that the second number is greater than the first.

It reports a list of non-conforming entries.
