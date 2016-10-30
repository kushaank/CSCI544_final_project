import re, os, glob,inspect
print('Editing files in '+os.getcwd()[26:])
properEOL=['.', ',', ';', '!', '"', '\'']
excludeTerms=['Notes:', 'Comments:', 'See also:', 'Credit:', 'http://', '# comments', 'Click here', '!!', 'commentConfig:', '\xe2', '|', '~', '\xc2', '\xef', '\xe2', '\xce']
emailRegExp=re.compile('[\S\s]*[\w]+@[\w]+\.[\w]+[\S\s]*')

fileToWriteNames=open('stanfordNlpFileList.lst', 'w+')
fileToWriteNames.truncate()

allFileNames=glob.glob("newsText*.txt")
for newsFileName in allFileNames:
	print newsFileName
	editedNews=' '
	with open(newsFileName) as newsFile:
		if os.stat(newsFileName)[6]!=0:
			for line in newsFile:
				if len(line)>2 and line[-4:-1]!='...':
					if line[-2] in properEOL:
						if emailRegExp.match(line)!=None: # if emailRegExp is in the line
							continue
						else:
							flag=False
							for st in excludeTerms:
								if st in line:
									flag=True
									break
							if not flag:
								editedNews=editedNews+'\n'+line
	fileToWrite=open(newsFileName, 'w+')
	fileToWrite.truncate()
	fileToWrite.write(editedNews)
	fileToWrite.close()
	fileToWriteNames.write("%s\n" %newsFileName)
fileToWriteNames.close()