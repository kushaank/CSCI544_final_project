#generate input trees for graphviz from SLR dependecies

import csv, os, glob, unicodedata, pygraphviz as pgv

# get the list of the files that have potential useful information based on predicates
os.chdir('..\..\DataFiles\\2014\\05\\19')
with open('finalPredicates3cols.csv') as datafilelist:
	reader = csv.reader(datafilelist, delimiter=",")
	filesList = list(reader)

# lambda function to add SRL to the lasbels
SRL_add = lambda a: ' ' if a=='_' else '_'+a

# os.chdir('SRLTreesVerbs')
listOfVerbs=[' allow.01', ' believe.01', ' blame.01', ' charge.01', ' claim.01', ' congratulate.01', ' evacuate.01', ' help.01', ' join.01', ' kill.01', ' leave.01', ' sign.01', ' strengthen.01', ' summon.01', ' support.01', ' suspend.01', ' target.01', ' threaten.01', ' urge.01', ' warn.01']
for verb in listOfVerbs:
	if not os.path.exists('SRLTreesVerbs\\'+verb.strip()):
		os.makedirs('SRLTreesVerbs\\'+verb.strip())
	infoFilesList=[]
	for line in filesList:
		if line[0].strip()!=line[2].strip() and line[-1].strip() not in infoFilesList and line[1]==verb:
			partNum=int(int(line[-1].strip()[8:])/600)+1
			filePath='ClearnlpOutput\Part'+str(partNum)+'\\'+line[-1].strip()+'.txt.srl'
			if os.path.exists(filePath):
				infoFilesList.append(filePath)

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
			pdfName='SRLTreesVerbs\\'+verb.strip()+'\\'+newsFileName.split('\\')[-1][:-8]+'_Sent'+str(newsSentences.index(sentence))+'.pdf'
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
			treeGraph.graph_attr['label']='File'+pdfName.split('\\')[-1][8:-4]+verb.strip()+'_'+verb.strip()+'\n'+sentenceText
			if verb.strip()[:-3] in sentenceText:
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

