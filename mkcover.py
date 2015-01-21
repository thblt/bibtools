import os, re, subprocess, sys
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import author as bpAuthor, editor as bpEditor
from jinja2 import Environment, FileSystemLoader
from tempfile import TemporaryDirectory

if len(sys.argv) < 2:
	print("Usage:\n\t{0} file.bib [...file2.bib]".format(sys.argv[0]))
	exit(-1)
	
matcher = re.compile('[A-Za-z\-\d:]+')
ignore = ['cite']

# Prepare Jinja2 template compiler

LATEX_SUBS = (
    (re.compile(r'\\'), r'\\textbackslash'),
    (re.compile(r'([{}_#%&$])'), r'\\\1'),
    (re.compile(r'~'), r'\~{}'),
    (re.compile(r'\^'), r'\^{}'),
    (re.compile(r'"'), r"''"),
    (re.compile(r'\.\.\.+'), r'\\ldots'),
)

def escape_tex(value):
	newval = value
	for pattern, replacement in LATEX_SUBS:
		newval = pattern.sub(replacement, newval)
	return newval

jinja = Environment(loader=FileSystemLoader(os.path.dirname(os.path.realpath(__file__))), extensions= ["jinja2.ext.loopcontrols"])
jinja.block_start_string = '((*'
jinja.block_end_string = '*))'
jinja.variable_start_string = '((('
jinja.variable_end_string = ')))'
jinja.comment_start_string = '((='
jinja.comment_end_string = '=))'
jinja.filters['escape_tex'] = escape_tex

# try:
template = jinja.get_template('mkcover.tex.tpl')
# except Exception as e:
# 	print(e.lineno)
# 	exit(-1)

# Author or editor customization

def names(entry):
	entry = bpAuthor(entry)
	entry = bpEditor(entry)
	
	if "author" in entry.keys():
		entry['author'] = ["\\textsc{"+x[:x.index(',')]+"}"+x[x.index(','):] for x in entry['author']]
	
	
	return entry
# Temp store

tempdir = TemporaryDirectory()

# Main code

bibs = []
for file in sys.argv[1:]:
	bibs.append (BibTexParser(open(file, 'r'), customization=names).get_entry_dict())

batch = 0
entries = dict()

while True:
	line = sys.stdin.readline(-1).strip()
	if not line: 
		if len(entries):
			# Render template
			latex = template.render(entries=entries)
			tmpFile = os.path.join(tempdir.name, str(batch))
			with open(tmpFile+".tex", 'w') as out:
				out.write(latex)
			# Pass to XeLaTeX
			with open(os.devnull, 'w') as fnull:
				subprocess.call(["xelatex", "-interaction=nonstopmode", tmpFile], cwd=tempdir.name, stdout=fnull)
			subprocess.call(["open", tmpFile+".pdf"]) # OSX-specific. Most unixes would use xdg-open, and Windows ???
			
			batch+=1
			entries = dict()
		else:
			print("NOTICE\tNothing to do.")
			
	entryNames = []
	pos = 0
	# Get entry names
	while True:
		match = matcher.search(line, pos)
		if not match: break
		pos = match.span(0)[1]
		if not match.group(0) in ignore:
			entryNames.append(match.group(0))
	
	for entry in entryNames: 
		# Find entry:
		data = None
		for bib in bibs:
			if entry in bib.keys():
				data = bib[entry]
				break
		if data:
			entries[entry] = data
			#@TODO Handle Crossref
		else:
			print("WARN\tNo such entry {0}".format(entry))
			
	