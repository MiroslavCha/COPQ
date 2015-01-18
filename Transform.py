from Tkinter import *
from tkFileDialog import *
import string
import json
import codecs
import io

global file

def callbackJson():
	fileName = askopenfilename(parent=root, filetypes = (("json files", "*.js"), ("All files", "*.*")))	
	if fileName:
		with codecs.open(fileName, encoding='utf-8', mode='r') as f:
			read_data = f.read()
		f.closed
		parseJson(read_data)
	
def callbackExcel():
	fileName = askopenfilename(parent=root, filetypes = (("Comma separated value", "*.csv"), ("All files", "*.*")))	
	if fileName:
		with codecs.open(fileName, encoding='utf-8', mode='r') as f:
			read_data = f.read()
		f.closed
		parseCsv(read_data)

def parseCsv(data):	
	lines = data.split('\n')
	lines = filter(bool, lines)	

	for i in range(0, len(lines)):
		lines[i] = lines[i].strip("\r")	
	
	print 'Found {0} lines'.format(len(lines) - 1)
		
	delimiter = ';'
		
	languages = lines[0].split(delimiter)	
	languages = filter(bool, languages)	
	
	print "Translating to", len(languages) - 1, "languages"	
		
	trans = {}
	lin = 0
	wrong = 1
	
	for i in range(1, len(lines)):		
		words = lines[i].split(delimiter)		
		words = filter(bool, words)	
		dict = {}		
		
		if len(words) == len(languages):
			lin = lin + 1
			for j in range(1, len(languages)):
								
				dict.update({languages[j]: words[j]})
		
			trans[words[0]] = dict;
		else:
			print wrong, "Can't tanslate " + lines[i]
			wrong = wrong + 1

	textJson = json.dumps(trans, ensure_ascii=False)
	
	textJson = textJson.replace("},", "},\n")

	textJson = "translations = " + textJson
	
	with io.open('labels.js', 'w', encoding='utf8') as json_file:    		
		json_file.write(textJson)		
	
	json_file.close()
	
	print lin, " records translated"

	return 0
		
def parseJson(data):
	if len(data) < 15:
		return -1
		
	#remove TRANSLATION string which mangle json format
	data = data[15:]
	dict = json.loads(data)
	csv = "id"
	
	itemKey, itemValue = dict.popitem()
		
	#csv delimiter
	delimiter = ";"
	
	#create csv header
	for lan, tran in itemValue.iteritems():
		csv = csv + delimiter + lan
			
	csv += '\n'		
	
	dict[itemKey] = itemValue
	
	#create records
	for id, translation in dict.iteritems():	
		csv = csv + id
		for lan, langTrans in translation.iteritems():
			csv = csv + delimiter + langTrans
		csv += '\n'			

	print csv
	
	text_file = codecs.open('out.csv', encoding='utf_8', mode='w+')
	text_file.write(csv)
	text_file.close()
	
	return 0
	
root = Tk()
root.wm_title("COPQ translation converter")

w = Label(root, text="Please choose a file to convert.") 

b1 = Button(text='Choose a Json file', state=DISABLED, command=callbackJson).pack(fill=X)
b2 = Button(text='Choose a Excel-csv file', command=callbackExcel).pack(fill=X)

w.pack()
root.mainloop()