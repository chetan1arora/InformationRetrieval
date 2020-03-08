# Static Indexing

#OS libraries
import os,sys
import operator
#NLP library used
import nltk
# nltk.download('punkt')
from nltk import regexp_tokenize

#HTML parsing library
import bs4

#Pickling library
import pickle


# Source from multiple documents
# # Main memory storing with compression

#Main memory contents

invertedIndex = {}
docSet = {}
# word: list of Docs mapping

def addWiki(wikiPath, invertedIndex,docSet):
	f=open(wikiPath,'r')
	unparsedData = f.read()
	f.close()

	#Parsing Data using BeautifulSoup

	soupData = bs4.BeautifulSoup(unparsedData,features="html.parser")
	docList = soupData.select('doc')

	# Separately process each document
	# data = [doc.getText().lower() for doc in docList]
	for doc in docList:
		docId = int(doc.get('id'))
		docSet[docId] = doc.get('title')
		listOfWords = []
		listOfWords =  [x for x in regexp_tokenize(doc.getText().lower(),r'[?"\'\s(),.&\-]', gaps=True) if x not in ('',' ')]
		dist = nltk.FreqDist(listOfWords)
		for word in dist:
			if(word not in invertedIndex):
				invertedIndex[word] = []
			invertedIndex[word].append((dist[word], docId))

wikiList = []
for i in range(25):
	temp = str(i)
	if(len(temp) == 1):
		temp = '0'+temp
	wikiList.append('AA/wiki_'+temp)


for wiki in wikiList:
	print("[+]Processing "+wiki)
	addWiki(wiki,invertedIndex,docSet)


f = open('docTitles','wb')
pickle.dump(docSet,f)
f.close()


f = open('postingLists','wb')
pickle.dump(invertedIndex,f)
# f.write(invertedIndex)
f.close()


