# Static Indexing

#OS libraries
import os,sys
import operator
import math

#NLP library used
import nltk

nltk.download('punkt')
nltk.download('stopwords')

# Regular Expression tokenizer
from nltk import regexp_tokenize
# Removing Stopwords
from nltk.corpus import stopwords

#HTML parsing library
import bs4

#Storing to disk using pickle
import pickle

#Main memory
invertedIndex = {}
docSet = {}
sw = dict.fromkeys(stopwords.words("english"),True)
base = 10
numWiki = 25

def addWiki(wikiPath, invertedIndex,docSet):
	f=open(wikiPath,'r')
	unparsedData = f.read()
	f.close()

	#Parsing Data using BeautifulSoup

	soupData = bs4.BeautifulSoup(unparsedData,features="html.parser")
	docList = soupData.select('doc')

	# Separately process each document
	for doc in docList:
		docId = int(doc.get('id'))
		listOfWords =  [x for x in regexp_tokenize(doc.getText().lower(),r'[?"\s(),.&–\-]', gaps=True) if x not in ('',' ')]
		dist = nltk.FreqDist(listOfWords)
		norm = 0
		for word in dist:
			if(word in sw):
				continue
			if word not in invertedIndex:	
				invertedIndex[word] = []
			invertedIndex[word].append((dist[word], docId))
			norm += math.pow(1 + math.log(dist[word],base),2)
		norm = math.pow(norm,-0.5)
		docSet[docId] = (doc.get('title'),norm)

wikiList = []
for i in range(numWiki):
	temp = str(i)
	if(len(temp) == 1):
		temp = '0'+temp
	wikiList.append('AA/wiki_'+temp)

print("Processing "+str(numWiki)+" wikis from AA...")
print("")
for wiki in wikiList:
	addWiki(wiki,invertedIndex,docSet)
	print("[+]Processed "+wiki)

# Writing to disk
print("\nWriting to Disk....")

f = open('docTitles','wb')
pickle.dump(docSet,f)
f.close()


f = open('postingLists','wb')
pickle.dump(invertedIndex,f)
# f.write(invertedIndex)
f.close()
print("Done!!")

