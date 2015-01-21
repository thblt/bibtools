import fileinput, re

r = re.compile("PMID?.*?(\d+)")
pmids = set()

for line in fileinput.input():
	pmids.update(r.findall(line))

print(' '.join(pmids))
print("Ok")