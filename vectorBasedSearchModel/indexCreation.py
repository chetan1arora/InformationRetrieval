# Static Indexing

#OS libraries
import os,sys
import operator
#NLP library used
import nltk
# nltk.download('punkt')
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+|\S+-')

#HTML parsing library
import bs4

#Pickling library
import pickle

#Finding outliers
from scipy import stats


# Source from multiple documents
# # Main memory storing with compression

#Main memory contents

invertedIndex = {}
docSet = {}
# word: list of Docs mapping

def truncateList(invertedIndex):
	# count = len(invertedIndex.keys())
	# s = 0
	# for x in invertedIndex:
	# 	s += len(invertedIndex[x])
	# av = int(s/count)
	# print(av)
	lenArray = [len(invertedIndex[x]) for x in invertedIndex]
	z = stats.zscore(lenArray)

	threshold = 3
	inliers = [lenArray[i] for i in range(len(lenArray)) if z[i]<threshold]
	maxValue = max(inliers)
	print(maxValue)
	print("Num of lists truncated"+str(len(invertedIndex.keys())-len(inliers)))
	for x in invertedIndex:
		invertedIndex[x] = invertedIndex[x][:2000+1]
	return invertedIndex

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
		listOfWords = tokenizer.tokenize(doc.getText().lower())
		# listOfWords =  [x for x in regexp_tokenize(doc.getText().lower(),r'[?"\'\s(),.&\-]', gaps=True) if x not in ('',' ')]
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

invertedIndex = truncateList(invertedIndex)


f = open('docTitles','wb')
pickle.dump(docSet,f)
f.close()


f = open('postingLists','wb')
pickle.dump(invertedIndex,f)
# f.write(invertedIndex)
f.close()


