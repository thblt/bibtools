# Reads SpringerLink URLs from stdin then:
#   - Generates a BibTex file containing formatted references.
#   - Stores all PDF in current directory, linking them from the BibTex file. 

import os, re, sys
from hashlib import sha1 as hashfunc
from urllib.request import urlopen, url2pathname
from urllib.parse import unquote
from html.parser import HTMLParser
from http.client import HTTPConnection

class SpringerExtractor(HTMLParser):

	translations = {"citation_volume": "Volume",
					"citation_issue": "Number",
					"citation_journal_title": "Journal",
					"citation_journal_abbrev": "Shortjournal",
					"citation_author": "Author",
					"citation_date": "_Date",
					"citation_publication_date": "_Date",
					"citation_title": "Title",
					"citation_language": "Hyphenation",
					"citation_firstpage": "_FirstPage",
					"citation_lastpage": "_LastPage",
					"citation_pdf_url" : "_FileUrl"
					}
	
	def meta(self, name, value):
		if name in self.translations:
			translated = self.translations[name]
			if translated in self.data:
				if not type(self.data[translated]) is list:
					self.data[translated] = [ self.data[translated] ]
				self.data[translated].append(value)
			else:	
				self.data[translated] = value
	
	def handle_starttag(self, tag, attrs):
		attrs = dict(attrs)
		if tag=="meta" and ("name" in attrs) and ("content" in attrs):
			# print(attrs)
			self.meta(attrs["name"], attrs['content'])
				
	def __init__(self):
		HTMLParser.__init__(self)
		self.data = { "Author": []}
	# def handle_endtag(self, tag):
	# 	print("END\t", tag)
	# 	
	# def handle_data(self, data):
	# 	print("DATA\t", data)
	# 	self.data = data

# Latex escape code from http://flask.pocoo.org/snippets/55/

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
	
#  End stolen code 

def download(url):
	#print("DOWN\t", url)
	i = urlopen(url)
	data = i.read()
	extension = os.path.splitext(url2pathname(i.geturl()))[1]
	name = hashfunc(url.encode("utf-8")).hexdigest() + extension
	
	with open(name, 'wb') as outfile:
		outfile.write(data)
	
	return os.path.abspath(name)
	
outCount = 0
def writeBibTex(f, data):
	global outCount

	# Authors
	data["Author"] = " and ".join(data["Author"])
	# Pages
	if ("_FirstPage" in data) and ("_LastPage" in data):
		if data["_FirstPage"] == data["_LastPage"]:
			data["Pages"] = data["_FirstPage"]
		else:
			data["Pages"] = "{0}--{1}".format(data["_FirstPage"], data["_LastPage"])
			
		del data["_FirstPage"], data["_LastPage"]
	# Date
	if ("_Date" in data) and not ("Year" in data):
		data["Year"] = data["_Date"][0:4]
		del data["_Date"]
	# File
	if "_FileUrl" in data:
		data["Local-Url"] = download(unquote(data["_FileUrl"]))
		del data["_FileUrl"]
		
	outCount += 1
	outfile.write("@article{{springer2Bib_tmp_{0},\n".format(outCount))
	for k, v in data.items():
		outfile.write("\t{0} = {{ {1} }},\n".format(k, escape_tex(v)))
	outfile.write("\t}\n\n")

##############
# Here we go #
##############

if len(sys.argv) != 2:
	print("Usage:\n\t{0} outputfile.bib".format(sys.argv[0]))
	exit(-1)

with open(sys.argv[1], 'w') as outfile:
	
	skip = 0	
	
	while(True):
		try:
			url = sys.stdin.readline().strip()
			if not url: 
				skip +=1
				if skip < 3:
					print("{0} more empty line{1} to exit.".format(3-skip, "s" if 3-skip>1 else ""))
				else:
					break
				continue


			skip = 0
		
			record = dict()
			x = SpringerExtractor()
			x.feed(urlopen(url).read().decode("utf-8"))
			writeBibTex(outfile, x.data)
			del x
			print("OK")
		except Exception as e:
			print("ERROR\tCan't handle URL: "+str(e))
			continue