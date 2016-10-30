#generate input trees for graphviz from SLR dependecies

import csv, os, glob, unicodedata, pygraphviz as pgv

# get the list of the files that have potential useful information based on predicates
os.chdir('..\..\DataFiles\\2014\\05\\19')
with open('finalPredicates3cols.csv') as datafilelist:
	reader = csv.reader(datafilelist, delimiter=",")
	filesList = list(reader)
infoFilesList=[]
for line in filesList:
	if line[0].strip()!=line[2].strip() and line[-1].strip() not in infoFilesList:
		partNum=int(int(line[-1].strip()[8:])/600)+1
		filePath='ClearnlpOutput\Part'+str(partNum)+'\\'+line[-1].strip()+'.txt.srl'
		if os.path.exists(filePath):
			infoFilesList.append(filePath)

# lambda function to add SRL to the lasbels
SRL_add = lambda a: ' ' if a=='_' else '_'+a

# generate the tree visualization files
for newsFileName in infoFilesList:
	with open(newsFileName) as semanticFile:
		reader = csv.reader(semanticFile, delimiter="\t")
		data = list(reader)
	i=0
	newsSentences=[]
	while i<len(data):
		sentence=[]
		while data[i]!=[]:
			sentence.append(data[i])
			i=i+1
		i=i+1
		newsSentences.append(sentence)
	for sentence in newsSentences:
		pdfName='SRLTrees\\'+newsFileName.split('\\')[-1][:-8]+'_Sent'+str(newsSentences.index(sentence))+'.pdf'
		treeGraph=pgv.AGraph(strict=False,directed=True)
		sentenceText=''
		for item in sentence:
			sentenceText+=item[1].decode('utf8', 'ignore')+' '
			if item[5]!=0:
				parentNode=sentence[int(item[-3])-1][0]+'_'+sentence[int(item[-3])-1][1].decode('utf8', 'ignore')+SRL_add(sentence[int(item[-3])-1][-1])
				try:
					treeGraph.add_edge(parentNode,item[0]+'_'+item[1].decode('utf8', 'ignore')+SRL_add(item[-1]))
				except:
					pass
		treeGraph.layout(prog='dot')
		treeGraph.graph_attr['label']='File'+pdfName[17:-4]+'\n'+sentenceText
		treeGraph.draw(pdfName)
		print pdfName







# get the list of all srl files, in different Part folders
# parts=glob.glob('ClearnlpOutput\Part*')
# srlFiles=[]
# for part in parts:
# 	os.chdir(part)
# 	partFiles=glob.glob('newsText*.txt.srl*')
# 	partFiles=[part+'\\'+filename for filename in partFiles]
# 	srlFiles+=partFiles
# 	os.chdir('..\..')

